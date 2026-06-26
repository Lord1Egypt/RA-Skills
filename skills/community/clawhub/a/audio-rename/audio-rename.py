#!/usr/bin/env python3
"""
Audio file renamer - converts Chinese/special char filenames to pure English.
Use this for mlx-stt compatibility when filenames contain non-ASCII characters.

Usage:
    python3 audio-rename.py <file_path>              # rename to video_audio.m4a
    python3 audio-rename.py <file_path> <new_name>   # rename to <new_name>.m4a
    python3 audio-rename.py <dir_path> --all         # batch rename all audio files
"""

import os
import sys

def get_unique_path(base_path):
    """Generate unique filename if target already exists."""
    if not os.path.exists(base_path):
        return base_path
    
    dir_name = os.path.dirname(base_path)
    filename = os.path.basename(base_path)
    name, ext = os.path.splitext(filename)
    
    counter = 1
    while True:
        new_path = os.path.join(dir_name, f"{name}_{counter}{ext}")
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def rename_file(file_path, new_name="video_audio"):
    """Rename a single audio file."""
    if not os.path.isfile(file_path):
        print(f"❌ Error: File '{file_path}' not found")
        return False
    
    dir_path = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    _, ext = os.path.splitext(filename)
    
    # Ensure ext starts with dot
    if ext and not ext.startswith('.'):
        ext = '.' + ext
    elif not ext:
        ext = '.m4a'  # default extension
    
    new_filename = f"{new_name}{ext}"
    new_path = os.path.join(dir_path, new_filename)
    new_path = get_unique_path(new_path)
    
    os.rename(file_path, new_path)
    print(f"✅ Renamed: {filename} → {os.path.basename(new_path)}")
    print(f"📁 Location: {new_path}")
    return True

def batch_rename(dir_path):
    """Batch rename all audio files in a directory."""
    if not os.path.isdir(dir_path):
        print(f"❌ Error: '{dir_path}' is not a directory")
        return False
    
    audio_extensions = {'.m4a', '.mp3', '.wav', '.flac', '.aac', '.ogg'}
    counter = 1
    
    for filename in sorted(os.listdir(dir_path)):
        _, ext = os.path.splitext(filename)
        if ext.lower() not in audio_extensions:
            continue
        
        old_path = os.path.join(dir_path, filename)
        if not os.path.isfile(old_path):
            continue
        
        new_filename = f"audio_{counter:03d}{ext}"
        new_path = os.path.join(dir_path, new_filename)
        new_path = get_unique_path(new_path)
        
        os.rename(old_path, new_path)
        print(f"✅ {filename} → {new_filename}")
        counter += 1
    
    print("✅ Batch rename complete!")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <file_path> [new_name]")
        print(f"  {sys.argv[0]} <dir_path> --all")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    if len(sys.argv) > 2 and sys.argv[2] == "--all":
        batch_rename(input_path)
    elif len(sys.argv) > 2:
        rename_file(input_path, sys.argv[2])
    else:
        rename_file(input_path)

if __name__ == "__main__":
    main()
