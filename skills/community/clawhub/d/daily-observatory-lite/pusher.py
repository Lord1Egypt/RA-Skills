#!/usr/bin/env python3
"""
Telegram 推播模組
"""

import subprocess

def send_telegram_message(chat_id, message):
    """發送訊息到 Telegram"""
    try:
        # 使用 openclaw agent 發送訊息
        cmd = [
            "openclaw", "agent",
            "--to", chat_id,
            "--message", message,
            "--deliver"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, "發送成功"
        else:
            return False, f"發送失敗: {result.stderr}"
    
    except Exception as e:
        return False, f"錯誤: {str(e)}"

if __name__ == "__main__":
    # 測試
    success, msg = send_telegram_message("TEST", "測試訊息")
    print(msg)
