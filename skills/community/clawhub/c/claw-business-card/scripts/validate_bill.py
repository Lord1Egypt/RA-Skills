#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
validate_bill.py — 验证账单合理性
用法: python validate_bill.py --bill-json '<json>' --budget-limit <amount>
      或: python validate_bill.py --bill-file <path> --budget-limit <amount>
返回: OK 或 DISPUTED（含原因）
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


def validate_bill(bill: dict, budget_limit: float) -> tuple[bool, list[str]]:
    """
    验证账单合理性
    返回: (is_valid, [错误原因列表])
    """
    errors = []

    token_count = bill.get("tokenCount", 0)
    rate = bill.get("ratePerKToken", 0)
    base_cost = bill.get("baseCost", 0)
    profit_amount = bill.get("profitAmount", 0)
    profit_margin = bill.get("profitMargin", 0)
    total_amount = bill.get("totalAmount", 0)

    # 规则1: Token 消耗为正数
    if token_count <= 0:
        errors.append(f"Token 消耗必须为正数，实际: {token_count}")

    # 规则2: 不超过预算上限的 120%
    max_allowed = budget_limit * 1.2
    if total_amount > max_allowed:
        errors.append(
            f"账单总额 {total_amount} 超过预算上限 {budget_limit} 的 120%（最高允许 {max_allowed:.4f}）"
        )

    # 规则3: 利润率在 10%–50% 之间
    if profit_margin < 0.10 or profit_margin > 0.50:
        errors.append(
            f"利润率 {profit_margin * 100:.1f}% 超出合理范围（10%–50%）"
        )

    # 规则4: 金额计算一致性
    expected_total = round(base_cost + profit_amount, 6)
    if abs(total_amount - expected_total) > 0.0001:
        errors.append(
            f"账单总额计算不一致：{base_cost} + {profit_amount} = {expected_total}，但账单显示 {total_amount}"
        )

    # 规则5: 基础成本计算正确
    if rate > 0 and token_count > 0:
        expected_base = round((token_count / 1000) * rate, 6)
        if abs(base_cost - expected_base) > 0.0001:
            errors.append(
                f"基础成本计算不一致：({token_count}/1000) x {rate} = {expected_base}，但账单显示 {base_cost}"
            )

    return len(errors) == 0, errors


if __name__ == "__main__":
    args = parse_args()

    # 读取账单
    bill = None
    if "bill_json" in args:
        bill = json.loads(args["bill_json"])
    elif "bill_file" in args:
        bill = json.loads(Path(args["bill_file"]).read_text(encoding="utf-8"))
    else:
        print("[ERROR] 需要 --bill-json 或 --bill-file", file=sys.stderr)
        sys.exit(1)

    budget_limit = float(args.get("budget_limit", 999999))

    is_valid, errors = validate_bill(bill, budget_limit)

    print("\n=== 账单验证结果 ===")
    print(f"  Token 消耗:  {bill.get('tokenCount', '?'):,}")
    print(f"  账单总额:    {bill.get('totalAmount', '?')} AgentToken")
    print(f"  预算上限:    {budget_limit} AgentToken")
    print(f"  利润率:      {bill.get('profitMargin', 0) * 100:.1f}%")
    print("=" * 40)

    if is_valid:
        print("[OK] 验证通过：账单合理")
        print("\nVALIDATION_RESULT=OK")
    else:
        print("[WARN] 验证失败：账单存在问题")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")
        print("\nVALIDATION_RESULT=DISPUTED")
        print(f"DISPUTE_REASONS={json.dumps(errors, ensure_ascii=False)}")
        sys.exit(2)
