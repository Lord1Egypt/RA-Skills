from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

from .constants import (
    DEFAULT_DELIVERY_POLICY,
    DEFAULT_FRESHNESS_DAYS,
    DEFAULT_NOTES_WARNING_CHARS,
    DEFAULT_THRESHOLD,
    FIT_MODEL_UNAVAILABLE,
    FIT_MODEL_UNAVAILABLE_TO_READ,
    FIT_NO_PERSONAL_DATA,
    FIT_REVIEW_SUMMARY_LIMIT,
    SUPPORTED_PRIVACY_MODES,
)
from .audible_fetch import (
    AudibleBlockedError,
    AudibleFetchError,
    SUPPORTED_AUDIBLE_FETCH_BACKENDS,
    fetch_text_with_final_url,
)
from .audible_source import (
    AudibleParseError,
    NoActivePromotionError,
    parse_audible_chip_genres,
    parse_audible_deal,
)
from .delivery import (
    build_cron_command,
    build_cron_message,
    deliver_message,
    find_matching_cron_job,
    list_cron_jobs,
    register_cron_job,
    normalize_delivery_policy,
    resolve_delivery_policy,
    resolve_delivery_settings,
    setup_configuration,
)
from .goodreads_csv import (
    classify_personal_match,
    effective_shelf,
    load_goodreads_csv,
)
from .rendering import (
    bold_visible_text,
    build_delivery_plan,
    format_runtime,
    offer_description,
    price_display,
    render_delivery_summary_message,
    render_final_message,
)
from .runtime_contract import (
    attach_prepare_result_artifact,
    attach_runtime_contract_artifacts,
    build_runtime_input,
    build_runtime_prompt,
    runtime_output_schema,
)
from .settings import (
    SUPPORTED_MARKETPLACES,
    config_template,
    default_artifact_dir,
    default_config_path,
    default_preferences_path,
    default_state_path,
    default_storage_dir,
    load_config,
    parse_csv_column_overrides,
    resolve_notes_text,
    skill_root,
    validate_marketplace,
    validate_timezone,
    workspace_root,
)
from .shared import (
    approx_token_count,
    atomic_write_text,
    ensure_parent,
    ensure_python_version,
    normalize_author_key,
    normalize_review_text,
    normalize_space,
    normalized_key,
    now_iso,
    parse_float,
    parse_int_value,
    parse_localized_price,
    parse_rating,
    prompt,
    read_json,
    split_author_roles,
    strip_html,
    truncate_text,
    write_json_atomic,
)


DOWNSTREAM_PREP_ARTIFACTS = (
    "runtime-output.json",
    "run-and-deliver-result.json",
    "mark-emitted-result.json",
)


def export_age_days(export_path: Path, logical_run_date: date) -> int:
    modified = datetime.fromtimestamp(export_path.stat().st_mtime, tz=UTC).date()
    return max(0, (logical_run_date - modified).days)


def logical_store_date(spec: dict[str, str], raw_today: str | None = None) -> date:
    if raw_today:
        return date.fromisoformat(raw_today)
    now_utc = datetime.now(UTC)
    return now_utc.astimezone(ZoneInfo(spec["timezone"])).date()


def build_deal_key(spec: dict[str, str], candidate: dict[str, Any], store_date: date) -> str:
    product_id = normalize_space(str(candidate.get("productId") or ""))
    if not product_id:
        parsed = urllib.parse.urlparse(str(candidate.get("audibleUrl") or ""))
        product_id = normalize_space(Path(parsed.path).stem or parsed.path.rstrip("/").rsplit("/", 1)[-1])
    return f"{spec['key']}:{store_date.isoformat()}:{product_id}"


def default_state() -> dict[str, Any]:
    return {
        "lastEmittedDealKey": None,
        "lastStaleWarningDate": None,
        "updatedAt": None,
    }


def load_state(path: Path | None) -> dict[str, Any]:
    if path is None:
        return default_state()
    payload = read_json(path, default_state())
    if not isinstance(payload, dict):
        return default_state()
    merged = {**default_state(), **payload}
    return merged


def save_state(path: Path, state: dict[str, Any]) -> None:
    payload = {**default_state(), **state, "updatedAt": now_iso()}
    write_json_atomic(path, payload)


def clear_downstream_prepare_artifacts(artifact_dir: Path) -> list[str]:
    cleared: list[str] = []
    for filename in DOWNSTREAM_PREP_ARTIFACTS:
        path = artifact_dir / filename
        if path.exists() and path.is_file():
            path.unlink()
            cleared.append(filename)
    return cleared


def append_unique_warning(warnings: list[str], message: str) -> None:
    normalized = normalize_space(message)
    if normalized and normalized not in warnings:
        warnings.append(normalized)


def fetch_metadata_from_attempts(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    normalized_attempts = [dict(attempt) for attempt in attempts if isinstance(attempt, dict)]
    if not normalized_attempts:
        return {}
    successful_attempt = next((attempt for attempt in reversed(normalized_attempts) if attempt.get("ok")), None)
    first_failure = next((attempt for attempt in normalized_attempts if not attempt.get("ok")), None)
    final_attempt = successful_attempt or normalized_attempts[-1]
    metadata: dict[str, Any] = {
        "backend": final_attempt.get("backend"),
        "attempts": normalized_attempts,
        "recoveredByFallback": bool(
            successful_attempt
            and first_failure
            and successful_attempt.get("backend") != first_failure.get("backend")
        ),
    }
    for source_key, target_key in (
        ("httpStatus", "httpStatus"),
        ("finalUrl", "finalUrl"),
        ("reasonCode", "reasonCode"),
    ):
        value = final_attempt.get(source_key)
        if value is None and first_failure:
            value = first_failure.get(source_key)
        if value is not None:
            metadata[target_key] = value
    if first_failure and first_failure.get("reasonCode"):
        metadata["firstFailureReasonCode"] = first_failure.get("reasonCode")
    return metadata


def make_prepare_result(
    status: str,
    reason_code: str,
    message: str,
    *,
    warnings: list[str],
    audible: dict[str, Any] | None = None,
    personal_data: dict[str, Any] | None = None,
    artifacts: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "status": status,
        "reasonCode": reason_code,
        "warnings": list(warnings),
        "audible": audible or {},
        "personalData": personal_data or {},
        "artifacts": artifacts or {},
        "metadata": metadata or {},
        "message": message,
    }


def make_audible_fetch_result(
    *,
    status: str,
    reason_code: str,
    message: str,
    warnings: list[str],
    spec: dict[str, str],
    requested_url: str,
    mode: str,
    privacy_mode: str,
    store_date: date,
) -> dict[str, Any]:
    return make_prepare_result(
        status,
        reason_code,
        message,
        warnings=warnings,
        audible={"marketplace": spec["key"], "requestedUrl": requested_url},
        personal_data={"mode": mode, "privacyMode": privacy_mode},
        artifacts={},
        metadata={
            "marketplace": spec["key"],
            "marketplaceLabel": spec["label"],
            "storeLocalDate": store_date.isoformat(),
            "timezone": spec["timezone"],
            "shortCircuit": True,
        },
    )


def attach_prepare_artifacts_for_status(
    artifact_dir: Path,
    prep_result: dict[str, Any],
    *,
    include_runtime_contract: bool = False,
) -> dict[str, Any]:
    if include_runtime_contract:
        return attach_runtime_contract_artifacts(artifact_dir, prep_result)
    return attach_prepare_result_artifact(artifact_dir, prep_result)


def scheduled_prepare_rejection(prep_result: dict[str, Any]) -> dict[str, Any] | None:
    metadata = dict(prep_result.get("metadata") or {})
    invocation_mode = normalize_space(str(metadata.get("invocationMode") or "")).lower()
    if invocation_mode != "scheduled":
        return None
    status = normalize_space(str(prep_result.get("status") or "")).lower()
    if status == "error":
        return {
            "reasonCode": "error_scheduled_prepare_failed",
            "message": "Scheduled delivery refused an error prepare result.",
            "prepareReasonCode": prep_result.get("reasonCode"),
            "prepareStatus": prep_result.get("status"),
        }
    marketplace = normalize_space(str(metadata.get("marketplace") or "")).lower() or "us"
    try:
        spec = validate_marketplace(marketplace)
        current_store_date = logical_store_date(spec)
    except Exception as exc:
        return {
            "reasonCode": "error_scheduled_prepare_date_unavailable",
            "message": f"Scheduled delivery could not validate the current Audible marketplace date: {exc}",
            "prepareReasonCode": prep_result.get("reasonCode"),
            "prepareStatus": prep_result.get("status"),
        }
    artifact_store_date = normalize_space(str(metadata.get("storeLocalDate") or ""))
    if artifact_store_date != current_store_date.isoformat():
        return {
            "reasonCode": "error_stale_scheduled_prepare_result",
            "message": (
                "Scheduled delivery refused a stale prepare artifact: "
                f"artifact storeLocalDate is {artifact_store_date or 'missing'}, "
                f"current {spec['label']} date is {current_store_date.isoformat()}."
            ),
            "prepareReasonCode": prep_result.get("reasonCode"),
            "prepareStatus": prep_result.get("status"),
            "artifactStoreLocalDate": artifact_store_date or None,
            "currentStoreLocalDate": current_store_date.isoformat(),
            "marketplace": spec["key"],
        }
    return None


def fetch_audible_deal_with_retry(
    fetcher: Callable[[str], tuple[str, str]],
    requested_url: str,
    *,
    retries: int,
    backoff_seconds: float,
    warnings: list[str],
    fetch_attempts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    retryable_errors = (AudibleFetchError, NoActivePromotionError)
    for attempt in range(max(0, retries) + 1):
        try:
            fetch_result = fetcher(requested_url)
            html_text, final_url = fetch_result
            if fetch_attempts is not None:
                fetch_attempts.extend(list(getattr(fetch_result, "attempts", []) or []))
            for warning in list(getattr(fetch_result, "warnings", []) or []):
                append_unique_warning(warnings, warning)
            return parse_audible_deal(html_text, final_url, requested_url)
        except retryable_errors as exc:
            if fetch_attempts is not None:
                fetch_attempts.extend(list(getattr(exc, "attempts", []) or []))
            if attempt >= max(0, retries):
                raise
            append_unique_warning(
                warnings,
                f"Retrying Audible daily promotion fetch after transient {type(exc).__name__}: {exc}"
            )
            if backoff_seconds > 0:
                time.sleep(backoff_seconds * (attempt + 1))


def build_fit_context_entries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        entry = {
            "entryId": index,
            "title": normalize_space(str(row.get("title") or "")),
            "author": normalize_space(str(row.get("author") or "")),
            "rating": int(row.get("myRating") or 0),
            "shelf": effective_shelf(row) or normalize_space(str(row.get("exclusiveShelf") or "")),
        }
        if normalize_review_text(str(row.get("myReview") or "")):
            entry["hasReview"] = True
        entries.append(entry)
    return entries


def build_review_source_entries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        review = normalize_review_text(str(row.get("myReview") or ""))
        if not review:
            continue
        entries.append(
            {
                "entryId": index,
                "title": normalize_space(str(row.get("title") or "")),
                "author": normalize_space(str(row.get("author") or "")),
                "rating": int(row.get("myRating") or 0),
                "shelf": effective_shelf(row) or normalize_space(str(row.get("exclusiveShelf") or "")),
                "reviewText": review,
            }
        )
    return entries


def build_fit_context(rated_or_reviewed_entries: list[dict[str, Any]]) -> dict[str, Any]:
    review_entries = build_review_source_entries(rated_or_reviewed_entries)
    review_count = sum(1 for row in rated_or_reviewed_entries if normalize_space(str(row.get("myReview") or "")))
    rating_distribution: dict[str, int] = {}
    for rating in range(1, 6):
        count = sum(1 for row in rated_or_reviewed_entries if int(row.get("myRating") or 0) == rating)
        if count:
            rating_distribution[str(rating)] = count
    return {
        "schemaVersion": 1,
        "entryCount": len(rated_or_reviewed_entries),
        "reviewCount": review_count,
        "ratingDistribution": rating_distribution,
        "entries": build_fit_context_entries(rated_or_reviewed_entries),
        "reviewSourceCount": len(review_entries),
    }


def build_review_source(rated_or_reviewed_entries: list[dict[str, Any]]) -> dict[str, Any]:
    entries = build_review_source_entries(rated_or_reviewed_entries)
    return {
        "schemaVersion": 1,
        "summaryLimitChars": FIT_REVIEW_SUMMARY_LIMIT,
        "entryCount": len(entries),
        "entries": entries,
    }


def build_context_budget(
    rated_or_reviewed_entries: list[dict[str, Any]],
    fit_context: dict[str, Any],
    review_source: dict[str, Any] | None,
    notes_text: str,
) -> dict[str, Any]:
    legacy_json = json.dumps(rated_or_reviewed_entries, sort_keys=True, ensure_ascii=False)
    fit_context_json = json.dumps(fit_context, sort_keys=True, ensure_ascii=False)
    review_source_json = json.dumps(review_source or {}, sort_keys=True, ensure_ascii=False)
    legacy_chars = len(legacy_json)
    fit_context_chars = len(fit_context_json)
    review_source_chars = len(review_source_json)
    review_count = int((review_source or {}).get("entryCount") or 0)
    estimated_review_summary_chars = review_count * FIT_REVIEW_SUMMARY_LIMIT
    estimated_final_chars = fit_context_chars + estimated_review_summary_chars
    notes_chars = len(notes_text)
    savings_chars = max(0, legacy_chars - estimated_final_chars)
    savings_percent = 0.0
    if legacy_chars:
        savings_percent = round((savings_chars / legacy_chars) * 100, 1)
    return {
        "legacyChars": legacy_chars,
        "legacyApproxTokens": approx_token_count(legacy_json),
        "fitContextBaseChars": fit_context_chars,
        "fitContextBaseApproxTokens": approx_token_count(fit_context_json),
        "reviewSourceRawChars": review_source_chars,
        "reviewSourceRawApproxTokens": approx_token_count(review_source_json),
        "estimatedReviewSummaryChars": estimated_review_summary_chars,
        "estimatedReviewSummaryApproxTokens": max(0, round(estimated_review_summary_chars / 4)),
        "estimatedFinalChars": estimated_final_chars,
        "estimatedFinalApproxTokens": max(0, round(estimated_final_chars / 4)),
        "savingsChars": savings_chars,
        "savingsPercent": savings_percent,
        "notesChars": notes_chars,
        "notesApproxTokens": approx_token_count(notes_text),
    }


def write_artifacts(
    artifact_dir: Path,
    audible: dict[str, Any],
    personal_data: dict[str, Any],
    fit_context: dict[str, Any] | None,
    review_source: dict[str, Any] | None,
    notes_text: str,
) -> dict[str, str]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    audible_path = artifact_dir / "audible.json"
    personal_path = artifact_dir / "personal-data.json"
    write_json_atomic(audible_path, audible)
    write_json_atomic(personal_path, personal_data)
    artifacts = {
        "audiblePath": str(audible_path),
        "personalDataPath": str(personal_path),
    }
    if fit_context is not None:
        fit_context_path = artifact_dir / "fit-context.json"
        write_json_atomic(fit_context_path, fit_context)
        artifacts["fitContextPath"] = str(fit_context_path)
    if review_source is not None and int(review_source.get("entryCount") or 0) > 0:
        review_source_path = artifact_dir / "review-source.json"
        write_json_atomic(review_source_path, review_source)
        artifacts["reviewSourcePath"] = str(review_source_path)
    if notes_text:
        notes_path = artifact_dir / "preferences.md"
        atomic_write_text(notes_path, notes_text.rstrip() + "\n")
        artifacts["notesPath"] = str(notes_path)
    return artifacts


def measure_context(
    csv_path: Path,
    *,
    csv_columns: dict[str, str] | None = None,
    notes_text: str = "",
    output_path: Path | None = None,
) -> dict[str, Any]:
    rows, stats = load_goodreads_csv(csv_path, csv_columns)
    rated_or_reviewed_entries = [
        row
        for row in rows
        if row.get("myRating", 0) > 0 or normalize_space(str(row.get("myReview") or ""))
    ]
    fit_context = build_fit_context(rated_or_reviewed_entries)
    review_source = build_review_source(rated_or_reviewed_entries)
    budget = build_context_budget(rated_or_reviewed_entries, fit_context, review_source, notes_text)
    if output_path is not None:
        write_json_atomic(output_path.expanduser(), fit_context)
        if int(review_source.get("entryCount") or 0) > 0:
            review_output = output_path.expanduser().with_name(output_path.expanduser().stem + ".review-source.json")
            write_json_atomic(review_output, review_source)
    return {
        "csvPath": str(csv_path),
        "totalRows": stats.get("totalRows", 0),
        "ratedOrReviewedRows": stats.get("ratedOrReviewedRows", 0),
        "reviewedRows": fit_context.get("reviewCount", 0),
        "fitContextPath": str(output_path.expanduser()) if output_path is not None else None,
        "reviewSourcePath": str(output_path.expanduser().with_name(output_path.expanduser().stem + ".review-source.json")) if output_path is not None and int(review_source.get("entryCount") or 0) > 0 else None,
        "fitContextEntryCount": fit_context.get("entryCount", 0),
        "contextBudget": budget,
    }


def normalize_fit_sentence(sentence: str) -> str:
    cleaned = normalize_space(sentence)
    if not cleaned:
        return ""
    if not cleaned.lower().startswith("fit:"):
        cleaned = f"Fit: {cleaned}"
    return cleaned


def validate_runtime_output(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Runtime output must be a JSON object.")
    if payload.get("schemaVersion") != 1:
        raise ValueError("Runtime output schemaVersion must be 1.")
    goodreads = payload.get("goodreads")
    fit = payload.get("fit")
    if not isinstance(goodreads, dict):
        raise ValueError("Runtime output must include a goodreads object.")
    if not isinstance(fit, dict):
        raise ValueError("Runtime output must include a fit object.")
    goodreads_status = normalize_space(str(goodreads.get("status") or "")).lower()
    fit_status = normalize_space(str(fit.get("status") or "")).lower()
    if goodreads_status not in {"resolved", "no_match", "lookup_failed"}:
        raise ValueError("goodreads.status must be resolved, no_match, or lookup_failed.")
    if fit_status not in {"written", "not_applicable", "unavailable"}:
        raise ValueError("fit.status must be written, not_applicable, or unavailable.")
    normalized = {
        "schemaVersion": 1,
        "goodreads": {
            "status": goodreads_status,
            "url": normalize_space(str(goodreads.get("url") or "")) or None,
            "title": normalize_space(str(goodreads.get("title") or "")) or None,
            "author": normalize_space(str(goodreads.get("author") or "")) or None,
            "averageRating": parse_float(goodreads.get("averageRating")),
            "ratingsCount": parse_int_value(goodreads.get("ratingsCount")),
            "evidence": normalize_space(str(goodreads.get("evidence") or "")) or None,
        },
        "fit": {
            "status": fit_status,
            "sentence": normalize_fit_sentence(str(fit.get("sentence") or "")) or None,
        },
    }
    normalized_goodreads = normalized["goodreads"]
    normalized_fit = normalized["fit"]
    if goodreads_status == "resolved":
        missing = [
            field
            for field in ("url", "title", "author", "averageRating")
            if not normalized_goodreads.get(field)
        ]
        if missing:
            raise ValueError(f"Resolved Goodreads output must include: {', '.join(missing)}.")
    else:
        for field in ("url", "title", "author", "averageRating", "ratingsCount"):
            if normalized_goodreads.get(field) not in (None, ""):
                raise ValueError(f"Goodreads status '{goodreads_status}' must not include {field}.")
    if fit_status == "written" and not normalized_fit.get("sentence"):
        raise ValueError("fit.status 'written' requires a non-empty sentence.")
    if fit_status != "written":
        normalized_fit["sentence"] = None
    return normalized

def finalize_skill_result(prep_result: dict[str, Any], runtime_output: dict[str, Any] | None = None) -> dict[str, Any]:
    if prep_result.get("status") in {"suppress", "error"}:
        final_result = {
            "schemaVersion": 1,
            "status": prep_result["status"],
            "reasonCode": prep_result["reasonCode"],
            "reasonText": prep_result.get("message"),
            "warnings": list(prep_result.get("warnings") or []),
            "audible": prep_result.get("audible") or {},
            "goodreads": {"status": "not_needed"},
            "fitSentence": "",
            "metadata": prep_result.get("metadata") or {},
        }
        final_result["message"] = render_final_message(final_result)
        return final_result

    validated_runtime = validate_runtime_output(runtime_output or {"schemaVersion": 1, "goodreads": {"status": "lookup_failed"}, "fit": {"status": "unavailable"}})
    personal_data = dict(prep_result.get("personalData") or {})
    exact_shelf = normalize_space(str(personal_data.get("exactShelfMatch") or ""))
    warnings = list(prep_result.get("warnings") or [])

    if validated_runtime["fit"]["status"] == "written" and validated_runtime["fit"]["sentence"]:
        fit_sentence = validated_runtime["fit"]["sentence"]
    elif exact_shelf == "to-read" and personal_data.get("allowModelPersonalization"):
        fit_sentence = FIT_MODEL_UNAVAILABLE_TO_READ
    elif personal_data.get("allowModelPersonalization"):
        fit_sentence = FIT_MODEL_UNAVAILABLE
    else:
        fit_sentence = FIT_NO_PERSONAL_DATA

    if exact_shelf == "to-read":
        reason_code = "recommend_to_read_override"
        reason_text = "Saved on your Goodreads to-read shelf."
        status = "recommend"
    else:
        goodreads = validated_runtime["goodreads"]
        if goodreads["status"] == "lookup_failed":
            reason_code = "error_goodreads_lookup_failed"
            reason_text = "Goodreads public lookup failed."
            status = "error"
        elif goodreads["status"] == "no_match":
            reason_code = "suppress_no_goodreads_match"
            reason_text = "No matching Goodreads book page could be confirmed."
            status = "suppress"
        else:
            threshold = float((prep_result.get("metadata") or {}).get("threshold") or DEFAULT_THRESHOLD)
            rating = goodreads.get("averageRating")
            if rating is None:
                reason_code = "error_goodreads_lookup_failed"
                reason_text = "Goodreads lookup did not return a usable public score."
                status = "error"
            elif rating <= threshold:
                reason_code = "suppress_below_goodreads_threshold"
                reason_text = f"Goodreads public score {rating:.2f} did not clear the {threshold:.1f} threshold."
                status = "suppress"
            else:
                reason_code = "recommend_public_threshold"
                reason_text = f"Goodreads public score {rating:.2f} cleared the {threshold:.1f} threshold."
                status = "recommend"

    final_result = {
        "schemaVersion": 1,
        "status": status,
        "reasonCode": reason_code,
        "reasonText": reason_text,
        "warnings": warnings,
        "audible": prep_result.get("audible") or {},
        "goodreads": validated_runtime["goodreads"],
        "fitSentence": fit_sentence,
        "metadata": prep_result.get("metadata") or {},
    }
    final_result["message"] = render_final_message(final_result)
    return final_result


def effective_mode(csv_path: Path | None, notes_text: str) -> tuple[str, str]:
    if csv_path and notes_text:
        return "full", "ready_full"
    if csv_path:
        return "full", "ready_full"
    if notes_text:
        return "notes", "ready_notes"
    return "public", "ready_public"


def prepare_run(
    options: dict[str, Any],
    *,
    fetcher: Callable[[str], tuple[str, str]] | None = None,
) -> dict[str, Any]:
    ensure_python_version()
    config_path = Path(options["configPath"]).resolve() if options.get("configPath") else None
    _, file_config = load_config(config_path)
    merged = {**file_config, **{key: value for key, value in options.items() if value is not None}}
    artifact_dir = Path(str(merged.get("artifactDir") or default_artifact_dir())).expanduser()
    cleared_downstream_artifacts = clear_downstream_prepare_artifacts(artifact_dir)
    fetch_attempts: list[dict[str, Any]] = []

    def finish_prepare(
        prep_result: dict[str, Any],
        *,
        include_runtime_contract: bool = False,
    ) -> dict[str, Any]:
        metadata = prep_result.setdefault("metadata", {})
        if isinstance(metadata, dict):
            if cleared_downstream_artifacts:
                metadata.setdefault("clearedDownstreamArtifacts", cleared_downstream_artifacts)
            fetch_metadata = fetch_metadata_from_attempts(fetch_attempts)
            if fetch_metadata:
                metadata.setdefault("fetch", fetch_metadata)
        return attach_prepare_artifacts_for_status(
            artifact_dir,
            prep_result,
            include_runtime_contract=include_runtime_contract,
        )

    marketplace = str(merged.get("audibleMarketplace") or "us").lower()
    try:
        spec = validate_marketplace(marketplace)
    except ValueError as exc:
        return finish_prepare(
            make_prepare_result(
                "error",
                "error_unsupported_marketplace",
                str(exc),
                warnings=[],
                metadata={
                    "marketplace": marketplace,
                    "invocationMode": normalize_space(str(merged.get("invocationMode") or "manual")).lower()
                    or "manual",
                    "supportedMarketplaces": sorted(SUPPORTED_MARKETPLACES),
                },
            )
        )

    warnings: list[str] = []
    invocation_mode = normalize_space(str(merged.get("invocationMode") or "manual")).lower() or "manual"
    threshold = float(merged.get("threshold") or DEFAULT_THRESHOLD)
    privacy_mode = normalize_space(str(merged.get("privacyMode") or "normal")).lower() or "normal"
    if privacy_mode not in SUPPORTED_PRIVACY_MODES:
        privacy_mode = "normal"
    requested_url = normalize_space(str(merged.get("audibleDealUrl") or spec["dealUrl"]))
    store_date = logical_store_date(spec, merged.get("today"))

    notes_file = normalize_space(str(merged.get("preferencesPath") or merged.get("notesFile") or ""))
    try:
        notes_text = resolve_notes_text(notes_file, str(merged.get("notesText") or ""))
    except FileNotFoundError as exc:
        return finish_prepare(
            make_prepare_result(
                "error",
                "error_missing_notes_file",
                str(exc),
                warnings=warnings,
                metadata={
                    "marketplace": spec["key"],
                    "marketplaceLabel": spec["label"],
                    "storeLocalDate": store_date.isoformat(),
                    "timezone": spec["timezone"],
                    "invocationMode": invocation_mode,
                    "configPath": str(config_path) if config_path else None,
                },
            )
        )

    notes_warning_chars = int(merged.get("notesWarningChars") or DEFAULT_NOTES_WARNING_CHARS)
    if notes_text and len(notes_text) > notes_warning_chars:
        warnings.append(
            f"Preference notes are {len(notes_text)} characters; fit generation may be slower."
        )

    csv_columns = dict(merged.get("csvColumns") or {})
    if merged.get("csvColumnOverrides"):
        csv_columns.update(dict(merged["csvColumnOverrides"]))

    csv_path = None
    if merged.get("goodreadsCsvPath"):
        csv_path = Path(str(merged["goodreadsCsvPath"])).expanduser()
        if not csv_path.exists():
            return finish_prepare(
                make_prepare_result(
                    "error",
                    "error_missing_csv",
                    f"Goodreads CSV not found at {csv_path}.",
                    warnings=warnings,
                    metadata={
                        "marketplace": spec["key"],
                        "marketplaceLabel": spec["label"],
                        "storeLocalDate": store_date.isoformat(),
                        "timezone": spec["timezone"],
                        "invocationMode": invocation_mode,
                        "configPath": str(config_path) if config_path else None,
                    },
                )
            )

    mode, ready_reason = effective_mode(csv_path, notes_text)
    audible_fetch_retries = int(merged.get("audibleFetchRetries") if merged.get("audibleFetchRetries") is not None else 2)
    audible_fetch_backoff_seconds = float(
        merged.get("audibleFetchBackoffSeconds") if merged.get("audibleFetchBackoffSeconds") is not None else 1.0
    )
    audible_fetch_backend = normalize_space(str(merged.get("audibleFetchBackend") or "auto")).lower() or "auto"
    if audible_fetch_backend not in SUPPORTED_AUDIBLE_FETCH_BACKENDS:
        append_unique_warning(
            warnings,
            f"Unsupported audibleFetchBackend '{audible_fetch_backend}' was ignored; using auto.",
        )
        audible_fetch_backend = "auto"
    active_fetcher = fetcher or (
        lambda url: fetch_text_with_final_url(
            url,
            retries=0,
            backoff_seconds=audible_fetch_backoff_seconds,
            backend=audible_fetch_backend,
        )
    )
    try:
        candidate = fetch_audible_deal_with_retry(
            active_fetcher,
            requested_url,
            retries=audible_fetch_retries,
            backoff_seconds=audible_fetch_backoff_seconds,
            warnings=warnings,
            fetch_attempts=fetch_attempts,
        )
    except NoActivePromotionError as exc:
        return finish_prepare(
            make_audible_fetch_result(
                status="suppress",
                reason_code="suppress_no_active_promotion",
                message=str(exc),
                warnings=warnings,
                spec=spec,
                requested_url=requested_url,
                mode=mode,
                privacy_mode=privacy_mode,
                store_date=store_date,
            )
        )
    except AudibleBlockedError as exc:
        return finish_prepare(
            make_audible_fetch_result(
                status="error",
                reason_code="error_audible_blocked",
                message=str(exc),
                warnings=warnings,
                spec=spec,
                requested_url=requested_url,
                mode=mode,
                privacy_mode=privacy_mode,
                store_date=store_date,
            )
        )
    except AudibleFetchError as exc:
        return finish_prepare(
            make_audible_fetch_result(
                status="error",
                reason_code="error_audible_fetch_failed",
                message=str(exc),
                warnings=warnings,
                spec=spec,
                requested_url=requested_url,
                mode=mode,
                privacy_mode=privacy_mode,
                store_date=store_date,
            )
        )
    except AudibleParseError as exc:
        return finish_prepare(
            make_audible_fetch_result(
                status="error",
                reason_code="error_audible_parse_failed",
                message=str(exc),
                warnings=warnings,
                spec=spec,
                requested_url=requested_url,
                mode=mode,
                privacy_mode=privacy_mode,
                store_date=store_date,
            )
        )

    state_path = Path(str(merged.get("stateFile") or "")).expanduser() if merged.get("stateFile") else None
    state = load_state(state_path)
    deal_key = build_deal_key(spec, candidate, store_date)
    if invocation_mode == "scheduled" and state_path and state.get("lastEmittedDealKey") == deal_key:
        return finish_prepare(
            {
                "schemaVersion": 1,
                "status": "suppress",
                "reasonCode": "suppress_duplicate_scheduled_run",
                "warnings": warnings,
                "audible": candidate,
                "personalData": {"mode": mode, "privacyMode": privacy_mode},
                "artifacts": {},
                "metadata": {
                    "marketplace": spec["key"],
                    "marketplaceLabel": spec["label"],
                    "storeLocalDate": store_date.isoformat(),
                    "timezone": spec["timezone"],
                    "dealKey": deal_key,
                    "invocationMode": invocation_mode,
                    "configPath": str(config_path) if config_path else None,
                    "stateFile": str(state_path) if state_path else None,
                    "shortCircuit": True,
                },
                "message": f"Scheduled run already emitted deal {deal_key}.",
            }
        )

    personal_rows: list[dict[str, Any]] = []
    csv_stats: dict[str, Any] = {}
    personal_match: dict[str, Any] = {"matched": False, "ambiguous": False, "effectiveShelf": "", "matches": []}
    freshness_days: int | None = None
    if csv_path:
        try:
            personal_rows, csv_stats = load_goodreads_csv(csv_path, csv_columns)
        except ValueError as exc:
            return finish_prepare(
                {
                    "schemaVersion": 1,
                    "status": "error",
                    "reasonCode": "error_csv_unreadable",
                    "warnings": warnings,
                    "audible": candidate,
                    "personalData": {"mode": mode, "privacyMode": privacy_mode},
                    "artifacts": {},
                    "metadata": {
                        "marketplace": spec["key"],
                        "marketplaceLabel": spec["label"],
                        "storeLocalDate": store_date.isoformat(),
                        "timezone": spec["timezone"],
                        "dealKey": deal_key,
                        "invocationMode": invocation_mode,
                        "configPath": str(config_path) if config_path else None,
                        "stateFile": str(state_path) if state_path else None,
                    },
                    "message": str(exc),
                }
            )
        except Exception as exc:
            return finish_prepare(
                {
                    "schemaVersion": 1,
                    "status": "error",
                    "reasonCode": "error_csv_unreadable",
                    "warnings": warnings,
                    "audible": candidate,
                    "personalData": {"mode": mode, "privacyMode": privacy_mode},
                    "artifacts": {},
                    "metadata": {
                        "marketplace": spec["key"],
                        "marketplaceLabel": spec["label"],
                        "storeLocalDate": store_date.isoformat(),
                        "timezone": spec["timezone"],
                        "dealKey": deal_key,
                        "invocationMode": invocation_mode,
                        "configPath": str(config_path) if config_path else None,
                        "stateFile": str(state_path) if state_path else None,
                    },
                    "message": f"Could not read Goodreads CSV: {exc}",
                }
            )
        personal_match = classify_personal_match(candidate, personal_rows)
        freshness_days = export_age_days(csv_path, store_date)
        if freshness_days > int(merged.get("freshnessDays") or DEFAULT_FRESHNESS_DAYS):
            last_warning = normalize_space(str(state.get("lastStaleWarningDate") or ""))
            should_warn = invocation_mode != "scheduled"
            if invocation_mode == "scheduled":
                if not last_warning:
                    should_warn = True
                else:
                    try:
                        delta = (store_date - date.fromisoformat(last_warning)).days
                    except Exception:
                        delta = 999
                    should_warn = delta >= 7
            if should_warn:
                warnings.append(
                    f"Your Goodreads export is {freshness_days} days old, so newer reads or shelf changes may be missing."
                )

    if personal_match.get("ambiguous"):
        return finish_prepare(
            {
                "schemaVersion": 1,
                "status": "error",
                "reasonCode": "error_ambiguous_personal_match",
                "warnings": warnings,
                "audible": candidate,
                "personalData": {
                    "mode": mode,
                    "privacyMode": privacy_mode,
                    "exactShelfMatch": "",
                    "matchedEntries": personal_match["matches"],
                },
                "artifacts": {},
                "metadata": {
                    "marketplace": spec["key"],
                    "marketplaceLabel": spec["label"],
                    "storeLocalDate": store_date.isoformat(),
                    "timezone": spec["timezone"],
                    "dealKey": deal_key,
                    "invocationMode": invocation_mode,
                    "configPath": str(config_path) if config_path else None,
                    "stateFile": str(state_path) if state_path else None,
                },
                "message": "Conflicting Goodreads CSV shelf states were found for the same book. Clean the CSV / Goodreads shelves for that title and rerun.",
            }
        )

    exact_shelf = str(personal_match.get("effectiveShelf") or "")
    if exact_shelf == "read":
        return finish_prepare(
            {
                "schemaVersion": 1,
                "status": "suppress",
                "reasonCode": "suppress_already_read",
                "warnings": warnings,
                "audible": candidate,
                "personalData": {
                    "mode": mode,
                    "privacyMode": privacy_mode,
                    "exactShelfMatch": exact_shelf,
                    "matchedEntries": personal_match["matches"],
                },
                "artifacts": {},
                "metadata": {
                    "marketplace": spec["key"],
                    "marketplaceLabel": spec["label"],
                    "storeLocalDate": store_date.isoformat(),
                    "timezone": spec["timezone"],
                    "dealKey": deal_key,
                    "invocationMode": invocation_mode,
                    "configPath": str(config_path) if config_path else None,
                    "stateFile": str(state_path) if state_path else None,
                    "shortCircuit": True,
                },
                "message": "Your Goodreads CSV already marks this book as read.",
            }
        )

    if exact_shelf == "currently-reading":
        return finish_prepare(
            {
                "schemaVersion": 1,
                "status": "suppress",
                "reasonCode": "suppress_currently_reading",
                "warnings": warnings,
                "audible": candidate,
                "personalData": {
                    "mode": mode,
                    "privacyMode": privacy_mode,
                    "exactShelfMatch": exact_shelf,
                    "matchedEntries": personal_match["matches"],
                },
                "artifacts": {},
                "metadata": {
                    "marketplace": spec["key"],
                    "marketplaceLabel": spec["label"],
                    "storeLocalDate": store_date.isoformat(),
                    "timezone": spec["timezone"],
                    "dealKey": deal_key,
                    "invocationMode": invocation_mode,
                    "configPath": str(config_path) if config_path else None,
                    "stateFile": str(state_path) if state_path else None,
                    "shortCircuit": True,
                },
                "message": "Your Goodreads CSV already marks this book as currently-reading.",
            }
        )

    rated_or_reviewed_entries = [
        row
        for row in personal_rows
        if row.get("myRating", 0) > 0 or normalize_space(str(row.get("myReview") or ""))
    ]
    fit_context = build_fit_context(rated_or_reviewed_entries) if rated_or_reviewed_entries else None
    review_source = build_review_source(rated_or_reviewed_entries) if rated_or_reviewed_entries else None
    context_budget = (
        build_context_budget(rated_or_reviewed_entries, fit_context or build_fit_context([]), review_source, notes_text)
        if csv_path
        else {
            "legacyChars": 0,
            "legacyApproxTokens": 0,
            "fitContextBaseChars": 0,
            "fitContextBaseApproxTokens": 0,
            "reviewSourceRawChars": 0,
            "reviewSourceRawApproxTokens": 0,
            "estimatedReviewSummaryChars": 0,
            "estimatedReviewSummaryApproxTokens": 0,
            "estimatedFinalChars": 0,
            "estimatedFinalApproxTokens": 0,
            "savingsChars": 0,
            "savingsPercent": 0.0,
            "notesChars": len(notes_text),
            "notesApproxTokens": approx_token_count(notes_text),
        }
    )

    allow_model_personalization = privacy_mode != "minimal" and bool(notes_text or rated_or_reviewed_entries)
    personal_data = {
        "mode": mode,
        "privacyMode": privacy_mode,
        "allowModelPersonalization": allow_model_personalization,
        "exactShelfMatch": exact_shelf,
        "matchedEntries": personal_match["matches"],
        "csv": {
            "path": str(csv_path) if csv_path else None,
            "freshnessDays": freshness_days,
            "stats": csv_stats,
            "ratedOrReviewedCount": len(rated_or_reviewed_entries),
            "reviewedCount": int((fit_context or {}).get("reviewCount") or 0),
            "fitContextEntryCount": int((fit_context or {}).get("entryCount") or 0),
            "reviewSourceCount": int((review_source or {}).get("entryCount") or 0),
            "contextBudget": context_budget,
        },
        "notes": {
            "path": notes_file or None,
            "chars": len(notes_text),
            "present": bool(notes_text),
        },
    }
    artifacts = write_artifacts(
        artifact_dir,
        candidate,
        personal_data,
        fit_context if allow_model_personalization else None,
        review_source if allow_model_personalization else None,
        notes_text if allow_model_personalization else "",
    )
    result = {
        "schemaVersion": 1,
        "status": "ready",
        "reasonCode": ready_reason,
        "warnings": warnings,
        "audible": candidate,
        "personalData": personal_data,
        "artifacts": artifacts,
        "metadata": {
            "marketplace": spec["key"],
            "marketplaceLabel": spec["label"],
            "timezone": spec["timezone"],
            "threshold": threshold,
            "dealKey": deal_key,
            "invocationMode": invocation_mode,
            "storeLocalDate": store_date.isoformat(),
            "configPath": str(config_path) if config_path else None,
            "stateFile": str(state_path) if state_path else None,
            "supportedMarketplaces": sorted(SUPPORTED_MARKETPLACES),
        },
        "message": "Preparation complete. The skill runtime can now resolve Goodreads public score and write the final recommendation.",
    }
    return finish_prepare(result, include_runtime_contract=True)


def mark_emitted(state_file: Path, deal_key: str, *, stale_warning_date: str | None = None) -> dict[str, Any]:
    state = load_state(state_file)
    state["lastEmittedDealKey"] = deal_key
    if stale_warning_date:
        state["lastStaleWarningDate"] = stale_warning_date
    save_state(state_file, state)
    return {"ok": True, "stateFile": str(state_file), "dealKey": deal_key, "staleWarningDate": stale_warning_date}


def mark_emitted_from_prepare(
    state_file: Path,
    prep_result: dict[str, Any],
    *,
    expected_deal_key: str | None = None,
    stale_warning_date: str | None = None,
) -> dict[str, Any]:
    metadata = dict(prep_result.get("metadata") or {})
    invocation_mode = normalize_space(str(metadata.get("invocationMode") or "")).lower()
    if invocation_mode != "scheduled":
        raise ValueError("mark-emitted requires a scheduled prepare artifact.")
    rejection = scheduled_prepare_rejection(prep_result)
    if rejection:
        raise ValueError(str(rejection.get("message") or rejection.get("reasonCode") or "prepare artifact rejected"))
    deal_key = normalize_space(str(metadata.get("dealKey") or ""))
    if not deal_key:
        raise ValueError("mark-emitted requires metadata.dealKey in the prepare artifact.")
    normalized_expected = normalize_space(str(expected_deal_key or ""))
    if normalized_expected and normalized_expected != deal_key:
        raise ValueError(
            f"mark-emitted refused deal key {normalized_expected}; current prepare artifact contains {deal_key}."
        )
    return mark_emitted(state_file, deal_key, stale_warning_date=stale_warning_date)


def show_csv_headers(export_path: Path) -> dict[str, Any]:
    with export_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return {"ok": True, "headers": list(reader.fieldnames or [])}
