#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
A500 (159339) 日线数据获取脚本

❗ 本模块只负责"原始行情数据采集"，禁止返回任何技术指标或衍生指标。

返回字段：
- 日期
- 开盘
- 收盘
- 最高
- 最低
- 成交量

说明：
- MACD(12,26,9)、RSI(14)、MA(7/14/20/60) 等指标不在本模块计算
- 提供至少 14 天历史数据供策略模块计算指标
"""

import os
import sys
from datetime import datetime, timedelta

import pandas as pd

# 优先使用当前仓库中的 akshare 版本，避免系统已安装旧版本 BUG
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import akshare as ak


def _normalize_date(date_str: str) -> str:
    """接受 YYYYMMDD 或 YYYY-MM-DD，统一转成 YYYY-MM-DD 字符串。"""
    s = date_str.strip().replace("-", "")
    if len(s) != 8 or not s.isdigit():
        raise ValueError("日期格式必须是 YYYYMMDD 或 YYYY-MM-DD")
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"


def _to_tx_symbol(symbol_or_name: str) -> str:
    """将代码或名称统一转换为腾讯接口需要的 sz/sh/bj 前缀代码。"""
    s = symbol_or_name.strip()
    # 已经带市场前缀
    if s.startswith(("sh", "sz", "bj")) and len(s) >= 8:
        return s

    # 通过 A 股列表解析代码或名称
    info_df = ak.stock_info_a_code_name()
    row = info_df[(info_df["code"] == s) | (info_df["name"] == s)]
    if row.empty:
        raise ValueError(f"无法根据输入解析股票: {symbol_or_name}")

    code = row.iloc[0]["code"]
    if code.startswith(("6", "9")):
        prefix = "sh"
    elif code.startswith(("0", "3")):
        prefix = "sz"
    elif code.startswith(("4", "8")):
        prefix = "bj"
    else:
        raise ValueError(f"无法为代码 {code} 推断市场前缀")
    return f"{prefix}{code}"


def fetch_stock_daily_tx(
    symbol_or_name: str,
    start_date: str,
    end_date: str,
    adjust: str = "",
) -> pd.DataFrame:
    """通用腾讯日线原始数据接口（不含任何技术指标）。

    :param symbol_or_name: 股票代码(可带不带市场前缀)或股票名称，例如 "159339"、"sz159339"、"平安银行"
    :param start_date: 开始日期，格式 YYYYMMDD 或 YYYY-MM-DD
    :param end_date: 结束日期，格式 YYYYMMDD 或 YYYY-MM-DD
    :param adjust: 复权类型，""=不复权, "qfq"=前复权, "hfq"=后复权
    :return: 原始 OHLCV 数据 DataFrame，列为 ["日期", "开盘", "收盘", "最高", "最低", "成交量"]
    """
    symbol = _to_tx_symbol(symbol_or_name)
    start_str = _normalize_date(start_date)
    end_str = _normalize_date(end_date)

    print(f"调用腾讯接口获取数据: {symbol}, {start_str} -> {end_str} ...")
    df = ak.stock_zh_a_hist_tx(
        symbol=symbol,
        start_date=start_str,
        end_date=end_str,
        adjust=adjust,
        timeout=30,
    )
    # 接口当前返回的列名为英文: ["date", "open", "close", "high", "low", "amount"]
    # 为了与脚本注释保持一致，这里统一映射成中文列名
    result = df[["date", "open", "close", "high", "low", "amount"]].copy()
    result.rename(
        columns={
            "date": "日期",
            "open": "开盘",
            "close": "收盘",
            "high": "最高",
            "low": "最低",
            "amount": "成交量",
        },
        inplace=True,
    )
    return result


def fetch_a500_daily(
    symbol: str = "sz159339",
    days: int = 120,
    adjust: str = "",
) -> pd.DataFrame:
    """获取 A500 日线原始数据（不含任何技术指标）- 腾讯接口

    :param symbol: 带市场标识的代码，默认 sz159339 (A500)
                   sz=深圳, sh=上海
    :param days: 获取天数，默认 30 天（确保有足够数据计算指标）
    :param adjust: 复权类型，""=不复权, "qfq"=前复权, "hfq"=后复权
    :return: 原始 OHLCV 数据
    :rtype: pd.DataFrame
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    try:
        return fetch_stock_daily_tx(
            symbol_or_name=symbol,
            start_date=start_str,
            end_date=end_str,
            adjust=adjust,
        )
    except Exception:
        print("获取数据失败，详细异常如下：")
        import traceback

        traceback.print_exc()
        raise


def main():
    """命令行入口。

     用法示例：
        1）通用拉取：
            python tencentdatafetch.py -s 159339 -b 20250101 -e 20250201 -a qfq

        2）仅指定代码，回溯 N 天（默认最近 120 天）：
            python tencentdatafetch.py -s 159339 -d 60
    """

    import argparse

    parser = argparse.ArgumentParser(description="腾讯日线原始数据获取脚本")
    parser.add_argument(
        "-s",
        "--symbol",
        help="股票代码或名称，例如 159339、sz159339、平安银行，必填",
    )
    parser.add_argument(
        "-b",
        "--start",
        help="开始日期，格式 YYYYMMDD 或 YYYY-MM-DD",
    )
    parser.add_argument(
        "-e",
        "--end",
        help="结束日期，格式 YYYYMMDD 或 YYYY-MM-DD",
    )
    parser.add_argument(
        "-a",
        "--adjust",
        choices=["", "qfq", "hfq"],
        default="",
        help="复权类型：空=不复权, qfq=前复权, hfq=后复权，默认不复权",
    )
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        default=120,
        help="若未提供 start/end，则向前回溯的天数，默认 120 天",
    )

    args = parser.parse_args()

    # 情况一：提供了 symbol + start + end -> 走通用接口
    if args.symbol and args.start and args.end:
        symbol_label = args.symbol
        print(
            f"正在获取 {symbol_label} 日线原始数据: {args.start} -> {args.end}, adjust={args.adjust} ..."
        )
        try:
            df = fetch_stock_daily_tx(
                symbol_or_name=args.symbol,
                start_date=args.start,
                end_date=args.end,
                adjust=args.adjust,
            )
        except Exception as e:
            print(f"获取数据时出错: {e}")
            import traceback

            traceback.print_exc()
            return None

    # 情况二：未提供完整起止日期，走“最近 N 天”逻辑
    else:
        if not args.symbol:
            print("错误：必须通过 -s/--symbol 指定股票代码或名称")
            return None
        symbol_label = args.symbol
        print(
            f"正在获取 {symbol_label} 最近 {args.days} 天日线原始数据, adjust={args.adjust} ..."
        )
        try:
            df = fetch_a500_daily(symbol=symbol_label, days=args.days, adjust=args.adjust)
        except Exception as e:
            print(f"获取数据时出错: {e}")
            import traceback

            traceback.print_exc()
            return None

    # 通用打印逻辑
    print(f"\n获取成功！共 {len(df)} 条数据")
    print("\n数据字段:", df.columns.tolist())

    print("\n" + "=" * 70)
    print(f"日线原始数据预览 ({symbol_label})")
    print("=" * 70)
    print(df.tail(10).to_string(index=False))

    print("\n最近 7 天数据（用于策略）:")
    recent = df.tail(7)
    print(recent.to_dict(orient="records"))

    return df


if __name__ == "__main__":
    main()
