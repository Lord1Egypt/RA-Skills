"""Heuristic candidate scoring for Founder Signal."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Callable, Iterable, Mapping

from .models import FounderSignalConfig, StructuredRedditEvidence

_RUBRIC_KEYS = (
    "relevance_to_draft",
    "user_pain_intensity",
    "opportunity_to_add_value_without_sounding_promotional",
    "freshness_commentability",
    "specificity_of_source_evidence",
)

_AGENT_REVIEW_KEYS = (
    "profile_fit",
    "audience_match",
    "pain_relevance",
    "reply_opportunity",
    "confidence",
)

_PAIN_MARKERS = (
    "pain",
    "struggle",
    "stuck",
    "frustrat",
    "brittle",
    "manual",
    "messy",
    "hard",
    "problem",
    "issue",
    "annoy",
    "waste",
)

_COMMENT_MARKERS = (
    "?",
    "anyone",
    "advice",
    "how do",
    "how can",
    "looking for",
    "recommend",
    "thoughts",
    "tips",
    "help",
)

_FRESH_MARKERS = (
    "today",
    "this week",
    "recently",
    "currently",
    "right now",
    "just",
    "lately",
    "now",
)

_SPECIFICITY_MARKERS = (
    "workflow",
    "step",
    "process",
    "example",
    "because",
    "using",
    "tool",
    "stack",
    "team",
    "client",
    "document",
    "markdown",
    "chatgpt",
    "claude",
    "notes",
)

_PREFIX_MATCH_MARKERS = frozenset({"frustrat", "annoy"})
_RELEVANCE_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "before",
        "for",
        "from",
        "in",
        "into",
        "is",
        "it",
        "of",
        "on",
        "or",
        "the",
        "to",
        "vs",
        "with",
        "without",
        "you",
        "your",
    }
)
_RELEVANCE_TOKEN_ALIASES = {
    "approval": {"approve", "approved", "approves", "approving"},
    "approve": {"approval", "approved", "approves", "approving"},
}
_STRUCTURED_SNAPSHOT_SUFFIX = "-text-snapshot.txt"
_STRUCTURED_EVIDENCE_SUFFIX = "-structured-evidence.json"
VERIFIED_READ_STATUSES = frozenset(
    {
        "verified_read_via_mirror",
        "verified_read_via_agent_browser",
        "verified_read_via_manual_snapshot",
        "verified_read_via_original",
    }
)

_PREDICTION_PATTERNS = (
    "prediction",
    "predict",
    "what happens after",
    "my guess",
    "agi arrives",
    "singularity",
    "how people think",
)
_GENERIC_AI_NEWS_PATTERNS = (
    "ai news",
    "news will unfold",
    "model releases",
    "bigger labs",
    "announced",
    "announcement",
    "launch",
    "released",
)
_SUBSCRIPTION_COMPARISON_PATTERNS = (
    "pro plan",
    "claude max",
    "subscription",
    "worth the price",
    "model limits",
    "better than",
    "vs ",
    " versus ",
    "compare",
)
_SUBSCRIPTION_COMPARISON_STRONG_PATTERNS = (
    "pro plan",
    "claude max",
    "worth the price",
    "better than",
    "vs ",
    " versus ",
    "compare",
)
_BENCHMARK_FLAMEWAR_PATTERNS = (
    "benchmark",
    "eval",
    "leaderboard",
    "flamewar",
    "which model is better",
    "better for coding",
    "better for long context",
)
_ANNOUNCEMENT_PATTERNS = (
    "announced",
    "announcement",
    "introducing",
    "launch",
    "launched",
    "shipping",
    "released",
)
_WEAK_PROFILE_NEGATIVE_TERMS = frozenset(
    {
        "subscription",
        "model",
        "model release",
        "which model",
        "grok",
        "vs claude",
    }
)


@dataclass(frozen=True)
class ScoreOutcome:
    scored_candidates: list[dict[str, Any]]
    selected_candidate: dict[str, Any] | None


@dataclass(frozen=True)
class _StructuredScoringContext:
    evidence: StructuredRedditEvidence
    evidence_path: Path


AgentReviewer = Callable[
    [list[dict[str, Any]], FounderSignalConfig],
    Mapping[str, Mapping[str, Any]],
]


def built_in_agent_reviewer(
    candidates: list[dict[str, Any]], config: FounderSignalConfig
) -> Mapping[str, Mapping[str, Any]]:
    """Provide a deterministic product-profile review when no external agent is wired."""
    reviews: dict[str, Mapping[str, Any]] = {}
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id") or "")
        if not candidate_id:
            continue

        breakdown = candidate.get("score_breakdown")
        if not isinstance(breakdown, Mapping):
            breakdown = {}
        rejection_signals = _string_list(candidate.get("rejection_signals"))
        relevance = int(breakdown.get("relevance_to_draft") or 1)
        pain = int(breakdown.get("user_pain_intensity") or 1)
        reply = int(breakdown.get("opportunity_to_add_value_without_sounding_promotional") or 1)
        specificity = int(breakdown.get("specificity_of_source_evidence") or 1)
        freshness = int(breakdown.get("freshness_commentability") or 1)

        profile_fit = min(5, max(4, relevance))
        pain_relevance = min(5, max(3, pain))
        reply_opportunity = min(5, max(1, reply))
        audience_match = _audience_match_score(candidate, config)
        confidence = min(5, max(3, round((specificity + freshness + relevance) / 3)))

        reason = "Relevant recent thread with concrete product workflow pain."
        review: dict[str, Any] = {
            "profile_fit": profile_fit,
            "audience_match": audience_match,
            "pain_relevance": pain_relevance,
            "reply_opportunity": reply_opportunity,
            "confidence": confidence,
            "reason": reason,
        }
        blocking_signals = [
            signal for signal in rejection_signals if signal != "post_too_old_for_engagement"
        ]
        if blocking_signals:
            review.update(
                {
                    "profile_fit": min(profile_fit, 2),
                    "pain_relevance": min(pain_relevance, 2),
                    "reply_opportunity": min(reply_opportunity, 2),
                    "confidence": max(confidence, 4),
                    "reason": f"Structured rejection signal: {blocking_signals[0]}.",
                    "reject_reason": blocking_signals[0],
                }
            )
        reviews[candidate_id] = review
    return reviews


def score_candidates(
    candidates: Iterable[dict[str, Any]],
    config: FounderSignalConfig,
    *,
    agent_reviewer: AgentReviewer | None = None,
) -> ScoreOutcome:
    """Score only verified candidates that have a saved evidence snapshot."""
    scored: list[dict[str, Any]] = []
    for candidate in candidates:
        normalized = _score_candidate(candidate, config)
        if normalized is not None:
            scored.append(normalized)

    if scored and agent_reviewer is not None:
        _apply_agent_reviews(scored, config, agent_reviewer)

    scored.sort(key=_sort_key, reverse=True)
    _apply_selection_gate(scored, agent_reviewer_used=agent_reviewer is not None)
    selected = next(
        (candidate for candidate in scored if candidate.get("selection_eligible")),
        None,
    )
    return ScoreOutcome(scored_candidates=scored, selected_candidate=selected)


def _score_candidate(
    candidate: dict[str, Any], config: FounderSignalConfig
) -> dict[str, Any] | None:
    read_status = str(candidate.get("read_status") or candidate.get("status") or "").strip()
    snapshot_value = str(candidate.get("evidence_snapshot_path") or "").strip()
    if read_status not in VERIFIED_READ_STATUSES or not snapshot_value:
        return None

    snapshot_path = Path(snapshot_value)
    if not snapshot_path.exists() or not snapshot_path.is_file():
        return None

    snapshot_text = snapshot_path.read_text(encoding="utf-8").strip()
    if not snapshot_text:
        return None

    structured = _load_structured_scoring_context(candidate, snapshot_path)
    if structured is None:
        breakdown = {
            "relevance_to_draft": _score_relevance(snapshot_text, config),
            "user_pain_intensity": _score_marker_count(snapshot_text, _PAIN_MARKERS),
            "opportunity_to_add_value_without_sounding_promotional": _score_add_value(snapshot_text),
            "freshness_commentability": _score_freshness(snapshot_text),
            "specificity_of_source_evidence": _score_specificity(snapshot_text),
        }
        total = sum(int(value) for value in breakdown.values())
        structured_evidence_path = ""
        structured_payload: dict[str, Any] | None = None
        rejection_signals: list[str] = []
    else:
        breakdown = _score_structured_breakdown(structured.evidence, config)
        rejection_signals = _structured_rejection_signals(structured.evidence, config)
        penalty = _structured_penalty(rejection_signals)
        breakdown["off_topic_penalty"] = penalty
        total = sum(
            int(value)
            for key, value in breakdown.items()
            if key != "off_topic_penalty"
        ) - penalty
        structured_evidence_path = str(structured.evidence_path)
        structured_payload = structured.evidence.to_dict()

    scored_candidate = dict(candidate)
    scored_candidate.update(
        {
            "platform": str(candidate.get("platform") or candidate.get("source_platform") or "reddit").strip().lower(),
            "source_platform": str(candidate.get("source_platform") or candidate.get("platform") or "reddit").strip().lower(),
            "source_id": str(candidate.get("source_id") or "").strip(),
            "source_url": str(candidate.get("source_url") or candidate.get("reddit_url") or "").strip(),
            "reddit_url": str(candidate.get("reddit_url") or candidate.get("source_url") or "").strip() if str(candidate.get("platform") or "reddit") == "reddit" else str(candidate.get("reddit_url") or "").strip(),
            "evidence_url": str(candidate.get("evidence_url") or "").strip(),
            "read_status": read_status,
            "evidence_snapshot_path": str(snapshot_path),
            "structured_evidence_path": structured_evidence_path,
            "structured_evidence": structured_payload,
            "rejection_signals": rejection_signals,
            "score_breakdown": breakdown,
            "score_total": total,
        }
    )
    return scored_candidate


def _sort_key(candidate: dict[str, Any]) -> tuple[int, int, int, int, str]:
    breakdown = candidate.get("score_breakdown")
    specificity = 0
    if isinstance(breakdown, dict):
        specificity = int(breakdown.get("specificity_of_source_evidence") or 0)
    agent_score = int(candidate.get("agent_review_score_total") or 0)
    return (
        1 if agent_score else 0,
        agent_score,
        int(candidate.get("score_total") or 0),
        specificity,
        str(candidate.get("candidate_id") or ""),
    )


def _apply_agent_reviews(
    scored: list[dict[str, Any]],
    config: FounderSignalConfig,
    agent_reviewer: AgentReviewer,
) -> None:
    review_inputs = [_candidate_review_input(candidate, config) for candidate in scored]
    reviews = agent_reviewer(review_inputs, config)
    for candidate in scored:
        candidate_id = str(candidate.get("candidate_id") or "")
        review = _normalize_agent_review(reviews.get(candidate_id))
        if review is None:
            continue
        candidate["agent_review"] = review
        candidate["agent_review_score_total"] = sum(
            int(review[key]) for key in _AGENT_REVIEW_KEYS
        )
        breakdown = candidate.setdefault("score_breakdown", {})
        if isinstance(breakdown, dict):
            breakdown["agent_profile_fit"] = review["profile_fit"]
            breakdown["agent_review_confidence"] = review["confidence"]
        candidate["score_total"] = int(candidate.get("score_total") or 0) + int(
            candidate["agent_review_score_total"]
        )


def _candidate_review_input(
    candidate: dict[str, Any], config: FounderSignalConfig
) -> dict[str, Any]:
    snapshot_path = Path(str(candidate.get("evidence_snapshot_path") or ""))
    try:
        snapshot_text = snapshot_path.read_text(encoding="utf-8").strip()
    except OSError:
        snapshot_text = ""
    structured_evidence = candidate.get("structured_evidence")
    if isinstance(structured_evidence, Mapping):
        structured_payload = dict(structured_evidence)
    else:
        structured_payload = None
    product_profile = {
        "profile_id": config.profile_id,
        "product_name": config.product_name,
        "product_one_liner": config.product_one_liner,
        "target_audience": config.target_audience,
        "keywords": list(config.keywords),
        "scoring_terms": list(config.scoring_terms),
        "subreddits": list(config.subreddits),
    }
    return {
        "candidate_id": str(candidate.get("candidate_id") or ""),
        "reddit_url": str(candidate.get("reddit_url") or ""),
        "evidence_url": str(candidate.get("evidence_url") or ""),
        "live_metadata": {
            "post_age_hours": candidate.get("post_age_hours"),
            "post_age_days": candidate.get("post_age_days"),
            "comment_count": candidate.get("comment_count"),
            "score": candidate.get("score"),
            "within_preferred_age_window": candidate.get("within_preferred_age_window"),
        },
        "deterministic_score_total": int(candidate.get("score_total") or 0),
        "deterministic_score_breakdown": dict(candidate.get("score_breakdown") or {}),
        "score_total": int(candidate.get("score_total") or 0),
        "score_breakdown": dict(candidate.get("score_breakdown") or {}),
        "evidence_snapshot_text": snapshot_text,
        "structured_evidence_path": str(candidate.get("structured_evidence_path") or ""),
        "structured_evidence": structured_payload,
        "post_title": str((structured_payload or {}).get("post_title") or ""),
        "post_body": str((structured_payload or {}).get("post_body") or ""),
        "subreddit": str((structured_payload or {}).get("subreddit") or ""),
        "comments_excerpt": str((structured_payload or {}).get("comments_excerpt") or ""),
        "product_profile": product_profile,
        "rejection_signals": list(candidate.get("rejection_signals") or []),
    }


def _normalize_agent_review(review: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(review, Mapping):
        return None
    normalized: dict[str, Any] = {}
    for key in _AGENT_REVIEW_KEYS:
        normalized[key] = _bounded_score(review.get(key))
    normalized["reason"] = str(review.get("reason") or "").strip()[:600]
    reject_reason = str(review.get("reject_reason") or "").strip()
    if reject_reason:
        normalized["reject_reason"] = reject_reason[:300]
    return normalized


def _apply_selection_gate(
    scored: list[dict[str, Any]], *, agent_reviewer_used: bool
) -> None:
    for candidate in scored:
        eligible, gate_reason = _selection_gate(candidate, agent_reviewer_used=agent_reviewer_used)
        candidate["selection_eligible"] = eligible
        candidate["selection_gate_reason"] = gate_reason


def _selection_gate(
    candidate: Mapping[str, Any], *, agent_reviewer_used: bool
) -> tuple[bool, str]:
    rejection_signals = _string_list(candidate.get("rejection_signals"))
    if "post_too_old_for_engagement" in rejection_signals:
        return False, "post_too_old_for_engagement"

    if agent_reviewer_used:
        review = candidate.get("agent_review")
        if not isinstance(review, Mapping):
            return False, "missing_agent_review"
        reject_reason = str(review.get("reject_reason") or "").strip()
        if reject_reason:
            return False, "agent_reject_reason"
        if int(review.get("profile_fit") or 0) < 4:
            return False, "low_profile_fit"
        if int(review.get("pain_relevance") or 0) < 3:
            return False, "low_pain_relevance"
        if int(review.get("confidence") or 0) < 3:
            return False, "low_confidence"
        return True, ""

    if candidate.get("structured_evidence"):
        breakdown = candidate.get("score_breakdown")
        relevance = 0
        if isinstance(breakdown, Mapping):
            relevance = int(breakdown.get("relevance_to_draft") or 0)
        if relevance < 3:
            return False, "structured_relevance_below_threshold"
        if rejection_signals:
            return False, "structured_rejection_signal"
    return True, ""


def _bounded_score(value: Any) -> int:
    try:
        numeric = int(value)
    except (TypeError, ValueError):
        return 1
    return min(5, max(1, numeric))


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _audience_match_score(candidate: Mapping[str, Any], config: FounderSignalConfig) -> int:
    structured = candidate.get("structured_evidence")
    if isinstance(structured, Mapping):
        content = "\n\n".join(
            str(structured.get(key) or "")
            for key in ("post_title", "post_body", "subreddit")
        )
    else:
        content = str(candidate.get("evidence_snapshot_text") or "")
    content = content.lower()
    signals = 0
    for subreddit in config.subreddits:
        subreddit_value = str(subreddit).strip().lower().lstrip("r/")
        if subreddit_value and f"r/{subreddit_value}" in content:
            signals += 1
            break
    for term in [*config.keywords, *config.scoring_terms]:
        if _relevance_marker_strength(content, str(term)) > 0:
            signals += 1
    if signals >= 4:
        return 5
    if signals >= 3:
        return 4
    if signals >= 2:
        return 3
    if signals >= 1:
        return 2
    return 1


def _score_relevance(snapshot_text: str, config: FounderSignalConfig) -> int:
    terms = [keyword for keyword in config.keywords if keyword.strip()]
    terms.append(config.product_name)
    terms.extend(config.scoring_terms)
    matches = sum(1 for term in terms if _contains_marker(snapshot_text, term))
    if matches >= 6:
        return 5
    if matches >= 4:
        return 4
    if matches >= 2:
        return 3
    if matches >= 1:
        return 2
    return 1


def _load_structured_scoring_context(
    candidate: Mapping[str, Any], snapshot_path: Path
) -> _StructuredScoringContext | None:
    candidates = []
    explicit_path = str(candidate.get("structured_evidence_path") or "").strip()
    if explicit_path:
        candidates.append(Path(explicit_path))
    sibling_path = _structured_evidence_sibling(snapshot_path)
    if sibling_path is not None:
        candidates.append(sibling_path)

    for evidence_path in candidates:
        if not evidence_path.exists() or not evidence_path.is_file():
            continue
        try:
            payload = json.loads(evidence_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        evidence = _structured_evidence_from_payload(payload, snapshot_path)
        if evidence is None:
            continue
        return _StructuredScoringContext(evidence=evidence, evidence_path=evidence_path)
    return None


def _structured_evidence_sibling(snapshot_path: Path) -> Path | None:
    if snapshot_path.name.endswith(_STRUCTURED_SNAPSHOT_SUFFIX):
        return snapshot_path.with_name(
            snapshot_path.name.replace(
                _STRUCTURED_SNAPSHOT_SUFFIX,
                _STRUCTURED_EVIDENCE_SUFFIX,
            )
        )
    return None


def _structured_evidence_from_payload(
    payload: Any, snapshot_path: Path
) -> StructuredRedditEvidence | None:
    if not isinstance(payload, Mapping):
        return None
    try:
        return StructuredRedditEvidence(
            post_title=str(payload.get("post_title") or "").strip(),
            post_body=str(payload.get("post_body") or "").strip(),
            subreddit=str(payload.get("subreddit") or "").strip(),
            comments_excerpt=str(payload.get("comments_excerpt") or "").strip(),
            extraction_quality=str(payload.get("extraction_quality") or "").strip(),
            raw_text_snapshot=str(payload.get("raw_text_snapshot") or "").strip()
            or snapshot_path.read_text(encoding="utf-8").strip(),
            post_age_days=_optional_int(payload.get("post_age_days")),
        )
    except OSError:
        return None


def _score_structured_breakdown(
    evidence: StructuredRedditEvidence, config: FounderSignalConfig
) -> dict[str, int]:
    title_text = evidence.post_title.strip()
    body_text = evidence.post_body.strip()
    comments_text = evidence.comments_excerpt.strip()
    combined_post_text = "\n\n".join(part for part in (title_text, body_text) if part).strip()
    total_context = "\n\n".join(
        part for part in (title_text, body_text, comments_text) if part
    ).strip()
    return {
        "relevance_to_draft": _score_structured_relevance(
            title_text,
            body_text,
            comments_text,
            config,
        ),
        "user_pain_intensity": _score_marker_count(combined_post_text or total_context, _PAIN_MARKERS),
        "opportunity_to_add_value_without_sounding_promotional": _score_add_value(
            combined_post_text or total_context
        ),
        "freshness_commentability": _score_freshness(combined_post_text or total_context),
        "specificity_of_source_evidence": _score_specificity(total_context),
    }


def _score_structured_relevance(
    title_text: str,
    body_text: str,
    comments_text: str,
    config: FounderSignalConfig,
) -> int:
    terms = [keyword for keyword in config.keywords if keyword.strip()]
    terms.append(config.product_name)
    terms.extend(config.scoring_terms)

    title_matches = sum(_relevance_marker_strength(title_text, term) for term in terms)
    body_matches = sum(_relevance_marker_strength(body_text, term) for term in terms)
    comment_matches = sum(_relevance_marker_strength(comments_text, term) for term in terms)
    weighted_matches = (title_matches * 3) + (body_matches * 2)

    if weighted_matches >= 8:
        return 5
    if weighted_matches >= 5:
        return 4
    if weighted_matches >= 2.5:
        return 3
    if weighted_matches >= 1:
        return 2
    if comment_matches:
        return 1
    return 1


def _structured_rejection_signals(
    evidence: StructuredRedditEvidence, config: FounderSignalConfig
) -> list[str]:
    content = "\n\n".join(
        part
        for part in (evidence.post_title, evidence.post_body, evidence.subreddit)
        if part
    )
    signals: list[str] = []
    if _contains_any_marker(content, _PREDICTION_PATTERNS):
        signals.append("prediction_or_speculation_thread")
    if _contains_any_marker(content, _GENERIC_AI_NEWS_PATTERNS):
        signals.append("generic_ai_news_thread")
    if _is_subscription_comparison_thread(evidence):
        signals.append("model_subscription_comparison")
    if _contains_any_marker(content, _BENCHMARK_FLAMEWAR_PATTERNS):
        signals.append("benchmark_or_flamewar_thread")
    if _contains_any_marker(content, _ANNOUNCEMENT_PATTERNS) and not _contains_any_marker(
        content,
        _PAIN_MARKERS + _COMMENT_MARKERS,
    ):
        signals.append("broad_announcement_without_user_problem")
    negative_terms = tuple(term for term in config.negative_scoring_terms if term.strip())
    if negative_terms and _has_profile_negative_signal(content, negative_terms):
        signals.append("profile_negative_scoring_term")
    if (
        evidence.post_age_days is not None
        and config.max_post_age_days >= 0
        and evidence.post_age_days > config.max_post_age_days
    ):
        signals.append("post_too_old_for_engagement")
    return signals


def _structured_penalty(rejection_signals: list[str]) -> int:
    if not rejection_signals:
        return 0
    return min(5, len(rejection_signals) + 1)


def _score_add_value(snapshot_text: str) -> int:
    lower = snapshot_text.lower()
    comment_markers = sum(1 for marker in _COMMENT_MARKERS if _contains_marker(lower, marker))
    if comment_markers >= 4:
        return 5
    if comment_markers >= 3:
        return 4
    if comment_markers >= 2:
        return 3
    if comment_markers >= 1 or " i " in f" {lower} ":
        return 2
    return 1


def _score_freshness(snapshot_text: str) -> int:
    lower = snapshot_text.lower()
    freshness = sum(1 for marker in _FRESH_MARKERS if _contains_marker(lower, marker))
    if "?" in snapshot_text:
        freshness += 1
    return min(5, max(1, freshness + 1))


def _score_specificity(snapshot_text: str) -> int:
    lower = snapshot_text.lower()
    lines = [line.strip() for line in snapshot_text.splitlines() if line.strip()]
    specificity = sum(1 for marker in _SPECIFICITY_MARKERS if _contains_marker(lower, marker))
    if any(char.isdigit() for char in snapshot_text):
        specificity += 1
    if len(lines) >= 3:
        specificity += 1
    if specificity >= 6:
        return 5
    if specificity >= 4:
        return 4
    if specificity >= 2:
        return 3
    if specificity >= 1:
        return 2
    return 1


def _score_marker_count(snapshot_text: str, markers: tuple[str, ...]) -> int:
    lower = snapshot_text.lower()
    matches = sum(1 for marker in markers if _contains_marker(lower, marker))
    return min(5, max(1, matches + 1))


def _is_subscription_comparison_thread(evidence: StructuredRedditEvidence) -> bool:
    title = evidence.post_title.strip()
    body = evidence.post_body.strip()
    content = "\n\n".join(part for part in (title, body) if part)
    if not content:
        return False

    title_strong_matches = _marker_match_count(title, _SUBSCRIPTION_COMPARISON_STRONG_PATTERNS)
    total_matches = _marker_match_count(content, _SUBSCRIPTION_COMPARISON_PATTERNS)
    if title_strong_matches >= 1 and total_matches >= 2:
        return True
    return total_matches >= 3


def _has_profile_negative_signal(text: str, terms: tuple[str, ...]) -> bool:
    matched_terms = [term.strip() for term in terms if _contains_marker(text, term)]
    if not matched_terms:
        return False
    strong_matches = [
        term
        for term in matched_terms
        if term.lower() not in _WEAK_PROFILE_NEGATIVE_TERMS or len(_meaningful_relevance_tokens(term)) >= 2
    ]
    if strong_matches:
        return True
    return len(matched_terms) >= 2


def _marker_match_count(text: str, markers: tuple[str, ...]) -> int:
    return sum(1 for marker in markers if _contains_marker(text, marker))


def _relevance_marker_strength(text: str, marker: str) -> float:
    if _contains_marker(text, marker):
        return 1.0

    marker_tokens = _meaningful_relevance_tokens(marker)
    if len(marker_tokens) < 2:
        return 0.0

    text_tokens = _tokenize_relevance_text(text)
    if not text_tokens:
        return 0.0

    matches = sum(1 for token in marker_tokens if _token_matches_relevance_text(token, text_tokens))
    if matches == len(marker_tokens):
        return 0.85
    if len(marker_tokens) >= 3 and matches >= len(marker_tokens) - 1:
        return 0.55
    return 0.0


def _meaningful_relevance_tokens(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) >= 3 and token not in _RELEVANCE_STOPWORDS
    ]


def _tokenize_relevance_text(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    normalized = set(tokens)
    for token in tokens:
        normalized.update(_relevance_token_variants(token))
    return normalized


def _token_matches_relevance_text(marker_token: str, text_tokens: set[str]) -> bool:
    variants = _relevance_token_variants(marker_token)
    variants.add(marker_token)
    return bool(variants.intersection(text_tokens))


def _relevance_token_variants(token: str) -> set[str]:
    variants = {token}
    variants.update(_RELEVANCE_TOKEN_ALIASES.get(token, set()))
    if len(token) <= 3:
        return variants

    if token.endswith("ies") and len(token) > 4:
        variants.add(f"{token[:-3]}y")
    if token.endswith("es") and len(token) > 4:
        variants.add(token[:-2])
    if token.endswith("s") and len(token) > 3:
        variants.add(token[:-1])
    if token.endswith("ing") and len(token) > 5:
        stem = token[:-3]
        variants.add(stem)
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            variants.add(stem[:-1])
    if token.endswith("ed") and len(token) > 4:
        variants.add(token[:-2])
    return variants


def _contains_marker(text: str, marker: str) -> bool:
    normalized_marker = marker.strip().lower()
    if not normalized_marker:
        return False
    if not any(char.isalnum() for char in normalized_marker):
        return normalized_marker in text.lower()
    if normalized_marker in _PREFIX_MATCH_MARKERS:
        return bool(re.search(rf"\b{re.escape(normalized_marker)}\w*", text.lower()))
    return bool(re.search(rf"(?<!\w){re.escape(normalized_marker)}(?!\w)", text.lower()))


def _contains_any_marker(text: str, markers: tuple[str, ...]) -> bool:
    return any(_contains_marker(text, marker) for marker in markers)
