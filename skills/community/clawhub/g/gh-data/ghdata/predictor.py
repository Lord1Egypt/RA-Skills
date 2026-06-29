"""
7规则投票引擎 — 纯数学计算方向预测
引用: MEMORY.md -> 7规则投票引擎 / predictor.py

本地版规则（与C#服务端同步，规则7不同）：
  1. 均线排列     — MA5>MA10>MA20>MA60=多头，反之空头
  2. MACD形态     — DIF>DEA+柱>0=多头，反之空头
  3. KDJ超买超卖  — J<20=超卖看多，J>80=超买看空
  4. RSI背离      — RSI<30=超卖看多，RSI>70=超买看空
  5. 成交量比     — 放量上涨/缩量下跌/放量下跌/缩量上涨
  6. K线形态识别  — 红三兵/三乌鸦/十字星/锤子/墓碑
  7. 波动位置     — 低位<20%反弹概率大，高位>80%回调概率大
     ⚠️ 本地版用波动位置替代资金面（因无实时资金流向数据）
        C#服务端规则7为资金面（近5日主力净额+融资余额变化）
"""
from . import config
from . import data_fetcher as fetcher
from . import db_manager as db


# ===== 技术指标计算 =====

def sma(data, n):
    if len(data) < n:
        return None
    return sum(data[-n:]) / n


def ema(data, n):
    if len(data) < n:
        return None
    m = 2 / (n + 1)
    e = sum(data[:n]) / n
    for v in data[n:]:
        e = (v - e) * m + e
    return e


def macd(close):
    if len(close) < 26:
        return None, None, None
    dif = ema(close, 12) - ema(close, 26)
    dea = ema(close[-9:], 9) if len(close) >= 9 else dif
    macd_val = (dif - dea) * 2
    return dif, dea, macd_val


def kdj(high, low, close):
    if len(high) < 9:
        return None, None, None
    ks, ds = [50], [50]
    for i in range(max(0, len(close) - 9), len(close)):
        hi = max(high[max(0, i - 8):i + 1])
        li = min(low[max(0, i - 8):i + 1])
        r = (close[i] - li) / (hi - li) * 100 if hi > li else 50
        k = 2 / 3 * ks[-1] + 1 / 3 * r
        d = 2 / 3 * ds[-1] + 1 / 3 * k
        ks.append(k)
        ds.append(d)
    j = 3 * ks[-1] - 2 * ds[-1]
    return ks[-1], ds[-1], j


def rsi(close, n=14):
    if len(close) < n + 1:
        return 50
    gains = losses = 0
    for i in range(-n, 0):
        d = close[i] - close[i - 1]
        if d > 0:
            gains += d
        else:
            losses -= d
    if losses == 0:
        return 100
    return 100 - 100 / (1 + (gains / n) / (losses / n))


def kptn_pattern(k):
    """K线形态识别"""
    if len(k) < 3:
        return "无"
    c = [x["close"] for x in k[-3:]]
    o = [x["open"] for x in k[-3:]]
    h, l = k[-1]["high"], k[-1]["low"]
    u = [c[i] > o[i] for i in range(3)]

    if all(u) and c[0] < c[1] < c[2]:
        return "红三兵"
    if not any(u) and c[0] > c[1] > c[2]:
        return "三只乌鸦"
    body = h - l
    if body > 0 and abs(c[-1] - o[-1]) / body < 0.1:
        return "十字星"
    cb = abs(c[-1] - o[-1])
    if cb > 0 and (min(c[-1], o[-1]) - l) > 2 * cb and (h - max(c[-1], o[-1])) < cb:
        return "锤子线"
    if cb > 0 and (h - max(c[-1], o[-1])) > 2 * cb and (min(c[-1], o[-1]) - l) < cb:
        return "墓碑线"
    return "无明确形态"


# ===== 7规则投票 =====

def predict(k):
    """
    7规则投票引擎
    返回 (direction, score, votes, signals, range_forecast)
    """
    if len(k) < 60:
        return "数据不足", 0, [], [], ""

    c = [x["close"] for x in k]
    h = [x["high"] for x in k]
    l = [x["low"] for x in k]
    v = [x["volume"] for x in k]

    score = config.BASE_SCORE
    votes = []
    signals = []

    # 规则1: 均线趋势
    m5 = sma(c, 5)
    m10 = sma(c, 10)
    m20 = sma(c, 20)
    m60 = sma(c, 60) if len(c) >= 60 else None
    if all(x is not None for x in [m5, m10, m20, m60]):
        if m5 > m10 > m20 > m60:
            score += 2
            votes.append({"n": "均线趋势", "v": 2, "d": "多头排列"})
        elif m5 < m10 < m20 < m60:
            score -= 2
            votes.append({"n": "均线趋势", "v": -2, "d": "空头排列"})
        else:
            votes.append({"n": "均线趋势", "v": 0, "d": "交叉黏合"})
    else:
        votes.append({"n": "均线趋势", "v": 0, "d": "N/A"})

    # 规则2: MACD
    dif, dea, m = macd(c)
    if all(x is not None for x in [dif, dea, m]):
        if dif > dea > 0 and m > 0:
            score += 2
            votes.append({"n": "MACD", "v": 2, "d": "零轴上金叉"})
        elif dif < dea < 0 and m < 0:
            score -= 2
            votes.append({"n": "MACD", "v": -2, "d": "零轴下死叉"})
        elif dif > dea:
            score += 1
            votes.append({"n": "MACD", "v": 1, "d": "DIF>DEA"})
        else:
            score -= 1
            votes.append({"n": "MACD", "v": -1, "d": "DIF<DEA"})
    else:
        votes.append({"n": "MACD", "v": 0, "d": "N/A"})

    # 规则3: KDJ
    k_, d_, j = kdj(h, l, c)
    if all(x is not None for x in [k_, d_, j]):
        if j < 20:
            score += 2
            votes.append({"n": "KDJ", "v": 2, "d": f"超卖J={j:.0f}"})
        elif j > 80:
            score -= 2
            votes.append({"n": "KDJ", "v": -2, "d": f"超买J={j:.0f}"})
        elif k_ > d_:
            score += 1
            votes.append({"n": "KDJ", "v": 1, "d": "K>D"})
        else:
            score -= 0.5
            votes.append({"n": "KDJ", "v": -0.5, "d": "K<D"})
    else:
        votes.append({"n": "KDJ", "v": 0, "d": "N/A"})

    # 规则4: RSI
    r = rsi(c)
    if r < 30:
        score += 2
        votes.append({"n": "RSI", "v": 2, "d": f"超卖{r:.0f}"})
        signals.append("RSI超卖")
    elif r > 70:
        score -= 2
        votes.append({"n": "RSI", "v": -2, "d": f"超买{r:.0f}"})
        signals.append("RSI超买")
    elif r > 50:
        score += 0.5
        votes.append({"n": "RSI", "v": 0.5, "d": f"偏强{r:.0f}"})
    else:
        score -= 0.5
        votes.append({"n": "RSI", "v": -0.5, "d": f"偏弱{r:.0f}"})

    # 规则5: 成交量
    if len(v) >= 10:
        avg_v = sum(v[-10:-1]) / 9
        if v[-1] > avg_v * 1.5 and c[-1] > c[-2]:
            score += 1
            votes.append({"n": "成交量", "v": 1, "d": "放量上涨"})
            signals.append("放量上涨")
        elif v[-1] > avg_v * 1.5 and c[-1] < c[-2]:
            score -= 1
            votes.append({"n": "成交量", "v": -1, "d": "放量下跌"})
            signals.append("放量下跌")
        elif v[-1] < avg_v * 0.5:
            votes.append({"n": "成交量", "v": 0, "d": "缩量"})
        else:
            votes.append({"n": "成交量", "v": 0, "d": "正常"})
    else:
        votes.append({"n": "成交量", "v": 0, "d": "N/A"})

    # 规则6: K线形态
    pattern = kptn_pattern(k)
    if pattern in ("红三兵", "锤子线"):
        score += 1
        votes.append({"n": "K线形态", "v": 1, "d": pattern})
        signals.append(pattern)
    elif pattern in ("三只乌鸦", "墓碑线"):
        score -= 1
        votes.append({"n": "K线形态", "v": -1, "d": pattern})
        signals.append(pattern)
    else:
        votes.append({"n": "K线形态", "v": 0, "d": pattern})

    # 规则7: 波动位置
    if len(c) >= 20:
        recent_high = max(c[-20:])
        recent_low = min(c[-20:])
        pos = (c[-1] - recent_low) / (recent_high - recent_low) * 100 if recent_high > recent_low else 50
        if pos < 20:
            score += 1.5
            votes.append({"n": "波动位置", "v": 1.5, "d": f"低位{pos:.0f}%"})
            signals.append("低位")
        elif pos > 80:
            score -= 1.5
            votes.append({"n": "波动位置", "v": -1.5, "d": f"高位{pos:.0f}%"})
            signals.append("高位")
        else:
            votes.append({"n": "波动位置", "v": 0, "d": f"中位{pos:.0f}%"})
    else:
        votes.append({"n": "波动位置", "v": 0, "d": "N/A"})

    # 综合判定
    if score >= 6.5:
        direction = "偏多"
    elif score >= 5.5:
        direction = "震荡偏多"
    elif score >= 4.5:
        direction = "震荡"
    elif score >= 3.5:
        direction = "震荡偏空"
    else:
        direction = "偏空"

    range_forecast = config.RANGE_MAP.get(direction, "")
    return direction, score, votes, signals, range_forecast


def analyze(code: str, klines: list = None) -> dict:
    """
    对指定股票进行方向预测
    klines: [{date, open, close, high, low, volume}, ...]
    如不传则自动从数据库拉取
    """
    if klines is None:
        # 直接从腾讯API拉取K线（不依赖WebAPI）
        raw = fetcher.fetch_kline(code, 365)
        if raw and isinstance(raw, list) and len(raw) > 0:
            klines = raw

    if len(klines) < 60:
        return {"code": code, "error": f"数据不足({len(klines)}条)", "direction": "数据不足"}

    direction, score, votes, signals, range_fc = predict(klines)
    latest = klines[-1]

    acc_all = db.get_accuracy_stats(code, 36500)
    acc_60 = db.get_accuracy_stats(code, 60)
    acc_30 = db.get_accuracy_stats(code, 30)

    # 规律挖掘
    from . import pattern_miner
    patterns = pattern_miner.mine(klines)

    return {
        "code": code,
        "name": "",
        "date": latest["date"],
        "price": latest["close"],
        "direction": direction,
        "score": score,
        "range_forecast": range_fc,
        "votes": votes,
        "signals": signals,
        "accuracy": {
            "all": acc_all,
            "60d": acc_60,
            "30d": acc_30,
        },
        "patterns": patterns,
    }


def judge(direction, actual_change):
    """判断预测是否正确"""
    if direction == "偏多" and actual_change > 0.5:
        return True
    if direction == "偏空" and actual_change < -0.5:
        return True
    if direction == "震荡偏多" and actual_change > -0.5:
        return True
    if direction == "震荡偏空" and actual_change < 0.5:
        return True
    if direction == "震荡" and -1 <= actual_change <= 1:
        return True
    return False
