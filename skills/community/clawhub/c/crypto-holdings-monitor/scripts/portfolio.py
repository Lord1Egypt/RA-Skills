#!/usr/bin/env python3
"""
Crypto Portfolio Tracker - 加密货币持仓追踪工具
"""
import os
import sys
import json
import argparse
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.crypto-portfolio.json")

# 简化版 CoinGecko API（免费，无需 Key）
PRICE_API = "https://api.coingecko.com/api/v3/simple/price"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"wallets": [], "holdings": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_price(coin_id):
    import urllib.request
    import urllib.parse
    url = f"{PRICE_API}?ids={coin_id}&vs_currencies=usd"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get(coin_id, {}).get("usd", 0)
    except Exception as e:
        print(f"❌ 获取价格失败: {e}")
        return 0

def cmd_add(args):
    data = load_data()
    wallet = args.wallet.strip()
    
    if wallet not in data["wallets"]:
        data["wallets"].append(wallet)
        save_data(data)
        print(f"✅ 已添加钱包: {wallet[:10]}...{wallet[-6:]}")
    else:
        print(f"⚠️ 钱包已存在")

def cmd_view(args):
    data = load_data()
    if not data["wallets"]:
        print("📭 暂无钱包")
        return
    
    print("📊 持仓概览")
    print("=" * 40)
    
    # 获取价格
    prices = {}
    for coin in ["bitcoin", "ethereum", "solana", "ripple", "cardano"]:
        prices[coin] = get_price(coin)
        print(f"  {coin}: ${prices[coin]:,}")
    
    print("\n💰 钱包地址:")
    for w in data["wallets"]:
        print(f"   • {w[:12]}...{w[-6:]}")

def cmd_refresh(args):
    print("🔄 刷新价格...")
    for coin in ["bitcoin", "ethereum", "solana"]:
        price = get_price(coin)
        print(f"  {coin}: ${price:,}")

def cmd_report(args):
    data = load_data()
    
    print("📈 加密货币持仓报告")
    print("=" * 50)
    print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # 价格
    prices = {}
    for coin in ["bitcoin", "ethereum", "solana", "ripple", "cardano"]:
        prices[coin] = get_price(coin)
    
    print("💵 当前价格:")
    for coin, price in prices.items():
        print(f"  {coin}: ${price:,.2f}")
    
    print()
    print(f"📪 监控钱包数: {len(data['wallets'])}")

def main():
    parser = argparse.ArgumentParser(description="Crypto Portfolio Tracker")
    subparsers = parser.add_subparsers()
    
    p_add = subparsers.add_parser("add", help="添加钱包地址")
    p_add.add_argument("wallet", help="钱包地址")
    p_add.set_defaults(func=cmd_add)
    
    p_view = subparsers.add_parser("view", help="查看持仓")
    p_view.set_defaults(func=cmd_view)
    
    p_refresh = subparsers.add_parser("refresh", help="刷新价格")
    p_refresh.set_defaults(func=cmd_refresh)
    
    p_report = subparsers.add_parser("report", help="生成报告")
    p_report.set_defaults(func=cmd_report)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
