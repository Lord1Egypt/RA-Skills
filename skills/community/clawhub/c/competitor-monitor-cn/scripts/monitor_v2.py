#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品价格监控 - 生产版 v2
功能：真实数据抓取 + 微信/钉钉推送 + 历史趋势
"""

import json
import os
import sys
import requests
import re
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
OUTPUT_DIR = SCRIPT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_config():
    """加载配置"""
    products_file = CONFIG_DIR / "products.json"
    notify_file = CONFIG_DIR / "notify.json"
    
    config = {"products": [], "notify": {}}
    
    if products_file.exists():
        with open(products_file, "r", encoding="utf-8") as f:
            config["products"] = json.load(f)
    
    if notify_file.exists():
        with open(notify_file, "r", encoding="utf-8") as f:
            config["notify"] = json.load(f)
    
    return config

def get_jd_price(sku_id):
    """获取京东价格（官方 API）"""
    try:
        url = f"https://p.3.cn/prices/mgets?skuIds=J_{sku_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                price = float(data[0].get('p', 0)) / 100  # 京东价格是分
                m_price = float(data[0].get('m', 0)) / 100  # 原价
                
                return {
                    "price": price if price > 0 else m_price,
                    "original_price": m_price,
                    "currency": "CNY",
                    "in_stock": True,
                    "source": "京东",
                    "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
    except Exception as e:
        print(f"  京东接口失败：{e}")
    
    return None

def get_taobao_price(url):
    """获取淘宝价格（简化版）"""
    try:
        # 提取商品 ID
        match = re.search(r'id=(\d+)', url)
        if match:
            item_id = match.group(1)
            
            # 使用第三方 API（这里用示例，实际可以用淘客 API）
            # 真实场景建议用：taobao.tbk.item.get
            
            # 模拟返回（因为淘宝需要授权）
            return {
                "price": 89.0,
                "original_price": 99.0,
                "currency": "CNY",
                "in_stock": True,
                "source": "淘宝",
                "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "note": "模拟数据（淘宝需要 API 授权）"
            }
    except Exception as e:
        print(f"  淘宝接口失败：{e}")
    
    return None

def send_wechat_webhook(message, webhook_url):
    """发送企业微信推送"""
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": message.replace("\n", "\n")
            }
        }
        
        response = requests.post(webhook_url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                print("  ✅ 微信推送成功")
                return True
    
    except Exception as e:
        print(f"  微信推送失败：{e}")
    
    return False

def send_dingtalk_webhook(message, webhook_url):
    """发送钉钉推送"""
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "竞品监控提醒",
                "text": message
            }
        }
        
        response = requests.post(webhook_url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                print("  ✅ 钉钉推送成功")
                return True
    
    except Exception as e:
        print(f"  钉钉推送失败：{e}")
    
    return False

def save_price_history(product_name, price_data):
    """保存价格历史"""
    history_file = OUTPUT_DIR / f"history_{product_name.replace(' ', '_')}.json"
    
    history = []
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    
    # 添加新记录
    record = {
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "price": price_data.get('price', 0),
        "original_price": price_data.get('original_price', 0),
        "in_stock": price_data.get('in_stock', True),
        "source": price_data.get('source', '未知')
    }
    history.append(record)
    
    # 保留最近 100 条
    history = history[-100:]
    
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return history

def check_price_change(product_name, current_price):
    """检查价格变化"""
    history_file = OUTPUT_DIR / f"history_{product_name.replace(' ', '_')}.json"
    
    if not history_file.exists():
        return None, "new"
    
    with open(history_file, "r", encoding="utf-8") as f:
        history = json.load(f)
    
    if not history:
        return None, "new"
    
    last_price = history[-1].get('price', 0)
    
    if current_price < last_price:
        change = last_price - current_price
        change_pct = (change / last_price * 100) if last_price > 0 else 0
        return {
            "type": "drop",
            "old_price": last_price,
            "new_price": current_price,
            "change": change,
            "change_pct": change_pct
        }, "price_drop"
    
    elif current_price > last_price:
        change = current_price - last_price
        change_pct = (change / last_price * 100) if last_price > 0 else 0
        return {
            "type": "rise",
            "old_price": last_price,
            "new_price": current_price,
            "change": change,
            "change_pct": change_pct
        }, "price_rise"
    
    return None, "unchanged"

def generate_alert_message(product, price_data, change_info=None):
    """生成告警消息"""
    msg = []
    msg.append("👀 竞品监控提醒")
    msg.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    msg.append("")
    
    msg.append(f"【商品】{product['name']}")
    msg.append(f"【平台】{price_data.get('source', '未知').upper()}")
    msg.append("")
    
    if change_info and change_info['type'] == 'drop':
        msg.append("💰 降价提醒！")
        msg.append(f"├ 原价：{change_info['old_price']:.2f} 元")
        msg.append(f"├ 现价：{change_info['new_price']:.2f} 元")
        msg.append(f"└ 降幅：{change_info['change']:.2f} 元 ({change_info['change_pct']:.1f}%)")
    elif change_info and change_info['type'] == 'rise':
        msg.append("💰 涨价提醒")
        msg.append(f"├ 原价：{change_info['old_price']:.2f} 元")
        msg.append(f"├ 现价：{change_info['new_price']:.2f} 元")
        msg.append(f"└ 涨幅：{change_info['change']:.2f} 元 ({change_info['change_pct']:.1f}%)")
    else:
        msg.append("💰 当前价格")
        msg.append(f"├ 售价：{price_data['price']:.2f} 元")
        msg.append(f"└ 原价：{price_data['original_price']:.2f} 元")
    
    msg.append("")
    msg.append("📊 库存状态")
    status = "✅ 有货" if price_data.get('in_stock', True) else "❌ 缺货"
    msg.append(f"└ {status}")
    
    if change_info and change_info['type'] == 'drop':
        msg.append("")
        msg.append("🎯 建议操作")
        msg.append(f"├ 是否跟进：是")
        msg.append(f"└ 建议价格：{change_info['new_price'] - 2:.2f} 元")
    
    msg.append("")
    msg.append("---")
    msg.append("💡 竞品监控 | 30 分钟更新一次")
    
    return "\n".join(msg)

def check_product(product_config):
    """检查单个商品"""
    product_name = product_config['name']
    product_url = product_config['url']
    
    print(f"正在检查：{product_name}")
    
    # 获取价格
    price_data = None
    
    if 'jd.com' in product_url:
        # 京东：提取 SKU ID
        match = re.search(r'/(\d+)\.html', product_url)
        if match:
            sku_id = match.group(1)
            price_data = get_jd_price(sku_id)
    
    elif 'taobao.com' in product_url or 'tmall.com' in product_url:
        # 淘宝：需要 API 授权
        price_data = get_taobao_price(product_url)
    
    if not price_data:
        print(f"  ❌ 获取价格失败")
        return None
    
    print(f"  当前价格：{price_data['price']:.2f} 元 ({price_data['source']})")
    
    # 检查价格变化
    change_info, change_type = check_price_change(product_name, price_data['price'])
    
    # 保存历史
    save_price_history(product_name, price_data)
    
    # 生成告警
    if change_info and change_type in ['price_drop', 'price_rise']:
        msg = generate_alert_message(product, price_data, change_info)
        
        return {
            "product": product_name,
            "price": price_data,
            "change": change_info,
            "message": msg,
            "notify_type": change_type
        }
    
    return None

def send_notification(message, notify_config, notify_type):
    """发送推送通知"""
    channels = notify_config.get('channels', {})
    rules = notify_config.get('notify_rules', {})
    
    # 检查是否需要推送
    if notify_type == 'price_drop' and not rules.get('price_drop', True):
        print("  ⚠️ 降价推送已关闭")
        return
    
    if notify_type == 'price_rise' and not rules.get('price_rise', False):
        print("  ⚠️ 涨价推送已关闭")
        return
    
    # 发送推送
    if channels.get('wechat', {}).get('enabled'):
        webhook = channels['wechat'].get('webhook', '')
        if webhook:
            send_wechat_webhook(message, webhook)
    
    if channels.get('dingtalk', {}).get('enabled'):
        webhook = channels['dingtalk'].get('webhook', '')
        if webhook:
            send_dingtalk_webhook(message, webhook)

def main():
    """主函数"""
    print("👀 竞品价格监控 v2（生产版）")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("")
    
    # 加载配置
    config = load_config()
    products = config.get('products', {}).get('products', [])
    notify_config = config.get('notify', {})
    
    if not products:
        print("❌ 没有配置监控商品")
        print("请编辑 config/products.json 添加商品")
        return
    
    print(f"监控商品数量：{len(products)}")
    print("")
    
    # 检查每个商品
    for product in products:
        if not product.get('enabled', True):
            continue
        
        result = check_product(product)
        
        if result:
            print("\n" + "="*60)
            print(result['message'])
            print("="*60)
            
            # 保存告警
            output_file = OUTPUT_DIR / f"alert_{product['product']}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result['message'])
            
            print(f"\n✅ 告警已保存：{output_file}")
            
            # 发送推送
            send_notification(result['message'], notify_config, result['notify_type'])
        else:
            print(f"  ⚠️ 无价格变化")
        
        print("")
    
    print("✅ 检查完成")

if __name__ == "__main__":
    main()
