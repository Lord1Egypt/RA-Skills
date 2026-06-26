#!/usr/bin/env python3
"""
calculate-cost.py — 根据 billing-rules.json 计算 OpenClaw session 成本

用法：
  python3 calculate-cost.py                    # 读取 stdin 的 JSON 数据
  python3 calculate-cost.py --file data.json   # 从文件读取
  python3 calculate-cost.py --session-status   # 解析 session_status 输出

输入格式（JSON 数组）：
[
  {"agent": "main", "model": "claude-3-sonnet", "input_tokens": 1000, "output_tokens": 500},
  ...
]
"""
import json
import sys
import os
import argparse
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
BILLING_RULES_PATH = SKILL_DIR / "references" / "billing-rules.json"
BUDGET_CONFIG_PATH = SKILL_DIR / "references" / "budget-config.yaml"


def load_billing_rules():
    with open(BILLING_RULES_PATH) as f:
        return json.load(f)


def get_model_rate(billing_rules, model_str):
    """从 billing_rules 中查找模型单价，支持 provider/model 格式"""
    providers = billing_rules.get("llm_providers", {})
    # 尝试 provider/model 格式
    if "/" in model_str:
        provider, model = model_str.split("/", 1)
        if provider in providers and model in providers[provider]:
            return providers[provider][model]
    # 直接匹配 model 名
    for provider_rates in providers.values():
        if model_str in provider_rates:
            return provider_rates[model_str]
    return None


def calculate_cost(records, billing_rules):
    """计算成本，返回 (total_usd, agent_costs, unknown_models)"""
    usd_to_cny = billing_rules.get("usd_to_cny", 7.2)
    agent_costs = {}
    unknown_models = set()
    total_usd = 0.0

    for rec in records:
        agent = rec.get("agent", "unknown")
        model = rec.get("model", "")
        input_tokens = rec.get("input_tokens", 0)
        output_tokens = rec.get("output_tokens", 0)

        rate = get_model_rate(billing_rules, model)
        if rate is None:
            unknown_models.add(model)
            cost_usd = 0.0
        else:
            cost_usd = (input_tokens * rate["input"] + output_tokens * rate["output"]) / 1000

        total_usd += cost_usd
        agent_costs[agent] = agent_costs.get(agent, 0.0) + cost_usd

    total_cny = total_usd * usd_to_cny
    agent_costs_cny = {k: v * usd_to_cny for k, v in agent_costs.items()}
    return total_cny, agent_costs_cny, unknown_models


def format_report(total_cny, agent_costs_cny, budget_daily=500):
    pct = total_cny / budget_daily * 100 if budget_daily else 0
    status = "✅" if pct < 50 else ("🟡" if pct < 80 else "🔴")

    lines = [
        f"📊 成本报告",
        f"总成本：¥{total_cny:.2f} / ¥{budget_daily:.0f}（预算）",
        f"使用率：{pct:.1f}% {status}",
        "",
        "分项明细（按 agent）：",
    ]
    for agent, cost in sorted(agent_costs_cny.items(), key=lambda x: -x[1]):
        lines.append(f"  • {agent}：¥{cost:.2f}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="输入 JSON 文件路径")
    parser.add_argument("--budget", type=float, default=500, help="每日预算（元）")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            records = json.load(f)
    else:
        records = json.load(sys.stdin)

    billing_rules = load_billing_rules()
    total_cny, agent_costs_cny, unknown_models = calculate_cost(records, billing_rules)

    print(format_report(total_cny, agent_costs_cny, args.budget))
    if unknown_models:
        print(f"\n⚠️ 未知模型（成本未计入）：{', '.join(unknown_models)}")
        print("请更新 references/billing-rules.json 添加对应计费规则。")


if __name__ == "__main__":
    main()
