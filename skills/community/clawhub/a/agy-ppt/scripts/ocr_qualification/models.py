"""Immutable, deterministic Phase 15.6 qualification results."""
from __future__ import annotations

from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any, Mapping


STATUSES = frozenset({"PASS", "FAIL", "SKIPPED", "ENVIRONMENT_REQUIRED"})


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


@dataclass(frozen=True)
class QualificationCase:
    case_id: str
    status: str
    evidence: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.case_id, str) or not self.case_id or self.case_id != self.case_id.strip():
            raise ValueError("qualification case_id must be stable and non-empty")
        if self.status not in STATUSES:
            raise ValueError("qualification status is invalid")
        if not isinstance(self.evidence, Mapping):
            raise ValueError("qualification evidence must be a mapping")
        object.__setattr__(self, "evidence", _freeze(self.evidence))

    def to_dict(self) -> dict[str, Any]:
        return {"case_id": self.case_id, "evidence": _plain(self.evidence), "status": self.status}


@dataclass(frozen=True)
class QualificationReport:
    schema_version: str
    baseline_sha: str
    runtime: Mapping[str, Any]
    platform: Mapping[str, Any]
    cases: tuple[QualificationCase, ...]
    release_readiness: str
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "phase15.6-internal/1" or len(self.baseline_sha) != 40:
            raise ValueError("qualification report identity is invalid")
        object.__setattr__(self, "runtime", _freeze(self.runtime))
        object.__setattr__(self, "platform", _freeze(self.platform))
        object.__setattr__(self, "cases", tuple(self.cases))
        object.__setattr__(self, "limitations", tuple(self.limitations))
        if not self.cases or any(not isinstance(case, QualificationCase) for case in self.cases):
            raise ValueError("qualification report requires cases")
        if len({case.case_id for case in self.cases}) != len(self.cases):
            raise ValueError("qualification case ids must be unique")
        if tuple(case.case_id for case in self.cases) != tuple(sorted(case.case_id for case in self.cases)):
            raise ValueError("qualification cases must be sorted")
        if self.release_readiness not in {
            "RELEASE READY", "RELEASE READY WITH DOCUMENTED PLATFORM LIMITATIONS", "RELEASE BLOCKED",
        }:
            raise ValueError("release readiness is invalid")

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_sha": self.baseline_sha,
            "cases": [case.to_dict() for case in self.cases],
            "limitations": list(self.limitations),
            "platform": _plain(self.platform),
            "release_readiness": self.release_readiness,
            "runtime": _plain(self.runtime),
            "schema_version": self.schema_version,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
