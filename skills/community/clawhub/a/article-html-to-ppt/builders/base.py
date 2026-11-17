from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Protocol

SupportLevel = Literal["full", "partial", "visual_only", "unsupported", "unknown"]


@dataclass
class BuilderCapability:
    name: str
    available: bool
    version: str | None = None
    command: str | None = None
    features: dict[str, bool | str] = field(default_factory=dict)
    components: dict[str, SupportLevel] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class BuildPlan:
    builder: str
    slides: list[dict[str, Any]] = field(default_factory=list)
    unsupported_objects: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    style_contract: dict[str, Any] = field(default_factory=dict)


@dataclass
class BuildResult:
    builder: str
    status: str
    pptx: str | None = None
    object_results: list[dict[str, Any]] = field(default_factory=list)
    fallbacks: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[dict[str, Any] | str] = field(default_factory=list)


@dataclass
class BuildInspection:
    builder: str
    status: str
    issues: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[dict[str, Any] | str] = field(default_factory=list)


@dataclass
class BuilderSelection:
    requested: str
    selected: str
    version: str | None
    selection_score: float
    selection_reasons: list[str]
    candidates: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "requested": self.requested,
            "selected": self.selected,
            "version": self.version,
            "selection_score": self.selection_score,
            "selection_reasons": self.selection_reasons,
            "candidates": self.candidates,
            "warnings": self.warnings,
            "errors": self.errors,
        }


class BuilderAdapter(Protocol):
    name: str

    def probe(self) -> BuilderCapability:
        ...

    def supports(self, component_type: str, delivery_route: str) -> SupportLevel:
        ...

    def plan(self, ppt_ir: dict[str, Any], style_contract: dict[str, Any], delivery_plan: dict[str, Any]) -> BuildPlan:
        ...

    def build(self, build_plan: BuildPlan, output_dir: Path) -> BuildResult:
        ...

    def inspect_output(self, pptx_path: Path) -> BuildInspection:
        ...
