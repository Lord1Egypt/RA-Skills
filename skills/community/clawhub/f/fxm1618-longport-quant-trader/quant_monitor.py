#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化交易持续监控 - 每 5 分钟执行
自动买入卖出 + 绩效跟踪
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime
import json
import time

load_dotenv()

STRATEGY = {
    "momentum": 0.015,      # +1.5%
    "reversion": -0.025,    # -2.5%
    "stop_loss": -0.08,     # -8%
    "take_profit": 0.15,    # +15%
    "position_pct": 0.25,   # 25% 仓位
    "max_positions": 5,
}

HK_STOCKS = [
    {'symbol': '700.HK', 'lot': 100},
    {'symbol': '9988.HK', 'lot': 100},
    {'symbol': '3690.HK', 'lot': 100},
    {'symbol': '1211.HK', 'lot': 500},
    {'symbol': '9618.HK', 'lot': 100},
]

PERF_FILE = '/tmp/quant_perf.json'

def load_perf():
    try:
        with open(PERF_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'trades': 0, 'wins': 0, 'losses': 0, 'pnl': 0, 'start': 800000}

def save_perf(p):
    with open(PERF_FILE, 'w') as f:
        json.dump(p, f, indent=2)

def run_check():
    config = Config.from_env()
    ctx = TradeContext(config)
    qctx = QuoteContext(config)
    perf = load_perf()
    
    print(f"\n{'='*70}")
    print(f"🔄 监控 - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*70}")
    
    # 资金
    cash = 0
    net = 0
    for b in ctx.account_balance():
        cash = float(b.cash_infos[0].available_cash) if b.cash_infos else 0
        net = float(b.net_assets)
    
    # 持仓
    positions = []
    resp = ctx.stock_positions()
    for channel in resp.channels:
        for pos in channel.positions:
            positions.append({
                'sym': pos.symbol,
                'qty': int(pos.quantity),
                'avail': int(pos.available_quantity),
                'cost': float(pos.cost_price),
            })
    
    # 行情
    symbols = [s['symbol'] for s in HK_STOCKS]
    quotes = qctx.quote(symbols)
    quote_dict = {q.symbol: q for q in quotes}
    
    trades = 0
    
    # 止盈止损
    print(f"\n💰 现金：HKD {cash:,.0f} | 净资产：HKD {net:,.0f}")
    print(f"\n📈 持仓 ({len(positions)})")
    
    for pos in positions:
        q = quote_dict.get(pos['sym'])
        if not q:
            continue
        
        price = float(q.last_done)
        pnl = (price - pos['cost']) * pos['qty']
        pnl_pct = (price - pos['cost']) / pos['cost']
        
        print(f"  {pos['sym']}: {pos['qty']}股 盈亏 HKD {pnl:+,.0f} ({pnl_pct*100:+.2f}%)")
        
        # 止盈
        if pnl_pct >= STRATEGY['take_profit']:
            print(f"    📤 止盈卖出 {pos['avail']}股")
            try:
                ctx.submit_order(
                    side=OrderSide.Sell,
                    symbol=pos['sym'],
                    order_type=OrderType.LO,
                    submitted_price=Decimal(f"{price:.2f}"),
                    submitted_quantity=Decimal(str(pos['avail'])),
                    time_in_force=TimeInForceType.Day,
                    remark='止盈'
                )
                perf['trades'] += 1
                perf['wins'] += 1
                perf['pnl'] += pnl
                trades += 1
            except Exception as e:
                print(f"    ❌ {e}")
        
        # 止损
        elif pnl_pct <= STRATEGY['stop_loss']:
            print(f"    📤 止损卖出 {pos['avail']}股")
            try:
                ctx.submit_order(
                    side=OrderSide.Sell,
                    symbol=pos['sym'],
                    order_type=OrderType.LO,
                    submitted_price=Decimal(f"{price:.2f}"),
                    submitted_quantity=Decimal(str(pos['avail'])),
                    time_in_force=TimeInForceType.Day,
                    remark='止损'
                )
                perf['trades'] += 1
                perf['losses'] += 1
                perf['pnl'] += pnl
                trades += 1
            except Exception as e:
                print(f"    ❌ {e}")
    
    # 买入
    pos_syms = [p['sym'] for p in positions]
    print(f"\n🔍 买入机会")
    
    for s in HK_STOCKS:
        sym = s['symbol']
        if sym in pos_syms or sym not in quote_dict:
            continue
        
        q = quote_dict[sym]
        change = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
        
        # 超跌或动量
        if change <= STRATEGY['reversion'] or change >= STRATEGY['momentum']:
            sig_type = '超跌' if change < 0 else '动量'
            buy_val = cash * STRATEGY['position_pct']
            qty = int(buy_val / float(q.last_done))
            qty = (qty // s['lot']) * s['lot']
            
            if qty >= s['lot'] and cash > 0:
                price = float(q.last_done) * 1.005
                print(f"  🟢 {sym} {sig_type} {change*100:.2f}% 买入{qty}股 @ {price:.2f}")
                
                try:
                    ctx.submit_order(
                        side=OrderSide.Buy,
                        symbol=sym,
                        order_type=OrderType.LO,
                        submitted_price=Decimal(f"{price:.2f}"),
                        submitted_quantity=Decimal(str(qty)),
                        time_in_force=TimeInForceType.Day,
                        remark=f'{sig_type}买入'
                    )
                    trades += 1
                except Exception as e:
                    print(f"    ❌ {e}")
            else:
                print(f"  ⚪ {sym} {change*100:+.2f}% 观望")
        else:
            print(f"  ⚪ {sym} {change*100:+.2f}% 观望")
    
    # 绩效
    print(f"\n📊 绩效")
    print(f"  交易：{perf['trades']}笔")
    if perf['trades'] > 0:
        win_rate = perf['wins'] / perf['trades'] * 100
        print(f"  胜率：{win_rate:.1f}% ({perf['wins']}胜{perf['losses']}负)")
    
    total_ret = (net - perf['start']) / perf['start'] * 100
    print(f"  收益：{total_ret:.2f}%")
    
    save_perf(perf)
    print(f"✅ 执行{trades}笔交易")
    
    return trades

if __name__ == "__main__":
    print("🚀 启动监控（每 5 分钟）| Ctrl+C 停止")
    try:
        while True:
            run_check()
            time.sleep(300)
    except KeyboardInterrupt:
        print("\n👋 停止")
