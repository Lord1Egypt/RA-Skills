#!/usr/bin/env python3
"""
携程笔记自动发布脚本
功能：打开携程发布页面，准备发布内容
"""

import os
import webbrowser
import time

def open_ctrip_publish():
    """打开发布页面"""
    urls = {
        "主页": "https://we.ctrip.com/publish/publishHome",
        "图文发布": "https://we.ctrip.com/publish/detail?articleType=1",
        "视频发布": "https://we.ctrip.com/publish/detail?articleType=2",
    }
    
    print("🚀 携程内容中心 - 发布页面")
    print("=" * 40)
    for name, url in urls.items():
        print(f"  {name}: {url}")
    print("=" * 40)
    
    # 打开发布主页
    webbrowser.open(urls["主页"])
    print("\n✅ 已打开发布页面，请扫码登录后告诉我您要发布的内容")

def main():
    open_ctrip_publish()

if __name__ == "__main__":
    main()