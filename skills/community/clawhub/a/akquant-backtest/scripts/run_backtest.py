#!/usr/bin/env python3
"""
AKQuant 策略回测快速工具
支持双均线策略、RSI策略等
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/akquant-backtest/scripts')
from double_ma_strategy import run_double_ma_backtest


if __name__ == '__main__':
    symbol = sys.argv[1] if len(sys.argv) > 1 else "000001"
    fast = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    slow = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    result = run_double_ma_backtest(
        symbol=symbol,
        fast_period=fast,
        slow_period=slow,
        initial_capital=100000,
        start_date="20240101",
        end_date="20241231"
    )
