"""core/session.py — 多 AI 客户端 Session 读取与解析

支持来源：
  - OpenClaw:       ~/.openclaw/agents/main/sessions/*.jsonl
  - Claude Cowork:  ~/Library/Application Support/Claude/local-agent-mode-sessions/**/*.jsonl
"""
from __future__ import annotations

import json, re, sys
from pathlib import Path
from datetime import datetime

HOME = Path.home()

# ── OpenClaw paths ───────────────────────────────────────
AGENTS_DIR = HOME / ".openclaw" / "agents"
SESSIONS_FILE = AGENTS_DIR / "main" / "sessions" / "sessions.json"
WORKSPACE_DIR = HOME / ".openclaw" / "workspace"

# ── Claude Cowork paths (macOS only) ─────────────────────
if sys.platform == "darwin":
    CLAUDE_SESSIONS_BASE = (
        HOME / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions"
    )
else:
    CLAUDE_SESSIONS_BASE = None

# 用于区分来源的前缀
_CLAUDE_PREFIX = "claude::"


# ── 系统消息过滤 ────────────────────────────────────────────

_SYSTEM_MSG_PATTERNS = (
    "System:",           # OpenClaw 心跳/系统事件
    "[Queued messages",  # OpenClaw 队列消息头
    "Exec completed",   # OpenClaw exec 完成通知
    "Conversation info", # Telegram 元数据包装
    "Sender ",          # Telegram sender 元数据
)

# 排除的消息类型（非真实用户对话）
_EXCLUDED_TYPES = {"toolResult", "toolCall", "system"}


def _is_real_user_message(text: str) -> bool:
    """判断一段文字是否是真实用户对话，而非 OpenClaw 内部系统消息。"""
    if not text or len(text.strip()) < 3:
        return False
    # 排除以系统标记开头的内容
    for pat in _SYSTEM_MSG_PATTERNS:
        if pat in text:
            return False
    return True


def _strip_telegram_meta(text: str) -> str:
    """去除 Telegram 元数据和 OpenClaw 系统事件包装，提取实际用户文本。"""
    try:
        # Telegram 元数据
        text = re.sub(r'System:\s*\[[^\]]+\]\s*', '', text)
        text = re.sub(
            r'Conversation info[^`]*`{3,}json.*?`{3,}',
            '', text, flags=re.DOTALL
        )
        text = re.sub(
            r'Sender[^`]*`{3,}json.*?`{3,}',
            '', text, flags=re.DOTALL
        )
        # OpenClaw 队列消息标记
        text = re.sub(r'\[Queued messages[^\]]*\]', '', text)
        text = re.sub(r'Queued #\d+', '', text)
        # OpenClaw exec 完成通知
        text = re.sub(r'Exec completed[^:\n]*::[^\n]+', '', text)
    except Exception as e:
        print(f"[session] strip_telegram_meta error: {e}")
    return text.strip()


# ── 通用 JSONL 解析（兼容 OpenClaw 和 Claude Cowork 格式）──

def _read_jsonl_messages(file_path: Path, limit: int = 100) -> list[dict]:
    """
    从任意 JSONL 文件读取消息，兼容两种格式：
      OpenClaw:      {"type": "message", "message": {"role": ..., "content": [...]}}
      Claude Cowork: {"type": "user"|"assistant", "message": {"role": ..., "content": ...}}

    过滤规则：
      - 排除 toolResult / toolCall / system 类型
      - 排除 OpenClaw 内部系统消息（System: / [Queued messages] / Exec completed 等）
      - 仅保留真实用户对话
    """
    messages = []
    try:
        with open(file_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    msg_type = obj.get("type", "")

                    # 排除非对话类型
                    if msg_type in _EXCLUDED_TYPES:
                        continue

                    # OpenClaw: type == "message"
                    if msg_type == "message":
                        msg = obj.get("message", {})
                        if not isinstance(msg, dict):
                            continue
                        role = msg.get("role", "")
                        content = msg.get("content", [])

                    # Claude Cowork: type == "user" or "assistant"
                    elif msg_type in ("user", "assistant"):
                        role = msg_type
                        msg = obj.get("message", {})
                        if isinstance(msg, dict):
                            content = msg.get("content", [])
                        else:
                            content = obj.get("content", [])
                    else:
                        continue

                    # 提取文本
                    text_parts = []
                    if isinstance(content, list):
                        for item in content:
                            if not isinstance(item, dict):
                                continue
                            if item.get("type") == "text":
                                raw = item.get("text", "")
                                cleaned = _strip_telegram_meta(raw)
                                if cleaned and _is_real_user_message(cleaned):
                                    text_parts.append(cleaned)
                    elif isinstance(content, str):
                        cleaned = _strip_telegram_meta(content)
                        if cleaned and _is_real_user_message(cleaned):
                            text_parts.append(cleaned)

                    if text_parts:
                        messages.append({
                            "role": role,
                            "text": " ".join(text_parts)[:500],
                            "timestamp": obj.get("timestamp", ""),
                        })
                except Exception:
                    continue
    except Exception as e:
        print(f"[session] _read_jsonl_messages error: {e}")
    return messages[-limit:]


# ── OpenClaw session 定位 ────────────────────────────────

def _get_openclaw_session_key() -> str | None:
    """
    返回最近活跃的 session key。
    优先规则：
      1. 跳过当前 agent 的自身 session（agent:main:main）—— 包含系统操作，非用户对话
      2. 优先找最近活跃的 Telegram session
      3. 否则找最近一个有实质对话的 session
    """
    try:
        if not SESSIONS_FILE.exists():
            return None
        sessions = json.loads(SESSIONS_FILE.read_text())
        if not sessions:
            return None

        # 优先：最近活跃的 Telegram session（任意用户）
        for _key, _meta in sorted(
            sessions.items(),
            key=lambda x: x[1].get("updatedAt", 0), reverse=True
        ):
            if "telegram" in _key.lower():
                return _key

        # 其次：按更新时间倒序，跳过 cron/subagent/当前 session
        for key, meta in sorted(
            sessions.items(),
            key=lambda x: x[1].get("updatedAt", 0),
            reverse=True
        ):
            if any(skip in key for skip in ("cron:", "sub-agent", "agent:main:main")):
                continue
            return key
    except Exception as e:
        print(f"[session] _get_openclaw_session_key error: {e}")
    return None


def _openclaw_key_to_path(session_key: str) -> Path | None:
    """将 OpenClaw session key 转换为 .jsonl 文件路径。"""
    try:
        sessions = json.loads(SESSIONS_FILE.read_text())
        meta = sessions.get(session_key, {})
        session_id = (
            meta.get("sessionId", "")
            or session_key.replace("agent:main:", "").replace(":", "_")
        )
        path = AGENTS_DIR / "main" / "sessions" / f"{session_id}.jsonl"
        return path if path.exists() else None
    except Exception:
        return None


def _openclaw_session_mtime(session_key: str) -> float:
    """返回 OpenClaw session 的最后修改时间（UNIX 时间戳）。"""
    try:
        sessions = json.loads(SESSIONS_FILE.read_text())
        meta = sessions.get(session_key, {})
        # updatedAt 可能是毫秒或秒
        t = meta.get("updatedAt", 0)
        if t > 1e12:
            t /= 1000  # 毫秒 → 秒
        return float(t)
    except Exception:
        return 0.0


# ── Claude Cowork session 定位 ───────────────────────────

def _find_latest_claude_session() -> Path | None:
    """
    在 Claude Cowork 会话目录中找到最近修改的 .jsonl 文件。
    跳过：audit.jsonl、subagents 目录下的文件。
    """
    if CLAUDE_SESSIONS_BASE is None or not CLAUDE_SESSIONS_BASE.exists():
        return None
    try:
        latest: Path | None = None
        latest_mtime = 0.0
        for jsonl in CLAUDE_SESSIONS_BASE.rglob("*.jsonl"):
            if jsonl.name == "audit.jsonl":
                continue
            if "subagents" in jsonl.parts:
                continue
            try:
                mtime = jsonl.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime
                    latest = jsonl
            except Exception:
                continue
        return latest
    except Exception as e:
        print(f"[session] _find_latest_claude_session error: {e}")
    return None


# ── 统一接口 ─────────────────────────────────────────────

def get_current_session_key() -> str | None:
    """
    返回最近活跃 session 的 key。
    - OpenClaw Telegram session:  优先，返回 key 字符串
    - Claude Cowork:             次优先，"claude::<绝对路径>"
    - 其他 OpenClaw session:      最后备选
    优先 Telegram session（通常包含真实对话内容），
    而 Claude Cowork session 更新频繁但多为工具调用记录。
    """
    # 优先：OpenClaw Telegram session
    tg_key = _get_openclaw_session_key()
    if tg_key and "telegram" in tg_key.lower():
        return tg_key

    # Claude Cowork 作为备选（比较 mtime）
    cl_path = _find_latest_claude_session()
    oc_key  = tg_key  # 可能是其他 OpenClaw session
    oc_mtime = _openclaw_session_mtime(oc_key) if oc_key else 0.0
    cl_mtime = cl_path.stat().st_mtime if cl_path else 0.0

    if cl_mtime > oc_mtime and cl_path is not None:
        return f"{_CLAUDE_PREFIX}{cl_path}"
    return oc_key  # 可能为 None


def read_session_messages(session_key: str, limit: int = 100) -> list[dict]:
    """读取 session 消息，自动按来源路由。"""
    if not session_key:
        return []

    if session_key.startswith(_CLAUDE_PREFIX):
        path = Path(session_key[len(_CLAUDE_PREFIX):])
        return _read_jsonl_messages(path, limit)

    # OpenClaw
    try:
        path = _openclaw_key_to_path(session_key)
        if path is None or not path.exists():
            # Telegram/子 session 文件不存在时，降级读主 session agent:main:main
            try:
                sessions_data = json.loads(SESSIONS_FILE.read_text())
                main_meta = sessions_data.get("agent:main:main", {})
                main_sid = main_meta.get("sessionId", "")
                if main_sid:
                    main_path = AGENTS_DIR / "main" / "sessions" / f"{main_sid}.jsonl"
                    if main_path.exists():
                        return _read_jsonl_messages(main_path, limit)
            except Exception:
                pass
            return []
        return _read_jsonl_messages(path, limit)
    except Exception as e:
        print(f"[session] read_session_messages error: {e}")
        return []


# ── 偏好信号识别 ────────────────────────────────────────

PREF_SIGNALS = [
    # 中文
    "我喜欢", "我一般", "我比较", "我通常", "我不喜欢",
    "我想要", "我宁愿", "我偏向", "我倾向于", "我比较喜欢",
    "我比较不", "我从来都", "我从来不会", "我不怎么",
    # 英文
    "i prefer", "i like", "i usually", "i typically", "i tend to",
    "i don't like", "i dislike", "i rather", "i'd rather", "i'm more",
]


def extract_preferences(messages: list[dict]) -> list[str]:
    """
    从用户消息中识别偏好表达。
    返回独立偏好的短句列表，每条不超过 100 字。
    """
    prefs = []
    seen = set()
    for m in messages:
        if m.get("role") != "user":
            continue
        text = m.get("text", "")
        text_lower = text.lower()
        for signal in PREF_SIGNALS:
            if signal.lower() in text_lower:
                # 提取包含该信号的那句话
                idx = text_lower.find(signal.lower())
                # 向前向后扩展，取完整句子（简单截断）
                start = max(0, idx - 10)
                end = min(len(text), idx + 80)
                snippet = text[start:end].strip()
                if len(snippet) < 10:
                    continue
                key = snippet[:60]  # 去重用前60字
                if key not in seen:
                    seen.add(key)
                    prefs.append(snippet)
    return prefs[:5]  # 最多5条


def _generate_paragraph_summary(messages: list[dict]) -> str:
    """
    把最近一段对话（用户+AI）合并成连贯的段落描述。
    格式："用户问了X，AI回答了Y，用户进一步讨论了Z..."
    """
    if not messages:
        return "当前 session 无对话内容"

    # 取最近 20 条，优先保留有实质内容的
    recent = messages[-20:]
    lines = []
    for m in recent:
        role = m.get("role", "")
        text = m.get("text", "")
        if not text or len(text) < 5:
            continue
        if role == "user":
            # 截断超长消息
            if len(text) > 150:
                text = text[:150] + "..."
            lines.append(f"用户：{text}")
        elif role == "assistant":
            # AI 回复取前100字摘要
            summary = text[:100] + "..." if len(text) > 100 else text
            lines.append(f"Two：{summary}")

    if not lines:
        return "当前 session 无实质对话内容"

    # 合并成段落
    paragraph = " | ".join(lines)
    if len(paragraph) > 500:
        paragraph = paragraph[:500] + "..."
    return paragraph


def build_session_summary(session_key: str) -> dict:
    """
    构建 session 摘要（对 amber_hunter.py 保持同一接口）。

    v0.8.8 改动：
    - 读最近 20 条消息（不只是最后一条）
    - 生成段落级摘要（连贯描述，不是单句）
    - 识别并提取用户偏好表达
    """
    messages = read_session_messages(session_key, limit=20)
    if not messages:
        return {"session_key": session_key, "summary": "", "messages": [], "preferences": []}

    # 段落级摘要
    paragraph = _generate_paragraph_summary(messages)

    # 提取偏好
    preferences = extract_preferences(messages)

    # 最后一条有实质内容的用户消息（保留，展示用）
    user_msgs = [m["text"] for m in messages if m.get("role") == "user" and len(m.get("text", "")) > 10]
    last_topic = user_msgs[-1] if user_msgs else ""

    source = "Claude Cowork" if session_key.startswith(_CLAUDE_PREFIX) else "OpenClaw"

    return {
        "session_key": session_key,
        "source": source,
        "summary": paragraph,
        "last_topic": last_topic[:200] if last_topic else "",
        "preferences": preferences,
        "message_count": len(messages),
        "recent_messages": messages[-6:],
    }


# ── 工作区文件（不变）────────────────────────────────────

def get_recent_files(limit: int = 10) -> list[dict]:
    """返回 workspace 最近修改的文件。"""
    try:
        files = []
        if not WORKSPACE_DIR.exists():
            return []
        all_files = [
            f for f in WORKSPACE_DIR.rglob("*")
            if f.is_file() and not f.name.startswith(".")
        ]
        for f in sorted(all_files, key=lambda x: -x.stat().st_mtime)[:limit]:
            try:
                files.append({
                    "path": str(f.relative_to(HOME)),
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                })
            except Exception:
                continue
        return files
    except Exception as e:
        print(f"[session] get_recent_files error: {e}")
        return []
