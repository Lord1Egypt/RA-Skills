#!/usr/bin/env python3
"""
Open WebUI 檔案上傳腳本
"""

import os
import sys
import requests
import argparse
from pathlib import Path

def get_config():
    """取得設定"""
    url = os.environ.get("OPENWEBUI_URL")
    api_key = os.environ.get("OPENWEBUI_API_KEY")
    
    if not url:
        print("❌ 錯誤：請設定環境變數 OPENWEBUI_URL")
        print("   例如：export OPENWEBUI_URL=\"http://192.168.0.176:3000\"")
        sys.exit(1)
    
    if not api_key:
        print("❌ 錯誤：請設定環境變數 OPENWEBUI_API_KEY")
        print("   例如：export OPENWEBUI_API_KEY=\"your_token\"")
        sys.exit(1)
    
    return {
        "url": url,
        "api_key": api_key
    }

def upload_file(file_path: str):
    """上傳檔案到知識庫"""
    config = get_config()
    
    if not os.path.exists(file_path):
        print(f"❌ 檔案不存在: {file_path}")
        return None
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}"
    }
    
    file_name = os.path.basename(file_path)
    
    try:
        with open(file_path, 'rb') as f:
            files = {
                'file': (file_name, f)
            }
            response = requests.post(
                f"{config['url']}/api/v1/files/upload",
                headers=headers,
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("❌ 認證失敗！請檢查 API Key")
            return None
        else:
            print(f"❌ 錯誤: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ 無法連接到 Open WebUI: {config['url']}")
        return None
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return None

def list_files():
    """列出已上傳的檔案"""
    config = get_config()
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}"
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
            return None
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Open WebUI 檔案上傳")
    parser.add_argument("--file", "-f", help="要上傳的檔案路徑")
    parser.add_argument("--list", "-l", action="store_true", help="列出已上傳的檔案")
    
    args = parser.parse_args()
    
    if args.list:
        print("📂 列出已上傳的檔案...")
        result = list_files()
        if result:
            print("✅ 檔案列表:")
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    if not args.file:
        print("❌ 請指定要上傳的檔案 (--file)")
        sys.exit(1)
    
    print(f"📤 上傳中: {args.file}")
    
    result = upload_file(args.file)
    
    if result:
        print("✅ 上傳成功!")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("❌ 上傳失敗")
        sys.exit(1)

if __name__ == "__main__":
    main()
