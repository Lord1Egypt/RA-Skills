"""提示词分层：把「逐轮不变的前缀」与「逐轮变化的后缀」分开。

为什么这么做：主流模型服务按**最长相同前缀**做 prefix cache。
只要把不变的部分（人格提示、队伍摘要、本章索引）放在最前且逐字节相同，
就能命中缓存，直接降低首字延迟与输入成本。

分层：
1. system：人格与输出契约（恒不变）
2. user/stable：队伍摘要 + 本章节点索引（同一章内不变）
3. user/volatile：当前节点骨架 + 场景切片 + 已知事实 + 本轮行动（每轮都变）
"""

from __future__ import annotations

import hashlib
from typing import Any

from ..judge.contracts import Question, validate_answers
from .plot_graph import injection_context, render_context, successors

MAX_SLICES = 4
RELEVANCE_FLOOR = 0.5


def stable_block(graph: dict[str, Any], party_digest: str) -> str:
    """同一章内逐字节不变的部分。"""
    chapter = ""
    node = None
    return "\n".join([
        "【队伍】",
        party_digest or "(无)",
        "",
        "【本章节点索引】",
        chapter or "(见当前节点)",
        "",
        "【输出契约】只输出 JSON；narration 是唯一自由文本字段；不得出现系统术语或节点编号。",
    ])


def volatile_block(graph: dict[str, Any], state: dict[str, Any], scene_slice: str,
                   canon_facts: list[str], extra_slices: list[str] | None,
                   action: str) -> str:
    ctx = injection_context(graph, state)
    reachable = successors(graph, str(state.get("current_node")))
    titles = {n["id"]: n["title"] for n in graph.get("nodes") or []}
    lines = [
        "【当前剧情骨架】", render_context(ctx), "",
        f"【可达节点】{', '.join(f'{nid}={titles.get(nid, nid)}' for nid in reachable[:8]) or '无'}",
        "【可达节点 id 白名单】" + (" ".join(reachable[:8]) or "(空)"),
        "",
        "【当前场景原文】", scene_slice or "(无)", "",
    ]
    if extra_slices:
        lines += ["【相关补充片段】", "\n---\n".join(extra_slices), ""]
    lines += ["【已知事实（不得冲突）】"]
    lines += [f"- {fact}" for fact in canon_facts[:20]] or ["- (无)"]
    if action:
        lines += ["", f"【本次玩家行动】{action}"]
    return "\n".join(lines)


def build_messages(graph: dict[str, Any], state: dict[str, Any], party_digest: str,
                   scene_slice: str, canon_facts: list[str],
                   extra_slices: list[str] | None = None, action: str = "") -> list[dict[str, str]]:
    """三段式消息：system / stable / volatile（顺序对 prefix cache 至关重要）。"""
    from .client import SYSTEM_PROMPT

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": stable_block(graph, party_digest)},
        {"role": "user", "content": volatile_block(graph, state, scene_slice,
                                                   canon_facts, extra_slices, action)},
    ]


def prefix_signature(messages: list[dict[str, str]]) -> str:
    """稳定前缀（system + stable）的指纹——变了就说明缓存要重建。"""
    stable = "\n␟\n".join(m.get("content", "") for m in messages[:2])
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]


def cacheable_prefix_chars(messages: list[dict[str, str]]) -> int:
    return sum(len(m.get("content", "")) for m in messages[:2])


def estimate_tokens(text: str) -> int:
    from .budget import estimate_tokens as _estimate
    return _estimate(text)


def build_relevance_questions(candidates: list[dict[str, Any]],
                              context: dict[str, Any]) -> list[Question]:
    """把「这段是否与当前情形相关」做成批量 Noul（一次调用问完所有候选）。"""
    current = context.get("current", {})
    question = (f"当前处于「{current.get('title')}」（{current.get('chapter')}）。"
                "下面这段模组内容是否与此刻的情形直接相关（会立刻被用到的信息）？")
    return [
        Question(f"s{index}_relevant", "noul", f"{question}\n内容：{item.get('text', '')[:400]}")
        for index, item in enumerate(candidates)
    ]


def select_relevant(candidates: list[dict[str, Any]], context: dict[str, Any],
                    provider, floor: float = RELEVANCE_FLOOR,
                    top_k: int = MAX_SLICES) -> list[dict[str, Any]]:
    """并行 Noul 选片段（预取期调用，不在关键路径）。"""
    if not candidates:
        return []
    questions = build_relevance_questions(candidates, context)
    raw = provider(questions, {"context": context}, "相关性筛选")
    payload = raw.get("answers") if isinstance(raw, dict) and "answers" in raw else raw
    answers = validate_answers(payload, questions)
    scored: list[tuple[float, dict[str, Any]]] = []
    for index, item in enumerate(candidates):
        answer = answers.get(f"s{index}_relevant")
        value = float(answer.value) if answer is not None else 0.0
        if answer is not None and answer.confidence is not None and answer.confidence < 0.3:
            value = 0.0
        scored.append((value, item))
    scored.sort(key=lambda pair: -pair[0])
    return [dict(item, relevance=round(value, 3))
            for value, item in scored[:top_k] if value >= floor]
