#!/usr/bin/env python3
"""
Manage user's custom cat preferences.
Commands: save, load, delete, list
"""

import json
import os
import sys
from datetime import datetime

def get_config_path():
    """Get path to user_cats.json"""
    return os.path.join(os.path.dirname(__file__), "..", "user_cats.json")

def save_cat(image_url=None, sound=None, user_id="default"):
    """Save user's custom cat preferences."""
    config_path = get_config_path()
    
    # Load existing or create new
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {}
    
    # Update user's preferences
    user_key = f"user_{user_id}"
    data[user_key] = {
        "image": image_url,
        "sound": sound,
        "updatedAt": datetime.now().isoformat()
    }
    
    # Save back
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return {"status": "saved", "user": user_key}

def load_cat(user_id="default"):
    """Load user's custom cat preferences."""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    user_key = f"user_{user_id}"
    return data.get(user_key)

def delete_cat(user_id="default"):
    """Delete user's custom cat preferences."""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        return {"status": "not_found"}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    user_key = f"user_{user_id}"
    if user_key in data:
        del data[user_key]
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "deleted"}
    
    return {"status": "not_found"}

def list_cats():
    """List all saved user cats."""
    config_path = get_config_path()
    
    if not os.path.exists(config_path):
        return []
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return list(data.keys())

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    user_id = sys.argv[2] if len(sys.argv) > 2 else "default"
    
    if command == "save":
        image = sys.argv[3] if len(sys.argv) > 3 else None
        sound = sys.argv[4] if len(sys.argv) > 4 else None
        result = save_cat(image, sound, user_id)
        print(json.dumps(result, ensure_ascii=False))
    
    elif command == "load":
        result = load_cat(user_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "delete":
        result = delete_cat(user_id)
        print(json.dumps(result, ensure_ascii=False))
    
    elif command == "list":
        result = list_cats()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print("""
Cat Therapy - User Cat Manager

Usage:
  python manage_user_cat.py save [user_id] [image_url] [sound]
  python manage_user_cat.py load [user_id]
  python manage_user_cat.py delete [user_id]
  python manage_user_cat.py list

Examples:
  python manage_user_cat.py save user123 https://example.com/cat.jpg "喵～咪～"
  python manage_user_cat.py load user123
  python manage_user_cat.py delete user123
""")
