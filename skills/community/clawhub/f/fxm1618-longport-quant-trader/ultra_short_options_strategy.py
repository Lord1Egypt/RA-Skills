#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超短线美股期权自动量化交易策略 v1.0
秒级/分钟级超短线策略

策略：
1. 秒级方向性期权（30 秒 -5 分钟）
2. 分钟级波动率突破（5-30 分钟）
3. 价差策略（30 分钟 -2 小时）
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import json

load_dotenv()

# ========== 策略配置 ==========
STRATEGIES = {
    "ultra_short_directional": {
        "name": "秒级方向性期权",
        "hold_time_sec": 300,  # 5 分钟
        "take_profit": 0.40,   # +40%
        "stop_loss": -0.18,    # -18%
        "position_size": 0.03, # 3% 仓位
        "target_underlyings": ["QQQ.US", "NVDA.US"],
        "min_volume_ratio": 3.0,
        "rsi_overbought": 60,
        "rsi_oversold": 40,
    },
    "minute_volatility_breakout": {
        "name": "分钟级波动率突破",
        "hold_time_min": 30,
        "take_profit": 0.80,
        "stop_loss": -0.25,
        "position_size": 0.05,
        "target_underlyings": ["QQQ.US", "NVDA.US", "TSLA.US"],
        "breakout_threshold": 0.02,  # 2% 突破
    },
    "spread_conservative": {
        "name": "价差策略（保守）",
        "hold_time_min": 120,
        "take_profit": 0.60,
        "stop_loss": -1.0,  # 最大亏损
        "position_size": 0.10,
        "target_underlyings": ["QQQ.US"],
    },
}

# 关键价位
KEY_LEVELS = {
    "QQQ.US": {"support": 595.0, "resistance": 605.0},
    "NVDA.US": {"support": 175.0, "resistance": 180.0},
    "TSLA.US": {"support": 390.0, "resistance": 400.0},
}

config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# ========== 技术指标计算 ==========

def calculate_rsi(prices, period=14):
    """计算 RSI"""
    if len(prices) < period + 1:
        return 50.0
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_volume_ratio(current_volume, avg_volume):
    """计算成交量比率"""
    if avg_volume == 0:
        return 1.0
    return current_volume / avg_volume

# ========== 信号生成 ==========

def generate_signal(symbol, quote, strategy_config):
    """生成交易信号"""
    price = float(quote.last_done)
    prev_close = float(quote.prev_close)
    change = (price - prev_close) / prev_close if prev_close > 0 else 0
    
    signal = {
        "symbol": symbol,
        "price": price,
        "change": change,
        "action": None,  # "BUY_CALL", "BUY_PUT", "SELL_SPREAD"
        "strength": 0,
        "reason": "",
    }
    
    # 秒级方向性策略
    if strategy_config["name"] == "秒级方向性期权":
        # 看涨信号
        if change >= 0.01 and change < 0.03:  # 上涨 1-3%
            signal["action"] = "BUY_CALL"
            signal["strength"] = min(change * 100, 10)
            signal["reason"] = f"上涨 {change*100:.2f}%"
        
        # 看跌信号
        elif change <= -0.01 and change > -0.03:  # 下跌 -1% 到 -3%
            signal["action"] = "BUY_PUT"
            signal["strength"] = min(abs(change) * 100, 10)
            signal["reason"] = f"下跌 {change*100:.2f}%"
    
    # 分钟级波动率突破
    elif strategy_config["name"] == "分钟级波动率突破":
        # 突破阻力位
        if symbol in KEY_LEVELS:
            resistance = KEY_LEVELS[symbol]["resistance"]
            support = KEY_LEVELS[symbol]["support"]
            
            if price >= resistance * 1.01:  # 突破阻力 1%
                signal["action"] = "BUY_CALL"
                signal["strength"] = 8
                signal["reason"] = f"突破阻力位 ${resistance}"
            
            elif price <= support * 0.99:  # 跌破支撑 1%
                signal["action"] = "BUY_PUT"
                signal["strength"] = 8
                signal["reason"] = f"跌破支撑位 ${support}"
    
    return signal

# ========== 交易执行 ==========

def execute_trade(signal, strategy_config):
    """执行交易（模拟）"""
    print(f"\n📤 执行交易")
    print(f"  标的：{signal['symbol']}")
    print(f"  方向：{signal['action']}")
    print(f"  价格：${signal['price']:.2f}")
    print(f"  强度：{signal['strength']}/10")
    print(f"  原因：{signal['reason']}")
    print(f"  策略：{strategy_config['name']}")
    print(f"  止盈：+{strategy_config['take_profit']*100:.0f}%")
    print(f"  止损：{strategy_config['stop_loss']*100:.0f}%")
    print(f"  仓位：{strategy_config['position_size']*100:.0f}%")
    
    # 模拟执行（实际交易需要长桥期权 API）
    # 这里仅打印交易信号
    return {
        "success": True,
        "signal": signal,
        "timestamp": datetime.now().isoformat(),
    }

# ========== 主监控循环 ==========

def monitor_and_trade():
    """监控并交易"""
    print("=" * 80)
    print("🚀 超短线美股期权自动量化交易 v1.0")
    print("=" * 80)
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"策略：秒级/分钟级超短线")
    print(f"标的：QQQ, NVDA, TSLA")
    print("=" * 80)
    print()
    
    # 账户状态
    try:
        balances = ctx.account_balance()
        for b in balances:
            cash = float(b.cash_infos[0].available_cash) if b.cash_infos else 0
            print(f"💰 可用现金：USD {cash:,.2f}")
            print(f"💰 净资产：USD {b.net_assets:,.2f}")
    except Exception as e:
        print(f"⚠️ 无法获取账户余额：{e}")
    
    print()
    print("-" * 80)
    print("开始监控...")
    print("-" * 80)
    
    trades = []
    scan_count = 0
    
    # 监控循环（模拟 10 次扫描）
    for i in range(10):
        scan_count += 1
        print(f"\n🔍 第{scan_count}次扫描 [{datetime.now().strftime('%H:%M:%S')}]")
        
        # 获取行情
        symbols = ["QQQ.US", "NVDA.US", "TSLA.US"]
        try:
            quotes = qctx.quote(symbols)
            quote_dict = {q.symbol: q for q in quotes}
            
            for symbol in symbols:
                if symbol not in quote_dict:
                    continue
                
                quote = quote_dict[symbol]
                price = float(quote.last_done)
                change = (quote.last_done - quote.prev_close) / quote.prev_close * 100 if quote.prev_close > 0 else 0
                
                print(f"  {symbol}: ${price:.2f} ({change:+.2f}%)")
                
                # 生成信号
                for strategy_name, strategy_config in STRATEGIES.items():
                    if symbol in strategy_config["target_underlyings"]:
                        signal = generate_signal(symbol, quote, strategy_config)
                        
                        if signal["action"]:
                            print(f"    🎯 信号：{signal['action']} (强度：{signal['strength']}/10)")
                            print(f"       原因：{signal['reason']}")
                            
                            # 执行交易
                            trade_result = execute_trade(signal, strategy_config)
                            trades.append(trade_result)
            
            # 等待 30 秒（模拟秒级监控）
            if i < 9:
                print(f"  ⏳ 等待 30 秒...")
                time.sleep(2)  # 模拟用 2 秒代替 30 秒
        
        except Exception as e:
            print(f"  ❌ 错误：{e}")
            time.sleep(5)
    
    # 总结
    print("\n" + "=" * 80)
    print("📊 扫描总结")
    print("=" * 80)
    print(f"扫描次数：{scan_count}")
    print(f"生成信号：{len(trades)}")
    print(f"平均强度：{sum(t['signal']['strength'] for t in trades)/len(trades) if trades else 0:.1f}/10")
    print("=" * 80)
    
    return trades

if __name__ == "__main__":
    try:
        trades = monitor_and_trade()
        print(f"\n✅ 测试完成！共生成 {len(trades)} 个交易信号")
    except KeyboardInterrupt:
        print("\n\n⏸️  用户中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
