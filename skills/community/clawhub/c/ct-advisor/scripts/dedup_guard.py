#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 同 origin 近似去重 + 本地答案缓存短路（改进 B，2026-09-23）

背景（来自 Ct-Advisor_连续提问诊断报告）：
  - 飞书后台：5/17 条连续提问是「逐字完全相同」的重复提交（用户 A 的 1176=1177=1178、
    用户 C 的 1170=1171）。虽然 Coze 服务端已有缓存四闸（跨请求命中已验证），
    但本地每次仍把整篇问题（含 32k 文档）重贴、重发云端 → 本地预处理与网络传输的浪费依旧。
  - 本模块在**本地**按 query_origin 记录近期问题与答案：下次同 origin 提交近似相同问题时，
    直接复用上次答案（本地短路），不再重发云端、不再重跑。命中后由 refine_answer.py 提示用户。

设计要点：
  - 只在「串行（complex/vague）路径」启用短路（forward_guards 控制），fire_only/collect
    路径保持零本地检索（遵守 race 硬闸门，绝不先本地检索再发 Coze）。
  - 相似度用 difflib.SequenceMatcher.quick_ratio()（O(n)、不建全矩阵），>= SIM_THRESHOLD 判重。
  - 仅当「存过答案」且「近期（WINDOW 秒内）」才短路，过期记录随写入滚动清理。
  - 任何异常一律回退为「不短路 / 不记录」（绝不阻断主流程）。

⚠️ 2026-10-30 总开关关闭（用户定形）：
  本模块复用「旧答案」本质是本地答案缓存，且 key 不含对话历史 → 追问可能命中
  首轮答案。与 session_store.global_cache / answer_cache 统一受
  `CT_ADVISOR_LOCAL_CACHE` 控制，**默认关闭**：`check()` 恒未命中、`record()` 空操作。
  恢复：设环境变量 `CT_ADVISOR_LOCAL_CACHE=1`。

依赖：stdlib-only（json / os / time / difflib）。
"""

import difflib
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 本地答案缓存总开关（2026-10-30，与 session_store.LOCAL_CACHE_ENABLED 同口径、同环境变量）。
LOCAL_CACHE_ENABLED = os.environ.get(
    "CT_ADVISOR_LOCAL_CACHE", "0").strip().lower() in ("1", "true", "yes", "on")

SIM_THRESHOLD = 0.90      # 近似相似度阈值（quick_ratio）
WINDOW = 1800             # 近期窗口（秒，30 分钟）
MAX_PER_ORIGIN = 20       # 每 origin 最多保留条数（滚动）


def _store_path() -> str:
    """去重库文件路径。

    CT_ADVISOR_DATA_ROOT 视为「数据根目录」（与 doc_memory 语义一致），文件名固定拼接；
    未设置时用技能自身的 config/dedup_store.json（生产路径）。
    """
    root = os.environ.get("CT_ADVISOR_DATA_ROOT")
    if root:
        return os.path.join(root, "dedup_store.json")
    return os.path.join(ROOT, "config", "dedup_store.json")


def _load() -> dict:
    try:
        with open(_store_path(), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _ensure_dir(d: str) -> None:
    """创建目录；忽略「已存在 / 权限」类异常（Windows 对部分临时目录的已知怪象）。"""
    if not d:
        return
    try:
        os.makedirs(d, exist_ok=True)
    except (FileExistsError, PermissionError, OSError):
        pass


def _save(store: dict) -> None:
    _ensure_dir(os.path.dirname(_store_path()))
    with open(_store_path(), "w", encoding="utf-8") as fh:
        json.dump(store, fh, ensure_ascii=False, indent=2)


def _similar(a: str, b: str) -> float:
    """近似相似度（0~1）。空串直接 0；长度悬殊过大直接 0（避免长文 vs 短文误判）。"""
    a, b = (a or "").strip(), (b or "").strip()
    if not a or not b:
        return 0.0
    if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.5:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).quick_ratio()


def check(query_origin: str, question: str) -> tuple:
    """检查是否近期重复提交。

    返回 (is_dup, prev_answer, minutes_ago)：
      - is_dup=True 且 prev_answer 非空 → 调用方应本地短路复用 prev_answer；
      - 任何异常 → (False, None, 0)。
    """
    if not LOCAL_CACHE_ENABLED:
        return False, None, 0
    try:
        origin = (query_origin or "").strip()
        if not origin:
            return False, None, 0
        store = _load()
        entries = store.get(origin) or []
        now = time.time()
        best = None
        best_sim = 0.0
        for e in entries:
            ts = e.get("ts") or 0
            if now - ts > WINDOW:
                continue
            sim = _similar(question or "", e.get("q") or "")
            if sim >= SIM_THRESHOLD and sim > best_sim:
                best_sim = sim
                best = e
        if best and (best.get("answer") or "").strip():
            mins = max(0, int((now - (best.get("ts") or now)) / 60))
            return True, best["answer"], mins
        return False, None, 0
    except Exception:  # noqa: BLE001
        return False, None, 0


def record(query_origin: str, question: str, answer: str) -> None:
    """记录一次「问题→答案」，供后续去重短路。开关关闭 / 异常静默忽略。"""
    if not LOCAL_CACHE_ENABLED:
        return
    try:
        origin = (query_origin or "").strip()
        if not origin or not (answer or "").strip():
            return
        store = _load()
        entries = store.get(origin) or []
        entries.append({
            "ts": time.time(),
            "q": (question or "").strip(),
            "answer": (answer or "").strip(),
        })
        # 滚动裁剪：仅保留最近 MAX_PER_ORIGIN 条，并丢弃窗口外旧条
        now = time.time()
        entries = [e for e in entries if now - (e.get("ts") or 0) <= WINDOW]
        entries = entries[-MAX_PER_ORIGIN:]
        store[origin] = entries
        _save(store)
    except Exception:  # noqa: BLE001
        pass


if __name__ == "__main__":
    # 自测
    import tempfile, os as _os
    _os.environ["CT_ADVISOR_DATA_ROOT"] = tempfile.mkdtemp()
    record("sha256:test", "请问主要终点该怎么设", "答：设为 ORR。")
    print(check("sha256:test", "请问主要终点该怎么设"))          # 应命中
    print(check("sha256:test", "样本量怎么算"))                    # 应不命中
