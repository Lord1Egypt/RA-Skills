#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
import re


INDEX_REALTIME = "INDEX_REALTIME"
KLINE_ANALYSIS = "KLINE_ANALYSIS"
KLINE_CHART = "KLINE_CHART"  # 新增：K线绘图
INTRADAY_ANALYSIS = "INTRADAY_ANALYSIS"
VOLUME_ANALYSIS = "VOLUME_ANALYSIS"  # 新增：分时量能分析
LIMIT_STATS = "LIMIT_STATS"
MONEY_FLOW = "MONEY_FLOW"
FUNDAMENTAL = "FUNDAMENTAL"
STOCK_OVERVIEW = "STOCK_OVERVIEW"
MARGIN_LHB = "MARGIN_LHB"
SECTOR_ANALYSIS = "SECTOR_ANALYSIS"
DERIVATIVES = "DERIVATIVES"
FUND_BOND = "FUND_BOND"
HK_US_MARKET = "HK_US_MARKET"
NEWS = "NEWS"
RESEARCH_REPORT = "RESEARCH_REPORT"
STOCK_PICK = "STOCK_PICK"
HELP = "HELP"  # 使用说明
PORTFOLIO = "PORTFOLIO"  # 持仓管理

@dataclass
class IntentObj:
    intent: str
    query: str
    symbol: Optional[str] = None
    target: Optional[str] = None
    date: Optional[str] = None
    period: Optional[str] = None
    top_n: Optional[int] = None


def _extract_symbol(query: str) -> Optional[str]:
    # A 股 6 位代码，允许 sh/sz/bj 前缀
    m = re.search(r"\b(?:sh|sz)?(\d{6})\b", query.lower())
    if m:
        return m.group(1)

    # 港股 5 位代码（无前缀）
    m = re.search(r"(?<!\d)(\d{5})(?!\d)", query)
    if m:
        return m.group(1)

    # 港股代码（HK 前缀）
    m = re.search(r"\bHK(\d{4,5})\b", query, re.IGNORECASE)
    if m:
        return f"HK{m.group(1)}"

    # 美股东财代码样式，如 105.TTE
    m = re.search(r"\b(\d{3}\.[A-Z]{1,10})\b", query)
    if m:
        return m.group(1)

    # 美股交易代码（支持 BRK.A）
    m = re.search(r"\b([A-Z]{1,6}(?:\.[A-Z])?)\b", query)
    if m:
        return m.group(1)

    return None


def _extract_target(query: str) -> Optional[str]:
    text = (query or "").strip()
    if not text:
        return None

    explicit_symbol = _extract_symbol(text)
    if explicit_symbol:
        return explicit_symbol

    cleaned = text
    cleanup_patterns = [
        r"\b\d{8}\b",
        r"\d{4}[-/]?\d{2}[-/]?\d{2}",
        r"最近\s*\d+\s*(日|天|周|月)",
        r"近\s*\d+\s*(日|天|周|月)",
        r"top\s*\d+",
        r"前\s*\d+\s*(名|条|个)?",
    ]
    for pattern in cleanup_patterns:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

    stop_words = [
        "实时", "行情", "大盘", "指数", "K线图", "k线图", "K线", "k线", "日线", "周线", "月线",
        "分时", "盘口", "逐笔", "量能", "放量", "缩量", "走势图", "趋势图", "分析", "看下", "评估", "综合",
        "资金流向", "资金流", "主力资金", "北向资金", "南向资金", "行业资金", "板块资金",
        "基本面", "财报", "财务", "市盈率", "市净率", "估值", "ROE", "roe", "毛利率", "净利率", "资产负债率",
        "融资融券", "龙虎榜", "两融", "融资余额", "融券余额", "研报", "研究报告", "机构评级",
        "财经新闻", "个股新闻", "新闻资讯", "新闻", "板块", "行业", "概念", "题材", "轮动",
        "涨幅榜", "跌幅榜", "港股", "美股", "基金", "净值", "可转债", "转债", "债券", "ETF", "etf",
        "期货", "期权", "衍生品", "主力合约", "帮助", "说明",
    ]
    for word in stop_words:
        cleaned = cleaned.replace(word, " ")

    cleaned = re.sub(r"[，。,.?？!！:：;；()（）\[\]{}<>《》/\\|_\-+]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return None

    candidates = re.findall(r"[A-Za-z]{1,10}(?:\.[A-Za-z])?|[\u4e00-\u9fff]{2,20}", cleaned)
    if not candidates:
        return None

    candidates = [item for item in candidates if item not in {"今天", "今日", "昨天", "昨日"}]
    if not candidates:
        return None

    return max(candidates, key=len)


def _extract_date(query: str) -> Optional[str]:
    m = re.search(r"\b(\d{8})\b", query)
    if m:
        d = m.group(1)
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"

    m = re.search(r"(\d{4})[-/]?(\d{2})[-/]?(\d{2})", query)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    if "今天" in query or "今日" in query:
        return datetime.now().strftime("%Y-%m-%d")
    if "昨天" in query or "昨日" in query:
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    return None


def _extract_period(query: str) -> Optional[str]:
    q = query.lower()
    if "1m" in q or "1分钟" in query:
        return "1"
    if "5m" in q or "5分钟" in query:
        return "5"
    if "15m" in q or "15分钟" in query:
        return "15"
    if "30m" in q or "30分钟" in query:
        return "30"
    if "60m" in q or "60分钟" in query:
        return "60"
    if "周线" in query or "week" in q:
        return "weekly"
    if "月线" in query or "month" in q:
        return "monthly"
    if "日线" in query or "day" in q or "daily" in q:
        return "daily"

    return None


def _extract_top_n(query: str) -> Optional[int]:
    m = re.search(r"top\s*(\d+)", query.lower())
    if m:
        return int(m.group(1))

    m = re.search(r"前\s*(\d+)\s*(名|条|个)?", query)
    if m:
        return int(m.group(1))

    # 支持"近N日"、"最近N天"等
    m = re.search(r"近\s*(\d+)\s*(日|天|周|月)", query)
    if m:
        return int(m.group(1))
    m = re.search(r"最近\s*(\d+)\s*(日|天|周|月)", query)
    if m:
        return int(m.group(1))

    return None


def _classify_intent(query: str) -> str:
    q = query.lower()

    if any(k in query for k in ["涨停", "跌停", "涨跌停"]):
        return LIMIT_STATS
    if any(k in query for k in ["推荐股票", "选股", "股票推荐", "有什么股票推荐"]):
        return STOCK_PICK
    if any(k in query for k in ["分时", "盘口", "逐笔"]):
        return INTRADAY_ANALYSIS
    # 分时量能分析
    if any(k in query for k in ["量能", "放量", "缩量", "主力动向", "抢筹", "出货", "封单", "分时量能"]):
        return VOLUME_ANALYSIS
    if any(k in query for k in ["k线", "K线", "日线", "周线", "月线"]) or "kline" in q:
        return KLINE_ANALYSIS
    # 绘图功能：K线图、走势、行情图
    if any(k in query for k in ["走势图", "趋势图", "行情图", "K线图", "k线图", "绘制", "画图", "图"]):
        return KLINE_CHART
    if any(k in query for k in ["怎么样", "分析", "看下", "评估", "综合"]):
        return STOCK_OVERVIEW
    if any(k in query for k in ["资金流", "主力资金", "北向资金", "南向资金", "东向资金", "行业资金", "板块资金"]):
        return MONEY_FLOW
    if any(k in query for k in ["基本面", "财报", "财务", "市盈率", "市净率", "估值", "roe", "ROE", "毛利率", "净利率", "资产负债率"]):
        return FUNDAMENTAL
    if any(k in query for k in ["融资融券", "龙虎榜", "两融", "融资余额", "融券余额"]):
        return MARGIN_LHB
    if any(k in query for k in ["研报", "研究报告", "机构评级"]):
        return RESEARCH_REPORT
    if any(k in query for k in ["财经新闻", "个股新闻", "新闻资讯", "新闻"]):
        return NEWS

    if any(k in query for k in ["港股", "美股", "纳斯达克", "道琼斯", "标普", "恒生", "恒指", "HK", "US"]):
        return HK_US_MARKET
    if any(k in query for k in ["期货", "期权", "衍生品", "主力合约", "if", "ih", "ic", "im"]):
        return DERIVATIVES
    if any(k in query for k in ["基金", "净值", "可转债", "转债", "债券", "etf", "ETF"]):
        return FUND_BOND
    if any(k in query for k in ["板块", "行业", "概念", "题材", "轮动", "涨幅榜", "跌幅榜"]):
        return SECTOR_ANALYSIS

    if any(k in query for k in ["大盘", "指数", "上证", "深证", "创业板", "实时", "行情"]):
        return INDEX_REALTIME

    # 使用说明
    if any(k in query for k in ["介绍股市", "股市怎么用", "使用说明", "帮助", "help", "说明", "玩法", "有哪些功能"]):
        return HELP

    # 持仓管理
    if any(k in query for k in ["持仓", "仓位", "我的股票"]):
        return PORTFOLIO

    return INDEX_REALTIME


def parse_query(query: str) -> IntentObj:
    query = (query or "").strip()
    return IntentObj(
        intent=_classify_intent(query),
        query=query,
        symbol=_extract_symbol(query),
        target=_extract_target(query),
        date=_extract_date(query),
        period=_extract_period(query),
        top_n=_extract_top_n(query),
    )
