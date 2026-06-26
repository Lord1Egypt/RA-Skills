"""
SOL RSI 动量策略
4h 周期，RSI 进入超买区 (>65) 追涨做多（动量策略），
RSI 进入超卖区 (<35) 追跌做空。
EMA50 趋势过滤，只做顺势。宽 trailing stop。
"""

import sys
sys.path.insert(0, '/scripts')

from data_client import DataClient
from indicators import Indicators as ind
import numpy as np

PARAMS = {
    'rsi_period': 14,
    'rsi_long_entry': 65,
    'rsi_short_entry': 35,
    'trend_ema': 50,
    'atr_period': 14,
    'sl_atr': 2.0,
    'trail_atr': 3.0,
    'max_bars': 40,
    'cooldown_bars': 5,
}


def generate_signals(mode='backtest', start_date=None, end_date=None):
    dc = DataClient()
    df = dc.get_perp_klines("SOLUSDT", "4h", start_date, end_date)

    close = df["close"].values.astype(float)
    high = df["high"].values.astype(float)
    low = df["low"].values.astype(float)

    rsi = ind.rsi(close, PARAMS['rsi_period'])
    ema_trend = ind.ema(close, PARAMS['trend_ema'])
    atr = ind.atr(high, low, close, PARAMS['atr_period'])

    lookback = PARAMS['trend_ema'] + 5
    signals = []
    in_position = False
    position_side = None
    entry_bar = 0
    entry_price = 0.0
    best_price = 0.0
    trail_stop = 0.0
    last_exit_bar = -999

    for i in range(lookback, len(df)):
        if np.isnan(rsi[i]) or np.isnan(ema_trend[i]) or np.isnan(atr[i]):
            continue
        if atr[i] <= 0:
            continue

        ts = str(df.iloc[i]["datetime"])
        price = close[i]

        if in_position:
            bars_held = i - entry_bar
            if position_side == "long":
                if price > best_price:
                    best_price = price
                    trail_stop = max(trail_stop, best_price - PARAMS['trail_atr'] * atr[i])
                sl_hit = price <= trail_stop
            else:
                if price < best_price:
                    best_price = price
                    trail_stop = min(trail_stop, best_price + PARAMS['trail_atr'] * atr[i])
                sl_hit = price >= trail_stop

            timeout = bars_held >= PARAMS['max_bars']
            exit_reason = None
            if sl_hit:
                exit_reason = "trailing stop"
            elif timeout:
                exit_reason = f"timeout {PARAMS['max_bars']} bars"

            if exit_reason:
                signals.append({
                    "timestamp": ts, "symbol": "SOLUSDT",
                    "action": "sell" if position_side == "long" else "buy",
                    "direction": position_side,
                    "confidence": 0.8, "reason": exit_reason,
                    "price_at_signal": price,
                })
                in_position = False
                last_exit_bar = i
            continue

        if i - last_exit_bar < PARAMS['cooldown_bars']:
            continue

        uptrend = close[i] > ema_trend[i]
        downtrend = close[i] < ema_trend[i]

        rsi_enter_long = rsi[i] > PARAMS['rsi_long_entry'] and rsi[i-1] <= PARAMS['rsi_long_entry']
        rsi_enter_short = rsi[i] < PARAMS['rsi_short_entry'] and rsi[i-1] >= PARAMS['rsi_short_entry']

        if rsi_enter_long and uptrend:
            sl = price - PARAMS['sl_atr'] * atr[i]
            signals.append({
                "timestamp": ts, "symbol": "SOLUSDT",
                "action": "buy", "direction": "long",
                "confidence": 0.8,
                "reason": f"RSI momentum entry {rsi[i]:.0f}, uptrend",
                "price_at_signal": price,
                "suggested_stop_loss": sl,
            })
            in_position = True
            position_side = "long"
            entry_bar = i
            entry_price = price
            best_price = price
            trail_stop = sl

        elif rsi_enter_short and downtrend:
            sl = price + PARAMS['sl_atr'] * atr[i]
            signals.append({
                "timestamp": ts, "symbol": "SOLUSDT",
                "action": "sell", "direction": "short",
                "confidence": 0.8,
                "reason": f"RSI momentum entry {rsi[i]:.0f}, downtrend",
                "price_at_signal": price,
                "suggested_stop_loss": sl,
            })
            in_position = True
            position_side = "short"
            entry_bar = i
            entry_price = price
            best_price = price
            trail_stop = sl

    return {"strategy_name": "SOL RSI Momentum", "signals": signals}
