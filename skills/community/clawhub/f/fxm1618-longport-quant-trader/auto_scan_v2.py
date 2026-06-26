#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股高频量化交易 - 最优策略持续扫描 v2.0
股票池：20 只高流动性港股
扫描频率：每 5 分钟
策略：智能路由 + 新风控 + 移动止盈
持仓上限：20 只
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import sys
import time

load_dotenv()

# ========== 最优策略配置 ==========
STRATEGIES = {
    "momentum": {
        "name": "动量追涨",
        "threshold": 0.013,  # +1.3%
        "position_size": 0.08,  # 8%（20 只分散）
        "take_profit": 0.02,
        "stop_loss": -0.01,
        "hold_time_min": 30,
    },
    "breakout": {
        "name": "突破追涨",
        "threshold": 0.02,
        "volume_ratio": 2.0,
        "position_size": 0.08,
        "trailing_stop": 0.01,  # 回撤 1% 止盈
        "stop_loss": -0.015,
        "hold_time_min": 60,
    },
    "grid": {
        "name": "网格交易",
        "grid_spacing": 0.025,
        "grid_levels": 6,
        "position_size": 0.06,  # 6%/格
        "stop_loss": -0.05,
    },
    "mean_reversion": {
        "name": "均值回归",
        "threshold": -0.023,
        "position_size": 0.08,
        "take_profit": 0.03,
        "stop_loss": -0.015,
        "hold_time_min": 90,
    },
}

# 股票池（20 只）- 扩展版
HK_STOCKS = [
    # 科技股（8 只）
    {"symbol": "700.HK", "name": "腾讯", "board_lot": 100, "type": "震荡", "strategy": "grid"},
    {"symbol": "9988.HK", "name": "阿里", "board_lot": 100, "type": "震荡", "strategy": "mean_reversion"},
    {"symbol": "3690.HK", "name": "美团", "board_lot": 100, "type": "趋势", "strategy": "momentum"},
    {"symbol": "9618.HK", "name": "京东", "board_lot": 100, "type": "震荡", "strategy": "mean_reversion"},
    {"symbol": "9888.HK", "name": "百度", "board_lot": 100, "type": "高波", "strategy": "breakout"},
    {"symbol": "1810.HK", "name": "小米", "board_lot": 500, "type": "高波", "strategy": "breakout"},
    {"symbol": "1024.HK", "name": "快手", "board_lot": 500, "type": "高波", "strategy": "momentum"},
    {"symbol": "9999.HK", "name": "网易", "board_lot": 100, "type": "震荡", "strategy": "mean_reversion"},
    
    # 新能源车（4 只）
    {"symbol": "1211.HK", "name": "比亚迪", "board_lot": 500, "type": "趋势", "strategy": "grid"},
    {"symbol": "2015.HK", "name": "理想", "board_lot": 100, "type": "高波", "strategy": "breakout"},
    {"symbol": "9866.HK", "name": "蔚来", "board_lot": 100, "type": "高波", "strategy": "breakout"},
    {"symbol": "9868.HK", "name": "小鹏", "board_lot": 100, "type": "高波", "strategy": "breakout"},
    
    # 金融股（5 只）
    {"symbol": "2318.HK", "name": "平安", "board_lot": 500, "type": "金融", "strategy": "grid"},
    {"symbol": "1299.HK", "name": "友邦", "board_lot": 100, "type": "金融", "strategy": "momentum"},
    {"symbol": "0005.HK", "name": "汇丰", "board_lot": 400, "type": "金融", "strategy": "mean_reversion"},
    {"symbol": "3988.HK", "name": "中行", "board_lot": 1000, "type": "金融", "strategy": "grid"},
    {"symbol": "2628.HK", "name": "人寿", "board_lot": 1000, "type": "金融", "strategy": "mean_reversion"},
    
    # 消费/医疗（3 只）
    {"symbol": "0001.HK", "name": "长和", "board_lot": 500, "type": "震荡", "strategy": "grid"},
    {"symbol": "1398.HK", "name": "工行", "board_lot": 1000, "type": "金融", "strategy": "grid"},
    {"symbol": "2382.HK", "name": "舜宇", "board_lot": 100, "type": "科技", "strategy": "momentum"},
]

config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# 持仓跟踪（移动止盈）
position_tracker = {}

# ========== 核心函数 ==========

def submit_order(symbol, side, price, quantity, strategy, remark=""):
    """提交订单"""
    try:
        order_price = Decimal(str(round(price, 2)))
        order_qty = Decimal(str(quantity))
        order_type = OrderType.MO if side == "Buy" else OrderType.LO
        
        resp = ctx.submit_order(
            side=OrderSide.Buy if side == "Buy" else OrderSide.Sell,
            symbol=symbol,
            order_type=order_type,
            submitted_price=order_price if side == "Buy" else None,
            submitted_quantity=order_qty,
            time_in_force=TimeInForceType.Day,
            remark=f"量化-{strategy}"
        )
        return {"success": True, "order_id": resp.order_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_exit(symbol, pos, price, strategy):
    """检查退出条件（止盈/止损）"""
    pnl_pct = (price - pos['cost']) / pos['cost'] * 100
    cfg = STRATEGIES[strategy]
    
    # 突破策略：移动止盈
    if strategy == "breakout":
        if symbol not in position_tracker:
            position_tracker[symbol] = {'highest': price, 'stop': price * 0.99}
        
        tracker = position_tracker[symbol]
        if price > tracker['highest']:
            tracker['highest'] = price
            tracker['stop'] = price * 0.99
        
        if price <= tracker['stop'] and pnl_pct > 0:
            return True, f"移动止盈 (+{pnl_pct:.1f}%)"
        if pnl_pct <= cfg['stop_loss'] * 100:
            return True, f"止损 ({pnl_pct:.1f}%)"
        return False, None
    
    # 其他策略：固定止盈止损
    if strategy == "grid":
        if pnl_pct <= cfg['stop_loss'] * 100:
            return True, f"破网止损 ({pnl_pct:.1f}%)"
        return False, None
    
    if 'take_profit' in cfg and pnl_pct >= cfg['take_profit'] * 100:
        return True, f"止盈 (+{pnl_pct:.1f}%)"
    if pnl_pct <= cfg['stop_loss'] * 100:
        return True, f"止损 ({pnl_pct:.1f}%)"
    
    return False, None

def scan_and_trade():
    """扫描并交易"""
    print()
    print("=" * 80)
    print(f"🔍 扫描交易 - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    # 账户状态
    balances = ctx.account_balance()
    cash = float(balances[0].cash_infos[0].available_cash) if balances[0].cash_infos else 0
    
    # 持仓
    resp = ctx.stock_positions()
    positions = []
    for channel in resp.channels:
        for pos in channel.positions:
            positions.append({
                'symbol': pos.symbol,
                'qty': int(pos.quantity),
                'cost': float(pos.cost_price),
            })
    
    position_symbols = [p['symbol'] for p in positions]
    trades = 0
    
    # 1. 检查持仓退出
    print(f"\n📊 持仓检查 ({len(position_symbols)}只)")
    for pos in positions:
        symbol = pos['symbol']
        stock = next((s for s in HK_STOCKS if s['symbol'] == symbol), None)
        if not stock:
            continue
        
        q = qctx.quote([symbol])[0]
        price = float(q.last_done)
        
        should_exit, reason = check_exit(symbol, pos, price, stock['strategy'])
        if should_exit:
            print(f"  {symbol} {reason} → 卖出 {pos['qty']}股")
            result = submit_order(symbol, "Sell", price, pos['qty'], stock['strategy'], reason)
            if result["success"]:
                print(f"    ✅ 订单 {result['order_id']}")
                trades += 1
                if symbol in position_tracker:
                    del position_tracker[symbol]
    
    # 2. 扫描买入机会
    print(f"\n🔍 买入扫描 (现金 HKD {cash:,.0f})")
    max_positions = 20  # 新风控：20 只
    available_slots = max_positions - len(position_symbols)
    
    if available_slots <= 0:
        print(f"  ⚠️  持仓已满 ({len(position_symbols)}/{max_positions})")
        return trades
    
    buy_signals = []
    for stock in HK_STOCKS:
        if stock['symbol'] in position_symbols:
            continue
        
        q = qctx.quote([stock['symbol']])[0]
        price = float(q.last_done)
        change = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
        strategy = stock['strategy']
        cfg = STRATEGIES[strategy]
        
        # 检查买入信号
        signal = False
        if strategy == "momentum" and change >= cfg['threshold']:
            signal = True
        elif strategy == "breakout" and change >= cfg['threshold']:
            signal = True
        elif strategy == "mean_reversion" and change <= cfg['threshold']:
            signal = True
        
        if signal:
            buy_signals.append({
                'symbol': stock['symbol'],
                'name': stock['name'],
                'price': price,
                'change': change * 100,
                'strategy': strategy,
                'board_lot': stock['board_lot'],
            })
    
    # 按强度排序，买入最强的
    buy_signals.sort(key=lambda x: abs(x['change']), reverse=True)
    
    for sig in buy_signals[:available_slots]:
        cfg = STRATEGIES[sig['strategy']]
        buy_value = cash * cfg['position_size']
        qty = int(buy_value / sig['price'])
        qty = (qty // sig['board_lot']) * sig['board_lot']
        
        if qty >= sig['board_lot']:
            print(f"  {sig['symbol']} {sig['name']} +{sig['change']:.1f}% → 买入 {qty}股")
            result = submit_order(sig['symbol'], "Buy", sig['price'], qty, sig['strategy'])
            if result["success"]:
                print(f"    ✅ 订单 {result['order_id']}")
                trades += 1
    
    print(f"\n✅ 执行 {trades} 笔交易")
    print("=" * 80)
    
    return trades

# ========== 主函数 ==========

def main():
    """持续扫描"""
    print()
    print("🚀 " + "=" * 78)
    print("🚀 港股高频量化交易 - 最优策略持续扫描 v2.0")
    print("🚀 " + "=" * 78)
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"股票池：20 只高流动性港股")
    print(f"策略：动量 + 突破 + 网格 + 回归")
    print(f"风控：移动止盈 + 分策略")
    print(f"持仓上限：20 只")
    print(f"扫描：每 5 分钟")
    print("=" * 79)
    print()
    
    total_trades = 0
    scans = 0
    
    while True:
        try:
            scans += 1
            trades = scan_and_trade()
            total_trades += trades
            
            print(f"\n💡 第{scans}次扫描 | 本次{trades}笔 | 累计{total_trades}笔")
            print(f"⏰ 下次扫描：5 分钟后")
            print()
            
            # 等待 5 分钟
            for i in range(300, 0, -1):
                sys.stdout.write(f"\r⏳ 倒计时：{i//60}:{i%60:02d} ")
                sys.stdout.flush()
                time.sleep(1)
            
        except KeyboardInterrupt:
            print(f"\n\n⏸️  暂停扫描")
            print(f"总扫描：{scans}次 | 总交易：{total_trades}笔")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
