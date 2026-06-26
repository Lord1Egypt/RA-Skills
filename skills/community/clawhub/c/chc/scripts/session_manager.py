#!/usr/bin/env python3
"""
CHC Session Manager - Claude Code CLI 会话管理工具

用法:
    python session_manager.py list          # 列出所有会话
    python session_manager.py status <id>   # 查看会话状态
    python session_manager.py clean         # 清理过期会话
    python session_manager.py info          # 显示配置信息
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

CLAUDE_SESSIONS_DIR = Path.home() / ".claude" / "sessions"
CLAUDE_SETTINGS_FILE = Path.home() / ".claude" / "settings.json"


def list_sessions():
    """列出所有 Claude Code 会话"""
    if not CLAUDE_SESSIONS_DIR.exists():
        print("未找到会话目录")
        return

    sessions = []
    for session_file in CLAUDE_SESSIONS_DIR.glob("*.json"):
        try:
            with open(session_file) as f:
                data = json.load(f)
            sessions.append({
                "id": session_file.stem,
                "cwd": data.get("cwd", "unknown"),
                "model": data.get("model", "unknown"),
                "created": data.get("createdAt", "unknown"),
                "updated": data.get("updatedAt", "unknown"),
                "messages": len(data.get("messages", [])),
            })
        except Exception as e:
            print(f"读取 {session_file} 失败: {e}")

    if not sessions:
        print("无活跃会话")
        return

    print(f"\n找到 {len(sessions)} 个会话:\n")
    for s in sessions:
        print(f"  [{s['id'][:8]}...]")
        print(f"    目录: {s['cwd']}")
        print(f"    模型: {s['model']}")
        print(f"    消息: {s['messages']} 条")
        print(f"    创建: {s['created']}")
        print()


def session_status(session_id: str):
    """查看特定会话状态"""
    session_file = CLAUDE_SESSIONS_DIR / f"{session_id}.json"
    if not session_file.exists():
        print(f"会话 {session_id} 不存在")
        return

    try:
        with open(session_file) as f:
            data = json.load(f)

        print(f"\n会话详情: {session_id}\n")
        print(f"  工作目录: {data.get('cwd', 'unknown')}")
        print(f"  模型: {data.get('model', 'unknown')}")
        print(f"  创建时间: {data.get('createdAt', 'unknown')}")
        print(f"  更新时间: {data.get('updatedAt', 'unknown')}")
        print(f"  消息数量: {len(data.get('messages', []))}")

        # 显示最近几条消息摘要
        messages = data.get("messages", [])
        if messages:
            print(f"\n  最近消息:")
            for msg in messages[-3:]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                if isinstance(content, list):
                    content = content[0].get("text", "")[:50] if content else ""
                print(f"    [{role}] {content[:50]}...")

    except Exception as e:
        print(f"读取会话失败: {e}")


def clean_sessions(days_old: int = 7):
    """清理过期会话"""
    if not CLAUDE_SESSIONS_DIR.exists():
        print("未找到会话目录")
        return

    cleaned = 0
    cutoff = datetime.now().timestamp() - (days_old * 86400)

    for session_file in CLAUDE_SESSIONS_DIR.glob("*.json"):
        try:
            with open(session_file) as f:
                data = json.load(f)
            updated = data.get("updatedAt", "")
            if updated:
                # 解析 ISO 时间戳
                ts = datetime.fromisoformat(updated.replace("Z", "+00:00")).timestamp()
                if ts < cutoff:
                    session_file.unlink()
                    cleaned += 1
                    print(f"已删除: {session_file.stem}")
        except Exception:
            pass

    print(f"\n清理完成: 删除 {cleaned} 个过期会话 (> {days_old} 天)")


def show_config():
    """显示 Claude Code 配置"""
    if not CLAUDE_SETTINGS_FILE.exists():
        print("未找到配置文件")
        return

    try:
        with open(CLAUDE_SETTINGS_FILE) as f:
            data = json.load(f)

        print("\nClaude Code 配置:\n")

        # API 配置
        env = data.get("env", {})
        if env:
            print("  API 配置:")
            base_url = env.get("ANTHROPIC_BASE_URL", "默认")
            print(f"    Base URL: {base_url}")
            auth_token = env.get("ANTHROPIC_AUTH_TOKEN", "")
            print(f"    Auth Token: {'已设置' if auth_token else '未设置'}")

        # 模型
        model = data.get("model", "默认")
        print(f"  模型: {model}")

        # 其他配置
        for key in ["thinking", "enableTokenCache", "allowedTools"]:
            if key in data:
                print(f"  {key}: {data[key]}")

    except Exception as e:
        print(f"读取配置失败: {e}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "list":
        list_sessions()
    elif command == "status":
        if len(sys.argv) < 3:
            print("需要会话 ID: python session_manager.py status <session-id>")
        else:
            session_status(sys.argv[2])
    elif command == "clean":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        clean_sessions(days)
    elif command == "info":
        show_config()
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()