#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""当日行情快照脚本（盘中实时版）

- 直接通过新浪行情 HTTP 接口 (hq.sinajs.cn) 获取实时盘口
- 支持代码或名称输入，返回单只 A 股/ETF 的盘中快照：
    - 最新价、涨跌幅、今开、最高、最低
    - 成交量、成交额（含全部原始字段，便于扩展）

说明：
- 使用的是盘口级实时数据，而非日线收盘数据；
- 更复杂的周+当天趋势判断，仍建议使用 analyze.py。
"""

from __future__ import annotations
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from typing import Any, Dict

# 确保可以导入同目录下的模块（如 sina_provider）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)


def _normalize_to_sina_symbol(symbol_or_name: str) -> str:
    """将用户输入统一转换为新浪实时接口使用的 sh/sz/bj 前缀代码。

    - 支持直接输入：600036 / sz159339 / sh600036 / bjXXXXXX
    - 对于中文名称，回退复用 sina_provider._to_sina_symbol 逻辑
    """

    s = symbol_or_name.strip()

    # 已带前缀
    if s.lower().startswith(("sh", "sz", "bj")) and len(s) >= 8:
        return s.lower()

    # 纯 6 位数字代码，按 A 股规则推断市场前缀
    if s.isdigit() and len(s) == 6:
        if s.startswith(("6", "9")):
            prefix = "sh"
        elif s.startswith(("0", "3")):
            prefix = "sz"
        elif s.startswith(("4", "8")):
            prefix = "bj"
        else:
            prefix = "sh"
        return f"{prefix}{s}"

    # 其他情况视为名称，复用 sina_provider 中的解析逻辑
    try:
        from sina_provider import _to_sina_symbol  # type: ignore

        return _to_sina_symbol(s)
    except Exception as err:  # noqa: BLE001
        raise ValueError(f"无法解析输入为有效 A 股代码或名称: {symbol_or_name}") from err


def _fetch_realtime_sina(symbols: list[str]) -> Dict[str, Dict[str, Any]]:
    """直接调用新浪 hq 实时接口，返回原始字段字典。

    返回结构：{symbol: {...}}，其中 symbol 形如 sh600036。
    """

    result: Dict[str, Dict[str, Any]] = {}
    if not symbols:
        return result

    codes_str = ",".join(symbols)
    url = f"https://hq.sinajs.cn/list={codes_str}"

    req = urllib.request.Request(
        url,
        headers={
            "Referer": "https://finance.sina.com.cn",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        },
    )

    resp = urllib.request.urlopen(req, timeout=10)
    text = resp.read().decode("gbk")

    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        # 形如: var hq_str_sh600036="名称,今开,昨收,现价,最高,最低,买一,卖一,成交量(股),成交额(元),...";
        match = re.match(r'var hq_str_(\w+)="([^"]*)"', line)
        if not match:
            continue

        symbol = match.group(1)
        data_str = match.group(2)
        if not data_str:
            continue

        fields = data_str.split(",")
        # 正常 A 股/ETF 返回字段至少 32 个
        if len(fields) < 32:
            continue

        try:
            name = fields[0]
            open_price = float(fields[1]) if fields[1] else float("nan")
            pre_close = float(fields[2]) if fields[2] else float("nan")
            price = float(fields[3]) if fields[3] else float("nan")
            high = float(fields[4]) if fields[4] else float("nan")
            low = float(fields[5]) if fields[5] else float("nan")
            volume_shares = int(float(fields[8])) if fields[8] else 0  # 股
            amount = float(fields[9]) if fields[9] else 0.0  # 元

            change_amt = price - pre_close if not any(
                map(lambda x: x != x, [price, pre_close])  # NaN 检测
            ) else float("nan")
            if not any(map(lambda x: x != x, [change_amt, pre_close])) and pre_close != 0:
                change_pct = (change_amt / pre_close) * 100.0
            else:
                change_pct = float("nan")

            trade_date = fields[30] if len(fields) > 30 and fields[30] else ""
            trade_time = fields[31] if len(fields) > 31 and fields[31] else ""
        except Exception:
            # 单行解析失败不影响其他标的
            continue

        result[symbol] = {
            "code": symbol[2:],  # 去掉 sh/sz/bj 前缀
            "name": name,
            "price": price,
            "open": open_price,
            "pre_close": pre_close,
            "high": high,
            "low": low,
            "volume": volume_shares,  # 成交量(股)
            "amount": amount,  # 成交额(元)
            "change_amt": change_amt,
            "change_pct": change_pct,
            "date": trade_date,
            "time": trade_time,
            "raw_fields": fields,
            "raw": data_str,
        }

    return result


def get_today_quote(symbol_or_name: str) -> Dict[str, Any]:
    """基于新浪实时接口，获取单只股票当前盘中行情快照。

    返回：最新价、涨跌幅、今开、最高、最低、成交量、成交额、换手率、总市值。
    """

    symbol_or_name = symbol_or_name.strip()

    # 统一转换为新浪实时接口需要的 symbol（sh/sz/bj 前缀）
    sina_symbol = _normalize_to_sina_symbol(symbol_or_name)

    try:
        realtime_map = _fetch_realtime_sina([sina_symbol])
    except Exception as err:  # noqa: BLE001
        raise RuntimeError(f"获取新浪实时盘口失败: {err}") from err

    data = realtime_map.get(sina_symbol)
    if not data:
        raise ValueError(f"在新浪实时行情接口中找不到股票: {symbol_or_name} ({sina_symbol})")

    code_val = str(data.get("code", sina_symbol[2:]))
    name_val = str(data.get("name", ""))
    price = float(data.get("price", float("nan")))
    change_pct = float(data.get("change_pct", float("nan")))
    open_price = float(data.get("open", float("nan")))
    high = float(data.get("high", float("nan")))
    low = float(data.get("low", float("nan")))
    volume = float(data.get("volume", float("nan")))  # 股
    amount = float(data.get("amount", float("nan")))  # 元

    trade_date = str(data.get("date") or datetime.now().strftime("%Y-%m-%d"))
    raw_fields = data.get("raw_fields") or []

    # 实时接口未直接给出换手率和总市值，这里保留字段但置为 NaN，
    # 以兼容之前返回结构；如后续需要可在此处补充自定义计算。
    turnover = float("nan")
    market_cap = float("nan")

    # 从原始字段中解析五档盘口（如可用）
    bids = []
    asks = []
    try:
        # 正常情况下 raw_fields 至少有 32 个元素
        if len(raw_fields) >= 32:
            for level in range(5):
                bid_vol_idx = 10 + 2 * level
                bid_prc_idx = 11 + 2 * level
                ask_vol_idx = 20 + 2 * level
                ask_prc_idx = 21 + 2 * level

                bid_volume = float(raw_fields[bid_vol_idx]) if raw_fields[bid_vol_idx] else 0.0
                bid_price = float(raw_fields[bid_prc_idx]) if raw_fields[bid_prc_idx] else float("nan")
                ask_volume = float(raw_fields[ask_vol_idx]) if raw_fields[ask_vol_idx] else 0.0
                ask_price = float(raw_fields[ask_prc_idx]) if raw_fields[ask_prc_idx] else float("nan")

                bids.append({"level": level + 1, "price": bid_price, "volume": bid_volume})
                asks.append({"level": level + 1, "price": ask_price, "volume": ask_volume})
    except Exception:
        # 盘口解析失败不影响主字段
        bids = []
        asks = []

    return {
        "code": code_val,
        "name": name_val,
        "date": trade_date,
        "price": price,
        "change_pct": change_pct,
        "open": open_price,
        "volume": volume,
        "high": high,
        "low": low,
        "amount": amount,
        "turnover": turnover,
        "market_cap": market_cap,
        "bids": bids,
        "asks": asks,
    }


def main() -> None:
    """命令行入口示例。

    示例：
      python today.py 招商银行
      python today.py 600036
      python today.py sz159339
    """

    import argparse

    parser = argparse.ArgumentParser(description="获取单只股票当日最新行情快照（JSON 输出）")
    parser.add_argument("symbol", help="股票代码或名称，例如 600036 / 招商银行 / sz159339")

    args = parser.parse_args()

    try:
        quote = get_today_quote(args.symbol)
    except Exception as e:  # noqa: BLE001
        print(f"获取当日行情失败: {e}")
        import traceback

        traceback.print_exc()
        return

    # 始终输出完整 JSON 字典（字段名 -> 数值）
    print(json.dumps(quote, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
