#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长桥 OpenAPI 交易执行脚本
支持下单、撤单、查询订单等功能
"""

from decimal import Decimal
from longport.openapi import TradeContext, Config, OrderSide, OrderType, TimeInForceType
from dotenv import load_dotenv
from datetime import datetime
import os

# 加载环境变量
load_dotenv()

class TradeExecutor:
    """交易执行器"""
    
    def __init__(self):
        """初始化交易上下文"""
        self.config = Config.from_env()
        self.ctx = TradeContext(self.config)
        print("✅ 交易上下文已初始化")
    
    def submit_buy(self, symbol: str, price: float, quantity: int, remark: str = ""):
        """
        买入订单
        
        Args:
            symbol: 证券代码（如 AAPL.US）
            price: 限价价格
            quantity: 数量
            remark: 备注
        """
        print(f"\n📤 提交买入订单：{symbol}")
        print(f"   价格：${price} | 数量：{quantity} | 备注：{remark}")
        
        try:
            resp = self.ctx.submit_order(
                side=OrderSide.Buy,
                symbol=symbol,
                order_type=OrderType.LO,
                submitted_price=Decimal(str(price)),
                submitted_quantity=Decimal(str(quantity)),
                time_in_force=TimeInForceType.Day,
                remark=remark
            )
            print(f"✅ 订单提交成功！订单 ID: {resp.order_id}")
            return resp.order_id
        except Exception as e:
            print(f"❌ 订单提交失败：{e}")
            return None
    
    def submit_sell(self, symbol: str, price: float, quantity: int, remark: str = ""):
        """
        卖出订单
        
        Args:
            symbol: 证券代码
            price: 限价价格
            quantity: 数量
            remark: 备注
        """
        print(f"\n📤 提交卖出订单：{symbol}")
        print(f"   价格：${price} | 数量：{quantity} | 备注：{remark}")
        
        try:
            resp = self.ctx.submit_order(
                side=OrderSide.Sell,
                symbol=symbol,
                order_type=OrderType.LO,
                submitted_price=Decimal(str(price)),
                submitted_quantity=Decimal(str(quantity)),
                time_in_force=TimeInForceType.Day,
                remark=remark
            )
            print(f"✅ 订单提交成功！订单 ID: {resp.order_id}")
            return resp.order_id
        except Exception as e:
            print(f"❌ 订单提交失败：{e}")
            return None
    
    def cancel_order(self, order_id: str):
        """
        撤单
        
        Args:
            order_id: 订单 ID
        """
        print(f"\n📤 撤销订单：{order_id}")
        
        try:
            self.ctx.withdraw_order(order_id)
            print(f"✅ 撤单成功！")
            return True
        except Exception as e:
            print(f"❌ 撤单失败：{e}")
            return False
    
    def get_today_orders(self):
        """
        查询今日订单
        
        Returns:
            订单列表
        """
        print("\n📋 查询今日订单...")
        
        try:
            orders = self.ctx.today_orders()
            print(f"✅ 共查询到 {len(orders)} 个订单")
            
            for order in orders:
                status_map = {
                    "Submitted": "已提交",
                    "Filled": "已成交",
                    "Cancelled": "已撤销",
                    "Rejected": "已拒绝",
                    "PartiallyFilled": "部分成交"
                }
                status = status_map.get(str(order.status), str(order.status))
                
                side_str = "买入" if order.side == OrderSide.Buy else "卖出"
                print(f"   {order.order_id}: {side_str} {order.symbol} {order.quantity}股 @ ${order.price} - {status}")
            
            return orders
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return []
    
    def get_account_balance(self):
        """
        查询账户余额
        
        Returns:
            账户余额信息
        """
        print("\n💰 查询账户余额...")
        
        try:
            balances = self.ctx.account_balance()
            
            for balance in balances:
                print(f"   币种：{balance.currency}")
                print(f"     总现金：${balance.total_cash:,.2f}")
                if balance.cash_infos:
                    cash = balance.cash_infos[0]
                    print(f"     可用现金：${cash.available_cash:,.2f}")
                    print(f"     冻结现金：${cash.frozen_cash:,.2f}")
            
            return balances
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return []
    
    def get_positions(self):
        """
        查询持仓
        
        Returns:
            持仓列表
        """
        print("\n📊 查询持仓...")
        
        try:
            resp = self.ctx.stock_positions()
            # resp.channels 是 StockPositionChannel 列表，每个 channel 有 positions 属性
            all_positions = []
            for channel in resp.channels:
                if hasattr(channel, 'positions'):
                    all_positions.extend(channel.positions)
            
            print(f"✅ 共查询到 {len(all_positions)} 个持仓")
            
            for pos in all_positions:
                symbol = pos.symbol if hasattr(pos, 'symbol') else 'N/A'
                quantity = pos.quantity if hasattr(pos, 'quantity') else 0
                cost_price = pos.cost_price if hasattr(pos, 'cost_price') else 0
                last_done = pos.last_done if hasattr(pos, 'last_done') else 0
                print(f"   {symbol}: {quantity}股 | 成本：${cost_price} | 市价：${last_done}")
            
            return all_positions
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return []

def main():
    """主函数 - 演示用法"""
    print()
    print("🚀 长桥 OpenAPI 交易执行器")
    print("=" * 60)
    
    executor = TradeExecutor()
    
    try:
        # 查询账户余额
        executor.get_account_balance()
        
        # 查询持仓
        executor.get_positions()
        
        # 查询今日订单
        executor.get_today_orders()
        
        # ============ 示例交易（注释掉，需要时取消注释）============
        # 买入 100 股 NVDA，限价$180
        # order_id = executor.submit_buy("NVDA.US", 180, 100, "测试买单")
        
        # 卖出 100 股 AAPL，限价$200
        # order_id = executor.submit_sell("AAPL.US", 200, 100, "测试卖单")
        
        # 撤单
        # executor.cancel_order("订单 ID")
        # =========================================================
        
    finally:
        print("\n✅ 交易执行器演示完成")
        print()
    
    print("=" * 60)

if __name__ == "__main__":
    main()
