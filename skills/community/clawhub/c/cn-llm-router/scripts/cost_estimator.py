"""跑前成本预估（v2.9.0 新增）。

本地分词器估 token × v2.7 档案价 → 批量任务总成本预估。
- token 估算：复用 text_splitter.estimate_tokens_simple，零依赖、离线
- 价格：复用 price_registry.estimate_cost（models.yaml 档案价）
- 超预算：返回需要显式确认标志，由 CLI 层强制 --yes 才启动

误差目标 ≤15%（实测回填后持续校正；档案缺失的模型标注为不可估）。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import text_splitter
import price_registry


def estimate_batch(items, model_name, out_token_ratio=0.5, overhead_per_item=20):
    """估算批量任务成本。

    items: payload 字符串列表。
    model_name: 目标模型名（用于查档案价）。
    out_token_ratio: 输出 token 按输入的比例估（默认 0.5）。
    overhead_per_item: 每条系统提示/消息封装的额外 token。

    返回 dict:
      count / in_tokens / out_tokens / total_cost / priced_count /
      unpriced_count / avg_cost / currency
    """
    price = price_registry.get_model_price(model_name)
    priced = price is not None
    total_in = 0
    for payload in items:
        total_in += text_splitter.estimate_tokens_simple(str(payload)) + overhead_per_item
    total_out = int(total_in * out_token_ratio)
    cost = price_registry.estimate_cost(model_name, total_in, total_out) if priced else 0.0
    return {
        "count": len(items),
        "model": model_name,
        "in_tokens": total_in,
        "out_tokens": total_out,
        "total_cost": round(cost, 4),
        "priced_count": len(items) if priced else 0,
        "unpriced_count": 0 if priced else len(items),
        "avg_cost": round(cost / len(items), 6) if items else 0.0,
        "priced": priced,
        "price_date": price.get("date", "") if price else "",
        "currency": "CNY",
    }


def budget_gate(estimate, budget, require_yes=True, confirmed=False):
    """预算闸门：超预算时要求显式确认。

    返回 dict: allowed / over_budget / reason / threshold / estimated
    - budget <= 0 表示未设预算，直接放行
    - over_budget 且未 confirmed → allowed=False（CLI 据此拦截）
    """
    over = budget > 0 and estimate["total_cost"] > budget
    allowed = True
    reason = "预算内或已确认"
    if over and require_yes and not confirmed:
        allowed = False
        reason = (
            "预估成本 ¥%.4f 超过预算 ¥%.4f，请确认后加 --yes 启动" %
            (estimate["total_cost"], budget)
        )
    elif over and confirmed:
        reason = "已显式确认（--yes），允许超预算执行"
    return {
        "allowed": allowed,
        "over_budget": over,
        "confirmed": confirmed,
        "reason": reason,
        "threshold": budget,
        "estimated": estimate["total_cost"],
    }


def render_estimate(est, gate=None):
    """人类可读的预估摘要。"""
    lines = []
    lines.append("💰 跑前成本预估（%s）" % est["model"])
    lines.append("  任务数   : %d" % est["count"])
    lines.append("  输入 token: %d（本地分词估算）" % est["in_tokens"])
    lines.append("  输出 token: %d（按输入 %.0f%% 估）" % (
        est["out_tokens"], est["out_tokens"] / est["in_tokens"] * 100 if est["in_tokens"] else 0))
    if est["priced"]:
        lines.append("  预估总成本: ¥%.4f（档案价，采集 %s）" % (est["total_cost"], est["price_date"] or "未知"))
        lines.append("  单条均价  : ¥%.6f" % est["avg_cost"])
    else:
        lines.append("  预估总成本: 无法估算（档案缺此模型价格，执行后按实测计费）")
    if gate:
        if gate["over_budget"]:
            lines.append("  ⚠️  超预算：预估 ¥%.4f > 阈值 ¥%.4f" % (gate["estimated"], gate["threshold"]))
            lines.append("     %s" % gate["reason"])
        else:
            lines.append("  ✅ %s" % gate["reason"])
    return "\n".join(lines)
