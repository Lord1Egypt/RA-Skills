"""
技术指标计算 - EMA 和 RSI
"""

from typing import List
from .models import Quote


def calc_ema(values: List[float], period: int) -> List[float]:
    """
    计算指数移动平均线 (EMA)

    EMA = (Close - EMA_prev) * multiplier + EMA_prev
    multiplier = 2 / (period + 1)
    """
    if len(values) < period:
        return []

    multiplier = 2 / (period + 1)

    # 第一个 EMA 用 SMA
    ema_values = []
    sma = sum(values[:period]) / period
    ema_values.append(sma)

    # 后续用 EMA 公式
    for i in range(period, len(values)):
        ema = (values[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)

    # 前面补 None 占位
    result = [None] * (period - 1) + ema_values
    return result


def calc_rsi(closes: List[float], period: int = 14) -> List[float]:
    """
    计算相对强弱指数 (RSI)

    RSI = 100 - (100 / (1 + RS))
    RS = 平均涨幅 / 平均跌幅
    """
    if len(closes) < period + 1:
        return []

    # 计算价格变化
    changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]

    gains = [max(0, c) for c in changes]
    losses = [max(0, -c) for c in changes]

    rsi_values = []

    # 第一个 RSI 用初始平均值
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    if avg_loss == 0:
        rsi_values.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi_values.append(100 - (100 / (1 + rs)))

    # 后续用平滑平均
    for i in range(period, len(changes)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            rsi_values.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)

    # 前面补 None 占位（period 个变化值 + 1 个初始 RSI）
    result = [None] * period + rsi_values
    return result


def calc_indicators(quotes: List[Quote]) -> List[dict]:
    """
    计算所有技术指标并返回格式化数据

    需要至少 30 天数据来计算 EMA30
    """
    if len(quotes) < 30:
        raise ValueError(f"Need at least 30 quotes, got {len(quotes)}")

    closes = [q.close for q in quotes]
    highs = [q.high for q in quotes]
    lows = [q.low for q in quotes]
    opens = [q.open for q in quotes]

    # 计算指标
    ema7 = calc_ema(closes, 7)
    ema30 = calc_ema(closes, 30)
    rsi14 = calc_rsi(closes, 14)

    # 只返回最近 7 天数据（去掉前面指标计算需要的历史数据）
    result = []
    for i in range(-7, 0):
        idx = len(quotes) + i
        q = quotes[idx]

        # 格式化日期为 MMDD
        date_str = q.time_open[5:10].replace("-", "")  # "2026-03-04" -> "0304"

        data = {
            "O": int(round(q.open)),
            "H": int(round(q.high)),
            "L": int(round(q.low)),
            "C": int(round(q.close)),
            "E7": int(round(ema7[idx])) if ema7[idx] is not None else None,
            "E30": int(round(ema30[idx])) if ema30[idx] is not None else None,
            "R14": int(round(rsi14[idx])) if rsi14[idx] is not None else None,
            "D": date_str,
        }
        result.append(data)

    return result
