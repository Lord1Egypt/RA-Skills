from __future__ import annotations

import hashlib
import json
import math
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


SCHEDULED_TRIGGER_FILENAME = "scheduled-trigger.js"
SCHEDULED_THINKING = "low"


def _run_openclaw(command: list[str], *, timeout: int, action: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"{action} timed out after {timeout} seconds.") from exc


def _json_output(stdout: str, *, action: str) -> Any:
    try:
        return json.loads(stdout.strip() or "{}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{action} returned invalid JSON.") from exc


def _successful_json_output(stdout: str, *, action: str) -> dict[str, Any]:
    payload = _json_output(stdout, action=action)
    if not isinstance(payload, dict):
        raise RuntimeError(f"{action} returned an unexpected JSON payload.")
    nested_value = payload.get("payload")
    nested = nested_value if isinstance(nested_value, dict) else {}
    failed = payload if payload.get("ok") is False else nested if nested.get("ok") is False else None
    if failed is not None:
        raise RuntimeError(str(failed.get("error") or failed.get("message") or f"{action} failed."))
    return payload


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
        "Complete the preprepared Audible deal run. Do not run preparation again. "
        "Follow the condition trigger's appended instructions exactly; "
        "return NO_REPLY after a skipped policy or successful direct delivery. "
        f"Config: {config_path}. State: {state_file}."
    )


def cron_declaration_key(config_path: Path) -> str:
    digest = hashlib.sha256(str(config_path.expanduser().resolve()).encode("utf-8")).hexdigest()[:20]
    return f"audible-goodreads-deal-scout:{digest}"


def scheduled_trigger_path(config_path: Path) -> Path:
    return config_path.expanduser().resolve().parent / SCHEDULED_TRIGGER_FILENAME


def build_scheduled_trigger_script(config_path: Path, state_file: Path) -> str:
    wrapper = skill_root() / "scripts" / "audible-goodreads-deal-scout.sh"
    command = shlex.join(
        [
            "sh",
            str(wrapper),
            "scheduled-gate",
            "--config-path",
            str(config_path.expanduser().resolve()),
            "--state-file",
            str(state_file.expanduser().resolve()),
        ]
    )
    return (
        f"const result = await tools.call('exec', {{ command: {json.dumps(command)} }});\n"
        "const output = String(result?.result?.details?.aggregated ?? result?.result?.output ?? '').trim();\n"
        "let response;\n"
        "try {\n"
        "  const gate = JSON.parse(output);\n"
        "  response = gate && gate.ok === true\n"
        "    ? { fire: Boolean(gate.fire), message: String(gate.message || ''), state: { reasonCode: String(gate.reasonCode || ''), storeLocalDate: String(gate.storeLocalDate || '') } }\n"
        "    : { fire: true, message: 'Scheduled preparation returned an error before the agent turn.', state: { reasonCode: 'trigger_gate_failed' } };\n"
        "} catch (error) {\n"
        "  response = { fire: true, message: 'Scheduled preparation failed before the agent turn. Inspect the trigger execution.', state: { reasonCode: 'trigger_invalid_json' } };\n"
        "}\n"
        "json(response);\n"
    )


def write_scheduled_trigger(config_path: Path, state_file: Path) -> Path:
    path = scheduled_trigger_path(config_path)
    atomic_write_text(path, build_scheduled_trigger_script(config_path, state_file))
    return path


def build_cron_command(
    *,
    openclaw_bin: str,
    spec: dict[str, str],
    config_path: Path,
    state_file: Path,
    name: str | None = None,
    cron_expr: str | None = None,
    delivery_config: dict[str, Any] | None = None,
) -> list[str]:
    validate_timezone(spec)
    resolved_openclaw_bin = resolve_openclaw_bin(openclaw_bin)
    command = [
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
        "--declaration-key",
        cron_declaration_key(config_path),
        "--light-context",
        "--thinking",
        SCHEDULED_THINKING,
        "--trigger-script",
        str(scheduled_trigger_path(config_path)),
        "--message",
        build_cron_message(config_path, state_file),
    ]
    command.extend(_cron_delivery_args(config_path, config=delivery_config))
    command.append("--json")
    return command


def list_cron_jobs(openclaw_bin: str) -> list[dict[str, Any]]:
    resolved_openclaw_bin = resolve_openclaw_bin(openclaw_bin)
    proc = _run_openclaw(
        [resolved_openclaw_bin, "--no-color", "cron", "list", "--json"],
        timeout=30,
        action="openclaw cron list",
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "openclaw cron list failed")
    payload = _json_output(proc.stdout, action="openclaw cron list")
    if isinstance(payload, dict) and payload.get("ok") is False:
        raise RuntimeError(str(payload.get("error") or "openclaw cron list failed"))
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
    delivery_channel: str | None = None,
    delivery_target: str | None = None,
) -> dict[str, Any] | None:
    for job in jobs:
        job_name = normalize_space(str(job.get("name") or ""))
        schedule_value = job.get("schedule")
        payload_value = job.get("payload")
        delivery_value = job.get("delivery")
        trigger_value = job.get("trigger")
        schedule = schedule_value if isinstance(schedule_value, dict) else {}
        payload = payload_value if isinstance(payload_value, dict) else {}
        delivery = delivery_value if isinstance(delivery_value, dict) else {}
        trigger = trigger_value if isinstance(trigger_value, dict) else {}
        job_cron = normalize_space(str(schedule.get("cron") or schedule.get("expr") or ""))
        if delivery_channel and delivery_target:
            delivery_matches = (
                normalize_space(str(delivery.get("channel") or "")) == delivery_channel
                and normalize_space(str(delivery.get("to") or "")) == delivery_target
            )
        else:
            delivery_matches = (
                not normalize_space(str(delivery.get("channel") or ""))
                and not normalize_space(str(delivery.get("to") or ""))
                and normalize_space(str(delivery.get("mode") or "none")) in {"", "none"}
            )
        if (
            job_name == name
            and job_cron == cron_expr
            and normalize_space(str(schedule.get("tz") or "")) == timezone_name
            and normalize_space(str(payload.get("message") or payload.get("text") or "")) == message
            and delivery_matches
            and payload.get("lightContext") is True
            and normalize_space(str(payload.get("thinking") or "")) == SCHEDULED_THINKING
            and bool(trigger.get("script"))
        ):
            return job
    return None


def find_related_cron_job(
    jobs: list[dict[str, Any]],
    *,
    name: str,
    message: str,
    config_path: Path,
) -> dict[str, Any] | None:
    config_marker = normalize_space(str(config_path))
    for job in jobs:
        job_name = normalize_space(str(job.get("name") or ""))
        payload_value = job.get("payload")
        payload = payload_value if isinstance(payload_value, dict) else {}
        job_message = normalize_space(str(payload.get("message") or payload.get("text") or ""))
        if job_name == name or (
            config_marker
            and config_marker in job_message
            and "audible-goodreads-deal-scout" in job_message
        ) or job_message == normalize_space(message):
            return job
    return None


def _cron_delivery_args(
    config_path: Path,
    *,
    editing: bool = False,
    config: dict[str, Any] | None = None,
) -> list[str]:
    if config is None:
        _, config = load_config(config_path)
    channel = normalize_space(str(config.get("deliveryChannel") or ""))
    target = normalize_space(str(config.get("deliveryTarget") or ""))
    if bool(channel) != bool(target):
        raise ValueError("deliveryChannel and deliveryTarget must be configured together.")
    if channel and target:
        return ["--announce", "--channel", channel, "--to", target]
    if editing:
        return ["--no-deliver", "--clear-channel", "--clear-to"]
    return ["--no-deliver"]


def build_cron_edit_command(
    *,
    openclaw_bin: str,
    job_id: str,
    spec: dict[str, str],
    config_path: Path,
    state_file: Path,
    name: str,
    cron_expr: str,
    enable: bool = False,
) -> list[str]:
    validate_timezone(spec)
    resolved_openclaw_bin = resolve_openclaw_bin(openclaw_bin)
    command = [
        resolved_openclaw_bin,
        "--no-color",
        "cron",
        "edit",
        job_id,
        "--name",
        name,
        "--cron",
        cron_expr,
        "--tz",
        spec["timezone"],
        "--session",
        "isolated",
        "--light-context",
        "--thinking",
        SCHEDULED_THINKING,
        "--trigger-script",
        str(scheduled_trigger_path(config_path)),
        "--message",
        build_cron_message(config_path, state_file),
    ]
    command.extend(_cron_delivery_args(config_path, editing=True))
    if enable:
        command.append("--enable")
    return command


def register_cron_job(
    *,
    openclaw_bin: str,
    spec: dict[str, str],
    config_path: Path,
    state_file: Path,
    name: str | None = None,
    cron_expr: str | None = None,
) -> dict[str, Any]:
    write_scheduled_trigger(config_path, state_file)
    job_name = name or f"Audible Goodreads Deal ({spec['key'].upper()})"
    schedule = cron_expr or spec["defaultCron"]
    message = build_cron_message(config_path, state_file)
    _, config = load_config(config_path)
    delivery_channel = normalize_space(str(config.get("deliveryChannel") or ""))
    delivery_target = normalize_space(str(config.get("deliveryTarget") or ""))
    jobs = list_cron_jobs(openclaw_bin)
    existing = find_matching_cron_job(
        jobs,
        name=job_name,
        cron_expr=schedule,
        timezone_name=spec["timezone"],
        message=message,
        delivery_channel=delivery_channel,
        delivery_target=delivery_target,
    )
    command = build_cron_command(
        openclaw_bin=openclaw_bin,
        spec=spec,
        config_path=config_path,
        state_file=state_file,
        name=job_name,
        cron_expr=schedule,
    )
    if existing and existing.get("enabled") is not False:
        return {"ok": True, "created": False, "updated": False, "existingJob": existing, "command": command}
    related = existing or find_related_cron_job(
        jobs,
        name=job_name,
        message=message,
        config_path=config_path,
    )
    if related and related.get("id"):
        edit_command = build_cron_edit_command(
            openclaw_bin=openclaw_bin,
            job_id=str(related["id"]),
            spec=spec,
            config_path=config_path,
            state_file=state_file,
            name=job_name,
            cron_expr=schedule,
            enable=True,
        )
        proc = _run_openclaw(edit_command, timeout=30, action="openclaw cron edit")
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "openclaw cron edit failed")
        updated_jobs = list_cron_jobs(openclaw_bin)
        updated_job = find_matching_cron_job(
            updated_jobs,
            name=job_name,
            cron_expr=schedule,
            timezone_name=spec["timezone"],
            message=message,
            delivery_channel=delivery_channel,
            delivery_target=delivery_target,
        )
        if not updated_job or updated_job.get("enabled") is False:
            raise RuntimeError("openclaw cron edit completed but the effective job does not match the requested config.")
        return {
            "ok": True,
            "created": False,
            "updated": True,
            "previousJob": related,
            "job": updated_job,
            "command": edit_command,
        }
    proc = _run_openclaw(command, timeout=30, action="openclaw cron add")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "openclaw cron add failed")
    payload = _successful_json_output(proc.stdout, action="openclaw cron add")
    created_jobs = list_cron_jobs(openclaw_bin)
    created_job = find_matching_cron_job(
        created_jobs,
        name=job_name,
        cron_expr=schedule,
        timezone_name=spec["timezone"],
        message=message,
        delivery_channel=delivery_channel,
        delivery_target=delivery_target,
    )
    if not created_job:
        raise RuntimeError("openclaw cron add completed but the requested job was not found afterward.")
    return {
        "ok": True,
        "created": True,
        "updated": False,
        "job": created_job,
        "raw": payload,
        "command": command,
    }


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


def disable_related_cron_job(
    *,
    openclaw_bin: str,
    config_path: Path,
    spec: dict[str, str],
    state_file: Path,
    name: str | None = None,
) -> dict[str, Any]:
    job_name = name or f"Audible Goodreads Deal ({spec['key'].upper()})"
    message = build_cron_message(config_path, state_file)
    jobs = list_cron_jobs(openclaw_bin)
    related = find_related_cron_job(jobs, name=job_name, message=message, config_path=config_path)
    if not related or not related.get("id"):
        return {"ok": True, "disabled": False, "job": None}
    command = [
        resolve_openclaw_bin(openclaw_bin),
        "--no-color",
        "cron",
        "edit",
        str(related["id"]),
        "--disable",
        "--no-deliver",
        "--clear-channel",
        "--clear-to",
        "--clear-trigger",
    ]
    proc = _run_openclaw(command, timeout=30, action="openclaw cron disable")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "openclaw cron disable failed")
    updated_jobs = list_cron_jobs(openclaw_bin)
    updated = next((job for job in updated_jobs if job.get("id") == related.get("id")), None)
    if not updated or updated.get("enabled") is not False:
        raise RuntimeError("openclaw cron disable completed but the job is still enabled or missing.")
    return {"ok": True, "disabled": True, "job": updated, "command": command}


def setup_configuration(
    options: dict[str, Any],
    *,
    openclaw_bin: str = "openclaw",
    register_cron: bool = False,
) -> dict[str, Any]:
    ensure_python_version()
    initial_storage_dir = Path(str(options.get("storageDir") or default_storage_dir())).expanduser().resolve()
    config_path = Path(str(options.get("configPath") or initial_storage_dir / "config.json")).expanduser().resolve()
    existing_config: dict[str, Any] = {}
    existing_config_found = config_path.exists()
    if config_path.exists():
        _, existing_config = load_config(config_path)

    def option_or_existing(key: str, default: Any = None) -> Any:
        if key in options and options.get(key) is not None:
            return options[key]
        if key in existing_config:
            return existing_config[key]
        return default

    marketplace = normalize_space(str(option_or_existing("audibleMarketplace", "us"))).lower() or "us"
    spec = validate_marketplace(marketplace)
    if options.get("storageDir"):
        storage_dir = Path(str(options["storageDir"])).expanduser().resolve()
    elif options.get("configPath"):
        storage_dir = config_path.parent
    else:
        storage_dir = initial_storage_dir
    def setup_path(value: Any) -> Path:
        path = Path(str(value)).expanduser()
        if not path.is_absolute():
            path = config_path.parent / path
        return path.resolve()

    state_file = setup_path(option_or_existing("stateFile", storage_dir / "state.json"))
    preferences_path = setup_path(option_or_existing("preferencesPath", storage_dir / "preferences.md"))
    threshold = float(option_or_existing("threshold", DEFAULT_THRESHOLD))
    if not math.isfinite(threshold) or not 0 <= threshold <= 5:
        raise ValueError("threshold must be a finite number between 0 and 5.")
    privacy_mode = normalize_space(str(option_or_existing("privacyMode", "normal"))).lower() or "normal"
    if privacy_mode not in SUPPORTED_PRIVACY_MODES:
        raise ValueError(f"privacyMode must be one of: {', '.join(sorted(SUPPORTED_PRIVACY_MODES))}.")
    notes_file = normalize_space(str(options.get("notesFile") or ""))
    notes_text = resolve_notes_text(notes_file, str(options.get("notesText") or ""))
    goodreads_csv = normalize_space(str(option_or_existing("goodreadsCsvPath", "")))
    daily_option = options.get("dailyAutomation")
    daily_enabled = (
        bool(existing_config.get("dailyCron") or existing_config.get("stateFile"))
        if daily_option is None
        else bool(daily_option)
    )
    cron_expr = normalize_space(str(option_or_existing("dailyCron", spec["defaultCron"])))
    artifact_dir = setup_path(option_or_existing("artifactDir", storage_dir / "artifacts" / "current"))
    no_delivery = bool(options.get("noDelivery"))
    delivery_channel = "" if no_delivery else normalize_space(str(option_or_existing("deliveryChannel", "")))
    delivery_target = "" if no_delivery else normalize_space(str(option_or_existing("deliveryTarget", "")))
    if bool(delivery_channel) != bool(delivery_target):
        raise ValueError("deliveryChannel and deliveryTarget must be configured together.")
    delivery_policy = normalize_delivery_policy(str(option_or_existing("deliveryPolicy", DEFAULT_DELIVERY_POLICY)))
    csv_columns = option_or_existing("csvColumns", {})
    if notes_text:
        notes_text = notes_text.rstrip() + "\n"
    preferences_config_path = str(preferences_path) if notes_text else existing_config.get("preferencesPath")
    freshness_days = int(option_or_existing("freshnessDays", DEFAULT_FRESHNESS_DAYS))
    if freshness_days < 0:
        raise ValueError("freshnessDays must be zero or greater.")
    fetch_backend = normalize_space(str(option_or_existing("audibleFetchBackend", "auto"))).lower() or "auto"
    if fetch_backend not in {"auto", "curl", "python"}:
        raise ValueError("audibleFetchBackend must be one of: auto, curl, python.")
    config_payload = dict(existing_config) if existing_config_found else config_template()
    config_payload.update(
        {
            "audibleMarketplace": spec["key"],
            "threshold": threshold,
            "goodreadsCsvPath": goodreads_csv or None,
            "preferencesPath": preferences_config_path,
            "privacyMode": privacy_mode,
            "stateFile": str(state_file) if daily_enabled else None,
            "artifactDir": str(artifact_dir),
            "freshnessDays": freshness_days,
            "csvColumns": csv_columns if isinstance(csv_columns, dict) else {},
            "audibleDealUrl": option_or_existing("audibleDealUrl"),
            "audibleFetchBackend": fetch_backend,
            "audibleAuthPath": option_or_existing("audibleAuthPath"),
            "dailyCron": cron_expr if daily_enabled else None,
            "deliveryChannel": delivery_channel or None,
            "deliveryTarget": delivery_target or None,
            "deliveryPolicy": delivery_policy,
        }
    )
    cron_command = None
    if daily_enabled:
        cron_command = build_cron_command(
            openclaw_bin=openclaw_bin,
            spec=spec,
            config_path=config_path,
            state_file=state_file,
            cron_expr=cron_expr,
            delivery_config=config_payload,
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

    config_written = False
    trigger_path: Path | None = None
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        write_json_atomic(config_path, config_payload)
        config_written = True
        if notes_text:
            atomic_write_text(preferences_path, notes_text)
        if daily_enabled:
            trigger_path = write_scheduled_trigger(config_path, state_file)
    except OSError as exc:
        return {
            **manual_result,
            "ok": False,
            "written": config_written,
            "manualOnly": not config_written,
            "error": str(exc),
        }

    result = {**manual_result, "written": True, "manualOnly": False}
    if daily_enabled:
        result["scheduledTriggerPath"] = str(trigger_path)
        if register_cron:
            result["cronRegistration"] = register_cron_job(
                openclaw_bin=openclaw_bin,
                spec=spec,
                config_path=config_path,
                state_file=state_file,
                cron_expr=cron_expr,
            )
    elif register_cron:
        result["cronRegistration"] = disable_related_cron_job(
            openclaw_bin=openclaw_bin,
            config_path=config_path,
            spec=spec,
            state_file=state_file,
        )
        trigger_path = scheduled_trigger_path(config_path)
        try:
            if trigger_path.exists():
                trigger_path.unlink()
        except OSError as exc:
            return {**result, "ok": False, "error": str(exc)}
    return result


def resolve_delivery_settings(
    *,
    config_path: Path | None,
    delivery_channel: str | None = None,
    delivery_target: str | None = None,
) -> tuple[Path, str, str, str]:
    path, config = load_config(config_path)
    channel_override = normalize_space(str(delivery_channel or ""))
    target_override = normalize_space(str(delivery_target or ""))
    if bool(channel_override) != bool(target_override):
        raise RuntimeError("--delivery-channel and --delivery-target must be passed together.")
    if channel_override and target_override:
        channel, target = channel_override, target_override
    else:
        channel = normalize_space(str(config.get("deliveryChannel") or ""))
        target = normalize_space(str(config.get("deliveryTarget") or ""))
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
        raise ValueError(
            f"deliveryPolicy must be one of: {', '.join(sorted(SUPPORTED_DELIVERY_POLICIES))}."
        )
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
    proc = _run_openclaw(command, timeout=60, action="openclaw message send")
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        raise RuntimeError(stderr or stdout or "openclaw message send failed")
    payload = _successful_json_output(stdout, action="openclaw message send")
    return {
        "ok": True,
        "delivered": not dry_run,
        "simulated": dry_run,
        "configPath": str(path),
        "deliveryChannel": channel,
        "deliveryTarget": target,
        "deliveryPolicy": policy,
        "dryRun": dry_run,
        "payload": payload.get("payload"),
        "raw": payload,
    }
