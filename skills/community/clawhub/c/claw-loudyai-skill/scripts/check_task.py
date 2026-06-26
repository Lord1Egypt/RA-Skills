#!/usr/bin/env python3
"""
查询任务状态和支付信息
"""
import requests
import json
import os

API_BASE = "https://api.loudy.ai/app-api/open-api/v1"
LOUDY_API_KEY = os.environ.get("LOUDY_API_KEY", "")

def check_task_status(task_id: int):
    """
    查询任务状态
    
    Args:
        task_id: 任务ID
    
    Returns:
        任务详情，包含:
        - taskStatus: 任务状态
        - auditStatus: 审核状态 (0=未审核, 1=通过, 2=拒绝)
        - taskLinks: 作品链接
        - txn: 交易哈希
    """
    url = f"{API_BASE}/earning-pool-tasks/{task_id}"
    headers = {
        "X-API-Key": LOUDY_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if data.get("code") != 0 and data.get("code") != 200:
        print(f"Error: {data.get('msg')}")
        return None
    
    return data.get("data")

def parse_audit_status(audit_status: int) -> str:
    """解析审核状态"""
    status_map = {
        0: "未审核",
        1: "审核通过",
        2: "审核拒绝"
    }
    return status_map.get(audit_status, "未知")

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python check_task.py <task_id>")
        sys.exit(1)
    
    task_id = int(sys.argv[1])
    task = check_task_status(task_id)
    
    if task:
        print(json.dumps(task, indent=2, ensure_ascii=False))
        print("\n--- 状态摘要 ---")
        print(f"任务状态: {task.get('taskStatus')}")
        print(f"审核状态: {parse_audit_status(task.get('auditStatus', 0))}")
        print(f"作品链接: {task.get('taskLinks')}")
        print(f"交易哈希: {task.get('txn')}")

if __name__ == "__main__":
    main()
