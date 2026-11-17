#!/usr/bin/env python3
"""Create a resumable adaptive image handoff pack from a JSON spec."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from handoff_common import BACKENDS, load_json, parse_dimensions, save_json, utc_now


CAPABILITY_VALUES = {"unknown", "available", "unavailable"}
JOB_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
FACT_SENSITIVITY_VALUES = {"low", "medium", "high"}
RENDER_STRATEGY_VALUES = {"auto", "generative", "mixed", "deterministic"}
TEXT_POLICY_MODES = {"open", "allowlist"}
EXTRA_READABLE_TEXT_VALUES = {"allow", "reject"}
DEFAULT_FORBIDDEN_PATTERNS = [
    "SHA256",
    "BLAKE3",
    "checksum",
    "hash",
    "commit ID",
    "timestamp",
    "version number",
    "unapproved file path",
    "unapproved numeric identifier",
]


def normalize_string_list(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    normalized: list[str] = []
    for index, raw in enumerate(value, start=1):
        item = str(raw).strip()
        if not item:
            raise ValueError(f"{label}[{index}] must not be empty")
        if len(item) > 500 or any(character in item for character in "\r\n"):
            raise ValueError(f"{label}[{index}] must be a single line of at most 500 characters")
        if item not in normalized:
            normalized.append(item)
    return normalized


def normalize_text_policy(spec: dict[str, Any], raw: dict[str, Any], job_id: str) -> dict[str, Any]:
    default_policy = spec.get("text_policy", {})
    job_policy = raw.get("text_policy", {})
    if default_policy is None:
        default_policy = {}
    if job_policy is None:
        job_policy = {}
    if not isinstance(default_policy, dict):
        raise ValueError("spec.text_policy must be an object")
    if not isinstance(job_policy, dict):
        raise ValueError(f"text_policy must be an object for {job_id}")

    mode = str(job_policy.get("mode", default_policy.get("mode", "open")))
    if mode not in TEXT_POLICY_MODES:
        raise ValueError(f"Unsupported text_policy.mode for {job_id}: {mode}")
    extra_readable_text = str(
        job_policy.get(
            "extra_readable_text",
            default_policy.get("extra_readable_text", "reject" if mode == "allowlist" else "allow"),
        )
    )
    if extra_readable_text not in EXTRA_READABLE_TEXT_VALUES:
        raise ValueError(
            f"Unsupported text_policy.extra_readable_text for {job_id}: {extra_readable_text}"
        )

    allowed_source = (
        job_policy["allowed_text"]
        if "allowed_text" in job_policy
        else default_policy.get("allowed_text", [])
    )
    allowed_text = normalize_string_list(allowed_source, f"text_policy.allowed_text for {job_id}")
    forbidden_patterns = normalize_string_list(
        default_policy.get("forbidden_patterns", []),
        "spec.text_policy.forbidden_patterns",
    )
    for item in normalize_string_list(
        job_policy.get("forbidden_patterns", []),
        f"text_policy.forbidden_patterns for {job_id}",
    ):
        if item not in forbidden_patterns:
            forbidden_patterns.append(item)
    if mode == "allowlist" and not forbidden_patterns:
        forbidden_patterns = list(DEFAULT_FORBIDDEN_PATTERNS)

    return {
        "mode": mode,
        "allowed_text": allowed_text,
        "forbidden_patterns": forbidden_patterns,
        "extra_readable_text": extra_readable_text,
    }


def resolve_render_strategy(
    spec: dict[str, Any],
    raw: dict[str, Any],
    fact_sensitivity: str,
    text_policy: dict[str, Any],
) -> tuple[str, str, str, str]:
    requested = str(raw.get("render_strategy", spec.get("render_strategy", "auto")))
    if requested not in RENDER_STRATEGY_VALUES:
        raise ValueError(f"Unsupported render_strategy: {requested}")

    local_renderer = str(spec.get("local_renderer", "unknown"))
    if fact_sensitivity == "high" and local_renderer == "available":
        recommended = "mixed"
        reason = "high fact sensitivity with an available deterministic text renderer"
    elif fact_sensitivity == "high":
        recommended = "generative"
        reason = "high fact sensitivity but no confirmed local renderer; enforce the strict text policy"
    elif fact_sensitivity == "medium" and text_policy["mode"] == "allowlist":
        recommended = "generative"
        reason = "bounded readable text can use generation with strict allowlist QA"
    else:
        recommended = "generative"
        reason = "low factual density leaves visual generation as the simplest route"

    selected = recommended if requested == "auto" else requested
    if requested != "auto" and requested != recommended:
        reason = f"explicit {requested} override; recommended {recommended} because {reason}"
    return requested, selected, recommended, reason


def render_text_policy(job: dict[str, Any]) -> str:
    policy = job["text_policy"]
    if policy["mode"] == "open":
        return "Visual composition and decorative copy may remain flexible. Do not invent factual claims."

    allowed = "\n".join(f"- {item}" for item in policy["allowed_text"]) or "- None"
    forbidden = "\n".join(f"- {item}" for item in policy["forbidden_patterns"]) or "- None"
    if job["render_strategy"] in {"mixed", "deterministic"}:
        instruction = (
            "Create the visual background and composition only. Do not render any legible words, "
            "letters, numbers, filenames, codes, hashes, or interface values. Reserve clean areas for "
            "a deterministic text overlay. The approved copy below is layout context and must not be "
            "drawn into the generated background."
        )
    else:
        instruction = (
            "Keep visual metaphors, composition, materials, and decorative shapes creative. Any legible "
            "text must come from the approved list below. Do not add plausible-looking technical details, "
            "metrics, labels, identifiers, or decorative pseudo-text."
        )

    return f"""{instruction}

### Approved readable text

{allowed}

### Forbidden readable patterns or concepts

{forbidden}

Extra readable text policy: `{policy['extra_readable_text']}`."""


def validate_spec(spec: dict[str, Any], spec_path: Path) -> list[dict[str, Any]]:
    run_id = str(spec.get("run_id", "")).strip()
    if not run_id:
        raise ValueError("spec.run_id is required")
    if len(run_id) > 128 or any(character in run_id for character in "\r\n"):
        raise ValueError("spec.run_id must be a single line of at most 128 characters")
    spec["run_id"] = run_id
    jobs = spec.get("jobs")
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("spec.jobs must be a non-empty array")

    requested_backend = str(spec.get("backend", "auto"))
    preferred_backend = str(spec.get("preferred_backend", "chatgpt_computer_use"))
    if requested_backend not in BACKENDS:
        raise ValueError(f"Unsupported backend: {requested_backend}")
    if preferred_backend not in BACKENDS - {"auto"}:
        raise ValueError(f"Unsupported preferred_backend: {preferred_backend}")
    local_renderer = str(spec.get("local_renderer", "unknown"))
    if local_renderer not in CAPABILITY_VALUES:
        raise ValueError(f"Unsupported local_renderer: {local_renderer}")

    default_dimensions = str(spec.get("dimensions", "1080x1440"))
    parse_dimensions(default_dimensions)
    job_ids: set[str] = set()
    filenames: set[str] = set()
    normalized: list[dict[str, Any]] = []

    for index, raw in enumerate(jobs, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"jobs[{index}] must be an object")
        job_id = str(raw.get("job_id", "")).strip()
        prompt = str(raw.get("prompt", "")).strip()
        intended_filename = str(raw.get("intended_filename", "")).strip()
        if not job_id or not prompt or not intended_filename:
            raise ValueError(f"jobs[{index}] requires job_id, prompt, and intended_filename")
        if not JOB_ID_PATTERN.fullmatch(job_id):
            raise ValueError(f"Unsafe job_id: {job_id}")
        if job_id in job_ids:
            raise ValueError(f"Duplicate job_id: {job_id}")
        if intended_filename in filenames:
            raise ValueError(f"Duplicate intended_filename: {intended_filename}")
        if Path(intended_filename).name != intended_filename:
            raise ValueError(f"intended_filename must be a basename: {intended_filename}")
        if Path(intended_filename).suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            raise ValueError(f"Unsupported output format: {intended_filename}")

        dimensions = str(raw.get("dimensions", default_dimensions))
        parse_dimensions(dimensions)
        fact_sensitivity = str(raw.get("fact_sensitivity", spec.get("fact_sensitivity", "low")))
        if fact_sensitivity not in FACT_SENSITIVITY_VALUES:
            raise ValueError(f"Unsupported fact_sensitivity for {job_id}: {fact_sensitivity}")
        text_policy = normalize_text_policy(spec, raw, job_id)
        (
            requested_render_strategy,
            render_strategy,
            recommended_render_strategy,
            render_strategy_reason,
        ) = resolve_render_strategy(spec, raw, fact_sensitivity, text_policy)
        references: list[str] = []
        raw_references = raw.get("reference_paths", [])
        if not isinstance(raw_references, list):
            raise ValueError(f"reference_paths must be an array for {job_id}")
        for value in raw_references:
            reference = Path(str(value)).expanduser()
            if not reference.is_absolute():
                reference = (spec_path.parent / reference).resolve()
            if not reference.is_file():
                raise ValueError(f"Missing reference for {job_id}: {reference}")
            references.append(str(reference))

        normalized.append(
            {
                "job_id": job_id,
                "source_id": str(raw.get("source_id", job_id)),
                "platform_profile": str(raw.get("platform_profile", spec.get("platform_profile", "generic"))),
                "dimensions": dimensions,
                "prompt": prompt,
                "intended_filename": intended_filename,
                "reference_paths": references,
                "fact_sensitivity": fact_sensitivity,
                "requested_render_strategy": requested_render_strategy,
                "render_strategy": render_strategy,
                "recommended_render_strategy": recommended_render_strategy,
                "render_strategy_reason": render_strategy_reason,
                "text_policy": text_policy,
            }
        )
        job_ids.add(job_id)
        filenames.add(intended_filename)

    return normalized


def write_prompt_files(
    handoff: Path,
    spec: dict[str, Any],
    jobs: list[dict[str, Any]],
    *,
    prompt_job_ids: set[str] | None = None,
    write_master: bool = True,
) -> None:
    style_prompt = str(spec.get("style_prompt", "")).strip()
    master = [
        "# Image Generation Handoff",
        "",
        f"Run: `{spec['run_id']}`",
        "",
        "Generate one independent image per job. Keep the series visually coherent, preserve",
        "the requested facts, and wait for the next job prompt after each image.",
        "",
        "## Shared visual direction",
        "",
        style_prompt or "Use the visual direction supplied in each job prompt.",
        "",
        "## Batch contract",
        "",
        f"- Image count: {len(jobs)}",
        "- Generate one image at a time.",
        "- Do not combine several jobs into a collage.",
        "- Prefer strong visual concepts; overlay exact dense text locally when needed.",
        "- Treat readable text as source-backed data and follow each job's text policy.",
        "- Never invent hashes, checksums, identifiers, timestamps, versions, paths, or metrics.",
    ]
    if write_master:
        (handoff / "master-prompt.md").write_text("\n".join(master) + "\n", encoding="utf-8")

    prompt_dir = handoff / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    for job in jobs:
        if prompt_job_ids is not None and job["job_id"] not in prompt_job_ids:
            continue
        references = "\n".join(f"- `{path}`" for path in job["reference_paths"]) or "- None"
        content = f"""# {job['job_id']}

Create one image for this job.

- Platform: `{job['platform_profile']}`
- Target dimensions: `{job['dimensions']}`
- Intended filename: `{job['intended_filename']}`
- Fact sensitivity: `{job['fact_sensitivity']}`
- Render strategy: `{job['render_strategy']}`

## Shared visual direction

{style_prompt or 'Follow the visual direction in the job request.'}

## Job request

{job['prompt']}

## Readable text and fact policy

{render_text_policy(job)}

## Reference images approved for this job

{references}

Generate only this image and keep it consistent with the current series.
"""
        (prompt_dir / f"{job['job_id']}.md").write_text(content, encoding="utf-8")

    overlay_jobs = [
        {
            "job_id": job["job_id"],
            "dimensions": job["dimensions"],
            "intended_filename": job["intended_filename"],
            "render_strategy": job["render_strategy"],
            "approved_text": job["text_policy"]["allowed_text"],
            "status": "planned",
        }
        for job in jobs
        if job["render_strategy"] in {"mixed", "deterministic"}
    ]
    save_json(
        handoff / "reports" / "text-overlay-plan.json",
        {"run_id": spec["run_id"], "jobs": overlay_jobs},
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--resume", action="store_true", help="Reuse an existing pack with the same run_id")
    parser.add_argument(
        "--refresh-prompts",
        action="store_true",
        help="With --resume, refresh queued, failed, or needs_revision prompts from the current spec",
    )
    args = parser.parse_args()
    if args.refresh_prompts and not args.resume:
        raise SystemExit("--refresh-prompts requires --resume")

    spec_path = args.spec.expanduser().resolve()
    handoff = args.out.expanduser().resolve()
    spec = load_json(spec_path)
    try:
        jobs = validate_spec(spec, spec_path)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    state_path = handoff / "jobs.json"

    if state_path.exists():
        existing = load_json(state_path)
        if args.resume and existing.get("run_id") == spec.get("run_id"):
            if args.refresh_prompts:
                existing_jobs = {job.get("job_id"): job for job in existing.get("jobs", [])}
                if set(existing_jobs) != {job["job_id"] for job in jobs}:
                    raise SystemExit("Cannot refresh prompts when the job-id set has changed")
                refreshed_files: list[str] = []
                refreshable = {"queued", "failed", "needs_revision"}
                for job in jobs:
                    current = existing_jobs[job["job_id"]]
                    if current.get("intended_filename") != job["intended_filename"]:
                        raise SystemExit(
                            f"Cannot change intended_filename while resuming {job['job_id']}"
                        )
                    for key, value in job.items():
                        current[key] = value
                    if "text_policy_qa" not in current:
                        current["text_policy_qa"] = {
                            "status": (
                                "legacy_unrecorded"
                                if current.get("status") == "qa_passed"
                                else "pending"
                            ),
                            "observed_extra_text": [],
                            "matched_forbidden_patterns": [],
                        }
                    if current.get("status") not in refreshable:
                        continue
                    refreshed_files.append(f"prompts/{job['job_id']}.md")

                if refreshed_files:
                    write_prompt_files(
                        handoff,
                        spec,
                        jobs,
                        prompt_job_ids={Path(path).stem for path in refreshed_files},
                        write_master=False,
                    )
                    external = existing.setdefault("external_handoff", {})
                    external["approved_prompt_files"] = [
                        path
                        for path in external.get("approved_prompt_files", [])
                        if path not in refreshed_files
                    ]
                    external["status"] = "awaiting_confirmation"
                    runtime = existing.setdefault("generation_runtime", {})
                    runtime["chatgpt_transmission"] = "pending"
                    existing["schema_version"] = 3
                    existing["updated_at"] = utc_now()
                    save_json(state_path, existing)
            print(state_path)
            return
        raise SystemExit(f"Handoff already exists: {state_path}. Use --resume for the same run.")

    for directory in ("inbox", "imported", "prompts", "reports"):
        (handoff / directory).mkdir(parents=True, exist_ok=True)

    created_at = utc_now()
    state_jobs: list[dict[str, Any]] = []
    for job in jobs:
        state_jobs.append(
            {
                **job,
                "prompt_file": f"prompts/{job['job_id']}.md",
                "status": "queued",
                "attempts": 0,
                "last_error": None,
                "generation_backend": None,
                "download": {},
                "import": {},
                "visual_qa": {"status": "pending", "notes": None},
                "text_policy_qa": {
                    "status": "pending" if job["text_policy"]["mode"] == "allowlist" else "not_applicable",
                    "observed_extra_text": [],
                    "matched_forbidden_patterns": [],
                },
                "human_confirmation": "pending",
            }
        )

    state = {
        "schema_version": 3,
        "run_id": spec["run_id"],
        "mode": "adaptive_image_handoff",
        "run_status": "awaiting_backend_selection",
        "created_at": created_at,
        "updated_at": created_at,
        "source_spec": spec_path.name,
        "master_prompt_file": "master-prompt.md",
        "generation_runtime": {
            "requested_backend": str(spec.get("backend", "auto")),
            "preferred_backend": str(spec.get("preferred_backend", "chatgpt_computer_use")),
            "computer_use": "unknown",
            "chatgpt_session": "unknown",
            "built_in_imagegen": "unknown",
            "local_renderer": str(spec.get("local_renderer", "unknown")),
            "chatgpt_transmission": "pending",
            "selected_backend": None,
            "selection_status": "pending",
            "selection_reason": None,
            "resolved_at": None,
        },
        "external_handoff": {
            "destination": "ChatGPT",
            "status": "not_started",
            "approved_prompt_files": [],
            "approved_reference_paths": [],
        },
        "jobs": state_jobs,
    }
    write_prompt_files(handoff, spec, jobs)
    save_json(state_path, state)
    print(state_path)


if __name__ == "__main__":
    main()
