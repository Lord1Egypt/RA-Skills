#!/usr/bin/env python3
"""
从 furcas.csv 读取数据，生成导入飞书多维表格的 JSON 批处理文件。
每批 ≤ 15 条，适配 feishu_bitable_app_table_record 工具的 batch_create。

用法:
    python scripts/generate_batches.py --csv /workspace/furcas.csv --output-dir /workspace --batch-size 15
"""

import csv
import json
import os
import sys
import argparse

FIELD_MAP = {
    "问题描述": "文本",
    "问题链接": "问题链接",
    "工单状态/修复情况": "工单状态|修复情况",
    "问题原因": "问题原因",
    "责任人": "责任人",
    "解决类别": "解决类别",
    "解决模块": "解决模块",
    "超时时间": "超时时间",
    "超时备注": "超时备注",
}


def convert_row(row):
    """将 CSV 的一行转换为多维表格的 fields 字典"""
    fields = {}
    for csv_key, bitable_key in FIELD_MAP.items():
        val = row.get(csv_key, "").strip()
        if bitable_key == "问题链接" and val:
            fields[bitable_key] = {"link": val, "text": "查看工单"}
        else:
            fields[bitable_key] = val
    return fields


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="/workspace/furcas.csv", help="CSV 文件路径")
    parser.add_argument("--output-dir", default="/workspace", help="JSON 文件输出目录")
    parser.add_argument("--batch-size", type=int, default=15, help="每批记录数")
    parser.add_argument("--prefix", default="new_batch_", help="文件名前缀")
    args = parser.parse_args()

    records = []
    with open(args.csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({"fields": convert_row(row)})

    total = len(records)
    print(f"共读取 {total} 条记录")

    batch_size = args.batch_size
    for i in range(0, total, batch_size):
        batch = records[i : i + batch_size]
        batch_num = i // batch_size + 1
        path = os.path.join(args.output_dir, f"{args.prefix}{batch_num}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"records": batch}, f, ensure_ascii=False)
        size_kb = len(json.dumps(batch, ensure_ascii=False)) / 1024
        print(f"  批 {batch_num}: {len(batch)} 条, {size_kb:.0f} KB → {path}")

    total_batches = (total - 1) // batch_size + 1
    print(f"\n共 {total} 条, 分为 {total_batches} 批")
    print("使用 feishu_bitable_app_table_record action=batch_create 逐批导入")
    print("records 参数必须使用 string='false'（JSON 数组格式）")


if __name__ == "__main__":
    main()
