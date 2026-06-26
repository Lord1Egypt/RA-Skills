#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""当日行情快照脚本（盘中实时版）

- 基于新浪实时接口 ``stock_zh_a_spot`` 获取当前盘中行情
- 按代码或名称筛选单只股票，输出：
    - 最新价、涨跌幅、成交量、最高、最低

说明：
- 使用的是新浪盘口实时数据，而非日线收盘数据；
- 更复杂的周+当天趋势判断，仍建议使用 analyze.py。
"""

from __future__ import annotations
import os
import sys
from datetime import datetime
from typing import Dict, Any

# 确保可以导入同目录下的 fetch 模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import time

import akshare as ak  # type: ignore


def _get_realtime_df(max_retries: int = 3) -> Any:
    """使用新浪实时接口获取全市场盘口数据，带简单重试。"""

    last_err: Exception | None = None

    for i in range(max_retries):
        try:
            return ak.stock_zh_a_spot()
        except Exception as err:  # noqa: BLE001
            last_err = err
            if i < max_retries - 1:
                time.sleep(1)

    if last_err is not None:
        raise last_err
    raise RuntimeError("获取新浪实时行情失败，且未捕获到具体异常")


def get_today_quote(symbol_or_name: str) -> Dict[str, Any]:
    """基于新浪实时接口，获取单只股票当前盘中行情快照。

    返回：最新价、涨跌幅、成交量、最高、最低。
    """

    symbol_or_name = symbol_or_name.strip()
    df = _get_realtime_df()

    # 规范化代码：接口内部代码为 6 位数字或带前缀（如 sz000001）
    code: str | None = None
    if symbol_or_name.startswith(("sh", "sz", "bj")) and len(symbol_or_name) >= 8:
        code = symbol_or_name[2:8]
    elif symbol_or_name.isdigit() and len(symbol_or_name) == 6:
        code = symbol_or_name

    row = None
    if code is not None and "代码" in df.columns:
        # 同时兼容 6 位数字代码和带前缀代码（如 sz000001）
        code_series = df["代码"].astype(str)
        candidate = df[(code_series == code) | (code_series.str[-6:] == code)]
        if not candidate.empty:
            row = candidate.iloc[0]

    # 回退：按名称精确匹配
    if row is None:
        candidate = df[df["名称"] == symbol_or_name]
        if not candidate.empty:
            row = candidate.iloc[0]

    if row is None:
        raise ValueError(f"在东财实时行情列表中找不到股票: {symbol_or_name}")

    code_val = str(row.get("代码"))
    name_val = str(row.get("名称"))
    price = float(row.get("最新价")) if row.get("最新价") is not None else float("nan")
    # 东财接口返回的涨跌幅已经是百分比单位
    change_pct = float(row.get("涨跌幅")) if row.get("涨跌幅") is not None else float("nan")
    volume = float(row.get("成交量")) if row.get("成交量") is not None else float("nan")
    high = float(row.get("最高")) if row.get("最高") is not None else float("nan")
    low = float(row.get("最低")) if row.get("最低") is not None else float("nan")
    trade_date = datetime.now().strftime("%Y-%m-%d")

    return {
        "code": code_val,
        "name": name_val,
        "date": trade_date,
        "price": price,
        "change_pct": change_pct,
        "volume": volume,
        "high": high,
        "low": low,
    }


def main() -> None:
    """命令行入口示例。

    示例：
      python today.py 招商银行
      python today.py 600036
      python today.py sz159339
    """

    import argparse

    parser = argparse.ArgumentParser(description="获取单只股票当日最新行情快照")
    parser.add_argument("symbol", help="股票代码或名称，例如 600036 / 招商银行 / sz159339")

    args = parser.parse_args()

    try:
        quote = get_today_quote(args.symbol)
    except Exception as e:  # noqa: BLE001
        print(f"获取当日行情失败: {e}")
        import traceback

        traceback.print_exc()
        return

    direction = "flat"
    if quote["change_pct"] > 0:
        direction = "up"
    elif quote["change_pct"] < 0:
        direction = "down"

    print("今日/最近交易日行情快照：")
    print(f"代码/名称: {quote['code']} / {quote['name']}")
    print(f"交易日期 : {quote['date']}")
    print(f"最新价   : {quote['price']}")
    print(f"涨跌幅   : {quote['change_pct']}% ({direction})")
    print(f"成交量   : {quote['volume']}")
    print(f"最高价   : {quote['high']}")
    print(f"最低价   : {quote['low']}")


if __name__ == "__main__":
    main()
