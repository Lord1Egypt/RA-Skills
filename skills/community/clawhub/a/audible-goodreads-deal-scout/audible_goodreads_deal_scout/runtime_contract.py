from __future__ import annotations

import json
import urllib.parse
from pathlib import Path
from typing import Any

from .constants import DEFAULT_THRESHOLD
from .shared import atomic_write_text, normalize_space, write_json_atomic


FIT_MIN_WORDS = 45
FIT_MAX_WORDS = 90
ROOT_FIELDS = {"schemaVersion", "goodreads", "fit"}
GOODREADS_FIELDS = {"status", "url", "title", "author", "averageRating", "ratingsCount", "evidence"}
FIT_FIELDS = {"status", "sentence"}


def runtime_output_schema() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "type": "object",
        "additionalProperties": False,
        "required": ["schemaVersion", "goodreads", "fit"],
        "properties": {
            "schemaVersion": {"const": 1},
            "goodreads": {
                "type": "object",
                "additionalProperties": False,
                "required": ["status"],
                "allOf": [
                    {
                        "if": {"properties": {"status": {"const": "resolved"}}, "required": ["status"]},
                        "then": {
                            "required": ["url", "title", "author", "averageRating"],
                            "properties": {
                                "url": {"type": "string"},
                                "title": {"type": "string"},
                                "author": {"type": "string"},
                                "averageRating": {"type": "number"},
                            },
                        },
                        "else": {
                            "properties": {
                                "url": {"type": "null"},
                                "title": {"type": "null"},
                                "author": {"type": "null"},
                                "averageRating": {"type": "null"},
                                "ratingsCount": {"type": "null"},
                            }
                        },
                    }
                ],
                "properties": {
                    "status": {
                        "enum": ["resolved", "no_match", "lookup_failed"],
                    },
                    "url": {
                        "type": ["string", "null"],
                        "pattern": r"^https://(?:www\.)?goodreads\.com/book/show/",
                    },
                    "title": {"type": ["string", "null"], "minLength": 1},
                    "author": {"type": ["string", "null"], "minLength": 1},
                    "averageRating": {"type": ["number", "null"], "minimum": 0, "maximum": 5},
                    "ratingsCount": {"type": ["integer", "null"], "minimum": 0},
                    "evidence": {"type": ["string", "null"]},
                },
            },
            "fit": {
                "type": "object",
                "additionalProperties": False,
                "required": ["status"],
                "allOf": [
                    {
                        "if": {"properties": {"status": {"const": "written"}}, "required": ["status"]},
                        "then": {
                            "required": ["sentence"],
                            "properties": {"sentence": {"type": "string", "minLength": 1}},
                        },
                        "else": {"properties": {"sentence": {"type": "null"}}},
                    }
                ],
                "properties": {
                    "status": {
                        "enum": ["written", "not_applicable", "unavailable"],
                    },
                    "sentence": {
                        "type": ["string", "null"],
                        "description": f"When status is written, a {FIT_MIN_WORDS}-{FIT_MAX_WORDS} word Fit paragraph.",
                    },
                },
            },
        },
    }


def _reject_unknown_fields(payload: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ValueError(f"{label} contains unknown field(s): {', '.join(unknown)}.")


def _optional_string(payload: dict[str, Any], field: str, label: str) -> str | None:
    value = payload.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{label}.{field} must be a string or null.")
    return normalize_space(value) or None


def _optional_number(payload: dict[str, Any], field: str, label: str) -> float | None:
    value = payload.get(field)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label}.{field} must be a number or null.")
    return float(value)


def _optional_integer(payload: dict[str, Any], field: str, label: str) -> int | None:
    value = payload.get(field)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{label}.{field} must be an integer or null.")
    return value


def normalize_fit_sentence(sentence: str) -> str:
    cleaned = normalize_space(sentence)
    if not cleaned:
        return ""
    if not cleaned.casefold().startswith("fit:"):
        cleaned = f"Fit: {cleaned}"
    return cleaned


def _validate_goodreads_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc.casefold() not in {"goodreads.com", "www.goodreads.com"}:
        raise ValueError("goodreads.url must be an HTTPS Goodreads URL.")
    if not parsed.path.startswith("/book/show/"):
        raise ValueError("goodreads.url must identify a Goodreads book page.")


def validate_runtime_output(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Runtime output must be a JSON object.")
    _reject_unknown_fields(payload, ROOT_FIELDS, "Runtime output")
    if payload.get("schemaVersion") != 1 or isinstance(payload.get("schemaVersion"), bool):
        raise ValueError("Runtime output schemaVersion must be 1.")
    goodreads = payload.get("goodreads")
    fit = payload.get("fit")
    if not isinstance(goodreads, dict):
        raise ValueError("Runtime output must include a goodreads object.")
    if not isinstance(fit, dict):
        raise ValueError("Runtime output must include a fit object.")
    _reject_unknown_fields(goodreads, GOODREADS_FIELDS, "goodreads")
    _reject_unknown_fields(fit, FIT_FIELDS, "fit")

    if not isinstance(goodreads.get("status"), str):
        raise ValueError("goodreads.status must be resolved, no_match, or lookup_failed.")
    if not isinstance(fit.get("status"), str):
        raise ValueError("fit.status must be written, not_applicable, or unavailable.")
    goodreads_status = normalize_space(goodreads["status"]).lower()
    fit_status = normalize_space(fit["status"]).lower()
    if goodreads_status not in {"resolved", "no_match", "lookup_failed"}:
        raise ValueError("goodreads.status must be resolved, no_match, or lookup_failed.")
    if fit_status not in {"written", "not_applicable", "unavailable"}:
        raise ValueError("fit.status must be written, not_applicable, or unavailable.")

    normalized_goodreads = {
        "status": goodreads_status,
        "url": _optional_string(goodreads, "url", "goodreads"),
        "title": _optional_string(goodreads, "title", "goodreads"),
        "author": _optional_string(goodreads, "author", "goodreads"),
        "averageRating": _optional_number(goodreads, "averageRating", "goodreads"),
        "ratingsCount": _optional_integer(goodreads, "ratingsCount", "goodreads"),
        "evidence": _optional_string(goodreads, "evidence", "goodreads"),
    }
    if goodreads_status == "resolved":
        missing = [
            field
            for field in ("url", "title", "author", "averageRating")
            if normalized_goodreads.get(field) is None
        ]
        if missing:
            raise ValueError(f"Resolved Goodreads output must include: {', '.join(missing)}.")
        _validate_goodreads_url(str(normalized_goodreads["url"]))
        rating = float(normalized_goodreads["averageRating"])
        if not 0 <= rating <= 5:
            raise ValueError("goodreads.averageRating must be between 0 and 5.")
        ratings_count = normalized_goodreads.get("ratingsCount")
        if ratings_count is not None and int(ratings_count) < 0:
            raise ValueError("goodreads.ratingsCount must be zero or greater.")
    else:
        for field in ("url", "title", "author", "averageRating", "ratingsCount"):
            if normalized_goodreads.get(field) is not None:
                raise ValueError(f"Goodreads status '{goodreads_status}' must not include {field}.")

    sentence_value = fit.get("sentence")
    if sentence_value is not None and not isinstance(sentence_value, str):
        raise ValueError("fit.sentence must be a string or null.")
    normalized_sentence = normalize_fit_sentence(sentence_value or "") or None
    if fit_status == "written":
        if not normalized_sentence:
            raise ValueError("fit.status 'written' requires a non-empty sentence.")
        word_count = len(normalized_sentence.split())
        if not FIT_MIN_WORDS <= word_count <= FIT_MAX_WORDS:
            raise ValueError(
                f"fit.sentence must contain {FIT_MIN_WORDS}-{FIT_MAX_WORDS} words when fit.status is 'written'; got {word_count}."
            )
    elif sentence_value is not None:
        raise ValueError(f"fit.status '{fit_status}' requires fit.sentence to be null or omitted.")

    return {
        "schemaVersion": 1,
        "goodreads": normalized_goodreads,
        "fit": {"status": fit_status, "sentence": normalized_sentence if fit_status == "written" else None},
    }


def build_runtime_input(prep_result: dict[str, Any]) -> dict[str, Any]:
    metadata = dict(prep_result.get("metadata") or {})
    personal_data = dict(prep_result.get("personalData") or {})
    exact_shelf = normalize_space(str(personal_data.get("exactShelfMatch") or ""))
    csv_data = dict(personal_data.get("csv") or {})
    context_budget = dict(csv_data.get("contextBudget") or {})
    artifact_paths = dict(prep_result.get("artifacts") or {})
    return {
        "schemaVersion": 1,
        "decisionContract": {
            "threshold": metadata.get("threshold", DEFAULT_THRESHOLD),
            "exactShelfMatch": exact_shelf,
            "toReadOverridesThreshold": True,
            "readAndCurrentlyReadingSuppress": True,
        },
        "audible": prep_result.get("audible") or {},
        "personalDataSummary": {
            "mode": personal_data.get("mode"),
            "privacyMode": personal_data.get("privacyMode"),
            "allowModelPersonalization": personal_data.get("allowModelPersonalization"),
            "exactShelfMatch": exact_shelf,
            "matchedEntryCount": len(personal_data.get("matchedEntries") or []),
            "csvRatedOrReviewedCount": int(csv_data.get("ratedOrReviewedCount") or 0),
            "csvReviewedCount": int(csv_data.get("reviewedCount") or 0),
            "fitEvidenceEntryCount": int(csv_data.get("fitEvidenceEntryCount") or 0),
            "fitEvidenceReviewCount": int(csv_data.get("fitEvidenceReviewCount") or 0),
            "fitContextApproxTokens": int(context_budget.get("estimatedFinalApproxTokens") or 0)
            if artifact_paths.get("fitContextPath")
            else 0,
            "notesPresent": bool(artifact_paths.get("notesPath")),
        },
        "artifactPaths": artifact_paths,
        "warnings": list(prep_result.get("warnings") or []),
        "requiredRuntimeOutputSchema": runtime_output_schema(),
    }


def build_runtime_prompt(runtime_input: dict[str, Any]) -> str:
    threshold = runtime_input["decisionContract"]["threshold"]
    exact_shelf = runtime_input["decisionContract"].get("exactShelfMatch") or ""
    artifact_paths = dict(runtime_input.get("artifactPaths") or {})
    lines = [
        "You are the skill runtime for audible-goodreads-deal-scout.",
        "Read the runtime input JSON and return JSON only.",
        "Do not invent fields outside the required runtime output schema.",
        "Use OpenClaw web/search to locate the Goodreads public book page and score when needed.",
        "Prefer Goodreads book pages over list, author, or discussion pages.",
        "Verify the Goodreads title/author match against the Audible title and author before trusting the score.",
        f"The public Goodreads threshold is {threshold:.1f}.",
    ]
    if exact_shelf == "to-read":
        lines.append("This book is already on the user's Goodreads to-read shelf. Goodreads lookup is optional for decisioning; a fit sentence is still useful.")
    else:
        lines.append("If Goodreads cannot be confidently matched, return goodreads.status = \"no_match\" or \"lookup_failed\" instead of guessing.")
    lines.extend(
        [
            "Fit generation rules:",
            "- If privacyMode is minimal, do not use personal CSV or notes content.",
            "- Read artifacts.fitEvidencePath first when present. It is a bounded, candidate-specific selection of related books plus positive and critical taste anchors.",
            "- Summarize each selected reviewText to 500 characters or fewer before reasoning from it; do not quote or mechanically truncate it in the final paragraph.",
            "- Treat review_backed entries as evidence about why the user liked or disliked something. A rating_only entry supports only that the user rated that title at that level; do not invent a reason.",
            "- Use artifacts.fitContextPath and artifacts.reviewSourcePath only when the bounded evidence is genuinely insufficient or contradictory. They contain the complete source history for fallback.",
            "- If you consult artifacts.reviewSourcePath, summarize each review-bearing entry to 500 characters or fewer before using it for fit reasoning. Do not mechanically truncate reviews.",
            "- Use artifacts.personalDataPath for summary metadata and exact shelf state, not for full taste history.",
            "- Write Fit as a compact, candidate-specific paragraph, not a generic recommendation template.",
            "- Preferred shape: 2 or 3 short sentences, roughly 45-90 words total.",
            "- Open with the candidate's distinctive subject, style, structure, or voice; do not open with 'strong fit', 'good fit', 'if you want', or 'your Goodreads history shows'.",
            "- Explain what is likely to appeal using at least one concrete personal evidence title when review-backed or rating evidence exists.",
            "- Include one candidate-specific limitation tied to personal evidence. Prefer a critical review anchor or a clearly relevant lower rating; do not manufacture a dislike.",
            "- Explain the connection between the candidate and the cited evidence instead of merely listing familiar titles.",
            "- If evidence is weak or conflicting, say that directly and use cautious language rather than broad claims about the user's taste.",
            "- If exactShelfMatch is to-read, mention that explicitly in the fit paragraph.",
            "- If there is no meaningful personal data, set fit.status to \"not_applicable\".",
            "- If the model cannot write a fit paragraph reliably, set fit.status to \"unavailable\".",
        ]
    )
    if not any(artifact_paths.get(key) for key in ("fitEvidencePath", "fitContextPath", "reviewSourcePath", "notesPath")):
        lines.append("- No personal CSV or notes artifacts are provided for this run beyond summary metadata and shelf state.")
    lines.extend(
        [
            "",
            "Required runtime output schema:",
            json.dumps(runtime_output_schema(), indent=2, sort_keys=True, ensure_ascii=False),
            "",
            "Runtime input JSON:",
            json.dumps(runtime_input, indent=2, sort_keys=True, ensure_ascii=False),
        ]
    )
    return "\n".join(lines) + "\n"


def write_runtime_contract_artifacts(artifact_dir: Path, prep_result: dict[str, Any]) -> dict[str, str]:
    runtime_input = build_runtime_input(prep_result)
    runtime_input_path = artifact_dir / "runtime-input.json"
    runtime_prompt_path = artifact_dir / "runtime-prompt.md"
    runtime_schema_path = artifact_dir / "runtime-output-schema.json"
    write_json_atomic(runtime_input_path, runtime_input)
    atomic_write_text(runtime_prompt_path, build_runtime_prompt(runtime_input))
    write_json_atomic(runtime_schema_path, runtime_output_schema())
    return {
        "runtimeInputPath": str(runtime_input_path),
        "runtimePromptPath": str(runtime_prompt_path),
        "runtimeOutputSchemaPath": str(runtime_schema_path),
    }


def attach_prepare_result_artifact(artifact_dir: Path, prep_result: dict[str, Any]) -> dict[str, Any]:
    prepare_result_path = artifact_dir / "prepare-result.json"
    prep_result.setdefault("artifacts", {})["prepareResultPath"] = str(prepare_result_path)
    write_json_atomic(prepare_result_path, prep_result)
    return prep_result


def attach_runtime_contract_artifacts(artifact_dir: Path, prep_result: dict[str, Any]) -> dict[str, Any]:
    runtime_artifacts = write_runtime_contract_artifacts(artifact_dir, prep_result)
    prep_result.setdefault("artifacts", {}).update(runtime_artifacts)
    return attach_prepare_result_artifact(artifact_dir, prep_result)
