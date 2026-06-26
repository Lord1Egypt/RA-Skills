#!/usr/bin/env python3
"""
Open WebUI RAG 搜尋腳本
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

def search(query: str, collection_name: str = None):
    """搜尋知識庫"""
    config = get_config()
    
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query
    }
    
    if collection_name:
        payload["collection_name"] = collection_name
    
    try:
        response = requests.post(
            f"{config['url']}/api/v1/rag",
            headers=headers,
            json=payload,
            timeout=30
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

def main():
    parser = argparse.ArgumentParser(description="Open WebUI RAG 搜尋")
    parser.add_argument("--query", "-q", required=True, help="搜尋關鍵字")
    parser.add_argument("--collection", "-c", help="知識庫名稱")
    
    args = parser.parse_args()
    
    print(f"🔍 搜尋: {args.query}")
    
    result = search(args.query, args.collection)
    
    if result:
        print("\n✅ 搜尋結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("❌ 搜尋失敗")
        sys.exit(1)

if __name__ == "__main__":
    main()
