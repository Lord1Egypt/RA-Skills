"""Run report rendering for Founder Signal."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

REPORT_FILENAME = "REPORT.md"
FAILED_FILENAME = "FAILED.md"
PUBLIC_RUN_REVIEW_FILENAME = "public-run-review.md"
_CANDIDATES_FILENAME = "candidates.json"
_OUTPUTS_CANDIDATES_FILENAME = "outputs/candidates.json"
_SELECTED_CANDIDATE_FILENAME = "selected-candidate.json"
_DAILY_REVIEW_FILENAME = "daily-review.md"
_SAFE = "safe_to_score_from_this_runtime"
_UNSAFE = "unsafe_to_score_from_this_runtime"


def write_report(*, run_dir: Path, artifact: Mapping[str, Any]) -> Path:
    report_path = run_dir / REPORT_FILENAME
    report_path.write_text(render_report(run_dir=run_dir, artifact=artifact), encoding="utf-8")
    return report_path


def write_failed_marker(*, run_dir: Path, artifact: Mapping[str, Any]) -> Path:
    failed_path = run_dir / FAILED_FILENAME
    failed_path.write_text(render_failed_marker(run_dir=run_dir, artifact=artifact), encoding="utf-8")
    return failed_path


def write_public_run_review(*, run_dir: Path, artifact: Mapping[str, Any]) -> Path:
    review_path = run_dir / PUBLIC_RUN_REVIEW_FILENAME
    review_path.write_text(render_public_run_review(run_dir=run_dir, artifact=artifact), encoding="utf-8")
    return review_path


def render_report(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    if _is_aggregate_run(artifact):
        return _render_aggregate_report(run_dir=run_dir, artifact=artifact)
    return _render_profile_report(run_dir=run_dir, artifact=artifact)


def render_failed_marker(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    lines = [
        "# Founder Signal Run Failed",
        "",
        f"- Run ID: {artifact.get('run_id') or run_dir.name}",
        f"- Run directory: {run_dir}",
        f"- Status: {_report_status(artifact)}",
    ]
    profile_id = str(artifact.get("profile_id") or "").strip()
    if profile_id:
        lines.append(f"- Profile ID: {profile_id}")
    product_name = str(artifact.get("product_name") or "").strip()
    if product_name:
        lines.append(f"- Product: {product_name}")
    daily_review_path = artifact.get("daily_review_path")
    if daily_review_path:
        lines.append(f"- Daily review: {daily_review_path}")
    error = artifact.get("error")
    if error:
        lines.append(f"- Error: {error}")
    failure_message = artifact.get("failure_message")
    if failure_message:
        lines.append(f"- Failure: {failure_message}")
    log_file = artifact.get("log_file")
    if log_file:
        lines.append(f"- Log file: {log_file}")
    stdout = str(artifact.get("publish_stdout") or "").rstrip()
    stderr = str(artifact.get("publish_stderr") or "").rstrip()
    if stdout:
        lines.extend(["", "## stdout", "", "```", stdout, "```"])
    if stderr:
        lines.extend(["", "## stderr", "", "```", stderr, "```"])
    return "\n".join(lines).rstrip() + "\n"


def render_public_run_review(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    if _is_aggregate_run(artifact):
        return _render_aggregate_public_run_review(run_dir=run_dir, artifact=artifact)
    return _render_profile_public_run_review(run_dir=run_dir, artifact=artifact)


def _render_profile_public_run_review(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    candidates = _load_candidates(run_dir)
    if not isinstance(candidates, list):
        candidates = []
    title_product = str(artifact.get("product_name") or artifact.get("profile_id") or "Run").strip()
    lines = [
        f"# Founder Signal Run Review - {title_product}",
        "",
        "## Summary",
        "",
        f"- Run ID: {artifact.get('run_id') or run_dir.name}",
        f"- Profile ID: {artifact.get('profile_id') or 'unknown'}",
        f"- Product: {artifact.get('product_name') or 'unknown'}",
        f"- Final status: {_report_status(artifact)}",
        f"- Candidates found: {_candidates_found(run_dir=run_dir, artifact=artifact)}",
        f"- Candidates verified: {_candidates_verified(run_dir=run_dir, artifact=artifact)}",
        f"- Action card generated: {_yes_no(artifact.get('action_card_generated'), fallback=False)}",
        f"- Draft publication attempted: {_yes_no(artifact.get('draft_publish_attempted'), fallback=False)}",
        f"- Draft publication succeeded: {_yes_no(artifact.get('draft_public_publish_succeeded'), fallback=False)}",
        "",
    ]
    failure_lines = _public_failure_lines(artifact)
    if failure_lines:
        lines.extend(["## Failure Summary", "", *failure_lines, ""])
    partial_lines = _partial_results_lines(run_dir=run_dir, artifact=artifact)
    if partial_lines:
        lines.extend(["## Partial Results", "", *partial_lines, ""])
    metrics = _discovery_metrics_lines(artifact)
    if metrics:
        lines.extend(["## Discovery Metrics", "", *[f"- {item}" for item in metrics], ""])
    candidate_lines = _public_candidate_table(candidates)
    if candidate_lines:
        lines.extend(["## Candidate Review", "", *candidate_lines, ""])
    daily_review = (run_dir / _DAILY_REVIEW_FILENAME)
    if daily_review.exists():
        lines.extend(["## Action Card", "", daily_review.read_text(encoding="utf-8").strip(), ""])
    return "\n".join(lines).rstrip() + "\n"


def _render_aggregate_public_run_review(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    profile_results = artifact.get("profile_results")
    if not isinstance(profile_results, list):
        profile_results = []
    lines = [
        "# Founder Signal Run Review",
        "",
        "## Summary",
        "",
        f"- Run ID: {artifact.get('run_id') or run_dir.name}",
        f"- Final status: {_report_status(artifact)}",
        f"- Profiles run: {len(profile_results)}",
        f"- Candidates found: {int(artifact.get('candidates_found') or 0)}",
        f"- Candidates verified: {int(artifact.get('candidates_verified') or 0)}",
        f"- Draft publication attempted: {_yes_no(artifact.get('draft_publish_attempted'), fallback=False)}",
        f"- Draft publication succeeded: {_yes_no(artifact.get('draft_public_publish_succeeded'), fallback=False)}",
        "",
        "## Profiles",
        "",
    ]
    if profile_results:
        lines.extend(
            [
                "| Profile | Status | Candidates found | Candidates verified | Action card | Draft attempted | Draft URL |",
                "| --- | --- | ---: | ---: | --- | --- | --- |",
            ]
        )
        for item in profile_results:
            if not isinstance(item, Mapping):
                continue
            lines.append(
                "| "
                + " | ".join(
                    [
                        _public_cell(item.get("profile_id") or "unknown"),
                        _public_cell(_report_status(item)),
                        str(int(item.get("candidates_found") or 0)),
                        str(int(item.get("candidates_verified") or 0)),
                        _yes_no(item.get("action_card_generated"), fallback=False),
                        _yes_no(item.get("draft_publish_attempted"), fallback=False),
                        _public_cell(item.get("draft_public_url") or item.get("draft_url") or "None"),
                    ]
                )
                + " |"
            )
    else:
        lines.append("No profile results were produced.")
    failure_lines = _public_failure_lines(artifact)
    if failure_lines:
        lines.extend(["", "## Failure Summary", "", *failure_lines])
    return "\n".join(lines).rstrip() + "\n"


def _render_profile_report(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    selected_candidate = _selected_candidate_payload(run_dir=run_dir, artifact=artifact)
    values = [
        ("Run ID", str(artifact.get("run_id") or run_dir.name)),
        ("Run datetime", str(artifact.get("created_at") or "")),
        ("Status", _report_status(artifact)),
        ("Candidates found", str(_candidates_found(run_dir=run_dir, artifact=artifact))),
        ("Platform candidate counts", _multiline_value(_platform_counts(run_dir=run_dir, artifact=artifact))),
        ("Candidates verified", str(_candidates_verified(run_dir=run_dir, artifact=artifact))),
        ("Selected candidate", _selected_candidate(run_dir=run_dir, artifact=artifact)),
        ("Discovery metrics", _multiline_value(_discovery_metrics_lines(artifact))),
        (
            "Selected candidate quality",
            _multiline_value(_selected_candidate_quality_lines(selected_candidate)),
        ),
        (
            "Skipped verified candidate decisions",
            _multiline_value(
                _skipped_verified_candidate_lines(
                    run_dir=run_dir,
                    artifact=artifact,
                    selected_candidate=selected_candidate,
                )
            ),
        ),
        ("Evidence files", _multiline_value(_evidence_files(run_dir=run_dir, artifact=artifact))),
        (
            "Action card generated",
            _yes_no(
                artifact.get("action_card_generated"),
                fallback=(run_dir / _DAILY_REVIEW_FILENAME).exists(),
            ),
        ),
        ("Action card generation mode", str(artifact.get("action_card_generation_mode") or "")),
        (
            "Draft public page published",
            _yes_no(
                artifact.get("draft_public_publish_succeeded"),
                fallback=bool(_draft_url(run_dir=run_dir, artifact=artifact)),
            ),
        ),
        (
            "Draft publish requested",
            _yes_no(
                artifact.get("draft_publish_requested"),
                fallback=bool(artifact.get("draft_publish_intent_path")),
            ),
        ),
        (
            "Draft review-page confirmation required",
            _yes_no(artifact.get("draft_publish_requires_confirmation"), fallback=False),
        ),
        (
            "Draft public publish confirmation required",
            _yes_no(artifact.get("draft_public_publish_requires_confirmation"), fallback=False),
        ),
        ("Draft publish intent", str(artifact.get("draft_publish_intent_path") or "")),
        ("Draft public URL", _draft_url(run_dir=run_dir, artifact=artifact)),
        ("Draft public publish error", str(artifact.get("draft_public_publish_error") or "")),
        ("Public run review", str(artifact.get("public_run_review_path") or "")),
        ("Failure stage", str(artifact.get("failure_stage") or "")),
        ("Public error summary", str(artifact.get("public_error_summary") or "")),
        ("Retry recommendation", str(artifact.get("retry_recommendation") or "")),
        (
            "Failures / rejected candidates",
            _multiline_value(_failures_and_rejections(run_dir=run_dir, artifact=artifact)),
        ),
        ("Safety decision", _safety_decision(artifact)),
    ]

    lines = ["# Founder Signal Run Report", ""]
    profile_id = str(artifact.get("profile_id") or "").strip()
    if profile_id:
        lines.extend(["## Profile ID", "", profile_id, ""])
    product_name = str(artifact.get("product_name") or "").strip()
    if product_name:
        lines.extend(["## Product", "", product_name, ""])
    for heading, value in values:
        lines.extend([f"## {heading}", "", value or "None", ""])
    return "\n".join(lines).rstrip() + "\n"


def _render_aggregate_report(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    profile_results = artifact.get("profile_results")
    if not isinstance(profile_results, list):
        profile_results = []
    values = [
        ("Run ID", str(artifact.get("run_id") or run_dir.name)),
        ("Run datetime", str(artifact.get("created_at") or "")),
        ("Status", _report_status(artifact)),
        ("Profiles requested", _multiline_value(_profile_ids(profile_results))),
        ("Profiles run", _multiline_value(_profile_ids(profile_results))),
        ("Profiles skipped", _multiline_value(_skipped_profiles(artifact))),
        ("Candidates found", _multiline_value(_aggregate_candidates(profile_results, "candidates_found"))),
        ("Platform candidate counts", _multiline_value(_aggregate_platform_counts(profile_results))),
        (
            "Candidates verified",
            _multiline_value(_aggregate_candidates(profile_results, "candidates_verified")),
        ),
        (
            "Discovery metrics",
            _multiline_value(_aggregate_discovery_metrics(profile_results, artifact)),
        ),
        ("Selected candidate", _multiline_value(_aggregate_selected(profile_results))),
        ("Evidence files", _multiline_value(_aggregate_evidence(profile_results))),
        (
            "Action card generated",
            _multiline_value(_aggregate_yes_no(profile_results, "action_card_generated")),
        ),
        (
            "Action card generation mode",
            _multiline_value(_aggregate_generation_modes(profile_results)),
        ),
        (
            "Draft public page published",
            _multiline_value(_aggregate_yes_no(profile_results, "draft_public_publish_succeeded")),
        ),
        (
            "Draft publish requested",
            _multiline_value(_aggregate_yes_no(profile_results, "draft_publish_requested")),
        ),
        (
            "Draft review-page confirmation required",
            _multiline_value(
                _aggregate_yes_no(profile_results, "draft_publish_requires_confirmation")
            ),
        ),
        (
            "Draft public publish confirmation required",
            _multiline_value(
                _aggregate_yes_no(profile_results, "draft_public_publish_requires_confirmation")
            ),
        ),
        ("Draft publish intent", _multiline_value(_aggregate_intents(profile_results))),
        ("Draft public URL", _multiline_value(_aggregate_urls(profile_results))),
        ("Draft public publish error", _multiline_value(_aggregate_publish_errors(profile_results))),
        ("Public run review", _multiline_value(_aggregate_public_reviews(profile_results))),
        (
            "Failures / rejected candidates",
            _multiline_value(_aggregate_failures(profile_results, artifact)),
        ),
        ("Safety decision", _safety_decision(artifact)),
    ]

    lines = ["# Founder Signal Run Report", ""]
    for heading, value in values:
        lines.extend([f"## {heading}", "", value or "None", ""])
    return "\n".join(lines).rstrip() + "\n"


def _is_aggregate_run(artifact: Mapping[str, Any]) -> bool:
    return isinstance(artifact.get("profile_results"), list)


def _profile_ids(profile_results: list[Any]) -> list[str]:
    values: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip()
        if profile_id:
            values.append(profile_id)
    return values


def _skipped_profiles(artifact: Mapping[str, Any]) -> list[str]:
    skipped = artifact.get("profiles_skipped")
    if not isinstance(skipped, list):
        return []
    return [str(item) for item in skipped if str(item).strip()]


def _aggregate_candidates(profile_results: list[Any], key: str) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        items.append(f"{profile_id}: {int(item.get(key) or 0)}")
    return items


def _aggregate_platform_counts(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        counts = item.get("platform_candidate_counts")
        if not isinstance(counts, Mapping):
            continue
        for platform, count in sorted(counts.items()):
            items.append(f"{profile_id}: {platform}: {int(count or 0)}")
    return items


def _aggregate_selected(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        selected = item.get("selected_candidate")
        if isinstance(selected, Mapping):
            label = _format_candidate(selected)
        else:
            label = str(selected or "None")
        items.append(f"{profile_id}: {label}")
    return items


def _aggregate_evidence(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        for evidence_file in item.get("evidence_files") or []:
            items.append(f"{profile_id}: {evidence_file}")
    return items


def _aggregate_generation_modes(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        mode = str(item.get("action_card_generation_mode") or "None").strip() or "None"
        items.append(f"{profile_id}: {mode}")
    return items


def _aggregate_yes_no(profile_results: list[Any], key: str) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        items.append(f"{profile_id}: {_yes_no(item.get(key), fallback=False)}")
    return items


def _aggregate_urls(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        draft_url = str(item.get("draft_public_url") or item.get("draft_url") or "").strip() or "None"
        items.append(f"{profile_id}: {draft_url}")
    return items


def _aggregate_intents(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        intent_path = str(item.get("draft_publish_intent_path") or "").strip() or "None"
        items.append(f"{profile_id}: {intent_path}")
    return items


def _aggregate_public_reviews(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        review_path = str(item.get("public_run_review_path") or "").strip() or "None"
        items.append(f"{profile_id}: {review_path}")
    return items


def _aggregate_publish_errors(profile_results: list[Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        error = str(item.get("draft_public_publish_error") or "").strip()
        if not error:
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        items.append(f"{profile_id}: {error}")
    return items


def _aggregate_failures(profile_results: list[Any], artifact: Mapping[str, Any]) -> list[str]:
    items: list[str] = []
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        for failure in _failures_and_rejections(run_dir=Path("."), artifact=item):
            items.append(f"{profile_id}: {failure}")
    for failure in artifact.get("failures") or []:
        failure_text = str(failure).strip()
        if failure_text:
            items.append(failure_text)
    return items


def _aggregate_discovery_metrics(profile_results: list[Any], artifact: Mapping[str, Any]) -> list[str]:
    lines = [
        f"total searched pages: {int(_discovery_metrics(artifact).get('searched_pages') or 0)}",
        f"total searched URLs: {len(_discovery_urls(_discovery_metrics(artifact)))}",
        f"total fresh candidates found: {int(_discovery_metrics(artifact).get('fresh_candidates_found') or 0)}",
        f"total excluded by history: {int(_discovery_metrics(artifact).get('excluded_by_history') or 0)}",
        f"total excluded by profile: {int(_discovery_metrics(artifact).get('excluded_by_profile') or 0)}",
        f"total excluded overall: {int(_discovery_metrics(artifact).get('total_excluded') or 0)}",
        f"total discovery budget pages: {int(_discovery_metrics(artifact).get('discovery_budget_pages') or 0)}",
        f"any profile exhausted discovery: {_yes_no(_discovery_metrics(artifact).get('discovery_exhausted'), fallback=False)}",
    ]
    for item in profile_results:
        if not isinstance(item, Mapping):
            continue
        profile_id = str(item.get("profile_id") or "").strip() or "unknown"
        metrics = _discovery_metrics(item)
        lines.append(
            (
                f"{profile_id}: pages={int(metrics.get('searched_pages') or 0)}, "
                f"urls={len(_discovery_urls(metrics))}, "
                f"fresh={int(metrics.get('fresh_candidates_found') or 0)}, "
                f"excluded={int(metrics.get('total_excluded') or 0)}, "
                f"budget={int(metrics.get('discovery_budget_pages') or 0)}, "
                f"exhausted={_yes_no(metrics.get('discovery_exhausted'), fallback=False)}"
            )
        )
    return lines


def _report_status(artifact: Mapping[str, Any]) -> str:
    status = str(artifact.get("status") or "").strip().lower()
    return "failed" if "fail" in status or status == "error" else "success"


def _candidates_found(*, run_dir: Path, artifact: Mapping[str, Any]) -> int:
    if artifact.get("candidates_found") is not None:
        return int(artifact["candidates_found"])
    candidates = _load_candidates(run_dir)
    return len(candidates) if isinstance(candidates, list) else 0


def _candidates_verified(*, run_dir: Path, artifact: Mapping[str, Any]) -> int:
    if artifact.get("candidates_verified") is not None:
        return int(artifact["candidates_verified"])
    candidates = _load_candidates(run_dir)
    if not isinstance(candidates, list):
        return 0
    verified = 0
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            continue
        if (
            candidate.get("verified") is True
            or str(candidate.get("status") or "").lower() == "verified"
            or str(candidate.get("read_status") or "").lower() == "verified_read_via_mirror"
        ):
            verified += 1
    return verified


def _platform_counts(*, run_dir: Path, artifact: Mapping[str, Any]) -> list[str]:
    counts = artifact.get("platform_candidate_counts")
    if not isinstance(counts, Mapping):
        counts = {}
        candidates = _load_candidates(run_dir)
        if isinstance(candidates, list):
            for candidate in candidates:
                if not isinstance(candidate, Mapping):
                    continue
                platform = str(candidate.get("platform") or candidate.get("source_platform") or "reddit").strip().lower() or "reddit"
                counts[platform] = int(counts.get(platform, 0)) + 1
    return [f"{platform}: {int(count or 0)}" for platform, count in sorted(counts.items())]


def _selected_candidate(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    selected = _selected_candidate_payload(run_dir=run_dir, artifact=artifact)
    if isinstance(selected, Mapping):
        return _format_candidate(selected)
    if isinstance(selected, str) and selected.strip():
        return selected.strip()
    selected_value = artifact.get("selected_candidate")
    if isinstance(selected_value, str) and selected_value.strip():
        return selected_value.strip()
    return "None"


def _selected_candidate_payload(*, run_dir: Path, artifact: Mapping[str, Any]) -> Mapping[str, Any] | None:
    selected = artifact.get("selected_candidate")
    if isinstance(selected, Mapping):
        return selected
    selected_file = _load_json(run_dir / _SELECTED_CANDIDATE_FILENAME)
    if isinstance(selected_file, Mapping):
        return selected_file
    return None


def _evidence_files(*, run_dir: Path, artifact: Mapping[str, Any]) -> list[str]:
    evidence_files = artifact.get("evidence_files")
    if isinstance(evidence_files, list):
        return [str(item) for item in evidence_files if str(item).strip()]
    return []


def _draft_url(*, run_dir: Path, artifact: Mapping[str, Any]) -> str:
    draft_url = str(artifact.get("draft_public_url") or artifact.get("draft_url") or "").strip()
    if draft_url:
        return draft_url
    return "None"


def _failures_and_rejections(*, run_dir: Path, artifact: Mapping[str, Any]) -> list[str]:
    items: list[str] = []
    failures = artifact.get("failures")
    if isinstance(failures, list):
        items.extend(str(item) for item in failures if str(item).strip())
    rejected = artifact.get("rejected_candidates")
    if isinstance(rejected, list):
        items.extend(str(item) for item in rejected if str(item).strip())
    error = str(artifact.get("error") or "").strip()
    if error:
        items.append(error)
    daily_review_path = str(artifact.get("daily_review_path") or "").strip()
    if daily_review_path:
        items.append(f"Preserved daily review: {daily_review_path}")
    publish_error = str(artifact.get("draft_public_publish_error") or "").strip()
    if publish_error:
        items.append(f"Draft publish failed: {publish_error}")
    deduped: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _discovery_metrics(artifact: Mapping[str, Any]) -> Mapping[str, Any]:
    metrics = artifact.get("discovery_metrics")
    if isinstance(metrics, Mapping):
        return metrics
    return {}


def _discovery_urls(metrics: Mapping[str, Any]) -> list[str]:
    urls = metrics.get("searched_urls")
    if not isinstance(urls, list):
        return []
    return [str(item) for item in urls if str(item).strip()]


def _discovery_metrics_lines(artifact: Mapping[str, Any]) -> list[str]:
    metrics = _discovery_metrics(artifact)
    if not metrics:
        return []
    urls = _discovery_urls(metrics)
    return [
        f"searched pages: {int(metrics.get('searched_pages') or 0)}",
        f"searched URLs: {len(urls)}",
        f"fresh candidates found: {int(metrics.get('fresh_candidates_found') or 0)}",
        f"excluded by history: {int(metrics.get('excluded_by_history') or 0)}",
        f"excluded by profile: {int(metrics.get('excluded_by_profile') or 0)}",
        f"total excluded: {int(metrics.get('total_excluded') or 0)}",
        f"discovery budget pages: {int(metrics.get('discovery_budget_pages') or 0)}",
        f"discovery exhausted: {_yes_no(metrics.get('discovery_exhausted'), fallback=False)}",
    ]


def _selected_candidate_quality_lines(selected_candidate: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(selected_candidate, Mapping):
        return []
    structured = selected_candidate.get("structured_evidence")
    score_breakdown = selected_candidate.get("score_breakdown")
    agent_review = selected_candidate.get("agent_review")
    lines: list[str] = []
    extraction_quality = ""
    if isinstance(structured, Mapping):
        extraction_quality = str(structured.get("extraction_quality") or "").strip()
    if extraction_quality:
        lines.append(f"structured extraction quality: {extraction_quality}")
    if isinstance(structured, Mapping) and structured.get("post_age_days") is not None:
        lines.append(f"post age days: {int(structured.get('post_age_days') or 0)}")
    relevance_line = _deterministic_relevance_line(score_breakdown)
    if relevance_line:
        lines.append(relevance_line)
    if isinstance(agent_review, Mapping):
        score_total = int(selected_candidate.get("agent_review_score_total") or 0)
        lines.append(f"agent review score: {score_total}/25")
        lines.extend(_agent_review_lines(agent_review))
    selection_eligible = selected_candidate.get("selection_eligible")
    if selection_eligible is not None:
        lines.append(
            f"selection eligible: {_yes_no(selection_eligible, fallback=False)}"
        )
    gate_reason = str(selected_candidate.get("selection_gate_reason") or "").strip()
    lines.append(f"selection gate reason: {gate_reason or 'passed'}")
    rejection_signals = _string_list(selected_candidate.get("rejection_signals"))
    lines.append(
        "rejection signals: "
        + (", ".join(rejection_signals) if rejection_signals else "none")
    )
    return lines


def _skipped_verified_candidate_lines(
    *,
    run_dir: Path,
    artifact: Mapping[str, Any],
    selected_candidate: Mapping[str, Any] | None,
) -> list[str]:
    selected_candidate_id = ""
    if isinstance(selected_candidate, Mapping):
        selected_candidate_id = str(selected_candidate.get("candidate_id") or "").strip()
    items: list[str] = []
    candidates = _load_candidates(run_dir)
    if not isinstance(candidates, list):
        return items
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            continue
        if not _is_verified_candidate(candidate):
            continue
        candidate_id = str(candidate.get("candidate_id") or "").strip()
        if candidate_id and candidate_id == selected_candidate_id:
            continue
        reasons = _candidate_skip_reasons(candidate)
        if not reasons:
            continue
        label = _format_candidate(candidate)
        items.append(f"{label}: {'; '.join(reasons)}")
    return items


def _is_verified_candidate(candidate: Mapping[str, Any]) -> bool:
    if candidate.get("verified") is True:
        return True
    if str(candidate.get("status") or "").strip().lower() == "verified":
        return True
    read_status = str(candidate.get("read_status") or "").strip().lower()
    if read_status.startswith("verified"):
        return True
    return False


def _candidate_skip_reasons(candidate: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    gate_reason = str(candidate.get("selection_gate_reason") or "").strip()
    if gate_reason:
        reasons.append(f"selection gate: {_humanize_key(gate_reason)}")
    rejection_signals = _string_list(candidate.get("rejection_signals"))
    if rejection_signals:
        reasons.append(f"rejection signals: {', '.join(rejection_signals)}")
    agent_review = candidate.get("agent_review")
    if isinstance(agent_review, Mapping):
        reject_reason = str(agent_review.get("reject_reason") or "").strip()
        if reject_reason:
            reasons.append(f"agent reject reason: {reject_reason}")
        reason = str(agent_review.get("reason") or "").strip()
        if reason and gate_reason:
            reasons.append(f"agent review reason: {reason}")
    return reasons


def _deterministic_relevance_line(score_breakdown: Any) -> str:
    if not isinstance(score_breakdown, Mapping):
        return ""
    title_relevance = score_breakdown.get("title_relevance")
    body_relevance = score_breakdown.get("body_relevance")
    relevance_total = score_breakdown.get("relevance_to_draft")
    if title_relevance is not None or body_relevance is not None:
        title_value = int(title_relevance or 0)
        body_value = int(body_relevance or 0)
        if relevance_total is not None:
            return (
                "deterministic title/body relevance: "
                f"title {title_value}, body {body_value}, total {int(relevance_total or 0)}"
            )
        return f"deterministic title/body relevance: title {title_value}, body {body_value}"
    if relevance_total is not None:
        return f"deterministic title/body relevance: overall {int(relevance_total or 0)}"
    return ""


def _agent_review_lines(agent_review: Mapping[str, Any]) -> list[str]:
    metrics = []
    for key in (
        "profile_fit",
        "audience_match",
        "pain_relevance",
        "reply_opportunity",
        "confidence",
    ):
        if key in agent_review:
            metrics.append(f"{_humanize_key(key)} {int(agent_review.get(key) or 0)}")
    lines: list[str] = []
    if metrics:
        lines.append("agent review components: " + ", ".join(metrics))
    reason = str(agent_review.get("reason") or "").strip()
    if reason:
        lines.append(f"agent review reason: {reason}")
    reject_reason = str(agent_review.get("reject_reason") or "").strip()
    if reject_reason:
        lines.append(f"agent reject reason: {reject_reason}")
    return lines


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _humanize_key(value: str) -> str:
    return value.replace("_", " ").strip()


def _safety_decision(artifact: Mapping[str, Any]) -> str:
    value = str(artifact.get("safety_decision") or "").strip()
    if value in {_SAFE, _UNSAFE}:
        return value
    return _UNSAFE


def _yes_no(value: Any, *, fallback: bool) -> str:
    if value is None:
        return "yes" if fallback else "no"
    return "yes" if bool(value) else "no"


def _multiline_value(items: list[str]) -> str:
    if not items:
        return "None"
    return "\n".join(f"- {item}" for item in items)


def _public_failure_lines(artifact: Mapping[str, Any]) -> list[str]:
    lines: list[str] = []
    has_failure = _report_status(artifact) == "failed" or bool(artifact.get("run_completed_with_errors"))
    if has_failure:
        lines.append(f"- Run status: {_report_status(artifact)}")
    failure_stage = str(artifact.get("failure_stage") or "").strip()
    if has_failure and failure_stage:
        lines.append(f"- Failure stage: {failure_stage}")
    last_completed_stage = str(artifact.get("last_completed_stage") or "").strip()
    if has_failure and last_completed_stage:
        lines.append(f"- Last completed stage: {last_completed_stage}")
    public_error_summary = str(artifact.get("public_error_summary") or "").strip()
    if has_failure and public_error_summary:
        lines.append(f"- Public error summary: {public_error_summary}")
    retry = str(artifact.get("retry_recommendation") or "").strip()
    if has_failure and retry:
        lines.append(f"- Retry recommendation: {retry}")
    publish_error = str(artifact.get("draft_public_publish_error") or "").strip()
    if publish_error:
        lines.append("- Draft publish failure: Draft publication failed after the local review artifact was generated.")
    return lines


def _partial_results_lines(*, run_dir: Path, artifact: Mapping[str, Any]) -> list[str]:
    return [
        f"- Candidates discovered before finalization: {_candidates_found(run_dir=run_dir, artifact=artifact)}",
        f"- Candidates verified before finalization: {_candidates_verified(run_dir=run_dir, artifact=artifact)}",
        f"- Action card generated: {_yes_no(artifact.get('action_card_generated'), fallback=False)}",
        f"- Partial results available: {_yes_no(artifact.get('partial_results_available'), fallback=False)}",
    ]


def _public_candidate_table(candidates: list[Any]) -> list[str]:
    if not candidates:
        return []
    rows = [
        "| Candidate | Platform | Status | Score | Source |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            continue
        rows.append(
            "| "
            + " | ".join(
                [
                    _public_cell(candidate.get("candidate_id") or "unknown"),
                    _public_cell(candidate.get("platform") or candidate.get("source_platform") or "unknown"),
                    _public_cell(candidate.get("read_status") or candidate.get("status") or "unknown"),
                    str(int(candidate.get("score_total") or candidate.get("agent_review_score_total") or 0)),
                    _public_cell(candidate.get("source_url") or candidate.get("reddit_url") or ""),
                ]
            )
            + " |"
        )
    return rows


def _public_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def _format_candidate(candidate: Mapping[str, Any]) -> str:
    for key in ("candidate_id", "id", "username", "title", "url"):
        value = str(candidate.get(key) or "").strip()
        if value:
            return value
    return json.dumps(dict(candidate), sort_keys=True)


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _load_candidates(run_dir: Path) -> Any:
    candidates = _load_json(run_dir / _OUTPUTS_CANDIDATES_FILENAME)
    if candidates is not None:
        return candidates
    return _load_json(run_dir / _CANDIDATES_FILENAME)
