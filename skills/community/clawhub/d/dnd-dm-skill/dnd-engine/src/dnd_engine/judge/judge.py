"""判定层：把类型化回答组合成 DecisionPacket（纯代码，非模型产出）。

三条入口：
  - run(..., answers_provider=None)：纯规则路径，不需要模型。
  - run(..., answers_provider=callable)：模型路径，含一次修复与本地兜底。
  - run_batch(...)（见 batch.py）：一次调用扇出多角色判定。

判定优先链：
  技能：模组钉住 > 模型选择 > 检定规则表
  DC ：模组原文 > 检定规则表 > 模型档位 > 默认档
低置信字段不采信，回退本地依据；仍有风险时置 escalate 供上层升级处理。
"""

from __future__ import annotations

from typing import Any, Callable

from . import check_rules
from .contracts import (
    DEFAULT_CONFIDENCE_FLOOR,
    DEFAULT_FLOOR_OVERRIDES,
    AnswerError,
    DecisionPacket,
    Question,
    validate_answers,
)
from .questions import (
    BAND_LABEL_TO_KEY,
    NO_TARGET,
    build_questions,
    label_to_skill,
    skill_labels,
)

AnswersProvider = Callable[..., dict[str, Any]]

_SOCIAL_SKILLS = {"persuasion", "deception", "intimidation", "performance"}
_BAND_BY_LABEL = BAND_LABEL_TO_KEY
_CRITICAL_FIELDS = ("requires_check", "check_skill", "dc_band", "acting_character")


def _rule_intent(skill: str, action: str) -> str:
    text = str(action or "").lower()
    if skill in _SOCIAL_SKILLS:
        return "社交"
    if skill == "sleight_of_hand" and any(k in text for k in ("开锁", "撬")):
        return "探索"
    return "探索"


def rule_only_answers(state: dict[str, Any], action: str,
                      questions: list[Question],
                      rules: dict[str, Any] | None = None) -> dict[str, Any]:
    """纯规则路径：不调用模型，直接由检定规则表合成回答。"""
    table = rules or check_rules.load_rules()
    hint = str(state.get("skill_hint") or "")
    lookup = check_rules.lookup(action, skill_hint=hint, rules=table)
    matched = lookup["source"] in ("check_rules", "skill_name", "skill_keyword", "skill_hint")

    labels = skill_labels(table)
    skill_label = lookup["skill_name"] if lookup["skill"] in table["skills"] else (labels[0] if labels else "")
    band_label = next((lab for lab, key in _BAND_BY_LABEL.items() if key == lookup["band"]),
                      table.get("band_labels", ["普通(15)"])[1])
    party = [str(n) for n in (state.get("acting_options") or [])] or ["(唯一角色)"]
    actor = str(state.get("acting_default") or party[0])
    targets = [str(t) for t in (state.get("targets") or [])]
    target = str(state.get("target_default") or (targets[0] if targets else NO_TARGET))
    if target not in targets:
        target = NO_TARGET

    values: dict[str, Any] = {
        "intent": _rule_intent(lookup["skill"], action) if matched else "探索",
        "acting_character": actor,
        "requires_check": 1.0 if matched else 0.0,
        "check_skill": skill_label,
        "dc_band": band_label,
        "advantage": "普通",
        "target": target,
        "rule_lookup": 0.0,
        "module_conflict": 0.0,
    }
    return {q.id: {"value": values.get(q.id), "confidence": 1.0} for q in questions}


def module_pin_by_keyword(state: dict[str, Any], action: str) -> tuple[str, int, str] | None:
    """按 `match` 关键词钉住（最具体，不依赖技能判断）。"""
    for entry in [e for e in (state.get("module_dcs") or []) if isinstance(e, dict)]:
        keyword = str(entry.get("match") or "")
        if keyword and keyword in str(action):
            return (str(entry.get("skill") or ""),
                    int(entry.get("dc", 15)),
                    str(entry.get("note") or keyword))
    return None


def module_pin_by_skill(state: dict[str, Any], skill: str) -> tuple[str, int, str] | None:
    """按技能相等钉住。"""
    if not skill:
        return None
    for entry in [e for e in (state.get("module_dcs") or []) if isinstance(e, dict)]:
        if str(entry.get("skill") or "") == skill:
            return (skill, int(entry.get("dc", 15)),
                    str(entry.get("note") or skill))
    return None


def module_pin(state: dict[str, Any], action: str,
               skill: str = "") -> tuple[str, int, str] | None:
    """模组原文钉住（关键词优先，其次技能相等）。返回 (skill, dc, 说明)。"""
    return module_pin_by_keyword(state, action) or module_pin_by_skill(state, skill)


def explicit_table_skill(action: str, rules: dict[str, Any]) -> str:
    """本地规则表的**显式**命中（动作关键词或技能名），视为高置信依据。"""
    lookup = check_rules.lookup(action, rules=rules)
    if lookup["source"] in ("check_rules", "skill_name"):
        return str(lookup["skill"])
    return ""


def resolve_dc(state: dict[str, Any], action: str, skill: str, band_label: str,
               rules: dict[str, Any]) -> tuple[int, str, list[str]]:
    """DC 解析链：module > check_rules > model_band > default。"""
    chain: list[str] = []

    for entry in state.get("module_dcs") or []:
        if not isinstance(entry, dict):
            continue
        entry_skill = str(entry.get("skill") or "")
        keyword = str(entry.get("match") or "")
        if (skill and entry_skill == skill) or (keyword and keyword in str(action)):
            chain.append(f"module:{entry.get('note') or entry_skill}")
            return int(entry.get("dc", 15)), "module", chain
    chain.append("module:miss")

    lookup = check_rules.lookup(action, skill_hint=skill, rules=rules)
    if lookup["source"] in ("check_rules", "skill_name") and lookup["dc"]:
        chain.append(f"check_rules:{lookup['band']}")
        return int(lookup["dc"]), "check_rules", chain
    if lookup["source"] in ("skill_keyword", "skill_hint") and lookup["dc"]:
        chain.append(f"skill_default:{lookup['band']}")
        return int(lookup["dc"]), "skill_default", chain
    chain.append("check_rules:miss")

    band_key = _BAND_BY_LABEL.get(band_label, "")
    model_dc = check_rules.band_dc(band_key, rules) if band_key else None
    if model_dc:
        chain.append(f"model_band:{band_key}")
        return int(model_dc), "model_band", chain

    default = check_rules.band_dc(rules.get("default_band", "normal"), rules) or 15
    chain.append("default")
    return int(default), "default", chain


def compose(state: dict[str, Any], action: str, answers: dict[str, Any],
            rules: dict[str, Any] | None = None,
            floor: float = DEFAULT_CONFIDENCE_FLOOR,
            floors: dict[str, float] | None = None) -> DecisionPacket:
    """用代码组合判定结果；低置信字段回退本地依据，必要时标记 escalate。"""
    table = rules or check_rules.load_rules()
    thresholds = dict(DEFAULT_FLOOR_OVERRIDES)
    if floors:
        thresholds.update(floors)
    packet = DecisionPacket()
    low: list[str] = []

    def floor_for(qid: str) -> float:
        return float(thresholds.get(qid, floor))

    def usable(qid: str) -> bool:
        answer = answers.get(qid)
        if answer is None:
            return False
        if answer.confidence is not None and answer.confidence < floor_for(qid):
            low.append(qid)
            return False
        return True

    def value(qid: str, fallback: Any) -> Any:
        answer = answers.get(qid)
        return answer.value if (answer is not None and usable(qid)) else fallback

    packet.intent = str(value("intent", "探索"))
    packet.acting_character = str(value("acting_character", "") or (state.get("acting_default") or ""))
    packet.advantage = str(value("advantage", "普通"))
    packet.target = str(value("target", NO_TARGET))
    packet.rule_lookup_needed = bool(answers["rule_lookup"].assertive) if usable("rule_lookup") else False
    packet.module_conflict = bool(answers["module_conflict"].assertive) if usable("module_conflict") else False

    # 是否要检定：
    #   - 模型表态（未被门控）时以模型为准（它能识别转述/提问/推测/玩笑这类伪动作）
    #   - 模型未表态（置信度不足）时，才用规则表强命中补位
    table_skill = explicit_table_skill(action, table)
    check_answer = answers.get("requires_check")
    if usable("requires_check"):
        packet.requires_check = bool(check_answer.assertive)
        check_source = "model"
    elif table_skill:
        packet.requires_check = True
        check_source = "table"
    else:
        packet.requires_check = False
        check_source = "none"

    if packet.requires_check:
        # 技能优先级：模组关键词钉住 > 规则表强命中 > 模型（高置信）> 模型（低置信，总比空白好）
        pin = module_pin_by_keyword(state, action)
        skill_answer = answers.get("check_skill")
        raw_label = str(skill_answer.value) if skill_answer is not None else ""
        model_skill = label_to_skill(raw_label, table) if usable("check_skill") else ""
        lowconf_skill = label_to_skill(raw_label, table)
        if pin and pin[0]:
            packet.skill = pin[0]
            skill_source = "module"
        else:
            packet.skill = table_skill or model_skill or lowconf_skill
            if table_skill:
                skill_source = "table"
            elif model_skill:
                skill_source = "model"
            elif lowconf_skill:
                skill_source = "model_lowconf"
            else:
                skill_source = "none"
            if not pin:
                pin = module_pin_by_skill(state, packet.skill)
                if pin:
                    skill_source = "module"
        if pin:
            if pin[0]:
                packet.skill = pin[0]
                skill_source = "module"
            packet.dc = pin[1]
            packet.dc_source = "module"
            packet.fallback_chain = [f"check:{check_source}", f"skill:{skill_source}",
                                     f"module:{pin[2]}"]
        else:
            band_label = str(value("dc_band", ""))
            packet.dc, packet.dc_source, chain = resolve_dc(
                state, action, packet.skill, band_label, table,
            )
            packet.fallback_chain = [f"check:{check_source}", f"skill:{skill_source}"] + chain
        packet.ability = str((check_rules.skill_info(packet.skill, table) or {}).get("ability", ""))
    else:
        packet.fallback_chain = ["no_check"]

    packet.low_confidence_fields = sorted(set(low))
    packet.escalation_reasons = _escalation_reasons(packet)
    packet.escalate = bool(packet.escalation_reasons)
    packet.notes = (
        f"{packet.acting_character} 的{packet.intent}行动 → "
        + (f"{packet.skill or '?'} 检定 DC {packet.dc}（来源 {packet.dc_source}）" if packet.requires_check
           else "无需检定")
    )
    return packet


def _escalation_reasons(packet: DecisionPacket) -> list[str]:
    reasons: list[str] = []
    if packet.module_conflict:
        reasons.append("与已知模组事实冲突")
    if packet.requires_check:
        if not packet.skill:
            reasons.append("需要检定但技能未确定")
        if packet.dc_source in ("default", "skill_default"):
            reasons.append("DC 无明确依据，仅用了默认档")
    for field in packet.low_confidence_fields:
        if field in _CRITICAL_FIELDS:
            reasons.append(f"{field} 置信度不足（已回退本地依据）")
    if packet.rule_lookup_needed:
        reasons.append("需查规则书确认机制")
    return reasons


def run(state: dict[str, Any], action: str,
        answers_provider: AnswersProvider | None = None,
        rules: dict[str, Any] | None = None,
        floor: float = DEFAULT_CONFIDENCE_FLOOR,
        floors: dict[str, float] | None = None) -> DecisionPacket:
    """执行一轮判定。answers_provider 返回 {"answers": {...}} 或直接 {...}。"""
    table = rules or check_rules.load_rules()
    questions = build_questions(state, action, table)

    if answers_provider is None:
        raw = rule_only_answers(state, action, questions, table)
        return compose(state, action, validate_answers(raw, questions), table, floor, floors)

    try:
        raw = answers_provider(questions, state, action)
        payload = raw.get("answers") if isinstance(raw, dict) and "answers" in raw else raw
        return compose(state, action, validate_answers(payload, questions), table, floor, floors)
    except AnswerError as first_error:
        # 一次修复尝试；仍失败则回退到纯规则路径（含原因记录）
        try:
            raw = answers_provider(questions, state, action, str(first_error))
            payload = raw.get("answers") if isinstance(raw, dict) and "answers" in raw else raw
            packet = compose(state, action, validate_answers(payload, questions), table, floor, floors)
            packet.notes += f" | 修复后通过（原错误：{first_error}）"
            return packet
        except (AnswerError, TypeError) as second_error:
            fallback = compose(
                state, action,
                validate_answers(rule_only_answers(state, action, questions, table), questions),
                table, floor, floors,
            )
            fallback.fallback_chain.insert(0, f"contract_error:{first_error}")
            fallback.notes += f" | 契约非法，已回退本地规则（{second_error}）"
            return fallback
