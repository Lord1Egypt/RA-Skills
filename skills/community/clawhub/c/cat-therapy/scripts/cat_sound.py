#!/usr/bin/env python3
"""
Generate cat sound effects (meow, purr) using TTS or return audio file paths.
For the cat-therapy skill.
"""

import os
import random

def get_cat_sound(sound_type="meow"):
    """
    Get cat sound effect.
    sound_type: "meow", "purr", or "random"
    Returns audio file path or TTS text.
    """
    
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    
    if sound_type == "random":
        sound_type = random.choice(["meow", "purr"])
    
    # Check for local audio files
    audio_files = []
    for f in os.listdir(assets_dir):
        if f.endswith(('.mp3', '.wav', '.ogg')) and sound_type in f.lower():
            audio_files.append(os.path.join(assets_dir, f))
    
    if audio_files:
        return {"path": random.choice(audio_files), "type": sound_type, "source": "local"}
    
    # Fallback to TTS text
    if sound_type == "meow":
        return {"tts": "喵～", "type": "meow", "source": "tts"}
    elif sound_type == "purr":
        return {"tts": "咕噜咕噜～", "type": "purr", "source": "tts"}
    
    return {"error": "No cat sound available"}

if __name__ == "__main__":
    import sys
    sound_type = sys.argv[1] if len(sys.argv) > 1 else "random"
    result = get_cat_sound(sound_type)
    print(result)
