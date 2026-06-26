#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
show_ledger.py — 格式化展示账本摘要
用法: python show_ledger.py [--workspace <path>] [--limit <n>] [--filter earn|spend|all]
"""
import json
from pathlib import Path
from datetime import datetime


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


def format_time(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str[:16] if iso_str else "---"


def show_ledger(workspace: Path, limit: int = 10, tx_filter: str = "all"):
    net_dir = workspace / "agent-network"
    ledger_path = net_dir / "ledger.json"

    if not ledger_path.exists():
        print("[ERROR] 账本不存在，请先运行 init.py 初始化")
        sys.exit(1)

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

    print("\n=== Agent Token 账本 ===")
    print(f"  当前余额:  {ledger['balance']:.4f} AgentToken")
    print(f"  累计收入:  {ledger['totalEarned']:.4f} AgentToken")
    print(f"  累计支出:  {ledger['totalSpent']:.4f} AgentToken")
    print("=" * 60)

    txs = ledger.get("transactions", [])

    # 过滤
    if tx_filter != "all":
        txs = [t for t in txs if t.get("type") == tx_filter]

    # 最新在前
    txs = list(reversed(txs))[:limit]

    if not txs:
        print("\n  暂无交易记录")
    else:
        print(f"\n  最近 {len(txs)} 条交易记录：\n")
        for tx in txs:
            tx_type = tx.get("type", "?")
            amount = tx.get("amount", 0)
            sign = "+" if tx_type in ("earn", "topup") else "-"
            color_tag = "[+]" if sign == "+" else "[-]"
            print(f"  {color_tag} [{format_time(tx.get('createdAt', ''))}] "
                  f"{sign}{amount:.4f} AgentToken")
            print(f"     类型: {tx_type}  |  对方: {tx.get('counterpartyName', '---')}")
            print(f"     说明: {tx.get('description', '---')}")
            if tx.get("tokenCount"):
                print(f"     Token: {tx['tokenCount']:,}  |  利润率: {tx.get('profitMargin', 0) * 100:.0f}%")
            print()

    # 任务统计
    tasks_dir = net_dir / "tasks"
    if tasks_dir.exists():
        task_files = list(tasks_dir.glob("*.json"))
        statuses = {}
        for tf in task_files:
            try:
                t = json.loads(tf.read_text(encoding="utf-8"))
                s = t.get("status", "unknown")
                statuses[s] = statuses.get(s, 0) + 1
            except Exception:
                pass

        if statuses:
            print("  任务统计：")
            for status, count in sorted(statuses.items()):
                print(f"    {status}: {count} 个")

    print()


if __name__ == "__main__":
    args = parse_args()
    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent
    limit = int(args.get("limit", 10))
    tx_filter = args.get("filter", "all")
    show_ledger(workspace, limit, tx_filter)
