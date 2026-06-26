from __future__ import annotations

import re
from sqlite3 import Connection


READ_PHRASES = [
    "上次",
    "之前",
    "还记得",
    "你答应我",
    "我说过",
    "我们聊过",
    "你知道我喜欢吃什么吗",
    "你记得我叫什么吗",
]

READ_STATE_PATTERNS = [
    r"喜欢吃什么",
    r"怎么叫我",
    r"记得我叫什么",
    r"我的昵称",
    r"我的偏好",
    r"我们现在是什么关系",
    r"那个长期项目",
]

WRITE_STABLE_PATTERNS = [
    r"以后(?:都)?(?:请|就)?叫我(?P<value>[\u4e00-\u9fffA-Za-z0-9_-]{1,20})",
    r"你可以叫我(?P<value>[\u4e00-\u9fffA-Za-z0-9_-]{1,20})",
    r"我更喜欢你叫我(?P<value>[\u4e00-\u9fffA-Za-z0-9_-]{1,20})",
    r"我喜欢(?P<value>[^，。！？\n]{1,30})",
    r"我不喜欢(?P<value>[^，。！？\n]{1,30})",
]

BOUNDARY_PATTERNS = [
    r"不要(?P<value>[^，。！？\n]{1,40})",
    r"别(?P<value>[^，。！？\n]{1,40})",
    r"请不要(?P<value>[^，。！？\n]{1,40})",
]

PROMISE_PATTERNS = [
    r"以后",
    r"下次",
    r"答应我",
    r"约好了",
    r"记得提醒我",
]

EVENT_PATTERNS = [
    r"今天发生了",
    r"刚刚发生了",
    r"我们一起",
    r"那件事",
    r"重要的事",
]

RELATIONSHIP_PATTERNS = [
    r"我信任你",
    r"我更依赖你了",
    r"我们更亲近了",
    r"我讨厌你",
    r"我不想理你",
]

EMOTION_PATTERNS = [
    r"我很难过",
    r"我很开心",
    r"我很生气",
    r"我很崩溃",
    r"我真的受不了",
]

SMALL_TALK_PATTERNS = [
    r"今天天气不错",
    r"我有点困",
    r"吃了吗",
    r"早上好",
    r"晚安",
]


def contains_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def detect_read_reasons(text: str, relationship_exists: bool) -> list[str]:
    reasons: list[str] = []
    if contains_any(text, READ_PHRASES):
        reasons.append("explicit_memory_reference")
    if any(re.search(pattern, text) for pattern in READ_STATE_PATTERNS):
        reasons.append("long_term_state_dependency")
    if relationship_exists and re.search(r"(关系|信任|昵称|偏好)", text):
        reasons.append("relationship_state_dependency")
    return list(dict.fromkeys(reasons))


def detect_write_reasons(text: str) -> list[str]:
    if any(re.search(pattern, text) for pattern in SMALL_TALK_PATTERNS):
        return []

    reasons: list[str] = []
    if any(re.search(pattern, text) for pattern in WRITE_STABLE_PATTERNS):
        reasons.append("stable_preference_or_nickname")
    if any(re.search(pattern, text) for pattern in BOUNDARY_PATTERNS):
        reasons.append("explicit_boundary")
    if any(re.search(pattern, text) for pattern in PROMISE_PATTERNS):
        reasons.append("future_promise_or_todo")
    if any(re.search(pattern, text) for pattern in EVENT_PATTERNS):
        reasons.append("important_shared_event")
    if any(re.search(pattern, text) for pattern in RELATIONSHIP_PATTERNS):
        reasons.append("relationship_state_change")
    if any(re.search(pattern, text) for pattern in EMOTION_PATTERNS):
        reasons.append("strong_emotion_change")
    return list(dict.fromkeys(reasons))


def fetch_memory_payload(
    connection: Connection,
    character_slug: str,
    user_id: str,
    *,
    profile_limit: int = 8,
    episodic_limit: int = 5,
    summary_limit: int = 3,
) -> dict:
    relationship_row = connection.execute(
        """
        SELECT relationship_label, trust_level, closeness_level, status_summary, updated_at
        FROM relationship_state
        WHERE character_slug = ? AND user_id = ?
        """,
        (character_slug, user_id),
    ).fetchone()
    profile_rows = connection.execute(
        """
        SELECT memory_key, memory_value, confidence, source, updated_at
        FROM profile_memory
        WHERE character_slug = ? AND user_id = ?
        ORDER BY updated_at DESC
        LIMIT ?
        """,
        (character_slug, user_id, profile_limit),
    ).fetchall()
    episodic_rows = connection.execute(
        """
        SELECT id, summary, event_type, emotional_intensity, source_excerpt, created_at
        FROM episodic_memory
        WHERE character_slug = ? AND user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (character_slug, user_id, episodic_limit),
    ).fetchall()
    summary_rows = connection.execute(
        """
        SELECT id, turn_start, turn_end, summary, created_at
        FROM conversation_summary
        WHERE character_slug = ? AND user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (character_slug, user_id, summary_limit),
    ).fetchall()
    return {
        "has_memory": bool(relationship_row or profile_rows or episodic_rows or summary_rows),
        "relationship_state": dict(relationship_row) if relationship_row else None,
        "profile_memory": [dict(row) for row in profile_rows],
        "episodic_memory": [dict(row) for row in episodic_rows],
        "conversation_summary": [dict(row) for row in summary_rows],
    }
