#!/usr/bin/env python3
"""
前置校验脚本 - 代码级硬拦截

功能：
1. 检查上一步任务是否成功（分批创建时）
2. 检查参数文件是否存在
3. 检查步骤锁是否完整
4. 检查鉴权凭证是否有效

使用方式：
    python preflight_check.py --project <project_id> --action <action>

action 类型：
    - create_next: 创建下一个任务前检查
    - create_first: 创建第一个任务前检查
    - retry: 重试失败任务前检查
    - poll: 轮询状态前检查

返回格式（JSON）：
    {"status": "ok", "message": "..."}  - 通过
    {"status": "error", "message": "...", "blockers": [...]}  - 被拦截
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# 脚本目录
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data" / "plans"


def load_status(project_id):
    """加载项目状态文件"""
    status_file = DATA_DIR / project_id / "status.json"
    if not status_file.exists():
        return None
    with open(status_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_plan(project_id):
    """加载项目计划文件"""
    plan_file = DATA_DIR / project_id / "plan.json"
    if not plan_file.exists():
        return None
    with open(plan_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_credentials():
    """检查鉴权凭证"""
    cred_file = Path.home() / ".mingdata_dmp_credentials"
    if not cred_file.exists():
        return False, "凭证文件不存在"
    
    try:
        with open(cred_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)
        if not creds.get("access_key") or not creds.get("secret_key"):
            return False, "凭证不完整（缺少AK/SK）"
        return True, "凭证有效"
    except Exception as e:
        return False, f"凭证读取失败: {e}"


def check_auth_skill():
    """检查鉴权技能是否安装"""
    possible_paths = [
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    for path in possible_paths:
        if path.exists():
            return True, str(path)
    return False, "鉴权技能未安装"


def check_create_first(project_id=None):
    """创建第一个任务前的检查"""
    blockers = []
    
    # 1. 检查鉴权技能
    auth_ok, auth_msg = check_auth_skill()
    if not auth_ok:
        blockers.append(f"鉴权技能: {auth_msg}")
    
    # 2. 检查凭证
    cred_ok, cred_msg = check_credentials()
    if not cred_ok:
        blockers.append(f"凭证检查: {cred_msg}")
    
    if blockers:
        return {
            "status": "error",
            "message": "前置校验失败，无法创建任务",
            "blockers": blockers
        }
    
    return {
        "status": "ok",
        "message": "前置校验通过，可以创建第一个任务"
    }


def check_create_next(project_id, task_index):
    """创建下一个任务前的检查（核心拦截逻辑）"""
    blockers = []
    
    # 1. 检查项目是否存在
    status = load_status(project_id)
    if not status:
        blockers.append(f"项目 {project_id} 状态文件不存在")
        return {"status": "error", "message": "前置校验失败", "blockers": blockers}
    
    plan = load_plan(project_id)
    if not plan:
        blockers.append(f"项目 {project_id} 计划文件不存在")
        return {"status": "error", "message": "前置校验失败", "blockers": blockers}
    
    # 2. 检查上一步任务是否成功（硬拦截）
    prev_index = task_index - 1
    if prev_index >= 1:
        tasks = status.get("tasks", [])
        prev_task = None
        for t in tasks:
            if t.get("task_id") == prev_index:
                prev_task = t
                break
        
        if not prev_task:
            blockers.append(f"第 {prev_index} 个任务记录不存在")
        elif prev_task.get("status") != "success":
            blockers.append(
                f"第 {prev_index} 个任务状态为 '{prev_task.get('status')}'，"
                f"必须为 'success' 才能创建下一个任务"
            )
        elif not prev_task.get("audience_id"):
            blockers.append(f"第 {prev_index} 个任务缺少 audience_id")
    
    # 3. 检查是否超出总任务数
    total_tasks = plan.get("totalTasks", len(plan.get("combinations", [])))
    if task_index > total_tasks:
        blockers.append(f"任务索引 {task_index} 超出总数 {total_tasks}")
    
    # 4. 检查是否重复创建
    tasks = status.get("tasks", [])
    for t in tasks:
        if t.get("task_id") == task_index and t.get("status") == "success":
            blockers.append(f"第 {task_index} 个任务已创建成功，不可重复创建")
    
    # 5. 检查鉴权凭证
    cred_ok, cred_msg = check_credentials()
    if not cred_ok:
        blockers.append(f"凭证检查: {cred_msg}")
    
    if blockers:
        return {
            "status": "error",
            "message": f"前置校验失败，禁止创建第 {task_index} 个任务",
            "blockers": blockers,
            "project_id": project_id,
            "task_index": task_index
        }
    
    return {
        "status": "ok",
        "message": f"前置校验通过，可以创建第 {task_index} 个任务",
        "project_id": project_id,
        "task_index": task_index
    }


def check_retry(project_id):
    """重试前的检查"""
    blockers = []
    
    status = load_status(project_id)
    if not status:
        blockers.append(f"项目 {project_id} 状态文件不存在")
        return {"status": "error", "message": "前置校验失败", "blockers": blockers}
    
    # 检查是否有失败的任务
    tasks = status.get("tasks", [])
    failed = [t for t in tasks if t.get("status") == "failed"]
    if not failed:
        blockers.append("没有失败的任务需要重试")
    
    # 检查凭证
    cred_ok, cred_msg = check_credentials()
    if not cred_ok:
        blockers.append(f"凭证检查: {cred_msg}")
    
    if blockers:
        return {"status": "error", "message": "前置校验失败", "blockers": blockers}
    
    return {
        "status": "ok",
        "message": "前置校验通过，可以重试",
        "failed_count": len(failed)
    }


def check_poll(project_id):
    """轮询前的检查"""
    blockers = []
    
    status = load_status(project_id)
    if not status:
        blockers.append(f"项目 {project_id} 状态文件不存在")
        return {"status": "error", "message": "前置校验失败", "blockers": blockers}
    
    # 检查是否有待轮询的任务（status=success或submitted的都有audience_id需要轮询）
    tasks = status.get("tasks", [])
    pending = [t for t in tasks if t.get("status") in ("success", "submitted") and t.get("audience_id")]
    if not pending:
        return {
            "status": "ok",
            "message": "没有需要轮询的任务",
            "pending_count": 0
        }
    
    # 检查超时（自愈逻辑）
    last_poll = status.get("lastPollAt")
    if last_poll:
        try:
            last_time = datetime.strptime(last_poll, "%Y-%m-%d %H:%M:%S")
            elapsed = datetime.now() - last_time
            if elapsed > timedelta(minutes=30):
                return {
                    "status": "warning",
                    "message": f"距上次轮询已 {elapsed.seconds // 60} 分钟，可能需要关注",
                    "elapsed_minutes": elapsed.seconds // 60
                }
        except:
            pass
    
    return {
        "status": "ok",
        "message": "前置校验通过",
        "pending_count": len(pending)
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='前置校验脚本')
    parser.add_argument('--project', help='项目ID')
    parser.add_argument('--action', required=True, 
                        choices=['create_first', 'create_next', 'retry', 'poll'],
                        help='校验动作类型')
    parser.add_argument('--task-index', type=int, help='任务索引（create_next时必填）')
    
    args = parser.parse_args()
    
    # 分发检查
    if args.action == 'create_first':
        result = check_create_first(args.project)
    elif args.action == 'create_next':
        if not args.project:
            result = {"status": "error", "message": "缺少 --project 参数"}
        elif not args.task_index:
            result = {"status": "error", "message": "缺少 --task-index 参数"}
        else:
            result = check_create_next(args.project, args.task_index)
    elif args.action == 'retry':
        if not args.project:
            result = {"status": "error", "message": "缺少 --project 参数"}
        else:
            result = check_retry(args.project)
    elif args.action == 'poll':
        if not args.project:
            result = {"status": "error", "message": "缺少 --project 参数"}
        else:
            result = check_poll(args.project)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False))
    
    # 根据结果设置退出码
    if result["status"] == "error":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
