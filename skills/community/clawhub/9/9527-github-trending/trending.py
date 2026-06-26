#!/usr/bin/env python3
"""
GitHub Trending 每日推送工具
自动获取 GitHub Trending 热门项目并推送到通知渠道
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Optional
import urllib.request
import urllib.error

def fetch_trending(language: str = "", since: str = "daily") -> list:
    """获取 GitHub Trending 项目列表（通过爬取页面）"""
    url = f"https://github.com/trending/{language}?since={since}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            return parse_trending_html(html)
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

def parse_trending_html(html: str) -> list:
    """解析 GitHub Trending 页面 HTML"""
    repos = []
    
    # 匹配每个仓库块
    pattern = r'<article[^>]*class="[^"]*Box-row[^"]*"[^>]*>(.*?)</article>'
    articles = re.findall(pattern, html, re.DOTALL)
    
    for article in articles[:10]:
        try:
            # 提取仓库名
            name_match = re.search(r'<h2[^>]*>.*?<a[^>]*href="/([^"]+)"[^>]*>', article, re.DOTALL)
            name = name_match.group(1).strip() if name_match else "Unknown"
            
            # 提取描述
            desc_match = re.search(r'<p[^>]*class="[^"]*col-9[^"]*"[^>]*>(.*?)</p>', article, re.DOTALL)
            description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else "无描述"
            description = description[:80]
            
            # 提取 stars
            stars_match = re.search(r'([0-9,]+)\s*stars?', article, re.IGNORECASE)
            stars = stars_match.group(1).replace(',', '') if stars_match else "0"
            
            # 提取今日 stars
            today_match = re.search(r'([0-9,]+)\s*stars?\s*today', article, re.IGNORECASE)
            today_stars = today_match.group(1).replace(',', '') if today_match else "0"
            
            repos.append({
                'name': name,
                'url': f'https://github.com/{name}',
                'description': description,
                'totalStars': int(stars),
                'starsToday': int(today_stars)
            })
        except Exception:
            continue
    
    return repos

def format_message(repos: list, language: str = "") -> str:
    """格式化消息"""
    lang_text = f"({language}) " if language else ""
    title = f"🔥 GitHub Trending {lang_text}{datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    if not repos:
        return title + "暂无数据"
    
    lines = []
    for i, repo in enumerate(repos, 1):
        name = repo.get('name', 'Unknown')
        url = repo.get('url', '')
        description = repo.get('description', '无描述')[:50]
        stars = repo.get('totalStars', 0)
        today_stars = repo.get('starsToday', 0)
        
        lines.append(
            f"{i}. [{name}]({url})\n"
            f"   ⭐ {stars} (+{today_stars} today)\n"
            f"   {description}"
        )
    
    return title + "\n\n".join(lines)

def send_telegram(message: str, token: str, chat_id: str) -> bool:
    """发送到 Telegram"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={
            'Content-Type': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('ok', False)
    except Exception as e:
        print(f"Telegram 发送失败: {e}")
        return False

def send_dingtalk(message: str, webhook: str) -> bool:
    """发送到钉钉"""
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'GitHub Trending',
            'text': message
        }
    }
    
    try:
        req = urllib.request.Request(webhook, data=json.dumps(data).encode('utf-8'), headers={
            'Content-Type': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('errcode', -1) == 0
    except Exception as e:
        print(f"钉钉发送失败: {e}")
        return False

def send_wecom(message: str, webhook: str) -> bool:
    """发送到企业微信"""
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'content': message
        }
    }
    
    try:
        req = urllib.request.Request(webhook, data=json.dumps(data).encode('utf-8'), headers={
            'Content-Type': 'application/json'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('errcode', -1) == 0
    except Exception as e:
        print(f"企业微信发送失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='GitHub Trending 每日推送')
    parser.add_argument('--language', '-l', default='', help='编程语言过滤')
    parser.add_argument('--since', '-s', default='daily', choices=['daily', 'weekly', 'monthly'], help='时间范围')
    parser.add_argument('--telegram', '-t', action='store_true', help='推送到 Telegram')
    parser.add_argument('--token', help='Telegram Bot Token')
    parser.add_argument('--chat_id', help='Telegram Chat ID')
    parser.add_argument('--dingtalk', '-d', action='store_true', help='推送到钉钉')
    parser.add_argument('--webhook', help='钉钉/企业微信 Webhook URL')
    parser.add_argument('--wecom', '-w', action='store_true', help='推送到企业微信')
    parser.add_argument('--output', '-o', default='text', choices=['text', 'json'], help='输出格式')
    
    args = parser.parse_args()
    
    # 获取数据
    repos = fetch_trending(args.language, args.since)
    
    # 输出
    if args.output == 'json':
        print(json.dumps(repos, ensure_ascii=False, indent=2))
    else:
        message = format_message(repos, args.language)
        print(message)
        
        # 推送
        if args.telegram and args.token and args.chat_id:
            if send_telegram(message, args.token, args.chat_id):
                print("\n✅ 已推送到 Telegram")
        
        if args.dingtalk and args.webhook:
            if send_dingtalk(message, args.webhook):
                print("\n✅ 已推送到钉钉")
        
        if args.wecom and args.webhook:
            if send_wecom(message, args.webhook):
                print("\n✅ 已推送到企业微信")

if __name__ == '__main__':
    main()
