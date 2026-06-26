#!/usr/bin/env python3
"""
BTC 10x 杠杆合约交易策略 V4.0 (优化持仓时间版)
- 止损: 4.5% (更宽松)
- 止盈: 8.0% (更宽松)
- 最小持仓: 4小时
- 移动止损: 3%
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import subprocess

class BTC10xStrategyV40:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = self.load_data_with_live_price()
        
        self.leverage = 10
        self.stop_loss_pct = 0.045     # 4.5% 止损（放宽）
        self.take_profit_pct = 0.08    # 8% 止盈（放宽）
        self.position_size = 0.20
        self.trailing_stop = 0.03      # 3% 移动止损（放宽）
        self.min_hold_hours = 4        # 最小持仓4小时
        
    def get_live_price(self):
        try:
            result = subprocess.run(
                ['okx', 'market', 'index-tickers', '--instId', 'BTC-USD'],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout
            if 'BTC-USD' in output:
                lines = output.split('\n')
                for line in lines:
                    if 'BTC-USD' in line:
                        parts = line.split()
                        for part in parts:
                            clean = part.replace(',', '').replace('$', '')
                            try:
                                return float(clean)
                            except:
                                continue
        except:
            pass
        return None
    
    def load_data_with_live_price(self):
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data, columns=['ts', 'open', 'high', 'low', 'close', 'confirm'])
        df['ts'] = df['ts'].astype(int)
        df['datetime'] = pd.to_datetime(df['ts'], unit='ms')
        df = df.sort_values('ts')
        for col in ['open', 'high', 'low', 'close']:
            df[col] = df[col].astype(float)
        
        live_price = self.get_live_price()
        if live_price:
            last_idx = df.index[-1]
            df.loc[last_idx, 'close'] = live_price
            if live_price > df.loc[last_idx, 'high']:
                df.loc[last_idx, 'high'] = live_price
            if live_price < df.loc[last_idx, 'low']:
                df.loc[last_idx, 'low'] = live_price
            print(f"📊 实时价格: ${live_price:,.0f}")
        
        return df
    
    def calculate_indicators(self):
        df = self.df.copy()
        df['ema3'] = df['close'].ewm(span=3, adjust=False).mean()
        df['ema8'] = df['close'].ewm(span=8, adjust=False).mean()
        df['ema13'] = df['close'].ewm(span=13, adjust=False).mean()
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=7).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=7).mean()
        df['rsi'] = 100 - (100 / (1 + gain / loss))
        df['momentum'] = df['close'].pct_change(2) * 100
        df['support'] = df['low'].rolling(10).min()
        df['resistance'] = df['high'].rolling(10).max()
        
        self.df = df
        return df
    
    def generate_signals(self):
        df = self.df.copy()
        
        df['signal_ema'] = 0
        df.loc[(df['ema3'] > df['ema8']) & (df['ema3'].shift(1) <= df['ema8'].shift(1)), 'signal_ema'] = 1
        df.loc[(df['ema3'] < df['ema8']) & (df['ema3'].shift(1) >= df['ema8'].shift(1)), 'signal_ema'] = -1
        
        df['signal_rsi'] = 0
        df.loc[df['rsi'] < 35, 'signal_rsi'] = 1
        df.loc[df['rsi'] > 65, 'signal_rsi'] = -1
        
        df['signal_momentum'] = 0
        df.loc[df['momentum'] > 1.5, 'signal_momentum'] = 1
        df.loc[df['momentum'] < -1.5, 'signal_momentum'] = -1
        
        df['signal_sr'] = 0
        df.loc[df['close'] > df['resistance'].shift(1) * 1.002, 'signal_sr'] = 1
        df.loc[df['close'] < df['support'].shift(1) * 0.998, 'signal_sr'] = -1
        
        df['signal_score'] = df['signal_ema'] * 2 + df['signal_rsi'] * 1 + df['signal_momentum'] * 1.5 + df['signal_sr'] * 1
        
        df['final_signal'] = 0
        df.loc[df['signal_score'] >= 1, 'final_signal'] = 1
        df.loc[df['signal_score'] <= -1, 'final_signal'] = -1
        
        df['signal_changed'] = df['final_signal'] != df['final_signal'].shift(1)
        df.loc[~df['signal_changed'], 'final_signal'] = 0
        
        self.df = df
        return df
    
    def backtest(self, initial_capital=1000):
        df = self.df.copy()
        capital = initial_capital
        position = 0
        entry_price = 0
        entry_time = None
        max_profit = 0
        trades = []
        
        for i in range(25, len(df)):
            current = df.iloc[i]
            signal = current['final_signal']
            
            if position != 0:
                price_change = (current['close'] - entry_price) / entry_price
                if position == -1:
                    price_change = -price_change
                pnl_pct = price_change * self.leverage
                
                if pnl_pct > max_profit:
                    max_profit = pnl_pct
                
                hold_time = current['datetime'] - entry_time
                hold_hours = hold_time.total_seconds() / 3600
                
                # 最小持仓时间检查
                if hold_hours < self.min_hold_hours:
                    # 不到最小持仓时间，不检查止盈止损
                    pass
                else:
                    # 止损
                    if pnl_pct <= -self.stop_loss_pct:
                        pnl = initial_capital * self.position_size * pnl_pct
                        capital += pnl
                        trades.append({'date': current['datetime'], 'action': 'STOP_LOSS',
                                      'pnl_pct': pnl_pct, 'hold_hours': hold_hours})
                        position = 0
                        max_profit = 0
                        continue
                    
                    # 止盈
                    if pnl_pct >= self.take_profit_pct:
                        pnl = initial_capital * self.position_size * pnl_pct
                        capital += pnl
                        trades.append({'date': current['datetime'], 'action': 'TAKE_PROFIT',
                                      'pnl_pct': pnl_pct, 'hold_hours': hold_hours})
                        position = 0
                        max_profit = 0
                        continue
                    
                    # 移动止损
                    if max_profit > 0.05 and pnl_pct <= max_profit - self.trailing_stop:
                        pnl = initial_capital * self.position_size * pnl_pct
                        capital += pnl
                        trades.append({'date': current['datetime'], 'action': 'TRAILING_STOP',
                                      'pnl_pct': pnl_pct, 'hold_hours': hold_hours})
                        position = 0
                        max_profit = 0
                        continue
                
                # 反向信号（不受最小持仓时间限制）
                if (position == 1 and signal == -1) or (position == -1 and signal == 1):
                    pnl = initial_capital * self.position_size * pnl_pct
                    capital += pnl
                    trades.append({'date': current['datetime'], 'action': 'REVERSE',
                                  'pnl_pct': pnl_pct, 'hold_hours': hold_hours})
                    position = 0
                    max_profit = 0
                    continue
            
            # 开新仓
            if position == 0 and signal != 0:
                position = signal
                entry_price = current['close']
                entry_time = current['datetime']
                max_profit = 0
                trades.append({'date': current['datetime'],
                              'action': 'OPEN_LONG' if position == 1 else 'OPEN_SHORT',
                              'price': entry_price})
        
        closed_trades = [t for t in trades if 'pnl_pct' in t]
        winning = len([t for t in closed_trades if t['pnl_pct'] > 0])
        losing = len([t for t in closed_trades if t['pnl_pct'] <= 0])
        
        avg_hold = np.mean([t['hold_hours'] for t in closed_trades if 'hold_hours' in t]) if closed_trades else 0
        
        return {
            'initial': initial_capital,
            'final': capital,
            'return': (capital - initial_capital) / initial_capital * 100,
            'trades': len(closed_trades),
            'winning': winning,
            'losing': losing,
            'win_rate': winning / len(closed_trades) * 100 if closed_trades else 0,
            'avg_hold_hours': avg_hold,
            'trade_list': trades
        }
    
    def run(self):
        print("=" * 100)
        print("BTC 10x 杠杆策略 V4.0 (优化持仓时间版)")
        print("=" * 100)
        print(f"   止损: {self.stop_loss_pct*100}% | 止盈: {self.take_profit_pct*100}% | 最小持仓: {self.min_hold_hours}h")
        
        self.calculate_indicators()
        self.generate_signals()
        
        result = self.backtest()
        
        print(f"\n💰 回测结果:")
        print(f"   初始: ${result['initial']:,.2f} → 最终: ${result['final']:,.2f}")
        print(f"   收益率: {result['return']:+.2f}%")
        print(f"   交易: {result['trades']}次 (胜{result['winning']}/负{result['losing']})")
        print(f"   胜率: {result['win_rate']:.1f}%")
        print(f"   平均持仓: {result['avg_hold_hours']:.1f}小时")
        
        if result['trades'] > 0:
            print(f"\n📋 最近10笔:")
            for t in result['trade_list'][-10:]:
                if 'pnl_pct' in t:
                    print(f"   {t['date'].strftime('%m-%d %H:%M')}: {t['action']:12} {t['pnl_pct']*100:+.1f}% ({t['hold_hours']:.1f}h)")
                else:
                    print(f"   {t['date'].strftime('%m-%d %H:%M')}: {t['action']:12} @ ${t['price']:,.0f}")
        
        latest = self.df.iloc[-1]
        signal_text = '🟢 开多' if latest['final_signal']==1 else '🔴 开空' if latest['final_signal']==-1 else '⚪ 观望'
        print(f"\n🎯 当前: {signal_text} @ ${latest['close']:,.0f}")
        
        if latest['final_signal'] != 0:
            entry = latest['close']
            if latest['final_signal'] == 1:
                stop = entry * (1 - self.stop_loss_pct / self.leverage)
                tp = entry * (1 + self.take_profit_pct / self.leverage)
            else:
                stop = entry * (1 + self.stop_loss_pct / self.leverage)
                tp = entry * (1 - self.take_profit_pct / self.leverage)
            print(f"   止损: ${stop:,.0f} | 止盈: ${tp:,.0f}")
            print(f"   最小持仓: {self.min_hold_hours}小时")
        
        print("=" * 100)
        return result

if __name__ == "__main__":
    DATA_FILE = os.path.expanduser("~/.okx_data/historical/btc_4h_recent.json")
    os.system('okx market index-candles BTC-USD --bar 4H --limit 100 --history --json > ~/.okx_data/historical/btc_4h_recent.json 2>/dev/null')
    
    strategy = BTC10xStrategyV40(DATA_FILE)
    result = strategy.run()
