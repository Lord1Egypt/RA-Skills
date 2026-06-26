#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""统一数据获取 + 指标计算脚本

流程：
- 优先通过新浪接口获取原始日线数据；
- 若新浪失败，则回退到腾讯接口；
- 在本模块内部计算 MA7/14/20/60、MACD(12,26,9)、RSI(14)。

注意：
- 下游原始行情模块（tencentdatafetch.py / xinlangdatafetch.py）禁止返回任何技术指标；
- 指标只在本脚本或策略脚本中计算和使用。
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta
from typing import Literal

import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
	sys.path.insert(0, ROOT_DIR)

PLAYGROUND_DIR = os.path.dirname(os.path.abspath(__file__))
if PLAYGROUND_DIR not in sys.path:
	sys.path.insert(0, PLAYGROUND_DIR)

from sina_provider import fetch_stock_daily_sina  # type: ignore
from tx_provider import fetch_stock_daily_tx  # type: ignore


def _calc_ma(df: pd.DataFrame, window: int) -> pd.Series:
	return df["收盘"].rolling(window=window, min_periods=window).mean()


def _calc_macd(
	close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> tuple[pd.Series, pd.Series, pd.Series]:
	ema_fast = close.ewm(span=fast, adjust=False).mean()
	ema_slow = close.ewm(span=slow, adjust=False).mean()
	dif = ema_fast - ema_slow
	dea = dif.ewm(span=signal, adjust=False).mean()
	macd = dif - dea
	return dif, dea, macd


def _calc_rsi(close: pd.Series, period: int = 14) -> pd.Series:
	delta = close.diff()
	gain = delta.where(delta > 0, 0.0)
	loss = -delta.where(delta < 0, 0.0)

	avg_gain = gain.rolling(window=period, min_periods=period).mean()
	avg_loss = loss.rolling(window=period, min_periods=period).mean()

	rs = avg_gain / avg_loss
	rsi = 100 - (100 / (1 + rs))
	return rsi


def fetch_with_fallback(
	symbol_or_name: str,
	start_date: str,
	end_date: str,
	adjust: str = "",
	prefer: Literal["sina", "tx"] = "sina",
) -> pd.DataFrame:
	"""优先使用指定数据源获取原始日线，不含任何技术指标，失败则自动切换到另一源。

	返回列：日期、开盘、收盘、最高、最低、成交量
	"""

	last_error: Exception | None = None

	sources: list[str]
	if prefer == "tx":
		sources = ["tx", "sina"]
	else:
		sources = ["sina", "tx"]

	for src in sources:
		try:
			if src == "sina":
				print("尝试通过新浪获取原始数据...")
				df = fetch_stock_daily_sina(
					symbol_or_name=symbol_or_name,
					start_date=start_date,
					end_date=end_date,
					adjust=adjust,
				)
			else:
				print("尝试通过腾讯获取原始数据...")
				df = fetch_stock_daily_tx(
					symbol_or_name=symbol_or_name,
					start_date=start_date,
					end_date=end_date,
					adjust=adjust,
				)

			expected_cols = {"日期", "开盘", "收盘", "最高", "最低", "成交量"}
			if not expected_cols.issubset(df.columns):
				raise ValueError(f"数据源 {src} 返回列不完整: {df.columns.tolist()}")

			print(f"使用数据源: {src}")
			return df.sort_values("日期").reset_index(drop=True)

		except Exception as e:  # noqa: BLE001
			print(f"通过 {src} 获取失败: {e}")
			last_error = e
			continue

	raise RuntimeError(f"新浪和腾讯数据源均获取失败: {last_error}")


def fetch_with_indicators(
	symbol_or_name: str,
	start_date: str,
	end_date: str,
	adjust: str = "",
	prefer: Literal["sina", "tx"] = "sina",
) -> pd.DataFrame:
	"""获取原始日线 + 在本函数中计算 MA/MACD/RSI 指标，并返回完整 DataFrame。"""

	df = fetch_with_fallback(
		symbol_or_name=symbol_or_name,
		start_date=start_date,
		end_date=end_date,
		adjust=adjust,
		prefer=prefer,
	)

	# 均线
	df["MA7"] = _calc_ma(df, 7)
	df["MA14"] = _calc_ma(df, 14)
	df["MA20"] = _calc_ma(df, 20)
	df["MA60"] = _calc_ma(df, 60)

	# MACD
	dif, dea, macd = _calc_macd(df["收盘"], fast=12, slow=26, signal=9)
	df["DIF"] = dif
	df["DEA"] = dea
	df["MACD"] = macd

	# RSI(14)
	df["RSI14"] = _calc_rsi(df["收盘"], period=14)

	return df


def main() -> None:
	"""简单命令行使用示例。

	示例：
	  1）指定起止日期：
	     python fetch.py 招商银行 --start 20250101 --end 20250320
	  2）按最近 N 天（默认 120 天）：
	     python fetch.py 招商银行 --days 120
	"""

	import argparse

	parser = argparse.ArgumentParser(description="获取原始数据并计算技术指标")
	parser.add_argument("symbol", help="股票代码或名称，例如 600036 / 招商银行 / sz159339")
	parser.add_argument("--start", help="开始日期，YYYYMMDD 或 YYYY-MM-DD")
	parser.add_argument("--end", help="结束日期，YYYYMMDD 或 YYYY-MM-DD")
	parser.add_argument(
		"--days",
		type=int,
		default=120,
		help="若未提供 start/end，则向前回溯的天数，默认 120 天",
	)
	parser.add_argument(
		"--prefer",
		choices=["sina", "tx"],
		default="sina",
		help="优先数据源，默认新浪",
	)
	parser.add_argument(
		"--adjust",
		choices=["", "qfq", "hfq"],
		default="",
		help="复权方式，默认不复权",
	)

	args = parser.parse_args()

	# 情况一：提供了 start + end -> 直接按起止日期拉取
	if args.start and args.end:
		start_str = args.start
		end_str = args.end
	else:
		# 情况二：按最近 N 天（默认 120 天）
		end_dt = datetime.now()
		start_dt = end_dt - timedelta(days=args.days)
		start_str = start_dt.strftime("%Y-%m-%d")
		end_str = end_dt.strftime("%Y-%m-%d")

	df = fetch_with_indicators(
		symbol_or_name=args.symbol,
		start_date=start_str,
		end_date=end_str,
		adjust=args.adjust,
		prefer=args.prefer,
	)

	print("\n获取并计算完成，字段如下：")
	print(df.columns.tolist())
	print("\n最后 10 行预览：")
	print(df.tail(10).to_string(index=False))

	# 将本次获取的数据保存为 CSV，方便后续验算
	safe_symbol = str(args.symbol).replace(" ", "")
	filename = f"fetch_{safe_symbol}_{start_str}_{end_str}.csv"
	output_path = os.path.join(PLAYGROUND_DIR, filename)
	df.to_csv(output_path, index=False, encoding="utf-8-sig")
	print(f"\n完整数据已保存到: {output_path}")


if __name__ == "__main__":
	main()
