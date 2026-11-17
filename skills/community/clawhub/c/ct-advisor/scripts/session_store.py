#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 统一会话存储（会话上下文 + 答案缓存 + 幂等去重），2026-10-22

背景（来自 advisorlog 近 30 天诊断）：
  - 会话上下文曾从未被主链路注入：context_stitch.pack_history_for_coze() 虽存在，
    但 entry.py / proxy 两条真实入口都没调用它 → Coze 永远只拿到单轮问题，
    用户被迫在「承接上一轮 / 继续调研」里手工复述背景（实测 18% 提问含此类回指）。
  - answer_cache / dedup_guard 只在 refine_answer.py 的 CLI 路径生效，entry.py 与
    workbench proxy 直连 Coze 时完全绕开 → 21% 的重复发送（11 个簇）白烧云端耗时。

本模块把三类能力按 session_id 聚合到**同一存储**，entry.py 与 proxy 共用，确保跨入口一致：
  1) history      多轮问答（conversation_history），注入 payload 供 Coze 判相关性
  2) global_cache 问题指纹 → 答案（跨 session 通用，同问题同答案）
  3) dedup        同 session 近窗近似重复（difflib quick_ratio），命中直回上轮答案

存储：{ROOT}/config/session_store.json（单文件，按 session_id 分组 + 顶层 global_cache）。
并发：跨进程用文件锁（Win msvcrt / POSIX fcntl），临界区短；锁失败静默降级（不阻断主流程）。
一切异常静默回退为「不命中 / 不记录」——永不阻断主流程（与 answer_cache / dedup_guard 约定一致）。

依赖：stdlib-only（hashlib / json / os / time / difflib / pathlib）。
"""

from __future__ import annotations

import contextlib
import difflib
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 2026-10-30（部署布局缺陷修复）：数据根目录可被环境变量覆盖。
# 背景：workbench/publish/ 是**扁平拷贝**（不含 scripts/），随工作台发布上云后
#   技能根目录不存在 → 内嵌副本的 `parent.parent` 会指向不可写/无意义的位置。
#   此时由代理设置 CT_ADVISOR_DATA_ROOT=应用根目录，使落盘位置稳定可写。
# 本地开发（scripts/ 真源在位）不设该变量 → 行为与修复前完全一致。
_ENV_DATA_ROOT = os.environ.get("CT_ADVISOR_DATA_ROOT", "").strip()
if _ENV_DATA_ROOT:
    try:
        ROOT = Path(_ENV_DATA_ROOT).expanduser().resolve()
    except Exception:  # noqa: BLE001
        pass
STORE_PATH = ROOT / "config" / "session_store.json"
LOCK_PATH = ROOT / "config" / ".session_store.lock"

# ── 上下文裁剪口径（对齐 context_stitch 模式 B：OR + 24h 硬上限）─────────────
HIST_TTL_ROUNDS = 10       # 有效轮数（OR：≤10 条即保留）
HIST_TTL_SECONDS = 7200    # 软时间窗 2h（OR：2h 内全留）
HIST_HARD_CAP = 86400      # 硬上限 24h（任何超 24h 必丢）
HIST_MAX_PREV_LEN = 200    # 单条 answer_summary 上限（防膨胀）

# ── 答案缓存 ────────────────────────────────────────────────────────────────
CACHE_TTL = int(os.environ.get("CT_ADVISOR_ANSWER_TTL", "1800"))  # 默认 30 分钟

# 2026-10-30（缓存键分区，P0）：
#   缓存价值来自**跨用户命中**（不同用户提同一问题直接复用），所以缓存必须在服务端，
#   不能放客户端（客户端缓存只在单浏览器内有效，跨用户零收益）。
#   但这与「连续对话」存在结构性张力：
#     - 跨用户复用要求键**只含问题**，否则每个用户历史不同 → 永不命中；
#     - 上下文正确性要求键**含历史**，否则追问会命中别处的答案。
#   解法：按「是否携带上下文」分区。
#     · 历史为空（首轮独立问题，跨用户重复度最高）→ 键含 hk="h0"，**写**全局缓存，跨用户复用；
#     · 历史非空（追问句如「那这个怎么办」，跨用户不可能重复）→ 键含真实历史指纹，
#       只写本会话 dedup（防重复计费），**不写**全局缓存，避免污染跨用户缓存。
# CACHE_VERSION：云端 bot 升级后旧答案整体失效，避免用户吃到上一版答案（曾误判成「升级没生效」）。
CACHE_VERSION = os.environ.get("CT_ADVISOR_CACHE_VER", "bot1.48")
CACHE_HK_EMPTY = "h0"          # 无上下文分区标识（全局可复用）

# 2026-10-30（用户要求 · 彻底关闭客户端缓存，避免与云端冲突）：
#   关掉的是「答案复用」的两条路径——
#     · global_cache（精确指纹，跨用户复用）
#     · dedup（会话内近似去重）
#   目的：消除「云端已升级 / 已修正，客户端仍回旧答案」这一类冲突，答案一律以云端为准。
#   **不关** history（多轮上下文注入不是缓存，属上下文正确性的一部分，必须保留）。
#   恢复：设环境变量 CT_ADVISOR_LOCAL_CACHE=1。
#   改动本文件必须同步 workbench/session_store.py 与 workbench/publish/session_store.py。
LOCAL_CACHE_ENABLED = os.environ.get(
    "CT_ADVISOR_LOCAL_CACHE", "0").strip().lower() in ("1", "true", "yes", "on")

# ── 幂等去重（近窗近似重复）─────────────────────────────────────────────────
DEDUP_WINDOW = 600         # 10 分钟（覆盖实测重发间隔 12~232s）
DEDUP_SIM = 0.90           # 近似相似度阈值（quick_ratio）
DEDUP_MAX_PER_SESSION = 20 # 每 session 保留条数（滚动）


# ── 跨平台文件锁 ──────────────────────────────────────────────────────────────
def _lock_ctx():
    """返回上下文管理器：进入临界区前获取文件锁，退出释放。失败静默降级。"""
    if sys.platform.startswith("win"):
        import msvcrt

        @contextlib.contextmanager
        def _cm():
            fh = None
            try:
                fh = open(LOCK_PATH, "a+")
                msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)
                yield
            except Exception:  # noqa: BLE001
                yield
            finally:
                try:
                    if fh is not None:
                        fh.seek(0)
                        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
                        fh.close()
                except Exception:  # noqa: BLE001
                    pass
        return _cm()
    else:
        import fcntl

        @contextlib.contextmanager
        def _cm():
            fh = None
            try:
                fh = open(LOCK_PATH, "a+")
                fcntl.flock(fh, fcntl.LOCK_EX)
                yield
            except Exception:  # noqa: BLE001
                yield
            finally:
                try:
                    if fh is not None:
                        fcntl.flock(fh, fcntl.LOCK_UN)
                        fh.close()
                except Exception:  # noqa: BLE001
                    pass
        return _cm()


def _load() -> dict:
    try:
        with open(STORE_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _save(data: dict) -> None:
    try:
        STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = STORE_PATH.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, STORE_PATH)  # 原子替换，避免半写损坏
    except Exception:  # noqa: BLE001
        pass


# ── 指纹 / 相似度 ──────────────────────────────────────────────────────────────
def hist_fingerprint(history=None) -> str:
    """会话上下文指纹（缓存键分区用）。无上下文 → "h0"（跨用户可复用区）。

    只取每轮 question（追问的语义由前序问题决定，答案正文过长且易变），按序拼接后取短哈希。
    任何异常 → "h?"（不可复用区，宁可不命中也不串答案）。
    """
    try:
        if not history or not isinstance(history, (list, tuple)):
            return CACHE_HK_EMPTY
        parts = []
        for h in history:
            if not isinstance(h, dict):
                continue
            q = h.get("question") or h.get("q") or h.get("content") or ""
            q = str(q).strip()
            if q:
                parts.append(q[:120])
        if not parts:
            return CACHE_HK_EMPTY
        raw = "||".join(parts)
        return "h" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    except Exception:  # noqa: BLE001
        return "h?"


def cache_key(question: str, doc_context: str = "", difficulty: str = "",
              output_format: str = "", history_key: str = CACHE_HK_EMPTY) -> str:
    """问题指纹。同问题 + 同附件载荷 + 同难度 + 同输出形态 + **同上下文分区** → 同 key。

    2026-10-22：纳入 output_format——doc 与 auto 答案必须分区缓存，否则选 doc 会命中
    auto 缓存拿到被截断的短文（见 answer_length_format_deviation_20261022.md F2）。
    2026-10-30：纳入 history_key + CACHE_VERSION——上下文变了答案就该变；bot 升级后旧答案作废。
    """
    raw = (f"{(question or '').strip()}|{doc_context or ''}|{difficulty or ''}"
           f"|{output_format or ''}|{history_key or CACHE_HK_EMPTY}|{CACHE_VERSION}")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def _similar(a: str, b: str) -> float:
    a, b = (a or "").strip(), (b or "").strip()
    if not a or not b:
        return 0.0
    if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.5:
        return 0.0  # 长度悬殊过大 → 0（防长文 vs 短文误判）
    return difflib.SequenceMatcher(None, a, b).quick_ratio()


def _prune_history(history: list, now: float) -> list:
    """按「OR + 24h 硬上限」语义裁剪（与 context_stitch.prune_history 一致）。"""
    if not history:
        return []
    kept = []
    for h in history:
        h = h or {}
        ts = h.get("ts")
        if ts is None:
            if len(kept) < HIST_TTL_ROUNDS:
                kept.append(h)
            continue
        try:
            age = now - float(ts)
        except (TypeError, ValueError):
            if len(kept) < HIST_TTL_ROUNDS:
                kept.append(h)
            continue
        if age > HIST_HARD_CAP:
            continue
        if age <= HIST_TTL_SECONDS:
            kept.append(h)
        elif len(kept) < HIST_TTL_ROUNDS:
            kept.append(h)
    return kept


def _summarize(answer: str, max_len: int = HIST_MAX_PREV_LEN) -> str:
    """从整段答案取首段摘要（无 LLM，规则化），供 Coze 注入历史上下文。"""
    ans = (answer or "").strip()
    if not ans:
        return ""
    first_para = ans.split("\n\n")[0].strip()
    if len(first_para) > max_len:
        first_para = first_para[:max_len] + "…"
    return first_para


# ── 对外 API ───────────────────────────────────────────────────────────────────
def history(session_id: str, now: float = None) -> list:
    """导出有界历史给 Coze（conversation_history 字段）。

    返回 [{question, answer_summary}, ...] 时间升序；无活跃会话或空 → []。
    session_id 为空 → 视为无会话（单轮模式），返回 []（不退化旧行为）。
    """
    if not session_id:
        return []
    if now is None:
        now = time.time()
    with _lock_ctx():
        data = _load()
        sess = (data.get("sessions") or {}).get(session_id)
        if not sess:
            return []
        raw_hist = sess.get("history") or []
        pruned = _prune_history(raw_hist, now)
        out = []
        for h in pruned:
            h = h or {}
            q = (h.get("q") or "").strip()
            ans = (h.get("answer_summary") or "").strip()
            if not q and not ans:
                continue
            out.append({"question": q, "answer_summary": ans})
        return out


def record(session_id: str, question: str, answer: str,
           answer_summary: str = "", difficulty: str = "",
           doc_context: str = "", output_format: str = "",
           history_key: str = "") -> None:
    """记录一轮真实产生的问答（出站成功后调用，非命中短路时）。

    - 写入 history（供后续轮次注入上下文）
    - 写入 global_cache（**仅无上下文分区 h0**；追问写入会污染跨用户缓存）
    - 写入本 session dedup 库（近窗近似重复短路）
    session_id 为空 → 仍可写 global_cache，但不写 history/dedup（单轮模式）。
    history_key 为空 → 由「写入前的服务端历史」自动推导，与提问侧口径一致。
    任何异常静默忽略。
    """
    if not (answer or "").strip():
        return
    now = time.time()
    summ = (answer_summary or "").strip() or _summarize(answer)
    with _lock_ctx():
        data = _load()
        # 上下文分区必须在**写入本轮 history 之前**推导，否则会把自己的问题算进指纹。
        hk = (history_key or "").strip()
        if not hk:
            try:
                _sess = (data.get("sessions") or {}).get(session_id) if session_id else None
                _raw = (_sess or {}).get("history") or []
                _pruned = _prune_history(_raw, now)
                # 2026-10-30 修正：指纹口径必须与提问侧 `hist_fingerprint(history)` 一致。
                # 旧实现只取 question、丢掉 answer_summary → 同一段历史在**写入侧**与
                # **读取侧**算出不同指纹 → 分区错位（重开缓存开关后表现为永不命中或误命中）。
                # `_prune_history` 已返回契约形态 [{question, answer_summary}]，直接传入即可。
                hk = hist_fingerprint(_pruned)
            except Exception:  # noqa: BLE001
                hk = "h?"
        key = cache_key(question, doc_context, difficulty, output_format, hk)
        # 只有「无上下文」分区写全局缓存 → 跨用户可复用区（首轮独立问题）
        # 2026-10-30：客户端缓存总开关关闭时不再写入（读取侧也已恒空）。
        if LOCAL_CACHE_ENABLED and hk == CACHE_HK_EMPTY:
            gcache = data.setdefault("global_cache", {})
            gcache[key] = {"ts": now, "answer": answer}
            # 全局缓存只保留最近 200 条，防无限膨胀
            if len(gcache) > 200:
                oldest = sorted(gcache.items(), key=lambda kv: kv[1].get("ts", 0))[:50]
                for k, _ in oldest:
                    gcache.pop(k, None)

        if session_id:
            sessions = data.setdefault("sessions", {})
            sess = sessions.setdefault(session_id, {"history": [], "dedup": [], "ts": 0})
            # history
            sess["history"] = _prune_history(
                sess.get("history", []) + [{
                    "ts": now, "q": (question or "").strip(),
                    "answer_summary": summ,
                }], now)
            sess["history"] = sess["history"][-HIST_TTL_ROUNDS:]
            # dedup 库：**仅首轮**记录。追问不参与缓存体系（答案由上下文决定，
            # 复用任何历史答案都是错的），因此不写，避免 session_store.json 无谓膨胀。
            # 2026-10-30：客户端缓存总开关关闭时不再写入（读取侧也已恒未命中）。
            if LOCAL_CACHE_ENABLED and hk == CACHE_HK_EMPTY:
                dup = sess.get("dedup", [])
                dup.append({"ts": now, "q": (question or "").strip(),
                            "answer": answer, "key": key, "fmt": output_format, "hk": hk})
                dup = [e for e in dup if now - (e.get("ts") or 0) <= DEDUP_WINDOW]
                sess["dedup"] = dup[-DEDUP_MAX_PER_SESSION:]
            sess["ts"] = now
        _save(data)


def cache_get(question: str, doc_context: str = "", difficulty: str = "",
              output_format: str = "", history_key: str = CACHE_HK_EMPTY) -> str:
    """全局精确指纹缓存命中 → 返回答案；否则空串。

    history_key 非 h0（追问场景）→ 直接不命中：全局缓存只服务「无上下文」分区，
    追问的正确性必须靠真实运行，不能拿别处答案顶上。

    2026-10-30：客户端缓存已总开关关闭（LOCAL_CACHE_ENABLED=False）→ 恒返回空串，
    答案一律以云端为准。恢复见模块顶部说明。
    """
    if not LOCAL_CACHE_ENABLED:
        return ""
    if (history_key or CACHE_HK_EMPTY) != CACHE_HK_EMPTY:
        return ""
    key = cache_key(question, doc_context, difficulty, output_format, history_key)
    if not key:
        return ""
    try:
        data = _load()
        obj = (data.get("global_cache") or {}).get(key)
        if not obj:
            return ""
        if time.time() - float(obj.get("ts") or 0) > CACHE_TTL:
            return ""
        return obj.get("answer") or ""
    except Exception:  # noqa: BLE001
        return ""


def dedup_check(session_id: str, question: str,
                window: int = DEDUP_WINDOW, output_format: str = "",
                history_key: str = "") -> tuple:
    """同 session 近窗近似重复检测。

    返回 (is_dup, prev_answer, secs_ago)：is_dup 且 prev_answer 非空 → 调用方应短路直回。
    session_id 为空 → 不查（单轮模式），返回 (False, None, 0)。
    output_format：仅当两侧均显式指定且不一致时跳过（doc 不短路到 auto 答案）。
    history_key：非空时要求上下文分区一致——同一句话在不同上下文里答案应当不同，
        否则第 1 轮问过的题在第 8 轮再问会拿到第 1 轮的答案（2026-10-30 修复）。

    2026-10-30：客户端缓存已总开关关闭（LOCAL_CACHE_ENABLED=False）→ 恒返回未命中，
    重复请求一律真实出站。恢复见模块顶部说明。
    """
    if not LOCAL_CACHE_ENABLED:
        return False, None, 0
    if not session_id:
        return False, None, 0
    try:
        now = time.time()
        data = _load()
        sess = (data.get("sessions") or {}).get(session_id)
        if not sess:
            return False, None, 0
        best, best_sim = None, 0.0
        for e in sess.get("dedup", []):
            ts = e.get("ts") or 0
            if now - ts > window:
                continue
            # 输出形态不同 → 视为不同请求（doc 不应复用 auto 答案）
            if output_format and e.get("fmt") and e.get("fmt") != output_format:
                continue
            # 上下文分区不同 → 不能复用（旧记录无 hk，按 h0 处理）
            if history_key and (e.get("hk") or CACHE_HK_EMPTY) != history_key:
                continue
            sim = _similar(question or "", e.get("q") or "")
            if sim >= DEDUP_SIM and sim > best_sim:
                best_sim, best = sim, e
        if best and (best.get("answer") or "").strip():
            secs = max(0, int(now - (best.get("ts") or now)))
            return True, best["answer"], secs
        return False, None, 0
    except Exception:  # noqa: BLE001
        return False, None, 0


def clear_session(session_id: str) -> None:
    """清空某 session 的 history + dedup（保留 global_cache）。新会话时调用。"""
    if not session_id:
        return
    with _lock_ctx():
        data = _load()
        sess = (data.get("sessions") or {}).pop(session_id, None)
        if sess is not None:
            _save(data)


# ── 离线自测 ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import tempfile

    _tmp = tempfile.mkdtemp()
    os.environ["CT_ADVISOR_DATA_ROOT"] = _tmp  # 不污染生产（本模块用固定 STORE_PATH，
    # 故额外覆盖：自测时改 STORE_PATH 指向临时目录）
    # 直接改模块级常量指向临时目录（仅自测用）
    STORE_PATH = Path(_tmp) / "session_store.json"
    LOCK_PATH = Path(_tmp) / ".session_store.lock"
    # 2026-10-30：客户端缓存默认关闭（生产态）。自测要验证缓存/去重逻辑本身，
    # 故此处强制打开；末尾再切回关闭态验证「开关确实生效」。
    LOCAL_CACHE_ENABLED = True

    sid = "sha256:selftest"
    q1 = "多中心研究中如果一个中心突然要退出怎么处理"
    q1b = "多中心研究如果一个中心突然退出怎么处理"   # 近似重复
    q2 = "样本量怎么估算"
    ans1 = "答：先评估对统计效能影响，与申办方/CRO 协商退出或保留已入组数据，按方案偏离处理并上报伦理。"
    ans2 = "答：按主要终点、效应量、α、power 估算。"

    # history 初始空
    assert history(sid) == [], "history 初始应为空"
    # record 一轮
    record(sid, q1, ans1)
    assert len(history(sid)) == 1, "record 后 history 应有 1 条"
    # dedup 近似命中
    hit, prev, ago = dedup_check(sid, q1b)
    assert hit and prev == ans1, "近窗近似重复应命中"
    # 精确缓存
    assert cache_get(q1) == ans1, "全局精确缓存应命中"
    assert cache_get(q2) == "", "不同问题不应命中"
    # 第二轮 record 后 history 增至 2
    record(sid, q2, ans2)
    assert len(history(sid)) == 2, "两轮后 history 应为 2"
    # 清空 session
    clear_session(sid)
    assert history(sid) == [], "clear 后 history 应空"
    assert cache_get(q1) == ans1, "clear 不清全局缓存"

    # ── 2026-10-30：上下文分区（跨用户复用 vs 追问隔离）──────────────────────
    assert hist_fingerprint(None) == CACHE_HK_EMPTY, "None 历史应落 h0 分区"
    assert hist_fingerprint([]) == CACHE_HK_EMPTY, "空历史应落 h0 分区"
    hk_a = hist_fingerprint([{"question": "问题A"}])
    hk_b = hist_fingerprint([{"question": "问题B"}])
    assert hk_a != hk_b and hk_a.startswith("h") and hk_a != CACHE_HK_EMPTY, "不同上下文指纹应不同"

    sid3 = "sha256:selftest-ctx"
    record(sid3, "首轮独立问题", "首轮答案")       # 历史空 → h0 → 写全局缓存
    assert cache_get("首轮独立问题") == "首轮答案", "首轮应进全局缓存（跨用户可复用）"
    record(sid3, "追问句", "追问答案")             # 历史非空 → 不写全局缓存
    assert cache_get("追问句") == "", "追问不应进全局缓存（会污染跨用户缓存）"
    # 非 h0 分区永不命中全局缓存
    assert cache_get("首轮独立问题", history_key=hk_a) == "", "非 h0 分区不得命中全局缓存"
    # dedup 也按上下文分区隔离：同一句话在不同上下文不能复用
    _hk_now = hist_fingerprint([{"question": "首轮独立问题"}])   # 模拟「已聊过一轮」的上下文
    _dh, _dv, _ = dedup_check(sid3, "首轮独立问题", history_key=_hk_now)
    assert not _dh, "同一句话在不同上下文不应 dedup 命中（否则串答案）"
    _dh2, _dv2, _ = dedup_check(sid3, "首轮独立问题", history_key=CACHE_HK_EMPTY)
    assert _dh2 and _dv2 == "首轮答案", "同上下文内重复提交仍应命中（防重复计费）"

    # ── 2026-10-30：客户端缓存总开关（生产默认关闭）验证 ────────────────────
    LOCAL_CACHE_ENABLED = False
    assert cache_get("首轮独立问题") == "", "关闭态：精确缓存必须不命中"
    _dh3, _dv3, _ = dedup_check(sid3, "首轮独立问题", history_key=CACHE_HK_EMPTY)
    assert not _dh3, "关闭态：近似去重必须不命中"
    record(sid3, "关闭态新问题", "关闭态新答案")
    assert cache_get("关闭态新问题") == "", "关闭态：不得写入全局缓存"
    assert len(history(sid3)) == 3, "关闭态：history 仍须照常写入（上下文不是缓存，不能关）"
    LOCAL_CACHE_ENABLED = True   # 复原

    print("session_store self-test: ALL PASSED")
