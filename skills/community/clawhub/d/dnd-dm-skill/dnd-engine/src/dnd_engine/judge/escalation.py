"""把 escalate 接到"人工确认 / 玩家澄清"。

判定层不自行猜：当判定存在风险（与模组冲突、DC 无依据、关键字段低置信…）时，
产出可展示的澄清请求，交给玩家或城主确认，再用确认结果修正判定包。

支持**逐字段**澄清：一次可以同时问"用哪项技能"和"难度按哪一档"。
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from . import check_rules
from .contracts import DecisionPacket
from .judge import module_pin, resolve_dc
from .questions import label_to_skill, skill_labels

GM_REASONS = ("与已知模组事实冲突", "需查规则书确认机制")
CONFIRM_LABEL = "按裁定执行"
DM_LABEL = "改由城主裁定"
FIELD_TEXT = {
    "check_skill": "技能",
    "dc_band": "难度档",
    "requires_check": "是否需要检定",
    "acting_character": "执行角色",
    "advantage": "优势/劣势",
}


@dataclass(slots=True)
class ClarificationRequest:
    kind: str            # player_choice | gm_confirm
    reason: str
    question: str
    options: list[str]
    field: str           # 需要澄清的字段：check_skill | dc_band | requires_check | ... | ""（整体确认）

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "reason": self.reason,
            "question": self.question,
            "options": list(self.options),
            "field": self.field,
        }


def _kind(reasons: list[str]) -> str:
    return "gm_confirm" if any(r.startswith(GM_REASONS) for r in reasons) else "player_choice"


def build_clarifications(packet: DecisionPacket, state: dict[str, Any] | None = None,
                         rules: dict[str, Any] | None = None) -> list[ClarificationRequest]:
    """按升级原因生成**逐字段**澄清请求；无升级则返回空列表。"""
    if not packet.escalate:
        return []
    table = rules or check_rules.load_rules()
    reasons = list(packet.escalation_reasons)
    kind = _kind(reasons)
    reason = reasons[0] if reasons else "判定不确定"
    requests: list[ClarificationRequest] = []

    # 以“低置信字段”为主线索逐字段提问（不依赖原因文本的字面措辞）
    fields: list[str] = list(packet.low_confidence_fields)
    if packet.requires_check and not packet.skill and "check_skill" not in fields:
        fields.append("check_skill")
    if packet.requires_check and packet.dc_source in ("default", "skill_default") \
            and "dc_band" not in fields:
        fields.append("dc_band")

    seen: set[str] = set()
    for field in fields:
        if field in seen:
            continue
        seen.add(field)
        if field == "check_skill":
            requests.append(ClarificationRequest(
                kind, reason, f"{packet.acting_character} 这个动作用哪一项技能？",
                skill_labels(table), "check_skill"))
        elif field == "dc_band":
            requests.append(ClarificationRequest(
                kind, reason, "这项检定的难度按哪一档？",
                [str(b) for b in table.get("band_labels", [])], "dc_band"))
        else:
            requests.append(ClarificationRequest(
                kind, reason, f"确认一下：{FIELD_TEXT.get(field, field)}？",
                [CONFIRM_LABEL, DM_LABEL], field))

    if not requests:
        requests.append(ClarificationRequest(
            kind, reason, "本次判定需要确认，按原判定继续吗？",
            [CONFIRM_LABEL, DM_LABEL], ""))
    return requests


def build_clarification(packet: DecisionPacket, state: dict[str, Any] | None = None,
                        rules: dict[str, Any] | None = None) -> ClarificationRequest | None:
    """只取最优先的一条（兼容旧调用）。"""
    requests = build_clarifications(packet, state, rules)
    return requests[0] if requests else None


def render_clarification(request: ClarificationRequest) -> str:
    who = "【需城主确认】" if request.kind == "gm_confirm" else "【需要你确认】"
    lines = [f"{who} {request.question}", f"（原因：{request.reason}）"]
    for index, option in enumerate(request.options, start=1):
        lines.append(f"  {index}. {option}")
    return "\n".join(lines)


def render_clarifications(requests: list[ClarificationRequest]) -> str:
    return "\n\n".join(render_clarification(item) for item in requests)


def _apply_value(updated: DecisionPacket, state: dict[str, Any], action: str,
                 choice: str, table: dict[str, Any]) -> None:
    """按取值类型修正：技能名 / 难度档 / 确认。"""
    choice = str(choice or "").strip()
    if choice in skill_labels(table):
        updated.requires_check = True
        updated.skill = label_to_skill(choice, table)
        updated.ability = str((check_rules.skill_info(updated.skill, table) or {}).get("ability", ""))
        pin = module_pin(state, action, updated.skill)
        if pin:
            updated.skill, updated.dc, updated.dc_source = pin[0] or updated.skill, pin[1], "module"
            updated.fallback_chain = ["check:module", "skill:module", f"module:{pin[2]}"]
        else:
            updated.dc, updated.dc_source, updated.fallback_chain = resolve_dc(
                state, action, updated.skill, "", table)
    elif choice in [str(b) for b in table.get("band_labels", [])]:
        updated.dc, updated.dc_source, updated.fallback_chain = resolve_dc(
            state, action, updated.skill, choice, table)
        if not updated.dc_source.endswith("default"):
            updated.dc_source = "clarified_band"


def apply_clarifications(packet: DecisionPacket, state: dict[str, Any], action: str,
                         choices: dict[str, str], rules: dict[str, Any] | None = None,
                         fields: list[str] | None = None) -> DecisionPacket:
    """用（可多字段的）澄清结果修正判定包；已解决的原因会被移除。

    choices: {字段: 取值}；若只给一个值而不给字段，按取值类型自动识别。
    """
    table = rules or check_rules.load_rules()
    updated = replace(packet, escalation_reasons=list(packet.escalation_reasons),
                      low_confidence_fields=list(packet.low_confidence_fields))

    if choices and all(not key for key in choices):
        values = list(choices.values())
    else:
        values = list(choices.values())

    for value in values:
        _apply_value(updated, state, action, value, table)

    if fields:
        remaining_low = [f for f in updated.low_confidence_fields if f not in fields]
    else:
        remaining_low = [f for f in updated.low_confidence_fields
                         if f not in ("check_skill", "dc_band")] if values else updated.low_confidence_fields
    updated.low_confidence_fields = remaining_low

    # GM 类原因（模组冲突/需查规则）保留，其余视为已处理
    updated.escalation_reasons = [r for r in updated.escalation_reasons
                                  if r.startswith(GM_REASONS)]
    updated.escalate = bool(updated.escalation_reasons)
    label = "、".join(str(v) for v in values) or "确认"
    updated.notes += f" | 已按澄清修正（{label}）"
    return updated


def apply_clarification(packet: DecisionPacket, state: dict[str, Any], action: str,
                        choice: str, rules: dict[str, Any] | None = None) -> DecisionPacket:
    """单字段澄清（兼容旧调用）：取值类型自动识别。"""
    return apply_clarifications(packet, state, action, {"": choice}, rules)
