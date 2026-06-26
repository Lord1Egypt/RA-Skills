#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股量化回测脚本 - 龙头低吸模式
==============================
策略逻辑：
1. 选龙头：近5日有涨停，且累计涨幅>20%
2. 等回调：股价回踩10日均线附近企稳（收盘价 >= 10日均线 * 0.98）
3. 买入：次日开盘买入
4. 卖出：+5%卖1/3，+8%卖1/3，破10日均线或+10%以上清仓，-5%止损
5. 持仓：最多3天

月目标：5-10%收益
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

try:
    import akshare as ak
    import pandas as pd
    import numpy as np
except ImportError:
    print("请先安装依赖：pip install akshare pandas numpy")
    sys.exit(1)


class DragonLowPickBacktest:
    """龙头低吸回测引擎"""
    
    def __init__(self, initial_capital: float = 50000, output_dir: str = "miaoxiang/backtest"):
        self.initial_capital = initial_capital
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 策略参数
        self.max_positions = 2          # 最多持仓2只
        self.max_holding_days = 3        # 最多持3天
        self.stop_loss = -0.05          # -5%止损
        self.take_profit_1 = 0.05        # +5%卖1/3
        self.take_profit_2 = 0.08        # +8%再卖1/3
        self.take_profit_3 = 0.10        # +10%以上清仓
        self.pullback_ratio = 0.98       # 回踩10日均线系数（收盘价 >= MA10 * 0.98）
        
        # 持仓数据结构: {symbol: {"shares": x, "cost": y, "buy_price": z, "buy_date": t, "days": n, "high_since_buy": h}}
        self.positions = {}
        self.cash = initial_capital
        self.trades = []
        self.daily_values = []
        
        # 龙头池缓存（避免重复计算）
        self.dragon_pool_cache = {}  # {date: [symbols]}
        
    def get_stock_daily(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取个股历史K线"""
        try:
            df = ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date, adjust="qfq")
            
            if len(df.columns) == 12:
                df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 
                              'amplitude', 'pct_change', 'change', 'turnover', 'pre_close']
            else:
                df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 
                              'amplitude', 'pct_change', 'change', 'turnover']
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            df['code'] = symbol
            
            # 计算均线
            df['ma5'] = df['close'].rolling(5).mean()
            df['ma10'] = df['close'].rolling(10).mean()
            df['ma20'] = df['close'].rolling(20).mean()
            
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def get_index_daily(self, symbol: str = "000300", start_date: str = "20240101") -> pd.DataFrame:
        """获取指数数据（大盘择时用）"""
        try:
            df = ak.stock_zh_index_daily(symbol=f"sh{symbol}")
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_date)].sort_values('date').reset_index(drop=True)
            df['ma20'] = df['close'].rolling(20).mean()
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def find_limit_up_stocks(self, date: str, lookback_days: int = 5) -> List[str]:
        """找出近N日有涨停的股票"""
        if date in self.dragon_pool_cache:
            return self.dragon_pool_cache[date]
        
        date_int = date.replace("-", "")
        result = []
        
        try:
            # 获取当日涨停股
            df_today = ak.stock_zh_a_spot_em()
            if not df_today.empty and '涨跌幅' in df_today.columns:
                limit_up = df_today[df_today['涨跌幅'] >= 9.5]
                if not limit_up.empty and '代码' in limit_up.columns:
                    result = limit_up['代码'].head(50).tolist()
        except Exception as e:
            print(f"获取涨停股失败: {e}")
        
        self.dragon_pool_cache[date] = result
        return result
    
    def check_is_dragon(self, df: pd.DataFrame, idx: int, lookback: int = 5) -> bool:
        """检查是否为龙头：近N日有涨停，且累计涨幅>20%"""
        if idx < lookback:
            return False
        
        recent = df.iloc[idx-lookback:idx+1]
        
        # 有涨停
        has_limit = (recent['pct_change'] >= 9.5).any()
        if not has_limit:
            return False
        
        # 累计涨幅>20%
        start_price = df.iloc[idx-lookback]['close']
        end_price = df.iloc[idx]['close']
        total_pct = (end_price - start_price) / start_price
        
        return total_pct > 0.20
    
    def check_pullback_to_ma10(self, df: pd.DataFrame, idx: int) -> bool:
        """检查是否回踩10日均线企稳"""
        if idx < 10 or pd.isna(df.iloc[idx]['ma10']):
            return False
        
        current_price = df.iloc[idx]['close']
        ma10 = df.iloc[idx]['ma10']
        
        # 收盘价在10日均线上方附近（允许2%以内）
        return current_price >= ma10 * self.pullback_ratio
    
    def find_buy_signals(self, date: str, stock_pool: List[str]) -> List[Dict]:
        """找出符合买入条件的股票"""
        signals = []
        date_int = date.replace("-", "")
        
        # 简化：直接用近期热门龙头股
        # 实际应该从涨停板中筛选
        popular_stocks = [
            "300750", "300308", "002594", "300274", "688981",  # 新能源车、光伏、半导体、AI
            "600519", "000858", "600036",  # 消费、金融
            "300059", "688111", "300454", "688008",  # 科技
            "002812", "002460", "002192", "002466",  # 锂电
            "600438", "002129", "300118",  # 光伏
            "688408", "688126", "688232",  # 半导体
            "688185", "688317", "300363",  # 医药
            "000807", "600111", "002340",  # 有色
            "688041", "688068", "301029", "301308", "301378"  # 次新/热门
        ]
        
        check_pool = stock_pool if stock_pool else popular_stocks
        
        for symbol in check_pool[:30]:
            df = self.get_stock_daily(symbol, "20240101", date_int)
            if df.empty or len(df) < 20:
                continue
            
            idx = len(df) - 1
            
            # 龙头条件：近5日有涨停且累计>20%
            is_dragon = self.check_is_dragon(df, idx, 5)
            if not is_dragon:
                continue
            
            # 回踩10日均线企稳
            is_pullback = self.check_pullback_to_ma10(df, idx)
            if not is_pullback:
                continue
            
            # 成交量放大
            vol_ma5 = df.iloc[idx-4:idx+1]['volume'].mean()
            if df.iloc[idx]['volume'] < vol_ma5 * 0.8:  # 缩量回调更好
                continue
            
            signals.append({
                'code': symbol,
                'close': df.iloc[idx]['close'],
                'pct_5d': (df.iloc[idx]['close'] - df.iloc[idx-5]['close']) / df.iloc[idx-5]['close'] * 100,
                'ma10': df.iloc[idx]['ma10'],
                'volume_ratio': df.iloc[idx]['volume'] / vol_ma5
            })
        
        # 按5日涨幅排序，取最强的
        signals.sort(key=lambda x: x['pct_5d'], reverse=True)
        return signals[:3]
    
    def buy_stock(self, symbol: str, price: float, date: str):
        """买入股票"""
        if len(self.positions) >= self.max_positions or self.cash < 5000:
            return False
        
        # 每只股票投入一半仓位
        amount = self.cash / 2
        amount = min(amount, self.cash * 0.6)  # 单票不超60%
        
        shares = int(amount / price / 100) * 100
        if shares < 100:
            return False
        
        cost = shares * price
        self.cash -= cost
        
        self.positions[symbol] = {
            'shares': shares,
            'cost': cost,
            'buy_price': price,
            'buy_date': date,
            'days': 0,
            'high_since_buy': price
        }
        
        self.trades.append({
            'date': date,
            'action': 'BUY',
            'symbol': symbol,
            'price': price,
            'shares': shares,
            'amount': cost
        })
        return True
    
    def sell_stock(self, symbol: str, price: float, date: str, reason: str):
        """卖出股票（清仓）"""
        if symbol not in self.positions:
            return
        
        pos = self.positions[symbol]
        shares = pos['shares']
        amount = shares * price
        profit_pct = (price - pos['buy_price']) / pos['buy_price'] * 100
        
        self.cash += amount
        self.trades.append({
            'date': date,
            'action': 'SELL',
            'symbol': symbol,
            'price': price,
            'shares': shares,
            'amount': amount,
            'profit_pct': profit_pct,
            'reason': reason,
            'holding_days': pos['days']
        })
        
        del self.positions[symbol]
    
    def sell_part(self, symbol: str, price: float, date: str, shares: int, reason: str):
        """卖出部分仓位"""
        if symbol not in self.positions:
            return
        
        pos = self.positions[symbol]
        amount = shares * price
        profit_pct = (price - pos['buy_price']) / pos['buy_price'] * 100
        
        self.cash += amount
        pos['shares'] -= shares
        
        self.trades.append({
            'date': date,
            'action': 'SELL_PART',
            'symbol': symbol,
            'price': price,
            'shares': shares,
            'amount': amount,
            'profit_pct': profit_pct,
            'reason': reason
        })
    
    def check_positions(self, df: pd.DataFrame, date: str):
        """检查持仓，处理止盈止损"""
        if not self.positions:
            return
        
        idx = len(df) - 1
        if idx < 0:
            return
        
        symbol = df.iloc[0]['code']
        if symbol not in self.positions:
            return
        
        current_price = df.iloc[idx]['close']
        ma10 = df.iloc[idx]['ma10']
        
        pos = self.positions[symbol]
        pos['days'] += 1
        pos['high_since_buy'] = max(pos['high_since_buy'], current_price)
        
        profit_pct = (current_price - pos['buy_price']) / pos['buy_price']
        
        # 止盈止损逻辑
        # 1. 破10日均线，清仓
        if not pd.isna(ma10) and current_price < ma10:
            self.sell_stock(symbol, current_price, date, f"破10日均线 ({current_price:.2f}<{ma10:.2f})")
            return
        
        # 2. +10%以上或不涨停，尾盘清仓（简化：收盘价>最高价-2%即持有）
        if profit_pct >= self.take_profit_3:
            # 检查是否涨停（简化：收盘价>=开盘价*1.09）
            open_price = df.iloc[idx]['open']
            is_limit_up = current_price >= open_price * 1.095
            if not is_limit_up:
                self.sell_stock(symbol, current_price, date, f"+10%以上不涨停清仓 ({profit_pct*100:.1f}%)")
                return
        
        # 3. +8%，卖2/3
        if profit_pct >= self.take_profit_2 and pos['shares'] >= 300:
            shares_to_sell = pos['shares'] // 3 * 2
            if shares_to_sell >= 100:
                self.sell_part(symbol, current_price, date, shares_to_sell, f"+8%卖2/3 ({profit_pct*100:.1f}%)")
        
        # 4. +5%，卖1/3
        elif profit_pct >= self.take_profit_1 and pos['shares'] >= 200:
            shares_to_sell = pos['shares'] // 3
            if shares_to_sell >= 100:
                self.sell_part(symbol, current_price, date, shares_to_sell, f"+5%卖1/3 ({profit_pct*100:.1f}%)")
        
        # 5. -5%止损
        elif profit_pct <= self.stop_loss:
            self.sell_stock(symbol, current_price, date, f"-5%止损 ({profit_pct*100:.1f}%)")
            return
        
        # 6. 持仓满3天
        elif pos['days'] >= self.max_holding_days:
            self.sell_stock(symbol, current_price, date, f"持仓满3天 ({profit_pct*100:.1f}%)")
    
    def is_market_good(self, index_df: pd.DataFrame, date: str) -> bool:
        """大盘择时：沪深300站上20日均线"""
        if index_df.empty:
            return True  # 没有数据默认做多
        
        idx_list = index_df[index_df['date'] <= date]
        if idx_list.empty:
            return True
        
        latest = idx_list.iloc[-1]
        if pd.isna(latest.get('ma20')):
            return True
        
        return latest['close'] >= latest['ma20']
    
    def run(self, start_date: str = "20240101", end_date: str = None, stock_pool: list = None):
        """运行回测"""
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        
        # 获取交易日历
        trading_dates = pd.bdate_range(start=start_date, end=end_date)
        
        # 获取沪深300数据用于择时
        index_df = self.get_index_daily("000300", start_date)
        
        print(f"=== 龙头低吸策略回测 ===")
        print(f"起始资金: {self.initial_capital:,.0f}")
        print(f"回测期间: {start_date} ~ {end_date}")
        print(f"止损: {self.stop_loss*100}% | 止盈: {self.take_profit_1*100}%, {self.take_profit_2*100}%, {self.take_profit_3*100}%")
        print(f"========================\n")
        
        # 模拟每日行情
        for i, date in enumerate(trading_dates[20:]):  # 跳过前20天（等数据）
            date_str = date.strftime("%Y-%m-%d")
            date_int = date.strftime("%Y%m%d")
            
            # 更新每日持仓净值
            total_value = self.cash
            for symbol, pos in self.positions.items():
                df = self.get_stock_daily(symbol, start_date, date_int)
                if not df.empty:
                    current_val = pos['shares'] * df.iloc[-1]['close']
                    total_value += current_val
            
            self.daily_values.append({
                'date': date_str,
                'cash': round(self.cash, 2),
                'positions_value': round(total_value - self.cash, 2),
                'total_value': round(total_value, 2),
                'profit_pct': round((total_value - self.initial_capital) / self.initial_capital * 100, 2)
            })
            
            # 大盘择时：沪深300需站上20日均线
            market_good = self.is_market_good(index_df, date_str)
            if not market_good:
                # 大盘不好，清仓所有持仓
                for symbol in list(self.positions.keys()):
                    df = self.get_stock_daily(symbol, start_date, date_int)
                    if not df.empty:
                        self.sell_stock(symbol, df.iloc[-1]['close'], date_str, "大盘破位清仓")
                continue
            
            # 选股买入（每3个交易日检查一次）
            if i % 3 == 0 and len(self.positions) < self.max_positions:
                signals = self.find_buy_signals(date_str, stock_pool)
                for stock in signals:
                    if len(self.positions) >= self.max_positions:
                        break
                    # 模拟开盘价=收盘价*1.01（略高开）
                    buy_price = stock['close'] * 1.01
                    self.buy_stock(stock['code'], buy_price, date_str)
            
            # 检查持仓
            for symbol in list(self.positions.keys()):
                df = self.get_stock_daily(symbol, start_date, date_int)
                if not df.empty:
                    self.check_positions(df, date_str)
        
        # 输出结果
        self.save_results()
        self.print_summary()
    
    def save_results(self):
        """保存结果"""
        df_daily = pd.DataFrame(self.daily_values)
        csv_path = self.output_dir / "dragon_lowpick_daily.csv"
        df_daily.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        df_trades = pd.DataFrame(self.trades)
        trades_path = self.output_dir / "dragon_lowpick_trades.csv"
        df_trades.to_csv(trades_path, index=False, encoding='utf-8-sig')
        
        print(f"\n结果已保存:")
        print(f"- {csv_path}")
        print(f"- {trades_path}")
    
    def print_summary(self):
        """打印回测摘要"""
        if not self.daily_values:
            print("无回测数据")
            return
        
        df = pd.DataFrame(self.daily_values)
        final_value = df.iloc[-1]['total_value']
        total_return = (final_value - self.initial_capital) / self.initial_capital * 100
        
        # 计算年化收益
        days = len(df)
        annual_return = ((1 + total_return/100) ** (250/days) - 1) * 100 if days > 0 else 0
        
        # 最大回撤
        df['peak'] = df['total_value'].cummax()
        df['drawdown'] = (df['total_value'] - df['peak']) / df['peak'] * 100
        max_drawdown = df['drawdown'].min()
        
        # 胜率统计
        df_trades = pd.DataFrame(self.trades)
        sell_trades = df_trades[df_trades['action'].isin(['SELL', 'SELL_PART'])] if not df_trades.empty else pd.DataFrame()
        
        wins = 0
        total_sells = 0
        win_rate = 0
        avg_win = 0
        avg_loss = 0
        
        if not sell_trades.empty and 'profit_pct' in sell_trades.columns:
            wins = len(sell_trades[sell_trades['profit_pct'] > 0])
            total_sells = len(sell_trades)
            win_rate = wins / total_sells * 100 if total_sells > 0 else 0
            
            wins_df = sell_trades[sell_trades['profit_pct'] > 0]
            loss_df = sell_trades[sell_trades['profit_pct'] <= 0]
            avg_win = wins_df['profit_pct'].mean() if not wins_df.empty else 0
            avg_loss = loss_df['profit_pct'].mean() if not loss_df.empty else 0
        
        print(f"\n{'='*35}")
        print(f"         龙头低吸策略回测结果")
        print(f"{'='*35}")
        print(f"  初始资金:      {self.initial_capital:>12,.0f}")
        print(f"  最终净值:      {final_value:>12,.0f}")
        print(f"  总收益率:      {total_return:>+10.2f}%")
        print(f"  年化收益率:    {annual_return:>+10.2f}%")
        print(f"  最大回撤:      {max_drawdown:>10.2f}%")
        print(f"  交易次数:      {len(df_trades):>10}")
        print(f"  卖出次数:      {total_sells:>10}")
        print(f"  胜率:          {win_rate:>10.1f}%")
        print(f"  平均盈利:      {avg_win:>+10.2f}%")
        print(f"  平均亏损:      {avg_loss:>10.2f}%")
        print(f"{'='*35}")
        
        # 按月统计
        if not df.empty:
            df['month'] = df['date'].str[:7]
            monthly = df.groupby('month').last()[['total_value', 'profit_pct']]
            print(f"\n月度收益:")
            for month, row in monthly.iterrows():
                print(f"  {month}: {row['profit_pct']:+.2f}%")


def main():
    parser = argparse.ArgumentParser(description="龙头低吸策略回测")
    parser.add_argument("--capital", type=float, default=50000, help="初始资金")
    parser.add_argument("--start", type=str, default="20240101", help="开始日期")
    parser.add_argument("--end", type=str, help="结束日期")
    parser.add_argument("--output", type=str, default="miaoxiang/backtest", help="输出目录")
    parser.add_argument("--query", type=str, help="自然语言参数")
    
    args = parser.parse_args()
    
    engine = DragonLowPickBacktest(initial_capital=args.capital, output_dir=args.output)
    engine.run(start_date=args.start, end_date=args.end)


if __name__ == "__main__":
    main()