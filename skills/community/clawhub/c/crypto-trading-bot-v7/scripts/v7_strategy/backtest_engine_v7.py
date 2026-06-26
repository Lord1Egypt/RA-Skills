"""
完整交易策略 - 小时级别 · 多策略组合 · 动态风控 v7
基于 新短线引擎方案.txt

支持：日线定方向、4小时定区间、1小时主信号
包含：趋势策略(Supertrend+ADX)、震荡策略(布林带+RSI+网格)
风控：动态ATR止损、波动率过滤、杠杆管理、盈利提现
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ========== 配置 ==========
DATA_PATH = '/home/user/.openclaw/workspace/crypto_data/SOLUSDT_1h.csv'
INITIAL_CAPITAL = 1000
COMMISSION = 0.0002  # 0.02%

# ========== 1. 数据加载 ==========
def load_data(filepath):
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.sort_values('timestamp').reset_index(drop=True)
    for c in ['open', 'high', 'low', 'close', 'volume']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

# ========== 2. 技术指标 ==========
def compute_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = np.abs(high - close.shift(1))
    tr3 = np.abs(low - close.shift(1))
    tr = np.maximum(np.maximum(tr1, tr2), tr3)
    return tr.rolling(period).mean()

def compute_adx(high, low, close, period=14):
    up = high.diff()
    down = -low.diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    atr = compute_atr(high, low, close, period)
    plus_di = 100 * plus_dm.rolling(period).mean() / atr
    minus_di = 100 * minus_dm.rolling(period).mean() / atr
    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
    return dx.rolling(period).mean()

def compute_bollinger(close, period=20, std=2.0):
    ma = close.rolling(period).mean()
    stddev = close.rolling(period).std()
    upper = ma + std * stddev
    lower = ma - std * stddev
    return ma, upper, lower

def compute_rsi(close, period=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def compute_supertrend(high, low, close, period=20, multiplier=3.5):
    atr = compute_atr(high, low, close, period)
    hl_avg = (high + low) / 2
    upper_band = hl_avg + multiplier * atr
    lower_band = hl_avg - multiplier * atr
    
    trend = np.zeros(len(close))
    st_val = np.zeros(len(close))
    
    for i in range(period, len(close)):
        if i == period:
            st_val[i] = upper_band.iloc[i]
            trend[i] = 1 if close.iloc[i] > st_val[i] else -1
        else:
            c = close.iloc[i]
            if c > upper_band.iloc[i-1]:
                trend[i] = 1
            elif c < lower_band.iloc[i-1]:
                trend[i] = -1
            else:
                trend[i] = trend[i-1]
            
            if trend[i] == 1:
                st_val[i] = lower_band.iloc[i] if trend[i-1] == -1 else max(lower_band.iloc[i], st_val[i-1])
            else:
                st_val[i] = upper_band.iloc[i] if trend[i-1] == 1 else min(upper_band.iloc[i], st_val[i-1])
    
    return trend

def compute_ma(close, period):
    return close.rolling(period).mean()

# ========== 3. 市场状态检测 ==========
def detect_market_state(daily_df, h4_df, current_atr, atr_history):
    """检测市场状态：趋势/震荡，高波动/正常"""
    if len(daily_df) < 50:
        return {'is_trending': False, 'is_high_vol': False, 'adx_daily': 0, 'atr_percentile': 0}
    
    # 日线ADX
    adx_daily = compute_adx(daily_df['high'], daily_df['low'], daily_df['close']).iloc[-1]
    if pd.isna(adx_daily):
        adx_daily = 0
    
    # 日线200MA方向
    ma200 = compute_ma(daily_df['close'], 200).iloc[-1]
    price_daily = daily_df['close'].iloc[-1]
    daily_trend = 'bullish' if price_daily > ma200 else 'bearish'
    
    # 4小时ADX
    if len(h4_df) >= 30:
        adx_4h = compute_adx(h4_df['high'], h4_df['low'], h4_df['close']).iloc[-1]
        if pd.isna(adx_4h):
            adx_4h = 0
    else:
        adx_4h = 0
    
    # ATR百分位
    atr_history.append(current_atr)
    if len(atr_history) > 200:
        atr_history.pop(0)
    
    if len(atr_history) >= 100:
        atr_percentile = np.sum(np.array(atr_history) < current_atr) / len(atr_history) * 100
    else:
        atr_percentile = 0
    
    is_trending = adx_daily > 25 or adx_4h > 25
    is_high_vol = atr_percentile > 90
    
    return {
        'is_trending': is_trending,
        'is_high_vol': is_high_vol,
        'adx_daily': adx_daily,
        'atr_percentile': atr_percentile,
        'daily_trend': daily_trend
    }

# ========== 4. 策略信号 ==========
def trend_signal(high, low, close, market_state, period=20, mult=3.5):
    """趋势策略: Supertrend + ADX过滤"""
    if market_state['is_high_vol']:
        return 0
    if market_state['adx_daily'] < 20:  # ADX门槛
        return 0
    
    trend = compute_supertrend(high, low, close, period, mult)
    return int(trend[-1])

def oscillator_signal(high, low, close, market_state, bb_period=20, bb_std=2.0, rsi_period=14):
    """震荡策略: 布林带 + RSI"""
    if market_state['is_high_vol']:
        return 0
    if market_state['adx_daily'] > 25:  # 震荡市ADX应低
        return 0
    
    _, upper, lower = compute_bollinger(close, bb_period, bb_std)
    rsi = compute_rsi(close, rsi_period)
    
    current_close = close.iloc[-1]
    current_lower = lower.iloc[-1]
    current_upper = upper.iloc[-1]
    current_rsi = rsi.iloc[-1]
    
    # 买入信号: 价格在下轨且RSI超卖
    if current_close <= current_lower and current_rsi < 35:
        return 1
    # 卖出信号: 价格在上轨且RSI超买
    elif current_close >= current_upper and current_rsi > 65:
        return -1
    return 0

# ========== 5. 风控与仓位 ==========
class RiskManager:
    def __init__(self, initial_equity, risk_pct=0.015, leverage=4, max_daily_loss=0.05, max_trades_per_day=8):
        self.initial_equity = initial_equity
        self.risk_pct = risk_pct
        self.leverage = leverage
        self.max_daily_loss = max_daily_loss
        self.max_trades_per_day = max_trades_per_day
        self.daily_loss = 0
        self.daily_trades = 0
        self.current_date = None
    
    def update_daily(self, date, equity):
        if self.current_date != date:
            self.current_loss = max(0, self.initial_equity - equity) if equity < self.initial_equity else 0
            self.daily_trades = 0
            self.current_date = date
    
    def can_trade(self):
        if self.current_loss > self.initial_equity * self.max_daily_loss:
            return False
        if self.daily_trades >= self.max_trades_per_day:
            return False
        return True
    
    def calc_position(self, equity, entry_price, stop_distance):
        risk_amount = equity * self.risk_pct
        pos = risk_amount / stop_distance if stop_distance > 0 else 0
        max_notional = equity * self.leverage
        max_pos = max_notional / entry_price
        return min(pos, max_pos)
    
    def get_stop(self, entry_price, direction, atr, trailing=False, highest=None, lowest=None):
        stop_dist = atr * 1.5
        if direction == 1:
            stop = entry_price - stop_dist
            if trailing and highest is not None:
                if highest - entry_price > atr * 2:
                    stop = max(stop, highest - stop_dist)
        else:
            stop = entry_price + stop_dist
            if trailing and lowest is not None:
                if entry_price - lowest > atr * 2:
                    stop = min(stop, lowest + stop_dist)
        return stop

# ========== 6. 回测引擎 ==========
def run_backtest():
    print('='*60)
    print('新短线引擎 v7 - SOL回测')
    print('='*60)
    
    # 加载数据
    df = load_data(DATA_PATH)
    df = df[df['timestamp'] >= '2025-09-01'].copy()
    df = df[df['timestamp'] <= '2026-03-26'].copy()
    df = df.reset_index(drop=True)
    n = len(df)
    print(f'数据: {n}条K线, {df["timestamp"].iloc[0]} -> {df["timestamp"].iloc[-1]}')
    
    # 计算1h指标
    df['atr'] = compute_atr(df['high'], df['low'], df['close'])
    df['adx'] = compute_adx(df['high'], df['low'], df['close'])
    ma, df['bb_upper'], df['bb_lower'] = compute_bollinger(df['close'])
    df['bb_ma'] = ma
    df['rsi'] = compute_rsi(df['close'])
    df['trend'] = compute_supertrend(df['high'], df['low'], df['close'])
    
    # 准备日线和4H数据
    df_daily = df.set_index('timestamp').resample('D').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna()
    df_h4 = df.set_index('timestamp').resample('4h').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna()
    
    print(f'日线: {len(df_daily)}条, 4H: {len(df_h4)}条')
    
    # 初始化
    equity = INITIAL_CAPITAL
    pos = 0
    entry_price = 0
    entry_size = 0
    stop_loss = 0
    highest_price = 0
    lowest_price = 0
    avg_entry = 0
    grid_count = 0
    direction = 0
    trades = []
    equity_curve = []
    atr_history = []
    
    risk_mgr = RiskManager(INITIAL_CAPITAL, risk_pct=0.015, leverage=4)
    
    print('\n开始回测...')
    print('-'*60)
    
    for i in range(30, n):
        date = df['timestamp'].iloc[i].date()
        price = df['close'].iloc[i]
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        atr = df['atr'].iloc[i] if pd.notna(df['atr'].iloc[i]) else price * 0.01
        
        # 更新风控日
        risk_mgr.update_daily(date, equity)
        
        # 市场状态
        daily_slice = df_daily[df_daily.index <= df['timestamp'].iloc[i]]
        h4_slice = df_h4[df_h4.index <= df['timestamp'].iloc[i]]
        market = detect_market_state(daily_slice, h4_slice, atr, atr_history)
        
        # 生成信号
        if pos == 0 and risk_mgr.can_trade():
            if market['is_trending']:
                sig = trend_signal(df['high'].iloc[:i+1], df['low'].iloc[:i+1], df['close'].iloc[:i+1], market)
            else:
                sig = oscillator_signal(df['high'].iloc[:i+1], df['low'].iloc[:i+1], df['close'].iloc[:i+1], market)
        else:
            sig = 0
        
        # 更新极值
        if pos != 0:
            highest_price = max(highest_price, high)
            lowest_price = min(lowest_price, low)
        
        # ========== 平仓检查 ==========
        exit_price = 0
        exit_signal = False
        
        if pos != 0:
            # 止损
            if direction == 1 and price <= stop_loss:
                exit_signal = True
                exit_price = stop_loss
            elif direction == -1 and price >= stop_loss:
                exit_signal = True
                exit_price = stop_loss
            
            # 移动止损
            if not exit_signal and pos != 0:
                new_stop = risk_mgr.get_stop(avg_entry, direction, atr, trailing=True, 
                                             highest=highest_price, lowest=lowest_price)
                if direction == 1 and new_stop > stop_loss:
                    stop_loss = new_stop
                elif direction == -1 and new_stop < stop_loss:
                    stop_loss = new_stop
            
            # 震荡策略分批止盈
            if not exit_signal and not market['is_trending'] and market['adx_daily'] <= 25:
                bb_mid = df['bb_ma'].iloc[i] if pd.notna(df['bb_ma'].iloc[i]) else price
                bb_upper = df['bb_upper'].iloc[i] if pd.notna(df['bb_upper'].iloc[i]) else price * 1.02
                bb_lower = df['bb_lower'].iloc[i] if pd.notna(df['bb_lower'].iloc[i]) else price * 0.98
                
                if direction == 1:
                    if price >= bb_mid:
                        # 平半仓
                        half_size = entry_size / 2
                        pnl = (price - avg_entry) * half_size
                        equity += pnl - price * half_size * COMMISSION
                        entry_size -= half_size
                        trades.append({'type': 'PARTIAL', 'pnl': pnl, 'price': price})
                    
                    if price >= bb_upper:
                        exit_signal = True
                        exit_price = price
                else:
                    if price <= bb_mid:
                        half_size = entry_size / 2
                        pnl = (avg_entry - price) * half_size
                        equity += pnl - price * half_size * COMMISSION
                        entry_size -= half_size
                        trades.append({'type': 'PARTIAL', 'pnl': pnl, 'price': price})
                    
                    if price <= bb_lower:
                        exit_signal = True
                        exit_price = price
            
            # 趋势策略信号反转
            if not exit_signal and market['is_trending']:
                if market['adx_daily'] >= 20:
                    current_trend = df['trend'].iloc[i] if pd.notna(df['trend'].iloc[i]) else 0
                    if direction == 1 and current_trend == -1:
                        exit_signal = True
                        exit_price = price
                    elif direction == -1 and current_trend == 1:
                        exit_signal = True
                        exit_price = price
            
            # 执行平仓
            if exit_signal:
                if entry_size > 0:
                    if direction == 1:
                        pnl = (exit_price - avg_entry) * entry_size
                    else:
                        pnl = (avg_entry - exit_price) * entry_size
                    equity += pnl - exit_price * entry_size * COMMISSION
                    trades.append({'type': 'CLOSE', 'pnl': pnl, 'price': exit_price, 'direction': direction})
                pos = 0
                entry_size = 0
                entry_price = 0
                avg_entry = 0
                stop_loss = 0
                highest_price = 0
                lowest_price = 0
                grid_count = 0
                direction = 0
                risk_mgr.daily_trades += 1
        
        # ========== 开仓 ==========
        if pos == 0 and sig != 0 and risk_mgr.can_trade():
            direction = sig
            entry_price = price
            stop_loss = risk_mgr.get_stop(price, direction, atr)
            stop_dist = abs(price - stop_loss)
            entry_size = risk_mgr.calc_position(equity, price, stop_dist)
            
            if entry_size > 0:
                equity -= price * entry_size * COMMISSION  # 扣手续费
                avg_entry = price
                highest_price = high
                lowest_price = low
                pos = 1
                grid_count = 0
                trades.append({'type': 'ENTRY', 'direction': direction, 'price': price, 'size': entry_size})
        
        # ========== 网格加仓(震荡策略) ==========
        if pos == 1 and not market['is_trending'] and grid_count < 3:
            if direction == 1:
                drop_pct = (avg_entry - price) / avg_entry
                if drop_pct >= 0.02:
                    add_size = entry_size * 0.5
                    add_cost = price * add_size * COMMISSION
                    equity -= add_cost
                    total_size = entry_size + add_size
                    avg_entry = (avg_entry * entry_size + price * add_size) / total_size
                    entry_size = total_size
                    stop_loss = avg_entry - atr * 1.5
                    grid_count += 1
                    trades.append({'type': 'GRID_ADD', 'price': price, 'size': add_size, 'grid_count': grid_count})
            else:
                rise_pct = (price - avg_entry) / avg_entry
                if rise_pct >= 0.02:
                    add_size = entry_size * 0.5
                    add_cost = price * add_size * COMMISSION
                    equity -= add_cost
                    total_size = entry_size + add_size
                    avg_entry = (avg_entry * entry_size + price * add_size) / total_size
                    entry_size = total_size
                    stop_loss = avg_entry + atr * 1.5
                    grid_count += 1
                    trades.append({'type': 'GRID_ADD', 'price': price, 'size': add_size, 'grid_count': grid_count})
        
        # 记录权益
        if pos == 1:
            if direction == 1:
                unrealized = (price - avg_entry) * entry_size
            else:
                unrealized = (avg_entry - price) * entry_size
            current_equity = equity + unrealized
        else:
            current_equity = equity
        
        if i % 200 == 0:
            equity_curve.append({'time': df['timestamp'].iloc[i], 'equity': current_equity, 'pos': pos})
    
    # ========== 结果统计 ==========
    closed_trades = [t for t in trades if t['type'] in ['CLOSE', 'ENTRY'] and 'pnl' in t]
    wins = [t for t in closed_trades if t.get('pnl', 0) > 0]
    win_rate = len(wins) / len(closed_trades) * 100 if closed_trades else 0
    
    total_pnl = sum(t.get('pnl', 0) for t in closed_trades)
    total_fees = sum(t.get('price', 0) * t.get('size', 0) * COMMISSION for t in trades if t['type'] in ['ENTRY', 'GRID_ADD', 'CLOSE'])
    
    net_return = (equity - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100
    
    # 计算最大回撤
    eq_df = pd.DataFrame(equity_curve)
    if len(eq_df) > 0:
        eq_df['peak'] = eq_df['equity'].cummax()
        eq_df['drawdown'] = (eq_df['equity'] - eq_df['peak']) / eq_df['peak'] * 100
        max_dd = eq_df['drawdown'].min()
    else:
        max_dd = 0
    
    grid_adds = len([t for t in trades if t['type'] == 'GRID_ADD'])
    partials = len([t for t in trades if t['type'] == 'PARTIAL'])
    
    print(f'\n========== 回测结果 ==========')
    print(f'初始资金: ${INITIAL_CAPITAL}')
    print(f'最终资金: ${equity:.2f}')
    print(f'净利润: ${equity - INITIAL_CAPITAL:.2f}')
    print(f'净收益率: {net_return:.2f}%')
    print(f'手续费: ${total_fees:.2f}')
    print(f'交易次数: {len(closed_trades)}')
    print(f'胜率: {win_rate:.1f}%')
    print(f'网格加仓: {grid_adds}')
    print(f'部分止盈: {partials}')
    print(f'最大回撤: {max_dd:.2f}%')
    print(f'='*60)
    
    # 保存结果
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_df = pd.DataFrame([{
        'capital': INITIAL_CAPITAL,
        'final_equity': equity,
        'net_profit': equity - INITIAL_CAPITAL,
        'net_return': net_return,
        'fees': total_fees,
        'total_trades': len(closed_trades),
        'win_rate': win_rate,
        'grid_adds': grid_adds,
        'partials': partials,
        'max_drawdown': max_dd
    }])
    result_df.to_excel(f'/home/user/.openclaw/workspace/v7_result_{ts}.xlsx', index=False)
    print(f'\n结果: v7_result_{ts}.xlsx')
    
    return result_df

if __name__ == '__main__':
    run_backtest()
