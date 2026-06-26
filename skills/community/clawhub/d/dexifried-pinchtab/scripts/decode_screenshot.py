#!/usr/bin/env python3
"""
decode_screenshot.py - Decode base64 screenshots from PinchTab and optionally send to Telegram
Usage: python3 decode_screenshot.py <tab_id> [--send-telegram <chat_id>] [--output <path>]
"""

import sys
import os
import base64
import json
import argparse
import subprocess
import requests
from pathlib import Path

def decode_screenshot(tab_id: str, server: str = "http://localhost:9867", token: str = "") -> tuple[str, bytes]:
    """Fetch and decode screenshot from PinchTab"""
    
    if not token:
        token = os.getenv("PINCHTAB_TOKEN", "")
    
    if not token:
        raise ValueError("PINCHTAB_TOKEN not set. Export it or pass via --token")
    
    print(f"📸 Fetching screenshot for tab: {tab_id}")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{server}/tabs/{tab_id}/screenshot", headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"PinchTab error: {response.status_code} - {response.text}")
    
    data = response.json()
    base64_str = data.get("base64")
    
    if not base64_str:
        raise ValueError("No base64 data in response")
    
    print("✅ Screenshot fetched. Decoding base64...")
    image_bytes = base64.b64decode(base64_str)
    
    return base64_str, image_bytes

def save_screenshot(image_bytes: bytes, output_path: str) -> str:
    """Save decoded image to file"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "wb") as f:
        f.write(image_bytes)
    
    size_kb = len(image_bytes) / 1024
    print(f"✅ Saved: {path} ({size_kb:.1f} KB)")
    return str(path)

def send_to_telegram(image_path: str, chat_id: str, bot_token: str = "", caption: str = "") -> bool:
    """Send image to Telegram"""
    
    if not bot_token:
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    if not bot_token:
        print("⚠️  TELEGRAM_BOT_TOKEN not set. Skipping Telegram send.")
        return False
    
    print(f"📤 Sending to Telegram (chat: {chat_id})...")
    
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    with open(image_path, "rb") as f:
        files = {"photo": f}
        data = {
            "chat_id": chat_id,
            "caption": caption or f"PinchTab Screenshot"
        }
        
        response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200 and response.json().get("ok"):
        print("✅ Sent to Telegram!")
        return True
    else:
        print(f"❌ Telegram error: {response.text}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Decode PinchTab base64 screenshots and optionally send to Telegram"
    )
    parser.add_argument("tab_id", help="PinchTab tab ID")
    parser.add_argument("--server", default="http://localhost:9867", help="PinchTab server URL")
    parser.add_argument("--token", help="PinchTab auth token (or set PINCHTAB_TOKEN)")
    parser.add_argument("--output", default="/tmp/pinchtab-screenshot.jpg", help="Output file path")
    parser.add_argument("--send-telegram", help="Send to Telegram (chat ID)")
    parser.add_argument("--telegram-token", help="Telegram bot token (or set TELEGRAM_BOT_TOKEN)")
    parser.add_argument("--caption", help="Telegram photo caption")
    
    args = parser.parse_args()
    
    try:
        # Decode screenshot
        base64_str, image_bytes = decode_screenshot(args.tab_id, args.server, args.token)
        
        # Save to file
        output_path = save_screenshot(image_bytes, args.output)
        
        # Send to Telegram if requested
        if args.send_telegram:
            send_to_telegram(
                output_path,
                args.send_telegram,
                args.telegram_token,
                args.caption
            )
        
        print(f"\n✨ Done! Screenshot: {output_path}")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
