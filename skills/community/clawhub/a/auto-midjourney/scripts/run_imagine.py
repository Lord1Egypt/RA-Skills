#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlencode

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mj_browser import (
    browser_fetch_json,
    wait_for_imagine_feed_jobs,
    wait_for_job_cdn_assets,
    wait_for_job_page_assets,
    watch_job_results,
)
from mj_alpha import (
    apply_preset,
    append_negative_terms,
    download_image,
    enrich_config_from_cookie,
    enforce_safe_limits,
    extract_job_ids,
    get_user_state,
    load_config,
    normalize_prompt,
    poll_job,
    print_json,
    record_submit,
    require_config,
    resolve_named_suffix,
    save_json,
    submit_imagine,
    summarize_job_images,
    wait_for_recent_job,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit a Midjourney Alpha imagine job and optionally wait.")
    parser.add_argument("prompt", help="Natural prompt or full MJ prompt")
    parser.add_argument("--dotenv", default=".env", help="Path to .env file")
    parser.add_argument("--transport", choices=["auto", "browser", "http"], default="auto", help="Request transport")
    parser.add_argument("--channel-id", help="Override MJ_CHANNEL_ID")
    parser.add_argument("--mode", help="Override MJ_MODE")
    parser.add_argument("--private", action="store_true", help="Submit as private/stealth")
    parser.add_argument("--public", action="store_true", help="Submit as public")
    parser.add_argument("--wait", action="store_true", help="Poll job status after submit")
    parser.add_argument("--attempts", type=int, default=60, help="Max poll attempts when --wait is enabled")
    parser.add_argument("--interval", type=float, help="Override MJ_POLL_INTERVAL_SECONDS")
    parser.add_argument("--default-version", default="8", help="Default Midjourney version when prompt has no version flag")
    parser.add_argument("--no-raw", action="store_true", help="Do not auto-append --raw")
    parser.add_argument("--preset", help="Preset name from config/presets.example.json or your own JSON file")
    parser.add_argument("--presets-file", default="config/presets.example.json", help="Path to presets JSON")
    parser.add_argument("--quality-profile", help="Quality profile name from config/quality-profiles.example.json")
    parser.add_argument("--quality-profiles-file", default="config/quality-profiles.example.json", help="Path to quality profiles JSON")
    parser.add_argument("--negative", help="Append a --no clause when the prompt does not already define one")
    parser.add_argument("--sync-user-state", action="store_true", help="Read /api/user-mutable-state and use server defaults when flags are not overridden")
    parser.add_argument("--unsafe-no-throttle", action="store_true", help="Disable local conservative rate limits")
    parser.add_argument("--wait-recent-jobs", action="store_true", help="Legacy: wait for the submitted job to appear in recent-jobs")
    parser.add_argument("--wait-page-assets", action="store_true", help="Wait for page resource URLs for this job_id to appear on the Alpha imagine page")
    parser.add_argument("--recent-attempts", type=int, default=40, help="Max recent-jobs polling attempts")
    parser.add_argument("--recent-amount", type=int, default=25, help="Recent-jobs page size while waiting")
    parser.add_argument("--download", action="store_true", help="Download result images to local disk after recent-jobs verification")
    parser.add_argument("--download-dir", default="outputs", help="Base directory for downloaded images")
    parser.add_argument(
        "--convert-to",
        choices=["original", "png"],
        default="original",
        help="Download images as their original format or browser-convert them to PNG",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print normalized payload without submitting")
    parser.add_argument("--output-dir", help="Directory for submit.json and poll.json")
    return parser


def resolve_preset_suffix(presets_file: str, preset_name: str | None) -> str | None:
    return resolve_named_suffix(presets_file, preset_name, label="preset")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.private and args.public:
        parser.error("Choose either --private or --public, not both")

    private = None
    if args.private:
        private = True
    elif args.public:
        private = False

    prompt = args.prompt
    preset_suffix = resolve_preset_suffix(args.presets_file, args.preset)
    if preset_suffix:
        prompt = apply_preset(prompt, preset_suffix)
    quality_suffix = resolve_named_suffix(args.quality_profiles_file, args.quality_profile, label="quality profile")
    if quality_suffix:
        prompt = apply_preset(prompt, quality_suffix)
    prompt = append_negative_terms(prompt, args.negative)

    normalized_prompt = normalize_prompt(
        prompt,
        default_version=args.default_version,
        add_raw=not args.no_raw,
    )

    config = enrich_config_from_cookie(load_config(args.dotenv))
    if args.channel_id:
        config.channel_id = args.channel_id

    user_state = None
    if args.sync_user_state and not args.dry_run:
        try:
            if args.transport in {"auto", "browser"}:
                try:
                    user_state = browser_fetch_json(
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
                    user_state = get_user_state(config)
            else:
                user_state = get_user_state(config)
        except Exception as exc:
            raise SystemExit(f"Failed to sync from user-mutable-state: {exc}")

        settings = user_state.get("settings", {}) if isinstance(user_state, dict) else {}
        if not args.mode and isinstance(settings.get("speed"), str):
            config.mode = settings["speed"]
        if private is None and isinstance(settings.get("visibility"), str):
            private = settings["visibility"].lower() in {"stealth", "private"}

    require_config(
        config,
        need_status=args.wait and not args.dry_run,
        need_cookie=not args.dry_run,
    )

    safe_limits = None
    if not args.dry_run and not args.unsafe_no_throttle:
        safe_limits = enforce_safe_limits(config)

    if args.dry_run:
        submit_result = submit_imagine(
            config,
            normalized_prompt,
            mode=args.mode,
            private=private,
            channel_id=args.channel_id,
            dry_run=True,
        )
    elif args.transport in {"auto", "browser"}:
        mode_to_use = args.mode or config.mode
        private_to_use = config.private if private is None else private
        payload = {
            "f": {"mode": mode_to_use, "private": private_to_use},
            "channelId": args.channel_id or config.channel_id,
            "metadata": {
                "isMobile": None,
                "imagePrompts": 0,
                "imageReferences": 0,
                "characterReferences": 0,
                "depthReferences": 0,
                "lightboxOpen": None,
            },
            "t": "imagine",
            "prompt": normalized_prompt,
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
            submit_result = submit_imagine(
                config,
                normalized_prompt,
                mode=args.mode,
                private=private,
                channel_id=args.channel_id,
                dry_run=False,
            )
            submit_result["transport"] = "http"
    else:
        submit_result = submit_imagine(
            config,
            normalized_prompt,
            mode=args.mode,
            private=private,
            channel_id=args.channel_id,
            dry_run=False,
        )
        submit_result["transport"] = "http"

    output = {
        "final_prompt": normalized_prompt,
        "preset": args.preset,
        "quality_profile": args.quality_profile,
        "negative": args.negative,
        "safe_mode": not args.unsafe_no_throttle,
        "safe_limits": safe_limits,
        "user_state_synced": bool(user_state),
        "user_state": user_state,
        "submit": submit_result,
    }

    if args.output_dir:
        save_json(Path(args.output_dir) / "submit.json", submit_result)

    job_ids = extract_job_ids(submit_result) if not args.dry_run else []

    if not args.dry_run:
        mode_used = (
            submit_result.get("payload", {})
            .get("f", {})
            .get("mode", config.mode)
        )
        private_used = (
            submit_result.get("payload", {})
            .get("f", {})
            .get("private", config.private if private is None else private)
        )
        output["usage_log_entry"] = record_submit(
            config,
            prompt=normalized_prompt,
            mode=str(mode_used),
            private=bool(private_used),
            job_id=job_ids[0] if job_ids else None,
            dry_run=False,
            submit_url=submit_result.get("submit_url", config.submit_url),
        )

    if (args.wait_recent_jobs or args.wait_page_assets or args.download) and not args.dry_run:
        if not job_ids:
            raise SystemExit("Submit response did not contain a job_id; cannot verify in recent-jobs.")
        if args.transport in {"auto", "browser"} and (args.wait_page_assets or args.download):
            watch_timeout = min(
                max(10.0, float(config.poll_interval_seconds) * 3.0),
                max(10.0, float(config.timeout_seconds)),
            )
            try:
                watch_result = watch_job_results(
                    [job_ids[0]],
                    page_url="https://alpha.midjourney.com/imagine",
                    min_count=4,
                    timeout_seconds=watch_timeout,
                )
                recent_result = (watch_result.get("jobs", {}) or {}).get(job_ids[0]) or {
                    "job_id": job_ids[0],
                    "done": False,
                    "result_urls": [],
                    "source": "network_watch",
                    "watch_result": watch_result,
                }
                recent_result.setdefault("source", "network_watch")
                recent_result.setdefault("watch_result", watch_result)
                if len(list(recent_result.get("result_urls") or [])) < 4:
                    feed_wait = wait_for_imagine_feed_jobs(
                        [job_ids[0]],
                        user_id=config.user_id or "",
                        csrf_protection=config.csrf_protection,
                        attempts=args.recent_attempts,
                        interval_seconds=config.poll_interval_seconds,
                        page_size=1000,
                        page_url="https://alpha.midjourney.com/imagine",
                        timeout_seconds=config.timeout_seconds,
                    )
                    recent_result = wait_for_job_cdn_assets(
                        job_ids[0],
                        attempts=max(2, min(6, args.recent_attempts // 4 or 2)),
                        interval_seconds=max(1.0, config.poll_interval_seconds),
                        timeout_seconds=config.timeout_seconds,
                    )
                    if len(list(recent_result.get("result_urls") or [])) < 4:
                        recent_result = wait_for_job_page_assets(
                            job_ids[0],
                            attempts=max(2, min(6, args.recent_attempts // 4 or 2)),
                            interval_seconds=max(1.0, config.poll_interval_seconds),
                            timeout_seconds=config.timeout_seconds,
                        )
                    recent_result["imagine_feed_check"] = feed_wait
                    recent_result["imagine_feed_job"] = (feed_wait.get("jobs", {}) or {}).get(job_ids[0])
            except Exception:
                if args.transport == "browser":
                    raise
                raise
        elif args.transport in {"auto", "browser"}:
            try:
                history = []
                recent_result = None
                for attempt in range(1, max(1, args.recent_attempts) + 1):
                    params = urlencode(
                        {
                            "userId": config.user_id,
                            "page": 1,
                            "amount": args.recent_amount,
                            "orderBy": "new",
                            "jobStatus": "completed",
                            "dedupe": "true",
                            "refreshApi": "0",
                        }
                    )
                    response = browser_fetch_json(
                        f"{config.recent_jobs_url}?{params}",
                        page_url="https://www.midjourney.com/",
                        headers={"accept": "*/*", "content-type": "application/json"},
                        timeout_seconds=config.timeout_seconds,
                    )
                    from mj_alpha import find_job_by_id
                    job = find_job_by_id(response, job_ids[0])
                    history.append({"attempt": attempt, "timestamp": int(__import__('time').time()), "match_found": job is not None})
                    if job:
                        recent_result = {
                            "job_id": job_ids[0],
                            "attempts": attempt,
                            "done": True,
                            "history": history,
                            "job": job,
                            "result_urls": list(job.get("image_paths") or []),
                        }
                        break
                    if attempt < args.recent_attempts:
                        __import__('time').sleep(config.poll_interval_seconds)
                if recent_result is None:
                    recent_result = {
                        "job_id": job_ids[0],
                        "attempts": args.recent_attempts,
                        "done": False,
                        "history": history,
                        "job": None,
                        "result_urls": [],
                    }
            except Exception:
                if args.transport == "browser":
                    raise
                recent_result = wait_for_recent_job(
                    config,
                    job_ids[0],
                    attempts=args.recent_attempts,
                    amount=args.recent_amount,
                )
        else:
            recent_result = wait_for_recent_job(
                config,
                job_ids[0],
                attempts=args.recent_attempts,
                amount=args.recent_amount,
            )
        output["recent_job_check"] = recent_result
        if args.output_dir:
            save_json(Path(args.output_dir) / "recent-job.json", recent_result)

        job = recent_result.get("job")
        if job:
            output["recent_job_summary"] = summarize_job_images(job)
        elif recent_result.get("result_urls"):
            output["recent_job_summary"] = {
                "job_id": job_ids[0],
                "image_count": len(recent_result.get("result_urls") or []),
                "image_paths": list(recent_result.get("result_urls") or []),
                "source": "page_assets",
            }

        if args.download:
            image_paths = list(recent_result.get("result_urls") or [])
            if not image_paths:
                raise SystemExit("No downloadable result URLs were found; cannot download.")

            job_output_dir = Path(args.download_dir) / (job_ids[0] if job_ids else "unknown-job")
            downloads = []
            for index, image_url in enumerate(image_paths, start=1):
                downloads.append(
                    download_image(
                        config,
                        image_url,
                        job_output_dir,
                        filename_stem=f"{job_ids[0]}_{index}",
                        convert_to=args.convert_to,
                    )
                )
            output["downloads"] = downloads
            if args.output_dir:
                save_json(Path(args.output_dir) / "downloads.json", downloads)

    if args.wait and not args.dry_run:
        if not job_ids:
            raise SystemExit("Submit response did not contain a job_id; cannot poll.")

        poll_result = poll_job(
            config,
            job_ids[0],
            attempts=args.attempts,
            interval_seconds=args.interval,
        )
        output["poll"] = poll_result

        if args.output_dir:
            save_json(Path(args.output_dir) / "poll.json", poll_result)

    print_json(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
