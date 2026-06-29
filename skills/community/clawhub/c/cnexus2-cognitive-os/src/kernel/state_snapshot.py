"""State snapshot — immutable. Mirrors core_essence/04_data_model_essence.md §3."""
from dataclasses import dataclass, field
from typing import Dict

@dataclass(frozen=True)
class EmotionSnapshot:
    val: float = 0.0
    arousal: float = 0.5
    dominance: float = 0.5

@dataclass(frozen=True)
class StateSnapshot:
    emotion: EmotionSnapshot = field(default_factory=EmotionSnapshot)
    relationship: Dict = field(default_factory=lambda: dict(tone=0.0, trust=0.5, familiarity=0.3))
    goal: Dict = field(default_factory=lambda: dict(current="converse", progress=0.0))
    attention: Dict = field(default_factory=lambda: dict(focus="general", level=0.5))
    meta: Dict = field(default_factory=lambda: dict(session_count=0, total_interactions=1))
