#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feishu-emoji 表情包发送工具

用法:
    python emoji_sender.py <关键词> [消息文字]
    
示例:
    python emoji_sender.py 收到
    python emoji_sender.py 猫猫 "猫猫表情包来了！🐱"
"""

import sys
import os
import requests
from bs4 import BeautifulSoup

# 配置
MEDIA_DIR = os.getenv("OPENCLAW_MEDIA_DIR", "/home/admin/.openclaw/media/inbound")
REFERER = "https://fabiaoqing.com/"
SEARCH_URL = "https://fabiaoqing.com/search/bqb/keyword/{keyword}/type/bq/page/1.html"

# 常用表情包 CDN 映射（备用）
EMOJI_CDN = {
    "收到": "https://img.soutula.com/bmiddle/006APoFYly1glojj7wfc5j306o06odg1.jpg",
    "好的": "https://img.soutula.com/bmiddle/006zwuLWgy1fgzrchhzc0j30b40b4t9e.jpg",
    "谢谢": "https://img.soutula.com/bmiddle/b64da6adly1h7z28dwuw0j20j60pf44a.jpg",
}

def get_emoji_url(keyword):
    """从 fabiaoqing.com 获取表情包图片 URL"""
    # 先检查是否有预定义映射
    if keyword in EMOJI_CDN:
        return EMOJI_CDN[keyword]
    
    # 否则爬取网站
    url = SEARCH_URL.format(keyword=keyword)
    headers = {"Referer": REFERER}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 查找第一个表情包的 data-original 属性
        img = soup.find('img', attrs={'data-original': True})
        if img:
            img_url = img['data-original']
            # 处理协议相对 URL
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            return img_url
    except Exception as e:
        print(f"⚠️ 获取表情包失败：{e}", file=sys.stderr)
    
    return None

def download_emoji(img_url, keyword):
    """下载表情包到媒体目录"""
    os.makedirs(MEDIA_DIR, exist_ok=True)
    
    # 生成文件名
    filename = f"emoji_{keyword}.jpg"
    filepath = os.path.join(MEDIA_DIR, filename)
    
    headers = {"Referer": REFERER}
    
    try:
        resp = requests.get(img_url, headers=headers, timeout=10)
        resp.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(resp.content)
        
        return filepath
    except Exception as e:
        print(f"⚠️ 下载失败：{e}", file=sys.stderr)
        return None

def send_emoji(filepath, message):
    """调用 OpenClaw message 工具发送表情包"""
    # 这里需要通过 OpenClaw 的 message 工具发送
    # 实际使用时，AI 会直接调用 message 工具
    # 这个函数仅作为示例
    print(f"✅ 表情包已保存到：{filepath}")
    print(f"📤 发送消息：{message}")
    print(f"\n请在 OpenClaw 中执行:")
    print(f'message(action="send", message="{message}", media="{filepath}")')

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    keyword = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) > 2 else f"{keyword}表情包来了！"
    
    print(f"🔍 搜索表情包：{keyword}")
    
    # 获取图片 URL
    img_url = get_emoji_url(keyword)
    if not img_url:
        print(f"❌ 未找到表情包：{keyword}")
        sys.exit(1)
    
    print(f"📥 下载表情包：{img_url}")
    
    # 下载
    filepath = download_emoji(img_url, keyword)
    if not filepath:
        print(f"❌ 下载失败")
        sys.exit(1)
    
    # 发送
    send_emoji(filepath, message)

if __name__ == "__main__":
    main()
