#!/usr/bin/env python3
"""
Codex notify hook（通用版本）
- 核心行为：发送 Telegram 通知 + 更新项目状态文件（由 Cron 推进）
- 不再启动新的 agent session（避免上下文割裂）

环境变量：
- OPENCLAW_AGENT_NAME: Agent 名称（用于选择 bot 账号）
- OPENCLAW_AGENT_CHAT_ID: 通知目标 chat ID
- OPENCLAW_AGENT_CHANNEL: 通知渠道
- OPENCLAW_PROJECT_STATE_FILE: 项目状态文件路径（可选，设置后启用状态模式）
- OPENCLAW_PROJECT_TASK_ID: 任务 ID（可选）
- OPENCLAW_PROJECT_TASK_DIR: 任务目录（可选）
"""
import json
import os
import subprocess
import sys
from datetime import datetime

# 日志文件隔离（按 agent 名称）
AGENT_NAME = os.environ.get("OPENCLAW_AGENT_NAME") or os.environ.get("CODEX_AGENT_NAME", "")
LOG_FILE = os.environ.get("OPENCLAW_LOG_FILE", f"/tmp/codex_notify_{AGENT_NAME or 'default'}.log")

# ============ 配置（从环境变量读取）============
CHAT_ID = os.environ.get("OPENCLAW_AGENT_CHAT_ID") or os.environ.get("CODEX_AGENT_CHAT_ID", "")
CHANNEL = os.environ.get("OPENCLAW_AGENT_CHANNEL") or os.environ.get("CODEX_AGENT_CHANNEL", "telegram")
PROJECT_STATE_FILE = os.environ.get("OPENCLAW_PROJECT_STATE_FILE", "")
PROJECT_TASK_ID = os.environ.get("OPENCLAW_PROJECT_TASK_ID", "")
PROJECT_TASK_DIR = os.environ.get("OPENCLAW_PROJECT_TASK_DIR", "")

# Bot 账号映射（根据 agent 名称选择）
AGENT_ACCOUNT_MAP = {
    "glm-agent": "geq1fan_bot",
    "kimi-agent": "Geq1fanBot",
    "gpt-agent": "Geq1fan_2Bot",
    "main": "geq1fan_bot",
}

ACCOUNT_ID = AGENT_ACCOUNT_MAP.get(AGENT_NAME, "geq1fan_bot")

# Telegram sender 脚本路径（相对路径，基于 skill 目录）
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENDER_SCRIPT = os.path.join(SKILL_DIR, "..", "telegram-sender", "scripts", "send.py")


def log(msg: str) -> None:
    """写入日志（用于调试）"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def send_notification(msg: str) -> bool:
    """发送 Telegram 通知（用户实时可见）"""
    try:
        full_msg = f"[{AGENT_NAME.upper()}] 🔔 Codex 任务完成\n\n{msg}"
        proc = subprocess.Popen(
            [
                "python3", SENDER_SCRIPT,
                "-m", full_msg,
                "-c", CHAT_ID,
                "-a", ACCOUNT_ID,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate(timeout=30)
        if proc.returncode != 0:
            log(f"send failed: {stderr.decode()[:200]}")
            return False
        log(f"send success: {stdout.decode()[:100]}")
        return True
    except Exception as e:
        log(f"send error: {e}")
        return False


def update_project_state(notification: dict) -> bool:
    """
    更新项目状态文件（由 Cron 巡检推进）
    
    状态文件结构参考：
    https://github.com/your-repo/codex-agent/blob/main/docs/project-state-schema.md
    """
    if not PROJECT_STATE_FILE or not PROJECT_TASK_ID:
        return False
    
    try:
        # 读取现有状态
        if os.path.exists(PROJECT_STATE_FILE):
            with open(PROJECT_STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        else:
            # 初始化新状态文件
            state = {
                "project": "codex-task",
                "sessionKey": f"agent:{AGENT_NAME}:main",
                "notificationRouting": {
                    "channel": CHANNEL,
                    "target": CHAT_ID,
                    "accountId": ACCOUNT_ID
                }
            }
        
        summary = notification.get("last-assistant-message", "Done")
        cwd = notification.get("cwd", PROJECT_TASK_DIR or "unknown")
        thread_id = notification.get("thread-id", "unknown")
        
        # 更新 activeTask
        active = state.get("activeTask", {})
        active["taskId"] = PROJECT_TASK_ID
        active["taskDir"] = PROJECT_TASK_DIR or cwd
        active["status"] = "review_pending"  # Codex 已完成，等待 review
        active["phase"] = "implementation"
        
        # 更新 runner 信息
        runner = active.get("runner", {})
        runner["kind"] = "codex_exec"
        runner["status"] = "completed"
        runner["completedAt"] = now_iso()
        runner["summary"] = summary
        runner["threadId"] = thread_id
        runner["cwd"] = cwd
        runner["agentName"] = AGENT_NAME or "main"
        active["runner"] = runner
        
        # 生成 wakeKey（用于去重）
        wake_key = f"{PROJECT_TASK_ID}:review_pending:{runner['completedAt']}"
        active["notify"] = active.get("notify", {})
        active["notify"]["lastWakeKey"] = ""  # 清空，让 Cron 可以推进
        
        state["activeTask"] = active
        state["updatedAt"] = now_iso()
        
        # 写回文件
        with open(PROJECT_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        log(f"project state updated: task={PROJECT_TASK_ID}, status=review_pending")
        return True
    except Exception as e:
        log(f"project state update error: {e}")
        return False


def main() -> int:
    if len(sys.argv) < 2:
        log("no payload received")
        return 0

    try:
        notification = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        log(f"JSON error: {e}")
        return 1

    if notification.get("type") != "agent-turn-complete":
        log(f"ignored event type: {notification.get('type')}")
        return 0

    summary = notification.get("last-assistant-message", "Done")
    cwd = notification.get("cwd", "unknown")
    thread_id = notification.get("thread-id", "unknown")

    log(f"complete: agent={AGENT_NAME}, account={ACCOUNT_ID}")
    log(f"summary: {summary[:100]}")

    # 1. 发送 Telegram 通知（实时推送给用户）
    if CHAT_ID:
        agent_msg = (
            f"📁 {cwd}\n"
            f"💬 {summary}\n"
            f"thread: {thread_id}"
        )
        send_notification(agent_msg)
    else:
        log("CHAT_ID not set, skipping notification")

    # 2. 更新项目状态文件（由 Cron 巡检推进）
    if PROJECT_STATE_FILE and PROJECT_TASK_ID:
        update_project_state(notification)
    else:
        log("project state mode not active (missing PROJECT_STATE_FILE or PROJECT_TASK_ID)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
