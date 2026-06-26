#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
get_token_usage.py — 获取任务的实际 Token 消耗
用法: python get_token_usage.py --workspace <path> --task-id <id>
      或: python get_token_usage.py --session-key <key>
      
输出: 实际 Token 消耗数量
"""
import json
import re
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


def get_task_token_usage(workspace: Path, task_id: str) -> dict:
    """
    从任务记录中获取 Token 消耗
    任务记录中应包含 taskStartTokens 和 taskEndTokens
    """
    task_path = workspace / "agent-network" / "tasks" / f"{task_id}.json"
    if not task_path.exists():
        return {"error": f"任务 {task_id} 不存在", "tokenCount": 0}
    
    task = json.loads(task_path.read_text(encoding="utf-8"))
    
    # 检查是否有记录
    start_tokens = task.get("taskStartTokens")
    end_tokens = task.get("taskEndTokens")
    
    if start_tokens is not None and end_tokens is not None:
        token_count = end_tokens - start_tokens
        return {
            "taskId": task_id,
            "startTokens": start_tokens,
            "endTokens": end_tokens,
            "tokenCount": token_count,
            "estimated": False
        }
    
    # 如果没有精确记录，返回估算
    return {
        "taskId": task_id,
        "tokenCount": 0,
        "estimated": True,
        "note": "请在任务开始和结束时记录 Token 数量"
    }


def estimate_from_conversation(task_description: str) -> int:
    """
    根据任务描述估算 Token 消耗
    这是一个粗略估算，作为备选方案
    """
    # 简单估算规则
    base_tokens = 1000  # 基础开销
    
    # 根据任务类型加量
    if any(kw in task_description for kw in ["搜索", "查找", "search"]):
        base_tokens += 500
    if any(kw in task_description for kw in ["整理", "分析", "report"]):
        base_tokens += 2000
    if any(kw in task_description for kw in ["写", "生成", "create"]):
        base_tokens += 3000
    if any(kw in task_description for kw in ["代码", "编程", "code"]):
        base_tokens += 2000
    
    return base_tokens


if __name__ == "__main__":
    args = parse_args()
    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent
    
    task_id = args.get("task_id")
    
    if task_id:
        result = get_task_token_usage(workspace, task_id)
    else:
        print("[ERROR] 需要 --task-id", file=sys.stderr)
        sys.exit(1)
    
    if "error" in result:
        print(f"[ERROR] {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n=== Token 消耗详情 ===")
    print(f"  任务ID: {result['taskId']}")
    print(f"  开始 Token: {result.get('startTokens', 'N/A'):,}")
    print(f"  结束 Token: {result.get('endTokens', 'N/A'):,}")
    print(f"  实际消耗: {result['tokenCount']:,}")
    print(f"  是否估算: {'是' if result.get('estimated') else '否'}")
    print(f"\nTOKEN_COUNT={result['tokenCount']}")
