#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息推送模块

支持：
- 钉钉机器人
- 钉钉个人消息（通过 OpenClaw）
"""

import requests
import json
from datetime import datetime
from typing import Optional, List

# ============== 钉钉机器人 ==============
def send_dingtalk_webhook(message: str, webhook_url: str = None) -> bool:
    """
    通过钉钉机器人 Webhook 发送消息
    
    Args:
        message: 消息内容
        webhook_url: Webhook URL
    
    Returns:
        是否成功
    """
    if not webhook_url:
        print("[钉钉 Webhook] 未配置 Webhook URL")
        return False
    
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        
        response = requests.post(webhook_url, headers=headers, json=data, timeout=10)
        result = response.json()
        
        if result.get("errcode") == 0:
            print(f"[钉钉推送] 发送成功")
            return True
        else:
            print(f"[钉钉推送] 发送失败：{result}")
            return False
    
    except Exception as e:
        print(f"[钉钉推送] 异常：{e}")
        return False


def send_dingtalk_markdown(title: str, text: str, webhook_url: str = None, 
                           at_all: bool = False) -> bool:
    """
    发送钉钉 Markdown 消息
    
    Args:
        title: 标题
        text: Markdown 内容
        webhook_url: Webhook URL
        at_all: 是否@所有人
    
    Returns:
        是否成功
    """
    if not webhook_url:
        return False
    
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "isAtAll": at_all
            }
        }
        
        response = requests.post(webhook_url, headers=headers, json=data, timeout=10)
        result = response.json()
        
        if result.get("errcode") == 0:
            return True
        else:
            print(f"[钉钉 Markdown] 发送失败：{result}")
            return False
    
    except Exception as e:
        print(f"[钉钉 Markdown] 异常：{e}")
        return False


# ============== 钉钉个人消息 (通过 OpenClaw) ==============
def send_dingtalk_personal(message: str, user_id: str = "235135121537852951") -> bool:
    """
    发送钉钉个人消息（通过 OpenClaw message 工具）
    
    注意：这个函数需要在 OpenClaw 环境中调用 message 工具
    
    Args:
        message: 消息内容
        user_id: 钉钉用户 ID
    
    Returns:
        是否成功
    """
    # 这个函数会在 OpenClaw 环境中被替换为实际的 message 工具调用
    # 示例代码：
    # from openclaw import message
    # message(action="send", channel="dingtalk", target=user_id, message=message)
    
    print(f"[钉钉个人消息] 准备发送给 {user_id}: {message[:50]}...")
    return True


# ============== 预警推送 ==============
def send_price_alert_notification(stock_code: str, stock_name: str, 
                                   current_price: float, target_price: float,
                                   direction: str, user_id: str = None) -> bool:
    """
    发送价格预警通知
    
    Args:
        stock_code: 股票代码
        stock_name: 股票名称
        current_price: 当前价格
        target_price: 目标价格
        direction: 方向 (up/down)
        user_id: 用户 ID
    
    Returns:
        是否成功
    """
    direction_str = "📈 涨至" if direction == "up" else "📉 跌至"
    emoji = "🚨"
    
    message = f"""{emoji}【价格预警触发】

📈 {stock_name} ({stock_code})
💰 当前价：¥{current_price:.2f}
🎯 目标价：¥{target_price:.2f} ({direction_str})
⏰ 触发时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️ 请及时关注行情变化！"""
    
    # 优先尝试个人消息
    if user_id:
        return send_dingtalk_personal(message, user_id)
    
    return True


def send_abnormal_stock_notification(abnormal_stocks: List[dict], user_id: str = None) -> bool:
    """
    发送异动股票通知
    
    Args:
        abnormal_stocks: 异动股票列表
        user_id: 用户 ID
    
    Returns:
        是否成功
    """
    if not abnormal_stocks:
        return True
    
    message = f"""⚠️【异动股票监控】

发现 {len(abnormal_stocks)} 只异动股票:

"""
    
    for stock in abnormal_stocks:
        change_emoji = "📈" if stock["change_pct"] > 0 else "📉"
        message += f"""{change_emoji} {stock['name']} ({stock['code']})
   现价：¥{stock['price']:.2f} ({stock['change_pct']:+.2f}%)
   原因：{' | '.join(stock['reasons'])}

"""
    
    message += f"\n⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    if user_id:
        return send_dingtalk_personal(message, user_id)
    
    return True


def send_daily_report_notification(report: str, user_id: str = None) -> bool:
    """
    发送每日报告通知
    
    Args:
        report: 日报内容
        user_id: 用户 ID
    
    Returns:
        是否成功
    """
    # 截取部分内容作为预览
    preview = report[:200].replace('\n', ' ') + "..."
    
    message = f"""📊【A 股投资日报】

{preview}

⏰ 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 完整报告请查看 OpenClaw"""
    
    if user_id:
        return send_dingtalk_personal(message, user_id)
    
    return True


# ============== 测试 ==============
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("消息推送模块测试")
    print("=" * 60)
    
    # 测试价格预警
    print("\n[测试] 价格预警通知")
    send_price_alert_notification(
        stock_code="002892",
        stock_name="科力尔",
        current_price=12.50,
        target_price=12.00,
        direction="down",
        user_id="235135121537852951"
    )
    
    # 测试异动股票
    print("\n[测试] 异动股票通知")
    abnormal = [
        {
            "code": "300059",
            "name": "东方财富",
            "price": 22.50,
            "change_pct": 6.5,
            "reasons": ["涨跌幅 +6.50%"]
        }
    ]
    send_abnormal_stock_notification(abnormal, user_id="235135121537852951")
    
    print("\n✅ 测试完成")
