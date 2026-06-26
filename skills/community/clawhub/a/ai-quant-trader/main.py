#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI量化交易助手 - 主程序
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from broker import SimulatedBroker
from strategy_gen import StrategyGenerator
from auto_trader import AutoTrader
from risk_manager import RiskManager
from stock_screener import StockScreener
from data_provider import DataProvider
import json
from datetime import datetime

class AIQuantTrader:
    """AI量化交易助手主类"""
    
    def __init__(self):
        # 初始化各模块
        self.broker = SimulatedBroker()
        self.strategy_gen = StrategyGenerator()
        self.auto_trader = AutoTrader(self.broker)
        self.risk_manager = RiskManager(self.broker)
        self.stock_screener = StockScreener()
        self.data_provider = DataProvider()
        
        # 加载用户数据
        self.load_user_data()
    
    def load_user_data(self):
        """加载用户数据"""
        data_dir = os.path.join(os.path.dirname(__file__), 'user_data')
        os.makedirs(data_dir, exist_ok=True)
        
        # 用户配置文件
        self.user_config_file = os.path.join(data_dir, 'config.json')
        self.strategies_file = os.path.join(data_dir, 'strategies.json')
        self.positions_file = os.path.join(data_dir, 'positions.json')
        
        # 加载配置
        if os.path.exists(self.user_config_file):
            with open(self.user_config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'initial_capital': 100000,
                'auto_trade_enabled': False,
                'risk_level': 'medium'
            }
        
        # 加载策略
        if os.path.exists(self.strategies_file):
            with open(self.strategies_file, 'r', encoding='utf-8') as f:
                self.strategies = json.load(f)
        else:
            self.strategies = {}
        
        # 加载持仓
        if os.path.exists(self.positions_file):
            with open(self.positions_file, 'r', encoding='utf-8') as f:
                positions_data = json.load(f)
                self.broker.load_positions(positions_data)
    
    def save_user_data(self):
        """保存用户数据"""
        # 保存配置
        with open(self.user_config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        
        # 保存策略
        with open(self.strategies_file, 'w', encoding='utf-8') as f:
            json.dump(self.strategies, f, ensure_ascii=False, indent=2)
        
        # 保存持仓
        positions_data = self.broker.get_positions_data()
        with open(self.positions_file, 'w', encoding='utf-8') as f:
            json.dump(positions_data, f, ensure_ascii=False, indent=2)
    
    def process_command(self, command):
        """处理用户命令"""
        try:
            parts = command.strip().split()
            if not parts:
                return "请输入有效命令"
            
            cmd_type = parts[0]
            
            if cmd_type == '/交易':
                return self.process_trade_command(parts[1:])
            elif cmd_type == '/策略':
                return self.process_strategy_command(parts[1:])
            elif cmd_type == '/自动':
                return self.process_auto_command(parts[1:])
            elif cmd_type == '/风控':
                return self.process_risk_command(parts[1:])
            elif cmd_type == '/选股':
                return self.process_screening_command(parts[1:])
            elif cmd_type == '/统计':
                return self.process_stat_command(parts[1:])
            elif cmd_type == '/持仓':
                return self.show_positions()
            elif cmd_type == '/帮助':
                return self.show_help()
            else:
                return f"未知命令: {command}\n输入 /帮助 查看可用命令"
        
        except Exception as e:
            return f"❌ 命令执行错误: {str(e)}"
    
    def process_trade_command(self, args):
        """处理交易命令"""
        if not args:
            return "交易命令格式: /交易 [操作] [参数]"
        
        operation = args[0]
        
        if operation == '设置本金':
            if len(args) < 2:
                return "格式: /交易 设置本金 [金额]"
            try:
                capital = float(args[1])
                self.broker.set_capital(capital)
                self.config['initial_capital'] = capital
                self.save_user_data()
                return f"✅ 已设置初始资金: {capital:,.2f}元"
            except ValueError:
                return "❌ 金额必须是数字"
        
        elif operation == '买入':
            if len(args) < 3:
                return "格式: /交易 买入 [股票代码] [数量]"
            symbol = args[1]
            try:
                amount = int(args[2])
                # 获取当前价格
                price = self.data_provider.get_current_price(symbol)
                if price is None:
                    return f"❌ 无法获取 {symbol} 的当前价格"
                
                result = self.broker.buy(symbol, amount, price)
                self.save_user_data()
                return result
            except ValueError:
                return "❌ 数量必须是整数"
        
        elif operation == '卖出':
            if len(args) < 3:
                return "格式: /交易 卖出 [股票代码] [数量]"
            symbol = args[1]
            try:
                amount = int(args[2])
                price = self.data_provider.get_current_price(symbol)
                if price is None:
                    return f"❌ 无法获取 {symbol} 的当前价格"
                
                result = self.broker.sell(symbol, amount, price)
                self.save_user_data()
                return result
            except ValueError:
                return "❌ 数量必须是整数"
        
        else:
            return f"未知交易操作: {operation}"
    
    def process_strategy_command(self, args):
        """处理策略命令"""
        if not args:
            return "策略命令格式: /策略 [操作] [参数]"
        
        operation = args[0]
        
        if operation == '生成':
            if len(args) < 2:
                return "格式: /策略 生成 [策略描述]"
            description = ' '.join(args[1:])
            return self.strategy_gen.generate_strategy(description, self.strategies)
        
        elif operation == '优化':
            if len(args) < 2:
                return "格式: /策略 优化 [策略名]"
            strategy_name = args[1]
            return self.strategy_gen.optimize_strategy(strategy_name, self.strategies)
        
        elif operation == '列表':
            return self.show_strategies()
        
        elif operation == '回测':
            if len(args) < 2:
                return "格式: /策略 回测 [策略名]"
            strategy_name = args[1]
            return self.strategy_gen.backtest_strategy(strategy_name, self.strategies)
        
        else:
            return f"未知策略操作: {operation}"
    
    def process_auto_command(self, args):
        """处理自动交易命令"""
        if not args:
            return "自动交易命令格式: /自动 [操作] [参数]"
        
        operation = args[0]
        
        if operation == '启用':
            if len(args) < 3:
                return "格式: /自动 启用 [策略名] [股票代码]"
            strategy_name = args[1]
            symbol = args[2]
            return self.auto_trader.enable_strategy(strategy_name, symbol, self.strategies)
        
        elif operation == '暂停':
            if len(args) < 2:
                return "格式: /自动 暂停 [股票代码]"
            symbol = args[1]
            return self.auto_trader.disable_strategy(symbol)
        
        elif operation == '列表':
            return self.auto_trader.list_strategies()
        
        else:
            return f"未知自动交易操作: {operation}"
    
    def process_risk_command(self, args):
        """处理风控命令"""
        if not args:
            return "风控命令格式: /风控 [操作] [参数]"
        
        operation = args[0]
        
        if operation == '设置止损':
            if len(args) < 3:
                return "格式: /风控 设置止损 [股票代码] [百分比]"
            symbol = args[1]
            try:
                percentage = float(args[2].rstrip('%'))
                return self.risk_manager.set_stop_loss(symbol, percentage)
            except ValueError:
                return "❌ 百分比必须是数字"
        
        elif operation == '设置止盈':
            if len(args) < 3:
                return "格式: /风控 设置止盈 [股票代码] [百分比]"
            symbol = args[1]
            try:
                percentage = float(args[2].rstrip('%'))
                return self.risk_manager.set_take_profit(symbol, percentage)
            except ValueError:
                return "❌ 百分比必须是数字"
        
        elif operation == '移动止盈':
            if len(args) < 3:
                return "格式: /风控 移动止盈 [股票代码] [回撤百分比]"
            symbol = args[1]
            try:
                percentage = float(args[2].rstrip('%'))
                return self.risk_manager.set_trailing_stop(symbol, percentage)
            except ValueError:
                return "❌ 百分比必须是数字"
        
        else:
            return f"未知风控操作: {operation}"
    
    def process_screening_command(self, args):
        """处理选股命令"""
        if not args:
            return "选股命令格式: /选股 [操作] [参数]"
        
        operation = args[0]
        
        if operation == '今日推荐':
            return self.stock_screener.get_today_recommendations()
        
        elif operation == '筛选':
            if len(args) < 2:
                return "格式: /选股 筛选 [条件]"
            conditions = ' '.join(args[1:])
            return self.stock_screener.screen_stocks(conditions)
        
        else:
            return f"未知选股操作: {operation}"
    
    def process_stat_command(self, args):
        """处理统计命令"""
        if not args:
            return "统计命令格式: /统计 [策略名]"
        
        strategy_name = args[0]
        if strategy_name in self.strategies:
            return self.strategy_gen.get_strategy_stats(strategy_name, self.strategies)
        else:
            return f"❌ 未找到策略: {strategy_name}"
    
    def show_positions(self):
        """显示持仓"""
        return self.broker.show_positions()
    
    def show_strategies(self):
        """显示策略列表"""
        if not self.strategies:
            return "📝 暂无策略，使用 /策略 生成 [描述] 创建策略"
        
        result = "📋 策略列表:\n"
        for name, strategy in self.strategies.items():
            created = strategy.get('created', '未知时间')
            result += f"\n🔹 {name}\n"
            result += f"   描述: {strategy.get('description', '无描述')}\n"
            result += f"   创建: {created}\n"
            if 'stats' in strategy:
                win_rate = strategy['stats'].get('win_rate', 0)
                result += f"   胜率: {win_rate:.1f}%\n"
        
        return result
    
    def show_help(self):
        """显示帮助"""
        help_text = """
🤖 AI量化交易助手 - 帮助手册

📊 交易命令:
  /交易 设置本金 [金额]   设置初始资金
  /交易 买入 [代码] [数量] 买入股票
  /交易 卖出 [代码] [数量] 卖出股票
  /持仓                   查看持仓

🤖 策略命令:
  /策略 生成 [描述]       AI生成策略
  /策略 优化 [策略名]     优化策略参数
  /策略 列表             查看所有策略
  /策略 回测 [策略名]     回测策略表现

⚡ 自动交易:
  /自动 启用 [策略] [代码] 启用自动交易
  /自动 暂停 [代码]       暂停自动交易
  /自动 列表             查看自动交易状态

🛡️ 风控命令:
  /风控 设置止损 [代码] [%] 设置止损
  /风控 设置止盈 [代码] [%] 设置止盈
  /风控 移动止盈 [代码] [%] 设置移动止盈

📈 选股统计:
  /选股 今日推荐          AI推荐今日股票
  /选股 筛选 [条件]       按条件筛选
  /统计 [策略名]         查看策略统计

❓ 其他:
  /帮助                  显示此帮助
  /持仓                  查看当前持仓

💡 示例:
  /交易 设置本金 100000
  /选股 今日推荐
  /策略 生成 "MACD金叉短线策略"
  /自动 启用 MACD策略 600519
  /风控 设置止损 600519 5%
"""
        return help_text

# 单例实例
_trader_instance = None

def get_trader():
    """获取交易助手实例"""
    global _trader_instance
    if _trader_instance is None:
        _trader_instance = AIQuantTrader()
    return _trader_instance

def handle_command(command):
    """处理命令入口函数"""
    trader = get_trader()
    return trader.process_command(command)

if __name__ == "__main__":
    # 测试代码
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        result = handle_command(command)
        print(result)
    else:
        print("AI量化交易助手已启动")
        print("输入 /帮助 查看命令")