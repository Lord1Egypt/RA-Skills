#!/usr/bin/env python3
"""
report_generator.py - 生成中英文 CSV 覆盖分析报告

从 coverage_analyzer.py 的分析结果 JSON 生成两份 CSV 报告：
  - coverage_report_zh.csv (中文)
  - coverage_report_en.csv (英文)

用法:
    python report_generator.py --analysis analysis_result.json -o /path/to/output/
"""

import json
import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("错误: 需要 pandas。请运行: pip install pandas openpyxl", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────────────────────────
# 列定义
# ─────────────────────────────────────────────

COLUMNS_ZH = [
    "CIS 规则编号",
    "CIS 规则标题",
    "配置项路径",
    "配置参数",
    "CIS 期望值",
    "OpenEuler 要求值",
    "覆盖状态",
    "匹配方式",
    "级别",
    "评分",
    "备注"
]

STATUS_LABELS_ZH = {
    "fully_covered": "完全覆盖",
    "partially_covered": "部分覆盖",
    "not_covered": "未覆盖"
}

COLUMNS_EN = [
    "CIS Rule ID",
    "CIS Rule Title",
    "Config Path",
    "Config Parameter",
    "CIS Expected Value",
    "OpenEuler Value",
    "Coverage Status",
    "Match Type",
    "Level",
    "Scoring",
    "Remarks"
]

STATUS_LABELS_EN = {
    "fully_covered": "Fully Covered",
    "partially_covered": "Partially Covered",
    "not_covered": "Not Covered"
}


def build_dataframe(results: list, lang: str = "zh") -> pd.DataFrame:
    """
    将分析结果转换为 DataFrame
    lang: "zh" 或 "en"
    """
    columns = COLUMNS_ZH if lang == "zh" else COLUMNS_EN
    status_labels = STATUS_LABELS_ZH if lang == "zh" else STATUS_LABELS_EN

    rows = []
    for r in results:
        status_label = status_labels.get(r.get("coverage_status", ""),
                                         r.get("coverage_status", ""))

        row = {}

        if lang == "zh":
            row["CIS 规则编号"] = r.get("rule_id", "")
            row["CIS 规则标题"] = r.get("title", "")
            row["配置项路径"] = r.get("config_path", "")
            row["配置参数"] = r.get("config_param", "")
            row["CIS 期望值"] = r.get("cis_expected_value", "")
            row["OpenEuler 要求值"] = r.get("oe_expected_value", "")
            row["覆盖状态"] = status_label
            row["匹配方式"] = r.get("match_type", "")
            row["级别"] = r.get("level", "")
            row["评分"] = r.get("scoring", "")
            row["备注"] = r.get("remarks", "")
        else:
            row["CIS Rule ID"] = r.get("rule_id", "")
            row["CIS Rule Title"] = r.get("title", "")
            row["Config Path"] = r.get("config_path", "")
            row["Config Parameter"] = r.get("config_param", "")
            row["CIS Expected Value"] = r.get("cis_expected_value", "")
            row["OpenEuler Value"] = r.get("oe_expected_value", "")
            row["Coverage Status"] = status_label
            row["Match Type"] = r.get("match_type", "")
            row["Level"] = r.get("level", "")
            row["Scoring"] = r.get("scoring", "")
            row["Remarks"] = r.get("remarks", "")

        rows.append(row)

    df = pd.DataFrame(rows, columns=columns)
    return df


def write_csv(df: pd.DataFrame, output_path: Path):
    """输出 CSV 文件"""
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"  [✓] CSV: {output_path}")


def write_summary(results: list, output_dir: Path, lang: str = "zh"):
    """输出摘要文本文件"""
    status_counts = {}
    for r in results:
        status = r["coverage_status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    total = len(results)

    if lang == "zh":
        summary_path = output_dir / "coverage_summary_zh.txt"
        lines = [
            "=" * 60,
            "CIS RHEL Benchmark → OpenEuler 安全基线覆盖分析报告",
            "=" * 60,
            f"",
            f"CIS 规则总数: {total}",
            f"OpenEuler 基线条目: {sum(1 for r in results if r.get('oe_config_path'))} (匹配到的)",
            f"",
            f"📊 覆盖统计:",
            f"  ✅ 完全覆盖 (Fully Covered): {status_counts.get('fully_covered', 0)}",
            f"  ⚠️  部分覆盖 (Partially Covered): {status_counts.get('partially_covered', 0)}",
            f"  ❌ 未覆盖 (Not Covered): {status_counts.get('not_covered', 0)}",
            f"",
            f"📄 CSV 报告文件:",
            f"  中文: {output_dir / 'coverage_report_zh.csv'}",
            f"  英文: {output_dir / 'coverage_report_en.csv'}",
            f"",
            f"生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
        ]
    else:
        summary_path = output_dir / "coverage_summary_en.txt"
        lines = [
            "=" * 60,
            "CIS RHEL Benchmark → OpenEuler Security Baseline Coverage Analysis",
            "=" * 60,
            f"",
            f"Total CIS Rules: {total}",
            f"Matched OpenEuler Items: {sum(1 for r in results if r.get('oe_config_path'))}",
            f"",
            f"📊 Coverage Summary:",
            f"  ✅ Fully Covered: {status_counts.get('fully_covered', 0)}",
            f"  ⚠️  Partially Covered: {status_counts.get('partially_covered', 0)}",
            f"  ❌ Not Covered: {status_counts.get('not_covered', 0)}",
            f"",
            f"📄 CSV Report Files:",
            f"  Chinese: {output_dir / 'coverage_report_zh.csv'}",
            f"  English: {output_dir / 'coverage_report_en.csv'}",
            f"",
            f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
        ]

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [✓] 摘要: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description="生成中英文 CSV 覆盖分析报告")
    parser.add_argument("--analysis", required=True,
                        help="分析结果 JSON 文件路径 (coverage_analyzer.py 输出)")
    parser.add_argument("-o", "--output", default=".",
                        help="报告输出目录 (默认: 当前目录)")
    args = parser.parse_args()

    # 加载分析结果
    with open(args.analysis, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = data.get("results", data)  # 兼容纯 results 数组或带 summary 的对象
    summary = data.get("summary", {})

    if isinstance(results, list):
        pass
    elif isinstance(data, list):
        results = data
    else:
        print(f"错误: 无法识别的 JSON 结构", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("错误: 无分析结果数据", file=sys.stderr)
        sys.exit(1)

    print(f"[*] 分析结果: {len(results)} 条规则")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成中文报告
    print("\n[*] 生成中文报告...")
    df_zh = build_dataframe(results, lang="zh")
    write_csv(df_zh, output_dir / "coverage_report_zh.csv")
    write_summary(results, output_dir, lang="zh")

    # 生成英文报告
    print("\n[*] 生成英文报告...")
    df_en = build_dataframe(results, lang="en")
    write_csv(df_en, output_dir / "coverage_report_en.csv")
    write_summary(results, output_dir, lang="en")

    # 打印统计
    print(f"\n{'=' * 50}")
    status_counts = {}
    for r in results:
        status = r["coverage_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    total = len(results)

    print(f"📊 覆盖统计:")
    sc = summary if summary else {}
    print(f"  ✅ 完全覆盖: {sc.get('fully_covered', status_counts.get('fully_covered', 0))}")
    print(f"  ⚠️  部分覆盖: {sc.get('partially_covered', status_counts.get('partially_covered', 0))}")
    print(f"  ❌ 未覆盖: {sc.get('not_covered', sc.get('not_covered', status_counts.get('not_covered', 0)))}")
    print(f"  📋 合计: {sc.get('cis_total', total)}")
    print(f"{'=' * 50}")

    print(f"\n[✓] 报告已生成至: {output_dir}")
    print(f"    中文: {output_dir / 'coverage_report_zh.csv'}")
    print(f"    英文: {output_dir / 'coverage_report_en.csv'}")
    print(f"    中文摘要: {output_dir / 'coverage_summary_zh.txt'}")
    print(f"    英文摘要: {output_dir / 'coverage_summary_en.txt'}")


if __name__ == "__main__":
    main()
