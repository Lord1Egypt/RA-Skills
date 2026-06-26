#!/usr/bin/env python3
"""
持仓优化建议功能

根据当前持仓 + 目标仓位 + 市场技术位
给出"现在该买什么、买多少"的明确建议

使用方式：
  python3 recommend.py              # 完整建议报告
  python3 recommend.py --threshold # 仅显示偏离超阈值项
  python3 recommend.py --dry-run   # 模拟，不推送
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from positions import get_all_positions
from fund_api import fetch_otc_fund_valuation, fetch_otc_fund_history
from technical import calc_rsi, calc_macd, calc_bollinger_bands

# ============ 目标仓位配置（示例模板）============
# 请根据个人风险偏好修改以下配置
TOTAL_TARGET = 10000  # 示例总目标（元），请替换为你的实际总投入

TARGET_ALLOCATION = {
    "000001": {"name": "示例混合型基金A",   "ratio": 0.25, "threshold": 0.05},
    "000002": {"name": "示例混合型基金B",   "ratio": 0.15, "threshold": 0.05},
    "000003": {"name": "示例债券型基金",     "ratio": 0.30, "threshold": 0.05},
    "000004": {"name": "示例黄金ETF联接",   "ratio": 0.15, "threshold": 0.05},
    "000005": {"name": "示例养老FOF",       "ratio": 0.10, "threshold": 0.03},
    "000006": {"name": "示例白银LOF",       "ratio": 0.05, "threshold": 0.03},
}

# ============ 建仓优先级评分 ============

def score_entry_opportunity(code: str) -> dict:
    """
    评估单只基金的建仓机会分数（0-100）
    分数越高 = 技术位越好，越适合现在买入
    """
    # 获取历史数据（倒序，最新在前）
    hist = fetch_otc_fund_history(code, days=60)
    if not hist or len(hist) < 20:
        return {"score": 50, "reason": "数据不足，默认中性", "rsi": 50, "boll_pos": 50}

    prices = [r["nav"] for r in hist]

    # 计算技术指标
    rsi = calc_rsi(prices, 14) or 50
    dif, dea, macd_hist = calc_macd(prices)
    boll_upper, boll_mid, boll_lower = calc_bollinger_bands(prices, 20)

    # 布林带位置：价格在中轨下方=安全，上轨附近=危险
    latest = prices[0]
    if boll_mid and boll_lower and boll_mid > boll_lower:
        boll_pos = (latest - boll_lower) / (boll_mid - boll_lower) * 100
    else:
        boll_pos = 50

    macd_signal = dif - dea if (dif is not None and dea is not None) else 0

    score = 50
    reasons = []

    # RSI评估
    if rsi < 30:
        score += 25
        reasons.append(f"RSI超卖{rsi:.0f}，低位买入机会好")
    elif rsi < 40:
        score += 15
        reasons.append(f"RSI偏低({rsi:.0f})，处于买入区间")
    elif rsi > 70:
        score -= 20
        reasons.append(f"RSI超买({rsi:.0f})，暂不追加")
    elif rsi > 60:
        score -= 5
        reasons.append(f"RSI偏高({rsi:.0f})，不急")

    # MACD评估
    if macd_signal > 0:
        score += 10
        reasons.append("MACD金叉信号，上涨动力积蓄中")
    elif macd_signal < -0.01:
        score -= 5
        reasons.append("MACD开口向下，短线承压")

    # 布林带评估
    if boll_pos < 30:
        score += 15
        reasons.append(f"价格处于布林下轨附近({boll_pos:.0f}%)，安全边际高")
    elif boll_pos > 70:
        score -= 10
        reasons.append(f"价格处于布林上轨({boll_pos:.0f}%)，向上空间有限")

    score = max(0, min(100, score))
    return {
        "score": score,
        "reason": "; ".join(reasons) if reasons else "技术位中性，无明显信号",
        "rsi": rsi,
        "macd_signal": macd_signal,
        "boll_pos": boll_pos,
    }


def generate_recommendation():
    """生成建仓优化建议"""
    # 1. 获取当前持仓
    positions = get_all_positions()
    position_value = 0.0
    position_by_code = {}

    for code, pos in positions.items():
        val = fetch_otc_fund_valuation(code)
        nav = val.get("nav", 0) if val else 0
        current_val = nav * pos["total_quantity"]
        position_value += current_val
        position_by_code[code] = {
            "shares": pos["total_quantity"],
            "avg_cost": pos["avg_cost"],
            "nav": nav,
            "current_value": current_val,
        }

    # 2. 计算各基金目标市值和缺口
    gaps = []
    for code, cfg in TARGET_ALLOCATION.items():
        target_value = TOTAL_TARGET * cfg["ratio"]
        current = position_by_code.get(code, {}).get("current_value", 0)
        gap = target_value - current
        gaps.append({
            "code": code,
            "name": cfg["name"],
            "target_value": target_value,
            "current_value": current,
            "gap": gap,
            "ratio": cfg["ratio"],
            "threshold": cfg["threshold"],
        })

    # 3. 评估每只基金的建仓机会分数
    for g in gaps:
        if g["gap"] > 10:  # 只对有建仓缺口的基金评分
            opp = score_entry_opportunity(g["code"])
            g["score"] = opp["score"]
            g["reason"] = opp["reason"]
            g["rsi"] = opp.get("rsi", None)
            g["boll_pos"] = opp.get("boll_pos", None)
        else:
            g["score"] = 0
            g["reason"] = "已接近或超过目标仓位"

    # 4. 过滤掉已建仓足够的
    actionable = [g for g in gaps if g["gap"] > 10]

    # 5. 按综合分排序：缺口权重60% + 技术位权重40%
    for g in actionable:
        # 缺口越大，优先级越高（归一化到0-100）
        gap_score = min(g["gap"] / (TOTAL_TARGET * 0.15) * 100, 100)  # 假设最大单一缺口15%
        g["combined_score"] = gap_score * 0.6 + g["score"] * 0.4

    actionable.sort(key=lambda x: -x["combined_score"])

    return {
        "total_target": TOTAL_TARGET,
        "position_value": position_value,
        "invested_ratio": position_value / TOTAL_TARGET * 100,
        "remaining": TOTAL_TARGET - position_value,
        "gaps": gaps,
        "actionable": actionable,
    }


def format_recommendation_report():
    """格式化输出建议报告"""
    data = generate_recommendation()

    lines = []
    lines.append("🎯 持仓优化建议报告")
    lines.append("=" * 40)
    lines.append(f"总目标：{data['total_target']:.0f}元")
    lines.append(f"已投：{data['position_value']:.0f}元 ({data['invested_ratio']:.1f}%)")
    lines.append(f"待投：{data['remaining']:.0f}元")
    lines.append("")

    # 当前持仓状态
    lines.append("【当前持仓状态】")
    invested = [g for g in data["gaps"] if g["current_value"] > 0]
    if invested:
        for g in invested:
            gap_pct = g["current_value"] / g["target_value"] * 100 if g["target_value"] > 0 else 0
            lines.append(
                f"  {g['name']}({g['code']})\n"
                f"    当前: {g['current_value']:.0f}元 / 目标: {g['target_value']:.0f}元 ({gap_pct:.0f}%)\n"
                f"    {g['reason']}"
            )
    else:
        lines.append("  暂无持仓")
    lines.append("")

    # 建仓建议（按优先级排序）
    actionable = data["actionable"]
    if not actionable:
        lines.append("✅ 仓位已接近目标，无需追加")
        return "\n".join(lines)

    lines.append("【建仓建议】（按优先级排序）")
    lines.append(f"说明：综合考虑「缺口大小(60%) + 技术位(40%)」排序")
    lines.append("")

    for i, g in enumerate(actionable[:6], 1):  # 最多6只
        # 计算建议买入份数
        nav = position_nav(g["code"])
        if nav and nav > 0:
            buy_shares = g["gap"] / nav
            buy_shares = int(buy_shares)  # 取整

            emoji = "🔴" if g["score"] < 40 else ("🟡" if g["score"] < 60 else "🟢")
            lines.append(
                f"{emoji} {i}. {g['name']}({g['code']})\n"
                f"   目标仓位: {g['ratio']*100:.0f}% = {g['target_value']:.0f}元\n"
                f"   缺口: {g['gap']:.0f}元 → 建议买入 ~{buy_shares}份 (净值{nav:.4f})\n"
                f"   技术位: {g['reason']}\n"
                f"   综合评分: {g['combined_score']:.0f}/100"
            )
            lines.append("")

    # 执行前提
    lines.append("【操作原则】")
    lines.append("  1. 先建债券和黄金底仓，再追混合型")
    lines.append("  2. 分3批次建仓：今天/1周后/2周后，各买1/3")
    lines.append("  3. 任何单只基金单次买入不超过目标仓位的50%")

    return "\n".join(lines)


def position_nav(code):
    """获取基金净值"""
    val = fetch_otc_fund_valuation(code)
    return val.get("nav", 0) if val else 0


if __name__ == "__main__":
    print(format_recommendation_report())
