#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bilibili Video Upload Skill
Usage: python upload.py <video_path> --title "Title" --desc "Description" --tags "tag1,tag2" --tid 138
"""

import argparse
import subprocess
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='Upload video to Bilibili')
    parser.add_argument('video_path', help='Full path to video file')
    parser.add_argument('--title', required=True, help='Video title')
    parser.add_argument('--desc', default='', help='Video description')
    parser.add_argument('--tags', default='', help='Comma-separated tags')
    parser.add_argument('--tid', type=int, default=138, help='Partition ID (default: 138=日常)')
    
    args = parser.parse_args()
    
    # Expand user path if ~ is used
    video_path = os.path.abspath(os.path.expanduser(args.video_path))
    
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        sys.exit(1)
    
    # Set UTF-8 encoding for Windows
    if os.name == 'nt':
        os.system('chcp 65001 > nul')
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    print(f"Starting upload: {video_path}")
    print(f"Title: {args.title}")
    
    cmd = [
        'biliup', 'upload',
        '--title', args.title,
        '--desc', args.desc,
        '--tag', args.tags,
        '--tid', str(args.tid),
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Upload completed successfully!")
        print("Note: Video will be visible after Bilibili review.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Upload failed with exit code: {e.returncode}")
        print("\nTroubleshooting:")
        print("1. Make sure you have logged in: run 'biliup login' in terminal")
        print("2. Scan the QR code with Bilibili App to complete login")
        print("3. Check encoding: run 'chcp 65001' before login on Windows")
        return False

if __name__ == '__main__':
    main()
