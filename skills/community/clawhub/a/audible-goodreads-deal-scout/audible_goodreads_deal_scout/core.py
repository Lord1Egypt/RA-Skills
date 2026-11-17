from __future__ import annotations

import csv
import json
import math
import time
import urllib.parse
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo

from .constants import (
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
    AudibleFetchResult,
    AudibleFetchError,
    SUPPORTED_AUDIBLE_FETCH_BACKENDS,
    fetch_text_with_final_url,
)
from .audible_source import (
    AudibleParseError,
    NoActivePromotionError,
    parse_audible_deal,
)
from .goodreads_csv import (
    classify_personal_match,
    effective_shelf,
    load_goodreads_csv,
)
from .fit_evidence import build_fit_evidence
from .rendering import (
    render_final_message,
)
from .runtime_contract import (
    attach_prepare_result_artifact,
    attach_runtime_contract_artifacts,
    validate_runtime_output,
)
from .settings import (
    SUPPORTED_MARKETPLACES,
    default_artifact_dir,
    load_config,
    resolve_configured_path,
    resolve_notes_text,
    validate_marketplace,
)
from .shared import (
    approx_token_count,
    atomic_write_text,
    ensure_python_version,
    normalize_review_text,
    normalize_space,
    now_iso,
    write_json_atomic,
)


AudibleFetcher = Callable[[str], tuple[str, str] | AudibleFetchResult]


DOWNSTREAM_PREP_ARTIFACTS = (
    "runtime-output.json",
    "run-and-deliver-result.json",
    "mark-emitted-result.json",
)
PREPARE_FETCH_ERRORS: dict[type[Exception], tuple[str, str]] = {
    NoActivePromotionError: ("suppress", "suppress_no_active_promotion"),
    AudibleBlockedError: ("error", "error_audible_blocked"),
    AudibleFetchError: ("error", "error_audible_fetch_failed"),
    AudibleParseError: ("error", "error_audible_parse_failed"),
}
CONFIG_PATH_KEYS = (
    "artifactDir",
    "audibleAuthPath",
    "goodreadsCsvPath",
    "notesFile",
    "preferencesPath",
    "stateFile",
)


class StateFileError(ValueError):
    pass


def export_age_days(export_path: Path, logical_run_date: date) -> int:
    modified = datetime.fromtimestamp(export_path.stat().st_mtime, tz=UTC).date()
    return max(0, (logical_run_date - modified).days)


def logical_store_date(
    spec: dict[str, str],
    raw_today: str | None = None,
    *,
    now_utc: datetime | None = None,
) -> date:
    if raw_today:
        return date.fromisoformat(raw_today)
    current_utc = now_utc or datetime.now(UTC)
    if current_utc.tzinfo is None:
        raise ValueError("now_utc must be timezone-aware.")
    return current_utc.astimezone(ZoneInfo(spec["timezone"])).date()


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
    if not path.exists():
        return default_state()
    try:
        if path.stat().st_size > 1024 * 1024:
            raise StateFileError(f"State file at {path} exceeds the 1 MiB safety limit.")
        payload = json.loads(path.read_text(encoding="utf-8"))
    except StateFileError:
        raise
    except Exception as exc:
        raise StateFileError(f"State file at {path} is not readable JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise StateFileError(f"State file at {path} must contain a JSON object.")
    merged = {**default_state(), **payload}
    for key in ("lastEmittedDealKey", "lastStaleWarningDate", "updatedAt"):
        if merged.get(key) is not None and not isinstance(merged[key], str):
            raise StateFileError(f"State field {key} must be a string or null.")
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
    successful_attempt = next(
        (
            attempt
            for attempt in reversed(normalized_attempts)
            if attempt.get("ok") is True and attempt.get("reasonCode") != "safe_redirect_followed"
        ),
        None,
    )
    first_failure = next((attempt for attempt in normalized_attempts if attempt.get("ok") is False), None)
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
    fetcher: AudibleFetcher,
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
    raise RuntimeError("Audible fetch retry loop ended without a result or error.")


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
    fit_evidence: dict[str, Any] | None,
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
    if fit_evidence is not None:
        fit_evidence_path = artifact_dir / "fit-evidence.json"
        write_json_atomic(fit_evidence_path, fit_evidence)
        artifacts["fitEvidencePath"] = str(fit_evidence_path)
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

    if (
        personal_data.get("allowModelPersonalization")
        and validated_runtime["fit"]["status"] == "written"
        and validated_runtime["fit"]["sentence"]
    ):
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
            threshold = _validated_threshold(
                (prep_result.get("metadata") or {}).get("threshold", DEFAULT_THRESHOLD)
            )
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


def _finish_prepare_result(
    *,
    artifact_dir: Path,
    cleared_downstream_artifacts: list[str],
    fetch_attempts: list[dict[str, Any]],
    prep_result: dict[str, Any],
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


def _prepare_metadata(
    spec: dict[str, str],
    store_date: date,
    invocation_mode: str,
    config_path: Path | None,
    *,
    state_path: Path | None = None,
    deal_key: str | None = None,
    short_circuit: bool = False,
) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "marketplace": spec["key"],
        "marketplaceLabel": spec["label"],
        "storeLocalDate": store_date.isoformat(),
        "timezone": spec["timezone"],
        "invocationMode": invocation_mode,
        "configPath": str(config_path) if config_path else None,
    }
    if state_path is not None:
        metadata["stateFile"] = str(state_path)
    if deal_key is not None:
        metadata["dealKey"] = deal_key
    if short_circuit:
        metadata["shortCircuit"] = True
    return metadata


def _fetch_candidate_for_prepare(
    merged: dict[str, Any],
    *,
    fetcher: AudibleFetcher | None,
    requested_url: str,
    spec: dict[str, str],
    mode: str,
    privacy_mode: str,
    store_date: date,
    warnings: list[str],
    fetch_attempts: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    retries_value = merged.get("audibleFetchRetries")
    backoff_value = merged.get("audibleFetchBackoffSeconds")
    retries = int(2 if retries_value is None else retries_value)
    backoff_seconds = float(1.0 if backoff_value is None else backoff_value)
    backend = normalize_space(str(merged.get("audibleFetchBackend") or "auto")).lower() or "auto"
    if backend not in SUPPORTED_AUDIBLE_FETCH_BACKENDS:
        append_unique_warning(warnings, f"Unsupported audibleFetchBackend '{backend}' was ignored; using auto.")
        backend = "auto"
    active_fetcher = fetcher or (
        lambda url: fetch_text_with_final_url(
            url,
            retries=0,
            backoff_seconds=backoff_seconds,
            backend=backend,
        )
    )
    try:
        candidate = fetch_audible_deal_with_retry(
            active_fetcher,
            requested_url,
            retries=retries,
            backoff_seconds=backoff_seconds,
            warnings=warnings,
            fetch_attempts=fetch_attempts,
        )
        return candidate, None
    except tuple(PREPARE_FETCH_ERRORS) as exc:
        status, reason_code = PREPARE_FETCH_ERRORS[type(exc)]
        return None, make_audible_fetch_result(
            status=status,
            reason_code=reason_code,
            message=str(exc),
            warnings=warnings,
            spec=spec,
            requested_url=requested_url,
            mode=mode,
            privacy_mode=privacy_mode,
            store_date=store_date,
        )


def _load_personal_library(
    csv_path: Path | None,
    csv_columns: dict[str, Any],
    candidate: dict[str, Any],
    *,
    store_date: date,
    state: dict[str, Any],
    invocation_mode: str,
    freshness_limit: int,
    warnings: list[str],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], int | None]:
    empty_match: dict[str, Any] = {
        "matched": False,
        "ambiguous": False,
        "effectiveShelf": "",
        "matches": [],
    }
    if csv_path is None:
        return [], {}, empty_match, None

    rows, stats = load_goodreads_csv(csv_path, csv_columns)
    personal_match = classify_personal_match(candidate, rows)
    freshness_days = export_age_days(csv_path, store_date)
    if freshness_days <= freshness_limit:
        return rows, stats, personal_match, freshness_days

    last_warning = normalize_space(str(state.get("lastStaleWarningDate") or ""))
    should_warn = invocation_mode != "scheduled"
    if invocation_mode == "scheduled":
        try:
            should_warn = not last_warning or (store_date - date.fromisoformat(last_warning)).days >= 7
        except ValueError:
            should_warn = True
    if should_warn:
        warnings.append(
            f"Your Goodreads export is {freshness_days} days old, so newer reads or shelf changes may be missing."
        )
    return rows, stats, personal_match, freshness_days


def _personal_match_short_circuit(
    personal_match: dict[str, Any],
    *,
    mode: str,
    privacy_mode: str,
    candidate: dict[str, Any],
    warnings: list[str],
    metadata: dict[str, Any],
) -> dict[str, Any] | None:
    matched_entries = list(personal_match.get("matches") or [])
    if personal_match.get("ambiguous"):
        return make_prepare_result(
            "error",
            "error_ambiguous_personal_match",
            "Conflicting Goodreads CSV shelf states were found for the same book. Clean the CSV / Goodreads shelves for that title and rerun.",
            warnings=warnings,
            audible=candidate,
            personal_data={
                "mode": mode,
                "privacyMode": privacy_mode,
                "exactShelfMatch": "",
                "matchedEntries": matched_entries,
            },
            metadata=metadata,
        )

    exact_shelf = normalize_space(str(personal_match.get("effectiveShelf") or ""))
    shelf_results = {
        "read": ("suppress_already_read", "Your Goodreads CSV already marks this book as read."),
        "currently-reading": (
            "suppress_currently_reading",
            "Your Goodreads CSV already marks this book as currently-reading.",
        ),
    }
    if exact_shelf not in shelf_results:
        return None
    reason_code, message = shelf_results[exact_shelf]
    return make_prepare_result(
        "suppress",
        reason_code,
        message,
        warnings=warnings,
        audible=candidate,
        personal_data={
            "mode": mode,
            "privacyMode": privacy_mode,
            "exactShelfMatch": exact_shelf,
            "matchedEntries": matched_entries,
        },
        metadata={**metadata, "shortCircuit": True},
    )


def _empty_context_budget(notes_text: str) -> dict[str, Any]:
    return {
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


def _build_personalization_artifacts(
    *,
    artifact_dir: Path,
    candidate: dict[str, Any],
    personal_rows: list[dict[str, Any]],
    csv_path: Path | None,
    csv_stats: dict[str, Any],
    freshness_days: int | None,
    personal_match: dict[str, Any],
    mode: str,
    privacy_mode: str,
    notes_file: str,
    notes_text: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    rated_or_reviewed_entries = [
        row
        for row in personal_rows
        if row.get("myRating", 0) > 0 or normalize_space(str(row.get("myReview") or ""))
    ]
    fit_context = build_fit_context(rated_or_reviewed_entries) if rated_or_reviewed_entries else None
    review_source = build_review_source(rated_or_reviewed_entries) if rated_or_reviewed_entries else None
    fit_evidence = build_fit_evidence(candidate, rated_or_reviewed_entries) if rated_or_reviewed_entries else None
    context_budget = (
        build_context_budget(
            rated_or_reviewed_entries,
            fit_context or build_fit_context([]),
            review_source,
            notes_text,
        )
        if csv_path
        else _empty_context_budget(notes_text)
    )
    allow_model_personalization = privacy_mode != "minimal" and bool(notes_text or rated_or_reviewed_entries)
    personal_data = {
        "mode": mode,
        "privacyMode": privacy_mode,
        "allowModelPersonalization": allow_model_personalization,
        "exactShelfMatch": str(personal_match.get("effectiveShelf") or ""),
        "matchedEntries": list(personal_match.get("matches") or []),
        "csv": {
            "path": str(csv_path) if csv_path else None,
            "freshnessDays": freshness_days,
            "stats": csv_stats,
            "ratedOrReviewedCount": len(rated_or_reviewed_entries),
            "reviewedCount": int((fit_context or {}).get("reviewCount") or 0),
            "fitContextEntryCount": int((fit_context or {}).get("entryCount") or 0),
            "reviewSourceCount": int((review_source or {}).get("entryCount") or 0),
            "fitEvidenceEntryCount": int(((fit_evidence or {}).get("selection") or {}).get("selectedEntryCount") or 0),
            "fitEvidenceReviewCount": int(((fit_evidence or {}).get("selection") or {}).get("selectedReviewCount") or 0),
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
        fit_evidence if allow_model_personalization else None,
        fit_context if allow_model_personalization else None,
        review_source if allow_model_personalization else None,
        notes_text if allow_model_personalization else "",
    )
    return personal_data, artifacts


def _resolve_file_config_paths(config_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    resolved = dict(config)
    for key in CONFIG_PATH_KEYS:
        path = resolve_configured_path(config_path, config.get(key))
        if path is not None:
            resolved[key] = str(path)
    return resolved


def _validated_threshold(value: Any) -> float:
    threshold = float(value)
    if not math.isfinite(threshold) or not 0 <= threshold <= 5:
        raise ValueError("threshold must be a finite number between 0 and 5.")
    return threshold


def prepare_run(
    options: dict[str, Any],
    *,
    fetcher: AudibleFetcher | None = None,
) -> dict[str, Any]:
    ensure_python_version()
    config_path = Path(str(options["configPath"])).expanduser().resolve() if options.get("configPath") else None
    resolved_config_path, file_config = load_config(config_path)
    file_config = _resolve_file_config_paths(resolved_config_path, file_config)
    merged = {**file_config, **{key: value for key, value in options.items() if value is not None}}
    artifact_dir = Path(str(merged.get("artifactDir") or default_artifact_dir())).expanduser()
    cleared_downstream_artifacts = clear_downstream_prepare_artifacts(artifact_dir)
    fetch_attempts: list[dict[str, Any]] = []

    def finish(prep_result: dict[str, Any], *, include_runtime_contract: bool = False) -> dict[str, Any]:
        return _finish_prepare_result(
            artifact_dir=artifact_dir,
            cleared_downstream_artifacts=cleared_downstream_artifacts,
            fetch_attempts=fetch_attempts,
            prep_result=prep_result,
            include_runtime_contract=include_runtime_contract,
        )

    marketplace = str(merged.get("audibleMarketplace") or "us").lower()
    invocation_mode = normalize_space(str(merged.get("invocationMode") or "manual")).lower() or "manual"
    try:
        spec = validate_marketplace(marketplace)
    except ValueError as exc:
        return finish(
            make_prepare_result(
                "error",
                "error_unsupported_marketplace",
                str(exc),
                warnings=[],
                metadata={
                    "marketplace": marketplace,
                    "invocationMode": invocation_mode,
                    "supportedMarketplaces": sorted(SUPPORTED_MARKETPLACES),
                },
            )
        )

    warnings: list[str] = []
    try:
        threshold = _validated_threshold(
            merged.get("threshold") if merged.get("threshold") is not None else DEFAULT_THRESHOLD
        )
    except (TypeError, ValueError) as exc:
        return finish(
            make_prepare_result(
                "error",
                "error_invalid_config",
                str(exc),
                warnings=[],
                metadata={"invocationMode": invocation_mode},
            )
        )
    privacy_mode = normalize_space(str(merged.get("privacyMode") or "normal")).lower() or "normal"
    if privacy_mode not in SUPPORTED_PRIVACY_MODES:
        return finish(
            make_prepare_result(
                "error",
                "error_invalid_config",
                f"privacyMode must be one of: {', '.join(sorted(SUPPORTED_PRIVACY_MODES))}.",
                warnings=[],
                metadata={"invocationMode": invocation_mode},
            )
        )
    requested_url = normalize_space(str(merged.get("audibleDealUrl") or spec["dealUrl"]))
    store_date = logical_store_date(spec, merged.get("today"))
    base_metadata = _prepare_metadata(spec, store_date, invocation_mode, resolved_config_path)

    notes_file = normalize_space(str(merged.get("preferencesPath") or merged.get("notesFile") or ""))
    try:
        notes_text = resolve_notes_text(notes_file, str(merged.get("notesText") or ""))
    except FileNotFoundError as exc:
        return finish(
            make_prepare_result(
                "error",
                "error_missing_notes_file",
                str(exc),
                warnings=warnings,
                metadata=base_metadata,
            )
        )

    notes_warning_chars = int(merged.get("notesWarningChars") or DEFAULT_NOTES_WARNING_CHARS)
    if notes_text and len(notes_text) > notes_warning_chars:
        warnings.append(f"Preference notes are {len(notes_text)} characters; fit generation may be slower.")

    csv_columns = dict(merged.get("csvColumns") or {})
    if merged.get("csvColumnOverrides"):
        csv_columns.update(dict(merged["csvColumnOverrides"]))
    csv_path = Path(str(merged["goodreadsCsvPath"])).expanduser() if merged.get("goodreadsCsvPath") else None
    if csv_path is not None and not csv_path.exists():
        return finish(
            make_prepare_result(
                "error",
                "error_missing_csv",
                f"Goodreads CSV not found at {csv_path}.",
                warnings=warnings,
                metadata=base_metadata,
            )
        )

    mode, ready_reason = effective_mode(csv_path, notes_text)
    candidate, fetch_error = _fetch_candidate_for_prepare(
        merged,
        fetcher=fetcher,
        requested_url=requested_url,
        spec=spec,
        mode=mode,
        privacy_mode=privacy_mode,
        store_date=store_date,
        warnings=warnings,
        fetch_attempts=fetch_attempts,
    )
    if fetch_error is not None:
        return finish(fetch_error)
    if candidate is None:
        raise RuntimeError("Audible fetch completed without a candidate or an error result.")

    state_path = Path(str(merged["stateFile"])).expanduser() if merged.get("stateFile") else None
    try:
        state = load_state(state_path)
    except StateFileError as exc:
        return finish(
            make_prepare_result(
                "error",
                "error_state_unreadable",
                str(exc),
                warnings=warnings,
                audible=candidate,
                metadata={**base_metadata, "stateFile": str(state_path) if state_path else None},
            )
        )
    deal_key = build_deal_key(spec, candidate, store_date)
    run_metadata = _prepare_metadata(
        spec,
        store_date,
        invocation_mode,
        resolved_config_path,
        state_path=state_path,
        deal_key=deal_key,
    )
    if invocation_mode == "scheduled" and state_path and state.get("lastEmittedDealKey") == deal_key:
        return finish(
            make_prepare_result(
                "suppress",
                "suppress_duplicate_scheduled_run",
                f"Scheduled run already emitted deal {deal_key}.",
                warnings=warnings,
                audible=candidate,
                personal_data={"mode": mode, "privacyMode": privacy_mode},
                metadata={**run_metadata, "shortCircuit": True},
            )
        )

    try:
        personal_rows, csv_stats, personal_match, freshness_days = _load_personal_library(
            csv_path,
            csv_columns,
            candidate,
            store_date=store_date,
            state=state,
            invocation_mode=invocation_mode,
            freshness_limit=int(merged.get("freshnessDays") or DEFAULT_FRESHNESS_DAYS),
            warnings=warnings,
        )
    except ValueError as exc:
        return finish(
            make_prepare_result(
                "error",
                "error_csv_unreadable",
                str(exc),
                warnings=warnings,
                audible=candidate,
                personal_data={"mode": mode, "privacyMode": privacy_mode},
                metadata=run_metadata,
            )
        )
    except Exception as exc:
        return finish(
            make_prepare_result(
                "error",
                "error_csv_unreadable",
                f"Could not read Goodreads CSV: {exc}",
                warnings=warnings,
                audible=candidate,
                personal_data={"mode": mode, "privacyMode": privacy_mode},
                metadata=run_metadata,
            )
        )

    short_circuit = _personal_match_short_circuit(
        personal_match,
        mode=mode,
        privacy_mode=privacy_mode,
        candidate=candidate,
        warnings=warnings,
        metadata=run_metadata,
    )
    if short_circuit is not None:
        return finish(short_circuit)

    personal_data, artifacts = _build_personalization_artifacts(
        artifact_dir=artifact_dir,
        candidate=candidate,
        personal_rows=personal_rows,
        csv_path=csv_path,
        csv_stats=csv_stats,
        freshness_days=freshness_days,
        personal_match=personal_match,
        mode=mode,
        privacy_mode=privacy_mode,
        notes_file=notes_file,
        notes_text=notes_text,
    )
    result = make_prepare_result(
        "ready",
        ready_reason,
        "Preparation complete. The skill runtime can now resolve Goodreads public score and write the final recommendation.",
        warnings=warnings,
        audible=candidate,
        personal_data=personal_data,
        artifacts=artifacts,
        metadata={
            **run_metadata,
            "threshold": threshold,
            "supportedMarketplaces": sorted(SUPPORTED_MARKETPLACES),
        },
    )
    return finish(result, include_runtime_contract=True)


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
    artifact_state_file = normalize_space(str(metadata.get("stateFile") or ""))
    if not artifact_state_file:
        raise ValueError("mark-emitted requires metadata.stateFile in the prepare artifact.")
    expected_state_path = Path(artifact_state_file).expanduser().resolve()
    requested_state_path = state_file.expanduser().resolve()
    if expected_state_path != requested_state_path:
        raise ValueError(
            f"mark-emitted refused state file {requested_state_path}; current prepare artifact uses {expected_state_path}."
        )
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
    return mark_emitted(requested_state_path, deal_key, stale_warning_date=stale_warning_date)


def show_csv_headers(export_path: Path) -> dict[str, Any]:
    with export_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return {"ok": True, "headers": list(reader.fieldnames or [])}
