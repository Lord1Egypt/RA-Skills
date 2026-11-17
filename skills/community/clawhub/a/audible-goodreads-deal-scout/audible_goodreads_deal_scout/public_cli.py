from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

from . import __version__
from . import core
from .audible_auth import auth_file_status, finish_external_auth, start_external_auth, test_authenticated_price
from .cli_errors import cli_error_payload
from .constants import DEFAULT_DELIVERY_POLICY, DEFAULT_THRESHOLD
from .delivery import (
    deliver_message,
    resolve_delivery_policy,
    setup_configuration,
)
from .diagnostics import doctor_report
from .repo_audit import publish_file_paths, scan_repo_for_leaks
from .rendering import build_delivery_plan
from .settings import (
    SUPPORTED_MARKETPLACES,
    default_storage_dir,
    load_config,
    parse_csv_column_overrides,
    resolve_notes_text,
    validate_marketplace,
)
from .shared import prompt, write_json_atomic
from .want_to_read_scan import report_json, scan_want_to_read

REQUIRED_PUBLISH_IGNORE_PATTERNS = (
    ".git/",
    ".audible-goodreads-deal-scout/",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "audible-auth*.json",
    ".pytest_cache/",
    ".ruff_cache/",
    ".coverage",
    "htmlcov/",
    "tests/",
    "docs/",
    "PROMPT_REQUEST.md",
)


def load_json_input(path_or_dash: str | None) -> dict:
    if not path_or_dash or path_or_dash == "-":
        return json.loads(sys.stdin.read())
    return json.loads(Path(path_or_dash).expanduser().read_text(encoding="utf-8"))


def load_ignore_entries(path: Path) -> set[str]:
    if not path.exists():
        return set()
    entries: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.add(stripped)
    return entries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prep layer for the Audible Goodreads Deal Scout skill.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Write config/preferences and optionally register a daily cron job.")
    setup_parser.add_argument("--config-path")
    setup_parser.add_argument("--storage-dir")
    setup_parser.add_argument("--state-file")
    setup_parser.add_argument("--preferences-path")
    setup_parser.add_argument("--audible-marketplace")
    setup_parser.add_argument("--audible-auth-path")
    setup_parser.add_argument("--audible-fetch-backend", choices=("auto", "python", "curl"))
    setup_parser.add_argument("--goodreads-csv")
    setup_parser.add_argument("--notes-file")
    setup_parser.add_argument("--notes-text")
    setup_parser.add_argument("--threshold", type=float, default=None)
    setup_parser.add_argument("--privacy-mode", default=None)
    setup_parser.add_argument("--artifact-dir")
    setup_parser.add_argument("--freshness-days", type=int, default=None)
    setup_parser.add_argument("--daily-cron")
    daily_group = setup_parser.add_mutually_exclusive_group()
    daily_group.add_argument("--daily-automation", dest="daily_automation", action="store_true")
    daily_group.add_argument("--no-daily-automation", dest="daily_automation", action="store_false")
    setup_parser.set_defaults(daily_automation=None)
    setup_parser.add_argument("--register-cron", action="store_true")
    setup_parser.add_argument("--openclaw-bin", default="openclaw")
    setup_parser.add_argument("--delivery-channel")
    setup_parser.add_argument("--delivery-target")
    setup_parser.add_argument("--delivery-policy")
    setup_parser.add_argument("--no-delivery", action="store_true")
    setup_parser.add_argument("--csv-column", action="append", default=[])
    setup_parser.add_argument("--non-interactive", action="store_true")

    prepare_parser = subparsers.add_parser("prepare", help="Fetch Audible, load CSV/notes, and emit prep JSON for the skill runtime.")
    prepare_parser.add_argument("--config-path")
    prepare_parser.add_argument("--audible-marketplace")
    prepare_parser.add_argument("--goodreads-csv")
    prepare_parser.add_argument("--notes-file")
    prepare_parser.add_argument("--notes-text")
    prepare_parser.add_argument("--threshold", type=float, default=None)
    prepare_parser.add_argument("--privacy-mode", default=None)
    prepare_parser.add_argument("--state-file")
    prepare_parser.add_argument("--artifact-dir")
    prepare_parser.add_argument("--today")
    prepare_parser.add_argument("--invocation-mode", choices=("manual", "scheduled"), default="manual")
    prepare_parser.add_argument("--audible-deal-url")
    prepare_parser.add_argument("--audible-fetch-backend", choices=("auto", "python", "curl"))
    prepare_parser.add_argument("--freshness-days", type=int, default=None)
    prepare_parser.add_argument("--notes-warning-chars", type=int, default=None)
    prepare_parser.add_argument("--csv-column", action="append", default=[])

    headers_parser = subparsers.add_parser("show-csv-headers", help="Print the CSV headers OpenClaw sees in a Goodreads export.")
    headers_parser.add_argument("csv_path")

    measure_parser = subparsers.add_parser(
        "measure-context",
        help="Measure and optionally write the compact CSV fit-context artifact.",
    )
    measure_parser.add_argument("--goodreads-csv", required=True)
    measure_parser.add_argument("--notes-file")
    measure_parser.add_argument("--notes-text")
    measure_parser.add_argument("--csv-column", action="append", default=[])
    measure_parser.add_argument("--output")

    scan_parser = subparsers.add_parser(
        "scan-want-to-read",
        help="Scan Goodreads Want-to-Read books for visible numeric Audible US discounts.",
    )
    scan_parser.add_argument("--config-path")
    scan_parser.add_argument("--limit", type=int)
    scan_parser.add_argument("--offset", type=int)
    scan_parser.add_argument("--scan-order", choices=("newest", "csv", "oldest", "random"))
    scan_parser.add_argument("--seed")
    scan_parser.add_argument("--max-requests", type=int)
    scan_parser.add_argument("--request-delay", type=float)
    scan_parser.add_argument("--min-discount-percent", type=int)
    scan_parser.add_argument("--output-json")
    scan_parser.add_argument("--output-md")
    scan_parser.add_argument("--include-non-deals", action="store_true", default=None)
    scan_parser.add_argument("--verbose", action="store_true", default=None)
    scan_parser.add_argument("--progress", choices=("plain", "json", "none"))
    scan_parser.add_argument("--progress-interval", type=float)
    scan_parser.set_defaults(enrich_goodreads_ratings=None)
    scan_parser.add_argument("--enrich-goodreads-ratings", dest="enrich_goodreads_ratings", action="store_true")
    scan_parser.add_argument("--no-goodreads-rating-enrichment", dest="enrich_goodreads_ratings", action="store_false")
    scan_parser.add_argument("--goodreads-rating-limit", type=int)
    scan_parser.add_argument("--refresh-cache", action="store_true", default=None)
    scan_parser.add_argument("--no-cache", action="store_true", default=None)
    scan_parser.add_argument("--offline-fixtures")
    scan_parser.add_argument("--title")
    scan_parser.add_argument("--author")
    scan_parser.add_argument("--audible-auth-path")

    auth_start_parser = subparsers.add_parser(
        "audible-auth-start",
        help="Start headless external-browser Audible auth for authenticated price lookup.",
    )
    auth_start_parser.add_argument("--auth-path", required=True)
    auth_start_parser.add_argument("--audible-marketplace", default="us")

    auth_finish_parser = subparsers.add_parser(
        "audible-auth-finish",
        help="Finish headless Audible auth by pasting the final Amazon redirect URL.",
    )
    auth_finish_parser.add_argument("--auth-path", required=True)
    auth_finish_parser.add_argument("--redirect-url", required=True)

    auth_test_parser = subparsers.add_parser(
        "audible-auth-test-price",
        help="Use saved Audible auth to fetch authenticated pricing for one Audible ASIN.",
    )
    auth_test_parser.add_argument("--auth-path", required=True)
    auth_test_parser.add_argument("--asin", required=True)

    auth_status_parser = subparsers.add_parser(
        "audible-auth-status",
        help="Inspect saved Audible auth readiness, expiry, and file permissions without printing tokens.",
    )
    auth_status_parser.add_argument("--auth-path", required=True)
    auth_status_parser.add_argument("--fix-permissions", action="store_true")

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check config, CSV, notes, auth, cache, delivery, cron, and wrapper readiness.",
    )
    doctor_parser.add_argument("--config-path")
    doctor_parser.add_argument("--auth-path")
    doctor_parser.add_argument("--openclaw-bin", default="openclaw")
    doctor_parser.add_argument("--check-cron", action="store_true")
    doctor_parser.add_argument("--check-audible-fetch", action="store_true")

    mark_parser = subparsers.add_parser("mark-emitted", help="Record a scheduled run's emitted deal key after the skill finishes.")
    mark_parser.add_argument("--state-file", required=True)
    mark_parser.add_argument("--prepare-json", required=True, help="Path to the scheduled prepare-result JSON that was delivered.")
    mark_parser.add_argument("--deal-key", help="Optional safety check; must match metadata.dealKey in --prepare-json.")
    mark_parser.add_argument("--stale-warning-date")

    gate_parser = subparsers.add_parser(
        "scheduled-gate",
        help="Prepare a scheduled run without a model and decide whether the cron agent should wake.",
    )
    gate_parser.add_argument("--config-path", required=True)
    gate_parser.add_argument("--state-file", required=True)

    audit_parser = subparsers.add_parser(
        "publish-audit",
        help="Check that the skill bundle is shaped correctly for ClawHub publishing.",
    )
    audit_parser.add_argument("--version", default=__version__)
    audit_parser.add_argument("--tags", default="latest")

    finalize_parser = subparsers.add_parser(
        "finalize",
        help="Validate runtime Goodreads/fit output and finalize the public result contract.",
    )
    finalize_parser.add_argument("--prepare-json", required=True, help="Path to prepare-result JSON or - for stdin.")
    finalize_parser.add_argument("--runtime-output", help="Path to runtime output JSON or - for stdin.")

    deliver_parser = subparsers.add_parser(
        "deliver",
        help="Send a finalized skill message through a configured delivery channel.",
    )
    deliver_parser.add_argument("--config-path")
    deliver_parser.add_argument("--final-json", help="Path to finalized result JSON containing a message field, or - for stdin.")
    deliver_parser.add_argument("--message-file", help="Path to a plain-text message file.")
    deliver_parser.add_argument("--delivery-channel")
    deliver_parser.add_argument("--delivery-target")
    deliver_parser.add_argument("--openclaw-bin", default="openclaw")
    deliver_parser.add_argument("--dry-run", action="store_true")

    run_and_deliver_parser = subparsers.add_parser(
        "run-and-deliver",
        help="Finalize a runtime result and deliver the rendered message in one step.",
    )
    run_and_deliver_parser.add_argument("--prepare-json", required=True, help="Path to prepare-result JSON or - for stdin.")
    run_and_deliver_parser.add_argument("--runtime-output", help="Path to runtime output JSON or - for stdin.")
    run_and_deliver_parser.add_argument("--config-path")
    run_and_deliver_parser.add_argument("--delivery-channel")
    run_and_deliver_parser.add_argument("--delivery-target")
    run_and_deliver_parser.add_argument("--delivery-policy")
    run_and_deliver_parser.add_argument("--openclaw-bin", default="openclaw")
    run_and_deliver_parser.add_argument("--dry-run", action="store_true")

    subparsers.add_parser("version", help="Print the bundled skill CLI version.")
    return parser


def interactive_setup_defaults(args: argparse.Namespace) -> dict[str, object]:
    candidate_config_path = (
        Path(args.config_path).expanduser()
        if args.config_path
        else Path(args.storage_dir).expanduser() / "config.json"
        if args.storage_dir
        else default_storage_dir() / "config.json"
    )
    existing: dict[str, object] = {}
    if candidate_config_path.exists():
        _, existing = load_config(candidate_config_path)
    marketplace = args.audible_marketplace or prompt(
        "Which Audible store do you want to use?", str(existing.get("audibleMarketplace") or "us")
    )
    personalized = prompt("Do you want personalized recommendations? (yes/no)", "yes").casefold() in {"y", "yes"}
    csv_path = args.goodreads_csv
    notes_text = args.notes_text
    notes_file = args.notes_file
    if personalized:
        if not csv_path:
            csv_path = prompt("Optional Goodreads CSV path (leave blank to skip)", "")
        if not notes_file and not notes_text:
            notes_choice = prompt("Optional notes file path or leave blank to paste notes next", "")
            if notes_choice:
                notes_file = notes_choice
            else:
                pasted = prompt("Optional freeform reading notes (leave blank to skip)", "")
                notes_text = pasted
    threshold = args.threshold if args.threshold is not None else float(
        prompt("Goodreads score threshold", str(existing.get("threshold", DEFAULT_THRESHOLD)))
    )
    existing_daily = bool(existing.get("dailyCron") or existing.get("stateFile"))
    daily_automation = args.daily_automation
    if daily_automation is None:
        daily_automation = prompt(
            "Do you want daily automation? (yes/no)", "yes" if existing_daily else "no"
        ).casefold() in {"y", "yes"}
    storage_dir = args.storage_dir or prompt(
        "Where should config/state be saved?",
        str(default_storage_dir()),
    )
    daily_cron = args.daily_cron
    if daily_automation and not daily_cron:
        try:
            spec = validate_marketplace(marketplace)
            daily_cron = prompt("Daily cron expression", str(existing.get("dailyCron") or spec["defaultCron"]))
        except ValueError:
            daily_cron = None
    delivery_target = args.delivery_target or prompt(
        "Optional Telegram/transport delivery target", str(existing.get("deliveryTarget") or "")
    )
    delivery_policy = args.delivery_policy or prompt(
        "Delivery policy (positive_only / always_full / summary_on_non_match)",
        str(existing.get("deliveryPolicy") or DEFAULT_DELIVERY_POLICY),
    )
    return {
        "audibleMarketplace": marketplace,
        "audibleAuthPath": args.audible_auth_path,
        "audibleFetchBackend": args.audible_fetch_backend,
        "goodreadsCsvPath": csv_path or None,
        "notesText": notes_text or "",
        "notesFile": notes_file or None,
        "threshold": threshold,
        "dailyAutomation": daily_automation,
        "storageDir": storage_dir,
        "dailyCron": daily_cron,
        "privacyMode": args.privacy_mode or str(existing.get("privacyMode") or "normal"),
        "artifactDir": args.artifact_dir,
        "freshnessDays": args.freshness_days,
        "csvColumns": parse_csv_column_overrides(args.csv_column) if args.csv_column else None,
        "stateFile": args.state_file,
        "configPath": args.config_path,
        "preferencesPath": args.preferences_path,
        "deliveryChannel": args.delivery_channel
        or str(existing.get("deliveryChannel") or "")
        or ("telegram" if delivery_target else None),
        "deliveryTarget": delivery_target or None,
        "deliveryPolicy": delivery_policy,
        "noDelivery": args.no_delivery,
    }


def command_setup(args: argparse.Namespace) -> int:
    if args.non_interactive:
        payload = {
            "configPath": args.config_path,
            "storageDir": args.storage_dir,
            "stateFile": args.state_file,
            "preferencesPath": args.preferences_path,
            "audibleMarketplace": args.audible_marketplace,
            "audibleAuthPath": args.audible_auth_path,
            "audibleFetchBackend": args.audible_fetch_backend,
            "goodreadsCsvPath": args.goodreads_csv,
            "notesFile": args.notes_file,
            "notesText": args.notes_text or "",
            "threshold": args.threshold,
            "privacyMode": args.privacy_mode,
            "artifactDir": args.artifact_dir,
            "freshnessDays": args.freshness_days,
            "dailyCron": args.daily_cron,
            "dailyAutomation": args.daily_automation,
            "csvColumns": parse_csv_column_overrides(args.csv_column) if args.csv_column else None,
            "deliveryChannel": args.delivery_channel,
            "deliveryTarget": args.delivery_target,
            "deliveryPolicy": args.delivery_policy,
            "noDelivery": args.no_delivery,
        }
    else:
        payload = interactive_setup_defaults(args)
    result = setup_configuration(payload, openclaw_bin=args.openclaw_bin, register_cron=args.register_cron)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result.get("ok") and result.get("written") else 1


def command_prepare(args: argparse.Namespace) -> int:
    payload = {
        "configPath": args.config_path,
        "audibleMarketplace": args.audible_marketplace,
        "goodreadsCsvPath": args.goodreads_csv,
        "notesFile": args.notes_file,
        "notesText": args.notes_text,
        "threshold": args.threshold,
        "privacyMode": args.privacy_mode,
        "stateFile": args.state_file,
        "artifactDir": args.artifact_dir,
        "today": args.today,
        "invocationMode": args.invocation_mode,
        "audibleDealUrl": args.audible_deal_url,
        "audibleFetchBackend": args.audible_fetch_backend,
        "freshnessDays": args.freshness_days,
        "notesWarningChars": args.notes_warning_chars,
        "csvColumnOverrides": parse_csv_column_overrides(args.csv_column),
    }
    print(json.dumps(core.prepare_run(payload), indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_show_csv_headers(args: argparse.Namespace) -> int:
    result = core.show_csv_headers(Path(args.csv_path).expanduser())
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_measure_context(args: argparse.Namespace) -> int:
    notes_text = resolve_notes_text(args.notes_file, args.notes_text)
    result = core.measure_context(
        Path(args.goodreads_csv).expanduser(),
        csv_columns=parse_csv_column_overrides(args.csv_column),
        notes_text=notes_text,
        output_path=Path(args.output).expanduser() if args.output else None,
    )
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_scan_want_to_read(args: argparse.Namespace) -> int:
    progress = args.progress
    if progress is None:
        config_path = Path(args.config_path).expanduser() if args.config_path else None
        _, scan_config = load_config(config_path)
        progress = str(scan_config.get("progress") or "plain")
    payload = {
        "configPath": args.config_path,
        "limit": args.limit,
        "offset": args.offset,
        "scanOrder": args.scan_order,
        "seed": args.seed,
        "maxRequests": args.max_requests,
        "requestDelay": args.request_delay,
        "minDiscountPercent": args.min_discount_percent,
        "outputJson": args.output_json,
        "outputMd": args.output_md,
        "includeNonDeals": args.include_non_deals,
        "verbose": args.verbose,
        "progress": progress,
        "progressInterval": args.progress_interval,
        "enrichGoodreadsRatings": args.enrich_goodreads_ratings,
        "goodreadsRatingLimit": args.goodreads_rating_limit,
        "refreshCache": args.refresh_cache,
        "noCache": args.no_cache,
        "offlineFixtures": args.offline_fixtures,
        "title": args.title,
        "author": args.author,
        "audibleAuthPath": args.audible_auth_path,
    }
    report, markdown, exit_code = scan_want_to_read(payload)
    if report.get("status") == "error":
        if args.output_json:
            write_json_atomic(Path(args.output_json).expanduser(), report)
        print(report_json(report), end="")
        return exit_code
    print(markdown, end="")
    return exit_code


def command_audible_auth_start(args: argparse.Namespace) -> int:
    result = start_external_auth(Path(args.auth_path).expanduser(), marketplace=args.audible_marketplace)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_audible_auth_finish(args: argparse.Namespace) -> int:
    result = finish_external_auth(Path(args.auth_path).expanduser(), redirect_url=args.redirect_url)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_audible_auth_test_price(args: argparse.Namespace) -> int:
    result = test_authenticated_price(Path(args.auth_path).expanduser(), args.asin)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_audible_auth_status(args: argparse.Namespace) -> int:
    result = auth_file_status(Path(args.auth_path).expanduser(), fix_permissions=args.fix_permissions)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result.get("ok") else 1


def command_doctor(args: argparse.Namespace) -> int:
    result = doctor_report(
        config_path=Path(args.config_path).expanduser() if args.config_path else None,
        auth_path=Path(args.auth_path).expanduser() if args.auth_path else None,
        openclaw_bin=args.openclaw_bin,
        check_live_cron=args.check_cron,
        check_audible_fetch=args.check_audible_fetch,
    )
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result.get("ok") else 1


def command_version(_: argparse.Namespace) -> int:
    print(json.dumps({"ok": True, "version": __version__}, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_mark_emitted(args: argparse.Namespace) -> int:
    try:
        result = core.mark_emitted_from_prepare(
            Path(args.state_file).expanduser(),
            load_json_input(args.prepare_json),
            expected_deal_key=args.deal_key,
            stale_warning_date=args.stale_warning_date,
        )
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "stateFile": args.state_file,
                    "prepareJson": args.prepare_json,
                    "error": str(exc),
                },
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )
        return 1
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_scheduled_gate(args: argparse.Namespace) -> int:
    config_path = Path(args.config_path).expanduser().resolve()
    state_file = Path(args.state_file).expanduser().resolve()
    prep = core.prepare_run(
        {
            "configPath": str(config_path),
            "stateFile": str(state_file),
            "invocationMode": "scheduled",
        }
    )
    status = str(prep.get("status") or "error")
    reason_code = str(prep.get("reasonCode") or "error_unknown")
    metadata = dict(prep.get("metadata") or {})
    artifacts = dict(prep.get("artifacts") or {})
    prepare_path = str(artifacts.get("prepareResultPath") or "")
    _, policy = resolve_delivery_policy(config_path=config_path)
    fire = True
    message = ""
    if reason_code == "suppress_duplicate_scheduled_run":
        fire = False
    elif status == "suppress" and policy == "positive_only":
        fire = False
    elif status == "ready":
        runtime_prompt = str(artifacts.get("runtimePromptPath") or "")
        runtime_output = str(Path(prepare_path).parent / "runtime-output.json")
        run_command = shlex.join(
            [
                "sh",
                str(Path(__file__).resolve().parents[1] / "scripts" / "audible-goodreads-deal-scout.sh"),
                "run-and-deliver",
                "--config-path",
                str(config_path),
                "--prepare-json",
                prepare_path,
                "--runtime-output",
                runtime_output,
            ]
        )
        mark_command = shlex.join(
            [
                "sh",
                str(Path(__file__).resolve().parents[1] / "scripts" / "audible-goodreads-deal-scout.sh"),
                "mark-emitted",
                "--state-file",
                str(state_file),
                "--prepare-json",
                prepare_path,
                "--deal-key",
                str(metadata.get("dealKey") or ""),
            ]
        )
        message = (
            f"Preparation is ready at {prepare_path}. Read and follow {runtime_prompt}; write its JSON result to "
            f"{runtime_output}. Then run `{run_command}`. Run `{mark_command}` only when that command reports "
            "delivered=true. Return NO_REPLY after delivery or a policy skip."
        )
    elif status == "suppress":
        run_command = shlex.join(
            [
                "sh",
                str(Path(__file__).resolve().parents[1] / "scripts" / "audible-goodreads-deal-scout.sh"),
                "run-and-deliver",
                "--config-path",
                str(config_path),
                "--prepare-json",
                prepare_path,
            ]
        )
        mark_command = shlex.join(
            [
                "sh",
                str(Path(__file__).resolve().parents[1] / "scripts" / "audible-goodreads-deal-scout.sh"),
                "mark-emitted",
                "--state-file",
                str(state_file),
                "--prepare-json",
                prepare_path,
                "--deal-key",
                str(metadata.get("dealKey") or ""),
            ]
        )
        message = (
            f"Preparation is a deterministic suppression at {prepare_path}. Run `{run_command}`; run `{mark_command}` "
            "only when delivered=true, then return NO_REPLY."
        )
    else:
        message = f"Scheduled Audible preparation failed ({reason_code}): {prep.get('message') or 'unknown error'}"
    result = {
        "ok": True,
        "fire": fire,
        "status": status,
        "reasonCode": reason_code,
        "storeLocalDate": metadata.get("storeLocalDate"),
        "message": message,
    }
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


def command_publish_audit(args: argparse.Namespace) -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    publish_ignore_path = skill_dir / ".clawhubignore"
    required_files = {
        "CHANGELOG.md": skill_dir / "CHANGELOG.md",
        "SKILL.md": skill_dir / "SKILL.md",
        "README.md": skill_dir / "README.md",
        "TRUST.md": skill_dir / "TRUST.md",
        "LICENSE.txt": skill_dir / "LICENSE.txt",
        "config.example.json": skill_dir / "config.example.json",
        "scripts/audible-goodreads-deal-scout.sh": skill_dir / "scripts" / "audible-goodreads-deal-scout.sh",
        "agents/openai.yaml": skill_dir / "agents" / "openai.yaml",
    }
    package_dir = skill_dir / "audible_goodreads_deal_scout"
    for path in sorted(package_dir.glob("*.py")):
        required_files[path.relative_to(skill_dir).as_posix()] = path
    skill_text = required_files["SKILL.md"].read_text(encoding="utf-8") if required_files["SKILL.md"].exists() else ""
    publish_ignore_entries = load_ignore_entries(publish_ignore_path)
    published_paths = publish_file_paths(skill_dir, publish_ignore_entries)
    published_relative_paths = {path.relative_to(skill_dir).as_posix() for path in published_paths}
    missing_publish_ignore_patterns = [
        pattern for pattern in REQUIRED_PUBLISH_IGNORE_PATTERNS if pattern not in publish_ignore_entries
    ]
    warnings: list[str] = []
    if args.version != __version__:
        warnings.append(f"Requested publish version {args.version} does not match package version {__version__}.")
    changelog_path = required_files["CHANGELOG.md"]
    changelog_text = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else ""
    if f"## {__version__}" not in changelog_text and f"## v{__version__}" not in changelog_text:
        warnings.append(f"CHANGELOG.md does not contain a section for package version {__version__}.")
    if "skillKey" not in skill_text:
        warnings.append("SKILL.md metadata should declare metadata.openclaw.skillKey for stable settings lookup.")
    if "requires" not in skill_text:
        warnings.append("SKILL.md metadata should declare install/runtime requirements.")
    if "license:" not in skill_text:
        warnings.append("SKILL.md frontmatter should declare a license.")
    if '"category"' not in skill_text and "category:" not in skill_text:
        warnings.append("SKILL.md metadata should declare a category for marketplace discoverability.")
    for label, path in required_files.items():
        if not path.exists():
            warnings.append(f"Missing required publish file: {label}")
        elif label not in published_relative_paths:
            warnings.append(f"Required runtime file is excluded from the publish bundle: {label}")
    if not publish_ignore_path.exists():
        warnings.append("Missing .clawhubignore; publish bundles should exclude tests, docs, and generated local state.")
    elif missing_publish_ignore_patterns:
        warnings.append(
            ".clawhubignore should exclude publish-time artifacts: "
            + ", ".join(missing_publish_ignore_patterns)
        )
    leak_audit = scan_repo_for_leaks(skill_dir, paths=published_paths)
    if not leak_audit["ok"]:
        warnings.extend(
            f"Privacy leak marker '{finding['marker']}' found in {finding['type']} {finding['path']}"
            for finding in leak_audit["findings"]
        )
    result = {
        "ok": not warnings,
        "files": {label: path.exists() for label, path in required_files.items()},
        "frontmatter": {
            "hasName": "name:" in skill_text,
            "hasDescription": "description:" in skill_text,
            "hasLicense": "license:" in skill_text,
            "hasSkillKey": "skillKey" in skill_text,
            "hasCategory": '"category"' in skill_text or "category:" in skill_text,
            "hasRequirements": "requires" in skill_text,
        },
        "publishIgnore": {
            "exists": publish_ignore_path.exists(),
            "requiredExclusions": list(REQUIRED_PUBLISH_IGNORE_PATTERNS),
            "requiredExclusionsPresent": publish_ignore_path.exists() and not missing_publish_ignore_patterns,
            "missingExclusions": missing_publish_ignore_patterns,
        },
        "publishBundle": {
            "fileCount": len(published_relative_paths),
            "runtimeModuleCount": len(list(package_dir.glob("*.py"))),
            "requiredRuntimeFilesIncluded": all(
                label in published_relative_paths for label, path in required_files.items() if path.exists()
            ),
        },
        "privacyAudit": leak_audit,
        "supportedMarketplaces": sorted(SUPPORTED_MARKETPLACES),
        "recommendedPublishCommand": (
            'clawhub publish . --slug audible-goodreads-deal-scout '
            f'--name "Audible Goodreads Deal Scout" --version {args.version} --tags {args.tags}'
        ),
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["ok"] else 1


def command_finalize(args: argparse.Namespace) -> int:
    prep_payload = load_json_input(args.prepare_json)
    runtime_payload = load_json_input(args.runtime_output) if args.runtime_output else None
    result = core.finalize_skill_result(prep_payload, runtime_payload)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_deliver(args: argparse.Namespace) -> int:
    message_text = ""
    if args.final_json:
        final_payload = load_json_input(args.final_json)
        message_text = str(final_payload.get("message") or "")
    elif args.message_file:
        message_text = Path(args.message_file).expanduser().read_text(encoding="utf-8")
    else:
        message_text = sys.stdin.read()
    result = deliver_message(
        message_text=message_text,
        config_path=Path(args.config_path).expanduser() if args.config_path else None,
        delivery_channel=args.delivery_channel,
        delivery_target=args.delivery_target,
        openclaw_bin=args.openclaw_bin,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_run_and_deliver(args: argparse.Namespace) -> int:
    prep_payload = load_json_input(args.prepare_json)
    scheduled_rejection = core.scheduled_prepare_rejection(prep_payload)
    if scheduled_rejection:
        print(
            json.dumps(
                {
                    "ok": False,
                    "delivered": False,
                    "reasonCode": scheduled_rejection["reasonCode"],
                    "error": scheduled_rejection["message"],
                    "prepareJson": args.prepare_json,
                    "prepareResult": prep_payload,
                },
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )
        return 1
    runtime_payload = load_json_input(args.runtime_output) if args.runtime_output else None
    final_result = core.finalize_skill_result(prep_payload, runtime_payload)
    metadata = dict(prep_payload.get("metadata") or {})
    requested_config_path = Path(args.config_path).expanduser().resolve() if args.config_path else None
    artifact_config_text = str(metadata.get("configPath") or "").strip()
    artifact_config_path = Path(artifact_config_text).expanduser().resolve() if artifact_config_text else None
    if str(metadata.get("invocationMode") or "").strip().lower() == "scheduled":
        if artifact_config_path is None:
            raise ValueError("Scheduled delivery requires metadata.configPath in the prepare artifact.")
        if requested_config_path is not None and requested_config_path != artifact_config_path:
            raise ValueError(
                f"Scheduled delivery refused config {requested_config_path}; prepare artifact uses {artifact_config_path}."
            )
    effective_config_path = requested_config_path or artifact_config_path
    _, configured_policy = resolve_delivery_policy(
        config_path=effective_config_path,
        delivery_policy=args.delivery_policy,
    )
    delivery_plan = build_delivery_plan(
        final_result,
        configured_policy,
    )
    if not delivery_plan["shouldDeliver"]:
        print(
            json.dumps(
                {"ok": True, "delivered": False, "deliveryPlan": delivery_plan, "finalResult": final_result},
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )
        return 0
    try:
        delivery_result = deliver_message(
            message_text=str(delivery_plan.get("message") or ""),
            config_path=effective_config_path,
            delivery_channel=args.delivery_channel,
            delivery_target=args.delivery_target,
            openclaw_bin=args.openclaw_bin,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "delivered": False,
                    "error": str(exc),
                    "deliveryPlan": delivery_plan,
                    "finalResult": final_result,
                },
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )
        return 1
    print(
        json.dumps(
            {
                "ok": True,
                "delivered": bool(delivery_result.get("delivered")),
                "simulated": bool(delivery_result.get("simulated")),
                "deliveryPlan": delivery_plan,
                "finalResult": final_result,
                "delivery": delivery_result,
            },
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "setup":
            return command_setup(args)
        if args.command == "prepare":
            return command_prepare(args)
        if args.command == "show-csv-headers":
            return command_show_csv_headers(args)
        if args.command == "measure-context":
            return command_measure_context(args)
        if args.command == "scan-want-to-read":
            return command_scan_want_to_read(args)
        if args.command == "audible-auth-start":
            return command_audible_auth_start(args)
        if args.command == "audible-auth-finish":
            return command_audible_auth_finish(args)
        if args.command == "audible-auth-test-price":
            return command_audible_auth_test_price(args)
        if args.command == "audible-auth-status":
            return command_audible_auth_status(args)
        if args.command == "doctor":
            return command_doctor(args)
        if args.command == "version":
            return command_version(args)
        if args.command == "mark-emitted":
            return command_mark_emitted(args)
        if args.command == "scheduled-gate":
            return command_scheduled_gate(args)
        if args.command == "publish-audit":
            return command_publish_audit(args)
        if args.command == "finalize":
            return command_finalize(args)
        if args.command == "deliver":
            return command_deliver(args)
        if args.command == "run-and-deliver":
            return command_run_and_deliver(args)
    except Exception as exc:
        print(
            json.dumps(
                cli_error_payload(
                    command=str(args.command or ""),
                    reason_code="cli_command_failed",
                    message=str(exc),
                    error_type=type(exc).__name__,
                ),
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        )
        return 1
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
