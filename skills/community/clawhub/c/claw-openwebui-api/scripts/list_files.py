#!/usr/bin/env python3
"""
Open WebUI 列出已上傳檔案腳本
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

def list_files():
    """列出已上傳的檔案"""
    config = get_config()
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{config['url']}/api/v1/files",
            headers=headers,
            timeout=30
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
    parser = argparse.ArgumentParser(description="列出 Open WebUI 已上傳檔案")
    parser.add_argument("--json", "-j", action="store_true", help="輸出 JSON 格式")
    
    parser.parse_args()
    
    print("📂 取得檔案列表...")
    
    result = list_files()
    
    if result:
        if isinstance(result, dict) and "data" in result:
            files = result["data"]
            print(f"\n✅ 找到 {len(files)} 個檔案:\n")
            for f in files:
                print(f"  - {f.get('name', 'unknown')}")
                print(f"    ID: {f.get('id', 'N/A')}")
                print(f"    大小: {f.get('size', 'N/A')} bytes\n")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("❌ 取得失敗")

if __name__ == "__main__":
    main()
