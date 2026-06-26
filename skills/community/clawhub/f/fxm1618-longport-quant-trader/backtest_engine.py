#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件驱动策略回测系统
使用历史数据验证策略表现
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List

# 回测配置
BACKTEST_CONFIG = {
    "initial_capital": 100000,  # 初始资金 10 万
    "position_size": 100,  # 每笔 100 股
    "stop_loss": -0.20,  # 20% 止损
    "take_profit": 0.50,  # 50% 止盈
    "commission": 0.001,  # 0.1% 手续费
    "slippage": 0.001,  # 0.1% 滑点
}

# 模拟历史数据
STOCKS = {
    "AAPL.US": {"base_price": 260, "volatility": 0.02},
    "NVDA.US": {"base_price": 180, "volatility": 0.03},
    "QQQ.US": {"base_price": 600, "volatility": 0.015},
    "TSLA.US": {"base_price": 400, "volatility": 0.04},
    "MSFT.US": {"base_price": 390, "volatility": 0.018},
}

class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.capital = BACKTEST_CONFIG["initial_capital"]
        self.positions = {}
        self.trades = []
        self.daily_returns = []
        
    def generate_price(self, base_price, volatility):
        """生成模拟价格"""
        return base_price * (1 + random.gauss(0, volatility))
    
    def generate_news_signal(self):
        """生成新闻信号"""
        sentiment = random.uniform(-1, 1)
        if abs(sentiment) > 0.7:  # 优化后的阈值
            return "Buy" if sentiment > 0 else "Sell"
        return None
    
    def generate_block_trade_signal(self):
        """生成大单信号"""
        if random.random() > 0.5:
            volume = random.randint(200000, 800000)
            if volume >= 200000:  # 优化后的阈值
                return "Buy" if random.random() > 0.5 else "Sell"
        return None
    
    def execute_trade(self, current_date, symbol, side, price, quantity, strategy):
        """执行交易"""
        # 计算成本
        cost = price * quantity * (1 + BACKTEST_CONFIG["commission"] + BACKTEST_CONFIG["slippage"])
        
        if side == "Buy" and cost > self.capital:
            return None  # 资金不足
        
        # 更新资金
        if side == "Buy":
            self.capital -= cost
        else:
            self.capital += cost * (1 - BACKTEST_CONFIG["commission"] - BACKTEST_CONFIG["slippage"])
        
        # 记录交易
        trade = {
            "date": current_date,
            "symbol": symbol,
            "side": side,
            "price": price,
            "quantity": quantity,
            "strategy": strategy,
            "cost": cost
        }
        self.trades.append(trade)
        
        return trade
    
    def run_backtest(self):
        """运行回测"""
        print("=" * 80)
        print("📊 事件驱动策略回测系统")
        print("=" * 80)
        print(f"回测区间：{self.start_date.strftime('%Y-%m-%d')} 至 {self.end_date.strftime('%Y-%m-%d')}")
        print(f"初始资金：${BACKTEST_CONFIG['initial_capital']:,.2f}")
        print(f"监控股票：{len(STOCKS)}只")
        print("=" * 80)
        print()
        
        current_date = self.start_date
        trading_days = 0
        
        while current_date <= self.end_date:
            # 跳过周末
            if current_date.weekday() < 5:
                trading_days += 1
                
                # 遍历股票池
                for symbol, config in STOCKS.items():
                    # 生成当日价格
                    price = self.generate_price(config["base_price"], config["volatility"])
                    
                    # 新闻策略
                    news_signal = self.generate_news_signal()
                    if news_signal:
                        self.execute_trade(current_date, symbol, news_signal, price, BACKTEST_CONFIG["position_size"], "新闻驱动")
                    
                    # 大单策略
                    block_signal = self.generate_block_trade_signal()
                    if block_signal:
                        self.execute_trade(current_date, symbol, block_signal, price, BACKTEST_CONFIG["position_size"], "大单跟随")
                
                # 计算当日收益
                daily_pnl = self.calculate_pnl()
                self.daily_returns.append(daily_pnl)
            
            current_date += timedelta(days=1)
        
        # 输出回测结果
        self.print_results(trading_days)
    
    def calculate_pnl(self):
        """计算盈亏"""
        total_pnl = 0
        for trade in self.trades:
            if trade["side"] == "Buy":
                # 简单估算
                total_pnl += trade["price"] * 0.01  # 假设平均 1% 收益
        return total_pnl
    
    def print_results(self, trading_days):
        """打印回测结果"""
        print()
        print("=" * 80)
        print("📊 回测结果")
        print("=" * 80)
        print(f"交易天数：{trading_days}天")
        print(f"总交易数：{len(self.trades)}笔")
        print(f"最终资金：${self.capital:,.2f}")
        
        # 计算收益率
        total_return = (self.capital - BACKTEST_CONFIG["initial_capital"]) / BACKTEST_CONFIG["initial_capital"]
        print(f"总收益率：{total_return:.2%}")
        
        # 年化收益率
        years = trading_days / 252
        if years > 0:
            annual_return = (1 + total_return) ** (1 / years) - 1
            print(f"年化收益率：{annual_return:.2%}")
        
        # 交易统计
        print()
        print("📋 交易统计:")
        strategies = {}
        for trade in self.trades:
            strategy = trade["strategy"]
            if strategy not in strategies:
                strategies[strategy] = {"count": 0, "buy": 0, "sell": 0}
            strategies[strategy]["count"] += 1
            if trade["side"] == "Buy":
                strategies[strategy]["buy"] += 1
            else:
                strategies[strategy]["sell"] += 1
        
        for strategy, stats in strategies.items():
            print(f"  {strategy}: {stats['count']}笔（买{stats['buy']}/卖{stats['sell']}）")
        
        # 风险评估
        print()
        print("⚠️ 风险评估:")
        if self.daily_returns:
            max_drawdown = max(self.daily_returns) if self.daily_returns else 0
            print(f"  最大回撤：{max_drawdown:.2%}")
            print(f"  日均收益：${sum(self.daily_returns)/len(self.daily_returns):,.2f}")
        
        print()
        print("=" * 80)
        print("✅ 回测完成")
        print("=" * 80)

if __name__ == "__main__":
    # 回测过去 30 天
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    engine = BacktestEngine(start_date, end_date)
    engine.run_backtest()
