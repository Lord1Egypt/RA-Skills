#!/usr/bin/env python3
"""
AKQuant 双均线策略示例
使用 AKShare 获取数据，AKQuant 进行回测
"""

import akquant as aq
import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


class DoubleMAStrategy:
    """
    双均线策略
    金叉买入，死叉卖出
    """
    
    def __init__(self, fast_period=10, slow_period=30):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.fast_ma = aq.SMA(fast_period)
        self.slow_ma = aq.SMA(slow_period)
        self.position = 0
        
    def on_bar(self, bar):
        """K线事件"""
        # 更新指标
        self.fast_ma.update(bar['close'])
        self.slow_ma.update(bar['close'])
        
        # 指标初始化完成后再交易
        if not self.fast_ma.value or not self.slow_ma.value:
            return 'HOLD'
            
        fast_val = self.fast_ma.value
        slow_val = self.slow_ma.value
        
        # 金叉买入 (快线上穿慢线)
        if fast_val > slow_val and self.position <= 0:
            self.position = 1
            return 'BUY'
        
        # 死叉卖出 (快线下穿慢线)
        elif fast_val < slow_val and self.position > 0:
            self.position = 0
            return 'SELL'
        
        return 'HOLD'


def load_stock_data(symbol="000001", start_date=None, end_date=None):
    """
    使用 AKShare 获取股票数据，优先使用本地 CSV
    
    Args:
        symbol: 股票代码 (如 "000001" 平安银行)
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
    """
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    
    # 检查是否有本地 CSV 数据
    csv_path = f"/root/.openclaw/workspace/data/etf_{symbol}_history.csv"
    
    if os.path.exists(csv_path):
        print(f"发现本地数据：{csv_path}")
        # 读取本地 CSV
        df = pd.read_csv(csv_path)
        
        # 重命名列以适配 AKQuant（CSV 使用英文列名）
        df = df.rename(columns={
            'date': 'timestamp',
            'open': 'open',
            'close': 'close',
            'high': 'high',
            'low': 'low',
            'volume': 'volume'
        })
        
        # 转换日期格式
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        print(f"从本地加载 {len(df)} 条数据")
        return df
    else:
        print(f"正在获取 {symbol} 从 {start_date} 到 {end_date} 的数据...")
        
        # 获取日线数据（回退到网络）
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        # 重命名列以适配 AKQuant
        df = df.rename(columns={
            '日期': 'timestamp',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume'
        })
        
        # 转换日期格式
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        print(f"获取到 {len(df)} 条数据")
        return df


def run_double_ma_backtest(symbol="000001", fast_period=10, slow_period=30, 
                           initial_capital=100000, start_date=None, end_date=None):
    """
    运行双均线回测
    
    Args:
        symbol: 股票代码
        fast_period: 快线周期
        slow_period: 慢线周期
        initial_capital: 初始资金
        start_date: 开始日期
        end_date: 结束日期
    """
    print("="*60)
    print(f"双均线策略回测: {symbol}")
    print(f"快线周期: {fast_period}, 慢线周期: {slow_period}")
    print(f"初始资金: {initial_capital:,.0f}")
    print("="*60)
    
    # 1. 获取数据
    df = load_stock_data(symbol, start_date, end_date)
    
    # 2. 创建策略
    strategy = DoubleMAStrategy(fast_period, slow_period)
    
    # 3. 手动模拟回测（简化版）
    print("\n交易记录:")
    print("-"*60)
    
    trades = []
    position = 0
    cash = initial_capital
    shares = 0
    fast_ma = aq.SMA(fast_period)
    slow_ma = aq.SMA(slow_period)
    
    for idx, row in df.iterrows():
        price = row['close']
        
        # 更新指标
        fast_ma.update(price)
        slow_ma.update(price)
        
        if idx < slow_period:  # 等待指标初始化
            continue
            
        fast_val = fast_ma.value
        slow_val = slow_ma.value
        
        # 买入信号
        if fast_val > slow_val and position == 0:
            shares = int(cash / price / 100) * 100  # 按手买入
            if shares > 0:
                cost = shares * price
                cash -= cost
                position = 1
                trades.append({
                    'type': 'BUY',
                    'date': row['timestamp'],
                    'price': price,
                    'shares': shares,
                    'cost': cost
                })
                print(f"[BUY]  {row['timestamp'].strftime('%Y-%m-%d')} @ {price:.2f} 数量:{shares}")
        
        # 卖出信号
        elif fast_val < slow_val and position == 1:
            revenue = shares * price
            cash += revenue
            trades.append({
                'type': 'SELL',
                'date': row['timestamp'],
                'price': price,
                'shares': shares,
                'revenue': revenue
            })
            print(f"[SELL] {row['timestamp'].strftime('%Y-%m-%d')} @ {price:.2f} 数量:{shares}")
            shares = 0
            position = 0
    
    # 最终市值
    final_value = cash + shares * df['close'].iloc[-1]
    total_return = (final_value - initial_capital) / initial_capital * 100
    
    print("-"*60)
    print(f"\n回测结果:")
    print(f"  初始资金: {initial_capital:,.0f}")
    print(f"  最终市值: {final_value:,.0f}")
    print(f"  总收益率: {total_return:+.2f}%")
    print(f"  交易次数: {len(trades)}")
    
    return {
        'symbol': symbol,
        'trades': trades,
        'initial_capital': initial_capital,
        'final_value': final_value,
        'return_pct': total_return,
        'data': df
    }


def main():
    """主函数"""
    import sys
    
    # 默认参数
    symbol = sys.argv[1] if len(sys.argv) > 1 else "000001"
    fast = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    slow = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    # 运行回测
    result = run_double_ma_backtest(
        symbol=symbol,
        fast_period=fast,
        slow_period=slow,
        initial_capital=100000,
        start_date="20240101",
        end_date="20241231"
    )
    
    return result


if __name__ == '__main__':
    main()
