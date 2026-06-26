#!/usr/bin/env python3
"""
ETH/USDT 多维技术分析与交易策略输出
- 方向：LONG / SHORT
- entry：进场价
- stop : 止损价
- tp1、tp2、tp3：分批止盈价（可自行增删）
"""
import sys, json, datetime, os
import pandas as pd
import numpy as np
import ccxt
import pandas_ta as ta

# -------------------------------------------------
# 1. 数据获取（Binance 1h K 线，最近 60 天）
# -------------------------------------------------
def fetch_ohlcv(symbol: str, timeframe: str = "1h", days: int = 60):
    exchange = ccxt.binance({"enableRateLimit": True})
    now = exchange.milliseconds()
    since = now - days * 24 * 60 * 60 * 1000
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)
    df = pd.DataFrame(ohlcv, columns=["ts", "open", "high", "low", "close", "volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    return df

# -------------------------------------------------
# 2. 指标计算（MACD、EMA、MA、KDJ、BOLL、RSI、ADX）
# -------------------------------------------------
def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df.ta.macd(append=True)                     # MACD, MACDs, MACDh
    df.ta.ema(length=20, append=True)          # EMA_20
    df.ta.sma(length=50, append=True)          # SMA_50
    df.ta.kdj(append=True)                     # KDJ_K, KDJ_D, KDJ_J
    df.ta.bbands(length=20, std=2, append=True)  # BB_upper, BB_middle, BB_lower
    df.ta.rsi(length=14, append=True)          # RSI_14
    df.ta.adx(length=14, append=True)          # ADX_14, ADX_minus, ADX_plus
    return df

# -------------------------------------------------
# 3. 缠论‑like 趋势判定（高低点结构）
# -------------------------------------------------
def chanlun_trend(df: pd.DataFrame) -> str:
    # 取最近 30 根 K 线的高低点
    recent = df.tail(30)
    high = recent["high"].max()
    low = recent["low"].min()
    # 若当前价接近最高点且 MACD 正向，判为上升趋势
    if df.iloc[-1]["close"] > high * 0.98 and df.iloc[-1]["MACD_12_26_9"] > 0:
        return "UP"
    # 若当前价接近最低点且 MACD 负向，判为下降趋势
    if df.iloc[-1]["close"] < low * 1.02 and df.iloc[-1]["MACD_12_26_9"] < 0:
        return "DOWN"
    return "SIDE"

# -------------------------------------------------
# 4. K 线形态检测（裸K、吞没、锤子、上吊等）
# -------------------------------------------------
def candle_patterns(df: pd.DataFrame) -> dict:
    last = df.iloc[-1]
    patterns = {}

    # 裸K（实体小于影线的 30%）
    body = abs(last["close"] - last["open"])
    upper = last["high"] - max(last["close"], last["open"])
    lower = min(last["close"], last["open"]) - last["low"]
    if body < 0.3 * (upper + lower):
        patterns["naked"] = True

    # 吞没形态（前一根为阴线，当前为阳线且收盘>前收盘且开盘<前开盘）
    if len(df) >= 2:
        prev = df.iloc[-2]
        if prev["close"] < prev["open"] and last["close"] > last["open"]:
            if last["close"] > prev["close"] and last["open"] < prev["open"]:
                patterns["engulfing"] = True

    # 锤子/上吊（下影线长于实体2倍，上影线短）
    if lower > 2 * body and upper < body * 0.5:
        patterns["hammer"] = True
    if upper > 2 * body and lower < body * 0.5:
        patterns["hanging_man"] = True

    return patterns

# -------------------------------------------------
# 5. 大单成交量（近似多庄/空庄筹码区）
# -------------------------------------------------
def volume_blocks(df: pd.DataFrame) -> dict:
    # 取最近 200 根 K 线的平均成交量
    avg_vol = df["volume"].tail(200).mean()
    # 大单阈值设为 3 倍平均
    big_vol = df["volume"] > 3 * avg_vol
    # 根据价格区间统计大单出现的区间
    price_bins = np.arange(df["close"].min(), df["close"].max(), (df["close"].max() - df["close"].min()) / 20)
    bin_idx = np.digitize(df["close"], price_bins)
    block_counts = {}
    for i, is_big in enumerate(big_vol):
        if is_big:
            bin_key = round(price_bins[bin_idx[i] - 1], 2)
            block_counts[bin_key] = block_counts.get(bin_key, 0) + 1
    # 取出现次数最多的 2-3 个区间作为“筹码集中区”
    top_bins = sorted(block_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    return {"hot_zones": [b[0] for b in top_bins]}

# -------------------------------------------------
# 6. 情绪与猎杀区（简化版：结合 ADX、RSI、BOLL）
# -------------------------------------------------
def sentiment_hunt(df: pd.DataFrame) -> dict:
    last = df.iloc[-1]
    # ADX > 25 表示趋势强，RSI > 70 可能超买，收盘靠近上轨可能是做市商的获利区
    hunt = {}
    if last["ADX_14"] > 25 and last["RSI_14"] > 70 and last["close"] > last["BB_upper"]:
        hunt["market_maker_hunt"] = True
    if last["ADX_14"] > 25 and last["RSI_14"] < 30 and last["close"] < last["BB_lower"]:
        hunt["market_maker_hunt"] = True
    return hunt

# -------------------------------------------------
# 7. 综合信号生成
# -------------------------------------------------
def generate_signal(df: pd.DataFrame) -> dict:
    last = df.iloc[-1]

    # 各类判断
    trend = chanlun_trend(df)
    patterns = candle_patterns(df)
    vol_info = volume_blocks(df)
    sentiment = sentiment_hunt(df)

    # 多空条件（根据经验自行组合，您可以自行调参）
    long_cond = (
        trend == "UP"
        and last["MACD_12_26_9"] > last["MACDs_12_26_9"]          # MACD 金叉
        and last["close"] > last["EMA_20"]                       # 价格在 EMA 之上
        and ("naked" in patterns or "hammer" in patterns)      # 形态支持
        and not sentiment.get("market_maker_hunt")             # 没有明显做市商猎杀
    )

    short_cond = (
        trend == "DOWN"
        and last["MACD_12_26_9"] < last["MACDs_12_26_9"]          # MACD 死叉
        and last["close"] < last["EMA_20"]                       # 价格在 EMA 之下
        and ("naked" in patterns or "hanging_man" in patterns) # 形态支持
        and not sentiment.get("market_maker_hunt")
    )

    # 计算止损、止盈（基于 ATR 以及筹码区）
    # 简单的 ATR（14）* 1.5 作为止损幅度
    df["tr"] = np.maximum(df["high"] - df["low"],
                          np.maximum(abs(df["high"] - df["close"].shift()),
                                     abs(df["low"] - df["close"].shift())))
    atr = df["tr"].rolling(14).mean().iloc[-1]

    if long_cond:
        entry = float(last["close"])
        stop = round(entry - atr * 1.5, 2)          # 止损
        # 分三档止盈：1% / 2% / 4%（可自行调节）
        tp1 = round(entry * 1.01, 2)
        tp2 = round(entry * 1.02, 2)
        tp3 = round(entry * 1.04, 2)
        signal = "LONG"
    elif short_cond:
        entry = float(last["close"])
        stop = round(entry + atr * 1.5, 2)          # 止损（空头在上方）
        tp1 = round(entry * 0.99, 2)
        tp2 = round(entry * 0.98, 2)
        tp3 = round(entry * 0.96, 2)
        signal = "SHORT"
    else:
        # 无明确信号
        return {}

    # 汇总输出
    result = {
        "signal": signal,
        "entry": entry,
        "stop": stop,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "trend": trend,
        "patterns": list(patterns.keys()),
        "hot_zones": vol_info["hot_zones"],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    return result

# -------------------------------------------------
# 8. 主入口
# -------------------------------------------------
def main():
    pair = sys.argv[1] if len(sys.argv) > 1 else "ETH/USDT"

    # 获取并计算
    df = fetch_ohlcv(pair)
    df = compute_indicators(df)

    # 生成信号
    signal = generate_signal(df)

    # 输出（如果有信号则打印 JSON，否则打印空对象）
    print(json.dumps(signal, ensure_ascii=False, indent=2) if signal else json.dumps({}))

if __name__ == "__main__":
    # 保证脚本在自身目录运行，方便相对路径
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
