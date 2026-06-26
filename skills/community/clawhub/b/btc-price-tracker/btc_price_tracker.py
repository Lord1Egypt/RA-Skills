#!/usr/bin/env python3
"""
BTC Price Tracker - OpenClaw Skill
实时比特币价格监控和警报系统
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import Optional, Dict, List, Any
import requests

# 配置
ALERTS_FILE = os.path.join(os.path.dirname(__file__), "alerts.json")
API_URL = "https://api.coingecko.com/api/v3/simple/price"
LANGUAGE = os.environ.get("OPENCLAW_LANG", "zh")  # 默认中文


def get_btc_price() -> Optional[Dict[str, Any]]:
    """获取比特币实时价格"""
    try:
        response = requests.get(
            API_URL,
            params={"ids": "bitcoin", "vs_currencies": "usd,cny,sgd", "include_24hr_change": "true"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("bitcoin")
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误：{e}")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ 数据解析错误：{e}")
        return None


def format_price(price: float, currency: str = "USD") -> str:
    """格式化价格显示"""
    if currency.upper() == "USD":
        return f"${price:,.2f}"
    elif currency.upper() == "CNY":
        return f"¥{price:,.2f}"
    elif currency.upper() == "SGD":
        return f"S${price:,.2f}"
    return f"{price:,.2f} {currency}"


def format_change(change: float) -> str:
    """格式化涨跌幅显示"""
    symbol = "📈" if change >= 0 else "📉"
    return f"{symbol} {change:.2f}%"


def load_alerts() -> List[Dict[str, Any]]:
    """加载警报列表"""
    if not os.path.exists(ALERTS_FILE):
        return []
    try:
        with open(ALERTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ 读取警报文件失败：{e}")
        return []


def save_alerts(alerts: List[Dict[str, Any]]) -> bool:
    """保存警报列表"""
    try:
        with open(ALERTS_FILE, "w", encoding="utf-8") as f:
            json.dump(alerts, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"❌ 保存警报失败：{e}")
        return False


def check_alerts(price_data: Dict[str, Any]) -> List[str]:
    """检查是否触发警报"""
    alerts = load_alerts()
    triggered = []
    
    usd_price = price_data.get("usd", 0)
    cny_price = price_data.get("cny", 0)
    sgd_price = price_data.get("sgd", 0)
    
    for alert in alerts:
        if alert.get("active", False):
            currency = alert.get("currency", "USD").upper()
            target_price = alert.get("price", 0)
            condition = alert.get("condition", "above")
            
            if currency == "USD":
                current_price = usd_price
            elif currency == "CNY":
                current_price = cny_price
            elif currency == "SGD":
                current_price = sgd_price
            else:
                continue
            
            triggered_flag = False
            if condition == "above" and current_price >= target_price:
                triggered_flag = True
            elif condition == "below" and current_price <= target_price:
                triggered_flag = True
            
            if triggered_flag:
                msg = f"🚨 警报触发！{alert.get('name', '警报')}：当前价格 {format_price(current_price, currency)} {condition} {format_price(target_price, currency)}"
                triggered.append(msg)
    
    return triggered


def add_alert(name: str, price: float, condition: str, currency: str = "USD") -> bool:
    """添加新警报"""
    if condition not in ["above", "below"]:
        print("❌ 条件必须是 'above' 或 'below'")
        return False
    
    alerts = load_alerts()
    alert_id = len(alerts) + 1
    
    new_alert = {
        "id": alert_id,
        "name": name,
        "price": price,
        "condition": condition,
        "currency": currency,
        "active": True,
        "created_at": datetime.now().isoformat()
    }
    
    alerts.append(new_alert)
    if save_alerts(alerts):
        print(f"✅ 警报已添加：{name} - 当价格 {condition} {format_price(price, currency)} 时通知")
        return True
    return False


def list_alerts() -> None:
    """列出所有警报"""
    alerts = load_alerts()
    if not alerts:
        print("📭 暂无警报")
        return
    
    print("\n📋 当前警报列表：")
    print("-" * 60)
    for alert in alerts:
        status = "✅" if alert.get("active", False) else "❌"
        condition_text = "高于" if alert.get("condition") == "above" else "低于"
        print(f"{status} #{alert['id']} {alert['name']}")
        print(f"   条件：当价格 {condition_text} {format_price(alert['price'], alert['currency'])}")
        print(f"   创建：{alert.get('created_at', '未知')[:19]}")
    print("-" * 60)


def delete_alert(alert_id: int) -> bool:
    """删除警报"""
    alerts = load_alerts()
    found = False
    new_alerts = []
    
    for alert in alerts:
        if alert.get("id") == alert_id:
            found = True
            print(f"🗑️ 已删除警报：{alert.get('name')}")
        else:
            new_alerts.append(alert)
    
    if found:
        save_alerts(new_alerts)
    else:
        print(f"❌ 未找到 ID 为 {alert_id} 的警报")
    
    return found


def show_price(show_change: bool = True) -> None:
    """显示当前价格"""
    price_data = get_btc_price()
    if not price_data:
        return
    
    usd = price_data.get("usd", 0)
    cny = price_data.get("cny", 0)
    sgd = price_data.get("sgd", 0)
    
    print("\n💰 比特币当前价格：")
    print(f"  USD: {format_price(usd)}")
    print(f"  CNY: {format_price(cny)}")
    print(f"  SGD: {format_price(sgd)}")
    
    if show_change and "usd_24h_change" in price_data:
        change = price_data["usd_24h_change"]
        print(f"  24h 变化：{format_change(change)}")
    
    # 检查警报
    triggered = check_alerts(price_data)
    if triggered:
        print("\n" + "\n".join(triggered))


def send_telegram_message(message: str) -> bool:
    """发送 Telegram 消息（通过 OpenClaw 主程序）"""
    # 在 OpenClaw 环境中，这会被主程序处理
    # 这里只是打印，实际发送由主程序完成
    print(f"\n📱 [Telegram 通知] {message}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="BTC Price Tracker - 比特币价格监控和警报",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s price                    查看当前价格
  %(prog)s alert --name "高价警报" --price 100000 --condition above
  %(prog)s alerts                   列出所有警报
  %(prog)s delete 1                 删除 ID 为 1 的警报
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 价格命令
    subparsers.add_parser("price", help="查看当前比特币价格")
    
    # 添加警报
    alert_parser = subparsers.add_parser("alert", help="添加价格警报")
    alert_parser.add_argument("--name", "-n", required=True, help="警报名称")
    alert_parser.add_argument("--price", "-p", type=float, required=True, help="目标价格")
    alert_parser.add_argument("--condition", "-c", choices=["above", "below"], 
                             default="above", help="触发条件：above(高于) 或 below(低于)")
    alert_parser.add_argument("--currency", "-C", choices=["USD", "CNY", "SGD"],
                             default="USD", help="货币单位")
    
    # 列出警报
    subparsers.add_parser("alerts", help="列出所有警报")
    
    # 删除警报
    delete_parser = subparsers.add_parser("delete", help="删除警报")
    delete_parser.add_argument("id", type=int, help="要删除的警报 ID")
    
    # 检查警报
    subparsers.add_parser("check", help="检查是否触发警报")
    
    args = parser.parse_args()
    
    if args.command == "price":
        show_price()
    
    elif args.command == "alert":
        add_alert(args.name, args.price, args.condition, args.currency)
    
    elif args.command == "alerts":
        list_alerts()
    
    elif args.command == "delete":
        delete_alert(args.id)
    
    elif args.command == "check":
        price_data = get_btc_price()
        if price_data:
            triggered = check_alerts(price_data)
            if triggered:
                print("\n".join(triggered))
            else:
                print("✅ 暂无触发的警报")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
