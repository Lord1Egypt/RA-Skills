"""
基金技术指标计算模块
纯 Python 实现，不依赖任何量化库
"""
import math
from typing import Optional


def calc_ma(prices: list, period: int) -> Optional[float]:
    """简单移动平均"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def calc_ema(prices: list, period: int) -> Optional[float]:
    """指数移动平均"""
    if len(prices) < period:
        return None
    alpha = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = alpha * p + (1 - alpha) * ema
    return ema


def calc_rsi(prices: list, period: int = 14) -> Optional[float]:
    """相对强弱指数 RSI"""
    if len(prices) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i-1]
        if delta > 0:
            gains.append(delta)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(delta))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calc_macd(prices: list, fast: int = 12, slow: int = 26, signal: int = 9):
    """MACD 指标"""
    if len(prices) < slow + signal:
        return None, None, None

    def ema_single(data, n):
        alpha = 2 / (n + 1)
        ema = data[0]
        for v in data[1:]:
            ema = alpha * v + (1 - alpha) * ema
        return ema

    ema_fast = ema_single(prices, fast)
    ema_slow = ema_single(prices, slow)

    if ema_fast is None or ema_slow is None:
        return None, None, None

    dif = ema_fast - ema_slow
    # Signal line = EMA of DIF over `signal` periods (simplified)
    # We approximate signal as DIF * 0.9 for short signals
    dea = dif * 0.9  # simplified

    macd = (dif - dea) * 2  # histogram
    return round(dif, 4), round(dea, 4), round(macd, 4)


def calc_stochastics(highs: list, lows: list, closes: list, period: int = 14) -> Optional[tuple]:
    """随机指标 KDJ"""
    if len(closes) < period:
        return None, None, None
    recent_high = max(highs[-period:])
    recent_low = min(lows[-period:])
    k = 50.0
    d = 50.0
    if recent_high != recent_low:
        k = (closes[-1] - recent_low) / (recent_high - recent_low) * 100
    d = k * 0.9 + 50 * 0.1  # simplified
    j = 3 * k - 2 * d
    return round(k, 2), round(d, 2), round(j, 2)


def calc_bollinger_bands(prices: list, period: int = 20, std_dev: int = 2) -> Optional[tuple]:
    """布林带"""
    if len(prices) < period:
        return None, None, None
    ma = sum(prices[-period:]) / period
    variance = sum((p - ma) ** 2 for p in prices[-period:]) / period
    std = math.sqrt(variance)
    upper = ma + std_dev * std
    lower = ma - std_dev * std
    return round(upper, 4), round(ma, 4), round(lower, 4)


def calc_volatility(prices: list) -> float:
    """年化波动率"""
    if len(prices) < 2:
        return 0.0
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    if not returns:
        return 0.0
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / len(returns)
    return round(math.sqrt(variance * 252) * 100, 2)  # 年化


def calc_max_drawdown(prices: list) -> float:
    """最大回撤"""
    if not prices:
        return 0.0
    peak = prices[0]
    max_dd = 0.0
    for p in prices:
        if p > peak:
            peak = p
        dd = (peak - p) / peak * 100
        if dd > max_dd:
            max_dd = dd
    return round(max_dd, 2)


def calc_var(prices: list, confidence: float = 0.95) -> float:
    """
    历史模拟法 VaR（Value at Risk）
    持仓N天，在给定置信度下最大可能亏损比例

    Args:
        prices: 历史净值列表（最新在前）
        confidence: 置信度，默认95%
    Returns:
        VaR百分比，如 2.5 表示95%置信度下单日最大亏损2.5%
    """
    if len(prices) < 10:
        return 0.0
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    if not returns:
        return 0.0
    returns.sort()
    # 95% VaR：取5%分位数的绝对值
    idx = int(len(returns) * (1 - confidence))
    var_pct = abs(returns[max(0, idx - 1)]) * 100
    return round(var_pct, 2)


def calc_sortino_ratio(prices: list, risk_free_rate: float = 0.03, target_return: float = 0.0) -> float:
    """
    索提诺比率（Sortino Ratio）
    只考虑下行风险的收益质量指标

    Args:
        prices: 历史净值列表
        risk_free_rate: 年化无风险收益率，默认3%
        target_return: 目标收益率，默认0
    Returns:
        索提诺比率
    """
    if len(prices) < 10:
        return 0.0
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    if not returns:
        return 0.0
    mean_ret = sum(returns) / len(returns) * 252
    # 下行波动率（只算负收益）
    neg_returns = [r for r in returns if r < target_return]
    if not neg_returns:
        return 0.0
    downside_std = math.sqrt(sum(r ** 2 for r in neg_returns) / len(neg_returns)) * math.sqrt(252)
    if downside_std == 0:
        return 0.0
    sortino = (mean_ret - risk_free_rate) / downside_std
    return round(sortino, 2)


def calc_calmar_ratio(prices: list, risk_free_rate: float = 0.03) -> float:
    """
    卡玛比率（Calmar Ratio）
    年化收益 / 最大回撤

    Args:
        prices: 历史净值列表
        risk_free_rate: 年化无风险收益率，默认3%
    Returns:
        卡玛比率（正值表示收益覆盖回撤）
    """
    if len(prices) < 10:
        return 0.0
    # 年化收益率
    if prices[0] == 0:
        return 0.0
    total_return = (prices[0] - prices[-1]) / prices[-1]
    years = len(prices) / 252
    annual_return = ((1 + total_return) ** (1 / years) - 1) if years > 0 else 0
    max_dd = calc_max_drawdown(prices)
    if max_dd == 0:
        return 0.0
    calmar = (annual_return - risk_free_rate) / (max_dd / 100)
    return round(calmar, 2)



    """最大回撤"""
    if not prices:
        return 0.0
    peak = prices[0]
    max_dd = 0.0
    for p in prices:
        if p > peak:
            peak = p
        dd = (peak - p) / peak * 100
        if dd > max_dd:
            max_dd = dd
    return round(max_dd, 2)


def calc_sharpe_ratio(prices: list, risk_free_rate: float = 0.03) -> float:
    """夏普比率（简化）"""
    if len(prices) < 2:
        return 0.0
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    if not returns:
        return 0.0
    mean_ret = sum(returns) / len(returns)
    std_ret = math.sqrt(sum((r - mean_ret) ** 2 for r in returns) / len(returns)) if len(returns) > 1 else 0
    if std_ret == 0:
        return 0.0
    sharpe = (mean_ret * 252 - risk_free_rate) / (std_ret * math.sqrt(252))
    return round(sharpe, 2)


def analyze_trend(prices: list, short_ma: int = 5, long_ma: int = 20) -> str:
    """判断趋势"""
    if len(prices) < long_ma:
        return "数据不足"
    ma_short = calc_ma(prices, short_ma)
    ma_long = calc_ma(prices, long_ma)
    if ma_short is None or ma_long is None:
        return "数据不足"
    if prices[-1] > ma_short > ma_long:
        return "上升趋势 📈"
    elif prices[-1] < ma_short < ma_long:
        return "下降趋势 📉"
    elif ma_short > ma_long:
        return "震荡偏强 ↗️"
    else:
        return "震荡偏弱 ↘️"


def analyze_fund(fund_code: str, history_data: list) -> dict:
    """
    对单只基金进行完整技术分析
    history_data: [{"date": "2024-01-01", "nav": 1.234, "change": 0.5}, ...]
    """
    if not history_data or len(history_data) < 10:
        return {"error": "历史数据不足"}

    prices = [d["nav"] for d in history_data]
    changes = [d.get("change", 0) for d in history_data]

    # 历史数据是按日期倒序的（最新在前），prices[0]是最新的
    latest_nav = prices[0]
    latest_date = history_data[0].get("date", "")
    latest_change = changes[0] if changes else 0

    ma5 = calc_ma(prices, 5)
    ma10 = calc_ma(prices, 10)
    ma20 = calc_ma(prices, 20)
    ma60 = calc_ma(prices, 60) if len(prices) >= 60 else None

    rsi14 = calc_rsi(prices, 14)
    dif, dea, macd_hist = calc_macd(prices)
    k, d, j = calc_stochastics(prices, prices, prices) if len(prices) >= 14 else (None, None, None)
    boll_upper, boll_mid, boll_lower = calc_bollinger_bands(prices, 20)

    trend = analyze_trend(prices)
    volatility = calc_volatility(prices)
    max_drawdown = calc_max_drawdown(prices)
    sharpe = calc_sharpe_ratio(prices)
    var_95 = calc_var(prices, 0.95)
    sortino = calc_sortino_ratio(prices)
    calmar = calc_calmar_ratio(prices)

    # 近1周/1月/3月/6月/1年收益率
    def period_return(days):
        if len(prices) < days + 1:
            return None
        try:
            return round((prices[0] - prices[days]) / prices[days] * 100, 2)
        except (IndexError, ZeroDivisionError):
            return None

    return {
        "code": fund_code,
        "prices": prices,
        "changes": changes,
        "latest_nav": latest_nav,
        "latest_date": latest_date,
        "latest_change": latest_change,
        "ma5": round(ma5, 4) if ma5 else None,
        "ma10": round(ma10, 4) if ma10 else None,
        "ma20": round(ma20, 4) if ma20 else None,
        "ma60": round(ma60, 4) if ma60 else None,
        "rsi14": round(rsi14, 2) if rsi14 else None,
        "macd_dif": dif,
        "macd_dea": dea,
        "macd_hist": macd_hist,
        "kdj_k": k,
        "kdj_d": d,
        "kdj_j": j,
        "boll_upper": boll_upper,
        "boll_middle": boll_mid,
        "boll_lower": boll_lower,
        "trend": trend,
        "volatility": volatility,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe,
        "var_95": var_95,
        "sortino_ratio": sortino,
        "calmar_ratio": calmar,
        "return_1w": period_return(5),
        "return_1m": period_return(22),
        "return_3m": period_return(66),
        "return_6m": period_return(126),
        "return_1y": period_return(252),
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from fund_api import fetch_otc_fund_history, fetch_otc_fund_valuation

    print("=== 测试技术分析 ===")
    valuation = fetch_otc_fund_valuation("161226")
    history = fetch_otc_fund_history("161226", days=90)
    if history:
        result = analyze_fund("161226", history)
        print({k: v for k, v in result.items() if k not in ["prices", "changes"]})
