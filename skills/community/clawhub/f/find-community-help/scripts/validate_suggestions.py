#!/usr/bin/env python3
"""Validate the canonical find-community-help suggestion block."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse


START = "<!-- find-community-help:suggestions:start -->"
END = "<!-- find-community-help:suggestions:end -->"
LEGACY_START = "<!-- agent-travel:suggestions:start -->"
LEGACY_END = "<!-- agent-travel:suggestions:end -->"
TOP_LEVEL_REQUIRED = {
    "generated_at",
    "expires_at",
    "search_mode",
    "tool_preference",
    "source_scope",
    "thread_scope",
    "problem_fingerprint",
    "advisory_only",
}
TOP_LEVEL_OPTIONAL = {
    "trigger_reason",
    "visibility",
    "fingerprint_hash",
    "reuse_gate",
    "budget",
    "private_source_opt_in",
    "consent_basis",
}
ITEM_REQUIRED = {
    "title",
    "applies_when",
    "hint",
    "confidence",
    "manual_check",
    "solves_point",
    "new_idea",
    "fit_reason",
    "match_reasoning",
    "version_scope",
    "do_not_apply_when",
}
ALLOWED_LEVELS = {"low", "medium", "high"}
ALLOWED_TOOL_PREFERENCES = {"public-only", "all-available", "custom"}
ALLOWED_VISIBILITY = {"silent_until_relevant", "show_on_next_relevant_turn"}
ALLOWED_SOURCE_SCOPE_PARTS = {"primary", "secondary", "tertiary"}
ALLOWED_EVIDENCE_TIERS = ALLOWED_SOURCE_SCOPE_PARTS
ALLOWED_EVIDENCE_SOURCE_KINDS = {
    "primary": {
        "advisory",
        "changelog",
        "clawhub_metadata",
        "cve",
        "github_advisory",
        "maintainer_thread",
        "nvd",
        "official",
        "official_discussion",
        "official_docs",
        "official_github_discussion",
        "official_github_issue",
        "official_github_release",
        "official_issue",
        "official_reference",
        "release_notes",
        "security_advisory",
        "vendor_forum_staff",
        "vendor_security_advisory",
    },
    "secondary": {
        "clawhub_review",
        "community",
        "github_discussion",
        "github_issue",
        "maintained_qna",
        "qna",
        "research",
        "research_paper",
        "stackoverflow",
        "vendor_forum",
        "vendor_forum_user",
    },
    "tertiary": {
        "blog",
        "chat_community",
        "discord_summary",
        "forum",
        "reddit",
        "social",
        "workaround",
    },
}
ALLOWED_TRIGGER_REASONS = {
    "heartbeat",
    "scheduled",
    "task_end",
    "failure_recovery",
    "idle_fallback",
    "user_request",
    "manual_request",
}
ALLOWED_REUSE_GATES = {"min_4_of_5_axes_and_ttl_valid"}
BOOLEAN_TEXT = {"true", "false"}
ALLOWED_CONSENT_BASIS = {
    "user_explicit_private_source_opt_in",
    "user_explicit_request",
}
DISALLOWED_EVIDENCE_REFERENCE_PREFIXES = (
    "sanitized-local-session:",
    "local-session:",
    "fixture:",
)
SUGGESTION_LIMITS = {"low": 1, "medium": 3, "high": 5}
MAX_TTL = timedelta(days=14)
FINGERPRINT_HASH_PATTERN = re.compile(r"^(?:h64|sha256):[0-9a-f]{64}$")
MATCH_AXES = {
    "host",
    "version",
    "symptom",
    "constraint_pattern",
    "desired_next_outcome",
}
MATCH_AXIS_ALIASES = {
    "constraint": "constraint_pattern",
}
KEY_PATTERN = re.compile(r"^([a-z_]+):\s*(.*)$")
SUGGESTION_HEADING_PATTERN = re.compile(r"^##\s+suggestion-\d+\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to a markdown file containing suggestion markers")
    return parser.parse_args()


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1


def parse_iso(value: str) -> datetime:
    if not value.strip():
        raise ValueError("timestamp must be non-empty")
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include a timezone offset")
    return parsed


def normalize_part(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def split_scope(value: str) -> set[str]:
    return {normalize_part(part) for part in re.split(r"[^A-Za-z0-9]+", value) if part.strip()}


def canonicalize_axis(axis: str) -> str:
    normalized = normalize_part(axis)
    return MATCH_AXIS_ALIASES.get(normalized, normalized)


def parse_evidence_source(item: str) -> tuple[str, str]:
    label, separator, reference = str(item).partition(":")
    normalized_label = normalize_part(label)
    normalized_reference = reference.strip() if separator else ""
    if normalized_reference:
        parsed = urlparse(normalized_reference)
        if parsed.scheme and parsed.netloc:
            host = parsed.netloc.lower()
            path = parsed.path.rstrip("/")
            query = f"?{parsed.query}" if parsed.query else ""
            normalized_reference = f"{host}{path}{query}"
    return normalized_label, normalized_reference


def is_disallowed_evidence_reference(reference: str) -> bool:
    lowered = reference.strip().lower()
    return any(lowered.startswith(prefix) for prefix in DISALLOWED_EVIDENCE_REFERENCE_PREFIXES)


def split_evidence_label(label: str) -> tuple[str, str]:
    tier, separator, source_kind = label.partition("_")
    return tier, source_kind if separator else ""


@dataclass
class SuggestionBlockParser:
    top_level: dict[str, str] = field(default_factory=dict)
    suggestions: list[dict[str, object]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    current_suggestion: dict[str, object] | None = None
    active_child_list: str | None = None
    last_scalar_key: str | None = None

    def start_suggestion(self) -> None:
        self.current_suggestion = {"evidence": [], "match_reasoning": []}
        self.suggestions.append(self.current_suggestion)
        self.active_child_list = None
        self.last_scalar_key = None

    def start_child_list(self, name: str) -> None:
        if self.current_suggestion is None:
            self.errors.append(f"found {name} block before any suggestion heading")
            return
        self.active_child_list = name
        self.last_scalar_key = None

    def add_list_item(self, line: str) -> None:
        if self.current_suggestion is None or self.active_child_list is None:
            self.errors.append(f"unexpected list item outside block: {line}")
            return
        target = self.current_suggestion.get(self.active_child_list)
        if not isinstance(target, list):
            self.errors.append(f"{self.active_child_list} block is not a list")
            return
        target.append(line[2:].strip())
        self.last_scalar_key = None

    def add_key_value(self, key: str, value: str) -> None:
        self.active_child_list = None
        self.last_scalar_key = None
        if self.current_suggestion is None:
            if key in ITEM_REQUIRED:
                self.errors.append(f"suggestion field {key} must appear under a suggestion heading")
                return
            self.top_level[key] = value
            return
        if key in TOP_LEVEL_REQUIRED or key in TOP_LEVEL_OPTIONAL:
            self.errors.append(f"top-level field {key} must appear before the first suggestion heading")
            return
        self.current_suggestion[key] = value
        self.last_scalar_key = key

    def add_continuation(self, line: str) -> None:
        if self.current_suggestion is None or self.active_child_list is not None or self.last_scalar_key is None:
            self.reject_line(line)
            return
        previous = str(self.current_suggestion.get(self.last_scalar_key, "")).strip()
        self.current_suggestion[self.last_scalar_key] = f"{previous} {line}".strip()

    def reject_line(self, line: str) -> None:
        self.active_child_list = None
        self.last_scalar_key = None
        self.errors.append(f"unrecognized line: {line}")


def parse_block(path: Path) -> tuple[dict[str, str], list[dict[str, object]], list[str]]:
    text = path.read_text(encoding="utf-8")
    start = text.rfind(START)
    end = text.rfind(END)
    if start == -1 or end == -1 or end <= start:
        start = text.rfind(LEGACY_START)
        end = text.rfind(LEGACY_END)
        marker_len = len(LEGACY_START)
    else:
        marker_len = len(START)
    if start == -1 or end == -1 or end <= start:
        return {}, [], ["missing or invalid find-community-help markers"]

    block = text[start + marker_len : end].strip()
    lines = [line.rstrip() for line in block.splitlines()]
    parser = SuggestionBlockParser()

    for raw_line in lines:
        line = raw_line.strip()
        if (
            not line
            or line.startswith("# find-community-help suggestions")
            or line.startswith("# agent-travel suggestions")
        ):
            continue
        if SUGGESTION_HEADING_PATTERN.match(line):
            parser.start_suggestion()
            continue
        if line == "evidence:":
            parser.start_child_list("evidence")
            continue
        if line == "match_reasoning:":
            parser.start_child_list("match_reasoning")
            continue
        if line.startswith("- "):
            parser.add_list_item(line)
            continue

        match = KEY_PATTERN.match(line)
        if not match:
            parser.add_continuation(line)
            continue

        key, value = match.groups()
        parser.add_key_value(key, value)

    return parser.top_level, parser.suggestions, parser.errors


def suggestion_limit(top_level: dict[str, str]) -> int | None:
    values = []
    for key in ("budget", "search_mode"):
        value = top_level.get(key)
        if value in SUGGESTION_LIMITS:
            values.append(SUGGESTION_LIMITS[value])
    return min(values) if values else None


def validate_top_level_required_fields(top_level: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if top_level.get("advisory_only", "").lower() != "true":
        errors.append("advisory_only must be true")
    if top_level.get("thread_scope") != "active_conversation_only":
        errors.append("thread_scope must be active_conversation_only")
    for field in sorted(TOP_LEVEL_REQUIRED - {"advisory_only"}):
        if not top_level.get(field, "").strip():
            errors.append(f"{field} must be non-empty")
    return errors


def validate_top_level_mode_fields(top_level: dict[str, str]) -> list[str]:
    errors: list[str] = []
    budget = top_level.get("budget", "")
    if budget and budget not in ALLOWED_LEVELS:
        errors.append("budget must be one of: low, medium, high")
    search_mode = top_level.get("search_mode", "")
    if search_mode not in ALLOWED_LEVELS:
        errors.append("search_mode must be one of: low, medium, high")
    if budget and search_mode and budget != search_mode:
        errors.append("budget must match search_mode when both are present")
    tool_preference = top_level.get("tool_preference", "")
    if tool_preference not in ALLOWED_TOOL_PREFERENCES:
        errors.append("tool_preference must be one of: all-available, custom, public-only")
    private_source_opt_in = top_level.get("private_source_opt_in", "").strip().lower()
    if private_source_opt_in and private_source_opt_in not in BOOLEAN_TEXT:
        errors.append("private_source_opt_in must be true or false when present")
    if tool_preference in {"all-available", "custom"} and private_source_opt_in != "true":
        errors.append("non-public tool_preference requires private_source_opt_in: true")
    if private_source_opt_in == "true" and not top_level.get("consent_basis", "").strip():
        errors.append("private_source_opt_in requires a non-empty consent_basis")
    consent_basis = top_level.get("consent_basis", "").strip()
    if private_source_opt_in == "true" and consent_basis and consent_basis not in ALLOWED_CONSENT_BASIS:
        allowed = ", ".join(sorted(ALLOWED_CONSENT_BASIS))
        errors.append(f"consent_basis must be one of: {allowed}")
    return errors


def validate_source_scope(top_level: dict[str, str]) -> list[str]:
    errors: list[str] = []
    source_scope = split_scope(top_level.get("source_scope", ""))
    if "primary" not in source_scope:
        errors.append("source_scope must include primary")
    invalid_source_scope = sorted(source_scope - ALLOWED_SOURCE_SCOPE_PARTS)
    if invalid_source_scope:
        errors.append(f"source_scope contains unsupported tiers: {', '.join(invalid_source_scope)}")
    return errors


def validate_optional_top_level_fields(top_level: dict[str, str]) -> list[str]:
    errors: list[str] = []
    visibility = top_level.get("visibility")
    if visibility and visibility not in ALLOWED_VISIBILITY:
        errors.append("visibility must be one of: show_on_next_relevant_turn, silent_until_relevant")

    trigger_reason = top_level.get("trigger_reason")
    if trigger_reason and trigger_reason not in ALLOWED_TRIGGER_REASONS:
        errors.append(
            "trigger_reason must be one of: failure_recovery, heartbeat, idle_fallback, manual_request, scheduled, task_end, user_request"
        )

    reuse_gate = top_level.get("reuse_gate")
    if reuse_gate and reuse_gate not in ALLOWED_REUSE_GATES:
        errors.append("reuse_gate must be: min_4_of_5_axes_and_ttl_valid")
    return errors


def validate_fingerprint_fields(top_level: dict[str, str]) -> list[str]:
    errors: list[str] = []
    fingerprint_hash = top_level.get("fingerprint_hash", "")
    if fingerprint_hash and not FINGERPRINT_HASH_PATTERN.fullmatch(fingerprint_hash):
        errors.append("fingerprint_hash must be formatted as h64:<64 lowercase hex chars>")

    fingerprint_parts = [part.strip() for part in top_level.get("problem_fingerprint", "").split("|") if part.strip()]
    if len(fingerprint_parts) < 4:
        errors.append("problem_fingerprint must contain at least 4 non-empty segments")
    return errors


def validate_timestamp_window(top_level: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if {"generated_at", "expires_at"} <= set(top_level):
        try:
            generated = parse_iso(top_level["generated_at"])
            expires = parse_iso(top_level["expires_at"])
            if expires <= generated:
                errors.append("expires_at must be later than generated_at")
            if expires - generated > MAX_TTL:
                errors.append("expires_at must be within 14 days of generated_at")
        except (TypeError, ValueError) as exc:
            errors.append(f"invalid ISO date: {exc}")
    return errors


def validate_top_level(top_level: dict[str, str], suggestion_count: int) -> list[str]:
    missing = sorted(TOP_LEVEL_REQUIRED - set(top_level))
    if missing:
        return [f"missing top-level fields: {', '.join(missing)}"]

    errors: list[str] = []
    errors.extend(validate_top_level_required_fields(top_level))
    errors.extend(validate_top_level_mode_fields(top_level))
    errors.extend(validate_source_scope(top_level))
    errors.extend(validate_optional_top_level_fields(top_level))
    errors.extend(validate_fingerprint_fields(top_level))
    errors.extend(validate_timestamp_window(top_level))
    limit = suggestion_limit(top_level)
    if limit is not None and suggestion_count > limit:
        errors.append(f"{top_level.get('search_mode', '')} allows at most {limit} suggestion(s)")

    return errors


def validate_required_suggestion_fields(index: int, suggestion: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for field in sorted(ITEM_REQUIRED - {"match_reasoning"}):
        value = str(suggestion.get(field, "")).strip()
        if not value:
            errors.append(f"suggestion-{index} field {field} must be non-empty")

    confidence = str(suggestion.get("confidence", ""))
    if confidence not in ALLOWED_LEVELS:
        errors.append(f"suggestion-{index} confidence must be one of: low, medium, high")
    return errors


def validate_evidence(
    index: int,
    evidence: object,
    declared_source_scope: set[str],
) -> list[str]:
    errors: list[str] = []
    if not isinstance(evidence, list) or len(evidence) < 2:
        errors.append(f"suggestion-{index} needs at least 2 evidence items")
        return errors

    evidence_tiers = set()
    evidence_sources = set()
    evidence_format_error = False
    for item in evidence:
        if ":" not in str(item):
            errors.append(f"suggestion-{index} evidence items must use source_label: reference format")
            evidence_format_error = True
            continue
        label, source_key = parse_evidence_source(str(item))
        if not label or not source_key:
            errors.append(f"suggestion-{index} evidence items must include a non-empty source label and reference")
            evidence_format_error = True
            continue
        if is_disallowed_evidence_reference(source_key):
            errors.append(
                f"suggestion-{index} evidence reference must cite an external source; "
                "local session fixtures belong in case metadata"
            )
            evidence_format_error = True
            continue
        tier, source_kind = split_evidence_label(label)
        evidence_tiers.add(tier)
        evidence_sources.add(source_key)
        if tier not in ALLOWED_EVIDENCE_TIERS:
            errors.append(
                f"suggestion-{index} evidence tier {tier} is unsupported; use primary_, secondary_, or tertiary_ labels"
            )
            evidence_format_error = True
            continue
        if source_kind not in ALLOWED_EVIDENCE_SOURCE_KINDS[tier]:
            allowed = ", ".join(sorted(ALLOWED_EVIDENCE_SOURCE_KINDS[tier]))
            errors.append(
                f"suggestion-{index} evidence source kind {label} is unsupported; "
                f"use {tier}_ plus one of: {allowed}"
            )
            evidence_format_error = True
            continue
        if tier not in declared_source_scope:
            errors.append(f"suggestion-{index} evidence tier {tier} must be declared in source_scope")

    if evidence_format_error:
        return errors
    if "primary" not in evidence_tiers:
        errors.append(f"suggestion-{index} needs at least 1 primary evidence item")
    if not any(tier != "primary" for tier in evidence_tiers):
        errors.append(f"suggestion-{index} needs at least 1 non-primary cross-validation evidence item")
    if len(evidence_sources) < 2:
        errors.append(
            f"suggestion-{index} needs at least 2 distinct evidence sources, "
            "including one primary and one independent non-primary source"
        )
    return errors


def validate_match_reasoning(index: int, match_reasoning: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(match_reasoning, list) or len(match_reasoning) < 4:
        errors.append(f"suggestion-{index} needs at least 4 match_reasoning items")
        return errors

    axes = set()
    for item in match_reasoning:
        if ":" not in str(item):
            errors.append(f"suggestion-{index} match_reasoning items must use axis: explanation format")
            break
        axis, explanation = str(item).split(":", 1)
        normalized_axis = canonicalize_axis(axis)
        if normalized_axis not in MATCH_AXES:
            continue
        if not explanation.strip():
            errors.append(f"suggestion-{index} match_reasoning explanations must be non-empty")
            break
        axes.add(normalized_axis)
    if len(axes) < 4:
        errors.append(f"suggestion-{index} needs at least 4 distinct match_reasoning axes")
    return errors


def validate_suggestion(
    index: int,
    suggestion: dict[str, object],
    declared_source_scope: set[str],
) -> list[str]:
    missing = sorted(ITEM_REQUIRED - set(suggestion))
    if missing:
        return [f"suggestion-{index} is missing fields: {', '.join(missing)}"]

    errors = validate_required_suggestion_fields(index, suggestion)
    errors.extend(validate_evidence(index, suggestion.get("evidence", []), declared_source_scope))
    errors.extend(validate_match_reasoning(index, suggestion.get("match_reasoning", [])))
    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    if not path.exists():
        return fail([f"file not found: {path}"])

    try:
        top_level, suggestions, errors = parse_block(path)
    except OSError as exc:
        return fail([f"failed to read {path}: {exc}"])

    errors.extend(validate_top_level(top_level, len(suggestions)))
    if not suggestions:
        errors.append("no suggestions found")

    declared_source_scope = split_scope(top_level.get("source_scope", ""))
    for index, suggestion in enumerate(suggestions, start=1):
        errors.extend(validate_suggestion(index, suggestion, declared_source_scope))

    if errors:
        return fail(errors)

    print(f"OK: validated {len(suggestions)} suggestion(s) in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
