#!/usr/bin/env python3
"""
Apple Health Exercise Readiness Analyzer
查询苹果健康当日数据，判断身体状况是否适合锻炼。
输出四档建议：重度锻炼 / 中度锻炼 / 轻度锻炼 / 建议休息
"""

import zipfile
import xml.etree.ElementTree as ET
import json
import sys
import argparse
import os
import statistics
from datetime import date, datetime, timedelta

# ── Sleep stage identifiers ────────────────────────────────────────

ASLEEP_VALUES = {
    "HKCategoryValueSleepAnalysisAsleep",
    "HKCategoryValueSleepAnalysisAsleepDeep",
    "HKCategoryValueSleepAnalysisAsleepREM",
    "HKCategoryValueSleepAnalysisAsleepCore",
}
DEEP_SLEEP_VALUES = {"HKCategoryValueSleepAnalysisAsleepDeep"}

# ── Parsing helpers ────────────────────────────────────────────────

def parse_dt(s: str) -> datetime | None:
    """Parse Apple Health date string (with or without timezone offset)."""
    for fmt in ("%Y-%m-%d %H:%M:%S %z", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def local_date(dt: datetime) -> date:
    """Extract the local calendar date from a parsed datetime."""
    return dt.date()


# ── Extract health data from ZIP ───────────────────────────────────

def load_xml_root(zip_path: str) -> ET.Element:
    with zipfile.ZipFile(zip_path, "r") as zf:
        xml_name = next(
            (n for n in zf.namelist()
             if n.endswith("export.xml") and "export_cda" not in n),
            None,
        )
        if not xml_name:
            raise ValueError(
                "在 ZIP 中找不到 export.xml。"
                "请确认使用的是苹果健康官方导出文件（设置 → 健康数据 → 导出）。"
            )
        print(f"[解析] {xml_name} …", file=sys.stderr)
        with zf.open(xml_name) as f:
            return ET.parse(f).getroot()


# ── Collect today's metrics ────────────────────────────────────────

def collect_metrics(root: ET.Element, target_date: date) -> dict:
    """
    Iterate the XML once and collect:
      - Last night's sleep (sessions ending on target_date)
      - HRV, RHR, SpO2, respiratory rate for target_date
      - 30-day baseline for HRV and RHR
      - Active energy burned yesterday
    """
    yesterday = target_date - timedelta(days=1)
    baseline_start = target_date - timedelta(days=30)

    hrv_today, rhr_today, spo2_today, resp_today = [], [], [], []
    hrv_baseline, rhr_baseline = [], []
    active_energy_yesterday = []

    # Sleep: list of dicts {start, end, value}
    sleep_segments: list[dict] = []

    for rec in root.iter("Record"):
        rtype = rec.get("type", "")
        start_str = rec.get("startDate", "")
        end_str = rec.get("endDate", "")
        value_str = rec.get("value", "")

        start_dt = parse_dt(start_str)
        if start_dt is None:
            continue
        start_d = local_date(start_dt)

        # ── Sleep ──────────────────────────────────────────────────
        if rtype == "HKCategoryTypeIdentifierSleepAnalysis":
            if value_str not in ASLEEP_VALUES:
                continue
            end_dt = parse_dt(end_str)
            if end_dt is None:
                continue
            end_d = local_date(end_dt)
            # Keep segments that ended today and started yesterday or today
            if end_d == target_date and start_d in (yesterday, target_date):
                duration_h = (end_dt - start_dt).total_seconds() / 3600
                if 0 < duration_h < 16:
                    sleep_segments.append(
                        {"start": start_dt, "end": end_dt, "value": value_str}
                    )
            continue

        # ── Numeric metrics ────────────────────────────────────────
        try:
            val = float(value_str)
        except (ValueError, TypeError):
            continue

        if rtype == "HKQuantityTypeIdentifierHeartRateVariabilitySDNN":
            if start_d == target_date:
                hrv_today.append(val)
            elif baseline_start <= start_d < target_date:
                hrv_baseline.append(val)

        elif rtype == "HKQuantityTypeIdentifierRestingHeartRate":
            if start_d == target_date:
                rhr_today.append(val)
            elif baseline_start <= start_d < target_date:
                rhr_baseline.append(val)

        elif rtype == "HKQuantityTypeIdentifierOxygenSaturation":
            # Apple Health stores SpO2 as a decimal (0.95 = 95%)
            pct = val * 100 if val <= 1.0 else val
            if start_d == target_date:
                spo2_today.append(pct)

        elif rtype == "HKQuantityTypeIdentifierRespiratoryRate":
            if start_d == target_date:
                resp_today.append(val)

        elif rtype == "HKQuantityTypeIdentifierActiveEnergyBurned":
            if start_d == yesterday:
                active_energy_yesterday.append(val)

    # ── Merge overlapping sleep intervals ──────────────────────────
    def merge_intervals(segs):
        if not segs:
            return []
        segs = sorted(segs, key=lambda x: x[0])
        merged = [list(segs[0])]
        for s, e in segs[1:]:
            if s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        return merged

    asleep_ivs = [(s["start"], s["end"]) for s in sleep_segments]
    deep_ivs = [
        (s["start"], s["end"])
        for s in sleep_segments
        if s["value"] in DEEP_SLEEP_VALUES
    ]

    merged_asleep = merge_intervals(asleep_ivs)
    merged_deep = merge_intervals(deep_ivs)

    total_sleep_h = (
        sum((e - s).total_seconds() / 3600 for s, e in merged_asleep)
        if merged_asleep else None
    )
    total_deep_h = (
        sum((e - s).total_seconds() / 3600 for s, e in merged_deep)
        if merged_deep else None
    )
    deep_pct = (
        round(total_deep_h / total_sleep_h * 100, 1)
        if (total_sleep_h and total_deep_h and total_sleep_h > 0)
        else None
    )

    def avg(lst):
        return statistics.mean(lst) if lst else None

    return {
        "date": target_date.isoformat(),
        "sleep_hours": round(total_sleep_h, 2) if total_sleep_h else None,
        "deep_sleep_pct": deep_pct,
        "hrv_today": round(avg(hrv_today), 1) if avg(hrv_today) else None,
        "hrv_baseline_30d": round(avg(hrv_baseline), 1) if avg(hrv_baseline) else None,
        "rhr_today": round(avg(rhr_today), 1) if avg(rhr_today) else None,
        "rhr_baseline_30d": round(avg(rhr_baseline), 1) if avg(rhr_baseline) else None,
        "spo2_today": round(avg(spo2_today), 1) if avg(spo2_today) else None,
        "respiratory_rate": round(avg(resp_today), 1) if avg(resp_today) else None,
        "active_energy_yesterday_kcal": (
            round(sum(active_energy_yesterday)) if active_energy_yesterday else None
        ),
    }


# ── Scoring engine ─────────────────────────────────────────────────

def compute_readiness(m: dict) -> dict:
    """
    Score the body's exercise readiness on a 0-100 scale.
    Deduct points for negative signals; positives are noted but don't add points
    (a well-rested body is the baseline expectation).

    Final score → level:
      75-100  →  重度锻炼 (Intense)
      55-74   →  中度锻炼 (Moderate)
      35-54   →  轻度锻炼 (Light)
       0-34   →  建议休息 (Rest)
    """
    score = 100
    warnings: list[str] = []
    positives: list[str] = []

    # ── Sleep duration ─────────────────────────────────────────────
    sleep = m.get("sleep_hours")
    if sleep is not None:
        if sleep < 5:
            score -= 40
            warnings.append(f"昨晚睡眠严重不足（{sleep:.1f} 小时），身体几乎没有时间修复")
        elif sleep < 6:
            score -= 25
            warnings.append(f"昨晚睡眠不足（{sleep:.1f} 小时），恢复质量受到明显影响")
        elif sleep < 7:
            score -= 10
            warnings.append(f"昨晚睡眠偏少（{sleep:.1f} 小时），存在轻度疲劳")
        else:
            positives.append(f"昨晚睡眠充足（{sleep:.1f} 小时）")
    else:
        score -= 5  # 轻微惩罚：无睡眠数据

    # ── Deep sleep ────────────────────────────────────────────────
    deep = m.get("deep_sleep_pct")
    if deep is not None:
        if deep < 10:
            score -= 20
            warnings.append(f"深睡眠比例极低（{deep:.0f}%，参考值 ≥15%），身体修复效率差")
        elif deep < 15:
            score -= 10
            warnings.append(f"深睡眠比例偏低（{deep:.0f}%，参考值 ≥15%）")
        else:
            positives.append(f"深睡眠比例良好（{deep:.0f}%）")

    # ── HRV ───────────────────────────────────────────────────────
    hrv = m.get("hrv_today")
    hrv_base = m.get("hrv_baseline_30d")
    if hrv is not None:
        if hrv_base and hrv_base > 0:
            pct = (hrv - hrv_base) / hrv_base * 100
            if pct < -25:
                score -= 30
                warnings.append(
                    f"HRV 显著低于基线（今日 {hrv:.0f} ms vs 30日均值 {hrv_base:.0f} ms，"
                    f"↓{abs(pct):.0f}%）——自主神经恢复严重不足，提示过度训练或身体应激"
                )
            elif pct < -15:
                score -= 20
                warnings.append(
                    f"HRV 低于基线（今日 {hrv:.0f} ms vs 30日均值 {hrv_base:.0f} ms，↓{abs(pct):.0f}%）"
                )
            elif pct < -5:
                score -= 8
                warnings.append(
                    f"HRV 略低于基线（今日 {hrv:.0f} ms vs 30日均值 {hrv_base:.0f} ms）"
                )
            elif pct > 10:
                positives.append(
                    f"HRV 高于基线（今日 {hrv:.0f} ms vs 30日均值 {hrv_base:.0f} ms，↑{pct:.0f}%）——恢复状态优秀"
                )
            else:
                positives.append(
                    f"HRV 处于正常范围（今日 {hrv:.0f} ms vs 30日均值 {hrv_base:.0f} ms）"
                )
        else:
            # 无基线时用绝对阈值
            if hrv < 20:
                score -= 20
                warnings.append(f"HRV 较低（{hrv:.0f} ms），自主神经恢复可能不足")
            elif hrv >= 50:
                positives.append(f"HRV 处于较高水平（{hrv:.0f} ms）")
            else:
                positives.append(f"HRV 有记录（{hrv:.0f} ms）")

    # ── Resting Heart Rate ─────────────────────────────────────────
    rhr = m.get("rhr_today")
    rhr_base = m.get("rhr_baseline_30d")
    if rhr is not None:
        if rhr_base and rhr_base > 0:
            pct = (rhr - rhr_base) / rhr_base * 100
            if pct > 15:
                score -= 25
                warnings.append(
                    f"静息心率显著高于基线（今日 {rhr:.0f} bpm vs 30日均值 {rhr_base:.0f} bpm，"
                    f"↑{pct:.0f}%）——提示疲劳、身体应激或潜在感染"
                )
            elif pct > 8:
                score -= 15
                warnings.append(
                    f"静息心率高于基线（今日 {rhr:.0f} bpm vs 30日均值 {rhr_base:.0f} bpm，↑{pct:.0f}%）"
                )
            elif pct > 4:
                score -= 5
                warnings.append(f"静息心率略高于基线（今日 {rhr:.0f} bpm）")
            else:
                positives.append(
                    f"静息心率正常（今日 {rhr:.0f} bpm vs 30日均值 {rhr_base:.0f} bpm）"
                )
        else:
            if rhr > 90:
                score -= 25
                warnings.append(f"静息心率偏高（{rhr:.0f} bpm），建议充分休息")
            elif rhr > 80:
                score -= 10
                warnings.append(f"静息心率略高（{rhr:.0f} bpm）")
            else:
                positives.append(f"静息心率良好（{rhr:.0f} bpm）")

    # ── SpO2 ──────────────────────────────────────────────────────
    spo2 = m.get("spo2_today")
    if spo2 is not None:
        if spo2 < 93:
            score -= 50
            warnings.append(
                f"⚠️  血氧饱和度过低（{spo2:.1f}%）——存在健康风险，强烈建议今日不运动并尽快就医"
            )
        elif spo2 < 95:
            score -= 20
            warnings.append(f"血氧饱和度偏低（{spo2:.1f}%，参考值 ≥95%），避免高强度运动")
        else:
            positives.append(f"血氧饱和度正常（{spo2:.1f}%）")

    # ── Respiratory rate ──────────────────────────────────────────
    resp = m.get("respiratory_rate")
    if resp is not None:
        if resp > 22:
            score -= 15
            warnings.append(f"呼吸频率偏高（{resp:.1f} 次/分，参考值 12-20），可能存在身体应激")
        elif resp > 18:
            score -= 5
            warnings.append(f"呼吸频率略高（{resp:.1f} 次/分）")
        else:
            positives.append(f"呼吸频率正常（{resp:.1f} 次/分）")

    # ── Previous day's exercise load ───────────────────────────────
    energy = m.get("active_energy_yesterday_kcal")
    if energy is not None:
        if energy > 800:
            score -= 15
            warnings.append(
                f"昨日运动量较大（活动消耗约 {energy:.0f} 千卡），身体仍在从高负荷中恢复"
            )
        elif energy > 500:
            score -= 5
            warnings.append(f"昨日有中等运动量（活动消耗约 {energy:.0f} 千卡）")
        elif energy and energy > 0:
            positives.append(f"昨日活动量适中（消耗约 {energy:.0f} 千卡）")

    # ── Determine level ────────────────────────────────────────────
    score = max(0, min(100, score))

    if score >= 75:
        level, level_zh, emoji = "intense", "重度锻炼", "💪"
        recommendation = (
            "身体状态优秀，非常适合高强度训练。"
            "可以进行 HIIT、力量训练、长跑或竞技性运动，"
            "充分利用今日良好的恢复状态提升体能。"
        )
        exercise_examples = "跑步（配速挑战）、力量训练、HIIT、球类运动"
        intensity_guide = "目标心率区间：最大心率的 75–90%"
    elif score >= 55:
        level, level_zh, emoji = "moderate", "中度锻炼", "🏃"
        recommendation = (
            "身体状态良好，适合中等强度有氧运动。"
            "推荐慢跑、游泳、骑行或团体健身课，"
            "注意控制强度，运动后确保充足补水和恢复。"
        )
        exercise_examples = "慢跑、游泳、骑行、椭圆机、普拉提"
        intensity_guide = "目标心率区间：最大心率的 60–75%"
    elif score >= 35:
        level, level_zh, emoji = "light", "轻度锻炼", "🚶"
        recommendation = (
            "身体存在一定疲劳信号，建议以低强度活动为主。"
            "散步、拉伸和瑜伽有助于促进血液循环而不增加额外负担，"
            "避免高强度训练，优先保障睡眠和恢复。"
        )
        exercise_examples = "快走、轻度拉伸、瑜伽、太极"
        intensity_guide = "目标心率区间：最大心率的 50–60%，时长控制在 30 分钟以内"
    else:
        level, level_zh, emoji = "rest", "建议休息", "😴"
        recommendation = (
            "身体恢复状态较差，今日不建议进行正式锻炼。"
            "强行运动不仅效果大打折扣，还可能增加受伤风险和免疫压力。"
            "充足的休息、充分的睡眠和营养补充，本身就是最好的「训练」。"
        )
        exercise_examples = "轻度散步（<15 分钟）或完全休息"
        intensity_guide = "如必须活动，保持极低强度，心率不超过最大心率的 50%"

    return {
        "score": score,
        "level": level,
        "level_zh": level_zh,
        "emoji": emoji,
        "recommendation": recommendation,
        "exercise_examples": exercise_examples,
        "intensity_guide": intensity_guide,
        "positive_signals": positives,
        "warning_signals": warnings,
    }


# ── Report formatter ───────────────────────────────────────────────

def format_report(m: dict, r: dict) -> str:
    bar_filled = round(r["score"] / 100 * 20)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    lines = [
        "=" * 62,
        f"  🍎  苹果健康 · 今日运动建议  ({m['date']})",
        "=" * 62,
        "",
        f"  综合评分  [{bar}] {r['score']}/100",
        f"  运动建议  {r['emoji']}  {r['level_zh']}",
        "",
        "  📋  建议说明",
        f"  {r['recommendation']}",
        "",
        f"  推荐运动：{r['exercise_examples']}",
        f"  强度参考：{r['intensity_guide']}",
        "",
    ]

    if r["positive_signals"]:
        lines.append("  ✅  积极信号")
        for s in r["positive_signals"]:
            lines.append(f"     · {s}")
        lines.append("")

    if r["warning_signals"]:
        lines.append("  ⚠️   注意信号")
        for s in r["warning_signals"]:
            lines.append(f"     · {s}")
        lines.append("")

    def fmt(v, spec, unit):
        return f"{v:{spec}} {unit}" if v is not None else "无数据"

    lines += [
        "  📊  今日数据摘要",
        f"     昨晚睡眠时长   : {fmt(m['sleep_hours'], '.1f', '小时')}",
        f"     深睡眠比例     : {fmt(m['deep_sleep_pct'], '.0f', '%')}",
        f"     HRV（今日）    : {fmt(m['hrv_today'], '.0f', 'ms')}",
        f"     HRV（30日均）  : {fmt(m['hrv_baseline_30d'], '.0f', 'ms')}",
        f"     静息心率（今日）: {fmt(m['rhr_today'], '.0f', 'bpm')}",
        f"     静息心率（30日）: {fmt(m['rhr_baseline_30d'], '.0f', 'bpm')}",
        f"     血氧饱和度     : {fmt(m['spo2_today'], '.1f', '%')}",
        f"     呼吸频率       : {fmt(m['respiratory_rate'], '.1f', '次/分')}",
        f"     昨日活动消耗   : {fmt(m['active_energy_yesterday_kcal'], '.0f', '千卡')}",
        "",
        "─" * 62,
        "  ⚕️  免责声明：本分析仅供健康管理参考，不构成医疗建议。",
        "       如有身体不适或持续异常，请咨询专业医生。",
        "=" * 62,
    ]

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Apple Health Exercise Readiness Analyzer — 今日运动适宜性分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python analyze.py ~/Downloads/export.zip
  python analyze.py ~/Downloads/export.zip --date 2026-04-03
  python analyze.py ~/Downloads/export.zip --json
  python analyze.py ~/Downloads/export.zip --out ./output
        """,
    )
    parser.add_argument("zip_path", help="苹果健康导出 ZIP 文件路径")
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="指定分析日期（默认为今天）",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出原始数据（适合脚本处理）",
    )
    parser.add_argument(
        "--out",
        metavar="DIR",
        help="将 JSON 结果保存到指定目录（同时生成 exercise_readiness.json）",
    )

    args = parser.parse_args()

    target_date = date.today()
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"错误：日期格式无效（{args.date}），请使用 YYYY-MM-DD 格式。", file=sys.stderr)
            sys.exit(1)

    print(f"[分析] 目标日期：{target_date}", file=sys.stderr)

    try:
        root = load_xml_root(args.zip_path)
    except (zipfile.BadZipFile, FileNotFoundError) as e:
        print(f"错误：无法读取 ZIP 文件 — {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

    metrics = collect_metrics(root, target_date)
    readiness = compute_readiness(metrics)

    result = {"metrics": metrics, "readiness": readiness}

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        out_path = os.path.join(args.out, "exercise_readiness.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[输出] JSON 已保存至：{out_path}", file=sys.stderr)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(metrics, readiness))


if __name__ == "__main__":
    main()
