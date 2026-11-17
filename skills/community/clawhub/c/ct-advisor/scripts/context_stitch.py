#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — 跨轮历史打包（模式 B / 2026-08-25 硬弃用本地 is_followup）

背景：
  - 类型 A 追问（"刚才说的那个药"）由 route.py ANAPHORA → vague → clarify_loop 覆盖。
  - 类型 B 追问（"若检验效能改用90%呢" / "如果HR是0.7呢"）无回指词，早期直接转发 Coze
    时 payload 只有 original_question、无上一题上下文 → Coze 重复追问已给参数。
  - 旧方案：本地用 is_followup() 正则猜"是不是追问"，命中才把追问缝合为自包含问题。
    实测脆弱（长句式设计演进全漏判），属脆弱分类器，已硬弃用。

模式 B（当前，对齐 ct-base/references/continuity.md §2）：
  - **永远**把有界历史经 `conversation_history`（结构化字段）外发给远端 Coze LLM，
    由远端判"是否追问 / 继承哪些前情"。本地不再用正则猜追问、不再做字符串前缀缝合。
  - 本地仅做确定性结构闸门：`is_ctx_valid`（24h 硬上限 + 2h/≤10 轮兜底）+ `prune_history`
    （有界裁剪），以及把历史导出为 Coze 可读的结构化列表。
  - 判权完全交给远端 LLM —— 无本地启发式盲区。

设计：
  - stdlib-only，无网络（除外发给本就要调用的 Coze 外）、无 LLM。
  - 缓存文件：{ROOT}/config/context_cache.json（本地运行态，写透镜像；非连续性唯一源，
    仅作下次打包的数据源；相关性判定由远端完成）。

用法：
  python scripts/context_stitch.py --store --q "<本轮问题>" --summary "<本轮结论摘要>"
        → 写入本轮上下文（供下一轮 pack_history_for_coze 使用）
  python scripts/context_stitch.py --clear
        → 清空会话上下文（新会话）
  echo "<用户问题>" | python scripts/context_stitch.py
        → 原样回显（调试用；模式 B 下本地不做任何改写）
"""

import argparse
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "config", "context_cache.json")
TTL_ROUNDS = 10         # 上下文有效轮数（OR 关系：满足"2h 内"或"≤10 条"任一即可保留）
TTL_SECONDS = 7200      # 软时间窗：同一机器过去 2 小时内的连续调用视为同一会话
HARD_CAP_SECONDS = 86400  # 硬上限：任何超过 24h 的记录一律丢弃（防孤立旧记录污染）
MAX_PREV_LEN = 200      # 拼接前缀上限（防止上下文膨胀）
MAX_HISTORY_CTX = 600   # 多轮累积上下文上限（防止膨胀）


def extract_summary(prev_q: str, prev_answer: str = "") -> str:
    """从上一轮问题中提取"关键实体摘要"（代码规则：保留药名/参数/终点，裁剪语气词）。

    优先用上一轮 Coze 结论首段（含设计实体），因为纯问题文本不含"已定的试验设计"。
    抽取为规则化兜底（无 LLM）：截取结论首段 + 命中关键设计词的句子。
    """
    prev_q = (prev_q or "").strip()
    if not prev_q:
        return ""
    # 若已有上一轮结论，优先用结论摘要（含设计实体），否则退化到问题摘要
    if prev_answer and prev_answer.strip():
        ans = prev_answer.strip()
        # 取首段（通常含核心设计结论）
        first_para = ans.split("\n\n")[0].strip()
        # 若首段过长，截取前 MAX_PREV_LEN
        if len(first_para) > MAX_PREV_LEN:
            first_para = first_para[:MAX_PREV_LEN] + "…"
        return first_para
    # 剥离已拼接前缀（防止多轮追问嵌套）。两种格式：
    #   "承接上一问（…），追问：X"（旧 stitch 产出，历史数据可能残留）
    #   "承接上一问（…），追问：X"（含全角括号变体）——统一取最后一个 "追问：" 之后
    idx = prev_q.rfind("追问：")
    if idx >= 0:
        prev_q = prev_q[idx + len("追问："):]
    # 裁剪首尾语气/承接词，保留主体
    s = prev_q
    s = s.strip()
    if len(s) > MAX_PREV_LEN:
        s = s[:MAX_PREV_LEN] + "…"
    return s


def load_cache():
    try:
        with open(CACHE, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def is_ctx_valid(cache: dict) -> bool:
    """上下文是否仍属活跃会话（决定是否允许打包历史）。

    2026-08-24 语义（OR + 24h 硬上限）：
      顶层判定依据最近一次写入 ts 与累积轮数——
        - 硬上限：最近写入 age > HARD_CAP_SECONDS(24h) → 失效（任何超 24h 必丢）；
        - 软条件（OR）：age <= TTL_SECONDS(2h)  OR  rounds <= TTL_ROUNDS(10)
          即"2h 内"与"≤10 轮"满足任一即视为活跃；两者都不满足（超 2h 且超 10 轮）才失效。
      注：单条 history 记录的裁剪（2h 内 OR ≤10 条，再 AND 未超 24h）由 `prune_history` 负责，
      与顶层判定保持同一 OR+硬上限语义。
    """
    if not isinstance(cache, dict):
        return False
    ts = cache.get("ts")
    rounds = int(cache.get("rounds", 0))
    if ts is None:
        # 兼容旧缓存（无 ts）：仅按轮数判，下次写会补 ts
        return rounds <= TTL_ROUNDS
    try:
        age = time.time() - float(ts)
    except (TypeError, ValueError):
        return False
    if age > HARD_CAP_SECONDS:
        return False
    return (age <= TTL_SECONDS) or (rounds <= TTL_ROUNDS)


def prune_history(history: list, now: float = None) -> list:
    """按「OR + 24h 硬上限」语义裁剪历史，是 continuation 上下文保留的唯一权威逻辑。

    保留规则（每条记录独立判定）：
      keep = (age <= TTL_SECONDS[2h])  OR  (len(保留集) <= TTL_ROUNDS[10])
             再 AND  (age <= HARD_CAP_SECONDS[24h])
    即：在 2h 内的记录全留（不受 10 条限制）；超 2h 的记录按"总数 ≤10"兜底截断；
        任何超过 24h 的记录无条件丢弃。
    store 段与读取处均复用本函数，避免规则分散。
    """
    if not history:
        return []
    if now is None:
        now = time.time()
    kept = []
    for h in history:
        ts = (h or {}).get("ts")
        if ts is None:
            # 无 ts 的旧记录：按"轮数兜底"纳入（不超 10 即可），下次写会补 ts
            if len(kept) < TTL_ROUNDS:
                kept.append(h)
            continue
        try:
            age = now - float(ts)
        except (TypeError, ValueError):
            if len(kept) < TTL_ROUNDS:
                kept.append(h)
            continue
        if age > HARD_CAP_SECONDS:
            continue  # 超 24h 硬丢
        if age <= TTL_SECONDS:
            kept.append(h)  # 2h 内全留
        elif len(kept) < TTL_ROUNDS:
            kept.append(h)  # 超 2h 但总数未超 10，兜底留
    return kept


def save_cache(cache):
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        cache = dict(cache or {})
        cache.setdefault("ts", time.time())
        with open(CACHE, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass


def pack_history_for_coze(cache: dict = None, now: float = None) -> list:
    """导出有界历史给 Coze（conversation_history 字段），由远端 LLM 自行判相关性。

    模式 B 唯一权威路径：本地只做结构闸门 + 24h 硬上限（确定性、可测），
    把"哪些前情相关、如何引用"委派给本就要调用的 Coze LLM，避免代码层窄启发式
    漏判长句式设计演进（2026-08-24 CTDB_advisorlog 实测盲区）。

    返回：[{'question': str, 'answer_summary': str}, ...]，按时间升序（最早在前）。
    规则：
      - 顶层失效（is_ctx_valid=False：超 24h 或 超 2h 且超 10 轮）→ 返回 []；
      - 否则用 prune_history（OR + 24h 硬上限）裁剪后导出；
      - 单条空内容（q 与 answer_summary 皆空）跳过；
      - 空 history 也返回 []（Coze 端据此忽略，保证历史版本兼容）。
    """
    if cache is None:
        cache = load_cache()
    if not isinstance(cache, dict) or not is_ctx_valid(cache):
        return []
    history = prune_history(cache.get("history", []) or [], now=now)
    out = []
    for h in history:
        h = h or {}
        q = (h.get("q") or "").strip()
        ans = (h.get("answer_summary") or h.get("summary") or "").strip()
        if not q and not ans:
            continue
        out.append({"question": q, "answer_summary": ans})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="ct-advisor 跨轮历史打包（模式 B）")
    ap.add_argument("--store", action="store_true",
                    help="存储本轮上下文（--q + --summary）")
    ap.add_argument("--q", default="", help="本轮问题（--store 用）")
    ap.add_argument("--summary", default="", help="本轮结论摘要（--store 用）")
    ap.add_argument("--clear", action="store_true", help="清空会话上下文")
    args = ap.parse_args()

    if args.clear:
        save_cache({"rounds": 0})
        print("cleared")
        return 0

    if args.store:
        cache = load_cache()
        cache["rounds"] = 0
        cache["q"] = args.q
        cache["summary"] = args.summary
        save_cache(cache)
        print("stored")
        return 0

    # 模式 B：本地不做追问判定 / 字符串缝合。历史打包由 refine_answer 经
    # pack_history_for_coze 完成。此处 stdin 仅原样回显（调试用）。
    q = sys.stdin.read().strip()
    print(q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
