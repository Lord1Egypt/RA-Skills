"""
BTC Trend Pullback — 趋势回踩策略
4h 周期，EMA50 判趋势方向，价格回踩 EMA20 后入场，ATR trailing 出场。
多空双向，低频高质量交易。
"""

import sys
sys.path.insert(0, '/scripts')

from data_client import DataClient
from indicators import Indicators as ind
import numpy as np

PARAMS = {
    'trend_ema': 50,
    'entry_ema': 20,
    'rsi_period': 14,
    'rsi_long_min': 35,
    'rsi_long_max': 60,
    'rsi_short_min': 40,
    'rsi_short_max': 65,
    'atr_period': 14,
    'sl_atr': 1.5,
    'tp_atr': 3.5,
    'trail_atr': 2.0,
    'max_bars': 40,
    'cooldown_bars': 5,
}


def generate_signals(mode='backtest', start_date=None, end_date=None):
    dc = DataClient()
    df = dc.get_perp_klines("BTCUSDT", "4h", start_date, end_date)

    close = df["close"].values.astype(float)
    high = df["high"].values.astype(float)
    low = df["low"].values.astype(float)

    ema_trend = ind.ema(close, PARAMS['trend_ema'])
    ema_entry = ind.ema(close, PARAMS['entry_ema'])
    rsi = ind.rsi(close, PARAMS['rsi_period'])
    atr = ind.atr(high, low, close, PARAMS['atr_period'])

    lookback = PARAMS['trend_ema'] + 5
    signals = []
    in_position = False
    position_side = None
    entry_bar = 0
    entry_price = 0.0
    trail_stop = 0.0
    last_exit_bar = -999

    for i in range(lookback, len(df)):
        if np.isnan(ema_trend[i]) or np.isnan(ema_entry[i]) or np.isnan(rsi[i]) or np.isnan(atr[i]):
            continue
        if atr[i] <= 0:
            continue

        ts = str(df.iloc[i]["datetime"])
        price = close[i]

        if in_position:
            bars_held = i - entry_bar

            if position_side == "long":
                new_trail = price - PARAMS['trail_atr'] * atr[i]
                trail_stop = max(trail_stop, new_trail)
                sl_hit = low[i] <= trail_stop
                tp_hit = price >= entry_price + PARAMS['tp_atr'] * atr[entry_bar]
                timeout = bars_held >= PARAMS['max_bars']
                trend_lost = close[i] < ema_trend[i] and close[i-1] < ema_trend[i-1]
            else:
                new_trail = price + PARAMS['trail_atr'] * atr[i]
                trail_stop = min(trail_stop, new_trail)
                sl_hit = high[i] >= trail_stop
                tp_hit = price <= entry_price - PARAMS['tp_atr'] * atr[entry_bar]
                timeout = bars_held >= PARAMS['max_bars']
                trend_lost = close[i] > ema_trend[i] and close[i-1] > ema_trend[i-1]

            exit_reason = None
            if sl_hit:
                exit_reason = "trailing stop"
            elif tp_hit:
                exit_reason = "take profit"
            elif timeout:
                exit_reason = f"timeout {PARAMS['max_bars']} bars"
            elif trend_lost:
                exit_reason = "trend reversed"

            if exit_reason:
                signals.append({
                    "timestamp": ts, "symbol": "BTCUSDT",
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

        uptrend = close[i] > ema_trend[i] and ema_entry[i] > ema_trend[i]
        downtrend = close[i] < ema_trend[i] and ema_entry[i] < ema_trend[i]

        touched_entry_ema = low[i] <= ema_entry[i] * 1.005 and close[i] > ema_entry[i]
        touched_entry_ema_short = high[i] >= ema_entry[i] * 0.995 and close[i] < ema_entry[i]

        if uptrend and touched_entry_ema:
            rsi_ok = PARAMS['rsi_long_min'] <= rsi[i] <= PARAMS['rsi_long_max']
            if rsi_ok:
                sl = price - PARAMS['sl_atr'] * atr[i]
                tp = price + PARAMS['tp_atr'] * atr[i]
                trail_stop = price - PARAMS['trail_atr'] * atr[i]
                signals.append({
                    "timestamp": ts, "symbol": "BTCUSDT",
                    "action": "buy", "direction": "long",
                    "confidence": 0.85,
                    "reason": f"uptrend pullback to EMA{PARAMS['entry_ema']} RSI={rsi[i]:.0f}",
                    "price_at_signal": price,
                    "suggested_stop_loss": sl,
                    "suggested_take_profit": tp,
                })
                in_position = True
                position_side = "long"
                entry_bar = i
                entry_price = price

        elif downtrend and touched_entry_ema_short:
            rsi_ok = PARAMS['rsi_short_min'] <= rsi[i] <= PARAMS['rsi_short_max']
            if rsi_ok:
                sl = price + PARAMS['sl_atr'] * atr[i]
                tp = price - PARAMS['tp_atr'] * atr[i]
                trail_stop = price + PARAMS['trail_atr'] * atr[i]
                signals.append({
                    "timestamp": ts, "symbol": "BTCUSDT",
                    "action": "sell", "direction": "short",
                    "confidence": 0.85,
                    "reason": f"downtrend pullback to EMA{PARAMS['entry_ema']} RSI={rsi[i]:.0f}",
                    "price_at_signal": price,
                    "suggested_stop_loss": sl,
                    "suggested_take_profit": tp,
                })
                in_position = True
                position_side = "short"
                entry_bar = i
                entry_price = price

    return {"strategy_name": "BTC Trend Pullback", "signals": signals}


if __name__ == "__main__":
    result = generate_signals("backtest", "2025-01-01", "2025-12-31")
    print(f"策略: {result['strategy_name']}")
    print(f"信号数: {len(result['signals'])}")
    for s in result['signals'][:10]:
        print(f"  {s['timestamp']} {s['action']} {s['direction']} @ {s['price_at_signal']:.2f} | {s['reason']}")
