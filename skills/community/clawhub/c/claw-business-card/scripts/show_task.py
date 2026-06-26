#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
show_task.py — 查看任务详情，包括完整交流日志
用法: python show_task.py --workspace <path> --task-id <id>
      python show_task.py --workspace <path> --list
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


def show_task(workspace: Path, task_id: str):
    net_dir = workspace / "agent-network"
    task_path = net_dir / "tasks" / f"{task_id}.json"
    
    if not task_path.exists():
        print(f"[ERROR] 任务 {task_id} 不存在")
        sys.exit(1)
    
    task = json.loads(task_path.read_text(encoding="utf-8"))
    
    print(f"\n{'='*60}")
    print(f"任务详情 - {task.get('title', '未命名')}")
    print(f"{'='*60}")
    print(f"  任务ID:    {task.get('taskId')}")
    print(f"  角色:      {'委托方' if task.get('role') == 'requester' else '承接方'}")
    print(f"  状态:      {task.get('status')}")
    print(f"  好友:      {task.get('counterpartyName', '---')}")
    print(f"  预算上限:  {task.get('budgetLimit', '---')} AgentToken")
    print(f"  截止时间:  {format_time(task.get('deadline', ''))}")
    print(f"  创建时间:  {format_time(task.get('createdAt', ''))}")
    print(f"  更新时间:  {format_time(task.get('updatedAt', ''))}")
    
    print(f"\n--- 任务描述 ---")
    print(f"  {task.get('description', '---')}")
    
    if task.get("result"):
        print(f"\n--- 任务结果 ---")
        result = task["result"]
        print(f"  格式:      {result.get('format', 'text')}")
        print(f"  内容:      {result.get('content', '---')[:200]}...")
        print(f"  收到时间:  {format_time(result.get('receivedAt', ''))}")
    
    if task.get("bill"):
        print(f"\n--- 账单 ---")
        bill = task["bill"]
        print(f"  Token 消耗:  {bill.get('tokenCount', 0):,}")
        print(f"  基础费率:    {bill.get('ratePerKToken')} AgentToken/K")
        print(f"  基础成本:    {bill.get('baseCost')} AgentToken")
        print(f"  利润率:      {bill.get('profitMargin', 0) * 100:.0f}%")
        print(f"  利润金额:    {bill.get('profitAmount')} AgentToken")
        print(f"  ─────────────────")
        print(f"  账单总额:    {bill.get('totalAmount')} AgentToken")
        print(f"  账单状态:    {bill.get('status')}")
    
    if task.get("timeline"):
        print(f"\n--- 交流日志 ---")
        for entry in task["timeline"]:
            print(f"  [{format_time(entry.get('time', ''))}] {entry.get('event')}")
            print(f"    {entry.get('note', '')}")
    
    print(f"\n{'='*60}")


def list_tasks(workspace: Path):
    net_dir = workspace / "agent-network"
    tasks_dir = net_dir / "tasks"
    
    if not tasks_dir.exists():
        print("[INFO] 暂无任务记录")
        return
    
    task_files = list(tasks_dir.glob("*.json"))
    if not task_files:
        print("[INFO] 暂无任务记录")
        return
    
    print(f"\n{'='*60}")
    print(f"任务列表 (共 {len(task_files)} 个)")
    print(f"{'='*60}")
    print(f"{'任务ID':<8} {'标题':<20} {'角色':<6} {'状态':<10} {'好友':<10}")
    print(f"{'-'*60}")
    
    for tf in sorted(task_files, key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            task = json.loads(tf.read_text(encoding="utf-8"))
            task_id = task.get("taskId", "")[:8]
            title = task.get("title", "未命名")[:18]
            role = "委托" if task.get("role") == "requester" else "承接"
            status = task.get("status", "unknown")[:8]
            friend = task.get("counterpartyName", "---")[:8]
            print(f"{task_id:<8} {title:<20} {role:<6} {status:<10} {friend:<10}")
        except Exception:
            pass
    
    print(f"{'='*60}")


if __name__ == "__main__":
    args = parse_args()
    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent
    
    task_id = args.get("task_id")
    
    if args.get("list"):
        list_tasks(workspace)
    elif task_id:
        show_task(workspace, task_id)
    else:
        print("用法: show_task.py --task-id <id> | --list")
        sys.exit(1)
