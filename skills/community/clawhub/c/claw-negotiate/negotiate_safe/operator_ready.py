"""Operator install/setup helpers for negotiate_safe.

These commands are for people installing the skill on their own OpenClaw
instance. They fail before a live negotiation when required config,
sshsign, or OpenClaw primitives are missing.
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping


Runner = Callable[..., subprocess.CompletedProcess]


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str = ""
    fix: str = ""


ENV_PATH_PREFIX = "skills.entries.negotiate_safe.env."
SKILL_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = SKILL_DIR / "skill_manifest.json"
OPENCLAW_CONFIG_PATH = Path("/root/.openclaw/openclaw.json")


def _env(env: Mapping[str, str] | None) -> Mapping[str, str]:
    if env is not None:
        return env
    merged: dict[str, str] = {}
    try:
        cfg = json.loads(OPENCLAW_CONFIG_PATH.read_text(encoding="utf-8"))
        skill_env = (
            cfg.get("skills", {})
            .get("entries", {})
            .get("negotiate_safe", {})
            .get("env", {})
        )
        if isinstance(skill_env, dict):
            merged.update({str(k): str(v) for k, v in skill_env.items() if v is not None})
    except (OSError, json.JSONDecodeError, AttributeError):
        pass
    merged.update(os.environ)
    return merged


def load_skill_manifest(path: str | Path = MANIFEST_PATH) -> dict:
    """Load the install manifest used by deploy/install tooling."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_env_file(path: str | Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE env file for operator setup."""
    updates: dict[str, str] = {}
    p = Path(path).expanduser()
    for lineno, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"{p}:{lineno}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            raise ValueError(f"{p}:{lineno}: empty key")
        updates[key] = value
    return updates


def _check_env_present(env: Mapping[str, str], key: str, fix: str = "") -> Check:
    value = (env.get(key) or "").strip()
    return Check(
        name=key,
        ok=bool(value),
        detail="configured" if value else "missing",
        fix=fix or f"openclaw config set {ENV_PATH_PREFIX}{key} <value>",
    )


def _check_role(env: Mapping[str, str]) -> Check:
    role = (env.get("NEGOTIATE_SAFE_BOT_ROLE") or "").strip().lower()
    ok = role in ("founder", "investor")
    return Check(
        name="NEGOTIATE_SAFE_BOT_ROLE",
        ok=ok,
        detail=role or "missing",
        fix=(
            f"openclaw config set {ENV_PATH_PREFIX}"
            "NEGOTIATE_SAFE_BOT_ROLE founder"
        ),
    )


def _check_command(
    name: str,
    argv: list[str],
    runner: Runner,
    timeout: int = 10,
    accept_json_error: bool = False,
) -> Check:
    try:
        result = runner(argv, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return Check(name=name, ok=False, detail=f"{argv[0]} not found", fix=f"Install {argv[0]}.")
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode(errors="ignore") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode(errors="ignore") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        body = (stdout or stderr or "").strip()
        if "Usage:" in body:
            return Check(name=name, ok=True, detail=body[:160])
        return Check(name=name, ok=False, detail="timeout", fix="Check network/service availability.")
    except OSError as exc:
        return Check(name=name, ok=False, detail=str(exc), fix="Check local command availability.")

    body = (result.stdout or result.stderr or "").strip()
    if result.returncode == 0:
        return Check(name=name, ok=True, detail=body[:160] or "ok")
    if accept_json_error:
        try:
            payload = json.loads(result.stdout or "{}")
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict) and payload.get("error"):
            return Check(name=name, ok=True, detail=f"available ({payload['error']})")
    return Check(name=name, ok=False, detail=body[:200] or f"exit {result.returncode}", fix="Run the command manually for details.")


def _check_lease_command(host: str, runner: Runner) -> Check:
    name = "workflow leases"
    try:
        result = runner(
            [
                "ssh", host, "acquire-lease",
                "--session-id", "__doctor_missing__",
                "--role", "founder",
                "--action", "negotiate",
                "--holder", "doctor",
                "--ttl", "15",
            ],
            capture_output=True, text=True, timeout=15,
        )
    except FileNotFoundError:
        return Check(name=name, ok=False, detail="ssh not found", fix="Install ssh.")
    except subprocess.TimeoutExpired:
        return Check(name=name, ok=False, detail="timeout", fix="Check sshsign availability.")
    except OSError as exc:
        return Check(name=name, ok=False, detail=str(exc), fix="Check local ssh availability.")

    body = (result.stdout or result.stderr or "").strip()
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        payload = {}
    if isinstance(payload, dict):
        error = str(payload.get("error") or "")
        if error and "unknown command" not in error.lower():
            return Check(name=name, ok=True, detail=f"available ({error})")
        if payload.get("generation"):
            return Check(name=name, ok=True, detail="available")
    return Check(
        name=name,
        ok=False,
        detail=body[:200] or f"exit {result.returncode}",
        fix="Deploy an sshsign build that supports acquire-lease.",
    )


def doctor_checks(
    env: Mapping[str, str] | None = None,
    runner: Runner = subprocess.run,
) -> list[Check]:
    e = _env(env)
    checks = [
        _check_env_present(e, "USER_DID"),
        _check_env_present(e, "TELEGRAM_BOT_USERNAME"),
        _check_role(e),
    ]
    host = (e.get("SSHSIGN_HOST") or "sshsign.dev").strip()
    checks.append(_check_command(
        "sshsign get-session",
        ["ssh", host, "get-session", "--session-id", "__doctor_missing__"],
        runner=runner,
        timeout=15,
        accept_json_error=True,
    ))
    checks.append(_check_command(
        "openclaw cron list",
        ["openclaw", "cron", "list"],
        runner=runner,
        timeout=30,
    ))
    checks.append(_check_command(
        "openclaw message send",
        ["openclaw", "message", "send", "--help"],
        runner=runner,
        timeout=30,
    ))
    checks.append(_check_lease_command(host, runner=runner))
    return checks


def format_doctor(checks: list[Check]) -> str:
    lines: list[str] = []
    for check in checks:
        status = "ok" if check.ok else "fail"
        detail = f" - {check.detail}" if check.detail else ""
        lines.append(f"{status:<5} {check.name}{detail}")
        if not check.ok and check.fix:
            lines.append(f"fix   {check.fix}")
    return "\n".join(lines) + ("\n" if lines else "")


def build_operator_updates(
    *,
    role: str,
    bot_username: str = "",
    sshsign_host: str = "",
    scan_interval: str = "",
) -> dict[str, str]:
    role_norm = role.strip().lower()
    if role_norm not in ("founder", "investor"):
        raise ValueError("--role must be founder or investor")

    updates = {"NEGOTIATE_SAFE_BOT_ROLE": role_norm}
    if bot_username:
        handle = bot_username.strip()
        if handle.startswith("@"):
            handle = handle[1:]
        updates["TELEGRAM_BOT_USERNAME"] = handle
    if sshsign_host:
        updates["SSHSIGN_HOST"] = sshsign_host.strip()
    if scan_interval:
        updates["CLAW_NEGOTIATE_SCAN_INTERVAL"] = scan_interval.strip()
    return updates


def _config_has_env_value(key: str, value: str, path: Path | None = None) -> bool:
    path = path or OPENCLAW_CONFIG_PATH
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    env = (
        cfg.get("skills", {})
        .get("entries", {})
        .get("negotiate_safe", {})
        .get("env", {})
    )
    return isinstance(env, dict) and str(env.get(key) or "") == value


def persist_operator_updates(
    updates: dict[str, str],
    runner: Runner = subprocess.run,
) -> list[str]:
    failures: list[str] = []
    for key, value in updates.items():
        path = f"{ENV_PATH_PREFIX}{key}"
        try:
            result = runner(
                ["openclaw", "config", "set", path, value],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            if not _config_has_env_value(key, value):
                failures.append(key)
            continue
        except (FileNotFoundError, OSError):
            failures.append(key)
            continue
        if result.returncode != 0 and not _config_has_env_value(key, value):
            failures.append(key)
    return failures
