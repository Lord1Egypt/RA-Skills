#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股高频量化交易 v2.0 - 增强版
策略：动量 + 均值回归 + 网格交易 + 智能路由
账户：LBPT10034472（模拟盘）
目标：胜率>70%, 年化>200%
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import os

load_dotenv()

# ========== 策略配置 v2.0 ==========
STRATEGIES = {
    "momentum": {
        "name": "动量追涨",
        "threshold": 0.013,  # +1.3%
        "position_size": 0.15,  # 15%
        "stop_loss": -0.01,  # -1%
        "take_profit": 0.02,  # +2%
        "hold_time": 30,  # 分钟
    },
    "mean_reversion": {
        "name": "均值回归",
        "threshold": -0.023,  # -2.3%
        "position_size": 0.12,  # 12%
        "stop_loss": -0.015,  # -1.5%
        "take_profit": 0.025,  # +2.5%
        "hold_time": 60,
    },
    "grid": {
        "name": "网格交易",
        "grid_spacing": 0.025,  # 2.5% 一格
        "grid_levels": 6,  # 6 层
        "position_size": 0.08,  # 每格 8%
        "target_stocks": ["700.HK", "9988.HK"],  # 震荡股
    },
    "breakout": {
        "name": "突破追涨",
        "threshold": 0.02,  # +2%
        "volume_ratio": 3.0,  # 3 倍量
        "position_size": 0.20,  # 20%
        "stop_loss": -0.008,  # -0.8%
        "take_profit": 0.015,  # +1.5%
        "hold_time": 15,
    },
}

# 股票池 + 策略匹配
HK_STOCKS = [
    {"symbol": "700.HK", "name": "腾讯", "board_lot": 100, "type": "震荡", "best_strategy": "grid"},
    {"symbol": "9988.HK", "name": "阿里", "board_lot": 100, "type": "震荡", "best_strategy": "mean_reversion"},
    {"symbol": "3690.HK", "name": "美团", "board_lot": 100, "type": "趋势", "best_strategy": "momentum"},
    {"symbol": "1211.HK", "name": "比亚迪", "board_lot": 500, "type": "趋势", "best_strategy": "momentum"},
    {"symbol": "9618.HK", "name": "京东", "board_lot": 100, "type": "震荡", "best_strategy": "mean_reversion"},
    {"symbol": "1810.HK", "name": "小米", "board_lot": 500, "type": "高波", "best_strategy": "breakout"},
    {"symbol": "2015.HK", "name": "理想", "board_lot": 100, "type": "高波", "best_strategy": "breakout"},
    {"symbol": "9866.HK", "name": "蔚来", "board_lot": 100, "type": "高波", "best_strategy": "breakout"},
]

config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# ========== 智能路由函数 ==========

def analyze_market_condition(symbol, quote):
    """分析市场环境，选择最优策略"""
    change = (quote.last_done - quote.prev_close) / quote.prev_close if quote.prev_close > 0 else 0
    
    # 波动率判断（简化版）
    volatility = abs(change)
    
    # 策略评分
    scores = {
        "momentum": 0,
        "mean_reversion": 0,
        "grid": 0,
        "breakout": 0,
    }
    
    # 动量策略：涨幅>1.3%
    if change >= STRATEGIES["momentum"]["threshold"]:
        scores["momentum"] += 8
    
    # 均值回归：跌幅>2.3%
    if change <= STRATEGIES["mean_reversion"]["threshold"]:
        scores["mean_reversion"] += 8
    
    # 网格交易：震荡市（-1% 到 +1%）
    if -0.01 <= change <= 0.01:
        scores["grid"] += 7
    
    # 突破策略：涨幅>2% 且放量
    if change >= STRATEGIES["breakout"]["threshold"]:
        scores["breakout"] += 9
    
    # 选择得分最高的策略
    best_strategy = max(scores.items(), key=lambda x: x[1])
    
    return best_strategy[0], scores

# ========== 交易执行函数 ==========

def submit_order(symbol, side, price, quantity, strategy, remark=""):
    """提交订单"""
    try:
        order_price = Decimal(str(round(price, 3)))
        order_qty = Decimal(str(quantity))
        order_type = OrderType.ELO if side == "Buy" else OrderType.LO
        
        resp = ctx.submit_order(
            side=OrderSide.Buy if side == "Buy" else OrderSide.Sell,
            symbol=symbol,
            order_type=order_type,
            submitted_price=order_price,
            submitted_quantity=order_qty,
            time_in_force=TimeInForceType.Day,
            remark=f"{strategy}-{remark}"
        )
        return {"success": True, "order_id": resp.order_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

def execute_grid_trading(symbol, stock_info, cash):
    """执行网格交易"""
    print(f"\n🕸️  网格交易 - {symbol} {stock_info['name']}")
    print("-" * 60)
    
    # 获取当前价格
    quote = qctx.quote([symbol])[0]
    current_price = float(quote.last_done)
    
    cfg = STRATEGIES["grid"]
    grid_spacing = cfg["grid_spacing"]
    grid_levels = cfg["grid_levels"]
    
    # 生成网格订单
    buy_orders = []
    sell_orders = []
    
    for i in range(1, grid_levels + 1):
        buy_price = current_price * (1 - grid_spacing * i)
        sell_price = current_price * (1 + grid_spacing * i)
        
        # 计算买入数量
        buy_value = cash * cfg["position_size"]
        qty = int(buy_value / buy_price)
        qty = (qty // stock_info["board_lot"]) * stock_info["board_lot"]
        
        if qty >= stock_info["board_lot"]:
            buy_orders.append({
                "price": round(buy_price, 2),
                "quantity": qty,
                "side": "Buy"
            })
            sell_orders.append({
                "price": round(sell_price, 2),
                "quantity": qty,
                "side": "Sell"
            })
    
    # 提交买单
    for order in buy_orders:
        print(f"  挂单买入 {order['quantity']}股 @ HKD {order['price']:.2f}")
        result = submit_order(symbol, "Buy", order["price"], order["quantity"], "网格")
        if result["success"]:
            print(f"    ✅ 订单 ID: {result['order_id']}")
        else:
            print(f"    ❌ 失败：{result['error']}")
    
    return len(buy_orders)

# ========== 主函数 ==========

def main():
    """主函数 - 高频自动量化交易"""
    print()
    print("=" * 80)
    print("🚀 港股高频量化交易 v2.0 - 增强版")
    print("=" * 80)
    print(f"账户：LBPT10034472（模拟盘）")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"策略：动量 + 均值回归 + 网格 + 突破")
    print(f"目标：胜率>70%, 年化>200%")
    print("=" * 80)
    print()
    
    # 1. 账户状态
    print("💰 账户状态")
    print("-" * 80)
    balances = ctx.account_balance()
    cash = 0
    net_assets = 0
    for b in balances:
        cash = float(b.cash_infos[0].available_cash) if b.cash_infos else 0
        net_assets = float(b.net_assets)
        print(f"可用现金：HKD {cash:,.2f}")
        print(f"净资产：HKD {net_assets:,.2f}")
    print()
    
    # 2. 当前持仓
    print("📊 当前持仓")
    print("-" * 80)
    resp = ctx.stock_positions()
    positions = []
    for channel in resp.channels:
        for pos in channel.positions:
            positions.append({
                'symbol': pos.symbol,
                'qty': int(pos.quantity),
                'available': int(pos.available_quantity),
                'cost': float(pos.cost_price),
            })
            print(f"{pos.symbol}: {pos.quantity}股 @ HKD {pos.cost_price:.2f}")
    
    if not positions:
        print("无持仓")
    print()
    
    # 3. 获取行情 + 智能策略匹配
    print("🔍 扫描机会 + 智能策略匹配")
    print("-" * 80)
    symbols = [s["symbol"] for s in HK_STOCKS]
    quotes = qctx.quote(symbols)
    quote_dict = {q.symbol: q for q in quotes}
    
    for stock in HK_STOCKS:
        symbol = stock["symbol"]
        if symbol not in quote_dict:
            continue
        
        q = quote_dict[symbol]
        change = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
        
        # 智能路由：选择最优策略
        best_strategy, scores = analyze_market_condition(symbol, q)
        
        # 显示股票状态
        flag = "📈" if change > 0.02 else "📉" if change < -0.02 else "➖"
        print(f"\n{flag} {symbol} {stock['name']} | HKD {q.last_done:.2f} ({change*100:+.2f}%)")
        print(f"   类型：{stock['type']} | 推荐策略：{stock['best_strategy']}")
        print(f"   策略评分：{scores}")
        print(f"   最优策略：{STRATEGIES[best_strategy]['name']}")
        
        # 执行交易
        position_symbols = [p['symbol'] for p in positions]
        
        # 已持仓 → 检查止盈止损
        if symbol in position_symbols:
            pos = next((p for p in positions if p['symbol'] == symbol), None)
            if pos:
                pnl_pct = (float(q.last_done) - pos['cost']) / pos['cost'] * 100
                print(f"   盈亏：{pnl_pct:+.2f}%")
                
                # 止盈检查（+2%）
                if pnl_pct >= 2.0:
                    print(f"   📤 止盈信号！卖出 {pos['available']}股")
                    result = submit_order(symbol, "Sell", float(q.last_done), pos['available'], "止盈")
                    if result["success"]:
                        print(f"   ✅ 订单 ID: {result['order_id']}")
                
                # 止损检查（-1%）
                elif pnl_pct <= -1.0:
                    print(f"   📤 止损信号！卖出 {pos['available']}股")
                    result = submit_order(symbol, "Sell", float(q.last_done), pos['available'], "止损")
                    if result["success"]:
                        print(f"   ✅ 订单 ID: {result['order_id']}")
        
        # 未持仓 → 执行买入策略
        elif symbol not in position_symbols:
            # 网格交易（针对震荡股）
            if stock['type'] == '震荡' and best_strategy == 'grid':
                execute_grid_trading(symbol, stock, cash)
            
            # 均值回归（超跌）
            elif change <= STRATEGIES["mean_reversion"]["threshold"]:
                print(f"   📈 均值回归信号！买入")
                buy_value = cash * STRATEGIES["mean_reversion"]["position_size"]
                qty = int(buy_value / float(q.last_done))
                qty = (qty // stock["board_lot"]) * stock["board_lot"]
                
                if qty >= stock["board_lot"]:
                    result = submit_order(symbol, "Buy", float(q.last_done) * 1.005, qty, "均值回归")
                    if result["success"]:
                        print(f"   ✅ 买入 {qty}股，订单 ID: {result['order_id']}")
            
            # 动量策略（追涨）
            elif change >= STRATEGIES["momentum"]["threshold"]:
                print(f"   📈 动量信号！买入")
                buy_value = cash * STRATEGIES["momentum"]["position_size"]
                qty = int(buy_value / float(q.last_done))
                qty = (qty // stock["board_lot"]) * stock["board_lot"]
                
                if qty >= stock["board_lot"]:
                    result = submit_order(symbol, "Buy", float(q.last_done) * 1.005, qty, "动量")
                    if result["success"]:
                        print(f"   ✅ 买入 {qty}股，订单 ID: {result['order_id']}")
    
    print()
    print("=" * 80)
    print("✅ 扫描完成")
    print("=" * 80)
    print()
    
    # 4. 查看订单
    print("📋 今日订单")
    print("-" * 80)
    orders = ctx.today_orders()
    if orders:
        for o in orders:
            status_map = {
                'NotReported': '待报送',
                'Submitted': '已报送',
                'PartiallyFilled': '部分成交',
                'Filled': '已成交',
                'Cancelled': '已取消',
                'Rejected': '已拒绝',
            }
            status = status_map.get(str(o.status), str(o.status))
            side_str = "买入" if str(o.side) == "Buy" else "卖出"
            print(f"{o.symbol} {side_str} {o.quantity}股 - {status}")
    else:
        print("无订单")
    
    print()
    print("=" * 80)
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
