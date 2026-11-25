#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把财报指标 JSON 转成一页 Markdown 速查表。"""

import argparse
import json
import sys


PERCENT_METRICS = ("毛利率", "净利率", "ROE", "资产负债率", "研发费用率")
MONEY_METRICS = ("营业收入", "归母净利润", "扣非归母净利润", "经营现金流净额", "总市值")


def fmt(value, name):
    if value is None or value == "":
        return "未披露"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if name in PERCENT_METRICS:
        return f"{number:.2f}%"
    if name in MONEY_METRICS:
        return f"{number:,.2f}"
    return f"{number:,.2f}"


def pct(value):
    if value is None or value == "":
        return "—"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{number:+.2f}%"


def main():
    parser = argparse.ArgumentParser(description="财报一页速查表生成")
    parser.add_argument("--input", required=True, help="指标 JSON")
    parser.add_argument("--out", help="输出 Markdown 文件")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    company = data.get("company", "未命名公司")
    code = data.get("code", "")
    period = data.get("period", "报告期未填写")
    scope = data.get("scope", "口径未填写")
    report_type = data.get("report_type", "报告类型未填写")
    unit = data.get("unit", "亿元")
    source = data.get("source", "来源未填写")
    metrics = data.get("metrics", [])

    if not metrics:
        print("metrics 不能为空")
        return 2
    if source == "来源未填写":
        print("[WARN] 缺少数据来源，正式交付前必须补上")

    lines = [
        f"# {company}{('（' + code + '）') if code else ''} {period} 业绩速查",
        f"> 口径：{scope}｜类型：{report_type}｜单位：{unit}｜来源：{source}",
        "",
        "| 指标 | 本期 | 上年同期 | 同比 | 备注 |",
        "| --- | --- | --- | --- | --- |",
    ]

    warnings = []
    for metric in metrics:
        name = metric.get("name", "未命名指标")
        current = metric.get("value")
        prior = metric.get("prior")
        yoy = metric.get("yoy")
        if yoy in (None, "") and current not in (None, "") and prior not in (None, "", 0):
            try:
                yoy = (float(current) - float(prior)) / abs(float(prior)) * 100
            except (TypeError, ValueError):
                yoy = None
                warnings.append(f"{name} 无法计算同比，已留空")
        note = metric.get("note", "")
        if current in (None, ""):
            warnings.append(f"{name} 本期缺失，已标为未披露")
        lines.append(f"| {name} | {fmt(current, name)} | {fmt(prior, name)} | {pct(yoy)} | {note} |")

    content = "\n".join(lines) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"已写入 {args.out}")
    else:
        print(content)

    if warnings:
        print("\n[WARN]")
        for item in warnings:
            print(f"- {item}")
    print("\n提示：结论、风险与免责声明由模型补充，脚本只负责表格与数值格式化。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
