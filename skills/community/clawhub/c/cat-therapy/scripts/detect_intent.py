#!/usr/bin/env python3
"""
Detect user intent for cat-therapy skill.
Determines if user wants to:
1. Trigger cat therapy
2. Save custom cat
3. Save custom sound
4. Reset preferences
5. Just chatting (no action)
"""

import json
import sys

# Trigger phrases for cat therapy
THERAPY_TRIGGERS_ZH = [
    "休息一下", "累了", "好累", "累死了",
    "想撸猫", "看看猫", "猫图", "猫咪", "猫猫",
    "压力大", "放松一下", "治愈我", "不开心",
    "喵", "喵喵", "喵星人",
    "想猫了", "吸猫", "云撸猫"
]

THERAPY_TRIGGERS_EN = [
    "tired", "exhausted", "need a break", "need rest",
    "show me cats", "cat pics", "cat pictures", "kitten",
    "stress", "relax", "cheer me up", "heal me",
    "meow", "cat therapy", "cat time"
]

# Save custom cat phrases
SAVE_CAT_ZH = [
    "这是我的猫", "这是我家猫", "我家猫",
    "保存这只猫", "用这只猫", "设置这只猫",
    "以后用这只", "这只治愈我", "这是主子",
    "我家主子", "这是我养的猫"
]

SAVE_CAT_EN = [
    "this is my cat", "my cat", "save this cat",
    "use this cat", "set this cat", "my kitty",
    "this is my kitty", "my own cat"
]

# Save custom sound phrases
SAVE_SOUND_ZH = [
    "这是我家猫的声音", "猫叫是", "叫声是",
    "保存这个声音", "猫叫声音", "喵喵叫"
]

SAVE_SOUND_EN = [
    "this is my cat's sound", "cat sound", "meow sound",
    "save this sound", "my cat says"
]

# Reset phrases
RESET_ZH = ["重置猫咪", "恢复默认", "删除自定义", "清除猫咪"]
RESET_EN = ["reset cat", "restore default", "delete custom", "clear cat"]

def detect_intent(message, has_image=False, has_audio=False, context=None):
    """
    Detect user intent from message.
    
    Args:
        message: User's message text
        has_image: Whether message includes an image
        has_audio: Whether message includes audio
        context: Previous conversation context (optional)
    
    Returns:
        dict: {"action": "...", "confidence": 0.0-1.0, "data": {...}}
    """
    
    text = message.lower().strip()
    
    # Check for reset command
    for phrase in RESET_ZH + RESET_EN:
        if phrase in text:
            return {"action": "reset", "confidence": 0.95, "data": {}}
    
    # Check for save cat (requires image)
    if has_image:
        for phrase in SAVE_CAT_ZH + SAVE_CAT_EN:
            if phrase in text:
                return {
                    "action": "save_cat",
                    "confidence": 0.9,
                    "data": {"has_image": True}
                }
        
        # If just image without save phrase, check context
        if context and context.get("in_therapy_session"):
            # In therapy session + image = might want to save
            if "这" in text or "this" in text or "用" in text:
                return {
                    "action": "save_cat",
                    "confidence": 0.7,
                    "data": {"has_image": True}
                }
    
    # Check for save sound
    if has_audio or "声音" in text or "sound" in text:
        for phrase in SAVE_SOUND_ZH + SAVE_SOUND_EN:
            if phrase in text:
                return {
                    "action": "save_sound",
                    "confidence": 0.9,
                    "data": {"has_audio": has_audio}
                }
    
    # Check for therapy trigger
    for phrase in THERAPY_TRIGGERS_ZH + THERAPY_TRIGGERS_EN:
        if phrase in text:
            # Detect language
            lang = "en" if any(p in text for p in THERAPY_TRIGGERS_EN) else "zh"
            return {
                "action": "therapy",
                "confidence": 0.95,
                "data": {"language": lang}
            }
    
    # No intent detected
    return {"action": "none", "confidence": 0.0, "data": {}}

if __name__ == "__main__":
    # Test mode
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        result = detect_intent(message)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Interactive test
        print("Cat Therapy Intent Detector")
        print("Enter messages to test (or 'quit' to exit)\n")
        
        while True:
            msg = input("> ").strip()
            if msg.lower() in ["quit", "exit", "q"]:
                break
            
            result = detect_intent(msg)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print()
