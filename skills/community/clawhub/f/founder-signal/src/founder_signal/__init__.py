"""Founder Signal package scaffold."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .action_card import SelectedCandidate, action_card_generation_mode, generate_action_card
from .candidate_history import load_excluded_source_ids, record_discovered_candidates
from .candidate_discovery import DiscoveryResult, discover_candidates
from .config import load_profiles
from .draft_publish import publish_daily_review_to_draft, write_public_draft_publish_intent
from .models import FounderSignalConfig
from .platforms import get_adapter
from .reddit_fetcher import (
    fetch_reddit_evidence,
    persist_failed_evidence_read,
    persist_verified_text_snapshot,
    to_eddrit_url,
)
from .report import write_failed_marker, write_public_run_review, write_report
from .scoring import (
    VERIFIED_READ_STATUSES,
    AgentReviewer,
    built_in_agent_reviewer,
    score_candidates,
)


def run_once(
    root_dir: Path,
    run_dir: Path,
    *,
    selected_profile_id: str | None = None,
    draft_runner=None,
    agent_reviewer: AgentReviewer | None = None,
) -> dict:
    """Run Founder Signal for one selected profile or all enabled profiles."""
    effective_agent_reviewer = agent_reviewer or built_in_agent_reviewer
    artifact = _new_root_artifact(run_dir)
    try:
        profiles = load_profiles(root_dir, selected_profile_id=selected_profile_id)
    except Exception as exc:
        artifact.update(
            {
                "status": "failed",
                "error": str(exc),
                "run_completed_with_errors": True,
                "failure_stage": "profile_loading",
                "public_error_summary": _sanitize_public_error(exc, stage="profile_loading"),
                "retry_recommendation": _retry_recommendation("profile_loading"),
                "next_step": "fix_configuration_and_retry",
                "failures": [str(exc)],
            }
        )
        _finalize_public_review_and_publish(
            root_dir=root_dir,
            run_dir=run_dir,
            artifact=artifact,
            profile_id=selected_profile_id or "aggregate",
            draft_runner=draft_runner,
        )
        _write_run_artifacts(run_dir=run_dir, artifact=artifact, include_failed_marker=True)
        return artifact

    artifact["profiles_requested"] = [profile.profile_id for profile, _ in profiles]

    profile_results: list[dict] = []
    for profile, profile_path in profiles:
        profile_run_dir = run_dir / "profiles" / profile.profile_id
        profile_results.append(
            run_profile_once(
                root_dir=root_dir,
                run_dir=profile_run_dir,
                profile=profile,
                profile_path=profile_path,
                draft_runner=draft_runner,
                agent_reviewer=effective_agent_reviewer,
            )
        )

    artifact.update(_summarize_profile_results(profile_results))
    public_run_review_path = write_public_run_review(run_dir=run_dir, artifact=artifact)
    artifact.update(
        {
            "public_run_review_generated": True,
            "public_run_review_path": str(public_run_review_path),
        }
    )
    _write_run_artifacts(
        run_dir=run_dir,
        artifact=artifact,
        include_failed_marker=artifact["status"] == "failed",
    )
    return artifact


def run_profile_once(
    *,
    root_dir: Path,
    run_dir: Path,
    profile: FounderSignalConfig,
    profile_path: Path,
    draft_runner=None,
    agent_reviewer: AgentReviewer | None = None,
) -> dict:
    """Run the Founder Signal loop for one product profile."""
    artifact = _new_profile_artifact(run_dir=run_dir, profile=profile, profile_path=profile_path)
    outputs_dir = run_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    selected_candidate_path = run_dir / "selected-candidate.json"
    candidates_path = outputs_dir / "candidates.json"
    failure_stage = "initialization"

    try:
        failure_stage = "candidate_history"
        excluded_source_ids, exclusion_counts = load_excluded_source_ids(
            root_dir=root_dir,
            profile_id=profile.profile_id,
            profile_excluded_urls_by_platform={
                platform: platform_config.excluded_urls
                for platform, platform_config in profile.platforms.items()
            },
            ttl_days=profile.history_ttl_days,
        )
        artifact.update(exclusion_counts)
        artifact["discovery_mode"] = profile.discovery_mode

        failure_stage = "candidate_discovery"
        discovery_result = discover_candidates(
            profile,
            excluded_reddit_urls={
                item.removeprefix("reddit:")
                for item in excluded_source_ids
                if item.startswith("reddit:")
            },
            profile_excluded_reddit_urls={
                str(url).strip() for url in profile.excluded_reddit_urls if str(url).strip()
            },
            history_excluded_reddit_urls={
                item.removeprefix("reddit:")
                for item in excluded_source_ids
                if item.startswith("reddit:")
            },
            excluded_source_ids=excluded_source_ids,
        )
        discovered_candidates = discovery_result.candidates
        artifact["candidates_found"] = len(discovered_candidates)
        artifact["discovery_metrics"] = discovery_result.metrics
        artifact["last_completed_stage"] = "candidate_discovery"

        hydrated_candidates: list[dict] = []
        rejected_candidates: list[str] = []
        evidence_files: list[str] = []
        for candidate in discovered_candidates:
            failure_stage = "candidate_verification"
            platform = str(candidate.get("platform") or "reddit")
            adapter = get_adapter(platform)
            candidate_for_hydration = dict(candidate)
            if platform == "reddit":
                source_url = str(
                    candidate_for_hydration.get("source_url")
                    or candidate_for_hydration.get("reddit_url")
                    or ""
                ).strip()
                if source_url:
                    candidate_for_hydration.setdefault("source_url", source_url)
                    candidate_for_hydration.setdefault("reddit_url", source_url)
                    candidate_for_hydration.setdefault("source_id", f"reddit:{source_url}")
                    candidate_for_hydration.setdefault("source_platform", "reddit")
                    candidate_for_hydration.setdefault("platform", "reddit")
            try:
                result = adapter.hydrate_candidate(candidate_for_hydration, run_dir)
            except Exception as exc:
                if platform != "reddit":
                    raise
                result = persist_failed_evidence_read(
                    candidate_id=str(candidate_for_hydration["candidate_id"]),
                    reddit_url=str(
                        candidate_for_hydration.get("reddit_url")
                        or candidate_for_hydration.get("source_url")
                        or ""
                    ),
                    run_dir=run_dir,
                    error_message=str(exc),
                )
            _ensure_evidence_files(result)
            evidence_files.extend(
                str(path)
                for path in (
                    result.raw_html_path,
                    result.text_snapshot_path,
                    result.source_url_path,
                    result.evidence_url_path,
                )
            )
            structured_path = getattr(result, "structured_evidence_path", None)
            if structured_path is not None:
                evidence_files.append(str(structured_path))
            hydrated_candidate = {
                **candidate_for_hydration,
                "platform": str(candidate_for_hydration.get("platform") or result.platform),
                "source_platform": str(candidate_for_hydration.get("source_platform") or result.platform),
                "source_id": str(
                    candidate_for_hydration.get("source_id") or f"{result.platform}:{result.source_url}"
                ),
                "reddit_url": (
                    result.source_url
                    if str(candidate_for_hydration.get("platform") or result.platform) == "reddit"
                    else str(candidate_for_hydration.get("reddit_url") or "")
                ),
                "source_url": result.source_url,
                "evidence_url": result.evidence_url,
                "read_status": result.status,
                "status": result.status,
                "verified": result.status in VERIFIED_READ_STATUSES,
                "evidence_snapshot_path": str(result.text_snapshot_path),
                "raw_html_path": str(result.raw_html_path),
                "source_url_path": str(result.source_url_path),
                "evidence_url_path": str(result.evidence_url_path),
                "structured_evidence_path": str(structured_path) if structured_path else "",
                "structured_evidence": (
                    result.structured_evidence.to_dict()
                    if getattr(result, "structured_evidence", None) is not None
                    else None
                ),
                "verification_method": str(candidate_for_hydration.get("verification_method") or ""),
                "verified_by": str(candidate_for_hydration.get("verified_by") or ""),
            }
            hydrated_candidates.append(hydrated_candidate)
            if result.status not in VERIFIED_READ_STATUSES:
                rejected_candidates.append(str(candidate["candidate_id"]))

        artifact["last_completed_stage"] = "candidate_verification"
        failure_stage = "candidate_scoring"
        score_outcome = score_candidates(
            hydrated_candidates,
            profile,
            agent_reviewer=agent_reviewer,
        )
        scored_by_id = {
            str(candidate["candidate_id"]): candidate for candidate in score_outcome.scored_candidates
        }
        final_candidates = [
            scored_by_id.get(str(candidate["candidate_id"]), candidate)
            for candidate in hydrated_candidates
        ]

        candidates_path.write_text(json.dumps(final_candidates, indent=2) + "\n", encoding="utf-8")
        artifact["last_completed_stage"] = "candidate_scoring"
        failure_stage = "candidate_history_recording"
        history_path = record_discovered_candidates(
            root_dir=root_dir,
            profile_id=profile.profile_id,
            run_id=run_dir.parent.parent.name,
            candidates=final_candidates or discovered_candidates,
        )
        artifact["candidate_history_path"] = str(history_path)

        selected_candidate = score_outcome.selected_candidate
        if selected_candidate is not None:
            failure_stage = "action_card_generation"
            selected_payload = {
                "platform": selected_candidate.get("platform", "reddit"),
                "source_platform": selected_candidate.get(
                    "source_platform", selected_candidate.get("platform", "reddit")
                ),
                "source_url": selected_candidate["source_url"],
                "source_id": selected_candidate.get("source_id", ""),
                "reddit_url": selected_candidate.get("reddit_url", ""),
                "evidence_url": selected_candidate["evidence_url"],
                "read_status": selected_candidate["read_status"],
                "score_total": selected_candidate["score_total"],
                "score_breakdown": selected_candidate["score_breakdown"],
                "agent_review": selected_candidate.get("agent_review", {}),
                "agent_review_score_total": selected_candidate.get("agent_review_score_total", 0),
                "evidence_snapshot_path": selected_candidate["evidence_snapshot_path"],
                "structured_evidence_path": selected_candidate.get("structured_evidence_path", ""),
                "structured_evidence": selected_candidate.get("structured_evidence"),
                "candidate_id": selected_candidate.get("candidate_id", ""),
                "selection_eligible": selected_candidate.get("selection_eligible"),
                "selection_gate_reason": selected_candidate.get("selection_gate_reason", ""),
                "rejection_signals": selected_candidate.get("rejection_signals", []),
                "profile_id": profile.profile_id,
                "product_name": profile.product_name,
            }
            mode = action_card_generation_mode(selected_payload)
            if mode:
                selected_payload["action_card_generation_mode"] = mode
                selected_candidate["action_card_generation_mode"] = mode
            selected_candidate_path.write_text(
                json.dumps(selected_payload, indent=2) + "\n",
                encoding="utf-8",
            )
            daily_review_path = generate_action_card(
                run_dir,
                selected_payload,
                product_name=profile.product_name,
                profile_id=profile.profile_id,
            )
        else:
            daily_review_path = None

        artifact.update(
            {
                "candidates_verified": len(score_outcome.scored_candidates),
                "platform_candidate_counts": _platform_counts(final_candidates),
                "selected_candidate": selected_candidate or "",
                "selected_candidate_path": (
                    str(selected_candidate_path) if selected_candidate_path.exists() else ""
                ),
                "evidence_files": evidence_files,
                "rejected_candidates": rejected_candidates,
                "agent_review_used": any(
                    bool(candidate.get("agent_review")) for candidate in score_outcome.scored_candidates
                ),
                "action_card_generated": daily_review_path is not None,
                "action_card_generation_mode": (
                    selected_candidate.get("action_card_generation_mode", "")
                    if daily_review_path is not None and selected_candidate is not None
                    else ""
                ),
                "daily_review_path": str(daily_review_path) if daily_review_path is not None else "",
                "safety_decision": (
                    "safe_to_score_from_this_runtime"
                    if score_outcome.scored_candidates
                    else "unsafe_to_score_from_this_runtime"
                ),
                "next_step": (
                    "review_draft_page"
                    if daily_review_path is not None
                    else "no_verified_candidate_found_review_report_ready"
                ),
            }
        )
        artifact["partial_results_available"] = bool(final_candidates)
        if (
            profile.discovery_mode == "live"
            and not discovered_candidates
            and bool(discovery_result.metrics.get("no_live_candidate_found"))
        ):
            artifact["next_step"] = "no_live_candidate_found"
    except Exception as exc:
        artifact.update(
            {
                "status": "failed",
                "error": str(exc),
                "run_completed_with_errors": True,
                "failure_stage": failure_stage,
                "public_error_summary": _sanitize_public_error(exc, stage=failure_stage),
                "retry_recommendation": _retry_recommendation(failure_stage),
                "partial_results_available": bool(artifact.get("candidates_found") or artifact.get("candidates_verified")),
                "next_step": "inspect_failed_run_report",
                "failures": [str(exc)],
            }
        )

    _finalize_public_review_and_publish(
        root_dir=root_dir,
        run_dir=run_dir,
        artifact=artifact,
        profile_id=profile.profile_id,
        draft_runner=draft_runner,
    )

    _write_run_artifacts(
        run_dir=run_dir,
        artifact=artifact,
        include_failed_marker=artifact["status"] == "failed",
    )
    return artifact


def _new_root_artifact(run_dir: Path) -> dict:
    return {
        "run_id": run_dir.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "success",
        "run_dir": str(run_dir),
        "invariant": "every run produces a public-safe review and attempts Draft review publication",
        "next_step": "review_report",
        "profiles_requested": [],
        "profiles_skipped": [],
        "profile_results": [],
        "candidates_found": 0,
        "candidates_verified": 0,
        "action_card_generated": False,
        "draft_published": False,
        "draft_url": "",
        "review_url": "",
        "human_review_ready": False,
        "public_run_review_generated": False,
        "public_run_review_path": "",
        "draft_publish_attempted": False,
        "draft_publish_requested": False,
        "draft_public_publish_succeeded": False,
        "draft_public_url": "",
        "draft_public_publish_error": "",
        "public_error_summary": "",
        "failure_stage": "",
        "retry_recommendation": "",
        "run_completed_with_errors": False,
        "last_completed_stage": "",
        "partial_results_available": False,
        "evidence_files": [],
        "rejected_candidates": [],
        "failures": [],
        "safety_decision": "unsafe_to_score_from_this_runtime",
        "discovery_metrics": _empty_discovery_metrics(),
    }


def _new_profile_artifact(
    *,
    run_dir: Path,
    profile: FounderSignalConfig,
    profile_path: Path,
) -> dict:
    return {
        "run_id": run_dir.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "success",
        "run_dir": str(run_dir),
        "invariant": "every run produces a public-safe review and attempts Draft review publication",
        "next_step": "review_report",
        "profile_id": profile.profile_id,
        "profile_path": str(profile_path),
        "product_name": profile.product_name,
        "platforms_enabled": sorted(profile.platforms),
        "candidates_found": 0,
        "candidates_verified": 0,
        "action_card_generated": False,
        "draft_published": False,
        "draft_url": "",
        "review_url": "",
        "human_review_ready": False,
        "public_run_review_generated": False,
        "public_run_review_path": "",
        "draft_publish_attempted": False,
        "draft_publish_requested": False,
        "draft_public_publish_succeeded": False,
        "draft_public_url": "",
        "draft_public_publish_error": "",
        "public_error_summary": "",
        "failure_stage": "",
        "retry_recommendation": "",
        "run_completed_with_errors": False,
        "last_completed_stage": "",
        "partial_results_available": False,
        "evidence_files": [],
        "rejected_candidates": [],
        "failures": [],
        "safety_decision": "unsafe_to_score_from_this_runtime",
        "discovery_metrics": _empty_discovery_metrics(),
    }


def _summarize_profile_results(profile_results: list[dict]) -> dict:
    candidates_found = sum(int(item.get("candidates_found") or 0) for item in profile_results)
    candidates_verified = sum(int(item.get("candidates_verified") or 0) for item in profile_results)
    failures: list[str] = []
    draft_url = ""
    draft_page_id = ""
    draft_publish_execution_log_path = ""
    draft_public_publish_error = ""
    evidence_files: list[str] = []
    draft_publish_intent_paths: list[str] = []
    discovery_metrics = _empty_discovery_metrics()
    status = "success"
    for item in profile_results:
        profile_id = str(item.get("profile_id") or "unknown")
        evidence_files.extend(str(path) for path in item.get("evidence_files") or [])
        if item.get("draft_url"):
            draft_url = str(item["draft_url"])
        if item.get("draft_page_id"):
            draft_page_id = str(item["draft_page_id"])
        if item.get("draft_publish_execution_log_path"):
            draft_publish_execution_log_path = str(item["draft_publish_execution_log_path"])
        if item.get("draft_publish_intent_path"):
            draft_publish_intent_paths.append(str(item["draft_publish_intent_path"]))
        if item.get("draft_public_publish_error") and not draft_public_publish_error:
            draft_public_publish_error = str(item["draft_public_publish_error"])
        _merge_discovery_metrics(discovery_metrics, item.get("discovery_metrics") or {})
        item_status = str(item.get("status") or "success")
        if item_status == "published":
            status = "published"
        elif item_status == "failed":
            status = "failed"
        for failure in item.get("failures") or []:
            failures.append(f"{profile_id}: {failure}")
        if item.get("error"):
            failures.append(f"{profile_id}: {item['error']}")
    return {
        "status": status,
        "profile_results": profile_results,
        "candidates_found": candidates_found,
        "candidates_verified": candidates_verified,
        "action_card_generated": any(bool(item.get("action_card_generated")) for item in profile_results),
        "draft_published": any(bool(item.get("draft_published")) for item in profile_results),
        "draft_public_publish_succeeded": any(
            bool(item.get("draft_public_publish_succeeded")) for item in profile_results
        ),
        "draft_publish_requested": any(bool(item.get("draft_publish_requested")) for item in profile_results),
        "draft_publish_requires_confirmation": any(
            bool(item.get("draft_publish_requires_confirmation")) for item in profile_results
        ),
        "draft_public_publish_requires_confirmation": any(
            bool(item.get("draft_public_publish_requires_confirmation")) for item in profile_results
        ),
        "draft_publish_intent_paths": draft_publish_intent_paths,
        "draft_url": draft_url,
        "draft_public_url": draft_url,
        "draft_public_publish_error": draft_public_publish_error,
        "draft_page_id": draft_page_id,
        "draft_publish_execution_log_path": draft_publish_execution_log_path,
        "evidence_files": evidence_files,
        "rejected_candidates": [],
        "discovery_metrics": discovery_metrics,
        "failures": _dedupe(failures),
        "draft_publish_attempted": any(bool(item.get("draft_publish_attempted")) for item in profile_results),
        "human_review_ready": any(bool(item.get("human_review_ready")) for item in profile_results),
        "review_url": draft_url,
        "run_completed_with_errors": any(bool(item.get("run_completed_with_errors")) for item in profile_results),
        "partial_results_available": any(bool(item.get("partial_results_available")) for item in profile_results),
        "safety_decision": (
            "safe_to_score_from_this_runtime"
            if candidates_verified
            else "unsafe_to_score_from_this_runtime"
        ),
        "next_step": (
            "review_draft_page"
            if draft_url
            else "fix_draft_cli_and_retry_publish"
            if any(str(item.get("draft_public_publish_error") or "").strip() for item in profile_results)
            else "retry_draft_publish"
            if any(bool(item.get("draft_publish_attempted")) for item in profile_results)
            else "no_live_candidate_found"
            if profile_results
            and all(str(item.get("next_step") or "") == "no_live_candidate_found" for item in profile_results)
            else "no_verified_candidate_found_review_report_ready"
        ),
    }


def _platform_counts(candidates: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for candidate in candidates:
        platform = str(candidate.get("platform") or candidate.get("source_platform") or "reddit").strip().lower() or "reddit"
        counts[platform] = counts.get(platform, 0) + 1
    return counts


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def _empty_discovery_metrics() -> dict:
    return {
        "searched_pages": 0,
        "searched_urls": [],
        "live_feed_requests": 0,
        "live_feed_failures": 0,
        "live_feed_items_seen": 0,
        "filtered_candidates": 0,
        "filter_reason_counts": {},
        "excluded_by_history": 0,
        "excluded_by_profile": 0,
        "total_excluded": 0,
        "fresh_candidates_found": 0,
        "discovery_budget_pages": 0,
        "discovery_exhausted": False,
        "no_live_candidate_found": False,
    }


def _merge_discovery_metrics(destination: dict, source: dict) -> None:
    destination["searched_pages"] += int(source.get("searched_pages") or 0)
    destination["live_feed_requests"] += int(source.get("live_feed_requests") or 0)
    destination["live_feed_failures"] += int(source.get("live_feed_failures") or 0)
    destination["live_feed_items_seen"] += int(source.get("live_feed_items_seen") or 0)
    destination["filtered_candidates"] += int(source.get("filtered_candidates") or 0)
    destination["excluded_by_history"] += int(source.get("excluded_by_history") or 0)
    destination["excluded_by_profile"] += int(source.get("excluded_by_profile") or 0)
    destination["total_excluded"] += int(source.get("total_excluded") or 0)
    destination["fresh_candidates_found"] += int(source.get("fresh_candidates_found") or 0)
    destination["discovery_budget_pages"] += int(source.get("discovery_budget_pages") or 0)
    destination["discovery_exhausted"] = destination["discovery_exhausted"] or bool(
        source.get("discovery_exhausted")
    )
    destination["no_live_candidate_found"] = destination["no_live_candidate_found"] or bool(
        source.get("no_live_candidate_found")
    )
    for reason, count in (source.get("filter_reason_counts") or {}).items():
        destination["filter_reason_counts"][str(reason)] = int(
            destination["filter_reason_counts"].get(str(reason)) or 0
        ) + int(count or 0)
    for discovery_url in source.get("searched_urls") or []:
        if discovery_url not in destination["searched_urls"]:
            destination["searched_urls"].append(str(discovery_url))


def _ensure_evidence_files(result) -> None:
    fallback_values = {
        result.raw_html_path: "Founder Signal evidence artifact missing after fetch.\n",
        result.text_snapshot_path: "Founder Signal evidence snapshot missing after fetch.\n",
        result.source_url_path: f"{result.source_url}\n",
        result.evidence_url_path: f"{result.evidence_url}\n",
    }
    for path, fallback in fallback_values.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(fallback, encoding="utf-8")


def _finalize_public_review_and_publish(
    *,
    root_dir: Path,
    run_dir: Path,
    artifact: dict,
    profile_id: str,
    draft_runner,
) -> None:
    daily_review_path = run_dir / "daily-review.md"
    if daily_review_path.exists():
        artifact["daily_review_path"] = str(daily_review_path)
    artifact.update(
        {
            "draft_publish_attempted": True,
            "draft_publish_requested": True,
            "draft_published": False,
            "draft_public_publish_succeeded": False,
            "draft_public_publish_error": "",
            "human_review_ready": False,
            "review_url": "",
            "external_public_publish_requires_confirmation": True,
        }
    )
    public_run_review_path = write_public_run_review(run_dir=run_dir, artifact=artifact)
    artifact.update(
        {
            "public_run_review_generated": True,
            "public_run_review_path": str(public_run_review_path),
        }
    )
    try:
        publish_intent = write_public_draft_publish_intent(
            run_dir=run_dir,
            profile_id=profile_id,
        )
        artifact.update(
            {
                "draft_publish_intent_path": str(publish_intent.path),
                "draft_visibility": publish_intent.visibility,
                "draft_publish_requires_confirmation": publish_intent.requires_confirmation,
                "draft_public_publish_requires_confirmation": (
                    publish_intent.public_publish_requires_confirmation
                ),
            }
        )
        publish_result = publish_daily_review_to_draft(
            intent=publish_intent,
            workspace_root=root_dir,
            runner=draft_runner,
        )
        (run_dir / "draft-url.txt").write_text(publish_result.url + "\n", encoding="utf-8")
        (root_dir / "latest-draft-url.txt").write_text(publish_result.url + "\n", encoding="utf-8")
        execution_log_path = run_dir / "draft-publish-execution.json"
        execution_log_path.write_text(
            json.dumps(
                {
                    "draft_page_id": publish_result.page_id,
                    "draft_public_url": publish_result.url,
                    "stages": publish_result.execution_log,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        artifact.update(
            {
                "draft_published": True,
                "draft_url": publish_result.url,
                "draft_page_id": publish_result.page_id,
                "draft_public_publish_succeeded": True,
                "draft_public_url": publish_result.url,
                "draft_public_publish_error": "",
                "draft_publish_execution_log_path": str(execution_log_path),
                "publish_stdout": publish_result.stdout,
                "publish_stderr": publish_result.stderr,
                "review_url": publish_result.url,
                "human_review_ready": True,
                "next_step": "review_draft_page",
            }
        )
    except Exception as exc:
        artifact.update(
            {
                "draft_published": False,
                "draft_public_publish_succeeded": False,
                "draft_public_publish_error": str(exc),
                "human_review_ready": False,
                "review_url": "",
                "next_step": "fix_draft_cli_and_retry_publish",
            }
        )
    write_public_run_review(run_dir=run_dir, artifact=artifact)


def _sanitize_public_error(exc: Exception, *, stage: str) -> str:
    message = f"{type(exc).__name__}: {exc}"
    message = re.sub(r"(?i)(api[_-]?key|token|authorization|bearer|password|secret)[=: ]+\S+", r"\1=<redacted>", message)
    message = re.sub(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]+", "Bearer <redacted>", message)
    message = re.sub(r"(/[A-Za-z0-9._@%+=:, -]+)+", "<local path>", message)
    message = re.sub(r"File \"[^\"]+\", line \d+, in [^\n]+", "File <redacted stack frame>", message)
    message = " ".join(message.split())
    if len(message) > 240:
        message = message[:237].rstrip() + "..."
    if not message:
        return f"The run failed during {stage.replace('_', ' ')}."
    return f"The run failed during {stage.replace('_', ' ')}. {message}"


def _retry_recommendation(stage: str) -> str:
    recommendations = {
        "profile_loading": "Check the selected profile configuration and rerun.",
        "candidate_history": "Check local candidate history state and rerun.",
        "candidate_discovery": "Re-run after checking discovery inputs and platform adapters.",
        "candidate_verification": "Re-run after checking the source fetch and verification adapter.",
        "candidate_scoring": "Re-run after checking scoring inputs and reviewer configuration.",
        "candidate_history_recording": "Check local state write permissions and rerun.",
        "action_card_generation": "Review the selected candidate payload and rerun.",
    }
    return recommendations.get(stage, "Inspect the local run artifact, fix the failed stage, and rerun.")


def _write_run_artifacts(*, run_dir: Path, artifact: dict, include_failed_marker: bool) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = run_dir / "run.json"
    artifact_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    write_report(run_dir=run_dir, artifact=artifact)
    if include_failed_marker:
        write_failed_marker(run_dir=run_dir, artifact=artifact)


__all__ = [
    "AgentReviewer",
    "SelectedCandidate",
    "built_in_agent_reviewer",
    "fetch_reddit_evidence",
    "persist_failed_evidence_read",
    "generate_action_card",
    "persist_verified_text_snapshot",
    "run_once",
    "run_profile_once",
    "to_eddrit_url",
]
