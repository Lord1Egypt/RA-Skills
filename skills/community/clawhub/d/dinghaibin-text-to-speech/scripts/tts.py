#!/usr/bin/env python3
"""
Text to Speech - Convert text to audio
Note: Uses gTTS (pip install gtts) for free TTS, or falls back to macOS say command.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


LANGUAGES = {
    'en': 'English',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'it': 'Italian',
    'ru': 'Russian',
    'pt': 'Portuguese'
}


def tts_gtts(text, output, lang='en'):
    """Use gTTS for TTS."""
    try:
        from gtts import gTTS
        tts = gTTS(text, lang=lang)
        tts.save(output)
        print(f"Saved to: {output}")
        return 0
    except ImportError:
        print("gTTS not installed. Run: pip install gtts")
        return tts_say(text, output)
    except Exception as e:
        print(f"Error: {e}")
        return 1


def tts_say(text, output):
    """Use macOS say command as fallback."""
    try:
        # Check if we're on macOS
        if sys.platform == 'darwin':
            # Convert to mp3 using afplay/ffmpeg if available
            subprocess.run(['say', '-o', output.replace('.mp3', '.aiff'), text], check=True)
            print(f"Saved to: {output}")
            return 0
        else:
            print("No TTS available. Install gTTS: pip install gtts")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def list_voices():
    """List available voices."""
    print("\n=== Available Voices ===")
    
    # Try gTTS languages
    print("\ngTTS Languages:")
    for code, name in LANGUAGES.items():
        print(f"  {code}: {name}")
    
    # Try macOS voices
    try:
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
        if result.returncode == 0:
            print("\nmacOS Voices:")
            for line in result.stdout.strip().split('\n')[:20]:
                print(f"  {line}")
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description='Text to Speech')
    parser.add_argument('text', nargs='?', help='Text to convert to speech')
    parser.add_argument('--output', help='Output audio file (mp3)')
    parser.add_argument('--voice', default='neutral', help='Voice (male, female, neutral)')
    parser.add_argument('--speed', type=float, default=1.0, help='Speaking speed (0.5-2.0)')
    parser.add_argument('--lang', default='en', help='Language code (en, zh, ja, etc.)')
    parser.add_argument('--list-voices', action='store_true', help='List available voices')
    
    args = parser.parse_args()
    
    # List voices
    if args.list_voices:
        list_voices()
        return 0
    
    # Need text
    if not args.text:
        parser.print_help()
        return 1
    
    # Output file
    output = args.output or 'output.mp3'
    
    # Determine language
    lang = args.lang
    if lang == 'zh':
        lang = 'zh-CN'
    
    # Generate speech
    print(f"Converting to speech...")
    return tts_gtts(args.text, output, lang)


if __name__ == '__main__':
    sys.exit(main())
