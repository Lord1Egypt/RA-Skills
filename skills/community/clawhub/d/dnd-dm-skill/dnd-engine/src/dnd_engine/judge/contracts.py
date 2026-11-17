"""判定层契约：类型化提问与类型化回答（纯数据，零依赖）。

借鉴 TypeSafe AI 的 System One 思路：把"机械判定"表达成原子问题，
由模型（或本地规则表）给出类型化答案，再由引擎代码组合成 DecisionPacket。
本模块不调用任何模型，只定义契约与校验。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

QUESTION_TYPES = ("choice", "score", "noul")

# 置信度门控阈值：低于此值的字段不采信，回退到本地规则
DEFAULT_CONFIDENCE_FLOOR = 0.60

# 关键字段的更严门限（可被调用方覆盖）
DEFAULT_FLOOR_OVERRIDES: dict[str, float] = {
    "requires_check": 0.55,
    "check_skill": 0.70,
    "dc_band": 0.75,
    "acting_character": 0.55,
}


class AnswerError(ValueError):
    """回答不符合契约（用于触发一次修复或回退）。"""


@dataclass(slots=True)
class Question:
    """一个原子判定问题。"""

    id: str
    type: str
    instructions: str
    criteria: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.type not in QUESTION_TYPES:
            raise ValueError(f"unsupported question type: {self.type}")
        if not self.id or not self.id.replace("_", "").isalnum():
            raise ValueError(f"invalid question id: {self.id!r}")
        if self.type in ("choice", "score") and not self.criteria:
            raise ValueError(f"{self.type} question requires criteria: {self.id}")

    def to_json(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"id": self.id, "type": self.type,
                                   "instructions": self.instructions}
        if self.criteria:
            payload["criteria"] = list(self.criteria)
        return payload


@dataclass(slots=True)
class Answer:
    """类型化回答。value 语义：choice=选项字符串；score=档位字符串；noul=0..1。"""

    id: str
    type: str
    value: Any
    probabilities: dict[str, float] | None = None
    confidence: float | None = None

    @property
    def assertive(self) -> bool:
        """noul 是否判为成立（>=0.5）。"""
        try:
            return float(self.value) >= 0.5
        except (TypeError, ValueError):
            return False


def validate_answer(raw: Any, question: Question) -> Answer:
    """严格校验一个回答；不符合契约时抛 AnswerError。"""
    if not isinstance(raw, dict):
        raise AnswerError(f"{question.id}: answer must be an object")
    if raw.get("type") not in (None, question.type):
        raise AnswerError(f"{question.id}: type mismatch")
    value = raw.get("value", raw.get("choice", raw.get("score", raw.get("noul"))))
    if value is None and "value" not in raw:
        raise AnswerError(f"{question.id}: missing value")

    if question.type in ("choice", "score"):
        text = str(value).strip()
        if text not in question.criteria:
            raise AnswerError(f"{question.id}: {text!r} is not one of {question.criteria}")
        value = text
    else:  # noul
        try:
            value = float(value)
        except (TypeError, ValueError) as exc:
            raise AnswerError(f"{question.id}: noul must be numeric") from exc
        if not 0.0 <= value <= 1.0:
            raise AnswerError(f"{question.id}: noul must be within 0..1")

    confidence = raw.get("confidence")
    if confidence is not None:
        try:
            confidence = float(confidence)
        except (TypeError, ValueError) as exc:
            raise AnswerError(f"{question.id}: confidence must be numeric") from exc
        if not 0.0 <= confidence <= 1.0:
            raise AnswerError(f"{question.id}: confidence must be within 0..1")

    probabilities = raw.get("probabilities")
    if probabilities is not None and not isinstance(probabilities, dict):
        raise AnswerError(f"{question.id}: probabilities must be an object")

    return Answer(id=question.id, type=question.type, value=value,
                  probabilities=probabilities, confidence=confidence)


def validate_answers(raw_answers: Any, questions: list[Question]) -> dict[str, Answer]:
    """批量校验；任一缺失/非法即抛错（供修复回路捕获）。"""
    if not isinstance(raw_answers, dict):
        raise AnswerError("answers must be an object keyed by question id")
    parsed: dict[str, Answer] = {}
    for question in questions:
        if question.id not in raw_answers:
            raise AnswerError(f"{question.id}: answer missing")
        parsed[question.id] = validate_answer(raw_answers[question.id], question)
    return parsed


def answer_json_schema(questions: list[Question]) -> dict[str, Any]:
    """给"强制结构化输出"用的 JSON Schema（可直接塞进 response_format）。"""
    properties: dict[str, Any] = {}
    for question in questions:
        if question.type in ("choice", "score"):
            value_schema: dict[str, Any] = {"type": "string", "enum": list(question.criteria)}
        else:
            value_schema = {"type": "number", "minimum": 0, "maximum": 1}
        properties[question.id] = {
            "type": "object",
            "properties": {
                "value": value_schema,
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            },
            "required": ["value"],
            "additionalProperties": False,
        }
    return {
        "type": "object",
        "properties": {"answers": {"type": "object", "properties": properties,
                                   "required": list(properties),
                                   "additionalProperties": False}},
        "required": ["answers"],
        "additionalProperties": False,
    }


@dataclass(slots=True)
class DecisionPacket:
    """一轮交互的判定结果（由引擎代码组合，非模型产出）。"""

    acting_character: str = ""
    intent: str = ""
    requires_check: bool = False
    ability: str = ""
    skill: str = ""
    dc: int = 0
    dc_source: str = ""
    advantage: str = "none"
    target: str = ""
    rule_lookup_needed: bool = False
    module_conflict: bool = False
    low_confidence_fields: list[str] = field(default_factory=list)
    fallback_chain: list[str] = field(default_factory=list)
    escalate: bool = False
    escalation_reasons: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "acting_character": self.acting_character,
            "intent": self.intent,
            "requires_check": self.requires_check,
            "ability": self.ability,
            "skill": self.skill,
            "dc": self.dc,
            "dc_source": self.dc_source,
            "advantage": self.advantage,
            "target": self.target,
            "rule_lookup_needed": self.rule_lookup_needed,
            "module_conflict": self.module_conflict,
            "low_confidence_fields": list(self.low_confidence_fields),
            "fallback_chain": list(self.fallback_chain),
            "escalate": self.escalate,
            "escalation_reasons": list(self.escalation_reasons),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DecisionPacket":
        """从 to_dict() 的结果重建（用于把判定包带过 HTTP 边界后再修正）。"""
        data = payload or {}
        return cls(
            acting_character=str(data.get("acting_character") or ""),
            intent=str(data.get("intent") or ""),
            requires_check=bool(data.get("requires_check", False)),
            ability=str(data.get("ability") or ""),
            skill=str(data.get("skill") or ""),
            dc=int(data.get("dc") or 0),
            dc_source=str(data.get("dc_source") or ""),
            advantage=str(data.get("advantage") or "none"),
            target=str(data.get("target") or ""),
            rule_lookup_needed=bool(data.get("rule_lookup_needed", False)),
            module_conflict=bool(data.get("module_conflict", False)),
            low_confidence_fields=list(data.get("low_confidence_fields") or []),
            fallback_chain=list(data.get("fallback_chain") or []),
            escalate=bool(data.get("escalate", False)),
            escalation_reasons=list(data.get("escalation_reasons") or []),
            notes=str(data.get("notes") or ""),
        )
