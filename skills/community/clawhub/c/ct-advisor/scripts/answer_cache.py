#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-advisor — 主链路本地答案缓存（2026-10-16）

背景（来自 log.docx 性能诊断）：
  entry.py 的主链路是
      entry.py → orchestrate.run_orchestrate → adapters.refiner.refine_forward → Coze
  这条链路上**没有任何 forward_guards / dedup_guard 调用**（守卫只在
  refine_answer.py 的命令行 main 里生效），因此 SKILL.md 承诺的
  「重跑命中本地 dedup 短路、不再打 Coze」在 entry.py 路径上从未成立。
  agent 一旦因 base64 校验失败或误判而重跑 entry.py，就是一次真实的 Coze 往返。

本模块给主链路补一层「按问题指纹」的精确缓存：
    key = sha256(original_question | doc_context | difficulty)
    TTL = 1800s（可用环境变量 CT_ADVISOR_ANSWER_TTL 覆盖）
命中 → 直接复用上次答案，0 次 Coze 调用。

设计要点：
  - 与 dedup_guard 不同，不依赖 query_origin（entry.py 从不设置该字段），
    改用问题指纹本身做 key，对「重跑同一问题」这一真实场景精确命中。
  - 任何异常一律静默回退为「不命中 / 不写入」，绝不阻断主流程。
  - 只缓存「纯答案」形态；委托块（<<<CT_TOOL_DELEGATE>>>）由调用方排除。

⚠️ 2026-10-30 总开关关闭（用户定形）：
  本模块的 key **不含对话历史**，因此「同一问题的首轮与追问」会共享同一条答案 ——
  这正是用户明确禁止的行为（缓存只应在**云端**、且**只服务首轮独立问题**）。
  现与其他本地缓存（session_store.global_cache / dedup_guard）统一受
  `CT_ADVISOR_LOCAL_CACHE` 控制，**默认关闭**：`get()` 恒返回空串、`put()` 空操作。
  关闭后「重跑同一问题」不再本地短路，改由云端缓存处理（跨用户命中更有价值）。
  恢复：设环境变量 `CT_ADVISOR_LOCAL_CACHE=1`。

依赖：stdlib-only（hashlib / json / os / time / pathlib）。
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 本地答案缓存总开关（2026-10-30，与 session_store.LOCAL_CACHE_ENABLED 同口径、同环境变量）。
# 默认关闭：答案缓存权收归云端 Coze，避免「云端已升级 / 已修正，客户端仍回旧答案」，
# 更避免「本地无历史 key 的缓存把首轮答案喂给追问」。
LOCAL_CACHE_ENABLED = os.environ.get(
    "CT_ADVISOR_LOCAL_CACHE", "0").strip().lower() in ("1", "true", "yes", "on")

# 与 dedup_guard.WINDOW 保持同口径（30 分钟）
TTL = int(os.environ.get("CT_ADVISOR_ANSWER_TTL", "1800"))


def _dir() -> Path:
    """缓存目录：CT_ADVISOR_DATA_ROOT 视为数据根目录（与 dedup_guard 语义一致）。"""
    root = os.environ.get("CT_ADVISOR_DATA_ROOT")
    base = Path(root) if root else (ROOT / "config")
    d = base / "answer_cache"
    try:
        d.mkdir(parents=True, exist_ok=True)
    except Exception:  # noqa: BLE001
        pass
    return d


def key_of(question: str, doc_context: str = "", difficulty: str = "") -> str:
    """问题指纹。同问题 + 同附件载荷 + 同难度 → 同 key。"""
    raw = f"{(question or '').strip()}|{doc_context or ''}|{difficulty or ''}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def get(key: str) -> str:
    """命中则返回缓存答案；未命中 / 过期 / 开关关闭 / 任何异常 → 空串。"""
    if not LOCAL_CACHE_ENABLED:
        return ""
    if not key:
        return ""
    try:
        f = _dir() / f"{key}.json"
        if not f.exists():
            return ""
        obj = json.loads(f.read_text(encoding="utf-8"))
        if time.time() - float(obj.get("ts") or 0) > TTL:
            return ""
        return obj.get("answer") or ""
    except Exception:  # noqa: BLE001
        return ""


def put(key: str, answer: str) -> None:
    """写入一次「问题指纹 → 答案」。开关关闭 / 空值 / 异常静默忽略。"""
    if not LOCAL_CACHE_ENABLED:
        return
    if not key or not (answer or "").strip():
        return
    try:
        (_dir() / f"{key}.json").write_text(
            json.dumps({"ts": time.time(), "answer": answer}, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:  # noqa: BLE001
        pass
    # 低频清理（约每 20 次写入触发一次）：get() 对过期条目只是返回空串，文件本身
    # 不会自动消失；不清理会随使用无限累积。异常静默，绝不影响主流程。
    try:
        if random.random() < 0.05:
            purge()
    except Exception:  # noqa: BLE001
        pass


def purge() -> int:
    """清理过期条目，返回删除数量（维护用，异常静默）。"""
    n = 0
    try:
        now = time.time()
        for f in _dir().glob("*.json"):
            try:
                obj = json.loads(f.read_text(encoding="utf-8"))
                if now - float(obj.get("ts") or 0) > TTL:
                    f.unlink()
                    n += 1
            except Exception:  # noqa: BLE001
                continue
    except Exception:  # noqa: BLE001
        pass
    return n


if __name__ == "__main__":
    # 离线自测：不联网、不触碰生产缓存目录
    import tempfile

    os.environ["CT_ADVISOR_DATA_ROOT"] = tempfile.mkdtemp()
    q1 = "多中心研究中如果一个中心突然要退出怎么处理"
    q2 = "样本量怎么估算"
    k1 = key_of(q1)
    k2 = key_of(q2)

    # 默认关闭态断言（2026-10-30）：get 恒空、put 不落盘
    LOCAL_CACHE_ENABLED = False
    put(k1, "关闭态答案")
    print("关闭态 get 恒空:", get(k1) == "")
    print("关闭态 put 不落盘:", not (_dir() / f"{k1}.json").exists())

    # 强制开启后再验读写语义
    LOCAL_CACHE_ENABLED = True
    print("key 稳定:", k1 == key_of(q1))
    print("不同问题 key 不同:", k1 != k2)
    print("初始未命中:", get(k1) == "")

    put(k1, "答案甲")
    print("写入后命中:", get(k1) == "答案甲")
    print("另一问题不误命中:", get(k2) == "")

    # 附件载荷不同 → key 不同（避免带不同文档时误复用）
    print("doc_context 参与 key:", key_of(q1, "DOC-A") != key_of(q1, "DOC-B"))
    print("purge:", purge())
