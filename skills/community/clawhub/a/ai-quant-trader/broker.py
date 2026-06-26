#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟交易引擎 - 支持蜻蜓点金手续费规则
"""

import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

class SimulatedBroker:
    """模拟券商（蜻蜓点金规则）"""
    
    def __init__(self, initial_capital=100000):
        # 资金管理
        self.initial_capital = float(initial_capital)
        self.capital = float(initial_capital)  # 可用资金
        self.total_capital = float(initial_capital)  # 总资产（现金+持仓市值）
        
        # 持仓管理
        self.positions = {}  # {symbol: {'shares': 100, 'avg_cost': 50.0, 'current_price': 55.0}}
        
        # 交易记录
        self.trade_history = []
        
        # 手续费规则（蜻蜓点金）
        self.commission_rate = 0.0003  # 佣金0.03%
        self.min_commission = 5.0  # 最低佣金5元
        self.stamp_tax_rate = 0.001  # 印花税0.1%（仅卖出）
        self.transfer_fee_rate = 0.00001  # 过户费0.001%
        
        print(f"✅ 模拟交易引擎初始化完成，初始资金: {self.initial_capital:,.2f}元")
    
    def calculate_fee(self, action, amount, price):
        """
        计算手续费（蜻蜓点金规则）
        
        参数:
            action: 'buy' 或 'sell'
            amount: 数量（股）
            price: 价格（元）
        
        返回:
            total_fee: 总手续费
            breakdown: 费用明细
        """
        trade_amount = amount * price
        
        # 佣金
        commission = trade_amount * self.commission_rate
        if commission < self.min_commission:
            commission = self.min_commission
        
        # 过户费（买卖都收）
        transfer_fee = trade_amount * self.transfer_fee_rate
        
        if action == 'buy':
            # 买入：佣金 + 过户费
            total_fee = commission + transfer_fee
            breakdown = {
                'commission': commission,
                'transfer_fee': transfer_fee,
                'stamp_tax': 0
            }
        else:  # sell
            # 卖出：佣金 + 印花税 + 过户费
            stamp_tax = trade_amount * self.stamp_tax_rate
            total_fee = commission + stamp_tax + transfer_fee
            breakdown = {
                'commission': commission,
                'stamp_tax': stamp_tax,
                'transfer_fee': transfer_fee
            }
        
        return total_fee, breakdown
    
    def set_capital(self, capital):
        """设置初始资金"""
        self.initial_capital = float(capital)
        self.capital = float(capital)
        self.total_capital = float(capital)
        self.positions = {}
        self.trade_history = []
        return f"✅ 资金已重置为: {capital:,.2f}元"
    
    def buy(self, symbol, amount, price, auto=False):
        """买入股票"""
        try:
            amount = int(amount)
            price = float(price)
            
            if amount <= 0:
                return "❌ 买入数量必须大于0"
            
            if price <= 0:
                return "❌ 价格必须大于0"
            
            # 计算总金额和手续费
            total_cost = amount * price
            fee, fee_breakdown = self.calculate_fee('buy', amount, price)
            total_with_fee = total_cost + fee
            
            # 检查资金是否足够
            if total_with_fee > self.capital:
                return f"❌ 资金不足，需要{total_with_fee:,.2f}元，可用{self.capital:,.2f}元"
            
            # 执行买入
            self.capital -= total_with_fee
            
            # 更新持仓
            if symbol in self.positions:
                # 已有持仓，计算平均成本
                pos = self.positions[symbol]
                total_shares = pos['shares'] + amount
                total_value = (pos['shares'] * pos['avg_cost']) + total_cost
                new_avg_cost = total_value / total_shares
                
                pos['shares'] = total_shares
                pos['avg_cost'] = new_avg_cost
                pos['current_price'] = price
            else:
                # 新建持仓
                self.positions[symbol] = {
                    'shares': amount,
                    'avg_cost': price,
                    'current_price': price,
                    'buy_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # 更新总资产
            self.update_total_capital(price)
            
            # 记录交易
            trade_record = {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'action': 'buy',
                'symbol': symbol,
                'amount': amount,
                'price': price,
                'total_cost': total_cost,
                'fee': fee,
                'fee_breakdown': fee_breakdown,
                'remaining_capital': self.capital,
                'auto': auto
            }
            self.trade_history.append(trade_record)
            
            return (f"✅ 买入成功！\n"
                   f"股票: {symbol}\n"
                   f"数量: {amount}股\n"
                   f"价格: {price:.2f}元\n"
                   f"总金额: {total_cost:,.2f}元\n"
                   f"手续费: {fee:.2f}元\n"
                   f"剩余资金: {self.capital:,.2f}元")
        
        except Exception as e:
            return f"❌ 买入失败: {str(e)}"
    
    def sell(self, symbol, amount, price, auto=False):
        """卖出股票"""
        try:
            amount = int(amount)
            price = float(price)
            
            if amount <= 0:
                return "❌ 卖出数量必须大于0"
            
            if price <= 0:
                return "❌ 价格必须大于0"
            
            # 检查持仓
            if symbol not in self.positions:
                return f"❌ 未持有股票: {symbol}"
            
            pos = self.positions[symbol]
            if amount > pos['shares']:
                return f"❌ 持仓不足，持有{pos['shares']}股，尝试卖出{amount}股"
            
            # 计算收入和手续费
            total_revenue = amount * price
            fee, fee_breakdown = self.calculate_fee('sell', amount, price)
            net_revenue = total_revenue - fee
            
            # 计算盈亏
            cost = amount * pos['avg_cost']
            profit = total_revenue - cost - fee
            profit_percentage = (profit / cost * 100) if cost > 0 else 0
            
            # 执行卖出
            self.capital += net_revenue
            
            # 更新持仓
            if amount == pos['shares']:
                # 全部卖出，删除持仓
                del self.positions[symbol]
            else:
                # 部分卖出
                pos['shares'] -= amount
                pos['current_price'] = price
            
            # 更新总资产
            self.update_total_capital(price)
            
            # 记录交易
            trade_record = {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'action': 'sell',
                'symbol': symbol,
                'amount': amount,
                'price': price,
                'total_revenue': total_revenue,
                'fee': fee,
                'fee_breakdown': fee_breakdown,
                'net_revenue': net_revenue,
                'profit': profit,
                'profit_percentage': profit_percentage,
                'remaining_capital': self.capital,
                'auto': auto
            }
            self.trade_history.append(trade_record)
            
            profit_text = "盈利" if profit >= 0 else "亏损"
            
            return (f"✅ 卖出成功！\n"
                   f"股票: {symbol}\n"
                   f"数量: {amount}股\n"
                   f"价格: {price:.2f}元\n"
                   f"总收入: {total_revenue:,.2f}元\n"
                   f"手续费: {fee:.2f}元\n"
                   f"净收入: {net_revenue:,.2f}元\n"
                   f"盈亏: {profit_text} {abs(profit):,.2f}元 ({profit_percentage:.1f}%)\n"
                   f"剩余资金: {self.capital:,.2f}元")
        
        except Exception as e:
            return f"❌ 卖出失败: {str(e)}"
    
    def update_total_capital(self, current_price=None):
        """更新总资产（现金+持仓市值）"""
        # 如果有指定价格，更新对应股票的当前价
        if current_price is not None:
            # 这里需要外部调用时指定symbol，简化处理
            pass
        
        # 计算持仓总市值
        position_value = 0
        for symbol, pos in self.positions.items():
            # 使用平均成本作为当前价（简化，实际应从市场获取）
            position_value += pos['shares'] * pos.get('current_price', pos['avg_cost'])
        
        self.total_capital = self.capital + position_value
    
    def show_positions(self):
        """显示持仓"""
        if not self.positions:
            return "📭 当前无持仓"
        
        result = "📊 当前持仓:\n"
        result += f"可用资金: {self.capital:,.2f}元\n"
        result += f"总资产: {self.total_capital:,.2f}元\n\n"
        
        total_position_value = 0
        total_profit = 0
        
        for symbol, pos in self.positions.items():
            shares = pos['shares']
            avg_cost = pos['avg_cost']
            current_price = pos.get('current_price', avg_cost)
            
            position_value = shares * current_price
            cost_value = shares * avg_cost
            profit = position_value - cost_value
            profit_percentage = (profit / cost_value * 100) if cost_value > 0 else 0
            
            total_position_value += position_value
            total_profit += profit
            
            profit_text = "📈" if profit >= 0 else "📉"
            
            result += (f"{profit_text} {symbol}\n"
                      f"   持仓: {shares}股\n"
                      f"   成本: {avg_cost:.2f}元\n"
                      f"   现价: {current_price:.2f}元\n"
                      f"   市值: {position_value:,.2f}元\n"
                      f"   盈亏: {profit:+,.2f}元 ({profit_percentage:+.1f}%)\n")
        
        result += f"\n📈 持仓总市值: {total_position_value:,.2f}元\n"
        result += f"💰 总盈亏: {total_profit:+,.2f}元"
        
        return result
    
    def get_position(self, symbol):
        """获取指定股票的持仓信息"""
        return self.positions.get(symbol)
    
    def get_positions_data(self):
        """获取持仓数据（用于保存）"""
        return {
            'capital': self.capital,
            'total_capital': self.total_capital,
            'positions': self.positions,
            'trade_history': self.trade_history[-100:]  # 只保存最近100条记录
        }
    
    def load_positions(self, data):
        """加载持仓数据"""
        if 'capital' in data:
            self.capital = data['capital']
            self.total_capital = data.get('total_capital', self.capital)
        
        if 'positions' in data:
            self.positions = data['positions']
        
        if 'trade_history' in data:
            self.trade_history = data['trade_history']
    
    def get_trade_history(self, limit=10):
        """获取交易历史"""
        if not self.trade_history:
            return "暂无交易记录"
        
        result = "📝 最近交易记录:\n"
        for trade in self.trade_history[-limit:]:
            action = "买入" if trade['action'] == 'buy' else "卖出"
            auto = "🤖" if trade.get('auto', False) else "👤"
            result += f"\n{auto} {trade['time']} {action} {trade['symbol']} {trade['amount']}股 @{trade['price']:.2f}元"
            if trade['action'] == 'sell' and 'profit' in trade:
                profit = trade['profit']
                result += f" 盈亏: {profit:+,.2f}元"
        
        return result
    
    def check_stop_loss(self, symbol, current_price, stop_loss_percent):
        """检查是否触发止损"""
        if symbol not in self.positions:
            return False, None
        
        pos = self.positions[symbol]
        avg_cost = pos['avg_cost']
        stop_loss_price = avg_cost * (1 - stop_loss_percent / 100)
        
        if current_price <= stop_loss_price:
            return True, stop_loss_price
        
        return False, None
    
    def check_take_profit(self, symbol, current_price, take_profit_percent):
        """检查是否触发止盈"""
        if symbol not in self.positions:
            return False, None
        
        pos = self.positions[symbol]
        avg_cost = pos['avg_cost']
        take_profit_price = avg_cost * (1 + take_profit_percent / 100)
        
        if current_price >= take_profit_price:
            return True, take_profit_price
        
        return False, None

# 测试代码
if __name__ == "__main__":
    broker = SimulatedBroker(100000)
    
    # 测试买入
    print(broker.buy("600519", 100, 1800))
    print(broker.show_positions())
    
    # 测试卖出
    print(broker.sell("600519", 50, 1850))
    print(broker.show_positions())
    
    # 测试交易历史
    print(broker.get_trade_history())