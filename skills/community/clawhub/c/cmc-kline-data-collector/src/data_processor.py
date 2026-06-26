"""
Data Processor - 数据处理和输出
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from .models import KlineData


class DataProcessor:
    """数据处理类"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def filter(
        self,
        kline: KlineData,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days: Optional[int] = None,
    ) -> KlineData:
        """
        过滤数据

        Args:
            kline: 原始 K 线数据
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
            days: 最近 N 天（与 start_date 互斥）

        Returns:
            过滤后的 KlineData
        """
        if days is not None:
            return kline.filter_by_days(days)

        return kline.filter_by_date(start_date, end_date)

    def save_json(self, kline: KlineData, filename: Optional[str] = None) -> str:
        """保存为 JSON"""
        if filename is None:
            filename = f"{kline.symbol.lower()}_kline.json"

        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(kline.to_json(), f, indent=2, ensure_ascii=False)

        print(f"Saved JSON: {filepath}")
        return str(filepath)

    def save_csv(self, kline: KlineData, filename: Optional[str] = None) -> str:
        """保存为 CSV"""
        if filename is None:
            filename = f"{kline.symbol.lower()}_kline.csv"

        filepath = self.output_dir / filename
        rows = kline.to_csv_rows()

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(f"Saved CSV: {filepath}")
        return str(filepath)

    def save(self, kline: KlineData, format: str = "json", filename: Optional[str] = None) -> str:
        """保存数据（JSON 或 CSV）"""
        if format.lower() == "csv":
            return self.save_csv(kline, filename)
        return self.save_json(kline, filename)

    def print_summary(self, kline: KlineData):
        """打印数据摘要"""
        if not kline.quotes:
            print(f"{kline.symbol}: No data")
            return

        first = kline.quotes[0]
        last = kline.quotes[-1]

        print(f"\n{kline.symbol} K 线数据摘要:")
        print(f"  数据条数：{len(kline.quotes)}")
        print(f"  时间范围：{first.time_open[:10]} ~ {last.time_open[:10]}")
        print(f"  最新价格：${last.close:,.2f}")
        print(f"  最高价格：${max(q.high for q in kline.quotes):,.2f}")
        print(f"  最低价格：${min(q.low for q in kline.quotes):,.2f}")
