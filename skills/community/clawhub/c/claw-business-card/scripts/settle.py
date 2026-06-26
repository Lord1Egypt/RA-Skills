#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
settle.py — 完成结算，更新 ledger.json
用法: python settle.py --workspace <path> --task-id <id> --type earn|spend
                       --amount <amount> --counterparty-id <id> --counterparty-name <name>
                       --token-count <n> --rate <rate> --profit-margin <margin>
                       --description <desc>
"""
import json
import uuid
from datetime import datetime, timezone
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


def settle(workspace: Path, args: dict):
    net_dir = workspace / "agent-network"
    ledger_path = net_dir / "ledger.json"

    if not ledger_path.exists():
        print("[ERROR] ledger.json 不存在，请先运行 init.py", file=sys.stderr)
        sys.exit(1)

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

    tx_type = args.get("type", "spend")
    amount = float(args.get("amount", 0))
    task_id = args.get("task_id", "")
    counterparty_id = args.get("counterparty_id", "")
    counterparty_name = args.get("counterparty_name", "")
    token_count = int(args.get("token_count", 0))
    rate = float(args.get("rate", 0.01))
    profit_margin = float(args.get("profit_margin", 0.20))
    description = args.get("description", "任务结算")

    now = datetime.now(timezone.utc).isoformat()

    # 检查余额（仅 spend 类型）
    if tx_type == "spend" and ledger["balance"] < amount:
        print(f"[ERROR] 余额不足：当前余额 {ledger['balance']} AgentToken，需要 {amount} AgentToken", file=sys.stderr)
        sys.exit(1)

    # 计算利润金额
    base_cost = (token_count / 1000) * rate if token_count > 0 else amount / (1 + profit_margin)
    profit_amount = round(base_cost * profit_margin, 6)

    # 创建交易记录
    tx = {
        "txId": str(uuid.uuid4()),
        "type": tx_type,
        "amount": round(amount, 6),
        "taskId": task_id,
        "counterpartyId": counterparty_id,
        "counterpartyName": counterparty_name,
        "description": description,
        "tokenCount": token_count,
        "ratePerKToken": rate,
        "profitAmount": profit_amount,
        "profitMargin": profit_margin,
        "status": "completed",
        "createdAt": now,
        "settledAt": now
    }

    # 更新余额
    if tx_type == "earn":
        ledger["balance"] = round(ledger["balance"] + amount, 6)
        ledger["totalEarned"] = round(ledger["totalEarned"] + amount, 6)
    elif tx_type == "spend":
        ledger["balance"] = round(ledger["balance"] - amount, 6)
        ledger["totalSpent"] = round(ledger["totalSpent"] + amount, 6)
    elif tx_type == "topup":
        ledger["balance"] = round(ledger["balance"] + amount, 6)
        ledger["totalEarned"] = round(ledger["totalEarned"] + amount, 6)
    elif tx_type == "withdraw":
        ledger["balance"] = round(ledger["balance"] - amount, 6)
        ledger["totalSpent"] = round(ledger["totalSpent"] + amount, 6)

    ledger["transactions"].append(tx)

    # 更新任务状态
    if task_id:
        task_path = net_dir / "tasks" / f"{task_id}.json"
        if task_path.exists():
            task = json.loads(task_path.read_text(encoding="utf-8"))
            task["status"] = "completed"
            task["updatedAt"] = now
            if task.get("bill"):
                task["bill"]["status"] = "approved"
                task["bill"]["validatedAt"] = now
            task["timeline"].append({
                "time": now,
                "event": "settled",
                "note": f"结算完成，金额: {amount} AgentToken"
            })
            task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")

    # 保存账本
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    action_word = "收入" if tx_type in ("earn", "topup") else "支出"
    print(f"\n[OK] 结算完成")
    print(f"   交易ID: {tx['txId']}")
    print(f"   类型: {tx_type} ({action_word})")
    print(f"   金额: {amount} AgentToken")
    print(f"   当前余额: {ledger['balance']} AgentToken")
    print(f"\nTX_ID={tx['txId']}")
    print(f"NEW_BALANCE={ledger['balance']}")


if __name__ == "__main__":
    args = parse_args()
    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent
    settle(workspace, args)
