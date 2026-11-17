"""一轮叙事流水线（P1）：一次调用出「叙事 + delta」，代码负责落地与把关。

分工：
- 模型：叙事文本 + 类型化 delta（advance_to / events / tone / 自检冲突）；
- 代码：可达性校验（不可达就丢弃推进）、状态落地、相关性筛选（预取期）、一致性复核（可选）。

每轮**只调用一次**模型；相关性筛选与一致性复核都不在关键路径上。
"""

from __future__ import annotations

from typing import Any

from ..judge.contracts import Question, validate_answers
from .contracts import TurnContractError, TurnResult, validate_turn
from .plot_graph import advance, injection_context, render_context, successors
from .prompt import MAX_SLICES, RELEVANCE_FLOOR, select_relevant  # 单一来源，避免重复实现
from .render import internal_leaks

MAX_SLICES = 4
RELEVANCE_FLOOR = 0.5


def build_prompt(graph: dict[str, Any], state: dict[str, Any],
                 scene_slice: str, canon_facts: list[str],
                 party_digest: str = "", extra_slices: list[str] | None = None,
                 variant: str = "") -> tuple[str, str]:
    """返回 (system, user)。system 逐轮不变、放最前，便于命中 prefix cache。"""
    from .client import SYSTEM_PROMPT

    ctx = injection_context(graph, state)
    reachable = successors(graph, str(state.get("current_node")))
    node_titles = {n["id"]: n["title"] for n in graph.get("nodes") or []}

    system = SYSTEM_PROMPT
    user_lines = [
        "【当前剧情骨架】", render_context(ctx), "",
        f"【可达节点】{', '.join(f'{nid}={node_titles.get(nid, nid)}' for nid in reachable[:8]) or '无'}",
        "【可达节点 id 白名单】" + (" ".join(reachable[:8]) or "(空)"),
        "",
        "【队伍】", party_digest or "(无)", "",
        "【当前场景原文】", scene_slice or "(无)", "",
    ]
    if extra_slices:
        user_lines += ["【相关补充片段】", "\n---\n".join(extra_slices), ""]
    user_lines += ["【已知事实（不得冲突）】"]
    user_lines += [f"- {fact}" for fact in canon_facts[:20]] or ["- (无)"]
    if variant:
        user_lines += ["", f"【本次玩家行动】{variant}"]
    return system, "\n".join(user_lines)


def run_turn(action: str, provider, graph: dict[str, Any], state: dict[str, Any],
             scene_slice: str, canon_facts: list[str], party_digest: str = "",
             extra_slices: list[str] | None = None,
             stream: bool = False, on_chunk=None) -> TurnResult:
    """执行一轮叙事：一次调用 + 一次修复机会；不合规则抛错交给上层回退。

    `stream=True` 时边收边把叙事增量交给 `on_chunk`（首字延迟大幅度降低）。
    消息分三段（system / stable / volatile），stable 逐轮不变以命中 prefix cache。
    """
    from .prompt import build_messages

    reachable = successors(graph, str(state.get("current_node")))
    messages = build_messages(graph, state, party_digest, scene_slice, canon_facts,
                              extra_slices, action)
    last_error = ""
    for _attempt in range(2):
        try:
            raw = provider.complete_json_messages(messages, stream=stream, on_chunk=on_chunk)
            result = validate_turn(raw, reachable)
            leaks = internal_leaks(result.narration)
            if leaks:
                raise TurnContractError(
                    "narration leaks internal terms: " + ", ".join(leaks[:4]))
            if result.delta.advance_to:
                result.notes.append(f"advance→{result.delta.advance_to}")
            return result
        except TurnContractError as exc:
            last_error = str(exc)
            messages = list(messages)
            messages[-1] = {
                "role": "user",
                "content": messages[-1]["content"] +
                f"\n\n【上次输出不合规，必须修正】{last_error}",
            }
    raise TurnContractError(f"turn contract failed after repair: {last_error}")


def apply_turn(state: dict[str, Any], graph: dict[str, Any],
               result: TurnResult) -> dict[str, Any]:
    """把 delta 落到剧情状态上；推进不可达则丢弃（fail closed，纵深防御）。"""
    delta = result.delta
    new_state = dict(state)
    allowed = successors(graph, str(state.get("current_node")))
    target = delta.advance_to
    if target and target not in allowed:
        result.rejected_advance = target
        result.notes.append(f"拒绝推进（不可达）：{target}")
        target = ""
    if target:
        new_state = advance(new_state, graph, target,
                            event=delta.events[0] if delta.events else "")
        if len(delta.events) > 1:
            new_state["events"] = list(new_state.get("events") or []) + delta.events[1:]
    elif delta.events:
        new_state["events"] = list(new_state.get("events") or []) + delta.events

    if delta.npc_attitude:
        new_state["last_npc_attitude"] = delta.npc_attitude
    if delta.tone:
        new_state["last_tone"] = delta.tone
    return new_state


def canon_facts(state: dict[str, Any], extra: list[str] | None = None) -> list[str]:
    """从状态里抽出「已知事实」——带上限，避免事实自己把上下文吃光。"""
    facts: list[str] = []
    for event in (state.get("events") or [])[-12:]:
        facts.append(str(event))
    for milestone in (state.get("milestones") or [])[-3:]:
        facts.append(f"已达里程碑：Lv{milestone.get('level')}")
    facts.extend(extra or [])
    return facts[-16:]


# ────────────────── 相关性筛选与一致性复核 ──────────────────
# select_relevant 定义在 prompt.py（与提示词分层同源），此处仅重导出。


def check_consistency(narration: str, facts: list[str], provider) -> tuple[float, str]:
    """独立复核叙事是否与已知事实冲突（额外一次调用；只在需要时开）。"""
    question = Question("conflict", "noul",
                        "下面这段叙事是否与【已知事实】冲突？\n"
                        f"【叙事】{narration[:800]}\n【已知事实】{'; '.join(facts[:12])}")
    raw = provider([question], {"facts": facts}, "一致性复核")
    payload = raw.get("answers") if isinstance(raw, dict) and "answers" in raw else raw
    answers = validate_answers(payload, [question])
    answer = answers.get("conflict")
    value = float(answer.value) if answer is not None else 0.0
    return value, ("conflict" if value >= 0.5 else "ok")
