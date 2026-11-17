"""一次调用扇出多角色判定（战斗回合）。

与逐条 run() 的区别：模型路径下**只发一次请求**，问完所有角色的所有原子问题；
加角色/加问题几乎不增加往返次数（借鉴 System One 的 fan-out）。纯规则路径则逐条走查表。
"""

from __future__ import annotations

from typing import Any, Callable

from . import check_rules
from .bridge import CheckOutcome, render, resolve_packet
from .contracts import DEFAULT_CONFIDENCE_FLOOR, DecisionPacket, Question, validate_answers
from .judge import compose, rule_only_answers
from .questions import build_questions

AnswersProvider = Callable[..., dict[str, Any]]


def build_batch_questions(state: dict[str, Any], declarations: list[dict[str, Any]],
                          rules: dict[str, Any] | None = None) -> list[Question]:
    """为每个角色声明生成带前缀的问题集（d0_xxx / d1_xxx ...）。"""
    table = rules or check_rules.load_rules()
    questions: list[Question] = []
    for index, declaration in enumerate(declarations):
        for question in build_questions(state, str(declaration.get("action") or ""), table):
            questions.append(Question(
                f"d{index}_{question.id}", question.type,
                question.instructions, list(question.criteria),
            ))
    return questions


def _state_for(state: dict[str, Any], declaration: dict[str, Any]) -> dict[str, Any]:
    """为单条声明派生一份状态：把该声明的执行者设为默认执行者。"""
    actor = str(declaration.get("actor") or "")
    if not actor:
        return state
    derived = dict(state)
    options = list(state.get("acting_options") or [])
    if actor not in options:
        options.append(actor)
    derived["acting_options"] = options
    derived["acting_default"] = actor
    return derived


def _answers_for(payload: Any, index: int) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    prefix = f"d{index}_"
    return {key[len(prefix):]: value for key, value in payload.items()
            if str(key).startswith(prefix)}


def _apply_attack_overrides(packet: DecisionPacket, declaration: dict[str, Any]) -> None:
    """攻击声明的固定语义（由引擎确定，不交给模型）：

    1. 必定要掷命中检定；
    2. AC 与命中机制都是确定的，因此不再因“DC 无依据/技能未定”而上报升级，
       仅保留“与模组事实冲突”这类真实风险。
    """
    if declaration.get("target_ac") is None:
        return
    packet.requires_check = True
    packet.escalation_reasons = [r for r in packet.escalation_reasons if "模组" in r]
    packet.escalate = bool(packet.escalation_reasons)


def run_batch(state: dict[str, Any], declarations: list[dict[str, Any]],
              answers_provider: AnswersProvider | None = None,
              rules: dict[str, Any] | None = None,
              floor: float = DEFAULT_CONFIDENCE_FLOOR,
              floors: dict[str, float] | None = None) -> list[DecisionPacket]:
    """批量判定。模型路径一次调用；契约不合规的个体单独回退本地规则。"""
    table = rules or check_rules.load_rules()
    packets: list[DecisionPacket] = []

    if answers_provider is None:
        for declaration in declarations:
            action = str(declaration.get("action") or "")
            decl_state = _state_for(state, declaration)
            questions = build_questions(decl_state, action, table)
            raw = rule_only_answers(decl_state, action, questions, table)
            packet = compose(decl_state, action, validate_answers(raw, questions),
                             table, floor, floors)
            _apply_attack_overrides(packet, declaration)
            packets.append(packet)
        return packets

    batch_questions = build_batch_questions(state, declarations, table)
    combined_action = " | ".join(
        f"{d.get('actor') or '?'}: {d.get('action') or ''}" for d in declarations
    )
    try:
        raw = answers_provider(batch_questions, state, combined_action)
        payload = raw.get("answers") if isinstance(raw, dict) and "answers" in raw else raw
    except Exception:
        payload = {}

    for index, declaration in enumerate(declarations):
        action = str(declaration.get("action") or "")
        decl_state = _state_for(state, declaration)
        questions = build_questions(decl_state, action, table)
        try:
            packet = compose(decl_state, action,
                             validate_answers(_answers_for(payload, index), questions),
                             table, floor, floors)
        except Exception:
            raw_rule = rule_only_answers(decl_state, action, questions, table)
            packet = compose(decl_state, action, validate_answers(raw_rule, questions),
                             table, floor, floors)
            packet.fallback_chain.insert(0, "batch_answer_invalid")
        _apply_attack_overrides(packet, declaration)
        packets.append(packet)
    return packets


def resolve_batch(state: dict[str, Any], declarations: list[dict[str, Any]],
                  answers_provider: AnswersProvider | None = None,
                  sheets: dict[str, dict] | None = None,
                  d20s: list[int | None] | None = None,
                  rules: dict[str, Any] | None = None,
                  floor: float = DEFAULT_CONFIDENCE_FLOOR,
                  floors: dict[str, float] | None = None) -> list[dict[str, Any]]:
    """批量判定并直接结算成检定明细。d20s 可传入固定骰面（测试/复现用）。"""
    table = rules or check_rules.load_rules()
    packets = run_batch(state, declarations, answers_provider, table, floor, floors)
    results: list[dict[str, Any]] = []
    for index, (declaration, packet) in enumerate(zip(declarations, packets)):
        actor = str(declaration.get("actor") or packet.acting_character or "")
        sheet = (sheets or {}).get(actor)
        d20 = d20s[index] if d20s and index < len(d20s) else None
        target_ac = declaration.get("target_ac")
        outcome: CheckOutcome = resolve_packet(
            packet, sheet=sheet, d20=d20, rules=table,
            target_ac=target_ac,
            weapon_name=str(declaration.get("weapon") or ""),
        )
        results.append({
            "actor": actor,
            "action": str(declaration.get("action") or ""),
            "packet": packet,
            "outcome": outcome,
            "text": render(outcome) if outcome.ran else (outcome.note or "无需检定"),
        })
    return results

def render_round(results: list[dict[str, Any]]) -> str:
    """把一轮批量判定渲染成可直接贴给玩家的文本。"""
    lines = [f"── 本回合判定（{len(results)} 名角色）──"]
    for result in results:
        packet = result["packet"]
        flag = " ⚠需升级" if packet.escalate else ""
        lines.append(f"[{result['actor']}] {result['action']}{flag}")
        lines.append(result["text"])
    return "\n".join(lines)
