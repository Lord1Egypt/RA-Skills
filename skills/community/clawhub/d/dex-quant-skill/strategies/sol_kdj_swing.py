"""
SOL KDJ Swing — KDJ 超买超卖摆动策略
4h 周期，KDJ 金叉/死叉 + EMA50 趋势过滤。
多空双向，适合 SOL 高波动特性。
"""

import sys
sys.path.insert(0, '/scripts')

from data_client import DataClient
from indicators import Indicators as ind
import numpy as np

PARAMS = {
    'k_period': 9,
    'd_period': 3,
    'j_smooth': 3,
    'trend_ema': 50,
    'k_oversold': 20,
    'k_overbought': 80,
    'rsi_period': 14,
    'rsi_confirm_long': 40,
    'rsi_confirm_short': 60,
    'atr_period': 14,
    'sl_atr': 1.8,
    'tp_atr': 3.5,
    'max_bars': 20,
    'cooldown_bars': 2,
}


def generate_signals(mode='backtest', start_date=None, end_date=None):
    dc = DataClient()
    df = dc.get_perp_klines("SOLUSDT", "4h", start_date, end_date)

    close = df["close"].values.astype(float)
    high = df["high"].values.astype(float)
    low = df["low"].values.astype(float)

    k_val, d_val, j_val = ind.kdj(high, low, close, PARAMS['k_period'], PARAMS['d_period'], PARAMS['j_smooth'])
    ema_trend = ind.ema(close, PARAMS['trend_ema'])
    rsi = ind.rsi(close, PARAMS['rsi_period'])
    atr = ind.atr(high, low, close, PARAMS['atr_period'])
    k_cross_up = ind.crossover(k_val, d_val)
    k_cross_down = ind.crossunder(k_val, d_val)

    lookback = PARAMS['trend_ema'] + 5
    signals = []
    in_position = False
    position_side = None
    entry_bar = 0
    entry_price = 0.0
    last_exit_bar = -999

    for i in range(lookback, len(df)):
        if np.isnan(k_val[i]) or np.isnan(ema_trend[i]) or np.isnan(rsi[i]) or np.isnan(atr[i]):
            continue
        if atr[i] <= 0:
            continue

        ts = str(df.iloc[i]["datetime"])
        price = close[i]

        if in_position:
            bars_held = i - entry_bar

            if position_side == "long":
                sl_hit = price <= entry_price - PARAMS['sl_atr'] * atr[entry_bar]
                tp_hit = price >= entry_price + PARAMS['tp_atr'] * atr[entry_bar]
                signal_exit = k_val[i] > PARAMS['k_overbought'] and k_cross_down[i]
            else:
                sl_hit = price >= entry_price + PARAMS['sl_atr'] * atr[entry_bar]
                tp_hit = price <= entry_price - PARAMS['tp_atr'] * atr[entry_bar]
                signal_exit = k_val[i] < PARAMS['k_oversold'] and k_cross_up[i]

            timeout = bars_held >= PARAMS['max_bars']

            exit_reason = None
            if sl_hit:
                exit_reason = "stop loss"
            elif tp_hit:
                exit_reason = "take profit"
            elif signal_exit:
                exit_reason = "KDJ overbought/oversold exit"
            elif timeout:
                exit_reason = f"timeout {PARAMS['max_bars']} bars"

            if exit_reason:
                signals.append({
                    "timestamp": ts, "symbol": "SOLUSDT",
                    "action": "sell" if position_side == "long" else "buy",
                    "direction": position_side,
                    "confidence": 0.8,
                    "reason": exit_reason,
                    "price_at_signal": price,
                })
                in_position = False
                last_exit_bar = i
            continue

        if i - last_exit_bar < PARAMS['cooldown_bars']:
            continue

        uptrend = close[i] > ema_trend[i]
        downtrend = close[i] < ema_trend[i]

        if k_cross_up[i] and k_val[i-1] < PARAMS['k_oversold'] and uptrend:
            rsi_ok = rsi[i] > PARAMS['rsi_confirm_long']
            if rsi_ok:
                sl = price - PARAMS['sl_atr'] * atr[i]
                tp = price + PARAMS['tp_atr'] * atr[i]
                signals.append({
                    "timestamp": ts, "symbol": "SOLUSDT",
                    "action": "buy", "direction": "long",
                    "confidence": 0.85,
                    "reason": f"KDJ golden cross from oversold K={k_val[i]:.0f} RSI={rsi[i]:.0f}",
                    "price_at_signal": price,
                    "suggested_stop_loss": sl,
                    "suggested_take_profit": tp,
                })
                in_position = True
                position_side = "long"
                entry_bar = i
                entry_price = price

        elif k_cross_down[i] and k_val[i-1] > PARAMS['k_overbought'] and downtrend:
            rsi_ok = rsi[i] < PARAMS['rsi_confirm_short']
            if rsi_ok:
                sl = price + PARAMS['sl_atr'] * atr[i]
                tp = price - PARAMS['tp_atr'] * atr[i]
                signals.append({
                    "timestamp": ts, "symbol": "SOLUSDT",
                    "action": "sell", "direction": "short",
                    "confidence": 0.85,
                    "reason": f"KDJ death cross from overbought K={k_val[i]:.0f} RSI={rsi[i]:.0f}",
                    "price_at_signal": price,
                    "suggested_stop_loss": sl,
                    "suggested_take_profit": tp,
                })
                in_position = True
                position_side = "short"
                entry_bar = i
                entry_price = price

    return {"strategy_name": "SOL KDJ Swing", "signals": signals}


if __name__ == "__main__":
    result = generate_signals("backtest", "2025-01-01", "2025-12-31")
    print(f"策略: {result['strategy_name']}")
    print(f"信号数: {len(result['signals'])}")
    for s in result['signals'][:10]:
        print(f"  {s['timestamp']} {s['action']} {s['direction']} @ {s['price_at_signal']:.2f} | {s['reason']}")
