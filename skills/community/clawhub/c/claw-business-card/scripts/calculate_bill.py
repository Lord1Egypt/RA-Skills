#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
calculate_bill.py — 根据 Token 消耗计算含利润的账单
用法: python calculate_bill.py --token-count <n> [--rate <rate>] [--profit-margin <margin>]
                               [--workspace <path>] [--task-id <id>]
输出: JSON 格式账单
"""
import json
from pathlib import Path


def parse_args():
    args = {}
    i = 1
    while i < len(sys.argv):
        key = sys.argv[i].lstrip("-").replace("-", "_")
        if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
            args[key] = sys.argv[i + 1]
            i += 2
        else:
            args[key] = True
            i += 1
    return args


def load_identity_rate(workspace: Path):
    """从 identity.json 读取默认费率和利润率"""
    identity_path = workspace / "agent-network" / "identity.json"
    if identity_path.exists():
        data = json.loads(identity_path.read_text(encoding="utf-8"))
        return data.get("ratePerKToken", 0.01), data.get("profitMargin", 0.20)
    return 0.01, 0.20


def calculate_bill(token_count: int, rate_per_k: float, profit_margin: float) -> dict:
    base_cost = (token_count / 1000) * rate_per_k
    profit_amount = base_cost * profit_margin
    total_amount = base_cost + profit_amount

    return {
        "tokenCount": token_count,
        "ratePerKToken": rate_per_k,
        "baseCost": round(base_cost, 6),
        "profitAmount": round(profit_amount, 6),
        "profitMargin": profit_margin,
        "totalAmount": round(total_amount, 6),
        "currency": "AgentToken"
    }


if __name__ == "__main__":
    args = parse_args()

    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent

    default_rate, default_margin = load_identity_rate(workspace)

    token_count = int(args.get("token_count", 0))
    rate = float(args.get("rate", default_rate))
    margin = float(args.get("profit_margin", default_margin))

    if token_count <= 0:
        print("[ERROR] --token-count 必须为正整数", file=sys.stderr)
        sys.exit(1)

    bill = calculate_bill(token_count, rate, margin)

    print("\n=== 账单明细 ===")
    print(f"  Token 消耗:  {bill['tokenCount']:,} tokens")
    print(f"  基础费率:    {bill['ratePerKToken']} AgentToken/K")
    print(f"  基础成本:    {bill['baseCost']} AgentToken")
    print(f"  利润率:      {bill['profitMargin'] * 100:.0f}%")
    print(f"  利润金额:    {bill['profitAmount']} AgentToken")
    print(f"  ---------------------------------")
    print(f"  账单总额:    {bill['totalAmount']} AgentToken")
    print("=" * 40)
    print(f"\nBILL_JSON={json.dumps(bill)}")
