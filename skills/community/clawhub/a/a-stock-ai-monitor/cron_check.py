#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Monitor Cron Job - 只在交易时间发送预警
通过 OpenClaw message tool 发送消息，不依赖 cron announce
"""

import sys
import io
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 修复 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 导入监控类
sys.path.insert(0, str(Path(__file__).parent))
from monitor import StockAlert, WATCHLIST

# 飞书配置
FEISHU_USER_ID = "ou_76cf01403b232cd9213972ea46c9ac9f"

def is_trading_time():
    """判断是否在交易时间（北京时间）"""
    now = datetime.now()
    hour, minute = now.hour, now.minute
    time_val = hour * 100 + minute
    weekday = now.weekday()
    
    # 周末不交易
    if weekday >= 5:
        return False
    
    # 交易时间: 9:30-11:30, 13:00-15:00
    morning = 930 <= time_val <= 1130
    afternoon = 1300 <= time_val <= 1500
    
    return morning or afternoon

def send_feishu_message(message: str):
    """通过 OpenClaw CLI 发送飞书消息"""
    try:
        # Windows 上需要使用 shell=True 来找到 npm 全局命令
        # 使用 --account main 指定正确的飞书账户
        cmd = "openclaw message send --channel feishu --account main --target user:" + FEISHU_USER_ID + " --message \"" + message.replace('"', '\\"') + "\""
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60,
            shell=True
        )
        if result.returncode != 0:
            print(f"发送消息失败: {result.stderr}", file=sys.stderr)
    except Exception as e:
        print(f"发送消息异常: {e}", file=sys.stderr)

def main():
    if not is_trading_time():
        # 非交易时间不做任何事
        return
    
    monitor = StockAlert()
    alerts = monitor.run_once(smart_mode=False)
    
    if alerts:
        # 有预警时，发送飞书消息
        message = "\n".join(alerts)
        send_feishu_message(message)
    # 无预警时不发送

if __name__ == '__main__':
    main()
