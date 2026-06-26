"""语义接口 - 自然语言查询路由"""
from __future__ import annotations
import re, logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

_NAME_MAP = {"招商银行":"600036.SH","中国平安":"601318.SH","平安银行":"000001.SZ","宁德时代":"300750.SZ","澜起科技":"688008.SH",
    "贵州茅台":"600519.SH","比亚迪":"002594.SZ","工商银行":"601398.SH","建设银行":"601939.SH","中信证券":"600030.SH","东方财富":"300059.SZ"}
_CODE_PATTERN = re.compile(r"\b(\d{6}\.(SH|SZ|HK))\b")
_SHORT_CODE = re.compile(r"\b(\d{6})\b")

def _resolve_code(text):
    m = _CODE_PATTERN.search(text)
    if m: return m.group(1)
    for name, code in _NAME_MAP.items():
        if name in text: return code
    m = _SHORT_CODE.search(text)
    if m: return f"{m.group(1)}.SH" if m.group(1).startswith("6") else f"{m.group(1)}.SZ"
    return None

def _resolve_codes(text):
    codes = [m.group(1) for m in _CODE_PATTERN.finditer(text)]
    if not codes:
        for name, code in _NAME_MAP.items():
            if name in text: codes.append(code)
    return list(set(codes))

_INTENT_PATTERNS = [
    ("full_review",["复盘","今日分析","大盘分析","市场分析","全面分析"]),
    ("analyze_market",["大盘","市场","指数","上证","行情怎么样"]),
    ("get_quote",["行情","价格","报价","现价","多少钱"]),
    ("analyze_stock",["分析","技术面","信号","买不买","能不能买","怎么看","走势"]),
    ("get_money_flow",["资金","主力","流入","流出","资金流向"]),
    ("get_sector_flow",["板块","行业","热门板块"]),
    ("get_dragon_tiger",["龙虎榜","游资","机构"]),
    ("get_positions",["持仓","仓位","我的股票"]),
    ("get_market_breadth",["涨跌","赚钱效应","广度"]),
    ("circuit_breaker_check",["熔断","极端","暴跌"]),
]

def _detect_intent(text):
    text_lower = text.lower()
    scores = {}
    for intent, keywords in _INTENT_PATTERNS:
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0: scores[intent] = score
    if not scores: return "analyze_stock" if _resolve_code(text) else "full_review"
    return max(scores, key=scores.get)

def _extract_params(text, intent):
    params = {}
    if intent in ("get_quote","analyze_stock","get_money_flow","get_signal_history"):
        code = _resolve_code(text)
        if code: params["code"] = code
    if intent == "get_signal_history":
        m = re.search(r"(\d+)\s*天", text)
        if m: params["days"] = int(m.group(1))
    if intent == "full_review":
        codes = _resolve_codes(text)
        if codes: params["watchlist"] = codes
    return params

def parse_query(text: str) -> Tuple[str, Dict[str, Any]]:
    intent = _detect_intent(text)
    params = _extract_params(text, intent)
    return intent, params

def execute_query(text, tools):
    tool_name, params = parse_query(text)
    method = getattr(tools, tool_name, None)
    if not method: return {"error": f"未知工具: {tool_name}"}
    try: return method(**params)
    except Exception as e: return {"error": str(e)}
