"""类型化判定层（judge）。

借鉴 TypeSafe AI 的 System One 思路：批量原子提问 → 类型化回答 → 代码组合成决策，
再由 bridge 直接结算成引擎检定明细。

公开 API：
    from dnd_engine.judge import run, resolve_packet, render, run_batch, resolve_batch
"""

from .batch import build_batch_questions, render_round, resolve_batch, run_batch
from .bridge import CheckOutcome, build_components, render, resolve_packet
from .contracts import (
    DEFAULT_CONFIDENCE_FLOOR,
    DEFAULT_FLOOR_OVERRIDES,
    Answer,
    AnswerError,
    DecisionPacket,
    Question,
    answer_json_schema,
    validate_answer,
    validate_answers,
)
from .escalation import (
    ClarificationRequest,
    apply_clarification,
    apply_clarifications,
    build_clarification,
    build_clarifications,
    render_clarification,
    render_clarifications,
)
from .judge import compose, module_pin, resolve_dc, rule_only_answers, run
from .module_data import (
    dcs_for_scene as load_module_dcs,
    enemy_profiles,
    load_encounters,
    scene_titles,
)
from .providers import HttpQuestionsProvider, describe_providers, resolve_provider
from .questions import build_questions

__all__ = [
    "Answer",
    "AnswerError",
    "CheckOutcome",
    "ClarificationRequest",
    "DEFAULT_CONFIDENCE_FLOOR",
    "DEFAULT_FLOOR_OVERRIDES",
    "DecisionPacket",
    "HttpQuestionsProvider",
    "Question",
    "answer_json_schema",
    "apply_clarification",
    "apply_clarifications",
    "build_batch_questions",
    "build_clarification",
    "build_clarifications",
    "build_components",
    "build_questions",
    "compose",
    "describe_providers",
    "enemy_profiles",
    "load_encounters",
    "load_module_dcs",
    "module_pin",
    "render",
    "render_clarification",
    "render_clarifications",
    "render_round",
    "resolve_batch",
    "resolve_dc",
    "resolve_packet",
    "resolve_provider",
    "rule_only_answers",
    "run",
    "run_batch",
    "scene_titles",
    "validate_answer",
    "validate_answers",
]
