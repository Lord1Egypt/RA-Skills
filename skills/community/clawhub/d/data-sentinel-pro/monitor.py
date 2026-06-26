#!/usr/bin/env python3
# scripts/monitor.py - 数据监控核心脚本

import requests
import json
import hashlib
import os
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re

# 配置
DATA_DIR = os.path.expanduser("~/.openclaw/data/sentinel")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_url_content(url):
    """获取网页内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        # 启用 SSL 验证确保安全
        response = requests.get(url, headers=headers, timeout=30, verify=True)
        response.raise_for_status()
        return response.text
    except requests.exceptions.SSLError as e:
        return f"ERROR: SSL verification failed - {str(e)}"
    except Exception as e:
        return f"ERROR: {str(e)}"

def extract_price(html, selector=None):
    """提取价格信息"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # 常见电商价格选择器
    price_patterns = [
        r'￥?(\d+\.?\d*)',  # ￥199.00
        r'价格 [：:]\s*￥?(\d+\.?\d*)',
        r'<[^>]*price[^>]*>([^<]+)',
    ]
    
    if selector:
        # 如果用户提供了自定义选择器
        elements = soup.select(selector)
        if elements:
            return elements[0].text.strip()
    
    # 默认尝试所有模式
    for pattern in price_patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    
    return None

def calculate_hash(content):
    """计算内容哈希值用于变化检测"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def load_previous_data(url):
    """加载上次监控的数据"""
    filename = os.path.join(DATA_DIR, hashlib.md5(url.encode()).hexdigest() + ".json")
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def save_current_data(url, data):
    """保存本次监控的数据"""
    filename = os.path.join(DATA_DIR, hashlib.md5(url.encode()).hexdigest() + ".json")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def check_for_changes(url, content, rule):
    """检查是否有变化"""
    prev = load_previous_data(url)
    current_hash = calculate_hash(content)
    
    result = {
        'url': url,
        'timestamp': datetime.now().isoformat(),
        'has_changed': False,
        'changes': []
    }
    
    if prev:
        # 检查整体变化
        if prev.get('hash') != current_hash:
            result['has_changed'] = True
            result['changes'].append('页面内容发生了变化')
        
        # 检查价格变化（如果是价格监控）
        if 'price' in rule:
            current_price = extract_price(content)
            prev_price = prev.get('price')
            if current_price and prev_price and current_price != prev_price:
                result['has_changed'] = True
                result['changes'].append(f'价格从 {prev_price} 变为 {current_price}')
                result['new_price'] = current_price
    else:
        # 首次监控
        result['has_changed'] = True
        result['changes'].append('首次监控，已记录初始状态')
    
    # 保存当前数据
    save_data = {
        'hash': current_hash,
        'timestamp': result['timestamp'],
        'price': extract_price(content) if 'price' in rule else None
    }
    save_current_data(url, save_data)
    
    return result

def send_notification(message, config):
    """发送通知（TG/邮件）"""
    # Telegram 通知
    if config.get('telegram_token'):
        tg_url = f"https://api.telegram.org/bot{config['telegram_token']}/sendMessage"
        data = {
            'chat_id': config.get('telegram_chat_id'),
            'text': message,
            'parse_mode': 'HTML'
        }
        try:
            requests.post(tg_url, json=data, timeout=10)
        except:
            pass
    
    # 邮件通知（可选）
    # ... 邮件发送逻辑
    
    print(f"NOTIFICATION: {message}")

def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) < 2:
        print("使用方法：monitor.py <url> [rule]")
        sys.exit(1)
    
    url = sys.argv[1]
    rule = sys.argv[2] if len(sys.argv) > 2 else "content"
    
    # 获取页面内容
    content = fetch_url_content(url)
    if content.startswith("ERROR:"):
        print(f"抓取失败：{content}")
        sys.exit(1)
    
    # 检查变化
    result = check_for_changes(url, content, rule)
    
    # 如果有变化，输出结果
    if result['has_changed']:
        message = f"🔔 <b>监控警报</b>\n"
        message += f"URL: {url}\n"
        message += f"时间：{result['timestamp']}\n"
        for change in result['changes']:
            message += f"• {change}\n"
        print(message)
        
        # 尝试加载配置发送通知
        try:
            config_path = os.path.expanduser("~/.openclaw/openclaw.json")
            with open(config_path, 'r') as f:
                config = json.load(f)
            skill_config = config.get('skills', {}).get('data-sentinel-pro', {})
            send_notification(message, skill_config)
        except:
            pass
    else:
        print(f"✓ 无变化 - {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
