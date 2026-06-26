#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQQ 期权监控与飞书推送
功能：实时监控 QQQ 价格，关键价位突破时推送
"""

import time
import httpx
from datetime import datetime
from longport.openapi import QuoteContext, Config
import os
from dotenv import load_dotenv

load_dotenv()

# ============ 配置 ============
# 长桥 API
LONGPORT_APP_KEY = os.getenv('LONGPORT_APP_KEY')
LONGPORT_APP_SECRET = os.getenv('LONGPORT_APP_SECRET')
LONGPORT_ACCESS_TOKEN = os.getenv('LONGPORT_ACCESS_TOKEN')

# 飞书 API
FEISHU_APP_ID = "cli_a92c2ade9ff99bd2"
FEISHU_APP_SECRET = "1SNIOfQTlKN2pCD2bWOlLhmIzF58C6gG"
FEISHU_USER_OPEN_ID = "ou_c3f01a621b3fef9a2b59368233bf7647"  # 房总的 open_id

# QQQ 关键价位
QQQ_SUPPORT = 595.08  # 支撑位（日内低点）
QQQ_RESISTANCE = 599.39  # 阻力位（日内高点）
QQQ_TARGET1 = 590.00  # 第一目标
QQQ_TARGET2 = 585.00  # 第二目标

# 推送间隔（秒）
PUSH_INTERVAL = 1800  # 30 分钟

# ============ 全局变量 ============
last_push_time = 0
last_price = 0
breakout_notified = {"support": False, "resistance": False}

# ============ 飞书推送函数 ============

def get_feishu_token():
    """获取飞书 Access Token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    response = httpx.post(url, json=payload, timeout=10)
    result = response.json()
    if result.get("code") == 0:
        return result.get("tenant_access_token")
    return None

def send_qqq_update(token, price, change, change_rate, high, low, volume, signal=None):
    """发送 QQQ 更新到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 确定颜色和 emoji
    if change >= 0:
        color = "green"
        emoji = "🟢"
    else:
        color = "red"
        emoji = "🔴"
    
    # 信号提示
    signal_text = ""
    if signal:
        signal_text = f"""
{{"tag": "div", "text": {{"tag": "lark_md", "content": "**⚠️ 信号:**\\n{signal}"}}}}
,"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    card_content = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"{emoji} QQQ 实时监控"},
            "template": color
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**现价**\\n${price:.2f}"}},
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**涨跌**\\n{change:+.2f} ({change_rate:+.2f}%)"}},
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**最高**\\n${high:.2f}"}},
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**最低**\\n${low:.2f}"}},
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**成交量**\\n{volume/1000000:.1f}M"}},
                    {"is_short": True, "text": {"tag": "lark_md", "content": f"**时间**\\n{now}"}}
                ]
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📊 关键价位**\\n\\n• 阻力位：${QQQ_RESISTANCE:.2f}（突破→看涨）\\n• 支撑位：${QQQ_SUPPORT:.2f}（跌破→看跌）\\n• 目标 1：${QQQ_TARGET1:.2f}\\n• 目标 2：${QQQ_TARGET2:.2f}"
                }
            },
            signal_text,
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**🎯 期权策略**\\n\\n当前建议：**QQQ Put**（看跌）\\n\\n行权价：$590 | 到期：本周五\\n止损：突破${QQQ_RESISTANCE:.2f}"
                }
            },
            {
                "tag": "note",
                "elements": [{"tag": "plain_text", "content": f"量化交易助手 · 自动推送 | 下次更新：30 分钟后"}]
            }
        ]
    }
    
    # 移除空的 signal_text 元素
    elements = [e for e in card_content["elements"] if e.get("tag") != "div" or e.get("text", {}).get("content", "").strip()]
    card_content["elements"] = elements
    
    payload = {
        "receive_id_type": "open_id",
        "receive_id": FEISHU_USER_OPEN_ID,
        "msg_type": "interactive",
        "content": card_content
    }
    
    response = httpx.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    return result

def send_breakout_alert(token, direction, price):
    """发送突破警报"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    if direction == "up":
        emoji = "🚀"
        title = "QQQ 突破阻力位"
        color = "green"
        content = f"**突破确认！**\\n\\nQQQ 突破阻力位 ${QQQ_RESISTANCE:.2f}\\n现价：${price:.2f}\\n\\n**操作建议：**\\n• Put 期权止损\\n• 考虑 Call 期权机会"
    else:
        emoji = "📉"
        title = "QQQ 跌破支撑位"
        color = "red"
        content = f"**跌破确认！**\\n\\nQQQ 跌破支撑位 ${QQQ_SUPPORT:.2f}\\n现价：${price:.2f}\\n\\n**操作建议：**\\n• Put 期权加仓机会\\n• 目标：${QQQ_TARGET1:.2f}"
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    card_content = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"{emoji} {title}"},
            "template": color
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            },
            {
                "tag": "note",
                "elements": [{"tag": "plain_text", "content": f"量化交易助手 · 突破警报 | {now}"}]
            }
        ]
    }
    
    payload = {
        "receive_id_type": "open_id",
        "receive_id": FEISHU_USER_OPEN_ID,
        "msg_type": "interactive",
        "content": card_content
    }
    
    response = httpx.post(url, headers=headers, json=payload, timeout=10)
    result = response.json()
    return result

# ============ 监控主循环 ============

def main():
    print("=" * 60)
    print("📊 QQQ 期权监控与飞书推送")
    print("=" * 60)
    print(f"\n监控标的：QQQ")
    print(f"支撑位：${QQQ_SUPPORT:.2f}")
    print(f"阻力位：${QQQ_RESISTANCE:.2f}")
    print(f"推送间隔：{PUSH_INTERVAL/60:.0f} 分钟")
    print(f"推送目标：房总 (ou_c3f01a621b3fef9a2b59368233bf7647)")
    print("\n开始监控...\n")
    
    # 配置长桥
    config = Config(
        app_key=LONGPORT_APP_KEY,
        app_secret=LONGPORT_APP_SECRET,
        access_token=LONGPORT_ACCESS_TOKEN
    )
    
    global last_push_time, breakout_notified
    last_push_time = time.time()  # 立即推送第一条
    
    push_count = 0
    
    while True:
        try:
            # 获取行情
            with QuoteContext(config) as qc:
                qqq = qc.quote("QQQ")
                price = qqq.last_done
                change = qqq.change
                change_rate = qqq.change_rate
                high = qqq.high
                low = qqq.low
                volume = qqq.volume
                
                now = time.time()
                
                # 获取飞书 Token
                token = get_feishu_token()
                if not token:
                    print("❌ 获取飞书 Token 失败")
                    time.sleep(60)
                    continue
                
                # 检查突破
                # 支撑位跌破
                if price < QQQ_SUPPORT and not breakout_notified["support"]:
                    print(f"📉 跌破支撑位：${price:.2f}")
                    send_breakout_alert(token, "down", price)
                    breakout_notified["support"] = True
                    breakout_notified["resistance"] = False
                    last_push_time = now
                    push_count += 1
                
                # 阻力位突破
                elif price > QQQ_RESISTANCE and not breakout_notified["resistance"]:
                    print(f"🚀 突破阻力位：${price:.2f}")
                    send_breakout_alert(token, "up", price)
                    breakout_notified["resistance"] = True
                    breakout_notified["support"] = False
                    last_push_time = now
                    push_count += 1
                
                # 定期推送（30 分钟）
                elif now - last_push_time >= PUSH_INTERVAL:
                    print(f"📊 定期推送 #{push_count + 1}：${price:.2f} ({change_rate*100:+.2f}%)")
                    signal = "看跌（支撑位附近）" if price < QQQ_SUPPORT + 2 else "观望（区间震荡）"
                    result = send_qqq_update(token, price, change, change_rate, high, low, volume, signal)
                    if result.get("code") == 0:
                        print("✅ 推送成功！")
                        push_count += 1
                    else:
                        print(f"❌ 推送失败：{result}")
                    last_push_time = now
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] QQQ: ${price:.2f} | 下次推送：{int((last_push_time + PUSH_INTERVAL - now)/60)} 分钟")
            
            time.sleep(60)  # 每分钟检查一次
            
        except KeyboardInterrupt:
            print(f"\n👋 停止监控，共推送 {push_count} 次")
            break
        except Exception as e:
            print(f"❌ 错误：{e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
