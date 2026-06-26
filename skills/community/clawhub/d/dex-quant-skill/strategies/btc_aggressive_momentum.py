"""
BTC Aggressive Momentum Breakout
快进快出，追强势突破，EMA9/21/55 + 20周期高点突破 + RSI + 放量确认
"""

import sys
sys.path.insert(0, '/Users/lvsanli/Desktop/dex-skill/scripts')

from data_client import DataClient
from indicators import Indicators as ind
import numpy as np

PARAMS = {
    'ema_fast': 9,
    'ema_mid': 21,
    'ema_slow': 55,
    'breakout_period': 20,
    'rsi_period': 14,
    'rsi_entry': 62,
    'rsi_exit': 48,
    'vol_mult': 1.5,
    'vol_period': 20,
    'sl_atr': 1.8,
    'tp_atr': 3.2,
    'max_bars': 18,
    'max_consecutive_losses': 3,
}


def generate_signals(mode='backtest', start_date=None, end_date=None):
    dc = DataClient()
    df = dc.get_perp_klines("BTCUSDT", "1h", start_date, end_date)

    close = df["close"].values.astype(float)
    high = df["high"].values.astype(float)
    low = df["low"].values.astype(float)
    volume = df["volume"].values.astype(float)

    ema_fast = ind.ema(close, PARAMS['ema_fast'])
    ema_mid = ind.ema(close, PARAMS['ema_mid'])
    ema_slow = ind.ema(close, PARAMS['ema_slow'])
    rsi = ind.rsi(close, PARAMS['rsi_period'])
    atr = ind.atr(high, low, close, 14)
    vol_ma = ind.sma(volume, PARAMS['vol_period'])

    bp = PARAMS['breakout_period']
    lookback = max(PARAMS['ema_slow'], bp, PARAMS['vol_period']) + 1

    signals = []
    in_position = False
    entry_bar = 0
    consecutive_losses = 0
    last_entry_price = 0.0

    for i in range(lookback, len(df)):
        if np.isnan(ema_fast[i]) or np.isnan(ema_mid[i]) or np.isnan(ema_slow[i]):
            continue
        if np.isnan(rsi[i]) or np.isnan(atr[i]) or np.isnan(vol_ma[i]):
            continue
        if atr[i] <= 0 or vol_ma[i] <= 0:
            continue

        ts = str(df.iloc[i]["datetime"])
        price = close[i]

        if in_position:
            bars_held = i - entry_bar
            sl_price = last_entry_price - PARAMS['sl_atr'] * atr[entry_bar]
            tp_price = last_entry_price + PARAMS['tp_atr'] * atr[entry_bar]

            exit_reason = None
            if price <= sl_price:
                exit_reason = f"止损触发 (SL={sl_price:.1f})"
                consecutive_losses += 1
            elif price >= tp_price:
                exit_reason = f"止盈触发 (TP={tp_price:.1f})"
                consecutive_losses = 0
            elif price < ema_mid[i]:
                exit_reason = "跌破EMA21"
                if price < last_entry_price:
                    consecutive_losses += 1
                else:
                    consecutive_losses = 0
            elif rsi[i] < PARAMS['rsi_exit']:
                exit_reason = f"RSI={rsi[i]:.1f}<{PARAMS['rsi_exit']}"
                if price < last_entry_price:
                    consecutive_losses += 1
                else:
                    consecutive_losses = 0
            elif bars_held >= PARAMS['max_bars']:
                exit_reason = f"持仓超{PARAMS['max_bars']}根K线"
                if price < last_entry_price:
                    consecutive_losses += 1
                else:
                    consecutive_losses = 0

            if exit_reason:
                signals.append({
                    "timestamp": ts,
                    "symbol": "BTCUSDT",
                    "action": "sell",
                    "direction": "long",
                    "confidence": 0.8,
                    "reason": exit_reason,
                    "price_at_signal": price,
                })
                in_position = False
            continue

        if consecutive_losses >= PARAMS['max_consecutive_losses']:
            if i > 0 and str(df.iloc[i]["datetime"])[:10] != str(df.iloc[i-1]["datetime"])[:10]:
                consecutive_losses = 0
            else:
                continue

        highest_n = np.max(high[i - bp:i])
        trend_aligned = ema_fast[i] > ema_mid[i] > ema_slow[i]
        breakout = price > highest_n
        rsi_ok = rsi[i] > PARAMS['rsi_entry']
        volume_surge = volume[i] > vol_ma[i] * PARAMS['vol_mult']

        if trend_aligned and breakout and rsi_ok and volume_surge:
            sl = price - PARAMS['sl_atr'] * atr[i]
            tp = price + PARAMS['tp_atr'] * atr[i]
            signals.append({
                "timestamp": ts,
                "symbol": "BTCUSDT",
                "action": "buy",
                "direction": "long",
                "confidence": 0.85,
                "reason": f"突破{bp}周期高点 EMA9>21>55 RSI={rsi[i]:.1f} Vol={volume[i]/vol_ma[i]:.1f}x",
                "price_at_signal": price,
                "suggested_stop_loss": sl,
                "suggested_take_profit": tp,
            })
            in_position = True
            entry_bar = i
            last_entry_price = price

    return {"strategy_name": "BTC Aggressive Momentum Breakout", "signals": signals}


if __name__ == "__main__":
    result = generate_signals("backtest", "2025-01-01", "2025-12-31")
    print(f"策略: {result['strategy_name']}")
    print(f"信号数: {len(result['signals'])}")
    for s in result['signals'][:5]:
        print(f"  {s['timestamp']} {s['action']} {s['direction']} @ {s['price_at_signal']:.2f} | {s['reason']}")
