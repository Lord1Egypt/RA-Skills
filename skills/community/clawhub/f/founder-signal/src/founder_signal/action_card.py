"""Founder-reviewable action card generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .models import RedditEvidenceReadResult, StructuredRedditEvidence
from .scoring import VERIFIED_READ_STATUSES

_DAILY_REVIEW_FILENAME = "daily-review.md"
_MAX_DRAFT_WORDS = 180
_MAX_BODY_EXCERPT_SENTENCES = 2
_MAX_BODY_EXCERPT_WORDS = 55


@dataclass(frozen=True)
class SelectedCandidate:
    """Normalized candidate payload for action card generation."""

    source_url: str
    evidence_url: str
    read_status: str
    evidence_snapshot_path: Path
    candidate_id: str = ""
    source_platform: str = "reddit"
    structured_evidence_path: Path | None = None
    structured_evidence: StructuredRedditEvidence | None = None
    agent_review: dict[str, Any] | None = None
    selection_eligible: bool | None = None
    selection_gate_reason: str = ""
    rejection_signals: tuple[str, ...] = ()

    @classmethod
    def from_input(cls, selected_candidate: Any) -> "SelectedCandidate | None":
        if isinstance(selected_candidate, cls):
            return selected_candidate
        if isinstance(selected_candidate, RedditEvidenceReadResult):
            return cls(
                source_url=selected_candidate.source_url,
                evidence_url=selected_candidate.evidence_url,
                read_status=selected_candidate.status,
                evidence_snapshot_path=selected_candidate.text_snapshot_path,
                candidate_id=selected_candidate.candidate_id,
                source_platform=selected_candidate.platform,
                structured_evidence_path=selected_candidate.structured_evidence_path,
                structured_evidence=selected_candidate.structured_evidence,
            )
        if isinstance(selected_candidate, (str, Path)):
            candidate_path = Path(selected_candidate)
            if not candidate_path.exists():
                return None
            payload = json.loads(candidate_path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                return None
            return cls.from_mapping(payload, base_dir=candidate_path.parent)
        if isinstance(selected_candidate, dict):
            return cls.from_mapping(selected_candidate)
        return cls.from_mapping(_object_to_mapping(selected_candidate))

    @classmethod
    def from_mapping(
        cls, payload: dict[str, Any], *, base_dir: Path | None = None
    ) -> "SelectedCandidate | None":
        source_url = _first_string(payload, "source_url", "reddit_url")
        evidence_url = _first_string(payload, "evidence_url")
        read_status = _first_string(payload, "read_status", "status")
        snapshot_value = _first_string(payload, "evidence_snapshot_path", "text_snapshot_path")
        if not source_url or not evidence_url or not read_status or not snapshot_value:
            return None

        snapshot_path = Path(snapshot_value)
        if base_dir is not None and not snapshot_path.is_absolute():
            snapshot_path = (base_dir / snapshot_path).resolve()

        structured_path = _optional_path(payload, "structured_evidence_path", base_dir=base_dir)
        structured_evidence = _structured_evidence_from_payload(
            payload.get("structured_evidence"),
            snapshot_path,
            structured_path,
        )

        return cls(
            source_url=source_url,
            evidence_url=evidence_url,
            read_status=read_status,
            evidence_snapshot_path=snapshot_path,
            candidate_id=_first_string(payload, "candidate_id"),
            source_platform=_first_string(payload, "source_platform", "platform") or "reddit",
            structured_evidence_path=structured_path,
            structured_evidence=structured_evidence,
            agent_review=_mapping_or_none(payload.get("agent_review")),
            selection_eligible=_optional_bool(payload.get("selection_eligible")),
            selection_gate_reason=_first_string(payload, "selection_gate_reason"),
            rejection_signals=_string_tuple(payload.get("rejection_signals")),
        )

    def is_verified(self) -> bool:
        return (
            self.read_status in VERIFIED_READ_STATUSES
            and self.evidence_snapshot_path.exists()
            and self.evidence_snapshot_path.is_file()
        )

    def has_usable_structured_evidence(self) -> bool:
        evidence = self.structured_evidence
        if evidence is None:
            return False
        if evidence.extraction_quality != "high":
            return False
        if not evidence.post_title.strip() or not evidence.post_body.strip():
            return False
        return True

    def is_actionable(self) -> bool:
        review = self.agent_review or {}
        reject_reason = str(review.get("reject_reason") or "").strip()
        if reject_reason:
            return False
        if self.selection_eligible is False:
            return False
        if self.selection_gate_reason in {"agent_reject_reason", "structured_rejection_signal"}:
            return False
        if self.rejection_signals:
            return False
        return self.is_verified()

    def action_card_generation_mode(self) -> str:
        return "structured" if self.has_usable_structured_evidence() else "snapshot_fallback"


def generate_action_card(
    run_dir: Path,
    selected_candidate: Any,
    *,
    product_name: str = "",
    profile_id: str = "",
) -> Path | None:
    """Write a single founder-reviewable action card for a verified candidate."""
    candidate = SelectedCandidate.from_input(selected_candidate)
    if candidate is None or not candidate.is_verified() or not candidate.is_actionable():
        return None

    generation_mode = candidate.action_card_generation_mode()
    evidence_excerpt = _build_evidence_excerpt(candidate)
    suggested_comment = _build_comment_draft(
        candidate,
        product_name=product_name,
        agent_review=candidate.agent_review or {},
    )

    output_path = run_dir / _DAILY_REVIEW_FILENAME
    run_dir.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        _render_daily_review(
            candidate=candidate,
            evidence_excerpt=evidence_excerpt,
            suggested_comment=suggested_comment,
            generation_mode=generation_mode,
            product_name=product_name,
            profile_id=profile_id,
        ),
        encoding="utf-8",
    )
    return output_path


def _object_to_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    return {
        key: getattr(value, key)
        for key in (
            "candidate_id",
            "platform",
            "source_platform",
            "source_url",
            "reddit_url",
            "evidence_url",
            "read_status",
            "status",
            "evidence_snapshot_path",
            "text_snapshot_path",
            "structured_evidence_path",
            "structured_evidence",
            "agent_review",
            "selection_eligible",
            "selection_gate_reason",
            "rejection_signals",
        )
        if hasattr(value, key)
    }


def _first_string(payload: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = payload.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def _optional_path(payload: dict[str, Any], key: str, *, base_dir: Path | None = None) -> Path | None:
    value = _first_string(payload, key)
    if not value:
        return None
    path = Path(value)
    if base_dir is not None and not path.is_absolute():
        path = (base_dir / path).resolve()
    return path


def _mapping_or_none(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return dict(value)
    return None


def _optional_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    items = [str(item).strip() for item in value if str(item).strip()]
    return tuple(items)


def _structured_evidence_from_payload(
    payload: Any,
    snapshot_path: Path,
    structured_path: Path | None,
) -> StructuredRedditEvidence | None:
    if isinstance(payload, dict):
        return StructuredRedditEvidence(
            post_title=str(payload.get("post_title") or "").strip(),
            post_body=str(payload.get("post_body") or "").strip(),
            subreddit=str(payload.get("subreddit") or "").strip(),
            comments_excerpt=str(payload.get("comments_excerpt") or "").strip(),
            extraction_quality=str(payload.get("extraction_quality") or "").strip(),
            raw_text_snapshot=str(payload.get("raw_text_snapshot") or "").strip(),
            post_age_days=_optional_int(payload.get("post_age_days")),
        )
    for path in [path for path in (structured_path,) if path is not None]:
        if not path.exists() or not path.is_file():
            continue
        try:
            structured_payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if not isinstance(structured_payload, dict):
            continue
        try:
            raw_snapshot = snapshot_path.read_text(encoding="utf-8").strip()
        except OSError:
            raw_snapshot = ""
        return StructuredRedditEvidence(
            post_title=str(structured_payload.get("post_title") or "").strip(),
            post_body=str(structured_payload.get("post_body") or "").strip(),
            subreddit=str(structured_payload.get("subreddit") or "").strip(),
            comments_excerpt=str(structured_payload.get("comments_excerpt") or "").strip(),
            extraction_quality=str(structured_payload.get("extraction_quality") or "").strip(),
            raw_text_snapshot=str(structured_payload.get("raw_text_snapshot") or "").strip()
            or raw_snapshot,
            post_age_days=_optional_int(structured_payload.get("post_age_days")),
        )
    return None


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def action_card_generation_mode(selected_candidate: Any) -> str:
    candidate = SelectedCandidate.from_input(selected_candidate)
    if candidate is None or not candidate.is_verified() or not candidate.is_actionable():
        return ""
    return candidate.action_card_generation_mode()


def _build_evidence_excerpt(candidate: SelectedCandidate) -> str:
    evidence = candidate.structured_evidence if candidate.has_usable_structured_evidence() else None
    if evidence is None:
        title, body = _snapshot_title_and_body(candidate.evidence_snapshot_path)
        excerpt_lines = [f"> Title: {title}"] if title else []
        body_excerpt = _body_excerpt(body)
        if body_excerpt:
            excerpt_lines.append(f"> Snapshot excerpt: {body_excerpt}")
        return "\n".join(excerpt_lines)
    excerpt_lines = [f"> Title: {evidence.post_title.strip()}"]
    body_excerpt = _body_excerpt(evidence.post_body)
    if body_excerpt:
        excerpt_lines.append(f"> Body: {body_excerpt}")
    return "\n".join(excerpt_lines)


def _build_comment_draft(
    candidate: SelectedCandidate,
    *,
    product_name: str,
    agent_review: dict[str, Any],
) -> str:
    evidence = candidate.structured_evidence if candidate.has_usable_structured_evidence() else None
    if evidence is None:
        title, body = _snapshot_title_and_body(candidate.evidence_snapshot_path)
        evidence = StructuredRedditEvidence(
            post_title=title,
            post_body=body or title,
            subreddit="",
            comments_excerpt="",
            extraction_quality="fallback",
            raw_text_snapshot=body or title,
            post_age_days=None,
        )
    draft = " ".join(
        (
            _problem_statement(evidence.post_body),
            _relevance_statement(evidence, product_name=product_name, agent_review=agent_review),
            _next_step_statement(evidence.post_body),
            _closing_question(evidence.post_body),
        )
    )
    return _clip_to_word_limit(" ".join(draft.split()), _MAX_DRAFT_WORDS)


def _body_excerpt(text: str) -> str:
    sentences = _sentences(text)
    excerpt = " ".join(sentences[:_MAX_BODY_EXCERPT_SENTENCES]).strip()
    if not excerpt:
        excerpt = _normalize_text(text)
    return _clip_words(excerpt, _MAX_BODY_EXCERPT_WORDS)


def _problem_statement(post_body: str) -> str:
    first_sentence = _sentences(post_body)[:1]
    if first_sentence:
        problem = first_sentence[0].rstrip(".!?")
        return f"You mentioned {problem.lower()}."
    return "You called out a concrete workflow problem."


def _relevance_statement(
    evidence: StructuredRedditEvidence,
    *,
    product_name: str,
    agent_review: dict[str, Any],
) -> str:
    body = evidence.post_body.lower()
    combined = f"{evidence.post_title} {evidence.post_body}".lower()
    if any(term in combined for term in ("agent", "tool call", "permission", "approval", "constrained")):
        return "That reads like an operations-control problem: the useful part is not making agents more autonomous, it is deciding where they should pause and ask for review."
    if any(term in combined for term in ("export", "conversation", "backup", "download data", "pdf")):
        return "That reads like a portability problem: the useful answers are only valuable if people can keep, search, and reuse them outside the chat window."
    if "warning" in combined:
        return "That reads like a data-retention problem: the painful part is realizing important chat context can disappear or become hard to recover."
    if "markdown" in body and "search" in body:
        return "That reads like a retrieval problem more than a writing problem, especially once useful answers are buried across tools."
    rationale = str(agent_review.get("reason") or "").strip()
    if rationale:
        clipped = _clip_words(rationale, 18).rstrip(".!?")
        return f"The part that seems worth fixing first is {clipped.lower()}."
    if product_name:
        return f"This feels relevant for anyone trying to make {product_name} fit the actual workflow instead of another generic capture step."
    return "That feels like a real reuse problem, not just a note-taking preference."


def _next_step_statement(post_body: str) -> str:
    body = post_body.lower()
    if any(term in body for term in ("agent", "tool call", "permission", "approval", "constrained")):
        return "A helpful next step is to write down the two or three actions that deserve a human checkpoint, then test one approval handoff before expanding the agent's scope."
    if any(term in body for term in ("export", "conversation", "backup", "download data", "pdf")):
        return "A helpful next step is to pick one export format and one naming rule, then test whether last week's most useful chats are actually findable again."
    if "screenshot" in body or "copy" in body:
        return "A helpful next step is to test one small capture rule for a week: every answer worth keeping goes into one markdown note with the prompt, the excerpt, and one line on why it mattered."
    if "search" in body or "find" in body:
        return "A helpful next step is to save five recent wins in one place and add the same two fields to each note so you can see whether retrieval gets easier before changing the whole system."
    return "A helpful next step is to map the exact moment context gets lost, then try a tiny repeatable capture template there before redesigning the rest of the workflow."


def _closing_question(post_body: str) -> str:
    body = post_body.lower()
    if any(term in body for term in ("agent", "tool call", "permission", "approval", "constrained")):
        return "Where would you want the first review checkpoint: before tool access, before external side effects, or before final handoff?"
    if any(term in body for term in ("export", "conversation", "backup", "download data", "pdf")):
        return "Is the harder part getting a complete export, or turning the export into something searchable afterward?"
    if "search" in body or "find" in body:
        return "Which part is failing more right now: capturing the useful answer or finding it again later?"
    return "Which step feels noisiest right now when you try to reuse something good later?"


def _sentences(text: str) -> list[str]:
    compact = " ".join(_normalize_text(text).split())
    if not compact:
        return []
    return [part.strip() for part in compact.split(". ") if part.strip()]


def _clip_words(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(".,;:") + "..."


def _clip_to_word_limit(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(".,;:") + "."


def _normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines() if line.strip())


def _render_daily_review(
    *,
    candidate: SelectedCandidate,
    evidence_excerpt: str,
    suggested_comment: str,
    product_name: str,
    profile_id: str,
    generation_mode: str,
) -> str:
    why_this_matters = (
        "The source describes a concrete builder problem in the founder's own words, so a "
        "grounded reply can add value without sounding promotional."
    )
    title_suffix = f" - {product_name}" if product_name else ""
    product_lines = ""
    if product_name:
        product_lines += f"- Product: {product_name}\n"
    if profile_id:
        product_lines += f"- Profile ID: {profile_id}\n"
    return (
        f"# Founder Signal Daily Review{title_suffix}\n\n"
        "## Action 1: Comment\n\n"
        "### Source\n\n"
        f"{product_lines}"
        f"- Source platform: {candidate.source_platform}\n"
        f"- Source URL: {candidate.source_url}\n"
        f"- Evidence URL: {candidate.evidence_url}\n"
        f"- Read status: {candidate.read_status}\n"
        f"- Evidence quality: {_evidence_quality_label(generation_mode)}\n"
        "- Evidence snapshot: saved in the private local run artifacts\n\n"
        "### Why this matters\n\n"
        f"{why_this_matters}\n\n"
        "### Source evidence\n\n"
        f"{evidence_excerpt}\n\n"
        f"Cited from the saved verified evidence snapshot and source URL `{candidate.source_url}`.\n\n"
        "### Suggested comment draft\n\n"
        f"{suggested_comment}\n\n"
        "### Founder action\n\n"
        "- [ ] Accept\n"
        "- [ ] Edit\n"
        "- [ ] Reject\n"
        "- [ ] Skip\n\n"
        "### Learning note\n\n"
        "*(To be filled after founder review)*\n"
    )


def _snapshot_title_and_body(snapshot_path: Path) -> tuple[str, str]:
    try:
        snapshot = snapshot_path.read_text(encoding="utf-8")
    except OSError:
        return "", ""
    lines = [line.strip() for line in snapshot.splitlines() if line.strip()]
    if not lines:
        return "", ""
    title = _clip_words(lines[0], 18)
    body = " ".join(lines[1:]).strip() or lines[0]
    return title, body


def _evidence_quality_label(generation_mode: str) -> str:
    if generation_mode == "structured":
        return "structured extraction"
    return "fallback from raw snapshot"
