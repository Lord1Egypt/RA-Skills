"""
core/extractor.py — Mem0-Style Auto-Extraction v1.2.28 P2-1
从对话自动抽取 facts/preferences/decisions，无需显式信号词
"""
from __future__ import annotations

import secrets, time
from typing import Optional

# ── Extraction patterns ────────────────────────────────────
PREF_PATTERNS = [
    "我比较喜欢", "我倾向于", "我宁可", "i prefer", "i tend to",
    "我一般会", "我通常", "我不太", "我从来", "我偏向",
]
DECISION_PATTERNS = [
    "决定用", "就选", "采用了", "选了", "decided on", "going with",
    "最后决定", "最终方案是", "最终决定",
]
FACT_PATTERNS = [
    "我叫", "我在", "我是做", "我的公司", "我住在",
    "我目前", "currently working on", "i'm building", "i'm developing",
]


def _quick_filter(text: str) -> list[str]:
    """快速过滤：返回可能的抽取类型列表"""
    types = []
    t = text.lower()
    for p in PREF_PATTERNS:
        if p.lower() in t:
            types.append("preference")
            break
    for p in DECISION_PATTERNS:
        if p.lower() in t:
            types.append("decision")
            break
    for p in FACT_PATTERNS:
        if p.lower() in t:
            types.append("personal_fact")
            break
    return types


def extract_memories_from_messages(messages: list[dict], session_id: str) -> list[dict]:
    """
    给定 session 消息列表，返回待入库的抽取结果。
    返回: [{"type": str, "memo": str, "context": str, "confidence": float, "source": str}, ...]
    """
    from core.wal import read_wal_entries
    from core.session import extract_preferences

    candidates: list[dict] = []
    seen_memos: set[str] = set()

    # 1. WAL 信号条目 → 直接抽取
    try:
        wal_entries = read_wal_entries(session_id, processed=False)
        for e in wal_entries:
            text = e.get("data", {}).get("text", "")
            if not text:
                continue
            sig_type = e.get("type", "")
            if sig_type in ("preference", "decision", "correction"):
                memo = text[:200]
                key = memo[:80].lower()
                if key not in seen_memos:
                    seen_memos.add(key)
                    confidence = 0.85 if sig_type in ("preference", "decision") else 0.7
                    candidates.append({
                        "type": sig_type,
                        "memo": memo,
                        "context": "",
                        "confidence": confidence,
                        "source": "wal_signal",
                    })
    except Exception:
        pass

    # 2. 偏好信号（extract_preferences）
    try:
        prefs = extract_preferences(messages)
        for p in prefs:
            key = p[:80].lower()
            if key not in seen_memos:
                seen_memos.add(key)
                candidates.append({
                    "type": "preference",
                    "memo": p[:200],
                    "context": "",
                    "confidence": 0.75,
                    "source": "pref_signal",
                })
    except Exception:
        pass

    # 3. LLM 结构化抽取（补充规则漏掉的）
    user_texts = [
        m["text"] for m in messages
        if m.get("role") == "user" and len(m.get("text", "")) > 20
    ]
    if user_texts:
        combined = "\n".join(f"- {t}" for t in user_texts[-15:])
        try:
            from core.llm import get_llm
            llm = get_llm()
            prompt = f"""从以下用户对话中抽取结构化记忆。每条包含：type / memo / context / confidence。

可用 type：personal_fact / preference / decision / context / learning

对话：
{combined[:2000]}

输出纯 JSON 数组（最多 5 条，无匹配则返回 []）：
[
  {{"type": "...", "memo": "...", "context": "...", "confidence": 0.8}},
  ...
]"""
            result = llm.complete_json(prompt)
            if isinstance(result, list):
                for item in result:
                    t = item.get("type", "")
                    memo = item.get("memo", "")
                    if not memo or not t:
                        continue
                    key = memo[:80].lower()
                    if key not in seen_memos:
                        seen_memos.add(key)
                        try:
                            conf = float(item.get("confidence", 0.5))
                        except (TypeError, ValueError):
                            conf = 0.5
                        candidates.append({
                            "type": t,
                            "memo": memo[:200],
                            "context": (item.get("context") or "")[:200],
                            "confidence": max(0.0, min(1.0, conf)),
                            "source": "llm_extraction",
                        })
        except Exception:
            pass

    return candidates[:10]


def auto_extract(session_key: str | None = None) -> dict:
    """
    自动抽取入口：读取 session 消息 → extract_memories_from_messages → 入库/进队列
    """
    from core.session import read_session_messages, get_current_session_key
    from core.db import insert_capsule, queue_insert, set_config
    from core.vector import index_capsule
    # v1.2.39: contradiction check
    from core.contradiction import check_contradiction_on_ingest

    sk = session_key or get_current_session_key()
    if not sk:
        return {"status": "no_session", "extracted": 0}

    messages = read_session_messages(sk, limit=50)
    if len(messages) < 2:
        return {"status": "too_few_messages", "extracted": 0}

    candidates = extract_memories_from_messages(messages, sk)
    stored = 0
    contradiction_warnings = []

    for c in candidates:
        cap_id = secrets.token_hex(8)
        now = time.time()
        memo = (c["memo"] or "").strip()
        if not memo:
            continue  # 跳过空白内容，防止重复空胶囊

        # v1.2.39: 时间解析 + 矛盾检测
        try:
            from amber_hunter import _infer_category_path
            cap_path = _infer_category_path(memo, c.get("context", ""), c["type"])
        except Exception:
            cap_path = "general/default"

        valid_from, valid_to, warnings = check_contradiction_on_ingest(memo, cap_path)
        contradiction_warnings.extend(warnings)

        if c["confidence"] >= 0.9:
            # 高置信 → 直接入库
            try:
                insert_capsule(
                    capsule_id=cap_id,
                    memo=memo,
                    content=c.get("context", ""),
                    tags=c["type"],
                    session_id=sk,
                    window_title=None,
                    url=None,
                    created_at=now,
                    source_type="auto_extract",
                    category="",
                    category_path=cap_path,
                    valid_from=valid_from,
                    valid_to=valid_to,
                )
                try:
                    index_capsule(cap_id, c["memo"], now)
                except Exception:
                    pass
                stored += 1
            except Exception:
                pass
        elif c["confidence"] >= 0.5:
            # 中置信 → 进审核队列
            try:
                queue_insert(
                    memo=c["memo"],
                    context=c.get("context", ""),
                    category=c["type"],
                    tags="auto_extract",
                    source="mem0_auto",
                    confidence=c["confidence"],
                )
                stored += 1
            except Exception:
                pass

    # 记录统计
    try:
        last_count = int((set_config("auto_extract_count", "0") or "0"))
        set_config("auto_extract_count", str(last_count + stored))
        set_config("auto_extract_last", str(time.time()))
    except Exception:
        pass

    return {"status": "ok", "extracted": stored, "session_key": sk,
            "contradictions": contradiction_warnings}
