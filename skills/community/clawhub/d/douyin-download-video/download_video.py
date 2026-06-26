#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
FFMPEG_DIR = SCRIPT_DIR / "ffmpeg"
if platform.system() == "Windows":
    FFMPEG_EXE = FFMPEG_DIR / "bin" / "ffmpeg.exe"
else:
    FFMPEG_EXE = FFMPEG_DIR / "bin" / "ffmpeg"
OUTPUT_DIR = Path.home() / "Downloads"

def setup_ffmpeg():
    """Download and setup ffmpeg if not already installed"""
    if FFMPEG_EXE.exists():
        print(f"FFmpeg already installed at: {FFMPEG_EXE}")
        return str(FFMPEG_EXE)
    
    print("Downloading FFmpeg...")
    
    if platform.system() == "Windows":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_file = Path(os.environ.get("TEMP", "/tmp")) / "ffmpeg.zip"
        
        try:
            urllib.request.urlretrieve(url, zip_file)
            print("Extracting FFmpeg...")
            
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(zip_file.parent)
            
            extracted_dirs = [d for d in zip_file.parent.iterdir() if d.is_dir() and d.name.startswith("ffmpeg-")]
            if extracted_dirs:
                extracted_dir = extracted_dirs[0]
                FFMPEG_DIR.mkdir(parents=True, exist_ok=True)
                
                for item in extracted_dir.iterdir():
                    dest = FFMPEG_DIR / item.name
                    if dest.exists():
                        if dest.is_dir():
                            shutil.rmtree(dest)
                        else:
                            dest.unlink()
                    shutil.move(str(item), str(dest))
                
                print(f"FFmpeg installed successfully at: {FFMPEG_EXE}")
                return str(FFMPEG_EXE)
            else:
                print("Error: Could not find extracted FFmpeg directory")
                sys.exit(1)
        finally:
            if zip_file.exists():
                zip_file.unlink()
    else:
        print("Auto-installation not supported on this platform. Please install FFmpeg manually.")
        print("Visit: https://ffmpeg.org/download.html")
        sys.exit(1)

def check_ytdlp():
    """Check if yt-dlp is installed, if not, install it"""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        print("yt-dlp is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True)
        print("yt-dlp installed successfully")

def download_video(url, quality="1080p", output_dir=None, audio_only=False):
    """Download video using yt-dlp"""
    
    ffmpeg_path = setup_ffmpeg()
    check_ytdlp()
    
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_template = str(output_dir / "%(title)s.%(ext)s")
    
    cmd = ["yt-dlp", url, "-o", output_template]
    
    if audio_only:
        cmd.extend(["--extract-audio", "--audio-format", "mp3"])
    else:
        if quality == "best":
            format_selector = "bestvideo+bestaudio/best"
        elif quality == "1080p":
            format_selector = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        elif quality == "720p":
            format_selector = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
        elif quality == "480p":
            format_selector = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
        elif quality == "360p":
            format_selector = "bestvideo[height<=360]+bestaudio/best[height<=360]/best"
        else:
            format_selector = "best"
        
        cmd.extend(["-f", format_selector, "--merge-output-format", "mp4"])
    
    cmd.extend(["--ffmpeg-location", ffmpeg_path])
    
    print(f"Downloading video: {url}")
    print(f"Quality: {quality}")
    print(f"Output directory: {output_dir}")
    
    subprocess.run(cmd, check=True)
    print("Download completed!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_video.py <URL> [options]")
        print("\nOptions:")
        print("  -q, --quality <quality>    Video quality (best, 1080p, 720p, 480p, 360p) [default: 1080p]")
        print("  -o, --output <dir>         Output directory [default: ~/Downloads]")
        print("  -a, --audio-only           Download audio only as MP3")
        print("\nExamples:")
        print('  python download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"')
        print('  python download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -q 720p')
        print('  python download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -o "D:/Videos"')
        print('  python download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -a')
        sys.exit(1)
    
    url = sys.argv[1]
    quality = "1080p"
    output_dir = None
    audio_only = False
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] in ["-q", "--quality"]:
            quality = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] in ["-o", "--output"]:
            output_dir = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] in ["-a", "--audio-only"]:
            audio_only = True
            i += 1
        else:
            i += 1
    
    download_video(url, quality, output_dir, audio_only)

if __name__ == "__main__":
    main()
