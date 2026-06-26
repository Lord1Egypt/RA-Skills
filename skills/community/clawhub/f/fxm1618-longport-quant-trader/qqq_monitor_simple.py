#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQQ 简单监控 - 每分钟检查，30 分钟推送一次
"""

import time
import json
from datetime import datetime
from longport.openapi import QuoteContext, Config
import os
from dotenv import load_dotenv

load_dotenv()

# 长桥 API
LONGPORT_APP_KEY = os.getenv('LONGPORT_APP_KEY')
LONGPORT_APP_SECRET = os.getenv('LONGPORT_APP_SECRET')
LONGPORT_ACCESS_TOKEN = os.getenv('LONGPORT_ACCESS_TOKEN')

# QQQ 关键价位
QQQ_SUPPORT = 595.08
QQQ_RESISTANCE = 599.39
QQQ_TARGET1 = 590.00
QQQ_TARGET2 = 585.00

# 推送间隔（秒）
PUSH_INTERVAL = 1800  # 30 分钟

# 状态文件
STATE_FILE = '/tmp/qqq_monitor_state.json'

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            'last_push': 0,
            'breakout_support': False,
            'breakout_resistance': False,
            'push_count': 0
        }

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def main():
    print("=" * 60)
    print("📊 QQQ 监控启动")
    print("=" * 60)
    
    config = Config(
        app_key=LONGPORT_APP_KEY,
        app_secret=LONGPORT_APP_SECRET,
        access_token=LONGPORT_ACCESS_TOKEN
    )
    
    state = load_state()
    push_count = state.get('push_count', 0)
    
    while True:
        try:
            with QuoteContext(config) as qc:
                qqq = qc.quote("QQQ")
                price = qqq.last_done
                change = qqq.change
                change_rate = qqq.change_rate
                high = qqq.high
                low = qqq.low
                volume = qqq.volume
                
                now = time.time()
                signal = "看跌" if price < 597 else "观望"
                
                # 输出到日志
                log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] QQQ: ${price:.2f} ({change_rate*100:+.2f}%) | 推送：{push_count} 次"
                print(log_msg)
                
                # 写入状态文件（供外部读取）
                status = {
                    'time': datetime.now().isoformat(),
                    'price': price,
                    'change': change,
                    'change_rate': change_rate,
                    'high': high,
                    'low': low,
                    'volume': volume,
                    'signal': signal,
                    'support': QQQ_SUPPORT,
                    'resistance': QQQ_RESISTANCE,
                    'last_push': state['last_push'],
                    'push_count': push_count,
                    'breakout_down': price < QQQ_SUPPORT and not state['breakout_support'],
                    'breakout_up': price > QQQ_RESISTANCE and not state['breakout_resistance']
                }
                
                with open('/tmp/qqq_status.json', 'w') as f:
                    json.dump(status, f, indent=2)
                
                # 检查突破
                if price < QQQ_SUPPORT and not state['breakout_support']:
                    print(f"📉 跌破支撑位：${price:.2f} - 需要推送警报")
                    state['breakout_support'] = True
                    state['breakout_resistance'] = False
                    state['last_push'] = now
                    state['push_count'] = push_count + 1
                    save_state(state)
                
                elif price > QQQ_RESISTANCE and not state['breakout_resistance']:
                    print(f"🚀 突破阻力位：${price:.2f} - 需要推送警报")
                    state['breakout_resistance'] = True
                    state['breakout_support'] = False
                    state['last_push'] = now
                    state['push_count'] = push_count + 1
                    save_state(state)
                
                # 定期推送
                elif now - state['last_push'] >= PUSH_INTERVAL:
                    print(f"📊 定期推送时间到 - 需要推送")
                    state['last_push'] = now
                    state['push_count'] = push_count + 1
                    save_state(state)
                
                push_count = state['push_count']
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            print(f"\n👋 停止监控，共推送 {push_count} 次")
            break
        except Exception as e:
            print(f"❌ 错误：{e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
