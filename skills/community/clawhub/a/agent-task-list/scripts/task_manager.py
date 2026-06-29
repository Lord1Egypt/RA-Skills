#!/usr/bin/env python3
"""
Agent 独立任务列表系统 - 核心管理脚本
支持任务创建、分配、状态更新、进度跟踪、历史记录
"""

import os
import sys
import json
import argparse
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# 路径配置
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
TASK_DATA_DIR = WORKSPACE_ROOT / "agent-tasks"
AGENTS_DIR = TASK_DATA_DIR / "agents"
HISTORY_DIR = TASK_DATA_DIR / "history"
TASK_COUNTER_FILE = TASK_DATA_DIR / "task-counter.txt"
INDEX_FILE = TASK_DATA_DIR / "index.json"

# 任务状态
TASK_STATUS_PENDING = "pending"
TASK_STATUS_RUNNING = "running"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"
TASK_STATUS_CANCELLED = "cancelled"

# 优先级范围
MIN_PRIORITY = 1
MAX_PRIORITY = 10


def ensure_dirs():
    """确保必要的目录存在"""
    TASK_DATA_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def get_task_counter() -> int:
    """获取任务计数器"""
    if TASK_COUNTER_FILE.exists():
        try:
            return int(TASK_COUNTER_FILE.read_text().strip())
        except:
            return 0
    return 0


def increment_task_counter() -> int:
    """增加任务计数器并返回新值"""
    counter = get_task_counter() + 1
    TASK_COUNTER_FILE.write_text(str(counter))
    return counter


def generate_task_id() -> str:
    """生成任务 ID"""
    counter = increment_task_counter()
    return f"task-{counter:03d}"


def get_timestamp() -> str:
    """获取当前时间戳（ISO 8601 格式）"""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")


def get_agent_task_file(agent_id: str) -> Path:
    """获取 Agent 任务列表文件路径"""
    agent_dir = AGENTS_DIR / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)
    return agent_dir / "task-list.json"


def load_agent_task_list(agent_id: str) -> Dict[str, Any]:
    """加载 Agent 任务列表"""
    task_file = get_agent_task_file(agent_id)
    
    if not task_file.exists():
        return {
            "agent_id": agent_id,
            "agent_name": agent_id,
            "current_task": None,
            "pending_tasks": [],
            "completed_tasks": [],
            "failed_tasks": [],
            "created_at": get_timestamp(),
            "updated_at": get_timestamp()
        }
    
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading task list: {e}", file=sys.stderr)
        return {
            "agent_id": agent_id,
            "agent_name": agent_id,
            "current_task": None,
            "pending_tasks": [],
            "completed_tasks": [],
            "failed_tasks": [],
            "created_at": get_timestamp(),
            "updated_at": get_timestamp()
        }


def save_agent_task_list(agent_id: str, task_list: Dict[str, Any]):
    """保存 Agent 任务列表"""
    task_file = get_agent_task_file(agent_id)
    task_list["updated_at"] = get_timestamp()
    
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(task_list, f, ensure_ascii=False, indent=2)


def archive_task(task: Dict[str, Any]):
    """归档完成任务到历史记录"""
    # 按月份创建目录
    completed_at = task.get("completed_at") or task.get("failed_at") or get_timestamp()
    month_dir = completed_at[:7]  # "2026-04"
    
    history_month_dir = HISTORY_DIR / month_dir
    history_month_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存到历史文件
    history_file = history_month_dir / f"{task['id']}.json"
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(task, f, ensure_ascii=False, indent=2)


def update_index(agent_id: str, task_list: Dict[str, Any]):
    """更新全局索引"""
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                index = json.load(f)
        except:
            index = {"agents": [], "total_tasks": {
                "current": 0, "pending": 0, "completed": 0, "failed": 0
            }}
    else:
        index = {"agents": [], "total_tasks": {
            "current": 0, "pending": 0, "completed": 0, "failed": 0
        }}
    
    # 更新或添加 Agent 信息
    agent_info = {
        "agent_id": agent_id,
        "agent_name": task_list.get("agent_name", agent_id),
        "task_count": {
            "current": 1 if task_list.get("current_task") else 0,
            "pending": len(task_list.get("pending_tasks", [])),
            "completed": len(task_list.get("completed_tasks", [])),
            "failed": len(task_list.get("failed_tasks", []))
        },
        "last_updated": task_list.get("updated_at", get_timestamp())
    }
    
    # 查找并更新或添加
    found = False
    for i, agent in enumerate(index["agents"]):
        if agent["agent_id"] == agent_id:
            index["agents"][i] = agent_info
            found = True
            break
    
    if not found:
        index["agents"].append(agent_info)
    
    # 更新总计
    total = {"current": 0, "pending": 0, "completed": 0, "failed": 0}
    for agent in index["agents"]:
        counts = agent.get("task_count", {})
        total["current"] += counts.get("current", 0)
        total["pending"] += counts.get("pending", 0)
        total["completed"] += counts.get("completed", 0)
        total["failed"] += counts.get("failed", 0)
    
    index["total_tasks"] = total
    
    # 保存索引
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def create_task(agent_id: str, name: str, description: str, priority: int = 5) -> Dict[str, Any]:
    """
    创建新任务
    
    Args:
        agent_id: Agent ID
        name: 任务名称
        description: 任务描述
        priority: 优先级 (1-10)
    
    Returns:
        任务创建结果
    """
    ensure_dirs()
    
    # 验证优先级
    if priority < MIN_PRIORITY or priority > MAX_PRIORITY:
        return {
            "status": "error",
            "error": f"优先级必须在 {MIN_PRIORITY}-{MAX_PRIORITY} 之间"
        }
    
    # 加载任务列表
    task_list = load_agent_task_list(agent_id)
    
    # 创建任务
    task_id = generate_task_id()
    task = {
        "id": task_id,
        "name": name,
        "description": description,
        "status": TASK_STATUS_PENDING,
        "priority": priority,
        "assigned_at": get_timestamp(),
        "agent_id": agent_id
    }
    
    # 添加到待办队列
    task_list["pending_tasks"].append(task)
    
    # 按优先级排序待办队列（优先级高的在前）
    task_list["pending_tasks"].sort(
        key=lambda t: (-t["priority"], t["assigned_at"])
    )
    
    # 保存任务列表
    save_agent_task_list(agent_id, task_list)
    
    # 更新索引
    update_index(agent_id, task_list)
    
    return {
        "status": "success",
        "task_id": task_id,
        "task": task,
        "message": f"任务已添加到 {agent_id} 的待办队列"
    }


def list_tasks(agent_id: str) -> Dict[str, Any]:
    """
    获取 Agent 任务列表
    
    Args:
        agent_id: Agent ID
    
    Returns:
        任务列表
    """
    ensure_dirs()
    return load_agent_task_list(agent_id)


def list_all_agents() -> Dict[str, Any]:
    """
    获取所有 Agent 的任务概览
    
    Returns:
        所有 Agent 的任务概览
    """
    ensure_dirs()
    
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "agents": [],
        "total_tasks": {
            "current": 0, "pending": 0, "completed": 0, "failed": 0
        }
    }


def get_task(task_id: str) -> Dict[str, Any]:
    """
    获取任务详情
    
    Args:
        task_id: 任务 ID
    
    Returns:
        任务详情
    """
    ensure_dirs()
    
    # 遍历所有 Agent 查找任务
    for agent_dir in AGENTS_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        
        task_list = load_agent_task_list(agent_dir.name)
        
        # 检查当前任务
        if task_list.get("current_task") and task_list["current_task"]["id"] == task_id:
            return {
                "status": "success",
                "task": task_list["current_task"],
                "agent_id": agent_dir.name,
                "location": "current_task"
            }
        
        # 检查待办任务
        for task in task_list.get("pending_tasks", []):
            if task["id"] == task_id:
                return {
                    "status": "success",
                    "task": task,
                    "agent_id": agent_dir.name,
                    "location": "pending_tasks"
                }
        
        # 检查已完成任务
        for task in task_list.get("completed_tasks", []):
            if task["id"] == task_id:
                return {
                    "status": "success",
                    "task": task,
                    "agent_id": agent_dir.name,
                    "location": "completed_tasks"
                }
        
        # 检查失败任务
        for task in task_list.get("failed_tasks", []):
            if task["id"] == task_id:
                return {
                    "status": "success",
                    "task": task,
                    "agent_id": agent_dir.name,
                    "location": "failed_tasks"
                }
    
    return {
        "status": "error",
        "error": f"任务 {task_id} 不存在"
    }


def start_task(agent_id: str) -> Dict[str, Any]:
    """
    Agent 开始执行下一个待办任务
    
    Args:
        agent_id: Agent ID
    
    Returns:
        任务启动结果
    """
    ensure_dirs()
    
    # 加载任务列表
    task_list = load_agent_task_list(agent_id)
    
    # 检查是否已有当前任务
    if task_list.get("current_task"):
        return {
            "status": "error",
            "error": f"Agent {agent_id} 已有当前任务：{task_list['current_task']['id']}"
        }
    
    # 检查是否有待办任务
    pending_tasks = task_list.get("pending_tasks", [])
    if not pending_tasks:
        return {
            "status": "error",
            "error": f"Agent {agent_id} 没有待办任务"
        }
    
    # 获取最高优先级的任务
    task = pending_tasks[0]
    
    # 从待办队列移除
    task_list["pending_tasks"].pop(0)
    
    # 更新任务状态
    task["status"] = TASK_STATUS_RUNNING
    task["started_at"] = get_timestamp()
    
    # 设置为当前任务
    task_list["current_task"] = task
    
    # 保存任务列表
    save_agent_task_list(agent_id, task_list)
    
    # 更新索引
    update_index(agent_id, task_list)
    
    return {
        "status": "success",
        "task_id": task["id"],
        "task": task,
        "message": "任务已开始执行"
    }


def complete_task(agent_id: str) -> Dict[str, Any]:
    """
    标记当前任务为完成
    
    Args:
        agent_id: Agent ID
    
    Returns:
        任务完成结果
    """
    ensure_dirs()
    
    # 加载任务列表
    task_list = load_agent_task_list(agent_id)
    
    # 检查是否有当前任务
    current_task = task_list.get("current_task")
    if not current_task:
        return {
            "status": "error",
            "error": f"Agent {agent_id} 没有当前任务"
        }
    
    # 更新任务状态
    current_task["status"] = TASK_STATUS_COMPLETED
    current_task["completed_at"] = get_timestamp()
    
    # 添加到已完成任务
    task_list["completed_tasks"].append(current_task)
    
    # 清空当前任务
    task_list["current_task"] = None
    
    # 归档任务
    archive_task(current_task)
    
    # 保存任务列表
    save_agent_task_list(agent_id, task_list)
    
    # 更新索引
    update_index(agent_id, task_list)
    
    return {
        "status": "success",
        "task_id": current_task["id"],
        "message": "任务已完成，已归档到历史记录"
    }


def fail_task(agent_id: str, error_message: str = "") -> Dict[str, Any]:
    """
    标记当前任务为失败
    
    Args:
        agent_id: Agent ID
        error_message: 错误信息
    
    Returns:
        任务失败结果
    """
    ensure_dirs()
    
    # 加载任务列表
    task_list = load_agent_task_list(agent_id)
    
    # 检查是否有当前任务
    current_task = task_list.get("current_task")
    if not current_task:
        return {
            "status": "error",
            "error": f"Agent {agent_id} 没有当前任务"
        }
    
    # 更新任务状态
    current_task["status"] = TASK_STATUS_FAILED
    current_task["failed_at"] = get_timestamp()
    current_task["error_message"] = error_message
    
    # 增加重试计数
    if "retry_count" not in current_task:
        current_task["retry_count"] = 0
    current_task["retry_count"] += 1
    
    # 添加到失败任务
    task_list["failed_tasks"].append(current_task)
    
    # 清空当前任务
    task_list["current_task"] = None
    
    # 归档任务
    archive_task(current_task)
    
    # 保存任务列表
    save_agent_task_list(agent_id, task_list)
    
    # 更新索引
    update_index(agent_id, task_list)
    
    return {
        "status": "success",
        "task_id": current_task["id"],
        "message": "任务已标记为失败"
    }


def cancel_task(agent_id: str, task_id: str) -> Dict[str, Any]:
    """
    取消任务（当前任务或待办任务）
    
    Args:
        agent_id: Agent ID
        task_id: 任务 ID
    
    Returns:
        任务取消结果
    """
    ensure_dirs()
    
    # 加载任务列表
    task_list = load_agent_task_list(agent_id)
    
    # 检查当前任务
    if task_list.get("current_task") and task_list["current_task"]["id"] == task_id:
        task = task_list["current_task"]
        task["status"] = TASK_STATUS_CANCELLED
        task["cancelled_at"] = get_timestamp()
        task_list["current_task"] = None
        
        save_agent_task_list(agent_id, task_list)
        update_index(agent_id, task_list)
        
        return {
            "status": "success",
            "task_id": task_id,
            "message": "当前任务已取消"
        }
    
    # 检查待办任务
    for i, task in enumerate(task_list.get("pending_tasks", [])):
        if task["id"] == task_id:
            task_list["pending_tasks"].pop(i)
            task["status"] = TASK_STATUS_CANCELLED
            task["cancelled_at"] = get_timestamp()
            
            save_agent_task_list(agent_id, task_list)
            update_index(agent_id, task_list)
            
            return {
                "status": "success",
                "task_id": task_id,
                "message": "待办任务已取消"
            }
    
    return {
        "status": "error",
        "error": f"任务 {task_id} 不存在或无法取消"
    }


def retry_task(agent_id: str, task_id: str) -> Dict[str, Any]:
    """
    重试失败任务
    
    Args:
        agent_id: Agent ID
        task_id: 任务 ID
    
    Returns:
        任务重试结果
    """
    ensure_dirs()
    
    # 加载任务列表
    task_list = load_agent_task_list(agent_id)
    
    # 从失败任务中查找
    task_index = None
    for i, task in enumerate(task_list.get("failed_tasks", [])):
        if task["id"] == task_id:
            task_index = i
            break
    
    if task_index is None:
        return {
            "status": "error",
            "error": f"失败任务 {task_id} 不存在"
        }
    
    # 从失败任务移除
    task = task_list["failed_tasks"].pop(task_index)
    
    # 重置任务状态
    task["status"] = TASK_STATUS_PENDING
    task["assigned_at"] = get_timestamp()
    task.pop("failed_at", None)
    task.pop("error_message", None)
    
    # 添加到待办队列
    task_list["pending_tasks"].append(task)
    
    # 按优先级排序
    task_list["pending_tasks"].sort(
        key=lambda t: (-t["priority"], t["assigned_at"])
    )
    
    # 保存任务列表
    save_agent_task_list(agent_id, task_list)
    
    # 更新索引
    update_index(agent_id, task_list)
    
    return {
        "status": "success",
        "task_id": task_id,
        "message": "任务已重新加入待办队列"
    }


def query_tasks(agent_id: str, status: str = None, min_priority: int = None) -> Dict[str, Any]:
    """
    查询任务
    
    Args:
        agent_id: Agent ID
        status: 任务状态（可选）
        min_priority: 最小优先级（可选）
    
    Returns:
        查询结果
    """
    ensure_dirs()
    
    task_list = load_agent_task_list(agent_id)
    results = []
    
    # 查询当前任务
    if task_list.get("current_task"):
        task = task_list["current_task"]
        if status and task["status"] != status:
            pass
        elif min_priority and task["priority"] < min_priority:
            pass
        else:
            results.append({"task": task, "location": "current_task"})
    
    # 查询待办任务
    for task in task_list.get("pending_tasks", []):
        if status and task["status"] != status:
            continue
        if min_priority and task["priority"] < min_priority:
            continue
        results.append({"task": task, "location": "pending_tasks"})
    
    # 查询已完成任务
    for task in task_list.get("completed_tasks", []):
        if status and task["status"] != status:
            continue
        if min_priority and task["priority"] < min_priority:
            continue
        results.append({"task": task, "location": "completed_tasks"})
    
    # 查询失败任务
    for task in task_list.get("failed_tasks", []):
        if status and task["status"] != status:
            continue
        if min_priority and task["priority"] < min_priority:
            continue
        results.append({"task": task, "location": "failed_tasks"})
    
    return {
        "status": "success",
        "agent_id": agent_id,
        "total": len(results),
        "tasks": results
    }


def get_stats(agent_id: str) -> Dict[str, Any]:
    """
    获取任务统计信息
    
    Args:
        agent_id: Agent ID
    
    Returns:
        统计信息
    """
    ensure_dirs()
    
    task_list = load_agent_task_list(agent_id)
    
    current_count = 1 if task_list.get("current_task") else 0
    pending_count = len(task_list.get("pending_tasks", []))
    completed_count = len(task_list.get("completed_tasks", []))
    failed_count = len(task_list.get("failed_tasks", []))
    total = current_count + pending_count + completed_count + failed_count
    
    # 计算成功率
    success_rate = 0.0
    if completed_count + failed_count > 0:
        success_rate = completed_count / (completed_count + failed_count)
    
    return {
        "status": "success",
        "agent_id": agent_id,
        "total": {
            "current": current_count,
            "pending": pending_count,
            "completed": completed_count,
            "failed": failed_count,
            "all": total
        },
        "success_rate": round(success_rate, 2)
    }


def get_history(agent_id: str, limit: int = 10) -> Dict[str, Any]:
    """
    获取任务历史记录
    
    Args:
        agent_id: Agent ID
        limit: 返回数量限制
    
    Returns:
        历史记录
    """
    ensure_dirs()
    
    task_list = load_agent_task_list(agent_id)
    
    # 合并已完成和失败任务，按时间排序
    history = []
    
    for task in task_list.get("completed_tasks", []):
        history.append(task)
    
    for task in task_list.get("failed_tasks", []):
        history.append(task)
    
    # 按完成时间排序
    history.sort(
        key=lambda t: t.get("completed_at") or t.get("failed_at") or t.get("assigned_at"),
        reverse=True
    )
    
    return {
        "status": "success",
        "agent_id": agent_id,
        "total": len(history),
        "history": history[:limit]
    }


def main():
    parser = argparse.ArgumentParser(description="Agent 独立任务列表系统")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新任务")
    create_parser.add_argument("--agent", required=True, help="Agent ID")
    create_parser.add_argument("--name", required=True, help="任务名称")
    create_parser.add_argument("--description", required=True, help="任务描述")
    create_parser.add_argument("--priority", type=int, default=5, help="优先级 (1-10)")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="获取 Agent 任务列表")
    list_parser.add_argument("--agent", required=True, help="Agent ID")
    
    # list-all 命令
    subparsers.add_parser("list-all", help="获取所有 Agent 任务概览")
    
    # get 命令
    get_parser = subparsers.add_parser("get", help="获取任务详情")
    get_parser.add_argument("--task-id", required=True, help="任务 ID")
    
    # start 命令
    start_parser = subparsers.add_parser("start", help="开始执行任务")
    start_parser.add_argument("--agent", required=True, help="Agent ID")
    
    # complete 命令
    complete_parser = subparsers.add_parser("complete", help="完成任务")
    complete_parser.add_argument("--agent", required=True, help="Agent ID")
    
    # fail 命令
    fail_parser = subparsers.add_parser("fail", help="标记任务失败")
    fail_parser.add_argument("--agent", required=True, help="Agent ID")
    fail_parser.add_argument("--error", default="", help="错误信息")
    
    # cancel 命令
    cancel_parser = subparsers.add_parser("cancel", help="取消任务")
    cancel_parser.add_argument("--agent", required=True, help="Agent ID")
    cancel_parser.add_argument("--task-id", required=True, help="任务 ID")
    
    # retry 命令
    retry_parser = subparsers.add_parser("retry", help="重试失败任务")
    retry_parser.add_argument("--agent", required=True, help="Agent ID")
    retry_parser.add_argument("--task-id", required=True, help="任务 ID")
    
    # query 命令
    query_parser = subparsers.add_parser("query", help="查询任务")
    query_parser.add_argument("--agent", required=True, help="Agent ID")
    query_parser.add_argument("--status", help="任务状态")
    query_parser.add_argument("--min-priority", type=int, help="最小优先级")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="获取统计信息")
    stats_parser.add_argument("--agent", required=True, help="Agent ID")
    
    # history 命令
    history_parser = subparsers.add_parser("history", help="获取历史记录")
    history_parser.add_argument("--agent", required=True, help="Agent ID")
    history_parser.add_argument("--limit", type=int, default=10, help="返回数量")
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # 执行命令
    result = None
    
    if args.command == "create":
        result = create_task(args.agent, args.name, args.description, args.priority)
    
    elif args.command == "list":
        result = list_tasks(args.agent)
    
    elif args.command == "list-all":
        result = list_all_agents()
    
    elif args.command == "get":
        result = get_task(args.task_id)
    
    elif args.command == "start":
        result = start_task(args.agent)
    
    elif args.command == "complete":
        result = complete_task(args.agent)
    
    elif args.command == "fail":
        result = fail_task(args.agent, args.error)
    
    elif args.command == "cancel":
        result = cancel_task(args.agent, args.task_id)
    
    elif args.command == "retry":
        result = retry_task(args.agent, args.task_id)
    
    elif args.command == "query":
        result = query_tasks(args.agent, args.status, args.min_priority)
    
    elif args.command == "stats":
        result = get_stats(args.agent)
    
    elif args.command == "history":
        result = get_history(args.agent, args.limit)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
