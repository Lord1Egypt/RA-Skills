#!/usr/bin/env python3
"""
generate-audio.py — Generate audio from script using ElevenLabs TTS

Strips citations from script and converts to speech using configured voice.

Usage:
    generate-audio.py --script script.txt --output episode.mp3 --config config.yaml
"""
import sys
import os
import re
import argparse
from pathlib import Path


def load_config(config_path: str) -> dict:
    """Load config (simplified YAML parser)"""
    with open(config_path) as f:
        content = f.read()
    
    config = {"voice": {}}
    
    # Parse voice section
    voice_match = re.search(r'voice:\s*\n((?:  \w+:.*\n?)*)', content)
    if voice_match:
        for line in voice_match.group(1).split('\n'):
            if ':' in line:
                key, val = line.strip().split(':', 1)
                config["voice"][key.strip()] = val.strip()
    
    return config


def strip_citations(script_text: str) -> str:
    """Remove all citation markers and formatting for clean TTS"""
    clean = script_text
    
    # Remove citation patterns
    clean = re.sub(r'\[Source:\s*[^\]]+\]', '', clean)
    clean = re.sub(r'\[Source:\s*[^\]]+\]', '', clean)  # Catch variants
    
    # Remove structural markers
    clean = re.sub(r'^\[VERIFIED\].*$', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^\[OPEN\].*$', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^\[CLOSE\].*$', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^\[END\].*$', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^\[SECTION \d+:.*$', '', clean, flags=re.MULTILINE)
    
    # Remove citations block
    clean = re.sub(r'^\*\*CITATIONS:\*\*.*?\[END\]', '', clean, flags=re.DOTALL | re.MULTILINE)
    
    # Remove markdown formatting
    clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)  # Bold
    clean = re.sub(r'\*([^*]+)\*', r'\1', clean)      # Italic
    clean = re.sub(r'^---+$', '', clean, flags=re.MULTILINE)  # Horizontal rules
    
    # Clean up whitespace
    clean = re.sub(r'\n\n\n+', '\n\n', clean)  # Multiple blank lines
    clean = clean.strip()
    
    return clean


def main():
    """Main entry point for audio generation preparation"""
    parser = argparse.ArgumentParser(description="Generate audio from podcast script")
    parser.add_argument("--script", required=True, help="Script text file")
    parser.add_argument("--output", required=True, help="Output MP3 file")
    parser.add_argument("--config", required=True, help="Config YAML file")
    args = parser.parse_args()
    
    print(f"=== GENERATING AUDIO ===")
    print(f"Script: {args.script}")
    print(f"Output: {args.output}")
    print()
    
    # Load script
    with open(args.script) as f:
        script_text = f.read()
    
    # Load config
    config = load_config(args.config)
    voice_config = config.get("voice", {})
    
    voice_id = voice_config.get("voice_id", "")
    if not voice_id:
        print("❌ No voice_id configured. Set voice.voice_id in your config.yaml")
        print("   Browse voices at: https://elevenlabs.io/voice-library")
        sys.exit(1)
    model = voice_config.get("model", "eleven_turbo_v2_5")
    
    print(f"Voice ID: {voice_id}")
    print(f"Model: {model}")
    print()
    
    # Strip citations
    clean_text = strip_citations(script_text)
    word_count = len(clean_text.split())
    
    print(f"Original length: {len(script_text.split())} words")
    print(f"Clean TTS text: {word_count} words")
    print()
    
    # Save clean text
    tts_file = args.output.replace('.mp3', '.txt')
    Path(tts_file).parent.mkdir(parents=True, exist_ok=True)
    with open(tts_file, 'w') as f:
        f.write(clean_text)
    
    print(f"✅ TTS-ready text saved to: {tts_file}")
    print()
    
    print("⚠️  This script prepares the text for TTS.")
    print("    Actual ElevenLabs TTS call must be performed by OpenClaw worker.")
    print()
    print("Worker should:")
    print(f"  1. Call elevenlabs_text_to_speech tool")
    print(f"  2. text={tts_file}")
    print(f"  3. voice_id={voice_id}")
    print(f"  4. model_id={model}")
    print(f"  5. output_directory={Path(args.output).parent}")
    print(f"  6. Rename output to: {args.output}")
    print()
    
    # Create placeholder MP3 marker
    with open(args.output + ".pending", 'w') as f:
        f.write(f"Pending TTS generation\nText: {tts_file}\nVoice: {voice_id}\nModel: {model}\n")
    
    print(f"✅ Created pending marker: {args.output}.pending")
    print(f"   Worker should generate MP3 to: {args.output}")


if __name__ == "__main__":
    main()
