#!/usr/bin/env python3
"""
测试链接验证脚本
功能：自动验证测试链接的联通率、下载功能、视频播放等

使用: python3 check_links.py <链接1> <链接2> ...
"""

import sys
import json
from playwright.sync_api import sync_playwright

# CDP连接地址
CDP_URL = "http://localhost:18800"

def verify_link(url):
    """验证单个链接"""
    result = {
        "url": url,
        "status": "unknown",
        "download_ok": False,
        "video_ok": False,
        "error": None
    }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            page = browser.new_page()
            
            # 打开页面
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # 检查页面加载
            result["status"] = "ok"
            
            # 检查下载按钮/提示
            download_elements = page.query_selector_all("a[href*='download'], button:has-text('下载'), text=下载")
            result["download_ok"] = len(download_elements) > 0
            
            # 检查视频播放
            video_elements = page.query_selector_all("video")
            if video_elements:
                result["video_ok"] = True
            
            browser.close()
            
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    
    return result

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 check_links.py <链接1> <链接2> ...")
        sys.exit(1)
    
    links = sys.argv[1:]
    results = []
    
    for link in links:
        print(f"验证: {link}")
        result = verify_link(link)
        results.append(result)
        
        status_icon = "✓" if result["status"] == "ok" else "✗"
        print(f"  {status_icon} 状态: {result['status']}")
        print(f"    下载: {'是' if result['download_ok'] else '否'}")
        print(f"    视频: {'是' if result['video_ok'] else '否'}")
        if result.get("error"):
            print(f"    错误: {result['error']}")
    
    # 输出JSON结果
    print("\n--- JSON结果 ---")
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
