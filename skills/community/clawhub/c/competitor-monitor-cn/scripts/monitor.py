#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品价格监控 - 核心脚本 v1
支持：淘宝/京东/拼多多/亚马逊
"""

import json
import os
import sys
import requests
import re
from datetime import datetime, timedelta
from pathlib import Path

# 不依赖 BeautifulSoup，用正则解析 HTML

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"

def load_config():
    """加载配置"""
    config_file = CONFIG_DIR / "products.json"
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "products": [
            {
                "name": "测试商品",
                "url": "https://item.taobao.com/item.htm?id=123456",
                "platform": "taobao",
                "target_price": 59.9,
                "check_interval": 30
            }
        ]
    }

def get_taobao_price(url):
    """获取淘宝/天猫价格（正则解析）"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html = response.text
            
            # 正则匹配价格
            price_patterns = [
                r'"price":["\']?([\d.]+)',  # JSON 格式
                r'data-price=["\']([\d.]+)["\']',  # data 属性
                r'￥\s*([\d.]+)',  # ￥符号
                r'([\d.]+)\s*元',  # 元单位
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, html)
                if match:
                    price = float(match.group(1))
                    if price > 0:
                        return {
                            "price": price,
                            "original_price": price,
                            "currency": "CNY",
                            "in_stock": True,
                            "source": "淘宝/天猫"
                        }
            
            return None
            
    except Exception as e:
        print(f"  淘宝接口失败：{e}")
    
    return None

def get_jd_price(url):
    """获取京东价格"""
    try:
        # 京东价格通常是异步加载，需要调用 API
        # 提取商品 ID
        match = re.search(r'/(\d+)\.html', url)
        if match:
            sku_id = match.group(1)
            
            # 京东价格 API
            api_url = f"https://p.3.cn/prices/mgets?skuIds=J_{sku_id}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    price = float(data[0].get('p', 0)) / 100  # 京东价格是分
                    return {
                        "price": price,
                        "original_price": price,
                        "currency": "CNY",
                        "in_stock": True,
                        "source": "京东"
                    }
    except Exception as e:
        print(f"  京东接口失败：{e}")
    
    return None

def get_pdd_price(url):
    """获取拼多多价格"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X)"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 拼多多价格通常在 data-price 属性中
            match = re.search(r'data-price=["\']([\d.]+)["\']', response.text)
            if match:
                price = float(match.group(1))
                return {
                    "price": price,
                    "original_price": price,
                    "currency": "CNY",
                    "in_stock": True,
                    "source": "拼多多"
                }
    except Exception as e:
        print(f"  拼多多接口失败：{e}")
    
    return None

def get_amazon_price(url):
    """获取亚马逊价格（正则解析）"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html = response.text
            
            # 正则匹配亚马逊价格
            price_patterns = [
                r'"priceAmount":[\s]*([\d.]+)',  # JSON 格式
                r'\$([\d.]+)',  # 美元符号
                r'€([\d.]+)',  # 欧元符号
                r'([\d.]+)\s*美元',  # 美元单位
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, html)
                if match:
                    price = float(match.group(1))
                    if price > 0:
                        return {
                            "price": price,
                            "original_price": price,
                            "currency": "USD",
                            "in_stock": True,
                            "source": "亚马逊"
                        }
    except Exception as e:
        print(f"  亚马逊接口失败：{e}")
    
    return None

def extract_price(text):
    """从文本中提取价格"""
    # 匹配价格模式：¥123.45 或 123.45 元
    patterns = [
        r'¥?\s*([\d,]+\.?\d*)',  # ¥123.45
        r'([\d,]+\.?\d*)\s*元',   # 123.45 元
        r'([\d,]+\.?\d*)',        # 纯数字
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            price_str = match.group(1).replace(',', '')
            try:
                price = float(price_str)
                if price > 0:
                    return price
            except ValueError:
                pass
    
    return 0

def get_product_price(product_config):
    """获取商品价格（多平台）"""
    url = product_config['url']
    platform = product_config.get('platform', 'taobao')
    
    if 'taobao.com' in url or 'tmall.com' in url:
        return get_taobao_price(url)
    elif 'jd.com' in url:
        return get_jd_price(url)
    elif 'pinduoduo.com' in url or 'yangkeduo.com' in url:
        return get_pdd_price(url)
    elif 'amazon' in url:
        return get_amazon_price(url)
    else:
        # 通用尝试
        return get_taobao_price(url)

def check_price_change(current_price, history):
    """检查价格变化"""
    if not history:
        return None, "new"
    
    last_price = history[-1].get('price', 0)
    last_time = history[-1].get('time', '')
    
    if current_price < last_price:
        change = last_price - current_price
        change_pct = (change / last_price * 100) if last_price > 0 else 0
        return {
            "type": "drop",
            "old_price": last_price,
            "new_price": current_price,
            "change": change,
            "change_pct": change_pct,
            "last_time": last_time
        }, "price_drop"
    
    elif current_price > last_price:
        change = current_price - last_price
        change_pct = (change / last_price * 100) if last_price > 0 else 0
        return {
            "type": "rise",
            "old_price": last_price,
            "new_price": current_price,
            "change": change,
            "change_pct": change_pct,
            "last_time": last_time
        }, "price_rise"
    
    return None, "unchanged"

def generate_alert_message(product_name, platform, price_data, change_info):
    """生成告警消息"""
    msg = []
    msg.append("👀 竞品监控提醒")
    msg.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    msg.append("")
    
    msg.append(f"【商品】{product_name}")
    msg.append(f"【平台】{platform}")
    msg.append("")
    
    if change_info['type'] == 'drop':
        msg.append("💰 降价提醒！")
        msg.append(f"├ 原价：{change_info['old_price']:.2f} 元")
        msg.append(f"├ 现价：{change_info['new_price']:.2f} 元")
        msg.append(f"└ 降幅：{change_info['change']:.2f} 元 ({change_info['change_pct']:.1f}%)")
    elif change_info['type'] == 'rise':
        msg.append("💰 涨价提醒")
        msg.append(f"├ 原价：{change_info['old_price']:.2f} 元")
        msg.append(f"├ 现价：{change_info['new_price']:.2f} 元")
        msg.append(f"└ 涨幅：{change_info['change']:.2f} 元 ({change_info['change_pct']:.1f}%)")
    else:
        msg.append(f"💰 当前价格：{price_data['price']:.2f} 元")
    
    msg.append("")
    msg.append("🎯 建议操作")
    if change_info['type'] == 'drop':
        msg.append(f"├ 是否跟进：是")
        msg.append(f"└ 建议价格：{change_info['new_price'] - 1:.2f} 元（略低于竞品）")
    else:
        msg.append(f"└ 维持原价或适当上调")
    
    msg.append("")
    msg.append("---")
    msg.append("💡 竞品监控 | 实时追踪市场动态")
    
    return "\n".join(msg)

def save_price_history(product_name, price_data):
    """保存价格历史"""
    history_file = SCRIPT_DIR / "output" / f"history_{product_name}.json"
    history_file.parent.mkdir(exist_ok=True)
    
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
    
    # 保留最近 100 条记录
    history = history[-100:]
    
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return history

def check_product(product_config):
    """检查单个商品"""
    product_name = product_config['name']
    product_url = product_config['url']
    
    print(f"正在检查：{product_name}")
    
    # 获取价格
    price_data = get_product_price(product_config)
    
    if not price_data:
        print(f"  ❌ 获取价格失败")
        return None
    
    print(f"  当前价格：{price_data['price']:.2f} 元 ({price_data['source']})")
    
    # 加载历史
    history_file = SCRIPT_DIR / "output" / f"history_{product_name}.json"
    history = []
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    
    # 检查价格变化
    change_info, change_type = check_price_change(price_data['price'], history)
    
    # 保存历史
    save_price_history(product_name, price_data)
    
    # 生成告警
    if change_info and change_type in ['price_drop', 'price_rise']:
        msg = generate_alert_message(
            product_name,
            price_data['source'],
            price_data,
            change_info
        )
        
        return {
            "product": product_name,
            "price": price_data,
            "change": change_info,
            "message": msg
        }
    
    return None

def main():
    """主函数"""
    print("👀 竞品价格监控 v1")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("")
    
    # 加载配置
    config = load_config()
    
    # 检查每个商品
    for product in config.get('products', []):
        if not product.get('enabled', True):
            continue
        
        result = check_product(product)
        
        if result:
            print("\n" + "="*60)
            print(result['message'])
            print("="*60)
            
            # 保存到文件
            output_dir = SCRIPT_DIR / "output"
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"alert_{product['product']}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result['message'])
            
            print(f"\n✅ 告警已保存：{output_file}")
        else:
            print(f"  ⚠️ 无价格变化")
    
    print("\n✅ 检查完成")

if __name__ == "__main__":
    main()
