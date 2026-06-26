#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书推送模块
功能：交易通知、持仓日报、策略信号
"""

import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

# ============ 配置 ============
# 飞书应用凭证（请从环境变量读取，勿硬编码）
# export FEISHU_APP_ID="your_app_id"
# export FEISHU_APP_SECRET="your_app_secret"
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")

# 机器人 Webhook URL（需要从事件与回调页面获取）
# 暂时使用应用内建的消息发送 API
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")  # 留空，使用 API 方式发送

# ============ 消息模板 ============

def format_trade_notification(order: Dict) -> Dict:
    """交易通知"""
    side_emoji = "🟢" if order["side"] == "Buy" else "🔴"
    side_text = "买入" if order["side"] == "Buy" else "卖出"
    
    content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{side_emoji} 交易执行通知"
                },
                "template": "blue" if order["side"] == "Buy" else "red"
            },
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**股票:**\n{order['symbol']} {order.get('name', '')}"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**方向:**\n{side_text}"}}
                    ]
                },
                {
                    "tag": "div",
                    "fields": [
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**数量:**\n{order['quantity']}股"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**价格:**\n{order['currency']} {order['price']:.3f}"}}
                    ]
                },
                {
                    "tag": "div",
                    "fields": [
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**金额:**\n{order['currency']} {order['amount']:,.2f}"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**策略:**\n{order.get('strategy', '手动')}"}}
                    ]
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**时间:** {order['timestamp']}\n**状态:** {order.get('status', '已提交')}"
                    }
                }
            ]
        }
    }
    return content

def format_daily_report(positions: List[Dict], cash: float, total_value: float, pnl: float) -> Dict:
    """持仓日报"""
    date = datetime.now().strftime("%Y-%m-%d")
    pnl_emoji = "📈" if pnl >= 0 else "📉"
    pnl_color = "green" if pnl >= 0 else "red"
    
    # 持仓列表
    position_rows = []
    for pos in positions:
        stock_pnl = pos.get("pnl", 0)
        stock_pnl_emoji = "🟢" if stock_pnl >= 0 else "🔴"
        position_rows.append({
            "tag": "tr",
            "cells": [
                {"tag": "td", "text": {"tag": "plain_text", "content": pos["symbol"]}},
                {"tag": "td", "text": {"tag": "plain_text", "content": pos.get("name", "")}},
                {"tag": "td", "text": {"tag": "plain_text", "content": str(pos["quantity"]}},
                {"tag": "td", "text": {"tag": "plain_text", "content": f"{pos['cost_price']:.3f}"}},
                {"tag": "td", "text": {"tag": "plain_text", "content": f"{pos['current_price']:.3f}"}},
                {"tag": "td", "text": {"tag": "plain_text", "content": f"{stock_pnl_emoji} {stock_pnl:+.2f} ({pos['pnl_rate']:+.2%})"}}
            ]
        })
    
    content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📊 持仓日报 ({date})"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**总资产:**\n{total_value:,.2f}"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**现金:**\n{cash:,.2f}"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**持仓市值:**\n{total_value - cash:,.2f}"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**今日盈亏:**\n{pnl_emoji} {pnl:+,.2f}"}}
                    ]
                },
                {
                    "tag": "table",
                    "header": ["代码", "名称", "数量", "成本", "现价", "盈亏"],
                    "rows": position_rows,
                    "column_width": [1, 2, 1, 1, 1, 2]
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": f"更新时间：{datetime.now().strftime('%H:%M:%S')} | 数据来源：长桥 OpenAPI"
                        }
                    ]
                }
            ]
        }
    }
    return content

def format_signal_notification(signal: Dict) -> Dict:
    """策略信号通知"""
    signal_type = signal.get("type", "未知")
    signal_emoji = "🟢" if signal["action"] == "Buy" else "🔴"
    
    content = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{signal_emoji} 策略信号 - {signal_type}"
                },
                "template": "green" if signal["action"] == "Buy" else "red"
            },
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**股票:**\n{signal['symbol']}"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**信号:**\n{signal['action']}"}}
                    ]
                },
                {
                    "tag": "div",
                    "fields": [
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**现价:**\n{signal['price']:.3f}"}},
                        {"is_short": True, "text": {"tag": "lark_md", "content": f"**理由:**\n{signal.get('reason', 'N/A')}"}}
                    ]
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**策略:** {signal.get('strategy', 'N/A')} | **时间:** {signal['timestamp']}"
                    }
                }
            ]
        }
    }
    return content

# ============ 发送函数 ============

def send_message(content: Dict) -> bool:
    """发送飞书消息"""
    if not FEISHU_WEBHOOK_URL:
        print("⚠️  飞书 Webhook URL 未配置，跳过发送")
        return False
    
    try:
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            json=content,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("✅ 飞书消息发送成功")
                return True
            else:
                print(f"❌ 飞书消息发送失败：{result}")
                return False
        else:
            print(f"❌ HTTP 错误：{response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送异常：{e}")
        return False

def notify_trade(order: Dict) -> bool:
    """发送交易通知"""
    content = format_trade_notification(order)
    return send_message(content)

def notify_daily_report(positions: List[Dict], cash: float, total_value: float, pnl: float) -> bool:
    """发送持仓日报"""
    content = format_daily_report(positions, cash, total_value, pnl)
    return send_message(content)

def notify_signal(signal: Dict) -> bool:
    """发送策略信号"""
    content = format_signal_notification(signal)
    return send_message(content)

# ============ 测试 ============

if __name__ == "__main__":
    print("飞书推送模块测试")
    print("=" * 60)
    
    # 测试交易通知
    test_order = {
        "symbol": "700.HK",
        "name": "腾讯控股",
        "side": "Buy",
        "quantity": 100,
        "price": 514.0,
        "currency": "HKD",
        "amount": 51400.0,
        "strategy": "均值回归",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "已成交"
    }
    
    print("\n1. 测试交易通知...")
    # notify_trade(test_order)
    print("⚠️  请先配置 FEISHU_WEBHOOK_URL")
    
    print("\n" + "=" * 60)
    print("配置说明:")
    print("1. 在飞书群聊创建自定义机器人")
    print("2. 复制 Webhook URL")
    print("3. 填入 feishu_push.py 的 FEISHU_WEBHOOK_URL 变量")
