#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股持续监控交易 - 每 5 分钟执行
策略：动量 + 均值回归 v2
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

STRATEGY = {
    "momentum_threshold": 0.013,  # +1.3%
    "reversion_threshold": -0.023,  # -2.3%
    "stop_loss": -0.10,  # -10%
    "take_profit": 0.20,  # +20%
}

HK_STOCKS = ['700.HK', '9988.HK', '3690.HK', '1211.HK', '9618.HK']

config = Config.from_env()

def run_check():
    ctx = TradeContext(config)
    qctx = QuoteContext(config)
    
    print(f"\n{'='*70}")
    print(f"🔄 监控检查 - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*70}")
    
    # 资金
    cash = 0
    for b in ctx.account_balance():
        cash = float(b.cash_infos[0].available_cash) if b.cash_infos else 0
    
    # 持仓
    positions = []
    resp = ctx.stock_positions()
    for channel in resp.channels:
        for pos in channel.positions:
            positions.append({
                'symbol': pos.symbol,
                'qty': int(pos.quantity),
                'avail': int(pos.available_quantity),
                'cost': float(pos.cost_price),
            })
    
    # 行情
    quotes = qctx.quote(HK_STOCKS)
    quote_dict = {q.symbol: q for q in quotes}
    
    trades = 0
    
    # 检查持仓止盈止损
    for pos in positions:
        q = quote_dict.get(pos['symbol'])
        if not q:
            continue
        
        price = float(q.last_done)
        pnl_pct = (price - pos['cost']) / pos['cost']
        
        # 止盈
        if pnl_pct >= STRATEGY['take_profit']:
            print(f"📤 {pos['symbol']} 止盈 +{pnl_pct*100:.1f}%")
            try:
                ctx.submit_order(
                    side=OrderSide.Sell,
                    symbol=pos['symbol'],
                    order_type=OrderType.LO,
                    submitted_price=Decimal(f"{price:.2f}"),
                    submitted_quantity=Decimal(str(pos['avail'])),
                    time_in_force=TimeInForceType.Day,
                    remark='止盈'
                )
                trades += 1
            except Exception as e:
                print(f"  ❌ {e}")
        
        # 止损
        elif pnl_pct <= STRATEGY['stop_loss']:
            print(f"📤 {pos['symbol']} 止损 {pnl_pct*100:.1f}%")
            try:
                ctx.submit_order(
                    side=OrderSide.Sell,
                    symbol=pos['symbol'],
                    order_type=OrderType.LO,
                    submitted_price=Decimal(f"{price:.2f}"),
                    submitted_quantity=Decimal(str(pos['avail'])),
                    time_in_force=TimeInForceType.Day,
                    remark='止损'
                )
                trades += 1
            except Exception as e:
                print(f"  ❌ {e}")
    
    # 买入超跌股票
    position_symbols = [p['symbol'] for p in positions]
    
    for q in quotes:
        if q.symbol in position_symbols:
            continue
        
        change = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
        
        if change <= STRATEGY['reversion_threshold'] and cash > 0:
            buy_value = cash * 0.5
            qty = int(buy_value / float(q.last_done))
            qty = (qty // 100) * 100
            
            if qty >= 100:
                price = float(q.last_done) * 1.005
                print(f"📤 {q.symbol} 超跌 {change*100:.1f}% 买入{qty}股")
                try:
                    ctx.submit_order(
                        side=OrderSide.Buy,
                        symbol=q.symbol,
                        order_type=OrderType.LO,
                        submitted_price=Decimal(f"{price:.2f}"),
                        submitted_quantity=Decimal(str(qty)),
                        time_in_force=TimeInForceType.Day,
                        remark='抄底'
                    )
                    trades += 1
                    cash -= qty * price
                except Exception as e:
                    print(f"  ❌ {e}")
    
    # 状态汇总
    print(f"\n💰 现金：HKD {cash:,.0f}")
    print(f"📈 持仓：{len(positions)}只")
    for pos in positions:
        q = quote_dict.get(pos['symbol'])
        if q:
            pnl = (float(q.last_done) - pos['cost']) * pos['qty']
            print(f"  {pos['symbol']}: HKD {pnl:+,.0f}")
    
    print(f"✅ 交易：{trades}笔")
    
    ctx.close()
    qctx.close()
    
    return trades

if __name__ == "__main__":
    print("🚀 启动持续监控（每 5 分钟）")
    print("按 Ctrl+C 停止")
    
    try:
        while True:
            run_check()
            time.sleep(300)  # 5 分钟
    except KeyboardInterrupt:
        print("\n👋 停止监控")
