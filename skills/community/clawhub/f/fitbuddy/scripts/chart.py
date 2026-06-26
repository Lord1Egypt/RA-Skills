#!/usr/bin/env python3
"""fitbuddy - 图表生成"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(SKILL_DIR, "fitbuddy-data")
RECORDS_DIR = os.path.join(DATA_DIR, "records")
CHARTS_DIR = os.path.join(DATA_DIR, "charts")

# Chinese font fallback
FONT_CANDIDATES = [
    "Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei",
    "PingFang SC", "Noto Sans CJK SC",
]


def setup_chinese_font():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import fontManager
    available = {f.name for f in fontManager.ttflist}
    for font in FONT_CANDIDATES:
        if font in available:
            plt.rcParams["font.sans-serif"] = [font, "DejaVu Sans"]
            plt.rcParams["axes.unicode_minus"] = False
            return font
    return None


def load_records(days=30):
    """Load records for the last N days, return list of record dicts."""
    records = []
    today = datetime.now().date()
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        path = os.path.join(RECORDS_DIR, f"{d}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                records.append(json.load(f))
        else:
            records.append({"date": str(d), "weight_kg": None, "daily_summary": {
                "total_calories_in": 0, "total_calories_out": 0,
                "total_protein_g": 0, "total_carbs_g": 0, "total_fat_g": 0,
            }, "water_ml": 0, "exercises": []})
    return records


def load_profile():
    path = os.path.join(DATA_DIR, "profile.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def cmd_weight_trend(args):
    import matplotlib.pyplot as plt
    setup_chinese_font()
    profile = load_profile()
    records = load_records(args.days)

    dates = []
    weights = []
    for r in records:
        if r.get("weight_kg") is not None:
            dates.append(r["date"])
            weights.append(r["weight_kg"])

    if not dates:
        print(json.dumps({"error": "没有体重数据"}))
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, weights, "o-", color="#4CAF50", linewidth=2, markersize=6)
    ax.set_xlabel("日期" if plt.rcParams.get("font.sans-serif", [""])[0] != "DejaVu Sans" else "Date")
    ax.set_ylabel("kg")
    ax.set_title("体重趋势")
    ax.grid(True, alpha=0.3)

    # Target line
    target = profile.get("target_weight_kg")
    if target:
        ax.axhline(y=target, color="red", linestyle="--", alpha=0.7, label=f"目标 {target}kg")
        ax.legend()

    # Annotate last point
    ax.annotate(f"{weights[-1]}kg", (dates[-1], weights[-1]),
                textcoords="offset points", xytext=(10, 5), fontsize=10)

    fig.autofmt_xdate()
    plt.tight_layout()

    os.makedirs(CHARTS_DIR, exist_ok=True)
    output = args.output or os.path.join(CHARTS_DIR, "weight-trend.png")
    fig.savefig(output, dpi=150)
    plt.close(fig)
    print(json.dumps({"chart": output}))


def cmd_calorie_balance(args):
    import matplotlib.pyplot as plt
    import numpy as np
    setup_chinese_font()
    records = load_records(args.days)

    dates = [r["date"][-5:] for r in records]  # MM-DD
    calories_in = [r["daily_summary"]["total_calories_in"] for r in records]
    calories_out = [r["daily_summary"]["total_calories_out"] for r in records]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(dates))
    width = 0.35
    bars1 = ax.bar(x - width/2, calories_in, width, label="摄入", color="#FF9800", alpha=0.8)
    bars2 = ax.bar(x + width/2, calories_out, width, label="消耗", color="#2196F3", alpha=0.8)

    profile = load_profile()
    target = profile.get("daily_calorie_target", 0)
    if target:
        ax.axhline(y=target, color="green", linestyle="--", alpha=0.7, label=f"目标 {target}")

    ax.set_xlabel("日期")
    ax.set_ylabel("kcal")
    ax.set_title("热量收支")
    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()

    os.makedirs(CHARTS_DIR, exist_ok=True)
    output = args.output or os.path.join(CHARTS_DIR, "calorie-balance.png")
    fig.savefig(output, dpi=150)
    plt.close(fig)
    print(json.dumps({"chart": output}))


def cmd_macro_pie(args):
    import matplotlib.pyplot as plt
    setup_chinese_font()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(RECORDS_DIR, f"{date_str}.json")
    if not os.path.exists(path):
        print(json.dumps({"error": f"没有 {date_str} 的记录"}))
        return

    with open(path, "r", encoding="utf-8") as f:
        rec = json.load(f)

    s = rec["daily_summary"]
    p_cal = s["total_protein_g"] * 4
    c_cal = s["total_carbs_g"] * 4
    f_cal = s["total_fat_g"] * 9

    if p_cal + c_cal + f_cal == 0:
        print(json.dumps({"error": "没有营养素数据"}))
        return

    labels = [f"蛋白质 {s['total_protein_g']}g", f"碳水 {s['total_carbs_g']}g", f"脂肪 {s['total_fat_g']}g"]
    sizes = [p_cal, c_cal, f_cal]
    colors = ["#FF6384", "#36A2EB", "#FFCE56"]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"{date_str} 营养素占比")
    plt.tight_layout()

    os.makedirs(CHARTS_DIR, exist_ok=True)
    output = args.output or os.path.join(CHARTS_DIR, f"macro-pie-{date_str}.png")
    fig.savefig(output, dpi=150)
    plt.close(fig)
    print(json.dumps({"chart": output}))


def cmd_weekly_report(args):
    import matplotlib.pyplot as plt
    setup_chinese_font()
    records = load_records(7)

    # Filter records with data
    valid = [r for r in records if r.get("weight_kg") or r["daily_summary"]["total_calories_in"] > 0]
    if not valid:
        print(json.dumps({"error": "本周没有记录数据"}))
        return

    report = {
        "start_date": records[0]["date"],
        "end_date": records[-1]["date"],
        "days_with_data": len(valid),
        "total_exercises": sum(len(r.get("exercises", [])) for r in valid),
        "total_water_ml": sum(r.get("water_ml", 0) for r in valid),
        "avg_calories_in": round(sum(r["daily_summary"]["total_calories_in"] for r in valid) / max(len(valid), 1)),
        "avg_calories_out": round(sum(r["daily_summary"]["total_calories_out"] for r in valid) / max(len(valid), 1)),
        "weight_start": next((r["weight_kg"] for r in valid if r.get("weight_kg")), None),
        "weight_end": next((r["weight_kg"] for r in reversed(valid) if r.get("weight_kg")), None),
    }
    print(json.dumps(report, ensure_ascii=False))


def cmd_monthly_report(args):
    import matplotlib.pyplot as plt
    setup_chinese_font()
    records = load_records(30)

    valid = [r for r in records if r.get("weight_kg") or r["daily_summary"]["total_calories_in"] > 0]
    if not valid:
        print(json.dumps({"error": "本月没有记录数据"}))
        return

    report = {
        "start_date": records[0]["date"],
        "end_date": records[-1]["date"],
        "days_with_data": len(valid),
        "total_exercises": sum(len(r.get("exercises", [])) for r in valid),
        "total_water_ml": sum(r.get("water_ml", 0) for r in valid),
        "avg_calories_in": round(sum(r["daily_summary"]["total_calories_in"] for r in valid) / max(len(valid), 1)),
        "avg_calories_out": round(sum(r["daily_summary"]["total_calories_out"] for r in valid) / max(len(valid), 1)),
        "weight_start": next((r["weight_kg"] for r in valid if r.get("weight_kg")), None),
        "weight_end": next((r["weight_kg"] for r in reversed(valid) if r.get("weight_kg")), None),
    }
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fitbuddy chart")
    sub = parser.add_subparsers(dest="command")

    p_wt = sub.add_parser("weight-trend")
    p_wt.add_argument("--data-dir", default=DATA_DIR)
    p_wt.add_argument("--output", default=None)
    p_wt.add_argument("--days", type=int, default=30)

    p_cb = sub.add_parser("calorie-balance")
    p_cb.add_argument("--data-dir", default=DATA_DIR)
    p_cb.add_argument("--output", default=None)
    p_cb.add_argument("--days", type=int, default=14)

    p_mp = sub.add_parser("macro-pie")
    p_mp.add_argument("--data-dir", default=DATA_DIR)
    p_mp.add_argument("--output", default=None)
    p_mp.add_argument("--date", default=None)

    p_wr = sub.add_parser("weekly-report")
    p_wr.add_argument("--data-dir", default=DATA_DIR)

    p_mr = sub.add_parser("monthly-report")
    p_mr.add_argument("--data-dir", default=DATA_DIR)

    args = parser.parse_args()
    if args.command == "weight-trend":
        cmd_weight_trend(args)
    elif args.command == "calorie-balance":
        cmd_calorie_balance(args)
    elif args.command == "macro-pie":
        cmd_macro_pie(args)
    elif args.command == "weekly-report":
        cmd_weekly_report(args)
    elif args.command == "monthly-report":
        cmd_monthly_report(args)
    else:
        parser.print_help()
