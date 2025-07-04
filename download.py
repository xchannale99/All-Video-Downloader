import os
import sys
from termcolor import cprint, colored
from pytube import YouTube
import yt_dlp

# Set up download directory
SAVE_DIR = os.path.expanduser("~/dw")
os.makedirs(SAVE_DIR, exist_ok=True)

def banner():
    cprint("==========================================", "cyan")
    cprint("   VIDEO DOWNLOADER BY HRIDOY HASAN MISHOR", "green", attrs=["bold"])
    cprint("==========================================\n", "cyan")

def select_quality():
    qualities = ["720p", "480p", "360p", "240p", "144p"]
    cprint("Select video quality:", "yellow")
    for i, q in enumerate(qualities, 1):
        print(f"{i}. {q}")
    choice = input(colored("Enter choice (1-5): ", "cyan"))
    return qualities[int(choice)-1] if choice in map(str, range(1, 6)) else "360p"

def download_youtube():
    link = input(colored("Enter YouTube Video URL: ", "yellow"))
    try:
        yt = YouTube(link)
        quality = select_quality()
        stream = yt.streams.filter(res=quality, progressive=True, file_extension="mp4").first()
        if stream:
            cprint(f"📥 Downloading in {quality}...", "green")
            stream.download(SAVE_DIR)
            cprint("✅ Download complete!", "green")
        else:
            cprint("⚠️ Desired quality not found. Downloading best available...", "red")
            yt.streams.get_highest_resolution().download(SAVE_DIR)
            cprint("✅ Fallback download complete!", "green")
    except Exception as e:
        cprint(f"❌ Error: {e}", "red")

def download_with_ytdlp(url, quality):
    ydl_opts = {
        'outtmpl': os.path.join(SAVE_DIR, '%(title)s.%(ext)s'),
        'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
        'quiet': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        cprint("✅ Download complete!", "green")
    except Exception as e:
        cprint(f"❌ Error: {e}", "red")

def download_facebook():
    link = input(colored("Enter Facebook Video URL: ", "yellow"))
    quality = select_quality().replace("p", "")
    download_with_ytdlp(link, quality)

def download_tiktok():
    link = input(colored("Enter TikTok Video URL: ", "yellow"))
    quality = select_quality().replace("p", "")
    download_with_ytdlp(link, quality)

def main():
    while True:
        banner()
        cprint("1. Download YouTube Video", "blue")
        cprint("2. Download Facebook Video", "blue")
        cprint("3. Download TikTok Video", "blue")
        cprint("4. Exit", "blue")
        choice = input(colored("Select option (1-4): ", "cyan"))

        if choice == "1":
            download_youtube()
        elif choice == "2":
            download_facebook()
        elif choice == "3":
            download_tiktok()
        elif choice == "4":
            cprint("👋 Exiting. Thank you!", "yellow")
            sys.exit()
        else:
            cprint("❌ Invalid option! Try again.", "red")

        input(colored("\n🔁 Press Enter to return to menu...", "magenta"))

if __name__ == "__main__":
    main()
