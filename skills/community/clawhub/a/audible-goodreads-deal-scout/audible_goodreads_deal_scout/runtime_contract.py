from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import DEFAULT_THRESHOLD
from .shared import atomic_write_text, normalize_space, write_json_atomic


def runtime_output_schema() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "type": "object",
        "required": ["schemaVersion", "goodreads", "fit"],
        "properties": {
            "schemaVersion": {"const": 1},
            "goodreads": {
                "type": "object",
                "required": ["status"],
                "properties": {
                    "status": {
                        "enum": ["resolved", "no_match", "lookup_failed"],
                    },
                    "url": {"type": ["string", "null"]},
                    "title": {"type": ["string", "null"]},
                    "author": {"type": ["string", "null"]},
                    "averageRating": {"type": ["number", "null"]},
                    "ratingsCount": {"type": ["integer", "null"]},
                    "evidence": {"type": ["string", "null"]},
                },
            },
            "fit": {
                "type": "object",
                "required": ["status"],
                "properties": {
                    "status": {
                        "enum": ["written", "not_applicable", "unavailable"],
                    },
                    "sentence": {"type": ["string", "null"]},
                },
            },
        },
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
            "- Use artifacts.fitContextPath as the primary CSV taste artifact when that file is present. It keeps every rated/reviewed book and strips low-value metadata.",
            "- If artifacts.reviewSourcePath exists, summarize each review-bearing entry to 500 characters or fewer before using it for fit reasoning. Do not mechanically truncate reviews.",
            "- Use artifacts.personalDataPath for summary metadata and exact shelf state, not for full taste history.",
            "- Write Fit as a compact paragraph, not a generic single sentence.",
            "- Preferred shape: 2 or 3 short sentences, roughly 45-90 words total.",
            "- Mention what is likely to appeal to the user and one concrete thing they may dislike or find limiting.",
            "- Avoid low-entropy filler like 'your Goodreads history shows interest' unless followed by specific taste detail.",
            "- If exactShelfMatch is to-read, mention that explicitly in the fit paragraph.",
            "- If there is no meaningful personal data, set fit.status to \"not_applicable\".",
            "- If the model cannot write a fit paragraph reliably, set fit.status to \"unavailable\".",
        ]
    )
    if not any(artifact_paths.get(key) for key in ("fitContextPath", "reviewSourcePath", "notesPath")):
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
