#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for emoji-wrapper skill
"""

import sys
from pathlib import Path

# Add workspace to path
workspace = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace))

# Import wrapper
sys.path.insert(0, str(workspace / "skills" / "emoji-wrapper"))
from script import EmojiWrapper

# Mock objects
class MockMessage:
    def __init__(self, content):
        self.content = content

class MockSession:
    def __init__(self, userid):
        self.userid = userid
        self.user = type('User', (), {'id': userid})

class MockCallback:
    def __init__(self):
        self.sent_messages = []

    def __call__(self, msg):
        self.sent_messages.append(msg)
        print(f"Callback sent: {msg[:50]}..." if len(msg) > 50 else f"Callback sent: {msg}")

# Test
print("=" * 60)
print("Emoji Wrapper Skill Test")
print("=" * 60)

wrapper = EmojiWrapper()

if not wrapper._initialized:
    print("ERROR: Wrapper not initialized. Make sure local-auto-emoji is working.")
    sys.exit(1)

# Use existing user with emojis (wrapper_test_full has 11 emojis)
test_userid = "wrapper_test_full"
wrapper._ensure_user(test_userid)
print(f"\nUsing existing user: {test_userid}")

# Verify emojis exist
emotions_to_test = ["cute", "blink", "hug", "flying_kiss", "happy", "cool", "angry", "sad"]
print("Checking emoji files:")
for emo in emotions_to_test:
    path = wrapper.bot.get_emoji_for_emotion(emo)
    if path:
        print(f"  {emo}: exists={path.exists()} name={path.name if path.exists() else 'N/A'}")
    else:
        print(f"  {emo}: NOT FOUND")

# Test messages
test_cases = [
    ("凯哥真厉害！[可爱] 好好玩～", "Single marker: [可爱]"),
    ("[眨眼]给你一个飞吻[飞吻]", "Multiple markers: [眨眼] + [飞吻]"),
    ("要抱抱[抱抱]！", "Marker at end: [抱抱]"),
    ("没有标记的纯文本消息", "No markers"),
    ("[悲伤]但是别难过", "Marker at start: [悲伤]"),
]

for text, description in test_cases:
    print(f"\n{description}")
    print(f"Input: {text}")

    # Test with callback
    callback = MockCallback()
    result = wrapper.process_message(
        MockMessage(text),
        session=MockSession(test_userid),
        callback=callback
    )

    print(f"Sent {len(callback.sent_messages)} messages:")
    for i, msg in enumerate(callback.sent_messages, 1):
        prefix = "🖼️ " if msg.startswith("MEDIA:") else "💬 "
        print(f"  {i}. {prefix}{msg[:60]}{'...' if len(msg) > 60 else ''}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
