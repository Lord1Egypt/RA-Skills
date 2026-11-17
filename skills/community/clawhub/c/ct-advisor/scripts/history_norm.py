#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ct-advisor — `conversation_history` 归一化（**单一事实来源** · 2026-10-30）

背景（本次缺陷修复的根因）
--------------------------
`conversation_history` 是 ct-base/references/continuity.md §2.2–§2.5 定义的**家族契约**：

    [{question, answer_summary}]    每轮 1 个 dict · 升序（最早在前）
    answer_summary ≤ 200 字符（取结论首段）· 轮数有界（cap）

但 2026-10-30 排查发现，同一字段存在**三个生产者、三种形态**：

  | 生产者                   | 形态                     | 顺序 | 摘要截断 |
  |--------------------------|--------------------------|------|----------|
  | scripts/entry.py         | question / answer_summary | 升序 | ✅ |
  | scripts/refine_answer.py | question / answer_summary | 升序 | ✅ |
  | workbench/index.html     | **{role, content}**       | **倒序** | ❌ 全文 |

且 workbench 代理的注入门控是 `if not data.get("conversation_history")`：
前端一旦发**非空**（哪怕形态错误），服务端那份**契约正确**的持久化历史
（`session_store.history()`）就**永远不会被注入**；而后端 `_history_fp` 只认
`question`/`answer_summary`，读到 role/content 一律取空 → **历史内容事实为空**，
连续追问退化为"按全新独立问题作答"。

本模块提供唯一的归一化实现，供下列入口共用：
  - workbench/ct-advisor-proxy.py  （工作台真实入口）
  - scripts/orchestrate.py         （CLI 主链路 RefineRequest 构建）
  - adapters/refiner.py            （RefineRequest.normalize 兜底）

后端 Coze 侧有一份**镜像实现** `adapters/coze/src/utils/history_norm.py`
（Coze 工作区独立打包，无法 import 本地 scripts/）；两侧行为由
`scripts/tests/test_history_norm.py` 的 parity 断言锁定，改一侧必须同步另一侧。

设计要点
--------
1. **形态归一**：契约形态直通；messages 形态（`{role, content}`）两两配对成轮，
   assistant 消息取结论首段作摘要。
2. **顺序归一**：messages 形态在本代码库中**只有** `workbench/index.html:lastTurns()`
   一个生产者，其产出为**新→旧**（`state.hist.slice().reverse()`）→ 归一时反转回升序。
   契约形态由生产者保证升序，原样保留。
3. **有界**：轮数上限 `max_rounds`；单轮摘要上限 `max_summary`。
4. **静默降级**：任何异常输入返回空列表，绝不抛错（不阻断主流程）。
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# ── 有界口径（对齐 ct-base continuity.md §2.4/§2.5）────────────────────────
DEFAULT_MAX_ROUNDS = 10        # 有效轮数上限（session_store.HIST_TTL_ROUNDS 同值）
DEFAULT_MAX_SUMMARY = 200      # 单轮 answer_summary 字符上限（MAX_PREV_LEN≈200）

# messages 形态里代表「用户问题」的角色
_USER_ROLES = ("user", "human", "")
# 代表「模型回答」的角色
_ASSISTANT_ROLES = ("assistant", "ai", "bot")


def _summarize(answer: Any, max_len: int = DEFAULT_MAX_SUMMARY) -> str:
    """从整段答案取**结论首段**作摘要（对齐 session_store._summarize / MAX_PREV_LEN）。

    反直觉经验（continuity.md §2.5）：结论首段含"已定的设计实体"，
    远端 LLM 据此继承前情比纯问题文本更准。
    """
    text = (answer or "").strip() if isinstance(answer, str) else str(answer or "").strip()
    if not text:
        return ""
    first = text.split("\n\n")[0].strip()
    if not first:
        first = text.split("\n", 1)[0].strip()
    if max_len and len(first) > max_len:
        first = first[:max_len] + "…"
    return first


def _looks_like_messages_form(items: List[Any]) -> bool:
    """判定整个列表是否为 messages 形态（`{role, content}`）。

    只要有一个条目带 `role`，或带 `content` 而不带契约字段，即判定为 messages 形态
    ——按**整体**判定，避免混合列表被逐条误判。
    """
    for e in items:
        if not isinstance(e, dict):
            continue
        if e.get("role") is not None:
            return True
        if "content" in e and not ({"question", "q", "answer_summary", "answer"} & set(e.keys())):
            return True
    return False


def normalize_history(raw: Any,
                      max_rounds: int = DEFAULT_MAX_ROUNDS,
                      max_summary: int = DEFAULT_MAX_SUMMARY) -> List[Dict[str, str]]:
    """把任意形态的 `conversation_history` 归一为契约形态。

    返回 `[{question, answer_summary}, ...]`，**升序**（最早在前）、每轮 1 个 dict。

    - 契约形态 `{question|q, answer_summary|answer}` → 直通（顺序原样保留）；
    - messages 形态 `{role, content}` → 两两配对成轮后**反转为升序**
      （本代码库唯一生产者 `workbench/index.html:lastTurns()` 产出为新→旧）；
    - 纯字符串条目 → 视为「只有问题、无摘要」的一轮；
    - 非 list / None / 其它异常 → 返回 `[]`（静默降级，不抛错）。
    """
    if not isinstance(raw, list) or not raw:
        return []
    try:
        msgs = _looks_like_messages_form(raw)
        turns: List[Dict[str, str]] = []
        for e in raw:
            if isinstance(e, str):
                t = e.strip()
                if t:
                    turns.append({"question": t, "answer_summary": ""})
                continue
            if not isinstance(e, dict):
                continue
            if msgs:
                content = e.get("content")
                if content is None:
                    content = e.get("text") or ""
                content = str(content).strip()
                if not content:
                    continue
                role = str(e.get("role") or "").strip().lower()
                if role in _ASSISTANT_ROLES:
                    # assistant 消息 → 配对到上一条「只有问题」的轮次作摘要；
                    # 若上一轮已有摘要或不存在 → 视为孤立 assistant，丢弃（无法构成一轮）
                    if turns and turns[-1]["question"] and not turns[-1]["answer_summary"]:
                        turns[-1]["answer_summary"] = _summarize(content, max_summary)
                else:
                    # user / 未知角色 → 开启新一轮
                    turns.append({"question": content, "answer_summary": ""})
            else:
                q = e.get("question")
                if q is None:
                    q = e.get("q")
                a = e.get("answer_summary")
                if a is None:
                    a = e.get("answer")
                q = str(q or "").strip()
                a_s = _summarize(a, max_summary)
                if not q and not a_s:
                    continue
                turns.append({"question": q, "answer_summary": a_s})
        if msgs:
            # lastTurns() 产出为「新→旧」→ 反转回契约要求的升序
            turns.reverse()
        turns = [t for t in turns if t["question"] or t["answer_summary"]]
        if max_rounds and len(turns) > max_rounds:
            turns = turns[-max_rounds:]
        return turns
    except Exception:  # noqa: BLE001  归一化失败绝不阻断主流程
        return []


def merge_history(primary: Optional[List[Dict[str, str]]],
                  secondary: Optional[List[Dict[str, str]]],
                  max_rounds: int = DEFAULT_MAX_ROUNDS) -> List[Dict[str, str]]:
    """合并两份**已归一且升序**的历史。

    - `primary` 为基（通常是服务端 session_store 历史，契约正确、跨刷新存活）；
    - `secondary` 中 `primary` 没有的轮次按问题文本去重后**追加到尾部**
      （尾部 = 更新的一轮，维持升序）；
    - 结果再按 `max_rounds` 截尾。
    """
    out: List[Dict[str, str]] = [dict(t) for t in (primary or [])]
    seen = {(t.get("question") or "").strip() for t in out if (t.get("question") or "").strip()}
    for t in (secondary or []):
        if not isinstance(t, dict):
            continue
        q = (t.get("question") or "").strip()
        a = (t.get("answer_summary") or "").strip()
        if not q:
            continue
        if q in seen:
            continue
        seen.add(q)
        out.append({"question": q, "answer_summary": a})
    if max_rounds and len(out) > max_rounds:
        out = out[-max_rounds:]
    return out


# ── 离线自测 ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 1) 契约形态直通
    c = [{"question": "Q1", "answer_summary": "A1"}, {"question": "Q2", "answer_summary": "A2"}]
    assert normalize_history(c) == c, "契约形态应原样保留"

    # 2) messages 形态（新→旧）→ 配对 + 反转回升序
    m = [
        {"role": "user", "content": "Q2"},
        {"role": "assistant", "content": "A2\n\ndetail"},
        {"role": "user", "content": "Q1"},
        {"role": "assistant", "content": "A1"},
    ]
    assert normalize_history(m) == [
        {"question": "Q1", "answer_summary": "A1"},
        {"question": "Q2", "answer_summary": "A2"},
    ], f"messages 形态应配对成轮并反转为升序：{normalize_history(m)}"

    # 3) 摘要取结论首段 + 200 字截断
    long_ans = "首段结论。" + "x" * 500 + "\n\n第二段"
    assert normalize_history([{"question": "Q", "answer_summary": long_ans}])[0]["answer_summary"].startswith("首段结论。")
    assert len(normalize_history([{"question": "Q", "answer_summary": long_ans}])[0]["answer_summary"]) <= 201

    # 4) 轮数有界
    many = [{"question": f"Q{i}", "answer_summary": f"A{i}"} for i in range(20)]
    assert len(normalize_history(many, max_rounds=6)) == 6, "轮数上限应生效"

    # 5) 异常输入静默降级
    assert normalize_history(None) == []
    assert normalize_history("not-a-list") == []
    assert normalize_history([None, 123, {}]) == []

    # 6) merge：primary 基 + secondary 新轮追加到尾部
    p = [{"question": "Q1", "answer_summary": "A1"}]
    s = [{"question": "Q1", "answer_summary": "A1"},
         {"question": "Q2", "answer_summary": "A2"}]
    assert merge_history(p, s) == [
        {"question": "Q1", "answer_summary": "A1"},
        {"question": "Q2", "answer_summary": "A2"},
    ], "secondary 的新轮应追加到尾部"

    print("history_norm self-test: ALL PASSED")
