#!/usr/bin/env python3
"""
audio-processor/scripts/extract_metadata.py
音频元数据提取与编辑
"""

import argparse
import json
import os

from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from mutagen.aac import AAC
from mutagen import File


def extract_metadata(path: str):
    audio = File(path)
    if audio is None:
        print(f"Error: cannot read metadata from {path}")
        return None
    
    info = {
        'file': path,
        'format': type(audio).__name__,
        'duration_sec': round(audio.info.length, 3) if hasattr(audio.info, 'length') else None,
        'sample_rate': audio.info.sample_rate if hasattr(audio.info, 'sample_rate') else None,
        'channels': audio.info.channels if hasattr(audio.info, 'channels') else None,
        'bitrate': audio.info.bitrate if hasattr(audio.info, 'bitrate') else None,
    }
    
    # Tags
    tags = {}
    if hasattr(audio, 'tags') and audio.tags:
        for key, value in audio.tags.items():
            tags[key] = str(value)
    elif hasattr(audio, 'vorbiscomment') and audio.vorbiscomment:
        for key, value in audio.vorbiscomment.items():
            tags[key] = str(value)
    
    info['tags'] = tags
    return info


def edit_metadata(path: str, tags: dict):
    audio = File(path, easy=True)
    if audio is None:
        print(f"Error: cannot edit metadata for {path}")
        return False
    
    for key, value in tags.items():
        audio[key] = value
    audio.save()
    print(f"Updated tags for: {path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Extract or edit audio metadata')
    parser.add_argument('input', help='Input audio file')
    parser.add_argument('--output', '-o', help='Output JSON file for extraction')
    parser.add_argument('--set-tag', '-t', action='append', nargs=2, metavar=('KEY', 'VALUE'),
                        help='Set a tag (e.g. --set-tag title "My Song")')
    parser.add_argument('--list', '-l', action='store_true', help='List all tags')
    args = parser.parse_args()
    
    if args.set_tag:
        tags = {k: v for k, v in args.set_tag}
        edit_metadata(args.input, tags)
    
    info = extract_metadata(args.input)
    if info:
        if args.list or not args.set_tag:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2, ensure_ascii=False)
            print(f"Metadata saved: {args.output}")


if __name__ == '__main__':
    main()
