"""ValidationAgent: downgrades-or-cross-checks LLM hypotheses. Deterministic.

Rules (E_VERSION_PLAN Prompt 6):
- LLM findings enter as llm_suggested and may ONLY move to:
  * cross_checked - when independent, traceable evidence supports them
    (a tool finding at the same location, or overlapping evidence);
  * manual_review - otherwise.
- The ValidationAgent NEVER upgrades anything to "proven" and NEVER claims
  a contract is safe.
- Keyword screening may only reduce calls, never remove analysis classes.
"""

from __future__ import annotations

import difflib
import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass, field

from agentsafe.schemas import Finding, FindingStatus

logger = logging.getLogger("agentSAFE.validation")

EVIDENCE_SIMILARITY_THRESHOLD = 0.60
LINE_OVERLAP_TOLERANCE = 5


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _location_overlap(a: str | None, a_line: int | None, b: str | None, b_line: int | None) -> bool:
    if a and b and _norm(a) == _norm(b):
        if a_line is None or b_line is None:
            return True
        return abs(a_line - b_line) <= LINE_OVERLAP_TOLERANCE
    return False


@dataclass
class ValidationOutcome:
    findings: list[Finding] = field(default_factory=list)
    cross_checked: int = 0
    manual_review: int = 0


class ValidationAgent:
    """Cross-checks llm_suggested findings against tool_detected evidence."""

    name = "validation"

    def validate(
        self, llm_findings: Sequence[Finding], tool_findings: Sequence[Finding]
    ) -> ValidationOutcome:
        outcome = ValidationOutcome()
        for f in llm_findings:
            if f.status != FindingStatus.LLM_SUGGESTED:
                outcome.findings.append(f)
                continue
            support = self._find_support(f, tool_findings)
            if support is not None:
                merged = f.model_copy(deep=True)
                merged.status = FindingStatus.CROSS_CHECKED
                merged.metadata = {
                    **merged.metadata,
                    "validation": {
                        "supporting_source": support.source,
                        "supporting_detector": support.detector_id,
                        "supporting_location": f"{support.file_path}:{support.line_start}",
                        "evidence_similarity": round(_similar(f.evidence, support.evidence), 3),
                    },
                }
                outcome.findings.append(merged)
                outcome.cross_checked += 1
            else:
                merged = f.model_copy(deep=True)
                merged.status = FindingStatus.MANUAL_REVIEW
                merged.metadata = {
                    **merged.metadata,
                    "validation": {
                        "supporting_source": None,
                        "reason": "no independent tool evidence found; needs human review",
                    },
                }
                outcome.findings.append(merged)
                outcome.manual_review += 1
        return outcome

    def _find_support(self, candidate: Finding, tools: Sequence[Finding]) -> Finding | None:
        """Independent support = tool finding at the same location, or with
        strongly similar evidence. Traceability is preserved in metadata."""
        best: Finding | None = None
        best_score = 0.0
        for t in tools:
            if t.status == FindingStatus.MANUAL_REVIEW:
                continue
            score = 0.0
            if _location_overlap(
                candidate.file_path,
                candidate.line_start,
                t.file_path,
                t.line_start,
            ):
                score = 0.9
            else:
                # Tool findings carry their explanation in `description` as
                # well as `evidence`; support may come from either.
                sim = max(
                    _similar(candidate.evidence, t.evidence),
                    _similar(candidate.evidence, t.description),
                )
                title_sim = _similar(candidate.title, t.title)
                if sim >= EVIDENCE_SIMILARITY_THRESHOLD and title_sim >= 0.4:
                    score = sim * 0.8
            if score > best_score:
                best, best_score = t, score
        return best if best_score >= EVIDENCE_SIMILARITY_THRESHOLD else None
