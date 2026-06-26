#!/usr/bin/env python3
"""
比特币价格自动监控脚本
每小时检查一次，如果触发警报就发送 Telegram 消息
"""

import json
import requests
import sys
import time
from datetime import datetime
import os

# 配置
ALERTS_FILE = os.path.join(os.path.dirname(__file__), 'alerts.json')
PRICE_API = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,cny,sgd&include_24hr_change=true"
LAST_PRICE_FILE = os.path.join(os.path.dirname(__file__), 'last_price.json')

# 防封 IP 配置
MAX_RETRIES = 3
RETRY_DELAY = 60  # 如果触发限流，等待 60 秒再重试
REQUEST_TIMEOUT = 10

def get_btc_price():
    """获取比特币实时价格（带防封 IP 保护）"""
    last_price = None
    try:
        # 尝试加载本地缓存价格
        if os.path.exists(LAST_PRICE_FILE):
            with open(LAST_PRICE_FILE, 'r', encoding='utf-8') as f:
                last_price = json.load(f)
    except:
        pass

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(PRICE_API, timeout=REQUEST_TIMEOUT)
            
            # 处理 429 Too Many Requests (IP 被封/限流)
            if response.status_code == 429:
                print(f"⚠️ 触发 CoinGecko 限流 (429)，等待 {RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
                continue
            
            response.raise_for_status()
            data = response.json()
            price_data = data['bitcoin']
            
            # 保存成功获取的价格到缓存
            with open(LAST_PRICE_FILE, 'w', encoding='utf-8') as f:
                json.dump(price_data, f, ensure_ascii=False)
            
            return price_data
            
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if "429" in error_msg or "rate limit" in error_msg.lower():
                print(f"⚠️ 触发限流，等待 {RETRY_DELAY} 秒后重试 ({attempt + 1}/{MAX_RETRIES})...")
                time.sleep(RETRY_DELAY)
                continue
            else:
                print(f"❌ 网络请求错误：{e}")
                break
        except Exception as e:
            print(f"❌ 获取价格失败：{e}")
            break
    
    # 如果所有重试都失败，返回本地缓存价格
    if last_price:
        print("⚠️ 使用本地缓存价格（网络请求失败）")
        return last_price
    
    return None

def load_alerts():
    """加载警报列表"""
    try:
        with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"❌ 读取警报失败：{e}")
        return []

def check_alerts(price_data):
    """检查是否触发警报"""
    alerts = load_alerts()
    if not alerts:
        return []
    
    current_price = price_data['usd']
    triggered = []
    
    for alert in alerts:
        condition = alert['condition']
        target_price = alert['price']
        name = alert['name']
        
        if condition == 'above' and current_price >= target_price:
            triggered.append({
                'name': name,
                'condition': '高于',
                'target': target_price,
                'current': current_price,
                'type': 'above'
            })
        elif condition == 'below' and current_price <= target_price:
            triggered.append({
                'name': name,
                'condition': '低于',
                'target': target_price,
                'current': current_price,
                'type': 'below'
            })
    
    return triggered

def send_notification(triggered_alerts, price_data):
    """发送通知（通过布布）"""
    if not triggered_alerts:
        return
    
    current_price = price_data['usd']
    change = price_data['usd_24h_change']
    
    message = f"🚨 **比特币价格警报触发！**\n\n"
    message += f"💰 当前价格：${current_price:,.2f}\n"
    message += f"📈 24h 变化：{change:+.2f}%\n\n"
    message += f"⚡ 触发的警报：\n"
    
    for alert in triggered_alerts:
        emoji = "📈" if alert['type'] == 'above' else "📉"
        message += f"{emoji} **{alert['name']}** - 价格{alert['condition']} ${alert['target']:,.2f}\n"
    
    message += f"\n⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 这里会调用布布的发送机制（实际实现时会通过 sessions_send 或类似机制）
    print(f"\n{'='*50}")
    print(message)
    print(f"{'='*50}\n")
    
    # 实际发送时，会调用布布的 API 发送 Telegram 消息
    # 这里只是模拟输出
    return message

def main():
    """主函数"""
    print(f"🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查比特币价格...")
    
    # 获取价格
    price_data = get_btc_price()
    if not price_data:
        print("❌ 无法获取价格，跳过本次检查")
        return
    
    current_price = price_data['usd']
    print(f"💰 当前价格：${current_price:,.2f} (24h: {price_data['usd_24h_change']:+.2f}%)")
    
    # 检查警报
    triggered = check_alerts(price_data)
    
    if triggered:
        print(f"🚨 发现 {len(triggered)} 个触发的警报！")
        send_notification(triggered, price_data)
    else:
        print("✅ 暂无警报触发")
    
    print("✅ 检查完成")

if __name__ == '__main__':
    main()
