#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股量化策略测试 - 多策略框架
策略 1: 动量策略（追涨强势股）
策略 2: 均值回归（买入超跌股）
策略 3: 网格交易（震荡市）
"""

from longport.openapi import TradeContext, QuoteContext, Config, OrderSide, OrderType, TimeInForceType
from decimal import Decimal
from datetime import datetime
from typing import List, Dict
import json

# 配置
config = Config.from_env()
ctx = TradeContext(config)
qctx = QuoteContext(config)

# ========== 策略配置 ==========
STRATEGIES = {
    "momentum": {
        "name": "动量策略",
        "desc": "追涨强势股，涨幅>2%",
        "min_change_rate": 0.02,
        "position_size": 100,
        "stop_loss": -0.05,
        "take_profit": 0.10,
        "auto_trade": False,  # 是否自动下单
    },
    "mean_reversion": {
        "name": "均值回归",
        "desc": "买入超跌股，跌幅>3%",
        "max_change_rate": -0.03,
        "position_size": 200,
        "stop_loss": -0.03,
        "take_profit": 0.05,
        "auto_trade": True,  # 开启自动交易
    },
    "grid": {
        "name": "网格交易",
        "desc": "震荡市低买高卖",
        "grid_size": 500,  # 每格 500 股
        "grid_spacing": 0.02,  # 2% 一格
        "grid_levels": 5,  # 5 层网格
        "auto_trade": False,
    }
}

# 港股股票池（蓝筹股，流动性好）
HK_STOCKS = [
    {"symbol": "700.HK", "name": "腾讯控股", "board_lot": 100},
    {"symbol": "9988.HK", "name": "阿里巴巴", "board_lot": 100},
    {"symbol": "3690.HK", "name": "美团", "board_lot": 100},
    {"symbol": "9618.HK", "name": "京东", "board_lot": 100},
    {"symbol": "1211.HK", "name": "比亚迪", "board_lot": 500},
]

# ========== 行情函数 ==========
def get_stock_quotes():
    """获取股票池行情"""
    symbols = [s["symbol"] for s in HK_STOCKS]
    quotes = qctx.quote(symbols)
    
    result = []
    for q in quotes:
        stock_info = next((s for s in HK_STOCKS if s["symbol"] == q.symbol), None)
        if stock_info:
            change_rate = (q.last_done - q.prev_close) / q.prev_close if q.prev_close > 0 else 0
            result.append({
                "symbol": q.symbol,
                "name": stock_info["name"],
                "price": float(q.last_done),
                "prev_close": float(q.prev_close),
                "change_rate": change_rate,
                "volume": int(q.volume) if hasattr(q, 'volume') else 0,
                "board_lot": stock_info["board_lot"],
            })
    return result

# ========== 策略函数 ==========
def momentum_strategy(quotes: List[Dict]) -> List[Dict]:
    """动量策略：选择涨幅>2% 的强势股"""
    cfg = STRATEGIES["momentum"]
    selected = [q for q in quotes if q["change_rate"] >= cfg["min_change_rate"]]
    selected.sort(key=lambda x: x["change_rate"], reverse=True)
    return selected[:3]  # 最多 3 只

def mean_reversion_strategy(quotes: List[Dict]) -> List[Dict]:
    """均值回归：选择跌幅>3% 的超跌股"""
    cfg = STRATEGIES["mean_reversion"]
    selected = [q for q in quotes if q["change_rate"] <= cfg["max_change_rate"]]
    selected.sort(key=lambda x: x["change_rate"])  # 跌幅最大的在前
    return selected[:3]

def grid_strategy(quote: Dict) -> Dict:
    """网格交易：生成买卖网格"""
    cfg = STRATEGIES["grid"]
    price = quote["price"]
    board_lot = quote["board_lot"]
    
    # 生成网格
    buy_orders = []
    sell_orders = []
    
    for i in range(1, cfg["grid_levels"] + 1):
        buy_price = price * (1 - cfg["grid_spacing"] * i)
        sell_price = price * (1 + cfg["grid_spacing"] * i)
        
        buy_orders.append({
            "price": round(buy_price, 2),
            "quantity": cfg["grid_size"] // board_lot * board_lot,  # 整手
            "side": "Buy"
        })
        sell_orders.append({
            "price": round(sell_price, 2),
            "quantity": cfg["grid_size"] // board_lot * board_lot,
            "side": "Sell"
        })
    
    return {
        "symbol": quote["symbol"],
        "name": quote["name"],
        "current_price": price,
        "buy_orders": buy_orders,
        "sell_orders": sell_orders,
    }

# ========== 交易函数 ==========
def submit_order(symbol: str, side: str, price: float, quantity: int, strategy: str = "") -> Dict:
    """提交订单"""
    try:
        # 港股价格精度：HKD 0.001
        order_price = Decimal(str(round(price, 3)))
        order_qty = Decimal(str(quantity))
        
        # 使用 ELO（增强限价单）或 LO（限价单）
        order_type = OrderType.ELO if side == "Buy" else OrderType.LO
        
        resp = ctx.submit_order(
            side=OrderSide.Buy if side == "Buy" else OrderSide.Sell,
            symbol=symbol,
            order_type=order_type,
            submitted_price=order_price,
            submitted_quantity=order_qty,
            time_in_force=TimeInForceType.Day,
            remark=f"量化-{strategy}"
        )
        return {"success": True, "order_id": resp.order_id, "price": float(order_price)}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ========== 主函数 ==========
def main():
    """主函数"""
    print()
    print("=" * 80)
    print("🤖 港股量化策略框架 - 多策略测试")
    print("=" * 80)
    print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"账户：模拟账户 (Demo A/C)")
    print("=" * 80)
    print()
    
    # 1. 获取行情
    print("📊 步骤 1: 获取港股行情")
    print("-" * 80)
    quotes = get_stock_quotes()
    for q in quotes:
        flag = "📈" if q["change_rate"] > 0.02 else "📉" if q["change_rate"] < -0.02 else "➖"
        print(f"{flag} {q['symbol']:12} {q['name']:10} | 最新：HKD {q['price']:8.2f} | 涨跌：{q['change_rate']:6.2%}")
    print()
    
    # 2. 策略 1: 动量策略
    print("🚀 策略 1: 动量策略（追涨强势股）")
    print("-" * 80)
    momentum_stocks = momentum_strategy(quotes)
    if momentum_stocks:
        for s in momentum_stocks:
            cfg = STRATEGIES["momentum"]
            cost = s["price"] * cfg["position_size"]
            print(f"✅ {s['symbol']} {s['name']}: 涨幅{s['change_rate']:.2%}")
            print(f"   建议买入：{cfg['position_size']}股 @ HKD{s['price']:.2f}")
            print(f"   预估成本：HKD{cost:,.2f}")
            print(f"   止损：HKD{s['price']*(1+cfg['stop_loss']):.2f} ({cfg['stop_loss']:.0%})")
            print(f"   止盈：HKD{s['price']*(1+cfg['take_profit']):.2f} ({cfg['take_profit']:.0%})")
    else:
        print("⚠️  无符合条件的强势股")
    print()
    
    # 3. 策略 2: 均值回归
    print("📉 策略 2: 均值回归（买入超跌股）")
    print("-" * 80)
    mr_stocks = mean_reversion_strategy(quotes)
    if mr_stocks:
        for s in mr_stocks:
            cfg = STRATEGIES["mean_reversion"]
            cost = s["price"] * cfg["position_size"]
            print(f"✅ {s['symbol']} {s['name']}: 跌幅{s['change_rate']:.2%}")
            print(f"   建议买入：{cfg['position_size']}股 @ HKD{s['price']:.2f}")
            print(f"   预估成本：HKD{cost:,.2f}")
            print(f"   止损：HKD{s['price']*(1+cfg['stop_loss']):.2f} ({cfg['stop_loss']:.0%})")
            print(f"   止盈：HKD{s['price']*(1+cfg['take_profit']):.2f} ({cfg['take_profit']:.0%})")
            
            # 自动交易
            if cfg.get("auto_trade", False):
                print(f"   🔄 自动下单中...")
                result = submit_order(s["symbol"], "Buy", s["price"], cfg["position_size"], "均值回归")
                if result["success"]:
                    print(f"   ✅ 订单提交成功！ID: {result['order_id']}")
                else:
                    print(f"   ❌ 订单失败：{result['error']}")
    else:
        print("⚠️  无符合条件的超跌股")
    print()
    
    # 4. 策略 3: 网格交易（以腾讯为例）
    print("🕸️  策略 3: 网格交易（震荡市）")
    print("-" * 80)
    tencent = next((q for q in quotes if q["symbol"] == "700.HK"), None)
    if tencent:
        grid = grid_strategy(tencent)
        print(f"{grid['symbol']} {grid['name']} 当前价：HKD{grid['current_price']:.2f}")
        print()
        print("买入网格（挂单）:")
        for order in grid["buy_orders"]:
            print(f"  买入 {order['quantity']}股 @ HKD{order['price']:.2f}")
        print()
        print("卖出网格（持仓卖出）:")
        for order in grid["sell_orders"]:
            print(f"  卖出 {order['quantity']}股 @ HKD{order['price']:.2f}")
    else:
        print("⚠️  无法获取腾讯行情")
    print()
    
    # 5. 账户状态
    print("💰 账户状态")
    print("-" * 80)
    balances = ctx.account_balance()
    for b in balances:
        print(f"币种：{b.currency}")
        print(f"  总现金：HKD{b.total_cash:,.2f}")
        if b.cash_infos:
            print(f"  可用现金：HKD{b.cash_infos[0].available_cash:,.2f}")
            print(f"  冻结现金：HKD{b.cash_infos[0].frozen_cash:,.2f}")
    print()
    
    # 6. 今日订单
    print("📋 今日订单")
    print("-" * 80)
    orders = ctx.today_orders()
    if orders:
        for o in orders:
            side_str = "买入" if str(o.side) == "Buy" else "卖出"
            print(f"{o.order_id}: {side_str} {o.symbol} {o.quantity}股 @ {o.price} - {o.status}")
    else:
        print("无订单")
    print()
    
    print("=" * 80)
    print("✅ 策略分析完成")
    print()
    print("⚠️  风险提示:")
    print("   - 这是策略框架演示，未实际下单")
    print("   - 模拟账户交易功能可能受限")
    print("   - 过往表现不代表未来收益")
    print("   - 量化交易需严格风控")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
