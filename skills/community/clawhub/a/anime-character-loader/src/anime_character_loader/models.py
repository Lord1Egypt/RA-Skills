"""Core data models for structured project layout."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class CharacterMatch:
    name: str
    source: str
    source_work: str
    confidence: float
    data: Dict[str, Any]
    disambiguation_note: str = ""
    cross_source_consistency: float = 0.0


@dataclass
class CrossSourceMatch:
    character_name: str
    source_work: str
    anilist_match: Optional[CharacterMatch]
    jikan_match: Optional[CharacterMatch]
    consistency_score: float
    combined_confidence: float


@dataclass
class ValidationResult:
    passed: bool
    score: float
    checks: Dict[str, Tuple[bool, str]]
    errors: List[str]
