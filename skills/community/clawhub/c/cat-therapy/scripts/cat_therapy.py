#!/usr/bin/env python3
"""
Cat Therapy Skill - Main Logic
Fetches cat image, handles user preferences, returns complete response data.
"""

import urllib.request
import json
import os
import random
import ssl

# ✅ 修复：启用 SSL 证书验证（安全）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

def get_user_preferences():
    """Load user's custom cat preferences if available."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "user_cats.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_user_preferences(prefs):
    """Save user's custom cat preferences."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "user_cats.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)

def get_cat_image(user_prefs=None):
    """Fetch cat image - use user's custom image if available, else random."""
    
    # Priority 1: User's custom image
    if user_prefs and "image" in user_prefs:
        return {"url": user_prefs["image"], "source": "user"}
    
    # Priority 2: Random from API
    try:
        req = urllib.request.Request(
            "https://api.thecatapi.com/v1/images/search",
            headers={"Accept": "application/json", "User-Agent": "CatTherapy/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0 and "url" in data[0]:
                return {"url": data[0]["url"], "source": "thecatapi"}
    except Exception:
        pass
    
    # Priority 3: Fallback URLs
    fallback_urls = [
        "https://cdn2.thecatapi.com/images/0XYvCQ7q2.jpg",
        "https://cdn2.thecatapi.com/images/b1.jpg",
        "https://cataas.com/cat",
    ]
    return {"url": random.choice(fallback_urls), "source": "fallback"}

def get_cat_sound(user_prefs=None):
    """Get cat sound - use user's custom sound if available, else TTS text."""
    
    # Priority 1: User's custom sound
    if user_prefs and "sound" in user_prefs:
        return {"text": user_prefs["sound"], "source": "user"}
    
    # Priority 2: Default TTS text
    return {"text": "喵～咕噜咕噜～", "source": "default"}

def get_quote(language="zh"):
    """Get a random healing quote in specified language."""
    i18n_dir = os.path.join(os.path.dirname(__file__), "..", "i18n")
    lang_file = os.path.join(i18n_dir, f"{language}.json")
    
    if os.path.exists(lang_file):
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            quotes = data.get("quotes", [])
            if quotes:
                return random.choice(quotes)
    
    # Fallback to English
    en_file = os.path.join(i18n_dir, "en.json")
    if os.path.exists(en_file):
        with open(en_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            quotes = data.get("quotes", [])
            if quotes:
                return random.choice(quotes)
    
    return "Take a break and relax! ✨"

if __name__ == "__main__":
    import sys
    
    # Check for user preferences
    user_prefs = get_user_preferences()
    
    # Get cat image
    image_result = get_cat_image(user_prefs)
    
    # Get cat sound
    sound_result = get_cat_sound(user_prefs)
    
    # Detect language from args
    language = sys.argv[1] if len(sys.argv) > 1 else "zh"
    
    # Get quote
    quote = get_quote(language)
    
    # Output complete response
    response = {
        "image": image_result,
        "sound": sound_result,
        "quote": quote,
        "language": language,
        "has_user_prefs": user_prefs is not None
    }
    
    print(json.dumps(response, ensure_ascii=False))
