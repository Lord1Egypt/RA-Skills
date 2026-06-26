#!/usr/bin/env python3
"""
Video Downloader - Download videos from YouTube and other platforms
Note: Requires yt-dlp (pip install yt-dlp)
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """Check if yt-dlp is installed."""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        return True
    except:
        return False


def install_yt_dlp():
    """Install yt-dlp."""
    print("Installing yt-dlp...")
    try:
        subprocess.run(['pip', 'install', 'yt-dlp'], check=True)
        return True
    except:
        print("Error: Could not install yt-dlp")
        return False


def list_formats(url):
    """List available formats."""
    try:
        cmd = ['yt-dlp', '--list-formats', url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def download_video(url, output=None, format_spec=None, quality=None, audio_only=False):
    """Download video."""
    cmd = ['yt-dlp']
    
    # Output template
    if output:
        cmd.extend(['-o', output])
    else:
        cmd.extend(['-o', '%(title)s.%(ext)s'])
    
    # Format
    if audio_only:
        cmd.extend(['-x', '--audio-format', 'mp3'])
    elif format_spec:
        cmd.append(f'--format={format_spec}')
    elif quality:
        quality_map = {
            '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        }
        cmd.append(f'--format={quality_map.get(quality, quality)}')
    
    cmd.append(url)
    
    try:
        print(f"Downloading: {url}")
        result = subprocess.run(cmd)
        return result.returncode
    except Exception as e:
        print(f"Error: {e}")
        return 1


def get_video_info(url):
    """Get video metadata."""
    try:
        cmd = ['yt-dlp', '--dump-json', '--no-download', url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        import json
        data = json.loads(result.stdout)
        print(f"Title: {data.get('title', 'N/A')}")
        print(f"Duration: {data.get('duration', 'N/A')} seconds")
        print(f"Uploader: {data.get('uploader', 'N/A')}")
        print(f"View count: {data.get('view_count', 'N/A')}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='Video Downloader')
    parser.add_argument('url', nargs='?', help='Video URL')
    parser.add_argument('--output', help='Output path')
    parser.add_argument('--format', help='Video format (mp4, webm)')
    parser.add_argument('--quality', help='Quality (best, 1080p, 720p, 480p)')
    parser.add_argument('--audio-only', action='store_true', help='Extract audio only')
    parser.add_argument('--list-formats', action='store_true', help='List available formats')
    parser.add_argument('--info', action='store_true', help='Show video info')
    
    args = parser.parse_args()
    
    # Check dependencies
    if not check_dependencies():
        if not install_yt_dlp():
            return 1
    
    # Need URL
    if not args.url:
        parser.print_help()
        return 1
    
    # List formats
    if args.list_formats:
        return list_formats(args.url)
    
    # Get info
    if args.info:
        return get_video_info(args.url)
    
    # Download
    return download_video(
        args.url,
        args.output,
        args.format,
        args.quality,
        args.audio_only
    )


if __name__ == '__main__':
    sys.exit(main())
