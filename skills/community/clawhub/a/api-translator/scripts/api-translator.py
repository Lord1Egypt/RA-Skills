#!/usr/bin/env python3
"""
API Translator - 將 API 文檔翻譯成繁體中文
使用 LLM API 進行翻譯
"""

import sys
import json
import subprocess

def fetch_url(url: str) -> str:
    """抓取網頁內容"""
    result = subprocess.run(
        ["web_fetch", "--url", url, "--maxChars", "50000"],
        capture_output=True,
        text=True
    )
    return result.stdout

def main():
    if len(sys.argv) < 2:
        print("用法: api-translator <API文檔URL>")
        print("範例: api-translator https://api.example.com/docs")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"🌐 抓取 API 文檔: {url}")
    
    # 抓取內容
    content = fetch_url(url)
    if not content:
        print("❌ 無法抓取網頁內容")
        sys.exit(1)
    
    # 顯示要翻譯的內容前 500 字預覽
    print(f"\n📄 內容預覽 (前 500 字):")
    print("-" * 40)
    print(content[:500] + "..." if len(content) > 500 else content)
    print("-" * 40)
    
    # 輸出翻譯 prompt
    print("\n🤖 請將以上 API 文檔翻譯成繁體中文（台灣用語）")
    print("📝 翻譯要求：")
    print("   - 保持 Markdown 格式")
    print("   - 保持程式碼不變")
    print("   - 只翻譯說明文字")
    print("   - 使用台灣用語（如：軟體而不是軟體）")

if __name__ == "__main__":
    main()
