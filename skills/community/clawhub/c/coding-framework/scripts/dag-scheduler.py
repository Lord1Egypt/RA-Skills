#!/usr/bin/env python3
"""
dag-scheduler.py — DAG 任务调度器

将大需求分解为有依赖关系的任务 DAG（有向无环图），
按拓扑排序和复杂度分层执行。

借鉴 ECC 的 Ralphinho 设计：
  - RFC 分解：将大需求分解为 WorkUnit（带依赖关系的 DAG）
  - 复杂度分层：trivial→small→medium→large，不同层级走不同深度的质量流水线
  - 作者偏差消除：每个阶段独立上下文窗口，reviewer 不是 author
  - 合并队列 + 驱逐：非冲突单元并行落地，冲突单元排队

核心概念：
  - WorkUnit: 一个独立的工作单元（任务）
  - Dependency: 任务间的依赖关系（前置任务）
  - Complexity: 复杂度等级（trivial/small/medium/large）
  - Stage: 执行阶段（plan/execute/review/optimize）

用法：
  python dag-scheduler.py create --name "feature-x" --description "实现功能X"
  python dag-scheduler.py add --dag "feature-x" --id "task-1" --description "..." --complexity "medium"
  python dag-scheduler.py depend --dag "feature-x" --from "task-2" --to "task-1"
  python dag-scheduler.py schedule --dag "feature-x"
  python dag-scheduler.py status --dag "feature-x"
  python dag-scheduler.py next --dag "feature-x"
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional


# ─── 常量 ───────────────────────────────────────────────────────────────────

DAGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dags")

# 复杂度等级及其对应的质量流水线深度
COMPLEXITY_LEVELS = {
    "trivial": {
        "weight": 1,
        "stages": ["execute"],  # 直接执行，无需审查
        "review_depth": "none",
        "estimated_minutes": 5,
    },
    "small": {
        "weight": 2,
        "stages": ["execute", "review"],  # 执行 + 轻量审查
        "review_depth": "light",
        "estimated_minutes": 15,
    },
    "medium": {
        "weight": 4,
        "stages": ["plan", "execute", "review"],  # 规划 + 执行 + 审查
        "review_depth": "standard",
        "estimated_minutes": 30,
    },
    "large": {
        "weight": 8,
        "stages": ["plan", "execute", "review", "optimize"],  # 完整流水线
        "review_depth": "deep",
        "estimated_minutes": 60,
    },
}

# 任务状态
TASK_STATUS = {
    "pending": "待执行",
    "in_progress": "执行中",
    "review": "审查中",
    "completed": "已完成",
    "blocked": "被阻塞",
    "failed": "失败",
}


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dags_dir():
    """确保 dags 目录存在。"""
    os.makedirs(DAGS_DIR, exist_ok=True)


def load_dag(dag_name: str) -> dict:
    """加载 DAG 文件。"""
    dag_path = os.path.join(DAGS_DIR, f"{dag_name}.json")
    if not os.path.exists(dag_path):
        return None
    with open(dag_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_dag(dag_name: str, data: dict):
    """保存 DAG 文件。"""
    ensure_dags_dir()
    dag_path = os.path.join(DAGS_DIR, f"{dag_name}.json")
    with open(dag_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def topological_sort(tasks: dict, dependencies: dict) -> list:
    """拓扑排序，返回执行顺序。"""
    # 构建入度表
    in_degree = {task_id: 0 for task_id in tasks}
    for task_id, deps in dependencies.items():
        for dep in deps:
            if dep in in_degree:
                in_degree[task_id] = in_degree.get(task_id, 0) + 1
    
    # BFS
    queue = [t for t, d in in_degree.items() if d == 0]
    result = []
    
    while queue:
        # 按复杂度排序（trivial 优先）
        queue.sort(key=lambda t: COMPLEXITY_LEVELS.get(tasks[t].get("complexity", "medium"), {}).get("weight", 4))
        task_id = queue.pop(0)
        result.append(task_id)
        
        # 更新入度
        for other_id, deps in dependencies.items():
            if task_id in deps:
                in_degree[other_id] -= 1
                if in_degree[other_id] == 0:
                    queue.append(other_id)
    
    # 检查是否有环
    if len(result) != len(tasks):
        return None  # 有环
    
    return result


def calculate_total_weight(tasks: dict) -> int:
    """计算总权重。"""
    total = 0
    for task in tasks.values():
        complexity = task.get("complexity", "medium")
        total += COMPLEXITY_LEVELS.get(complexity, {}).get("weight", 4)
    return total


def check_dependencies_met(task_id: str, dag: dict) -> bool:
    """检查任务的所有依赖是否已完成。"""
    deps = dag.get("dependencies", {}).get(task_id, [])
    for dep_id in deps:
        dep_task = dag.get("tasks", {}).get(dep_id, {})
        if dep_task.get("status") != "completed":
            return False
    return True


def get_pipeline_for_complexity(complexity: str) -> dict:
    """获取复杂度对应的质量流水线。"""
    return COMPLEXITY_LEVELS.get(complexity, COMPLEXITY_LEVELS["medium"])


# ─── 子命令实现 ──────────────────────────────────────────────────────────────

def cmd_create(args: argparse.Namespace) -> None:
    """创建新的 DAG。"""
    ensure_dags_dir()
    
    dag_name = args.name
    dag_path = os.path.join(DAGS_DIR, f"{dag_name}.json")
    
    if os.path.exists(dag_path) and not args.force:
        print(json.dumps({
            "success": False,
            "message": f"DAG 已存在: {dag_name}，使用 --force 覆盖"
        }, ensure_ascii=False))
        return
    
    dag = {
        "name": dag_name,
        "description": args.description,
        "tasks": {},
        "dependencies": {},
        "execution_order": [],
        "status": "planning",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "metadata": {
            "total_tasks": 0,
            "total_weight": 0,
            "estimated_minutes": 0,
        }
    }
    
    save_dag(dag_name, dag)
    
    print(json.dumps({
        "success": True,
        "action": "create",
        "dag_name": dag_name,
        "dag_path": dag_path,
        "message": f"已创建 DAG: {dag_name}"
    }, ensure_ascii=False, indent=2))


def cmd_add(args: argparse.Namespace) -> None:
    """添加任务到 DAG。"""
    dag = load_dag(args.dag)
    if not dag:
        print(json.dumps({"success": False, "message": f"DAG 不存在: {args.dag}"}, ensure_ascii=False))
        return
    
    task_id = args.id
    complexity = args.complexity or "medium"
    
    if complexity not in COMPLEXITY_LEVELS:
        print(json.dumps({
            "success": False,
            "message": f"无效复杂度: {complexity}，可选: {', '.join(COMPLEXITY_LEVELS.keys())}"
        }, ensure_ascii=False))
        return
    
    task = {
        "id": task_id,
        "description": args.description,
        "complexity": complexity,
        "status": "pending",
        "pipeline": get_pipeline_for_complexity(complexity),
        "created_at": now_iso(),
        "tags": args.tags.split(",") if args.tags else [],
    }
    
    dag["tasks"][task_id] = task
    dag["dependencies"][task_id] = []  # 初始化依赖列表
    
    # 更新元数据
    dag["metadata"]["total_tasks"] = len(dag["tasks"])
    dag["metadata"]["total_weight"] = calculate_total_weight(dag["tasks"])
    dag["metadata"]["estimated_minutes"] = sum(
        COMPLEXITY_LEVELS.get(t.get("complexity", "medium"), {}).get("estimated_minutes", 30)
        for t in dag["tasks"].values()
    )
    dag["updated_at"] = now_iso()
    
    save_dag(args.dag, dag)
    
    print(json.dumps({
        "success": True,
        "action": "add",
        "dag_name": args.dag,
        "task_id": task_id,
        "complexity": complexity,
        "pipeline": task["pipeline"],
        "message": f"已添加任务: {task_id} (复杂度: {complexity})"
    }, ensure_ascii=False, indent=2))


def cmd_depend(args: argparse.Namespace) -> None:
    """添加任务依赖关系。"""
    dag = load_dag(args.dag)
    if not dag:
        print(json.dumps({"success": False, "message": f"DAG 不存在: {args.dag}"}, ensure_ascii=False))
        return
    
    from_task = getattr(args, 'from')
    to_task = args.to
    
    # 验证任务存在
    if from_task not in dag["tasks"]:
        print(json.dumps({"success": False, "message": f"任务不存在: {from_task}"}, ensure_ascii=False))
        return
    if to_task not in dag["tasks"]:
        print(json.dumps({"success": False, "message": f"任务不存在: {to_task}"}, ensure_ascii=False))
        return
    
    # 添加依赖（from 依赖 to，即 to 必须先完成）
    if to_task not in dag["dependencies"][from_task]:
        dag["dependencies"][from_task].append(to_task)
    
    # 检查是否有环
    order = topological_sort(dag["tasks"], dag["dependencies"])
    if order is None:
        # 回滚
        dag["dependencies"][from_task].remove(to_task)
        print(json.dumps({"success": False, "message": "添加依赖会产生环"}, ensure_ascii=False))
        return
    
    dag["updated_at"] = now_iso()
    save_dag(args.dag, dag)
    
    print(json.dumps({
        "success": True,
        "action": "depend",
        "dag_name": args.dag,
        "from": from_task,
        "to": to_task,
        "message": f"已添加依赖: {from_task} -> {to_task}"
    }, ensure_ascii=False, indent=2))


def cmd_schedule(args: argparse.Namespace) -> None:
    """生成执行计划（拓扑排序）。"""
    dag = load_dag(args.dag)
    if not dag:
        print(json.dumps({"success": False, "message": f"DAG 不存在: {args.dag}"}, ensure_ascii=False))
        return
    
    order = topological_sort(dag["tasks"], dag["dependencies"])
    if order is None:
        print(json.dumps({"success": False, "message": "DAG 存在环，无法调度"}, ensure_ascii=False))
        return
    
    dag["execution_order"] = order
    dag["status"] = "scheduled"
    dag["scheduled_at"] = now_iso()
    dag["updated_at"] = now_iso()
    
    save_dag(args.dag, dag)
    
    # 生成执行计划详情
    schedule_detail = []
    for i, task_id in enumerate(order):
        task = dag["tasks"][task_id]
        complexity = task.get("complexity", "medium")
        pipeline = get_pipeline_for_complexity(complexity)
        deps = dag["dependencies"].get(task_id, [])
        
        schedule_detail.append({
            "order": i + 1,
            "task_id": task_id,
            "description": task.get("description", ""),
            "complexity": complexity,
            "stages": pipeline["stages"],
            "review_depth": pipeline["review_depth"],
            "estimated_minutes": pipeline["estimated_minutes"],
            "dependencies": deps,
            "can_parallel": len(deps) == 0 and i > 0,  # 无依赖且非首个任务可并行
        })
    
    print(json.dumps({
        "success": True,
        "action": "schedule",
        "dag_name": args.dag,
        "execution_order": order,
        "schedule": schedule_detail,
        "summary": {
            "total_tasks": len(order),
            "total_weight": dag["metadata"]["total_weight"],
            "estimated_minutes": dag["metadata"]["estimated_minutes"],
            "parallelizable": sum(1 for s in schedule_detail if s["can_parallel"]),
        },
        "message": f"已生成执行计划: {len(order)} 个任务，预计 {dag['metadata']['estimated_minutes']} 分钟"
    }, ensure_ascii=False, indent=2))


def cmd_status(args: argparse.Namespace) -> None:
    """查看 DAG 状态。"""
    dag = load_dag(args.dag)
    if not dag:
        print(json.dumps({"success": False, "message": f"DAG 不存在: {args.dag}"}, ensure_ascii=False))
        return
    
    # 统计各状态任务数
    status_counts = {}
    for task in dag["tasks"].values():
        status = task.get("status", "pending")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # 找出可执行的任务（依赖已满足）
    ready_tasks = []
    for task_id, task in dag["tasks"].items():
        if task.get("status") == "pending" and check_dependencies_met(task_id, dag):
            ready_tasks.append(task_id)
    
    print(json.dumps({
        "success": True,
        "action": "status",
        "dag_name": args.dag,
        "description": dag.get("description", ""),
        "status": dag.get("status", "planning"),
        "metadata": dag.get("metadata", {}),
        "status_counts": status_counts,
        "ready_tasks": ready_tasks,
        "tasks": {
            task_id: {
                "description": task.get("description", ""),
                "complexity": task.get("complexity", "medium"),
                "status": task.get("status", "pending"),
            }
            for task_id, task in dag["tasks"].items()
        },
        "dependencies": dag.get("dependencies", {}),
    }, ensure_ascii=False, indent=2))


def cmd_next(args: argparse.Namespace) -> None:
    """获取下一个可执行的任务。"""
    dag = load_dag(args.dag)
    if not dag:
        print(json.dumps({"success": False, "message": f"DAG 不存在: {args.dag}"}, ensure_ascii=False))
        return
    
    # 按执行顺序找第一个 pending 且依赖已满足的任务
    order = dag.get("execution_order", list(dag["tasks"].keys()))
    
    for task_id in order:
        task = dag["tasks"].get(task_id, {})
        if task.get("status") == "pending" and check_dependencies_met(task_id, dag):
            complexity = task.get("complexity", "medium")
            pipeline = get_pipeline_for_complexity(complexity)
            
            print(json.dumps({
                "success": True,
                "action": "next",
                "task_id": task_id,
                "task": task,
                "pipeline": pipeline,
                "dependencies_met": True,
                "message": f"下一个任务: {task_id} (复杂度: {complexity})"
            }, ensure_ascii=False, indent=2))
            return
    
    # 没有可执行的任务
    pending_count = sum(1 for t in dag["tasks"].values() if t.get("status") == "pending")
    if pending_count > 0:
        print(json.dumps({
            "success": True,
            "action": "next",
            "task_id": None,
            "message": f"有 {pending_count} 个待执行任务，但依赖未满足",
            "blocked": True,
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            "success": True,
            "action": "next",
            "task_id": None,
            "message": "所有任务已完成或无待执行任务",
            "completed": True,
        }, ensure_ascii=False, indent=2))


def cmd_update(args: argparse.Namespace) -> None:
    """更新任务状态。"""
    dag = load_dag(args.dag)
    if not dag:
        print(json.dumps({"success": False, "message": f"DAG 不存在: {args.dag}"}, ensure_ascii=False))
        return
    
    task_id = args.id
    new_status = args.status
    
    if task_id not in dag["tasks"]:
        print(json.dumps({"success": False, "message": f"任务不存在: {task_id}"}, ensure_ascii=False))
        return
    
    if new_status not in TASK_STATUS:
        print(json.dumps({
            "success": False,
            "message": f"无效状态: {new_status}，可选: {', '.join(TASK_STATUS.keys())}"
        }, ensure_ascii=False))
        return
    
    old_status = dag["tasks"][task_id].get("status", "pending")
    dag["tasks"][task_id]["status"] = new_status
    dag["tasks"][task_id]["updated_at"] = now_iso()
    
    # 检查是否所有任务完成
    all_completed = all(t.get("status") == "completed" for t in dag["tasks"].values())
    if all_completed:
        dag["status"] = "completed"
        dag["completed_at"] = now_iso()
    
    dag["updated_at"] = now_iso()
    save_dag(args.dag, dag)
    
    print(json.dumps({
        "success": True,
        "action": "update",
        "dag_name": args.dag,
        "task_id": task_id,
        "old_status": old_status,
        "new_status": new_status,
        "all_completed": all_completed,
        "message": f"已更新任务 {task_id}: {old_status} -> {new_status}"
    }, ensure_ascii=False, indent=2))


# ─── 参数解析 ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="DAG 任务调度器 — 将大需求分解为有依赖关系的任务 DAG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # create
    p_create = subparsers.add_parser("create", help="创建新的 DAG")
    p_create.add_argument("--name", required=True, help="DAG 名称")
    p_create.add_argument("--description", required=True, help="DAG 描述")
    p_create.add_argument("--force", action="store_true", help="覆盖已存在的 DAG")
    
    # add
    p_add = subparsers.add_parser("add", help="添加任务到 DAG")
    p_add.add_argument("--dag", required=True, help="DAG 名称")
    p_add.add_argument("--id", required=True, help="任务 ID")
    p_add.add_argument("--description", required=True, help="任务描述")
    p_add.add_argument("--complexity", choices=["trivial", "small", "medium", "large"], help="复杂度（默认 medium）")
    p_add.add_argument("--tags", help="标签（逗号分隔）")
    
    # depend
    p_depend = subparsers.add_parser("depend", help="添加任务依赖关系")
    p_depend.add_argument("--dag", required=True, help="DAG 名称")
    p_depend.add_argument("--from", required=True, help="依赖方任务 ID")
    p_depend.add_argument("--to", required=True, help="被依赖任务 ID")
    
    # schedule
    p_schedule = subparsers.add_parser("schedule", help="生成执行计划")
    p_schedule.add_argument("--dag", required=True, help="DAG 名称")
    
    # status
    p_status = subparsers.add_parser("status", help="查看 DAG 状态")
    p_status.add_argument("--dag", required=True, help="DAG 名称")
    
    # next
    p_next = subparsers.add_parser("next", help="获取下一个可执行的任务")
    p_next.add_argument("--dag", required=True, help="DAG 名称")
    
    # update
    p_update = subparsers.add_parser("update", help="更新任务状态")
    p_update.add_argument("--dag", required=True, help="DAG 名称")
    p_update.add_argument("--id", required=True, help="任务 ID")
    p_update.add_argument("--status", required=True, choices=TASK_STATUS.keys(), help="新状态")
    
    return parser


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    commands = {
        "create": cmd_create,
        "add": cmd_add,
        "depend": cmd_depend,
        "schedule": cmd_schedule,
        "status": cmd_status,
        "next": cmd_next,
        "update": cmd_update,
    }
    
    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
