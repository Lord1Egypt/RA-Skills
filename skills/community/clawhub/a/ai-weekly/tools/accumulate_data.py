#!/usr/bin/env python3
"""
accumulate_data.py

历史数据累积器：每次生成报告后将核心指标追加到 data/history.csv，
支撑周环比（WoW）和年同比（YoY）分析。

用法：
  # 追加本周数据
  python tools/accumulate_data.py --week 2026-W27 \
    --market-size 514.5 --funding-total 83.2 --chatgpt-share 46.4 \
    --enterprise-adoption 94 --top-model "GPT-5.6" --top-model-score 91.9

  # 查看历史数据
  python tools/accumulate_data.py --show

  # 计算与上周的环比
  python tools/accumulate_data.py --wow 2026-W27

  # 导出为 JSON
  python tools/accumulate_data.py --export history.json
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

# CSV 列定义
COLUMNS = [
    "week",              # 周数标签，如 2026-W27
    "date",              # 记录日期 YYYY-MM-DD
    "market_size_b",     # 全球AI市场规模（十亿美元）
    "funding_total_b",   # 本周融资总额（十亿美元）
    "chatgpt_share",     # ChatGPT 市场份额（%）
    "enterprise_adoption", # 企业AI采用率（%）
    "top_model",         # 排名第一的模型名称
    "top_model_score",   # 排名第一的模型分数
    "ma_total_b",        # 本周并购总额（十亿美元）
    "notes",             # 备注
]

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
HISTORY_CSV = DATA_DIR / "history.csv"


def init_csv() -> None:
    """初始化 CSV 文件（如不存在则创建）。"""
    DATA_DIR.mkdir(exist_ok=True)
    if not HISTORY_CSV.exists():
        with open(HISTORY_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
        print(f"✅ 已创建历史数据文件：{HISTORY_CSV}")


def append_record(record: dict) -> None:
    """追加一条记录到 CSV。如果周数已存在则更新。"""
    init_csv()

    # 读取现有数据
    rows = []
    with open(HISTORY_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # 检查是否已有该周的记录
    week = record.get("week", "")
    existing_idx = None
    for i, row in enumerate(rows):
        if row.get("week") == week:
            existing_idx = i
            break

    # 填充缺失字段
    for col in COLUMNS:
        if col not in record:
            record[col] = ""

    if existing_idx is not None:
        # 更新已有记录
        rows[existing_idx].update(record)
        print(f"📝 已更新 {week} 的记录")
    else:
        # 追加新记录
        rows.append(record)
        print(f"📝 已追加 {week} 的记录")

    # 写回 CSV
    with open(HISTORY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ 数据已保存到 {HISTORY_CSV}")


def load_history() -> list[dict]:
    """加载所有历史数据。"""
    if not HISTORY_CSV.exists():
        return []
    with open(HISTORY_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def show_history() -> None:
    """显示历史数据表格。"""
    rows = load_history()
    if not rows:
        print("📭 暂无历史数据")
        return

    print(f"\n📊 历史数据（共 {len(rows)} 条记录）")
    print("=" * 100)
    # 表头
    header = f"{'周数':<12} {'市场规模':>10} {'融资额':>10} {'ChatGPT%':>10} {'采用率':>8} {'Top模型':<16} {'分数':>6}"
    print(header)
    print("-" * 100)
    for r in rows:
        line = (f"{r.get('week', ''):<12} "
                f"${r.get('market_size_b', ''):>8}B  "
                f"${r.get('funding_total_b', ''):>8}B  "
                f"{r.get('chatgpt_share', ''):>9}%  "
                f"{r.get('enterprise_adoption', ''):>7}%  "
                f"{r.get('top_model', ''):<16} "
                f"{r.get('top_model_score', ''):>6}")
        print(line)
    print("=" * 100)


def calculate_wow(week: str) -> dict:
    """
    计算指定周与上一周的环比变化。
    返回 {"week", "prev_week", "metrics": [{"name", "current", "previous", "change", "change_pct"}]}
    """
    rows = load_history()
    if not rows:
        return {"error": "无历史数据"}

    # 找到当前周和上一周
    sorted_rows = sorted(rows, key=lambda r: r.get("week", ""))
    current = None
    prev = None

    for i, r in enumerate(sorted_rows):
        if r.get("week") == week:
            current = r
            if i > 0:
                prev = sorted_rows[i - 1]
            break

    if not current:
        return {"error": f"未找到 {week} 的记录"}
    if not prev:
        return {"error": f"无 {week} 的上一周数据", "current": current}

    # 数值指标
    numeric_metrics = [
        ("market_size_b",      "全球AI市场规模"),
        ("funding_total_b",    "本周融资总额"),
        ("chatgpt_share",      "ChatGPT市场份额"),
        ("enterprise_adoption","企业AI采用率"),
        ("top_model_score",    "Top模型分数"),
        ("ma_total_b",         "本周并购总额"),
    ]

    metrics = []
    for key, name in numeric_metrics:
        try:
            curr_val = float(current.get(key, 0) or 0)
            prev_val = float(prev.get(key, 0) or 0)
        except (ValueError, TypeError):
            continue

        if prev_val == 0:
            change = 0
            change_pct = 0
        else:
            change = curr_val - prev_val
            change_pct = round((change / prev_val) * 100, 2)

        metrics.append({
            "name":       name,
            "key":        key,
            "current":    curr_val,
            "previous":   prev_val,
            "change":     round(change, 2),
            "change_pct": change_pct,
            "direction":  "up" if change > 0 else ("down" if change < 0 else "flat"),
        })

    # 模型名称变化
    model_change = {
        "name":     "Top模型",
        "key":      "top_model",
        "current":  current.get("top_model", ""),
        "previous": prev.get("top_model", ""),
        "changed":  current.get("top_model", "") != prev.get("top_model", ""),
    }

    return {
        "week":       week,
        "prev_week":  prev.get("week", ""),
        "metrics":    metrics,
        "model":      model_change,
    }


def print_wow(wow_data: dict) -> None:
    """打印环比分析结果。"""
    if "error" in wow_data:
        print(f"❌ {wow_data['error']}")
        if "current" in wow_data:
            print(f"   当前周：{wow_data['current'].get('week', '')}")
        return

    print(f"\n📊 周环比分析：{wow_data['week']} vs {wow_data['prev_week']}")
    print("=" * 60)
    for m in wow_data["metrics"]:
        arrow = "▲" if m["direction"] == "up" else ("▼" if m["direction"] == "down" else "—")
        sign = "+" if m["change"] > 0 else ""
        print(f"  {m['name']:<16} {m['current']:>10}  "
              f"{arrow} {sign}{m['change']:.2f} ({sign}{m['change_pct']:.1f}%)")

    model = wow_data["model"]
    if model["changed"]:
        print(f"\n  🔄 Top模型变更：{model['previous']} → {model['current']}")
    else:
        print(f"\n  ✅ Top模型未变：{model['current']}")
    print("=" * 60)


def export_json(output_path: str) -> None:
    """导出历史数据为 JSON。"""
    rows = load_history()
    Path(output_path).write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"✅ 已导出 {len(rows)} 条记录到 {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="AI周报历史数据累积器 — 记录核心指标，支持环比分析"
    )

    # 追加数据
    parser.add_argument("--week", default=None, help="周数标签，如 2026-W27")
    parser.add_argument("--market-size", type=float, default=None, help="全球AI市场规模（$B）")
    parser.add_argument("--funding-total", type=float, default=None, help="本周融资总额（$B）")
    parser.add_argument("--chatgpt-share", type=float, default=None, help="ChatGPT市场份额（%）")
    parser.add_argument("--enterprise-adoption", type=float, default=None, help="企业AI采用率（%）")
    parser.add_argument("--top-model", default=None, help="排名第一的模型名称")
    parser.add_argument("--top-model-score", type=float, default=None, help="Top模型分数")
    parser.add_argument("--ma-total", type=float, default=None, help="本周并购总额（$B）")
    parser.add_argument("--notes", default="", help="备注")

    # 查询模式
    parser.add_argument("--show", action="store_true", help="显示历史数据表格")
    parser.add_argument("--wow", default=None, help="计算指定周与上周的环比，如 --wow 2026-W27")
    parser.add_argument("--export", default=None, help="导出为 JSON 文件")

    args = parser.parse_args()

    # 查询模式
    if args.show:
        show_history()
        return

    if args.wow:
        wow_data = calculate_wow(args.wow)
        print_wow(wow_data)
        return

    if args.export:
        export_json(args.export)
        return

    # 追加模式（需要至少 week 参数）
    if not args.week:
        parser.print_help()
        print("\n❌ 追加数据需要 --week 参数")
        sys.exit(1)

    record = {
        "week":      args.week,
        "date":      datetime.now().strftime("%Y-%m-%d"),
        "notes":     args.notes,
    }
    if args.market_size is not None:
        record["market_size_b"] = args.market_size
    if args.funding_total is not None:
        record["funding_total_b"] = args.funding_total
    if args.chatgpt_share is not None:
        record["chatgpt_share"] = args.chatgpt_share
    if args.enterprise_adoption is not None:
        record["enterprise_adoption"] = args.enterprise_adoption
    if args.top_model:
        record["top_model"] = args.top_model
    if args.top_model_score is not None:
        record["top_model_score"] = args.top_model_score
    if args.ma_total is not None:
        record["ma_total_b"] = args.ma_total

    append_record(record)


if __name__ == "__main__":
    main()
