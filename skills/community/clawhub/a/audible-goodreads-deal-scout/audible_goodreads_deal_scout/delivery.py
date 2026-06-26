from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .constants import DEFAULT_DELIVERY_POLICY, DEFAULT_FRESHNESS_DAYS, DEFAULT_THRESHOLD, SUPPORTED_DELIVERY_POLICIES, SUPPORTED_PRIVACY_MODES
from .settings import (
    config_template,
    default_storage_dir,
    load_config,
    resolve_notes_text,
    skill_root,
    validate_marketplace,
    validate_timezone,
)
from .shared import atomic_write_text, ensure_python_version, normalize_space, write_json_atomic


def resolve_openclaw_bin(openclaw_bin: str = "openclaw") -> str:
    env_bin = normalize_space(os.environ.get("OPENCLAW_BIN"))
    requested = normalize_space(openclaw_bin) or "openclaw"
    candidates: list[str] = []
    if env_bin and requested == "openclaw":
        candidates.append(env_bin)
    candidates.append(requested)
    home = Path.home()
    candidates.extend(
        [
            str(home / ".npm-global" / "bin" / "openclaw"),
            str(home / ".local" / "bin" / "openclaw"),
            "/usr/local/bin/openclaw",
        ]
    )
    for candidate in candidates:
        if not candidate:
            continue
        expanded = str(Path(candidate).expanduser()) if "/" in candidate else candidate
        if "/" in expanded:
            if Path(expanded).exists() and os.access(expanded, os.X_OK):
                return expanded
            continue
        resolved = shutil.which(expanded)
        if resolved:
            return resolved
    return requested


def build_cron_message(config_path: Path, state_file: Path) -> str:
    return (
        "Use $audible-goodreads-deal-scout to evaluate the current Audible daily promotion "
        f"with config at {config_path} in scheduled mode using state file {state_file}."
    )


def build_cron_command(
    *,
    openclaw_bin: str,
    spec: dict[str, str],
    config_path: Path,
    state_file: Path,
    name: str | None = None,
    cron_expr: str | None = None,
) -> list[str]:
    validate_timezone(spec)
    resolved_openclaw_bin = resolve_openclaw_bin(openclaw_bin)
    return [
        resolved_openclaw_bin,
        "--no-color",
        "cron",
        "add",
        "--name",
        name or f"Audible Goodreads Deal ({spec['key'].upper()})",
        "--cron",
        cron_expr or spec["defaultCron"],
        "--tz",
        spec["timezone"],
        "--session",
        "isolated",
        "--message",
        build_cron_message(config_path, state_file),
        "--announce",
        "--json",
    ]


def list_cron_jobs(openclaw_bin: str) -> list[dict[str, Any]]:
    resolved_openclaw_bin = resolve_openclaw_bin(openclaw_bin)
    proc = subprocess.run(
        [resolved_openclaw_bin, "--no-color", "cron", "list", "--json"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "openclaw cron list failed")
    try:
        payload = json.loads(proc.stdout.strip() or "{}")
    except Exception:
        return []
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        jobs = payload.get("jobs")
        if isinstance(jobs, list):
            return [item for item in jobs if isinstance(item, dict)]
    return []


def find_matching_cron_job(
    jobs: list[dict[str, Any]],
    *,
    name: str,
    cron_expr: str,
    timezone_name: str,
    message: str,
) -> dict[str, Any] | None:
    for job in jobs:
        job_name = normalize_space(str(job.get("name") or ""))
        schedule = job.get("schedule") if isinstance(job.get("schedule"), dict) else {}
        payload = job.get("payload") if isinstance(job.get("payload"), dict) else {}
        job_cron = normalize_space(str(schedule.get("cron") or schedule.get("expr") or ""))
        if (
            job_name == name
            and job_cron == cron_expr
            and normalize_space(str(schedule.get("tz") or "")) == timezone_name
            and normalize_space(str(payload.get("message") or payload.get("text") or "")) == message
        ):
            return job
    return None


def register_cron_job(
    *,
    openclaw_bin: str,
    spec: dict[str, str],
    config_path: Path,
    state_file: Path,
    name: str | None = None,
    cron_expr: str | None = None,
) -> dict[str, Any]:
    job_name = name or f"Audible Goodreads Deal ({spec['key'].upper()})"
    schedule = cron_expr or spec["defaultCron"]
    message = build_cron_message(config_path, state_file)
    jobs = list_cron_jobs(openclaw_bin)
    existing = find_matching_cron_job(
        jobs,
        name=job_name,
        cron_expr=schedule,
        timezone_name=spec["timezone"],
        message=message,
    )
    command = build_cron_command(
        openclaw_bin=openclaw_bin,
        spec=spec,
        config_path=config_path,
        state_file=state_file,
        name=job_name,
        cron_expr=schedule,
    )
    if existing:
        return {"ok": True, "created": False, "existingJob": existing, "command": command}
    proc = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "openclaw cron add failed")
    payload = json.loads(proc.stdout.strip() or "{}")
    return {"ok": True, "created": True, "job": payload.get("job"), "command": command}


def _next_step(label: str, description: str, argv: list[str], *, optional: bool = False) -> dict[str, Any]:
    return {
        "label": label,
        "description": description,
        "optional": optional,
        "argv": argv,
        "command": shlex.join(argv),
    }


def build_setup_next_steps(
    *,
    config_path: Path,
    storage_dir: Path,
    spec: dict[str, str],
    config_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    wrapper = str(skill_root() / "scripts" / "audible-goodreads-deal-scout.sh")
    launcher = ["sh", wrapper]
    config_arg = str(config_path)
    steps = [
        _next_step(
            "doctor",
            "Validate config, local files, wrapper, OpenClaw binary, delivery, cron, and auth readiness.",
            [*launcher, "doctor", "--config-path", config_arg],
        ),
        _next_step(
            "check-daily-deal",
            "Prepare today's Audible daily promotion result for the OpenClaw skill runtime.",
            [*launcher, "prepare", "--config-path", config_arg],
        ),
    ]
    if config_payload.get("goodreadsCsvPath"):
        steps.append(
            _next_step(
                "scan-want-to-read",
                "Run a small Want-to-Read discount scan to verify Goodreads CSV and Audible matching.",
                [*launcher, "scan-want-to-read", "--config-path", config_arg, "--limit", "40"],
            )
        )
    auth_path = normalize_space(str(config_payload.get("audibleAuthPath") or ""))
    if auth_path:
        steps.append(
            _next_step(
                "check-audible-auth",
                "Check saved Audible auth readiness and file permissions without printing tokens.",
                [*launcher, "audible-auth-status", "--auth-path", auth_path],
                optional=True,
            )
        )
    else:
        suggested_auth_path = str(storage_dir / "audible-auth.json")
        steps.append(
            _next_step(
                "optional-audible-auth",
                "Optional: start external-browser Audible auth for member-visible Want-to-Read prices.",
                [*launcher, "audible-auth-start", "--auth-path", suggested_auth_path, "--audible-marketplace", spec["key"]],
                optional=True,
            )
        )
    return steps


def setup_configuration(
    options: dict[str, Any],
    *,
    openclaw_bin: str = "openclaw",
    register_cron: bool = False,
) -> dict[str, Any]:
    ensure_python_version()
    marketplace = normalize_space(str(options.get("audibleMarketplace") or "us")).lower() or "us"
    spec = validate_marketplace(marketplace)
    storage_dir = Path(str(options.get("storageDir") or default_storage_dir())).expanduser()
    config_path = Path(str(options.get("configPath") or storage_dir / "config.json")).expanduser()
    state_file = Path(str(options.get("stateFile") or storage_dir / "state.json")).expanduser()
    preferences_path = Path(str(options.get("preferencesPath") or storage_dir / "preferences.md")).expanduser()
    threshold = float(options.get("threshold") or DEFAULT_THRESHOLD)
    privacy_mode = normalize_space(str(options.get("privacyMode") or "normal")).lower() or "normal"
    notes_file = normalize_space(str(options.get("notesFile") or ""))
    notes_text = resolve_notes_text(notes_file, str(options.get("notesText") or ""))
    goodreads_csv = normalize_space(str(options.get("goodreadsCsvPath") or ""))
    daily_enabled = bool(options.get("dailyAutomation"))
    cron_expr = normalize_space(str(options.get("dailyCron") or spec["defaultCron"]))
    artifact_dir = Path(str(options.get("artifactDir") or storage_dir / "artifacts" / "current")).expanduser()
    delivery_channel = normalize_space(str(options.get("deliveryChannel") or ""))
    delivery_target = normalize_space(str(options.get("deliveryTarget") or ""))
    delivery_policy = normalize_delivery_policy(str(options.get("deliveryPolicy") or DEFAULT_DELIVERY_POLICY))
    if notes_text:
        notes_text = notes_text.rstrip() + "\n"
    config_payload = config_template(
        audibleMarketplace=spec["key"],
        threshold=threshold,
        goodreadsCsvPath=goodreads_csv or None,
        preferencesPath=str(preferences_path) if notes_text else None,
        privacyMode=privacy_mode if privacy_mode in SUPPORTED_PRIVACY_MODES else "normal",
        stateFile=str(state_file) if daily_enabled else None,
        artifactDir=str(artifact_dir),
        freshnessDays=int(options.get("freshnessDays") or DEFAULT_FRESHNESS_DAYS),
        csvColumns=options.get("csvColumns") or {},
        audibleDealUrl=options.get("audibleDealUrl") or None,
        audibleFetchBackend=options.get("audibleFetchBackend") or "auto",
        audibleAuthPath=options.get("audibleAuthPath") or None,
        dailyCron=cron_expr if daily_enabled else None,
        deliveryChannel=delivery_channel or None,
        deliveryTarget=delivery_target or None,
        deliveryPolicy=delivery_policy,
    )
    cron_command = None
    if daily_enabled:
        cron_command = build_cron_command(
            openclaw_bin=openclaw_bin,
            spec=spec,
            config_path=config_path,
            state_file=state_file,
            cron_expr=cron_expr,
        )

    manual_result = {
        "ok": True,
        "written": False,
        "configPath": str(config_path),
        "preferencesPath": str(preferences_path) if notes_text else None,
        "stateFile": str(state_file) if daily_enabled else None,
        "config": config_payload,
        "configJson": json.dumps(config_payload, indent=2, sort_keys=True, ensure_ascii=False),
        "cronCommand": cron_command,
        "marketplace": spec["key"],
        "nextSteps": build_setup_next_steps(
            config_path=config_path,
            storage_dir=storage_dir,
            spec=spec,
            config_payload=config_payload,
        ),
    }

    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        write_json_atomic(config_path, config_payload)
        if notes_text:
            atomic_write_text(preferences_path, notes_text)
    except OSError:
        return {**manual_result, "manualOnly": True}

    result = {**manual_result, "written": True, "manualOnly": False}
    if daily_enabled and register_cron:
        result["cronRegistration"] = register_cron_job(
            openclaw_bin=openclaw_bin,
            spec=spec,
            config_path=config_path,
            state_file=state_file,
            cron_expr=cron_expr,
        )
    return result


def resolve_delivery_settings(
    *,
    config_path: Path | None,
    delivery_channel: str | None = None,
    delivery_target: str | None = None,
) -> tuple[Path, str, str, str]:
    path, config = load_config(config_path)
    channel = normalize_space(str(delivery_channel or config.get("deliveryChannel") or ""))
    target = normalize_space(str(delivery_target or config.get("deliveryTarget") or ""))
    policy = normalize_delivery_policy(str(config.get("deliveryPolicy") or DEFAULT_DELIVERY_POLICY))
    if not channel:
        raise RuntimeError(
            f"No delivery channel configured. Set deliveryChannel in {path} or pass --delivery-channel."
        )
    if not target:
        raise RuntimeError(
            f"No delivery target configured. Set deliveryTarget in {path} or pass --delivery-target."
        )
    return path, channel, target, policy


def resolve_delivery_policy(
    *,
    config_path: Path | None,
    delivery_policy: str | None = None,
) -> tuple[Path, str]:
    path, config = load_config(config_path)
    policy = normalize_delivery_policy(delivery_policy or str(config.get("deliveryPolicy") or DEFAULT_DELIVERY_POLICY))
    return path, policy


def normalize_delivery_policy(value: str | None) -> str:
    normalized = normalize_space(str(value or "")).lower() or DEFAULT_DELIVERY_POLICY
    if normalized not in SUPPORTED_DELIVERY_POLICIES:
        return DEFAULT_DELIVERY_POLICY
    return normalized


def deliver_message(
    *,
    message_text: str,
    config_path: Path | None,
    delivery_channel: str | None = None,
    delivery_target: str | None = None,
    openclaw_bin: str = "openclaw",
    dry_run: bool = False,
) -> dict[str, Any]:
    path, channel, target, policy = resolve_delivery_settings(
        config_path=config_path,
        delivery_channel=delivery_channel,
        delivery_target=delivery_target,
    )
    normalized_message = str(message_text or "").strip()
    if not normalized_message:
        raise RuntimeError("Cannot deliver an empty message.")
    command = [
        resolve_openclaw_bin(openclaw_bin),
        "message",
        "send",
        "--channel",
        channel,
        "--target",
        target,
        "--message",
        normalized_message,
        "--json",
    ]
    if dry_run:
        command.insert(-1, "--dry-run")
    proc = subprocess.run(command, capture_output=True, text=True, timeout=60)
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        raise RuntimeError(stderr or stdout or "openclaw message send failed")
    payload = json.loads(stdout or "{}")
    return {
        "ok": True,
        "configPath": str(path),
        "deliveryChannel": channel,
        "deliveryTarget": target,
        "deliveryPolicy": policy,
        "dryRun": dry_run,
        "payload": payload.get("payload") if isinstance(payload, dict) else payload,
        "raw": payload,
    }
