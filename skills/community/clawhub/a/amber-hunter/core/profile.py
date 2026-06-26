"""
core/profile.py — Structured User Profile Extraction v1.2.27 P1-1
WHO_I_AM / STACK / GOALS / PREFERENCES 四段画像
"""
from __future__ import annotations

import time

# ── Signal patterns ────────────────────────────────────────
_STACK_SIGNALS = [
    "我常用", "我主要用", "技术栈", "tech stack", "技术选型",
    "用 Python", "用 Rust", "用 Go", "基于", "开发环境",
    "开发语言", "框架", "数据库", "我写", "我最近在用",
]
_GOALS_SIGNALS = [
    "我的目标", "我想做", "我打算", "我正在学", "我的计划",
    "my goal", "i'm learning", "i want to build", "i'm working on",
    "打算用", "准备学", "想做一个", "下一步是",
]
_WHO_SIGNALS = [
    "我是", "我的背景", "我之前", "我来自", "我住在",
    "i'm a", "my background", "i work as", "i'm based in",
    "全栈", "工程师", "设计师", "产品", "独立开发",
]


def _detect_profile_signal(text: str) -> str:
    """检测文本属于哪个 profile section，默认返回 PREFERENCES"""
    t = text.lower()
    for kw in _GOALS_SIGNALS:
        if kw.lower() in t:
            return "GOALS"
    for kw in _STACK_SIGNALS:
        if kw.lower() in t:
            return "STACK"
    for kw in _WHO_SIGNALS:
        if kw.lower() in t:
            return "WHO_I_AM"
    return "PREFERENCES"


def build_or_update_profile(session_key: str) -> dict:
    """
    从当前 session 的 WAL 条目和偏好信号构建 profile。
    LLM 生成四段结构化内容并持久化到 DB。
    """
    from core.wal import read_wal_entries
    from core.session import read_session_messages, extract_preferences
    from core.db import get_profile, update_profile, insert_profile

    # 收集 WAL 条目文本
    entries = read_wal_entries(session_key, processed=False)
    texts = [e.get("data", {}).get("text", "") for e in entries if e.get("data", {}).get("text")]

    # 收集 session 偏好信号
    session_msgs = read_session_messages(session_key, limit=30)
    prefs = extract_preferences(session_msgs)
    all_texts = texts + prefs

    if not all_texts:
        return {}

    combined = "\n".join(f"- {t}" for t in all_texts[:30])
    if not combined.strip():
        return {}

    try:
        from core.llm import get_llm
        llm = get_llm()
        prompt = f"""基于以下用户表达，生成或更新结构化画像：

{combined}

输出纯 JSON（无其他内容）：
{{
  "WHO_I_AM": "你是谁（一句话）",
  "STACK": "技术栈（用/分隔）",
  "GOALS": "目标（1-2句）",
  "PREFERENCES": "偏好习惯（要点列表）"
}}"""
        profile_data = llm.complete_json(prompt)
    except Exception as e:
        import sys
        print(f"[profile] LLM extraction failed: {e}", file=sys.stderr)
        return {}

    valid_sections = {"WHO_I_AM", "STACK", "GOALS", "PREFERENCES"}
    for section, content in profile_data.items():
        if section not in valid_sections:
            continue
        if not content:
            continue
        existing = get_profile(section)
        if existing:
            update_profile(section, content, source="llm_extracted", session_id=session_key)
        else:
            insert_profile(section, content, source="llm_extracted", session_id=session_key)

    # 处理完 WAL 条目后标记为已处理（避免下次重复读取）
    from core.wal import mark_wal_processed
    for e in entries:
        mark_wal_processed(e.get("ts", 0))

    return profile_data


def get_full_profile() -> dict:
    """返回所有 profile sections 作为 dict"""
    from core.db import list_profile
    return list_profile()
