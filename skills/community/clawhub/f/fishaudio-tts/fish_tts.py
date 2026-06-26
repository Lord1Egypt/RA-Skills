#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FishAudio TTS - Generate natural human-like speech
Usage: python fish_tts.py --text "Text to convert" --output output.mp3 --voice female
"""

import argparse
import requests
import os
import sys

# Fix Unicode output on Windows
if os.name == 'nt':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

# Configure proxy from TOOLS.md if available
proxies = None
if os.path.exists(os.path.expanduser('~/.openclaw/workspace/TOOLS.md')):
    with open(os.path.expanduser('~/.openclaw/workspace/TOOLS.md'), 'r', encoding='utf-8') as f:
        content = f.read()
        # Look for proxy configuration
        if '127.0.0.1:7890' in content or 'http://127.0.0.1:7890' in content:
            proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890'
            }

def get_api_key():
    """Get API key from environment variable or TOOLS.md"""
    api_key = os.environ.get('FISH_AUDIO_API_KEY')
    if api_key:
        return api_key
    
    # Try to read from TOOLS.md
    tools_path = os.path.expanduser('~/.openclaw/workspace/TOOLS.md')
    if os.path.exists(tools_path):
        with open(tools_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for FishAudio API key
            for line in content.split('\n'):
                if 'fish' in line.lower() and 'api' in line.lower() and 'key' in line.lower():
                    # Extract key after colon
                    if ':' in line:
                        candidate = line.split(':', 1)[1].strip()
                        if candidate:
                            return candidate
    
    return None

def get_voice_id(voice_name):
    """Map voice name to FishAudio model ID"""
    voices = {
        'female': 'female',
        'male': 'male', 
        'neutral': 'neutral'
    }
    return voices.get(voice_name.lower(), 'female')

def generate_speech(text, output_path, voice_name='female', api_key=None):
    """Generate speech using FishAudio API"""
    
    if api_key is None:
        api_key = get_api_key()
    
    if api_key is None:
        print("❌ Error: Could not find FishAudio API key")
        print("Please get one from https://fish.audio/ and add it to:")
        print("1. Environment variable FISH_AUDIO_API_KEY, OR")
        print("2. Add to your TOOLS.md with FishAudio API key: ...")
        return False
    
    voice_id = get_voice_id(voice_name)
    
    # FishAudio API endpoint
    url = "https://api.fish.audio/v1/tts"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "voice_id": voice_id,
        "format": "mp3"
    }
    
    try:
        print(f"Generating speech with FishAudio...")
        print(f"Text length: {len(text)} characters")
        print(f"Voice: {voice_name}")
        if proxies:
            print(f"Using proxy: {proxies['https']}")
        
        response = requests.post(url, json=payload, headers=headers, proxies=proxies)
        response.raise_for_status()
        
        # Save the audio
        output_dir = os.path.dirname(os.path.abspath(output_path))
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"\n✅ Success! Audio saved to: {output_path}")
        print(f"File size: {os.path.getsize(output_path) / 1024:.1f} KB")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ API request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate speech using FishAudio TTS')
    parser.add_argument('--text', required=True, help='Text to convert to speech')
    parser.add_argument('--output', required=True, help='Output MP3 file path')
    parser.add_argument('--voice', default='female', help='Voice type: female/male/neutral (default: female)')
    parser.add_argument('--api-key', help='FishAudio API key (optional, will read from env or TOOLS.md)')
    
    args = parser.parse_args()
    
    # Expand user path
    output_path = os.path.abspath(os.path.expanduser(args.output))
    
    success = generate_speech(args.text, output_path, args.voice, args.api_key)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
