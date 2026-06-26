#!/usr/bin/env python3
"""
Open WebUI RAG 對話腳本
"""

import os
import sys
import requests
import argparse
import json

def get_config():
    """取得設定"""
    url = os.environ.get("OPENWEBUI_URL")
    api_key = os.environ.get("OPENWEBUI_API_KEY")
    
    if not url or not api_key:
        print("❌ 錯誤：請設定環境變數 OPENWEBUI_URL 和 OPENWEBUI_API_KEY")
        sys.exit(1)
    
    return {"url": url, "api_key": api_key}

def chat(message: str, model: str = None):
    """使用知識庫對話"""
    config = get_config()
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    # 預設模型
    if not model:
        model = "llama3"
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "mode": "chat",
        "include_rag_context": True
    }
    
    try:
        response = requests.post(
            f"{config['url']}/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 錯誤: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Open WebUI RAG 對話")
    parser.add_argument("--message", "-m", required=True, help="對話內容")
    parser.add_argument("--model", help="模型名稱")
    
    args = parser.parse_args()
    
    print(f"💬 對話中: {args.message}")
    
    result = chat(args.message, args.model)
    
    if result and "choices" in result:
        print("\n✅ 回覆:")
        print(result["choices"][0]["message"]["content"])
    else:
        print("❌ 對話失敗")

if __name__ == "__main__":
    main()
