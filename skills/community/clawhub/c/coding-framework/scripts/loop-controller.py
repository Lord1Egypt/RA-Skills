#!/usr/bin/env python3
"""
loop-controller.py — 迭代循环控制器

管理迭代循环的状态、条件检测和生命周期。
借鉴 Claude Code Ralph Wiggum 的 Stop Hook 自引用循环模式。

v10.1 改进:
  - 并发保护: PID 文件锁防止同名循环并发
  - 输入校验: --name 不允许特殊字符, --max 必须为正整数
  - 心跳检测: check 命令检测状态更新时间，超时警告可能死锁
  - cleanup 命令: 清理死锁或残留的状态文件
  - JSON 输出: 所有输出均为结构化 JSON

v10.2 改进:
  - Git 集成: --auto-commit 每次迭代前自动创建 Git 提交和 tag
  - rollback 命令: 支持回滚到指定迭代 (--to N / --prev / --initial)

v11.4 改进 (Backpressure 门控):
  - gates 子命令: 三层门控（编译/测试/质量）
  - 自动检测测试框架（pytest/npm test）
  - 自动检测 lint 工具（ruff/eslint）
  - 自动检测 typecheck 工具（mypy/tsc）
  - 门控失败时输出修复提示

子命令:
  init     - 初始化新的迭代循环
  check    - 检查是否应继续迭代
  update   - 更新当前迭代的结果
  complete - 标记循环完成
  cleanup  - 清理残留状态（v10.1 新增）
  rollback - 回滚到指定迭代（v10.2 新增）
  gates    - 运行三层门控检查（v11.4 新增）

用法:
  python loop-controller.py init --name "task" --mode max --max 10
  python loop-controller.py init --name "task" --mode max --max 10 --auto-commit
  python loop-controller.py check --state loop-state.json
  python loop-controller.py update --state loop-state.json --result pass --summary "done"
  python loop-controller.py complete --state loop-state.json --reason "目标达成"
  python loop-controller.py cleanup --state loop-state.json --force
  python loop-controller.py rollback --name "task" --to 3
  python loop-controller.py rollback --name "task" --prev
  python loop-controller.py rollback --name "task" --initial
  python loop-controller.py gates --files "src/main.py" --complexity medium
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# ─── 常量 ───────────────────────────────────────────────────────────────────

DEFAULT_STATE_FILE = "loop-state.json"
VALID_MODES = ("fixed", "max", "adaptive")
VALID_RESULTS = ("pass", "fail", "partial")
VALID_STATUSES = ("running", "completed", "failed", "cancelled")
DEFAULT_PATIENCE = 3
DEFAULT_HEARTBEAT_TIMEOUT = 300  # 秒，v10.1 新增
NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\u4e00-\u9fff]+$')  # 允许中英文、数字、下划线、连字符


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def validate_name(name: str) -> None:
    """校验任务名称（v10.1 新增）。"""
    if not name:
        error_exit("--name 不能为空")
    if len(name) > 100:
        error_exit("--name 长度不能超过 100 字符")
    if not NAME_PATTERN.match(name):
        error_exit(f"--name 包含非法字符: '{name}'，仅允许中英文、数字、下划线、连字符")


def load_state(path: str) -> dict:
    """加载状态文件，返回解析后的字典。"""
    p = Path(path)
    if not p.exists():
        error_exit(f"状态文件不存在: {path}")
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        error_exit(f"状态文件 {path} 格式错误: {e}")
    except OSError as e:
        error_exit(f"读取状态文件 {path} 失败: {e}")


def save_state(path: str, state: dict) -> None:
    """将状态字典写入文件。"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except OSError as e:
        error_exit(f"写入状态文件 {path} 失败: {e}")


def error_exit(msg: str, code: int = 1) -> None:
    """输出错误 JSON 并退出。"""
    print(json.dumps({"error": msg, "success": False}, ensure_ascii=False))
    sys.exit(code)


def output_result(data: dict) -> None:
    """输出结果 JSON 到 stdout。"""
    data["success"] = True
    print(json.dumps(data, ensure_ascii=False, indent=2))


def now_iso() -> str:
    """返回当前 UTC 时间的 ISO 格式字符串。"""
    return datetime.now(timezone.utc).isoformat()


def check_pid_alive(pid: int) -> bool:
    """检查 PID 是否存活（跨平台）。（v10.1 新增）"""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def check_existing_process(state: dict) -> Optional[dict]:
    """检查是否有同名循环在运行（v10.1 新增）。"""
    if state.get("status") != "running":
        return None
    
    pid = state.get("pid")
    if pid and check_pid_alive(pid):
        return {
            "running": True,
            "pid": pid,
            "name": state.get("name"),
            "message": f"循环 '{state.get('name')}' 正在运行 (PID={pid})"
        }
    return None


def check_heartbeat(state: dict, timeout: int = DEFAULT_HEARTBEAT_TIMEOUT) -> dict:
    """检查心跳，返回心跳状态。（v10.1 新增）"""
    updated_at = state.get("updated_at", "")
    if not updated_at:
        return {"healthy": True, "message": "无更新时间记录"}
    
    try:
        last_update = datetime.fromisoformat(updated_at)
        now = datetime.now(timezone.utc)
        elapsed = (now - last_update).total_seconds()
        
        if elapsed > timeout:
            return {
                "healthy": False,
                "elapsed_seconds": int(elapsed),
                "timeout_seconds": timeout,
                "message": f"⚠️ 心跳超时: {int(elapsed)}秒未更新 (阈值={timeout}秒)，可能已死锁"
            }
        return {
            "healthy": True,
            "elapsed_seconds": int(elapsed),
            "message": f"心跳正常: {int(elapsed)}秒前更新"
        }
    except ValueError:
        return {"healthy": True, "message": "无法解析更新时间"}


def is_sloppify_round(state: dict, iteration: int) -> bool:
    """判断当前轮次是否为 De-Sloppify 清理轮次。（v10.3 新增）
    
    De-Sloppify 模式在实现轮次之间插入清理轮次，保持代码简洁。
    例如 interval=2 时：实现1, 实现2, 清理, 实现3, 实现4, 清理, ...
    """
    sloppify = state.get("sloppify", {})
    if not sloppify.get("enabled"):
        return False
    
    interval = sloppify.get("interval", 2)
    # 每 (interval+1) 轮中，最后一轮是清理轮次
    # 例如 interval=2: 第3轮(3%3=0)、第6轮(6%3=0)是清理轮次
    return iteration > 0 and (iteration % (interval + 1)) == 0


# ─── Git 集成（v10.2 新增）────────────────────────────────────────────────────

def is_git_repo() -> bool:
    """检查当前目录是否在 Git 仓库中。"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() == "true"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def git_create_tag(tag_name: str, message: str) -> dict:
    """创建 Git tag。"""
    if not is_git_repo():
        return {"success": False, "message": "不在 Git 仓库中"}
    
    try:
        # 先暂存所有变更
        subprocess.run(["git", "add", "-A"], capture_output=True, timeout=10)
        # 创建提交
        subprocess.run(
            ["git", "commit", "-m", f"chore: {message}", "--allow-empty"],
            capture_output=True, timeout=10
        )
        # 创建 tag
        result = subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", message],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return {"success": True, "tag": tag_name, "message": message}
        else:
            return {"success": False, "message": f"tag 创建失败: {result.stderr.strip()}"}
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {"success": False, "message": f"Git 操作失败: {e}"}


def git_rollback_to_tag(tag_name: str) -> dict:
    """回滚到指定 tag。"""
    if not is_git_repo():
        return {"success": False, "message": "不在 Git 仓库中"}
    
    try:
        # 检查 tag 是否存在
        result = subprocess.run(
            ["git", "tag", "-l", tag_name],
            capture_output=True, text=True, timeout=5
        )
        if not result.stdout.strip():
            return {"success": False, "message": f"tag 不存在: {tag_name}"}
        
        # 回滚
        result = subprocess.run(
            ["git", "checkout", tag_name],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return {"success": True, "tag": tag_name, "message": f"已回滚到 {tag_name}"}
        else:
            return {"success": False, "message": f"回滚失败: {result.stderr.strip()}"}
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {"success": False, "message": f"Git 操作失败: {e}"}


def git_list_loop_tags(loop_name: str) -> list:
    """列出指定循环的所有 tag。"""
    if not is_git_repo():
        return []
    
    try:
        result = subprocess.run(
            ["git", "tag", "-l", f"loop/{loop_name}/iter/*"],
            capture_output=True, text=True, timeout=5
        )
        tags = [t.strip() for t in result.stdout.strip().split("\n") if t.strip()]
        # 按迭代号排序
        def extract_iter(tag):
            match = re.search(r"iter/(\d+)", tag)
            return int(match.group(1)) if match else 0
        tags.sort(key=extract_iter)
        return tags
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


# ─── 子命令实现 ──────────────────────────────────────────────────────────────

def cmd_init(args: argparse.Namespace) -> None:
    """初始化新的迭代循环。"""
    # v10.1: 输入校验
    validate_name(args.name)
    
    mode = args.mode
    if mode not in VALID_MODES:
        error_exit(f"无效模式 '{mode}'，可选: {', '.join(VALID_MODES)}")

    max_iter = args.max
    if max_iter < 1:
        error_exit("--max 必须 >= 1")
    if max_iter > 1000:
        error_exit("--max 不能超过 1000（防止无限循环）")

    # 解析完成条件
    completion_check = {"type": "none", "pattern": ""}
    if args.condition:
        if ":" in args.condition:
            ctype, pattern = args.condition.split(":", 1)
            ctype = ctype.strip().lower()
            if ctype not in ("regex", "file", "file-changed", "llm"):
                error_exit(f"无效条件类型 '{ctype}'，可选: regex, file, file-changed, llm")
            completion_check = {"type": ctype, "pattern": pattern.strip()}
        else:
            error_exit("条件格式错误，应为 'type:pattern'，如 'regex:BUILD SUCCESS'")

    patience = args.patience if args.patience else DEFAULT_PATIENCE

    state_path = args.state or DEFAULT_STATE_FILE
    
    # v10.1: 并发保护 - 检查是否已有同名循环在运行
    if Path(state_path).exists() and not getattr(args, 'force', False):
        existing = load_state(state_path)
        running_check = check_existing_process(existing)
        if running_check and running_check.get("running"):
            error_exit(
                f"同名循环 '{existing.get('name')}' 已在运行中 "
                f"(PID={running_check.get('pid')})。"
                f"使用 --force 强制重置，或使用 cleanup 命令清理。"
            )

    state = {
        "name": args.name,
        "mode": mode,
        "max_iterations": max_iter,
        "current_iteration": 0,
        "completion_check": completion_check,
        "patience": patience,
        "no_improvement_count": 0,
        "history": [],
        "artifacts": [],
        "status": "running",
        "metadata": {},
        "pid": os.getpid(),  # v10.1: 记录进程 ID
        "auto_commit": getattr(args, 'auto_commit', False),  # v10.2: Git 自动提交
        # v10.3: De-Sloppify 清理轮次
        "sloppify": {
            "enabled": getattr(args, 'sloppify', False),
            "interval": getattr(args, 'sloppify_interval', 2),
            "focus": [
                "删除测试语言/框架行为的测试用例",
                "删除类型系统已保证的冗余运行时检查",
                "删除过度防御性的错误处理",
                "删除 console.log / 注释掉的代码",
                "删除未使用的导入和变量",
                "简化冗余的条件判断",
            ],
        },
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }

    save_state(state_path, state)

    # v10.2: 创建初始 Git tag
    git_result = None
    if state.get("auto_commit"):
        tag_name = f"loop/{args.name}/iter/0"
        git_result = git_create_tag(tag_name, f"pre-iteration snapshot (loop: {args.name}, iter: 0)")

    output_result({
        "action": "init",
        "state_file": state_path,
        "name": args.name,
        "mode": mode,
        "max_iterations": max_iter,
        "pid": os.getpid(),
        "auto_commit": state.get("auto_commit", False),
        "git_tag": git_result,
        "message": f"循环已初始化: {args.name} (模式={mode}, 最大={max_iter})"
    })


def cmd_check(args: argparse.Namespace) -> None:
    """检查是否应继续迭代。"""
    state_path = args.state or DEFAULT_STATE_FILE
    state = load_state(state_path)

    # v10.1: 心跳检测
    heartbeat = check_heartbeat(state, args.heartbeat_timeout)
    
    if state["status"] != "running":
        output_result({
            "action": "check",
            "should_continue": False,
            "reason": f"循环已停止 (status={state['status']})",
            "iteration": state["current_iteration"],
            "heartbeat": heartbeat,
        })
        return

    current = state["current_iteration"]
    max_iter = state["max_iterations"]
    mode = state["mode"]

    if mode == "fixed":
        should_continue = current < max_iter
        # v10.3: 判断是否为清理轮次
        is_sloppify = is_sloppify_round(state, current + 1) if should_continue else False
        output_result({
            "action": "check",
            "should_continue": should_continue,
            "iteration": current,
            "max_iterations": max_iter,
            "remaining": max(0, max_iter - current),
            "reason": "固定次数未用完" if should_continue else "已达最大次数",
            "heartbeat": heartbeat,
            "is_sloppify_round": is_sloppify,  # v10.3
            "sloppify_focus": state.get("sloppify", {}).get("focus", []) if is_sloppify else [],
        })
        return

    if mode == "max":
        if current >= max_iter:
            output_result({
                "action": "check",
                "should_continue": False,
                "iteration": current,
                "reason": "已达最大迭代次数",
                "heartbeat": heartbeat,
            })
            return

        check = state.get("completion_check", {})
        condition_met = evaluate_condition(check, state)
        
        # v10.3: 判断是否为清理轮次
        is_sloppify = is_sloppify_round(state, current + 1) if not condition_met else False

        output_result({
            "action": "check",
            "should_continue": not condition_met,
            "iteration": current,
            "max_iterations": max_iter,
            "condition_met": condition_met,
            "reason": "完成条件已满足" if condition_met else "继续迭代",
            "heartbeat": heartbeat,
            "is_sloppify_round": is_sloppify,  # v10.3
            "sloppify_focus": state.get("sloppify", {}).get("focus", []) if is_sloppify else [],
        })
        return

    if mode == "adaptive":
        if current >= max_iter:
            output_result({
                "action": "check",
                "should_continue": False,
                "iteration": current,
                "reason": "已达最大迭代次数",
                "heartbeat": heartbeat,
            })
            return

        patience = state.get("patience", DEFAULT_PATIENCE)
        no_improve = state.get("no_improvement_count", 0)

        if no_improve >= patience:
            output_result({
                "action": "check",
                "should_continue": False,
                "iteration": current,
                "no_improvement_count": no_improve,
                "patience": patience,
                "reason": f"连续 {no_improve} 轮无改进 (patience={patience})",
                "heartbeat": heartbeat,
            })
            return

        # v10.3: 判断是否为清理轮次
        is_sloppify = is_sloppify_round(state, current + 1)

        output_result({
            "action": "check",
            "should_continue": True,
            "iteration": current,
            "no_improvement_count": no_improve,
            "patience": patience,
            "remaining": max(0, max_iter - current),
            "reason": "继续迭代",
            "heartbeat": heartbeat,
            "is_sloppify_round": is_sloppify,  # v10.3
            "sloppify_focus": state.get("sloppify", {}).get("focus", []) if is_sloppify else [],
        })
        return


def cmd_update(args: argparse.Namespace) -> None:
    """更新当前迭代的结果。"""
    state_path = args.state or DEFAULT_STATE_FILE
    state = load_state(state_path)

    if state["status"] != "running":
        error_exit(f"循环已停止 (status={state['status']})，无法更新")

    result = args.result
    if result not in VALID_RESULTS:
        error_exit(f"无效结果 '{result}'，可选: {', '.join(VALID_RESULTS)}")

    state["current_iteration"] += 1
    current = state["current_iteration"]

    # v10.2: 自动 Git 提交和 tag
    git_result = None
    if state.get("auto_commit"):
        loop_name = state.get("name", "unknown")
        tag_name = f"loop/{loop_name}/iter/{current}"
        git_result = git_create_tag(tag_name, f"pre-iteration snapshot (loop: {loop_name}, iter: {current})")

    entry = {
        "iteration": current,
        "timestamp": now_iso(),
        "result": result,
        "summary": args.summary or "",
    }
    if args.metrics:
        try:
            entry["metrics"] = json.loads(args.metrics)
        except json.JSONDecodeError:
            error_exit("--metrics 必须是有效的 JSON 字符串")

    state["history"].append(entry)

    if state["mode"] == "adaptive":
        if result == "pass":
            state["no_improvement_count"] = 0
        elif result == "partial":
            pass
        else:
            state["no_improvement_count"] = state.get("no_improvement_count", 0) + 1

    if args.artifact:
        if args.artifact not in state["artifacts"]:
            state["artifacts"].append(args.artifact)

    state["updated_at"] = now_iso()
    save_state(state_path, state)

    output_result({
        "action": "update",
        "iteration": current,
        "result": result,
        "git_tag": git_result,
        "message": f"迭代 {current} 已记录 (result={result})",
    })


def cmd_complete(args: argparse.Namespace) -> None:
    """标记循环完成。"""
    state_path = args.state or DEFAULT_STATE_FILE
    state = load_state(state_path)

    reason = args.reason or "手动完成"
    status = args.status if args.status else "completed"

    if status not in VALID_STATUSES:
        error_exit(f"无效状态 '{status}'，可选: {', '.join(VALID_STATUSES)}")

    state["status"] = status
    state["completion_reason"] = reason
    state["completed_at"] = now_iso()
    state["updated_at"] = now_iso()

    save_state(state_path, state)

    total = state["current_iteration"]
    history = state.get("history", [])
    passes = sum(1 for h in history if h.get("result") == "pass")
    fails = sum(1 for h in history if h.get("result") == "fail")

    output_result({
        "action": "complete",
        "status": status,
        "reason": reason,
        "total_iterations": total,
        "passes": passes,
        "fails": fails,
        "message": f"循环已完成: {total} 轮迭代, {passes} 通过, {fails} 失败",
    })


def cmd_cleanup(args: argparse.Namespace) -> None:
    """清理残留状态（v10.1 新增）。"""
    state_path = args.state or DEFAULT_STATE_FILE
    p = Path(state_path)
    
    if not p.exists():
        output_result({
            "action": "cleanup",
            "message": f"状态文件不存在，无需清理: {state_path}",
            "cleaned": False,
        })
        return
    
    state = load_state(state_path)
    
    # 检查是否在运行中
    if state.get("status") == "running" and not args.force:
        error_exit(
            f"循环 '{state.get('name', 'unknown')}' 仍在运行中 (status=running)。"
            f"使用 --force 强制清理。"
        )
    
    # 删除状态文件
    try:
        p.unlink()
        output_result({
            "action": "cleanup",
            "message": f"已清理状态文件: {state_path}",
            "cleaned": True,
            "previous_status": state.get("status"),
            "previous_name": state.get("name"),
        })
    except OSError as e:
        error_exit(f"删除状态文件失败: {e}")


def cmd_rollback(args: argparse.Namespace) -> None:
    """回滚到指定迭代（v10.2 新增）。"""
    loop_name = args.name
    
    # 确定目标迭代号
    if args.initial:
        target_iter = 0
    elif args.to is not None:
        target_iter = args.to
    elif args.prev:
        state_path = args.state or DEFAULT_STATE_FILE
        if not Path(state_path).exists():
            error_exit(f"状态文件不存在: {state_path}")
        state = load_state(state_path)
        current = state.get("current_iteration", 0)
        target_iter = max(0, current - 1)
    else:
        error_exit("必须指定 --to, --prev, 或 --initial")
    
    # 检查 Git 仓库
    if not is_git_repo():
        error_exit("不在 Git 仓库中，无法回滚。请确保在 Git 工作目录中运行。")
    
    # 构建 tag 名称
    tag_name = f"loop/{loop_name}/iter/{target_iter}"
    
    # 列出所有可用的 tag
    available_tags = git_list_loop_tags(loop_name)
    
    if not available_tags:
        error_exit(f"未找到循环 '{loop_name}' 的任何迭代记录。")
    
    # 执行回滚
    result = git_rollback_to_tag(tag_name)
    
    if result.get("success"):
        # 更新状态文件（如果存在）
        state_path = args.state or DEFAULT_STATE_FILE
        if Path(state_path).exists():
            state = load_state(state_path)
            state["current_iteration"] = target_iter
            state["rollback_at"] = now_iso()
            state["rollback_target"] = target_iter
            save_state(state_path, state)
        
        output_result({
            "action": "rollback",
            "loop_name": loop_name,
            "target_iteration": target_iter,
            "tag": tag_name,
            "available_tags": available_tags,
            "message": f"已回滚到迭代 {target_iter} (tag: {tag_name})",
        })
    else:
        error_exit(f"回滚失败: {result.get('message', '未知错误')}")


# ─── 条件评估 ────────────────────────────────────────────────────────────────

def evaluate_condition(check: dict, state: dict) -> bool:
    """评估完成条件是否满足。返回 True 表示条件已满足。"""
    ctype = check.get("type", "none")
    pattern = check.get("pattern", "")

    if ctype == "none":
        return False

    if ctype == "regex":
        history = state.get("history", [])
        if not history:
            return False
        last_summary = history[-1].get("summary", "")
        try:
            return bool(re.search(pattern, last_summary))
        except re.error:
            return False

    if ctype == "file":
        return Path(pattern).exists()

    if ctype == "file-changed":
        p = Path(pattern)
        if not p.exists():
            return False
        history = state.get("history", [])
        if not history:
            return False
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
            last_time = datetime.fromisoformat(history[-1]["timestamp"])
            return mtime > last_time
        except (OSError, ValueError):
            return False

    if ctype == "llm":
        return False

    return False


# ─── Backpressure 门控（v11.4 新增）────────────────────────────────────────────

def detect_test_framework(files: list) -> dict:
    """检测项目中的测试框架。"""
    # Python: pytest
    if Path("pytest.ini").exists() or Path("pyproject.toml").exists():
        # 检查 pyproject.toml 是否有 pytest 配置
        pyproject = Path("pyproject.toml")
        if pyproject.exists():
            content = pyproject.read_text(encoding="utf-8", errors="ignore")
            if "[tool.pytest" in content or "pytest" in content:
                return {"framework": "pytest", "command": "pytest", "detected": True}
        # 检查 conftest.py
        if Path("conftest.py").exists():
            return {"framework": "pytest", "command": "pytest", "detected": True}
        # 检查 tests/ 目录
        if Path("tests").is_dir():
            return {"framework": "pytest", "command": "pytest", "detected": True}

    # Python: unittest
    for f in files:
        if "test_" in str(f) or "_test.py" in str(f):
            return {"framework": "unittest", "command": "python -m unittest", "detected": True}

    # JavaScript/TypeScript: npm test
    package_json = Path("package.json")
    if package_json.exists():
        try:
            content = package_json.read_text(encoding="utf-8")
            pkg = json.loads(content)
            scripts = pkg.get("scripts", {})
            if "test" in scripts:
                return {"framework": "npm-test", "command": "npm test", "detected": True}
        except (json.JSONDecodeError, OSError):
            pass

    return {"framework": None, "command": None, "detected": False}


def detect_lint_tool(files: list) -> dict:
    """检测项目中的 lint 工具。"""
    # Python: ruff
    if Path("ruff.toml").exists() or Path(".ruff.toml").exists():
        return {"tool": "ruff", "check": "ruff check", "fix": "ruff check --fix", "detected": True}
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8", errors="ignore")
        if "[tool.ruff" in content:
            return {"tool": "ruff", "check": "ruff check", "fix": "ruff check --fix", "detected": True}

    # Python: flake8
    if Path(".flake8").exists() or Path("setup.cfg").exists():
        return {"tool": "flake8", "check": "flake8", "fix": None, "detected": True}

    # JavaScript/TypeScript: eslint
    for eslint_cfg in [".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml", "eslint.config.js", "eslint.config.mjs"]:
        if Path(eslint_cfg).exists():
            return {"tool": "eslint", "check": "npx eslint", "fix": "npx eslint --fix", "detected": True}
    package_json = Path("package.json")
    if package_json.exists():
        try:
            content = package_json.read_text(encoding="utf-8")
            pkg = json.loads(content)
            if "eslint" in pkg.get("devDependencies", {}) or "eslint" in pkg.get("dependencies", {}):
                return {"tool": "eslint", "check": "npx eslint", "fix": "npx eslint --fix", "detected": True}
        except (json.JSONDecodeError, OSError):
            pass

    return {"tool": None, "check": None, "fix": None, "detected": False}


def detect_typecheck_tool(files: list) -> dict:
    """检测项目中的类型检查工具。"""
    # Python: mypy
    if Path("mypy.ini").exists() or Path(".mypy.ini").exists():
        return {"tool": "mypy", "command": "mypy", "detected": True}
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8", errors="ignore")
        if "[tool.mypy" in content:
            return {"tool": "mypy", "command": "mypy", "detected": True}

    # TypeScript: tsc
    if Path("tsconfig.json").exists():
        return {"tool": "tsc", "command": "npx tsc --noEmit", "detected": True}

    return {"tool": None, "command": None, "detected": False}


def run_gate(name: str, command: str, files: list, timeout: int = 60) -> dict:
    """运行单个门控检查。"""
    # 构建命令（附加文件参数）
    full_cmd = command
    if files:
        # 对于 pytest/npm test，不直接附加文件名（它们自动发现）
        if name in ("pytest", "unittest", "npm-test"):
            pass  # 不附加文件
        else:
            full_cmd = f"{command} {' '.join(str(f) for f in files)}"

    try:
        result = subprocess.run(
            full_cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace"
        )
        passed = result.returncode == 0
        return {
            "gate": name,
            "status": "pass" if passed else "fail",
            "command": full_cmd,
            "exit_code": result.returncode,
            "stdout": result.stdout[-2000:] if result.stdout else "",  # 截断过长输出
            "stderr": result.stderr[-2000:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "gate": name,
            "status": "timeout",
            "command": full_cmd,
            "error": f"超时 ({timeout}s)",
        }
    except FileNotFoundError:
        return {
            "gate": name,
            "status": "skip",
            "command": full_cmd,
            "reason": "命令不存在",
        }


def find_related_tests(files: list) -> list:
    """根据修改的文件查找相关测试文件。"""
    test_files = []
    for f in files:
        f_str = str(f)
        # Python: src/main.py → tests/test_main.py
        if f_str.endswith(".py"):
            base = Path(f_str).stem
            candidates = [
                Path(f"tests/test_{base}.py"),
                Path(f"test/test_{base}.py"),
                Path(f"test_{base}.py"),
            ]
            for c in candidates:
                if c.exists() and c not in test_files:
                    test_files.append(c)
        # JS/TS: src/main.ts → tests/main.test.ts
        elif f_str.endswith((".ts", ".js", ".tsx", ".jsx")):
            base = Path(f_str).stem
            candidates = [
                Path(f"tests/{base}.test.ts"),
                Path(f"tests/{base}.test.js"),
                Path(f"tests/{base}.spec.ts"),
                Path(f"tests/{base}.spec.js"),
                Path(f"__tests__/{base}.test.ts"),
                Path(f"__tests__/{base}.test.js"),
            ]
            for c in candidates:
                if c.exists() and c not in test_files:
                    test_files.append(c)
    return [str(t) for t in test_files]


def cmd_gates(args: argparse.Namespace) -> None:
    """运行三层门控检查（v11.4 新增）。

    Gate 1: 编译门控（必须通过）
    Gate 2: 测试门控（复杂度 >= medium 时运行）
    Gate 3: 质量门控（lint + typecheck，仅在项目已配置时运行）
    """
    files = [f.strip() for f in args.files.split(",") if f.strip()] if args.files else []
    complexity = args.complexity or "medium"
    skip_gates = getattr(args, 'skip_gates', False)

    if skip_gates:
        output_result({
            "action": "gates",
            "overall": "skip",
            "reason": "用户指定 --skip-gates",
            "gates": {},
        })
        return

    gates = {}
    overall = "pass"

    # ─── Gate 1: 编译门控 ───
    compile_commands = []
    for f in files:
        if f.endswith(".py"):
            compile_commands.append(("compile-py", f"python -m py_compile {f}"))
        elif f.endswith((".js", ".jsx")):
            compile_commands.append(("compile-js", f"node --check {f}"))
        elif f.endswith((".ts", ".tsx")):
            compile_commands.append(("compile-ts", f"npx tsc --noEmit {f}"))
        elif f.endswith(".sh"):
            compile_commands.append(("compile-sh", f"bash -n {f}"))

    if compile_commands:
        for gate_name, cmd in compile_commands:
            result = run_gate(gate_name, cmd, [], timeout=30)
            gates[gate_name] = result
            if result["status"] != "pass":
                overall = "fail"
    else:
        gates["compile"] = {"status": "skip", "reason": "无可编译文件"}

    # ─── Gate 2: 测试门控（复杂度 >= medium）───
    if complexity in ("medium", "large", "critical"):
        test_fw = detect_test_framework(files)
        if test_fw["detected"]:
            # 查找相关测试文件
            related_tests = find_related_tests(files)
            if related_tests and test_fw["framework"] == "pytest":
                # 只运行相关测试
                test_cmd = f"pytest {' '.join(related_tests)} -x --tb=short"
            else:
                test_cmd = test_fw["command"]
            gates["test"] = run_gate("test", test_cmd, files, timeout=120)
            if gates["test"]["status"] != "pass":
                overall = "fail"
        else:
            gates["test"] = {"status": "skip", "reason": "未检测到测试框架"}
    else:
        gates["test"] = {"status": "skip", "reason": f"复杂度 {complexity} < medium，跳过测试"}

    # ─── Gate 3: 质量门控 ───
    # Lint
    lint = detect_lint_tool(files)
    if lint["detected"]:
        gates["lint"] = run_gate("lint", lint["check"], files, timeout=60)
        if gates["lint"]["status"] != "pass":
            # lint 失败不阻止整体通过（仅 warning），但记录
            gates["lint"]["fix_command"] = lint.get("fix")
    else:
        gates["lint"] = {"status": "skip", "reason": "未配置 lint 工具"}

    # Typecheck
    tc = detect_typecheck_tool(files)
    if tc["detected"]:
        gates["typecheck"] = run_gate("typecheck", tc["command"], files, timeout=60)
        if gates["typecheck"]["status"] != "pass":
            overall = "fail"
    else:
        gates["typecheck"] = {"status": "skip", "reason": "未配置 typecheck 工具"}

    # ─── 构建修复提示 ───
    fix_prompt_parts = []
    if overall == "fail":
        for gate_name, gate_result in gates.items():
            if gate_result["status"] == "fail":
                errors = gate_result.get("stderr", "") or gate_result.get("stdout", "")
                if errors:
                    fix_prompt_parts.append(f"[{gate_name}] {errors[:500]}")

    # ─── 输出 ───
    result_data = {
        "action": "gates",
        "overall": overall,
        "complexity": complexity,
        "files": files,
        "gates": gates,
    }

    if overall == "fail":
        result_data["action_needed"] = "fix_and_recheck"
        result_data["fix_prompt"] = "Fix the following gate failures:\n" + "\n---\n".join(fix_prompt_parts)
        # 自动修复提示
        lint_gate = gates.get("lint", {})
        if lint_gate.get("status") == "fail" and lint_gate.get("fix_command"):
            result_data["auto_fix_hint"] = f"Run: {lint_gate['fix_command']}"
    elif overall == "pass":
        result_data["action_needed"] = "proceed"
        result_data["message"] = "所有门控通过"

    output_result(result_data)


def cmd_report(args: argparse.Namespace) -> None:
    """生成迭代过程静态 HTML 报告（v11.4 新增）。"""
    state_path = args.state or DEFAULT_STATE_FILE
    state = load_state(state_path)

    fmt = getattr(args, 'format', 'html')
    output_path = args.output or f"iteration-report-{state.get('name', 'unknown')}.html"

    name = state.get("name", "unknown")
    status = state.get("status", "unknown")
    mode = state.get("mode", "unknown")
    max_iter = state.get("max_iterations", 0)
    current = state.get("current_iteration", 0)
    history = state.get("history", [])
    created_at = state.get("created_at", "")
    completed_at = state.get("completed_at", "")

    # 统计
    passes = sum(1 for h in history if h.get("result") == "pass")
    fails = sum(1 for h in history if h.get("result") == "fail")
    partials = sum(1 for h in history if h.get("result") == "partial")

    if fmt == "json":
        output_result({
            "action": "report",
            "format": "json",
            "name": name,
            "status": status,
            "iterations": {
                "total": current,
                "max": max_iter,
                "passes": passes,
                "fails": fails,
                "partials": partials,
            },
            "history": history,
            "output_file": output_path,
        })
        return

    # HTML 报告
    rows = ""
    for i, h in enumerate(history):
        result = h.get("result", "unknown")
        icon = "✅" if result == "pass" else "❌" if result == "fail" else "⚠️"
        summary = h.get("summary", "")[:100]
        ts = h.get("timestamp", "")[:19]
        metrics = h.get("metrics", {})
        metrics_str = ", ".join(f"{k}: {v}" for k, v in metrics.items()) if metrics else "-"
        rows += f"""
        <tr>
            <td>{i + 1}</td>
            <td>{icon} {result}</td>
            <td>{ts}</td>
            <td>{summary}</td>
            <td>{metrics_str}</td>
        </tr>"""

    # 门控结果（如果有 gates 数据）
    gates_section = ""
    gates_data = state.get("gates", {})
    if gates_data:
        gates_rows = ""
        for gate_name, gate_result in gates_data.items():
            g_status = gate_result.get("status", "unknown")
            g_icon = "✅" if g_status == "pass" else "❌" if g_status == "fail" else "⏭️"
            g_cmd = gate_result.get("command", "-")
            gates_rows += f"<tr><td>{gate_name}</td><td>{g_icon} {g_status}</td><td><code>{g_cmd}</code></td></tr>"
        gates_section = f"""
        <h2>🚧 Backpressure 门控</h2>
        <table>
            <tr><th>门控</th><th>状态</th><th>命令</th></tr>
            {gates_rows}
        </table>
        """

    progress_pct = int((current / max_iter) * 100) if max_iter > 0 else 0
    status_color = "#22c55e" if status == "completed" else "#ef4444" if status == "failed" else "#3b82f6"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>迭代报告: {name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; padding: 2rem; }}
        .container {{ max-width: 960px; margin: 0 auto; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; color: #f8fafc; }}
        h2 {{ font-size: 1.2rem; margin: 1.5rem 0 0.75rem; color: #94a3b8; border-bottom: 1px solid #334155; padding-bottom: 0.5rem; }}
        .meta {{ color: #64748b; font-size: 0.875rem; margin-bottom: 1.5rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
        .stat {{ background: #1e293b; border-radius: 8px; padding: 1rem; text-align: center; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; }}
        .stat-label {{ font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; }}
        .progress {{ background: #1e293b; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem; }}
        .progress-bar {{ height: 8px; background: #334155; border-radius: 4px; overflow: hidden; margin-top: 0.5rem; }}
        .progress-fill {{ height: 100%; background: {status_color}; border-radius: 4px; transition: width 0.3s; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }}
        th {{ text-align: left; padding: 0.5rem; background: #1e293b; color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        td {{ padding: 0.5rem; border-bottom: 1px solid #1e293b; font-size: 0.875rem; }}
        code {{ background: #1e293b; padding: 0.125rem 0.375rem; border-radius: 4px; font-size: 0.8rem; color: #7dd3fc; }}
        .footer {{ text-align: center; color: #475569; font-size: 0.75rem; margin-top: 2rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 迭代报告: {name}</h1>
        <div class="meta">
            模式: {mode} | 状态: <span style="color:{status_color}">{status}</span> | 
            创建: {created_at[:19]} | 完成: {completed_at[:19] if completed_at else '-'}
        </div>

        <div class="stats">
            <div class="stat">
                <div class="stat-value">{current}/{max_iter}</div>
                <div class="stat-label">迭代次数</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color:#22c55e">{passes}</div>
                <div class="stat-label">通过</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color:#ef4444">{fails}</div>
                <div class="stat-label">失败</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color:#f59e0b">{partials}</div>
                <div class="stat-label">部分</div>
            </div>
        </div>

        <div class="progress">
            <div style="display:flex;justify-content:space-between;font-size:0.875rem;">
                <span>进度</span><span>{progress_pct}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width:{progress_pct}%"></div>
            </div>
        </div>

        {gates_section}

        <h2>📝 迭代历史</h2>
        <table>
            <tr><th>#</th><th>结果</th><th>时间</th><th>摘要</th><th>指标</th></tr>
            {rows}
        </table>

        <div class="footer">
            Generated by loop-controller.py v11.4 | {datetime.now(timezone.utc).isoformat()[:19]}Z
        </div>
    </div>
</body>
</html>"""

    # 写入文件
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        output_result({
            "action": "report",
            "format": fmt,
            "output_file": output_path,
            "name": name,
            "iterations": current,
            "passes": passes,
            "fails": fails,
            "message": f"报告已生成: {output_path}",
        })
    except OSError as e:
        error_exit(f"写入报告失败: {e}")


# ─── 参数解析 ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="迭代循环控制器 — 管理迭代状态和生命周期 (v10.1)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    p_init = subparsers.add_parser("init", help="初始化新的迭代循环")
    p_init.add_argument("--name", required=True, help="循环任务名称 (仅允许中英文、数字、下划线、连字符)")
    p_init.add_argument("--mode", default="max", choices=VALID_MODES, help="迭代模式 (默认: max)")
    p_init.add_argument("--max", type=int, default=10, help="最大迭代次数 (默认: 10, 最大: 1000)")
    p_init.add_argument("--condition", help="完成条件，格式: type:pattern")
    p_init.add_argument("--patience", type=int, help="adaptive 模式的耐心值 (默认: 3)")
    p_init.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_init.add_argument("--force", action="store_true", help="强制重置已存在的循环")
    p_init.add_argument("--auto-commit", action="store_true",
                        help="v10.2: 每次迭代前自动创建 Git 提交和 tag，支持回滚")
    # v10.3: De-Sloppify 清理轮次
    p_init.add_argument("--sloppify", action="store_true",
                        help="v10.3: 启用 De-Sloppify 清理轮次（每 N 轮实现后加 1 轮清理）")
    p_init.add_argument("--sloppify-interval", type=int, default=2,
                        help="v10.3: De-Sloppify 间隔（默认每 2 轮实现后加 1 轮清理）")

    p_check = subparsers.add_parser("check", help="检查是否应继续迭代")
    p_check.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_check.add_argument("--heartbeat-timeout", type=int, default=DEFAULT_HEARTBEAT_TIMEOUT,
                         help=f"心跳超时秒数 (默认: {DEFAULT_HEARTBEAT_TIMEOUT})")

    p_update = subparsers.add_parser("update", help="更新当前迭代结果")
    p_update.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_update.add_argument("--result", required=True, choices=VALID_RESULTS, help="本轮结果")
    p_update.add_argument("--summary", help="本轮摘要")
    p_update.add_argument("--metrics", help="指标数据 (JSON 字符串)")
    p_update.add_argument("--artifact", help="产出文件路径")

    p_complete = subparsers.add_parser("complete", help="标记循环完成")
    p_complete.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_complete.add_argument("--reason", help="完成原因")
    p_complete.add_argument("--status", choices=VALID_STATUSES, help="最终状态 (默认: completed)")

    # v10.1: cleanup 子命令
    p_cleanup = subparsers.add_parser("cleanup", help="清理残留状态 (v10.1 新增)")
    p_cleanup.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_cleanup.add_argument("--force", action="store_true", help="强制清理运行中的循环")

    # v10.2: rollback 子命令
    p_rollback = subparsers.add_parser("rollback", help="回滚到指定迭代 (v10.2 新增)")
    p_rollback.add_argument("--name", required=True, help="循环任务名称")
    p_rollback.add_argument("--to", type=int, help="回滚到指定迭代号")
    p_rollback.add_argument("--prev", action="store_true", help="回滚到上一次迭代")
    p_rollback.add_argument("--initial", action="store_true", help="回滚到循环开始前 (iter/0)")
    p_rollback.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")

    # v11.4: gates 子命令（Backpressure 门控）
    p_gates = subparsers.add_parser("gates", help="运行三层门控检查 (v11.4 新增)")
    p_gates.add_argument("--files", help="要检查的文件列表（逗号分隔）")
    p_gates.add_argument("--complexity", choices=["trivial", "small", "medium", "large", "critical"],
                         default="medium", help="任务复杂度（影响门控严格程度）")
    p_gates.add_argument("--skip-gates", action="store_true", help="跳过所有门控")

    # v11.4: report 子命令（迭代报告）
    p_report = subparsers.add_parser("report", help="生成迭代过程报告 (v11.4 新增)")
    p_report.add_argument("--state", help="状态文件路径 (默认: loop-state.json)")
    p_report.add_argument("--format", choices=["html", "json"], default="html", help="输出格式")
    p_report.add_argument("--output", help="输出文件路径 (默认: iteration-report-<name>.html)")

    return parser


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "init": cmd_init,
        "check": cmd_check,
        "update": cmd_update,
        "complete": cmd_complete,
        "cleanup": cmd_cleanup,      # v10.1 新增
        "rollback": cmd_rollback,    # v10.2 新增
        "gates": cmd_gates,          # v11.4 新增
        "report": cmd_report,        # v11.4 新增
    }

    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
