"""
Example Custom Strategy: Mean Reversion + RSI + MACD Filters
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Combines the proven mean_reversion logic (BTC +4.78% baseline) with
RSI oversold/overbought confirmation and MACD trend alignment.

LONG:  Price drops 4%+ from 480-bar high AND RSI < 40 AND MACD histogram rising
SHORT: Price rises 4%+ from 480-bar low AND RSI > 60 AND MACD histogram falling
Exit:  3% recovery OR 5% stop loss OR 8% take profit

Tuned for 1-minute candle data with 3.5bps fees per trade.
"""


def strategy(df):
    signals = []
    in_position = False
    is_long = True
    entry_price = 0.0
    bars_since_exit = 999
    cooldown = 120        # 2h cooldown between trades
    lookback = 480        # 8h lookback window
    entry_threshold = 0.04  # 4% move to trigger entry
    exit_threshold = 0.03   # 3% recovery to take profit
    stop_loss = 0.05        # 5% stop loss
    take_profit = 0.08      # 8% take profit

    # Indicators for filtering
    rsi_vals = rsi(df["close"], period=14)
    _, _, macd_hist = macd(df["close"], fast=12, slow=26, signal=9)

    for i in range(lookback, len(df)):
        price = df.iloc[i]["close"]
        window = df.iloc[i - lookback:i]
        window_high = window["high"].max()
        window_low = window["low"].min()

        if not in_position:
            bars_since_exit += 1
            if bars_since_exit < cooldown:
                continue

            # LONG: price dropped from high + RSI confirms oversold area + MACD not deeply bearish
            drop_from_high = (window_high - price) / window_high
            if drop_from_high >= entry_threshold:
                rsi_ok = rsi_vals.iloc[i] < 40  # More lenient than pure RSI strategy
                macd_ok = macd_hist.iloc[i] > macd_hist.iloc[i - 1]  # MACD improving
                if rsi_ok and macd_ok:
                    signals.append({
                        "bar": i,
                        "action": "long",
                        "size": 0.2,
                        "reason": f"Drop {drop_from_high*100:.1f}% + RSI={rsi_vals.iloc[i]:.0f} + MACD↑",
                    })
                    in_position = True
                    is_long = True
                    entry_price = price
                    continue

            # SHORT: price rose from low + RSI confirms overbought area + MACD weakening
            rise_from_low = (price - window_low) / window_low
            if rise_from_low >= entry_threshold:
                rsi_ok = rsi_vals.iloc[i] > 60
                macd_ok = macd_hist.iloc[i] < macd_hist.iloc[i - 1]  # MACD declining
                if rsi_ok and macd_ok:
                    signals.append({
                        "bar": i,
                        "action": "short",
                        "size": 0.2,
                        "reason": f"Rise {rise_from_low*100:.1f}% + RSI={rsi_vals.iloc[i]:.0f} + MACD↓",
                    })
                    in_position = True
                    is_long = False
                    entry_price = price

        else:
            # PnL calculation
            if is_long:
                pnl_pct = (price - entry_price) / entry_price
            else:
                pnl_pct = (entry_price - price) / entry_price

            exit_reason = None
            if pnl_pct <= -stop_loss:
                exit_reason = f"Stop loss {pnl_pct*100:.1f}%"
            elif pnl_pct >= take_profit:
                exit_reason = f"Take profit {pnl_pct*100:.1f}%"
            elif pnl_pct >= exit_threshold:
                exit_reason = f"Target exit {pnl_pct*100:.1f}%"

            if exit_reason:
                signals.append({
                    "bar": i, "action": "close", "size": 1.0,
                    "reason": exit_reason,
                })
                in_position = False
                bars_since_exit = 0

    return signals
