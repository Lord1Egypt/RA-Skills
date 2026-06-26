#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Skill 入口

普通用户使用本文件。不需要安装 akshare / pandas / docker 等任何依赖。
本文件通过 HTTP 请求将意图发送至云端 akshare 数据服务，然后格式化输出。

使用方式：
  python3 main.py --query "茅台最近30天K线"
  python3 main.py --query "今日涨停统计"
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Any, Dict, Optional

from router import (
    DERIVATIVES,
    FUND_BOND,
    FUNDAMENTAL,
    HK_US_MARKET,
    INDEX_REALTIME,
    INTRADAY_ANALYSIS,
    KLINE_ANALYSIS,
    KLINE_CHART,
    LIMIT_STATS,
    MARGIN_LHB,
    MONEY_FLOW,
    NEWS,
    RESEARCH_REPORT,
    SECTOR_ANALYSIS,
    STOCK_OVERVIEW,
    STOCK_PICK,
    VOLUME_ANALYSIS,
    HELP,
    PORTFOLIO,
    parse_query,
    IntentObj,
)


DEFAULT_SERVICE_URL = "https://akshare.devtool.uk"
DEFAULT_SERVICE_TIMEOUT = int(os.getenv("OPENCLAW_SERVICE_TIMEOUT", "90"))


# ---------------------------------------------------------------------------
# 从云端服务获取数据
# ---------------------------------------------------------------------------

def call_service(service_url: str, intent_obj: IntentObj, timeout: int = DEFAULT_SERVICE_TIMEOUT) -> Dict[str, Any]:
    """向云端数据服务发送请求，返回原始数据字典。"""
    payload = {
        "intent": intent_obj.intent,
        "query": intent_obj.query or "",
        "symbol": intent_obj.symbol,
        "target": intent_obj.target,
        "date": intent_obj.date,
        "period": intent_obj.period,
        "top_n": intent_obj.top_n,
    }
    data = json.dumps(payload).encode("utf-8")
    url = service_url.rstrip("/") + "/query"

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"ok": False, "error": f"HTTP {e.code}: {body[:300]}"}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# 本地处理（不依赖云端服务的部分）
# ---------------------------------------------------------------------------

def _handle_help() -> Dict[str, Any]:
    return {
        "ok": True,
        "source": "help",
        "text": """📈 A股分析 Skill 使用指南

| 类型 | 示例 |
|------|------|
| 大盘 | A股大盘、上证指数 |
| 分时量能 | 茅台量能分析、600519放量分析 |
| K线 | 茅台近30日K线、600519周线 |
| K线图 | 茅台走势图、宁德时代K线图 |
| 涨跌停 | 今日涨停、跌停统计 |
| 资金流 | 茅台资金流向、市场资金流向 |
| 基本面 | 茅台财务指标、ROE |
| 个股综合 | 茅台怎么样、宁德时代分析 |
| 板块 | 行业板块涨跌、概念板块涨跌 |
| 股票推荐 | 推荐股票、半导体股票推荐 |
| 基金/可转债 | 基金净值、可转债行情 |
| 港股/美股 | 港股行情、英伟达美股 |
| 新闻 | 财经新闻、宁德时代研报 |

直接发给我就能查~""",
    }


def _handle_portfolio(intent_obj: IntentObj) -> Dict[str, Any]:
    """持仓管理在本地处理，不需要云端服务。"""
    import subprocess
    import re

    portfolio_script = os.path.join(os.path.dirname(__file__), "..", "a-stock-analysis", "scripts", "portfolio.py")
    query = intent_obj.query or ""

    if "添加" in query or "add" in query.lower():
        code_match = re.search(r"\b(\d{6})\b", query)
        cost_match = re.search(r"--?cost\s*(\d+\.?\d*)", query)
        qty_match = re.search(r"--?qty\s*(\d+)") or re.search(r"数量\s*(\d+)", query)
        if code_match and cost_match and qty_match:
            result = subprocess.run(
                ["python3", portfolio_script, "add",
                 code_match.group(1), "--cost", cost_match.group(1), "--qty", qty_match.group(1)],
                capture_output=True, text=True, timeout=10,
            )
            return {"ok": True, "source": "portfolio", "text": result.stdout or "已添加持仓"}
        return {"ok": False, "error": "请输入：添加持仓 代码 --cost 成本价 --qty 数量\n例如：添加持仓 600519 --cost 10.5 --qty 1000"}

    if "分析" in query:
        result = subprocess.run(
            ["python3", portfolio_script, "analyze"],
            capture_output=True, text=True, timeout=60,
        )
        return {"ok": True, "source": "portfolio", "text": result.stdout or "暂无持仓"}

    if "删除" in query or "移除" in query:
        code_match = re.search(r"\b(\d{6})\b", query)
        if code_match:
            result = subprocess.run(
                ["python3", portfolio_script, "remove", code_match.group(1)],
                capture_output=True, text=True, timeout=10,
            )
            return {"ok": True, "source": "portfolio", "text": result.stdout or "已删除"}
        return {"ok": False, "error": "请输入要删除的股票代码"}

    result = subprocess.run(
        ["python3", portfolio_script, "show"],
        capture_output=True, text=True, timeout=10,
    )
    return {"ok": True, "source": "portfolio", "text": result.stdout or "暂无持仓"}


# ---------------------------------------------------------------------------
# 输出格式化
# ---------------------------------------------------------------------------

def _render(intent_obj: IntentObj, result: Dict[str, Any]) -> str:
    from formatter import render_output
    return render_output(intent_obj, result, platform="qq")


# ---------------------------------------------------------------------------
# 主逻辑
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="A股分析 Skill（云端服务版）")
    parser.add_argument("--query", required=True, help="自然语言请求，例如：分析 600519 最近 30 天 K线")
    parser.add_argument("--platform", default="qq", choices=["qq", "telegram"], help="输出平台")
    args = parser.parse_args()

    intent_obj = parse_query(args.query)

    # HELP 和 PORTFOLIO 本地处理，不需要云端
    if intent_obj.intent == HELP:
        result = _handle_help()
    elif intent_obj.intent == PORTFOLIO:
        result = _handle_portfolio(intent_obj)
    else:
        result = call_service(DEFAULT_SERVICE_URL, intent_obj)

    try:
        output = _render(intent_obj, result)
    except Exception:
        # formatter 不存在或报错时直接输出 JSON
        ok = result.get("ok", False)
        if ok:
            output = json.dumps(result, ensure_ascii=False, indent=2)
        else:
            output = f"⚠️ 错误: {result.get('error', '未知错误')}"

    print(output)


if __name__ == "__main__":
    main()