"""
数据库管理器 — 通过 WebAPI HTTP 接口访问
技能包唯一依赖的端点：POST /api/klineanalyze, POST /api/screen

可用端点：
  POST /klineanalyze    → 全量分析（含准确率/规律/预测/信号/技术指标）
  POST /screen          → 选股筛选（方向/评分/准确率条件过滤）
"""
import requests
from typing import Optional, Any
from . import config

_session = requests.Session()
_session.headers.update({
    "User-Agent": "ghdataskill/1.0",
    "Content-Type": "application/json",
})


def _url(path: str) -> str:
    return f"{config.WEBAPI_BASE_URL}/{path.lstrip('/')}"


def _post(path: str, json_body: dict = None) -> Optional[Any]:
    try:
        resp = _session.post(_url(path), json=json_body or {}, timeout=config.TIMEOUT)
        if resp.status_code not in (200, 201):
            return None
        data = resp.json()
        if isinstance(data, dict):
            return data.get("result", data)
        return data
    except Exception as e:
        print(f"[db] POST {path} 失败: {e}")
        return None


# ===== 核心分析接口（唯一依赖）=====

def kline_analyze(code: str, today_kline: dict = None) -> dict:
    """
    POST /klineanalyze — 全量分析
    服务端计算：技术指标 + 信号 + 规律 + 预测 + 准确率 + 学习摘要
    这是技能包唯一调用的WebAPI接口
    自动传入全局APIKey用于验证
    """
    body = {"code": code}
    if config.API_KEY:
        body["apiKey"] = config.API_KEY
    if today_kline:
        body["todayKline"] = today_kline
    data = _post("klineanalyze", body)
    if data and isinstance(data, dict):
        # 新格式：{ data: {...}, apiKeyInfo: { remaining, ... } }
        inner = data.get("data")
        if inner is not None:
            return inner
        return data
    return {}


# ===== 准确率统计 =====

def get_accuracy_stats(code: str, days: int = 36500) -> dict:
    """
    从 klineanalyze 响应中提取方向准确率
    accuracy 结构: { all:{total,correct,rate}, period30:{...}, period60:{...} }
    """
    result = kline_analyze(code)
    acc = result.get("accuracy", {})

    if days >= 36500:
        stats = acc.get("all", {})
    elif days >= 60:
        stats = acc.get("period60", {})
    else:
        stats = acc.get("period30", {})

    if stats:
        return {
            "total": stats.get("total", 0),
            "correct": stats.get("correct", 0),
            "rate": round(stats.get("rate", 0), 1),
        }
    return {"total": 0, "correct": 0, "rate": 0}


# ===== 最新预测 =====

def get_predictions(code: str, limit: int = 30) -> list:
    """从 klineanalyze 提取最新预测"""
    result = kline_analyze(code)
    lp = result.get("latestPrediction", {}) or {}
    if lp:
        return [{
            "predict_date": lp.get("predictDate", ""),
            "direction": lp.get("direction", ""),
            "total_score": lp.get("totalScore", 0),
            "range_forecast": lp.get("rangeForecast", ""),
            "t1_direction": lp.get("t1Direction", ""),
            "t2_direction": lp.get("t2Direction", ""),
            "weekly_direction": lp.get("weeklyDirection", ""),
            "vote_detail": lp.get("voteDetail", ""),
        }]
    return []


# ===== 规律数据 =====

def get_patterns(code: str) -> list:
    """从 klineanalyze 提取规律"""
    result = kline_analyze(code)
    patterns = result.get("patterns", [])
    if patterns and isinstance(patterns, list):
        return [{
            "pattern_type": p.get("name", ""),
            "description": p.get("advice", ""),
            "avg_d3": p.get("avgD3", ""),
            "samples": p.get("samples", []),
        } for p in patterns]
    return []


def get_learning_summary(code: str) -> list:
    """从 klineanalyze 提取自学习摘要"""
    result = kline_analyze(code)
    return result.get("learningSummary", []) or []


# ===== 经验数据 =====

def get_experience(code: str) -> Optional[dict]:
    """从 klineanalyze 结果中提取经验摘要"""
    result = kline_analyze(code)
    if result:
        return {
            "stock_code": code,
            "stock_name": result.get("name", ""),
            "direction": result.get("latestPrediction", {}).get("direction", ""),
            "total_score": result.get("latestPrediction", {}).get("totalScore", 0),
            "accuracy_rate": result.get("accuracy", {}).get("all", {}).get("rate", 0),
        }
    return None


# ===== 选股筛选 =====

def screen_stocks(directions: list = None, min_score: float = None,
                  min_accuracy: float = None, min_correct_count: int = None,
                  sort_by: str = "score", top: int = 20, page: int = 1) -> dict:
    """
    POST /api/screen — 选股筛选
    基于 experience + accuracy_tracking 表筛选符合条件的股票

    参数:
        directions:     方向过滤，如 ["偏多","震荡偏多"]（不传查全部）
        min_score:      最低综合评分（0-10）
        min_accuracy:   最低准确率（%，如 60）
        min_correct_count: 最少正确次数
        sort_by:        排序字段：score(默认) / accuracy
        top:            每页条数，默认20
        page:           页码，默认1

    返回:
        { total: 总数, page: 页码, top: 每页条数,
          stocks: [{ code, name, direction, score, accuracy }] }

    示例:
        >>> screen_stocks(directions=["偏多"], min_score=5.0, min_accuracy=60, top=10)
    """
    body = {"top": top, "page": page, "sortBy": sort_by}
    if directions:
        body["directions"] = directions
    if min_score is not None:
        body["minScore"] = min_score
    if min_accuracy is not None:
        body["minAccuracy"] = min_accuracy
    if min_correct_count is not None:
        body["minCorrectCount"] = min_correct_count
    if config.API_KEY:
        body["apiKey"] = config.API_KEY

    data = _post("screen", body)
    if data and isinstance(data, dict):
        inner = data.get("data")
        if inner is not None:
            return inner
        return data
    return {"total": 0, "page": page, "top": top, "stocks": []}


def advanced_screen(mode: str = "momentum", base_directions: list = None,
                    base_min_score: float = None, base_min_accuracy: float = None,
                    momentum_chg20: float = None, momentum_ma_only: bool = False,
                    reversal_rsi: float = None, reversal_oversold: bool = False,
                    tech_ma_bullish: bool = False, tech_macd_golden: bool = False,
                    tech_vol_surge: bool = False,
                    sort_by: str = "score", top: int = 20) -> dict:
    """
    POST /api/screen/advanced — 高级选股（动量/反转/技术信号）

    参数:
        mode: "momentum"(动量) / "reversal"(反转) / "techsignal"(技术信号)
        base_directions: 基础方向过滤
        base_min_score: 基础最低评分
        base_min_accuracy: 基础最低准确率
        momentum_chg20: 最低近20日涨幅(%)
        momentum_ma_only: 仅均线多头
        reversal_rsi: RSI低于此值
        reversal_oversold: 超卖+MACD金叉
        tech_ma_bullish: 均线多头
        tech_macd_golden: MACD金叉
        tech_vol_surge: 放量
        sort_by: score / chg20 / rsi
        top: 最多返回条数

    返回:
        { total: 总数, stocks: [{ code, name, direction, score, accuracy,
          maStatus, chg20, rsi14, macdBar, volRatio, matchReasons }] }
    """
    body = {"mode": mode, "top": top, "sortBy": sort_by}
    if base_directions: body["baseDirections"] = base_directions
    if base_min_score is not None: body["baseMinScore"] = base_min_score
    if base_min_accuracy is not None: body["baseMinAccuracy"] = base_min_accuracy
    if momentum_chg20 is not None: body["momentumChg20"] = momentum_chg20
    if momentum_ma_only: body["momentumMAOnly"] = True
    if reversal_rsi is not None: body["reversalRSI"] = reversal_rsi
    if reversal_oversold: body["reversalOversold"] = True
    if tech_ma_bullish: body["techMABullish"] = True
    if tech_macd_golden: body["techMACDGolden"] = True
    if tech_vol_surge: body["techVolSurge"] = True
    if config.API_KEY:
        body["apiKey"] = config.API_KEY

    data = _post("screen/advanced", body)
    if data and isinstance(data, dict):
        inner = data.get("data")
        return inner if inner is not None else data
    return {"total": 0, "stocks": []}
