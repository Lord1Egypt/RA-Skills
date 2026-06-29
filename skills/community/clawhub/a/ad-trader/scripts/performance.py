#!/usr/bin/env python3
"""
广告投手 - 投放分析模块
KPI计算、异常检测、趋势分析、对比分析、计划诊断
"""

import sys
import json
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from data_manager import load_file, get_summary


def compute_kpi(records: list) -> dict:
    """计算核心KPI"""
    s = get_summary(records)
    return {
        "overview": s,
        "score": None,  # 后续评分
    }


def anomaly_detect(records: list, thresholds: dict = None) -> list:
    """
    异常检测
    thresholds: {"cpa_spike_pct": 50, "ctr_drop_pct": 30, "budget_burn_rate": 0.8}
    """
    if thresholds is None:
        thresholds = {"cpa_spike_pct": 50, "ctr_drop_pct": 30, "budget_burn_rate": 0.8}

    anomalies = []

    # 按日期分组
    daily_data = group_by_date(records)
    if len(daily_data) < 3:
        anomalies.append({
            "type": "数据不足",
            "severity": "warning",
            "message": "数据天数不足3天，无法进行可靠的异常检测",
            "suggestion": "积累更多数据后再分析"
        })
        return anomalies

    dates = sorted(daily_data.keys())

    # 1. 检测CPA突增
    for i in range(1, len(dates)):
        prev = daily_data[dates[i - 1]]
        curr = daily_data[dates[i]]
        prev_cpa = prev.get("cpa")
        curr_cpa = curr.get("cpa")
        if prev_cpa and curr_cpa and prev_cpa > 0:
            change_pct = (curr_cpa - prev_cpa) / prev_cpa * 100
            if change_pct > thresholds["cpa_spike_pct"]:
                anomalies.append({
                    "type": "CPA突增",
                    "severity": "critical" if change_pct > 100 else "warning",
                    "date": dates[i],
                    "prev_cpa": round(prev_cpa, 2),
                    "curr_cpa": round(curr_cpa, 2),
                    "change_pct": round(change_pct, 1),
                    "message": f"{dates[i]} CPA较前日上涨{change_pct:.0f}%: ¥{prev_cpa:.2f} → ¥{curr_cpa:.2f}",
                    "suggestion": "检查是否有新素材/新计划导致成本拉高，排查低效计划"
                })

    # 2. 检测CTR骤降
    for i in range(1, len(dates)):
        prev = daily_data[dates[i - 1]]
        curr = daily_data[dates[i]]
        prev_ctr = prev.get("ctr")
        curr_ctr = curr.get("ctr")
        if prev_ctr and curr_ctr and prev_ctr > 0:
            change_pct = (prev_ctr - curr_ctr) / prev_ctr * 100
            if change_pct > thresholds["ctr_drop_pct"]:
                anomalies.append({
                    "type": "CTR骤降",
                    "severity": "critical" if change_pct > 50 else "warning",
                    "date": dates[i],
                    "prev_ctr": round(prev_ctr * 100, 2),
                    "curr_ctr": round(curr_ctr * 100, 2),
                    "change_pct": round(change_pct, 1),
                    "message": f"{dates[i]} CTR较前日下降{change_pct:.0f}%: {prev_ctr*100:.1f}% → {curr_ctr*100:.1f}%",
                    "suggestion": "素材可能疲劳，建议更换新素材；或检查定向是否过窄"
                })

    # 3. 检测消耗异常
    avg_daily_cost = sum(d.get("cost", 0) for d in daily_data.values()) / len(daily_data)
    for date_str in dates:
        daily = daily_data[date_str]
        cost = daily.get("cost", 0)
        if avg_daily_cost > 0 and cost > avg_daily_cost * 2:
            anomalies.append({
                "type": "消耗暴增",
                "severity": "warning",
                "date": date_str,
                "cost": round(cost, 2),
                "avg_cost": round(avg_daily_cost, 2),
                "message": f"{date_str} 消耗 {cost:.2f} 超过日均 {avg_daily_cost:.2f} 的2倍",
                "suggestion": "检查是否有计划预算被放大、出价是否异常"
            })
        if avg_daily_cost > 0 and cost < avg_daily_cost * 0.3 and cost > 0:
            anomalies.append({
                "type": "消耗骤降",
                "severity": "warning",
                "date": date_str,
                "cost": round(cost, 2),
                "avg_cost": round(avg_daily_cost, 2),
                "message": f"{date_str} 消耗 {cost:.2f} 低于日均 {avg_daily_cost:.2f} 的30%",
                "suggestion": "检查计划是否被暂停、出价是否过低、审核是否被拒"
            })

    # 4. ROAS持续下降趋势
    recent_dates = dates[-3:] if len(dates) >= 3 else dates
    recent_roas = [daily_data[d].get("roas", 0) for d in recent_dates]
    if len(recent_roas) >= 3 and all(recent_roas[i] > 0 and recent_roas[i] < recent_roas[i - 1] for i in range(1, len(recent_roas))):
        anomalies.append({
            "type": "ROAS持续下降",
            "severity": "critical",
            "date": recent_dates[-1],
            "roas_trend": [round(r, 2) for r in recent_roas],
            "message": f"近{len(recent_dates)}天ROAS持续下降: {' → '.join(str(round(r,2)) for r in recent_roas)}",
            "suggestion": "紧急排查素材疲劳和人群耗尽，必要时暂停低效计划止损"
        })

    # 5. CVR波动检测
    for i in range(1, len(dates)):
        prev = daily_data[dates[i - 1]]
        curr = daily_data[dates[i]]
        prev_cvr = prev.get("cvr")
        curr_cvr = curr.get("cvr")
        if prev_cvr and curr_cvr and prev_cvr > 0:
            change_pct = (prev_cvr - curr_cvr) / prev_cvr * 100
            if change_pct > 30:
                anomalies.append({
                    "type": "CVR骤降",
                    "severity": "critical" if change_pct > 50 else "warning",
                    "date": dates[i],
                    "prev_cvr": round(prev_cvr * 100, 2),
                    "curr_cvr": round(curr_cvr * 100, 2),
                    "change_pct": round(change_pct, 1),
                    "message": f"{dates[i]} CVR较前日下降{change_pct:.0f}%: {prev_cvr*100:.1f}% → {curr_cvr*100:.1f}%",
                    "suggestion": "检查落地页是否正常加载、转化链路是否顺畅"
                })

    # 按严重度排序
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    anomalies.sort(key=lambda x: severity_order.get(x.get("severity"), 3))

    # 去重（同类型同日期）
    seen = set()
    unique = []
    for a in anomalies:
        key = (a["type"], a.get("date", ""))
        if key not in seen:
            seen.add(key)
            unique.append(a)

    return unique


def group_by_date(records: list) -> dict:
    """按日期聚合数据"""
    daily = defaultdict(lambda: {"impressions": 0, "clicks": 0, "cost": 0, "conversions": 0, "revenue": 0})
    for r in records:
        date_str = str(r.get("date", "unknown"))
        daily[date_str]["impressions"] += r.get("impressions", 0) or 0
        daily[date_str]["clicks"] += r.get("clicks", 0) or 0
        daily[date_str]["cost"] += r.get("cost", 0) or 0
        daily[date_str]["conversions"] += r.get("conversions", 0) or 0
        daily[date_str]["revenue"] += r.get("revenue", 0) or 0

    for d in daily.values():
        if d["impressions"] > 0:
            d["ctr"] = d["clicks"] / d["impressions"]
            d["cpm"] = d["cost"] / d["impressions"] * 1000
        if d["clicks"] > 0:
            d["cvr"] = d["conversions"] / d["clicks"]
            d["cpc"] = d["cost"] / d["clicks"]
        if d["conversions"] > 0:
            d["cpa"] = d["cost"] / d["conversions"]
        if d["cost"] > 0:
            d["roas"] = d["revenue"] / d["cost"]
            d["roi"] = (d["revenue"] - d["cost"]) / d["cost"]

    return dict(daily)


def group_by_campaign(records: list) -> dict:
    """按计划聚合数据"""
    campaigns = defaultdict(lambda: {"impressions": 0, "clicks": 0, "cost": 0, "conversions": 0, "revenue": 0})
    for r in records:
        camp = r.get("campaign", "未命名")
        campaigns[camp]["impressions"] += r.get("impressions", 0) or 0
        campaigns[camp]["clicks"] += r.get("clicks", 0) or 0
        campaigns[camp]["cost"] += r.get("cost", 0) or 0
        campaigns[camp]["conversions"] += r.get("conversions", 0) or 0
        campaigns[camp]["revenue"] += r.get("revenue", 0) or 0

    result = {}
    for name, d in campaigns.items():
        info = {"name": name, **d}
        if d["impressions"] > 0:
            info["ctr"] = round(d["clicks"] / d["impressions"] * 100, 2)
            info["cpm"] = round(d["cost"] / d["impressions"] * 1000, 2)
        if d["clicks"] > 0:
            info["cvr"] = round(d["conversions"] / d["clicks"] * 100, 2)
            info["cpc"] = round(d["cost"] / d["clicks"], 2)
        if d["conversions"] > 0:
            info["cpa"] = round(d["cost"] / d["conversions"], 2)
        if d["cost"] > 0:
            info["roas"] = round(d["revenue"] / d["cost"], 2)
            info["roi"] = round((d["revenue"] - d["cost"]) / d["cost"] * 100, 1)
        info["revenue"] = round(d["revenue"], 2)
        info["cost"] = round(d["cost"], 2)
        result[name] = info

    return result


def trend_analysis(records: list) -> dict:
    """趋势分析"""
    daily = group_by_date(records)
    dates = sorted(daily.keys())
    if len(dates) < 2:
        return {"error": "数据天数不足，无法分析趋势"}

    # CTRA趋势
    ctr_trend = [{"date": d, "value": round(daily[d].get("ctr", 0) * 100, 2)} for d in dates]

    # CVR趋势
    cvr_trend = [{"date": d, "value": round(daily[d].get("cvr", 0) * 100, 2)} for d in dates]

    # CPA趋势
    cpa_trend = [{"date": d, "value": round(daily[d].get("cpa", 0), 2)} for d in dates]

    # ROAS趋势
    roas_trend = [{"date": d, "value": round(daily[d].get("roas", 0), 2)} for d in dates]

    # 消耗趋势
    cost_trend = [{"date": d, "value": round(daily[d].get("cost", 0), 2)} for d in dates]

    # 最近3天趋势方向
    recent_ctr = [d["value"] for d in ctr_trend[-3:]] if len(ctr_trend) >= 3 else []
    recent_cpa = [d["value"] for d in cpa_trend[-3:]] if len(cpa_trend) >= 3 else []

    ctr_direction = "上升" if len(recent_ctr) >= 2 and recent_ctr[-1] > recent_ctr[0] else "下降"
    cpa_direction = "上升" if len(recent_cpa) >= 2 and recent_cpa[-1] > recent_cpa[0] else "下降"

    return {
        "date_count": len(dates),
        "ctr_trend": ctr_trend,
        "cvr_trend": cvr_trend,
        "cpa_trend": cpa_trend,
        "roas_trend": roas_trend,
        "cost_trend": cost_trend,
        "ctr_direction": ctr_direction,
        "cpa_direction": cpa_direction,
        "health_signal": "良好" if ctr_direction == "上升" and cpa_direction == "下降" else (
            "预警" if ctr_direction == "下降" and cpa_direction == "上升" else "需关注"
        ),
    }


def campaign_ranking(records: list) -> dict:
    """计划排行榜"""
    campaigns = group_by_campaign(records)
    camp_list = list(campaigns.values())

    # 按ROAS排名
    roas_rank = sorted(camp_list, key=lambda x: x.get("roas", 0), reverse=True)
    # 按消耗排名
    cost_rank = sorted(camp_list, key=lambda x: x.get("cost", 0), reverse=True)
    # 按CPA排名（越低越好）
    cpa_rank = sorted(camp_list, key=lambda x: x.get("cpa", 999999))

    # 综合评分（消耗权重0.3 + ROAS权重0.4 + CPA倒数权重0.3）
    max_cost = max(c.get("cost", 0) for c in camp_list) or 1
    max_roas = max(c.get("roas", 0) for c in camp_list) or 1
    min_cpa = min(c.get("cpa", 1) for c in camp_list) or 1

    for c in camp_list:
        score_cost = (c.get("cost", 0) / max_cost) * 30
        score_roas = (c.get("roas", 0) / max_roas) * 40 if max_roas > 0 else 0
        cpa_val = c.get("cpa", min_cpa)
        score_cpa = (min_cpa / cpa_val) * 30 if cpa_val > 0 else 0
        c["score"] = round(score_cost + score_roas + score_cpa, 1)

    overall_rank = sorted(camp_list, key=lambda x: x.get("score", 0), reverse=True)

    return {
        "top_by_roas": roas_rank[:5],
        "top_by_cost": cost_rank[:5],
        "top_by_cpa": cpa_rank[:5],
        "overall_ranking": overall_rank,
    }


def diagnose(records: list) -> dict:
    """综合诊断"""
    summary = get_summary(records)
    anomalies = anomaly_detect(records)
    trends = trend_analysis(records)
    ranking = campaign_ranking(records)

    # 健康评分（满分100）
    score = 100
    issues = []

    # ROAS评估
    roas = summary.get("roas", 0)
    if roas < 1:
        score -= 30
        issues.append({"severity": "critical", "item": "ROAS", "message": f"ROAS={roas}<1，投放处于亏损状态"})
    elif roas < 1.5:
        score -= 15
        issues.append({"severity": "warning", "item": "ROAS", "message": f"ROAS={roas}偏低，仅勉强持平"})
    elif roas < 2:
        score -= 5
        issues.append({"severity": "info", "item": "ROAS", "message": f"ROAS={roas}一般，有优化空间"})

    # CPA评估
    cpa = summary.get("avg_cpa", 0)
    if cpa > 100:
        score -= 20
        issues.append({"severity": "warning", "item": "CPA", "message": f"平均CPA=¥{cpa:.2f}偏高"})

    # CTR评估
    avg_ctr = summary.get("avg_ctr", 0)
    if avg_ctr < 1:
        score -= 15
        issues.append({"severity": "warning", "item": "CTR", "message": f"平均CTR={avg_ctr}%偏低，素材吸引力不足"})

    # CVR评估
    avg_cvr = summary.get("avg_cvr", 0)
    if avg_cvr < 1:
        score -= 15
        issues.append({"severity": "warning", "item": "CVR", "message": f"平均CVR={avg_cvr}%偏低，落地页或产品需优化"})

    # 异常情况扣分
    critical_anomalies = [a for a in anomalies if a.get("severity") == "critical"]
    score -= len(critical_anomalies) * 10

    score = max(0, min(100, score))

    # 评级
    if score >= 80:
        grade = "优秀"
    elif score >= 60:
        grade = "良好"
    elif score >= 40:
        grade = "需关注"
    else:
        grade = "严重"

    return {
        "health_score": score,
        "grade": grade,
        "summary": summary,
        "issues": issues,
        "anomalies": anomalies,
        "trends": trends,
        "ranking": ranking,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python performance.py <数据文件路径> [--diagnose] [--anomaly] [--trend] [--rank]")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        records, platform, meta = load_file(file_path)

        if "--diagnose" in sys.argv or len(sys.argv) == 2:
            result = diagnose(records)
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        elif "--anomaly" in sys.argv:
            anomalies = anomaly_detect(records)
            print(json.dumps(anomalies, ensure_ascii=False, indent=2, default=str))
        elif "--trend" in sys.argv:
            trends = trend_analysis(records)
            print(json.dumps(trends, ensure_ascii=False, indent=2, default=str))
        elif "--rank" in sys.argv:
            ranking = campaign_ranking(records)
            print(json.dumps(ranking, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
