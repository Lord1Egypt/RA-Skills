#!/usr/bin/env python3

from __future__ import annotations

import argparse
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_browser import (
    browser_fetch_imagine_feed,
    browser_fetch_json,
    wait_for_imagine_feed_jobs,
    wait_for_job_cdn_assets,
    wait_for_job_page_assets,
    wait_for_prompt_card_assets,
    watch_job_results,
)
from mj_alpha import (
    DEFAULT_METADATA,
    apply_preset,
    append_negative_terms,
    download_image,
    enrich_config_from_cookie,
    enforce_safe_limits,
    extract_job_ids,
    get_user_state,
    load_config,
    normalize_prompt,
    print_json,
    record_submit,
    require_config,
    resolve_named_suffix,
    save_json,
    submit_imagine,
    summarize_job_images,
    wait_for_recent_job,
)


SAFE_WAIT_RE = re.compile(r"wait at least ([0-9]+(?:\.[0-9]+)?) more seconds", re.IGNORECASE)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Midjourney jobs in batches with submit-first waiting.")
    parser.add_argument("prompts_file", help="Text file with one prompt per line")
    parser.add_argument("--dotenv", default=".env", help="Path to .env file")
    parser.add_argument("--transport", choices=["auto", "browser", "http"], default="browser", help="Request transport")
    parser.add_argument("--preset", help="Preset name from presets file")
    parser.add_argument("--presets-file", default="config/presets.example.json", help="Path to presets JSON")
    parser.add_argument("--quality-profile", help="Quality profile name from config/quality-profiles.example.json")
    parser.add_argument("--quality-profiles-file", default="config/quality-profiles.example.json", help="Path to quality profiles JSON")
    parser.add_argument("--negative", help="Append a --no clause when prompts do not already define one")
    parser.add_argument("--default-version", default="8", help="Default version when prompt has no version flag")
    parser.add_argument("--no-raw", action="store_true", help="Do not auto-append --raw")
    parser.add_argument("--sync-user-state", action="store_true", help="Read /api/user-mutable-state before the batch starts")
    parser.add_argument("--batch-size", type=int, default=10, help="Prompts per batch before waiting for that batch to finish")
    parser.add_argument("--batch-cooldown-seconds", type=float, default=0.0, help="Extra cooldown after each completed batch")
    parser.add_argument("--batch-cooldown-min-seconds", type=float, help="Minimum cooldown between completed batches")
    parser.add_argument("--batch-cooldown-max-seconds", type=float, help="Maximum cooldown between completed batches")
    parser.add_argument("--wait-mode", choices=["batch", "serial"], default="batch", help="Wait for one batch at a time or fully serialise each prompt")
    parser.add_argument("--submit-interval-seconds", type=float, help="Deprecated alias: fixed delay between submits")
    parser.add_argument("--submit-delay-min-seconds", type=float, default=1.0, help="Minimum delay between prompt submissions")
    parser.add_argument("--submit-delay-max-seconds", type=float, default=2.0, help="Maximum delay between prompt submissions")
    parser.add_argument("--recent-attempts", type=int, default=40, help="Max page asset polling attempts per job or batch")
    parser.add_argument("--recent-amount", type=int, default=25, help="Recent-jobs page size while waiting in HTTP mode")
    parser.add_argument("--download-dir", default="outputs/batch", help="Base directory for downloaded images")
    parser.add_argument(
        "--convert-to",
        choices=["original", "png"],
        default="original",
        help="Download images as their original format or browser-convert them to PNG",
    )
    parser.add_argument("--output", help="Write batch JSON result to file")
    return parser


def read_prompts(path: str | Path) -> list[str]:
    prompts: list[str] = []
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        prompts.append(line)
    return prompts


def resolve_preset_suffix(presets_file: str, preset_name: str | None) -> str | None:
    return resolve_named_suffix(presets_file, preset_name, label="preset")


def extract_safe_wait_seconds(message: str) -> float | None:
    match = SAFE_WAIT_RE.search(message)
    if not match:
        return None
    return float(match.group(1))


def wait_for_safe_window(config) -> dict[str, Any]:
    while True:
        try:
            return enforce_safe_limits(config)
        except RuntimeError as exc:
            wait_seconds = extract_safe_wait_seconds(str(exc))
            if wait_seconds is None:
                raise
            time.sleep(max(0.5, wait_seconds + 0.25))


def save_partial_output(args, results: list[dict[str, Any]], synced_user_state, config) -> None:
    if not args.output:
        return
    output = {
        "count": len(results),
        "batch_size": args.batch_size,
        "batch_cooldown_seconds": args.batch_cooldown_seconds,
        "wait_mode": args.wait_mode,
        "submit_delay_min_seconds": args.submit_delay_min_seconds,
        "submit_delay_max_seconds": args.submit_delay_max_seconds,
        "min_submit_interval_seconds": config.min_submit_interval_seconds,
        "preset": args.preset,
        "quality_profile": args.quality_profile,
        "negative": args.negative,
        "sync_user_state": bool(synced_user_state),
        "user_state": synced_user_state,
        "results": results,
    }
    save_json(args.output, output)


def maybe_sleep_between_submits(args, index: int, prompt_count: int, is_batch_boundary: bool) -> None:
    if index >= prompt_count or is_batch_boundary:
        return
    low = max(0.0, float(args.submit_delay_min_seconds))
    high = max(low, float(args.submit_delay_max_seconds))
    if high <= 0:
        return
    time.sleep(random.uniform(low, high))


def maybe_sleep_between_batches(args, index: int, prompt_count: int) -> None:
    if index >= prompt_count:
        return
    if args.batch_cooldown_min_seconds is not None or args.batch_cooldown_max_seconds is not None:
        low = float(args.batch_cooldown_min_seconds if args.batch_cooldown_min_seconds is not None else 0.0)
        high = float(args.batch_cooldown_max_seconds if args.batch_cooldown_max_seconds is not None else low)
        if high < low:
            raise SystemExit("--batch-cooldown-max-seconds must be >= --batch-cooldown-min-seconds")
        if high > 0:
            time.sleep(random.uniform(max(0.0, low), max(0.0, high)))
        return
    if args.batch_cooldown_seconds > 0:
        time.sleep(args.batch_cooldown_seconds)


def submit_prompt(config, args, final_prompt: str) -> tuple[dict[str, Any], str]:
    if args.transport in {"auto", "browser"}:
        payload = {
            "f": {"mode": config.mode, "private": config.private},
            "channelId": config.channel_id,
            "metadata": DEFAULT_METADATA,
            "t": "imagine",
            "prompt": final_prompt,
        }
        try:
            response = browser_fetch_json(
                config.submit_url,
                method="POST",
                headers={
                    "accept": "*/*",
                    "content-type": "application/json",
                    "x-csrf-protection": config.csrf_protection,
                },
                payload=payload,
                timeout_seconds=config.timeout_seconds,
            )
            submit_result = {
                "dry_run": False,
                "transport": "browser",
                "submit_url": config.submit_url,
                "payload": payload,
                "response": response,
                "job_ids": extract_job_ids(response),
            }
        except Exception:
            if args.transport == "browser":
                raise
            submit_result = submit_imagine(config, final_prompt)
            submit_result["transport"] = "http"
    else:
        submit_result = submit_imagine(config, final_prompt)
        submit_result["transport"] = "http"

    job_ids = extract_job_ids(submit_result)
    if not job_ids:
        raise SystemExit("Submit response did not contain a job_id.")
    return submit_result, job_ids[0]


def build_pending_item(
    *,
    index: int,
    batch_index: int,
    original_prompt: str,
    final_prompt: str,
    safe_limits: dict[str, Any],
    submit_result: dict[str, Any],
    job_id: str,
) -> dict[str, Any]:
    return {
        "index": index,
        "batch_index": batch_index,
        "original_prompt": original_prompt,
        "final_prompt": final_prompt,
        "safe_limits": safe_limits,
        "submit": submit_result,
        "job_id": job_id,
    }


def wait_for_pending_items(config, args, pending_items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if not pending_items:
        return {}

    if args.transport in {"auto", "browser"}:
        watch_timeout = min(
            max(10.0, float(config.poll_interval_seconds) * 3.0),
            max(10.0, float(config.timeout_seconds)),
        )
        try:
            watched = watch_job_results(
                [item["job_id"] for item in pending_items],
                page_url="https://alpha.midjourney.com/imagine",
                min_count=4,
                timeout_seconds=watch_timeout,
            )
            watched_jobs = watched.get("jobs", {}) if isinstance(watched, dict) else {}
            if watched_jobs:
                if all(len(list((watched_jobs.get(item["job_id"]) or {}).get("result_urls") or [])) >= 4 for item in pending_items):
                    return watched_jobs
        except Exception:
            if args.transport == "browser":
                raise
        feed_wait = wait_for_imagine_feed_jobs(
            [item["job_id"] for item in pending_items],
            user_id=config.user_id or "",
            csrf_protection=config.csrf_protection,
            attempts=args.recent_attempts,
            interval_seconds=config.poll_interval_seconds,
            page_size=max(1000, len(pending_items) * 8),
            page_url="https://alpha.midjourney.com/imagine",
            timeout_seconds=config.timeout_seconds,
        )
        jobs: dict[str, dict[str, Any]] = {}
        for item in pending_items:
            feed_row = (feed_wait.get("jobs", {}) or {}).get(item["job_id"]) or None
            attempts = max(2, min(6, args.recent_attempts // 4 or 2))
            page_result = wait_for_job_cdn_assets(
                item["job_id"],
                attempts=attempts,
                interval_seconds=max(1.0, config.poll_interval_seconds),
                timeout_seconds=config.timeout_seconds,
            )
            if len(list(page_result.get("result_urls") or [])) < 4:
                page_result = wait_for_job_page_assets(
                    item["job_id"],
                    attempts=attempts,
                    interval_seconds=max(1.0, config.poll_interval_seconds),
                    timeout_seconds=config.timeout_seconds,
                )
            if feed_row:
                page_result["imagine_feed_job"] = feed_row
            page_result["imagine_feed_check"] = feed_wait
            jobs[item["job_id"]] = page_result
        return jobs

    results: dict[str, dict[str, Any]] = {}
    for item in pending_items:
        recent_result = wait_for_recent_job(
            config,
            item["job_id"],
            attempts=args.recent_attempts,
            amount=args.recent_amount,
        )
        results[item["job_id"]] = recent_result
    return results


def finalize_pending_items(
    config,
    args,
    pending_items: list[dict[str, Any]],
    results: list[dict[str, Any]],
    synced_user_state,
) -> None:
    if not pending_items:
        return

    waited = wait_for_pending_items(config, args, pending_items)
    for item in pending_items:
        job_id = item["job_id"]
        recent_result = waited.get(job_id, {})

        if args.transport in {"auto", "browser"}:
            image_paths = list(recent_result.get("result_urls") or [])
            if not image_paths:
                fallback_result = wait_for_prompt_card_assets(
                    item["final_prompt"],
                    page_url="https://alpha.midjourney.com/imagine",
                    attempts=max(20, args.recent_attempts),
                    interval_seconds=config.poll_interval_seconds,
                    timeout_seconds=config.timeout_seconds,
                )
                if fallback_result.get("result_urls"):
                    recent_result = fallback_result
                    image_paths = list(fallback_result.get("result_urls") or [])
            job_summary = {
                "job_id": job_id,
                "image_count": len(image_paths),
                "image_paths": image_paths,
                "source": recent_result.get("source", "page_assets"),
            }
        else:
            job = recent_result.get("job")
            if not job:
                raise SystemExit(f"Job {job_id} was not found in recent-jobs for prompt #{item['index']}.")
            job_summary = summarize_job_images(job)
            image_paths = list(job.get("image_paths") or [])

        if not image_paths:
            raise SystemExit(f"Job {job_id} completed without image paths for prompt #{item['index']}.")

        job_output_dir = Path(args.download_dir) / job_id
        downloads = [
            download_image(
                config,
                image_url,
                job_output_dir,
                filename_stem=f"{job_id}_{image_index}",
                convert_to=args.convert_to,
            )
            for image_index, image_url in enumerate(image_paths, start=1)
        ]

        results.append(
            {
                "index": item["index"],
                "batch_index": item["batch_index"],
                "original_prompt": item["original_prompt"],
                "final_prompt": item["final_prompt"],
                "safe_limits": item["safe_limits"],
                "job_id": job_id,
                "submit": item["submit"],
                "recent_job_summary": job_summary,
                "recent_job_check": recent_result,
                "downloads": downloads,
            }
        )
        save_partial_output(args, results, synced_user_state, config)


def main() -> int:
    args = build_parser().parse_args()
    prompts = read_prompts(args.prompts_file)
    if not prompts:
        raise SystemExit("No prompts found in prompts file.")

    if args.submit_interval_seconds is not None:
        fixed = max(0.0, float(args.submit_interval_seconds))
        args.submit_delay_min_seconds = fixed
        args.submit_delay_max_seconds = fixed
    if args.submit_delay_max_seconds < args.submit_delay_min_seconds:
        raise SystemExit("--submit-delay-max-seconds must be >= --submit-delay-min-seconds")
    if (
        args.batch_cooldown_min_seconds is not None
        and args.batch_cooldown_max_seconds is not None
        and args.batch_cooldown_max_seconds < args.batch_cooldown_min_seconds
    ):
        raise SystemExit("--batch-cooldown-max-seconds must be >= --batch-cooldown-min-seconds")
    if args.batch_size < 0:
        raise SystemExit("--batch-size must be >= 0")

    config = enrich_config_from_cookie(load_config(args.dotenv))
    require_config(config)
    config.min_submit_interval_seconds = max(0.0, float(args.submit_delay_min_seconds))

    synced_user_state = None
    if args.sync_user_state:
        if args.transport in {"auto", "browser"}:
            try:
                synced_user_state = browser_fetch_json(
                    config.user_state_url,
                    headers={
                        "accept": "*/*",
                        "content-type": "application/json",
                        "x-csrf-protection": config.csrf_protection,
                    },
                    timeout_seconds=config.timeout_seconds,
                )
            except Exception:
                if args.transport == "browser":
                    raise
                synced_user_state = get_user_state(config)
        else:
            synced_user_state = get_user_state(config)
        settings = synced_user_state.get("settings", {}) if isinstance(synced_user_state, dict) else {}
        if isinstance(settings.get("speed"), str):
            config.mode = settings["speed"]
        if isinstance(settings.get("visibility"), str):
            config.private = settings["visibility"].lower() in {"stealth", "private"}

    preset_suffix = resolve_preset_suffix(args.presets_file, args.preset)
    quality_suffix = resolve_named_suffix(args.quality_profiles_file, args.quality_profile, label="quality profile")
    results: list[dict[str, Any]] = []
    pending_items: list[dict[str, Any]] = []
    prompt_count = len(prompts)
    effective_batch_size = args.batch_size or prompt_count

    for index, original_prompt in enumerate(prompts, start=1):
        prompt = original_prompt
        if preset_suffix:
            prompt = apply_preset(prompt, preset_suffix)
        if quality_suffix:
            prompt = apply_preset(prompt, quality_suffix)
        prompt = append_negative_terms(prompt, args.negative)
        final_prompt = normalize_prompt(
            prompt,
            default_version=args.default_version,
            add_raw=not args.no_raw,
        )

        safe_limits = wait_for_safe_window(config)
        submit_result, job_id = submit_prompt(config, args, final_prompt)

        record_submit(
            config,
            prompt=final_prompt,
            mode=str(submit_result.get("payload", {}).get("f", {}).get("mode", config.mode)),
            private=bool(submit_result.get("payload", {}).get("f", {}).get("private", config.private)),
            job_id=job_id,
            dry_run=False,
            submit_url=submit_result.get("submit_url", config.submit_url),
        )

        batch_index = ((index - 1) // effective_batch_size) + 1
        pending_items.append(
            build_pending_item(
                index=index,
                batch_index=batch_index,
                original_prompt=original_prompt,
                final_prompt=final_prompt,
                safe_limits=safe_limits,
                submit_result=submit_result,
                job_id=job_id,
            )
        )

        is_batch_boundary = index % effective_batch_size == 0 or index == prompt_count
        if args.wait_mode == "serial":
            finalize_pending_items(config, args, pending_items, results, synced_user_state)
            pending_items.clear()
        elif is_batch_boundary:
            finalize_pending_items(config, args, pending_items, results, synced_user_state)
            pending_items.clear()

        if is_batch_boundary:
            maybe_sleep_between_batches(args, index, prompt_count)
        elif args.wait_mode != "serial":
            maybe_sleep_between_submits(args, index, prompt_count, is_batch_boundary)

    output = {
        "count": len(results),
        "batch_size": args.batch_size,
        "batch_cooldown_seconds": args.batch_cooldown_seconds,
        "wait_mode": args.wait_mode,
        "submit_delay_min_seconds": args.submit_delay_min_seconds,
        "submit_delay_max_seconds": args.submit_delay_max_seconds,
        "min_submit_interval_seconds": config.min_submit_interval_seconds,
        "preset": args.preset,
        "quality_profile": args.quality_profile,
        "negative": args.negative,
        "sync_user_state": bool(synced_user_state),
        "user_state": synced_user_state,
        "results": results,
    }
    if args.output:
        save_json(args.output, output)
    print_json(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
