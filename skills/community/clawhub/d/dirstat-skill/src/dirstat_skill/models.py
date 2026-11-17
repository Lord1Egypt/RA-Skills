from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EngineInfo:
    binary: str
    resolved_path: Path


@dataclass(frozen=True)
class NormalizedNode:
    path: str
    name: str
    is_dir: bool
    asize: int
    dsize: int


@dataclass(frozen=True)
class ParsedExport:
    root_path: str
    nodes: list[NormalizedNode]


@dataclass(frozen=True)
class RawExportMetadata:
    engine_name: str
    root_paths: list[str]


@dataclass(frozen=True)
class AnalysisFinding:
    path: str
    dsize: int
    is_dir: bool
    analysis_kind: str
    attention_level: str
    review_reason: str
    evidence: str
    dependency_check_confidence: str
    selection_source: str
    group_key: str
    configured_dominant_percent: float
