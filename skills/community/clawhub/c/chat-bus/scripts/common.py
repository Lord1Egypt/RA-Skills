#!/usr/bin/env python3
"""
chat-bus 公共层
共享目录消息总线 — 用户注册、消息收发、房间管理
纯 Python 标准库，零外部依赖
"""

import sys
import os
import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path


# ─── Exit Codes ───────────────────────────────────────────
EXIT_OK = 0
EXIT_PARAM_ERROR = 1
EXIT_EXEC_ERROR = 2


# ─── JSON Protocol ────────────────────────────────────────
def parse_input():
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        return None
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        output_error(f"JSON 解析失败: {e}", EXIT_PARAM_ERROR)


def output_ok(data=None, message="ok"):
    result = {"status": "ok", "data": data, "message": message}
    print(json.dumps(result, ensure_ascii=False, default=str))


def output_error(message, code=EXIT_EXEC_ERROR):
    result = {"status": "error", "code": code, "message": message}
    print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
    sys.exit(code)


def get_param(params, key, default=None, required=False):
    if params is None:
        if required:
            output_error(f"缺少必要参数: {key}", EXIT_PARAM_ERROR)
        return default
    value = params.get(key, default)
    if required and (value is None or value == ""):
        output_error(f"缺少必要参数: {key}", EXIT_PARAM_ERROR)
    return value


# ─── Chat Bus Paths ───────────────────────────────────────
def get_chat_root(params=None):
    """获取共享目录根路径"""
    if params:
        custom = params.get("chat_dir") or params.get("shared_dir")
        if custom:
            return resolve_path(custom, must_exist=False)
    # 默认：当前工作目录下的 .chat-bus/
    return Path.cwd() / ".chat-bus"


def resolve_path(path, must_exist=False):
    if not path:
        output_error("路径不能为空", EXIT_PARAM_ERROR)
    p = Path(path)
    if not p.is_absolute():
        p = Path.cwd() / p
    p = p.resolve()
    if must_exist and not p.exists():
        output_error(f"路径不存在: {p}", EXIT_EXEC_ERROR)
    return p


def init_chat_root(chat_root):
    """初始化聊天目录结构"""
    (chat_root / "users").mkdir(parents=True, exist_ok=True)
    (chat_root / "inbox").mkdir(parents=True, exist_ok=True)
    (chat_root / "rooms").mkdir(parents=True, exist_ok=True)
    return chat_root


# ─── User Helpers ─────────────────────────────────────────
def get_current_user(params):
    """获取当前用户名"""
    username = get_param(params, "user") or get_param(params, "username") or get_param(params, "from")
    if not username:
        output_error("缺少 user 参数", EXIT_PARAM_ERROR)
    # 安全化用户名（仅允许字母数字下划线）
    safe = "".join(c for c in str(username) if c.isalnum() or c in "_-")
    if not safe:
        output_error(f"无效用户名: {username}", EXIT_PARAM_ERROR)
    return safe


def load_user_profile(chat_root, username):
    """加载用户配置"""
    profile_path = chat_root / "users" / f"{username}.json"
    if not profile_path.exists():
        return None
    try:
        return json.loads(profile_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_user_profile(chat_root, username, profile):
    """保存用户配置"""
    profile_path = chat_root / "users" / f"{username}.json"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    return profile_path


def ensure_inbox(chat_root, username):
    """确保用户收件箱目录存在"""
    inbox = chat_root / "inbox" / username
    inbox.mkdir(parents=True, exist_ok=True)
    return inbox


# ─── Message Helpers ──────────────────────────────────────
def gen_message_id():
    """生成消息 ID"""
    return uuid.uuid4().hex[:12]


def timestamp_str():
    """当前时间戳字符串"""
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def timestamp_iso():
    """当前时间 ISO 格式"""
    return datetime.now().isoformat()


def format_message_filename(sender, msg_id, ts=None):
    """生成消息文件名"""
    ts = ts or timestamp_str()
    return f"{ts}_{sender}_{msg_id}.json"


def parse_message_filename(filename):
    """解析消息文件名"""
    stem = Path(filename).stem
    # 格式: 2026-04-13_220500_alice_abc123def456
    parts = stem.split("_", 3)
    if len(parts) >= 4:
        return {
            "date": parts[0],
            "time": parts[1],
            "sender": parts[2],
            "id": parts[3],
        }
    return {"raw": stem}


def save_message(path, message):
    """保存消息到文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(message, ensure_ascii=False, indent=2), encoding="utf-8")


def load_message(path):
    """加载消息文件"""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
