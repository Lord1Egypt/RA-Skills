"""Agent framework: bounded LLM analysis with strict output schemas.

Contract code is treated as UNTRUSTED DATA. Agents never confirm findings:
everything they emit is llm_suggested and must pass the ValidationAgent.
Token/char budgets split large codebases into per-file/per-chunk calls, all
charged against the same per-audit LLM budget.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from agentsafe.llm.prompts import (
    BASIC_SCAN_SUFFIX,
    DEEP_DIVE_SUFFIX,
    system_prompt,
)
from agentsafe.llm.router import AuditBudget, LLMRouter
from agentsafe.schemas import Finding, FindingStatus

logger = logging.getLogger("agentSAFE.agents")

MAX_SEGMENT_CHARS = 12_000  # per LLM call, ~3k tokens of code
MAX_TOTAL_ANALYZED_CHARS = 60_000  # per agent across whole audit


class LLMFindingPayload(BaseModel):
    """Strict wire format the LLM must produce for one finding."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=300)
    severity: str
    description: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    recommendation: str = ""
    file_path: str | None = None
    line_start: int | None = Field(default=None, ge=1)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

    @field_validator("severity")
    @classmethod
    def _severity(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in {"critical", "high", "medium", "low", "info"}:
            raise ValueError(f"invalid severity: {v!r}")
        return v


class LLMFindingsPayload(BaseModel):
    """Root wire format: {"findings": [...]}."""

    model_config = ConfigDict(extra="forbid")
    findings: list[LLMFindingPayload] = Field(default_factory=list, max_length=50)


@dataclass
class AnalysisMaterial:
    """What the agents look at. Either verified source or bytecode-derived."""

    kind: str  # "source" | "bytecode"
    # For source: path -> content. For bytecode: label -> pseudo-source/disasm text.
    segments: dict[str, str]
    is_pseudo_source: bool = False
    bytecode: str | None = None

    def total_chars(self) -> int:
        return sum(len(v) for v in self.segments.values())

    def text(self) -> str:
        return "\n".join(self.segments.values())


@dataclass
class AgentResult:
    agent: str
    findings: list[Finding] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    segments_analyzed: int = 0
    skipped_reason: str | None = None


class BaseAgent:
    """One specialized LLM analyst. Subclasses set name/focus/keywords."""

    name: str = "base"
    focus: str = ""
    keywords: tuple[str, ...] = ()

    max_segment_chars: int = MAX_SEGMENT_CHARS
    max_total_chars: int = MAX_TOTAL_ANALYZED_CHARS

    def __init__(self, router: LLMRouter) -> None:
        self._router = router

    def _chunk(self, path: str, content: str) -> list[tuple[str, str]]:
        """Split oversized files at line boundaries (never mid-line silently)."""
        if len(content) <= self.max_segment_chars:
            return [(path, content)]
        chunks: list[tuple[str, str]] = []
        lines = content.splitlines(keepends=True)
        current: list[str] = []
        size = 0
        part = 0
        for line in lines:
            if size + len(line) > self.max_segment_chars and current:
                part += 1
                chunks.append((f"{path}#part{part}", "".join(current)))
                current, size = [], 0
            current.append(line)
            size += len(line)
        if current:
            part += 1
            chunks.append((f"{path}#part{part}", "".join(current)))
        return chunks

    def _user_prompt(self, label: str, text: str, deep: bool) -> str:
        notice = (
            "NOTE: the following is decompiled PSEUDO-SOURCE recovered from "
            "bytecode, NOT the original Solidity. It is an approximate "
            "representation; treat identifiers/structure as unreliable."
            if self.material_is_pseudo
            else ""
        )
        suffix = DEEP_DIVE_SUFFIX if deep else BASIC_SCAN_SUFFIX
        return f"""{notice}

{suffix}

=== UNTRUSTED CONTRACT DATA: {label} ===
{text}
=== END UNTRUSTED CONTRACT DATA ===

Audit the code above for your focus area. Respond with ONLY the strict JSON
object described in your instructions."""

    async def analyze(self, budget: AuditBudget, material: AnalysisMaterial) -> AgentResult:
        result = AgentResult(agent=self.name)
        self.material_is_pseudo = material.is_pseudo_source

        if not material.segments:
            result.skipped_reason = "no material provided"
            return result

        text = material.text()
        deep = any(kw.lower() in text.lower() for kw in self.keywords)

        work: list[tuple[str, str]] = []
        total = 0
        for path, content in material.segments.items():
            for label, chunk in self._chunk(path, content):
                if total + len(chunk) > self.max_total_chars:
                    result.errors.append(
                        f"analysis truncated: exceeded {self.max_total_chars} chars; "
                        f"unanalyzed remainder of {path}"
                    )
                    break
                work.append((label, chunk))
                total += len(chunk)

        for label, chunk in work:
            messages = [
                {"role": "system", "content": system_prompt(self.focus)},
                {"role": "user", "content": self._user_prompt(label, chunk, deep)},
            ]
            try:
                payload, call = await self._router.complete_json(
                    budget, messages, LLMFindingsPayload
                )
            except Exception as exc:  # budget/provider/schema errors are per-segment
                result.errors.append(f"{label}: {type(exc).__name__}: {exc}")
                continue
            result.segments_analyzed += 1
            for f in payload.findings:
                result.findings.append(self._to_finding(f, label, call))

        if result.errors and not result.findings and result.segments_analyzed == 0:
            result.skipped_reason = "; ".join(result.errors[:3])
        return result

    def _to_finding(self, p: LLMFindingPayload, label: str, call: Any) -> Finding:
        return Finding(
            title=p.title,
            severity=p.severity,  # type: ignore[arg-type]
            status=FindingStatus.LLM_SUGGESTED,
            source=[self.name],
            detector_id=None,
            description=p.description,
            evidence=p.evidence,
            recommendation=p.recommendation,
            file_path=p.file_path or (label.split("#part")[0] or None),
            line_start=p.line_start,
            confidence=p.confidence,
            metadata={
                "agent": self.name,
                "llm_provider": call.provider,
                "llm_model": call.model,
                "pseudo_source": self.material_is_pseudo,
            },
        )


def split_segments(files: Sequence[Any]) -> dict[str, str]:
    """SourceBundle.files -> segments dict (path -> content)."""
    return {sf.path: sf.content for sf in files}
