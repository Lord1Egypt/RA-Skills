"""
BTC MACD Trend — MACD 趋势跟踪策略
4h 周期，MACD 金叉/死叉 + EMA200 方向过滤 + 柱状图动量确认。
多空双向，中频交易。
"""

import sys
sys.path.insert(0, '/scripts')

from data_client import DataClient
from indicators import Indicators as ind
import numpy as np

PARAMS = {
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'trend_ema': 100,
    'fast_ema': 50,
    'rsi_period': 14,
    'rsi_long_min': 45,
    'rsi_short_max': 55,
    'atr_period': 14,
    'sl_atr': 1.5,
    'tp_atr': 4.0,
    'max_bars': 30,
    'hist_threshold': 0,
    'cooldown_bars': 3,
}


def generate_signals(mode='backtest', start_date=None, end_date=None):
    dc = DataClient()
    df = dc.get_perp_klines("BTCUSDT", "4h", start_date, end_date)

    close = df["close"].values.astype(float)
    high = df["high"].values.astype(float)
    low = df["low"].values.astype(float)

    macd_line, signal_line, histogram = ind.macd(close, PARAMS['macd_fast'], PARAMS['macd_slow'], PARAMS['macd_signal'])
    ema_trend = ind.ema(close, PARAMS['trend_ema'])
    ema_fast = ind.ema(close, PARAMS['fast_ema'])
    rsi = ind.rsi(close, PARAMS['rsi_period'])
    atr = ind.atr(high, low, close, PARAMS['atr_period'])

    macd_cross_up = ind.crossover(macd_line, signal_line)
    macd_cross_down = ind.crossunder(macd_line, signal_line)

    lookback = PARAMS['trend_ema'] + 5
    signals = []
    in_position = False
    position_side = None
    entry_bar = 0
    entry_price = 0.0
    last_exit_bar = -999

    for i in range(lookback, len(df)):
        if np.isnan(ema_trend[i]) or np.isnan(rsi[i]) or np.isnan(atr[i]):
            continue
        if np.isnan(macd_line[i]) or np.isnan(signal_line[i]) or np.isnan(histogram[i]):
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
                signal_exit = macd_cross_down[i]
                trend_exit = close[i] < ema_fast[i] and close[i-1] < ema_fast[i-1]
            else:
                sl_hit = price >= entry_price + PARAMS['sl_atr'] * atr[entry_bar]
                tp_hit = price <= entry_price - PARAMS['tp_atr'] * atr[entry_bar]
                signal_exit = macd_cross_up[i]
                trend_exit = close[i] > ema_fast[i] and close[i-1] > ema_fast[i-1]

            timeout = bars_held >= PARAMS['max_bars']

            exit_reason = None
            if sl_hit:
                exit_reason = "stop loss"
            elif tp_hit:
                exit_reason = "take profit"
            elif signal_exit:
                exit_reason = "MACD cross exit"
            elif trend_exit:
                exit_reason = f"price below EMA{PARAMS['fast_ema']}"
            elif timeout:
                exit_reason = f"timeout {PARAMS['max_bars']} bars"

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

        uptrend = close[i] > ema_trend[i] and ema_fast[i] > ema_trend[i]
        downtrend = close[i] < ema_trend[i] and ema_fast[i] < ema_trend[i]

        if macd_cross_up[i] and uptrend and histogram[i] > PARAMS['hist_threshold']:
            rsi_ok = rsi[i] > PARAMS['rsi_long_min']
            if rsi_ok:
                sl = price - PARAMS['sl_atr'] * atr[i]
                tp = price + PARAMS['tp_atr'] * atr[i]
                signals.append({
                    "timestamp": ts, "symbol": "BTCUSDT",
                    "action": "buy", "direction": "long",
                    "confidence": 0.85,
                    "reason": f"MACD golden cross above EMA{PARAMS['trend_ema']} RSI={rsi[i]:.0f}",
                    "price_at_signal": price,
                    "suggested_stop_loss": sl,
                    "suggested_take_profit": tp,
                })
                in_position = True
                position_side = "long"
                entry_bar = i
                entry_price = price

        elif macd_cross_down[i] and downtrend and histogram[i] < -PARAMS['hist_threshold']:
            rsi_ok = rsi[i] < PARAMS['rsi_short_max']
            if rsi_ok:
                sl = price + PARAMS['sl_atr'] * atr[i]
                tp = price - PARAMS['tp_atr'] * atr[i]
                signals.append({
                    "timestamp": ts, "symbol": "BTCUSDT",
                    "action": "sell", "direction": "short",
                    "confidence": 0.85,
                    "reason": f"MACD death cross below EMA{PARAMS['trend_ema']} RSI={rsi[i]:.0f}",
                    "price_at_signal": price,
                    "suggested_stop_loss": sl,
                    "suggested_take_profit": tp,
                })
                in_position = True
                position_side = "short"
                entry_bar = i
                entry_price = price

    return {"strategy_name": "BTC MACD Trend", "signals": signals}


if __name__ == "__main__":
    result = generate_signals("backtest", "2025-01-01", "2025-12-31")
    print(f"策略: {result['strategy_name']}")
    print(f"信号数: {len(result['signals'])}")
    for s in result['signals'][:10]:
        print(f"  {s['timestamp']} {s['action']} {s['direction']} @ {s['price_at_signal']:.2f} | {s['reason']}")
