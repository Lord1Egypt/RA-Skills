#!/usr/bin/env python3
"""Collect runtime signals and update the compliance assessment JSON.

Each control is judged on what can be observed or exercised on this host: the
guard is run through self-tests (approval without a terminal must be refused, a
forged session file must be discarded, an idle elevated session must expire),
not just checked for presence. A compliant control carries no gap, mitigation or
due date; an open control keeps the due date it was first given.

Review before use. This script makes no network calls itself. It runs
egress_monitor.py, which resolves allowlisted hostnames through DNS.
"""
import argparse
import contextlib
import io
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_logger  # noqa: E402
import security_config  # noqa: E402


AUDIT_LOG = Path.home() / ".openclaw" / "security" / "privileged-audit.jsonl"
OPENCLAW_DIR = Path.home() / ".openclaw"
REAL_SUDO = "/usr/bin/sudo"
GATEWAY_PLIST = Path.home() / "Library" / "LaunchAgents" / "ai.openclaw.gateway.plist"
SERVICE_ENV_FILE = OPENCLAW_DIR / "service-env" / "ai.openclaw.gateway.env"
MAX_RELEASE_AGE_MONTHS = 3


def run_cmd(cmd: List[str], env: Optional[Dict[str, str]] = None) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"\n{exc}"
    if proc.returncode != 0:
        return (proc.stdout or "") + "\n" + (proc.stderr or "")
    return proc.stdout


def resolve_openclaw_bin() -> str:
    override = Path.home() / ".openclaw" / "openclaw-bin-path.txt"
    if override.exists():
        candidate = override.read_text(encoding="utf-8").strip()
        if candidate and Path(candidate).exists():
            return candidate
    for candidate in (
        shutil.which("openclaw"),
        "/opt/homebrew/bin/openclaw",
        "/usr/local/bin/openclaw",
        str(Path.home() / ".npm-global" / "bin" / "openclaw"),
    ):
        if candidate and Path(candidate).exists():
            return candidate
    return "openclaw"


def _service_path() -> str:
    """The PATH the gateway service runs with, from its generated environment file."""
    try:
        for line in SERVICE_ENV_FILE.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\s*(?:export\s+)?PATH=(.*)$", line)
            if match:
                return match.group(1).strip().strip("'\"")
    except OSError:
        pass
    return ""


def openclaw_env(openclaw_bin: str) -> Dict[str, str]:
    """Environment for running the openclaw CLI.

    The CLI is a Node script. A scheduled job starts with a bare PATH that has no
    node on it, so add the places the gateway's own Node is found.
    """
    candidates = [str(Path(openclaw_bin).parent)] if os.path.isabs(openclaw_bin) else []
    candidates += [d for d in _service_path().split(":") if d]
    candidates += ["/opt/homebrew/bin", "/usr/local/bin"]
    current = [d for d in os.environ.get("PATH", "").split(":") if d]
    seen: List[str] = []
    for directory in candidates + current:
        if directory not in seen:
            seen.append(directory)
    env = dict(os.environ)
    env["PATH"] = ":".join(seen)
    return env


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def due_in(days: int) -> str:
    """Return an ISO date string *days* from now, for dynamic due dates."""
    return (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%d")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def load_openclaw_config() -> Optional[Dict[str, object]]:
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    if not cfg_path.exists():
        return None
    try:
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_env_flags() -> Dict[str, str]:
    """Settings from ~/.openclaw/env, read with the same loader the guard uses."""
    return security_config.load_env_file()


def load_json_file(path: Path) -> Optional[object]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def permissions_hardened(path: Path) -> bool:
    try:
        mode = path.stat().st_mode & 0o777
        return (mode & 0o077) == 0
    except Exception:
        return False


def find_channel_allowlists(cfg: Dict[str, object]) -> bool:
    channels = cfg.get("channels") if isinstance(cfg, dict) else None
    if not isinstance(channels, dict):
        return False
    for channel_cfg in channels.values():
        if isinstance(channel_cfg, dict):
            allow_from = channel_cfg.get("allowFrom")
            if isinstance(allow_from, list) and len(allow_from) > 0:
                return True
    return False


def group_mentions_required(cfg: Dict[str, object]) -> bool:
    channels = cfg.get("channels") if isinstance(cfg, dict) else None
    if isinstance(channels, dict):
        for channel_cfg in channels.values():
            groups = channel_cfg.get("groups") if isinstance(channel_cfg, dict) else None
            if isinstance(groups, dict):
                for group_cfg in groups.values():
                    if isinstance(group_cfg, dict) and group_cfg.get("requireMention") is True:
                        return True
    messages = cfg.get("messages") if isinstance(cfg, dict) else None
    if isinstance(messages, dict):
        group_chat = messages.get("groupChat")
        if isinstance(group_chat, dict) and group_chat.get("mentionPatterns"):
            return True
    return False


def gateway_loopback_configured(cfg: Optional[Dict[str, object]], cfg_text: str) -> bool:
    if isinstance(cfg, dict):
        gateway = cfg.get("gateway", {})
        mode = gateway.get("mode") if isinstance(gateway, dict) else None
        bind = gateway.get("bind") if isinstance(gateway, dict) else None
        auth = cfg.get("auth") or gateway.get("auth")
        auth_mode = auth.get("mode") if isinstance(auth, dict) else None
        return mode == "local" and bind == "loopback" and auth_mode == "token"
    return '"mode": "local"' in cfg_text and '"bind": "loopback"' in cfg_text and '"mode": "token"' in cfg_text


def runtime_hook_installed() -> bool:
    hook = Path.home() / ".openclaw" / "bin" / "sudo"
    return hook.exists() and os.access(hook, os.X_OK)


def alt_privilege_paths_present() -> bool:
    return bool(shutil.which("su") or shutil.which("doas"))


def audit_log_present() -> bool:
    return AUDIT_LOG.exists() and AUDIT_LOG.stat().st_size > 0


def backup_configured() -> bool:
    for candidate in (OPENCLAW_DIR / "backups", OPENCLAW_DIR / "backup"):
        if candidate.exists() and any(candidate.iterdir()):
            return True
    return False


def _shim_first(path_value: str) -> bool:
    entries = [e for e in str(path_value or "").split(":") if e]
    shim_dir = str(OPENCLAW_DIR / "bin")
    if shim_dir not in entries:
        return False
    system_dirs = [i for i, e in enumerate(entries) if e in ("/usr/bin", "/bin", "/usr/local/bin")]
    return not system_dirs or entries.index(shim_dir) < min(system_dirs)


def hook_on_gateway_path(config: Optional[Dict[str, object]] = None) -> Optional[bool]:
    """Whether OpenClaw finds the sudo shim before the real sudo.

    Checked in the order OpenClaw applies them:
    1. ``tools.exec.pathPrepend`` in openclaw.json, which OpenClaw puts first on the
       PATH of every command it runs.
    2. The generated service environment file, which replaces the LaunchAgent's PATH
       on current releases.
    3. The gateway LaunchAgent's own PATH (older releases).

    None when none of these exists, so it cannot be determined.
    """
    shim_dir = OPENCLAW_DIR / "bin"
    tools = config.get("tools") if isinstance(config, dict) else None
    exec_cfg = tools.get("exec") if isinstance(tools, dict) else None
    prepend = exec_cfg.get("pathPrepend") if isinstance(exec_cfg, dict) else None
    if isinstance(prepend, list) and any(
        isinstance(e, str) and Path(e).expanduser() == shim_dir for e in prepend
    ):
        return True

    try:
        for line in SERVICE_ENV_FILE.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^\s*(?:export\s+)?PATH=(.*)$", line)
            if match:
                return _shim_first(match.group(1).strip().strip("'\""))
    except OSError:
        pass

    try:
        with GATEWAY_PLIST.open("rb") as f:
            env = plistlib.load(f).get("EnvironmentVariables") or {}
    except Exception:
        return None
    return _shim_first(str(env.get("PATH") or ""))


def passwordless_sudo_available() -> Optional[bool]:
    """True when sudo runs a command without asking for a password (cached credentials ignored)."""
    if not Path(REAL_SUDO).exists():
        return None
    try:
        proc = subprocess.run([REAL_SUDO, "-n", "-k", "true"], capture_output=True, text=True, timeout=10)
    except Exception:
        return None
    return proc.returncode == 0


def openclaw_runs_as_root() -> bool:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return True
    try:
        from egress_monitor import is_openclaw_command

        listing = subprocess.run(["ps", "-axo", "user=,command="], capture_output=True, text=True).stdout
    except Exception:
        return False
    for line in listing.splitlines():
        user, _, command = line.strip().partition(" ")
        if user == "root" and is_openclaw_command(command.strip()):
            return True
    return False


def timeout_selftest() -> bool:
    """An elevated session idle past the limit must drop to normal mode and need approval again."""
    try:
        import root_session_guard as guard

        state = guard.default_state()
        stale = guard.to_iso(guard.now_utc() - timedelta(minutes=guard.DEFAULT_TIMEOUT_MINUTES + 1))
        state.privilege_mode = "elevated"
        state.last_elevated_activity_utc = stale
        state.allowed_commands = [guard.AllowedCommand(argv=["/usr/bin/true"], added_at_utc=stale)]
        with contextlib.redirect_stdout(io.StringIO()):
            code = guard.authorize(state, guard.DEFAULT_TIMEOUT_MINUTES, ["/usr/bin/true"], None)
        return code == 2 and state.privilege_mode == "normal" and not state.allowed_commands
    except Exception:
        return False


def guard_selftest() -> Dict[str, bool]:
    """Exercise the approval guard's two refusals without running or logging anything."""
    results = {"refuses_without_terminal": False, "discards_forged_state": False}
    try:
        import guarded_privileged_exec as guarded

        class NoTerminal:
            def available(self) -> bool:
                return False

        approved, outcome = guarded.obtain_approval(NoTerminal(), "self-test", ["/usr/bin/true"], audit=False)
        results["refuses_without_terminal"] = (approved, outcome) == (False, "no_terminal")
    except Exception:
        pass
    try:
        import root_session_guard as guard

        now = guard.to_iso(guard.now_utc())
        forged = {
            "privilege_mode": "elevated",
            "last_elevated_activity_utc": now,
            "last_normal_activity_utc": now,
            "last_transition_utc": now,
            "last_action": "forged",
            "approved_reason": "forged",
            "approved_session_id": None,
            "allowed_commands": [{"argv": ["/usr/bin/true"], "added_at_utc": now}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            security_config.write_private(path, json.dumps(forged))
            with contextlib.redirect_stderr(io.StringIO()):
                state = guard.load_state(path)
        results["discards_forged_state"] = state.privilege_mode == "normal" and not state.allowed_commands
    except Exception:
        pass
    return results


def release_age_months(version_text: str, today: Optional[datetime] = None) -> Optional[int]:
    """Months since the release named by a date-based version such as "OpenClaw 2026.4.2"."""
    match = re.search(r"\b(20\d{2})\.(\d{1,2})\.\d+", version_text or "")
    if not match or not 1 <= int(match.group(2)) <= 12:
        return None
    today = today or datetime.now(timezone.utc)
    return max(0, (today.year - int(match.group(1))) * 12 + today.month - int(match.group(2)))


def collect_runtime_signals(port_monitor_script: Path) -> Dict[str, object]:
    openclaw_bin = resolve_openclaw_bin()
    openclaw_config_text = run_cmd(["cat", str(Path.home() / ".openclaw" / "openclaw.json")])
    cli_env = openclaw_env(openclaw_bin)
    doctor_text = run_cmd([openclaw_bin, "doctor"], cli_env)
    gateway_status_text = run_cmd([openclaw_bin, "gateway", "status"], cli_env)
    version_text = run_cmd([openclaw_bin, "--version"], cli_env)

    port_report_raw = run_cmd(["python3", str(port_monitor_script), "--json"])
    egress_report_raw = run_cmd(
        ["python3", str(Path(__file__).resolve().parent / "egress_monitor.py"), "--json"]
    )

    try:
        port_report = json.loads(port_report_raw)
    except Exception:
        port_report = {"status": "error", "findings": [], "listening_services": []}

    try:
        egress_report = json.loads(egress_report_raw)
    except Exception:
        egress_report = {"status": "error", "findings": [], "connections": []}

    return {
        "openclaw_config_text": openclaw_config_text,
        "openclaw_config_json": load_openclaw_config(),
        "doctor_text": doctor_text,
        "gateway_status_text": gateway_status_text,
        "version_text": version_text,
        "port_report": port_report,
        "egress_report": egress_report,
        "env_flags": load_env_flags(),
        "hook_installed": runtime_hook_installed(),
        "hook_on_gateway_path": hook_on_gateway_path(load_openclaw_config()),
        "passwordless_sudo": passwordless_sudo_available(),
        "runs_as_root": openclaw_runs_as_root(),
        "timeout_selftest": timeout_selftest(),
        "guard_selftest": guard_selftest(),
        "audit_chain": audit_logger.verify(AUDIT_LOG),
        "backup_configured": backup_configured(),
        "secrets_hardened": permissions_hardened(OPENCLAW_DIR) and permissions_hardened(OPENCLAW_DIR / "openclaw.json"),
        "command_policy": load_json_file(Path.home() / ".openclaw" / "security" / "command-policy.json"),
        "prompt_policy": load_json_file(Path.home() / ".openclaw" / "security" / "prompt-policy.json"),
        "egress_allowlist": load_json_file(Path.home() / ".openclaw" / "security" / "egress_allowlist.json"),
    }


def set_check(
    checks_by_id: Dict[str, Dict[str, object]],
    check_id: str,
    status: str,
    risk: str,
    observed_state: str,
    evidence: str,
    gap: str,
    mitigation: str,
    owner: str,
    due_date: str,
) -> None:
    c = checks_by_id.setdefault(check_id, {"check_id": check_id})
    if status == "compliant":
        # Nothing is open, so there is nothing to fix and no deadline.
        gap, mitigation, due_date = "", "", ""
    elif c.get("status") in ("partial", "violation") and c.get("due_date"):
        # Keep the deadline an open control was first given; do not push it out on every run.
        due_date = str(c["due_date"])
    c["status"] = status
    c["risk"] = risk
    c["observed_state"] = observed_state
    c["evidence"] = evidence
    c["gap"] = gap
    c["mitigation"] = mitigation
    c["owner"] = owner
    c["due_date"] = due_date


def build_assessment(assessment: Dict[str, object], signals: Dict[str, object]) -> Dict[str, object]:
    checks = assessment.get("checks", [])
    checks_by_id = {c["check_id"]: c for c in checks if isinstance(c, dict) and c.get("check_id")}

    cfg_text = str(signals.get("openclaw_config_text") or "")
    cfg_json = signals.get("openclaw_config_json")
    doctor = str(signals.get("doctor_text") or "")
    version_text = str(signals.get("version_text") or "").strip()
    port_report = signals.get("port_report") or {}
    findings = port_report.get("findings", []) if isinstance(port_report, dict) else []
    insecure = [f for f in findings if isinstance(f, dict) and f.get("type") == "insecure-port"]
    unapproved_ports = [f for f in findings if isinstance(f, dict) and f.get("type") == "unapproved-port"]

    def sig(name: str, fallback):
        return signals[name] if name in signals else fallback()

    hook_ok = bool(sig("hook_installed", runtime_hook_installed))
    selftest = sig("guard_selftest", guard_selftest)
    selftest = selftest if isinstance(selftest, dict) else {}
    guard_ok = bool(selftest.get("refuses_without_terminal")) and bool(selftest.get("discards_forged_state"))
    if not guard_ok:
        approval_status, approval_observed = "violation", (
            "Approval guard self-test failed: "
            + ", ".join(k for k in ("refuses_without_terminal", "discards_forged_state") if not selftest.get(k))
            + "."
        )
    elif not hook_ok:
        approval_status, approval_observed = "violation", (
            "Approval guard works, but sudo is not routed through it (runtime hook not installed)."
        )
    else:
        approval_status, approval_observed = "compliant", (
            "Approval guard refuses without a terminal and discards forged session state; sudo is routed through it."
        )
    set_check(
        checks_by_id,
        "privilege_approval_required",
        approval_status,
        "high",
        approval_observed,
        "Ran the guard's self-tests (no terminal, forged session file) and checked for ~/.openclaw/bin/sudo.",
        "Privileged actions can run without an approval given by a person at a terminal.",
        "Run cyber-security-engineer/scripts/install-openclaw-runtime-hook.sh, restart the OpenClaw gateway, "
        "and reinstall the skill if the self-test fails.",
        "Security Engineering",
        due_in(14),
    )

    runs_as_root = bool(sig("runs_as_root", openclaw_runs_as_root))
    writable_issue = "not writable" in doctor.lower()
    if runs_as_root:
        least_status, least_observed = "violation", "OpenClaw or this assessment is running as root."
    elif writable_issue:
        least_status, least_observed = "partial", "OpenClaw runs as a normal user, but openclaw doctor reports state that is not writable."
    else:
        least_status, least_observed = "compliant", "OpenClaw runs as a normal user and openclaw doctor reports no state permission problems."
    set_check(
        checks_by_id,
        "least_privilege_enforced",
        least_status,
        "high",
        least_observed,
        "Checked the user OpenClaw processes run as, and openclaw doctor output for state permission warnings.",
        "OpenClaw has more privilege than it needs, or its state directory permissions are wrong.",
        "Run OpenClaw as a normal user and fix state directory ownership and permissions.",
        "Platform Security",
        due_in(7),
    )

    timeout_ok = bool(sig("timeout_selftest", timeout_selftest))
    set_check(
        checks_by_id,
        "elevation_timeout_30m",
        "compliant" if timeout_ok else "violation",
        "medium",
        "An elevated session idle for more than 30 minutes dropped to normal mode in a self-test."
        if timeout_ok
        else "Idle-timeout self-test failed: a stale elevated session was not dropped.",
        "Ran root_session_guard.py's authorization against a session idle for 31 minutes.",
        "An idle elevated session is not expired.",
        "Reinstall the skill so root_session_guard.py is intact, and route all privileged commands "
        "through guarded_privileged_exec.py.",
        "Security Engineering",
        due_in(14),
    )

    chain = sig("audit_chain", lambda: audit_logger.verify(AUDIT_LOG))
    chain = chain if isinstance(chain, dict) else {}
    if not chain.get("ok", False):
        audit_status = "violation"
        audit_observed = f"Audit log hash chain is broken at entry {chain.get('broken_at')}: {chain.get('error')}."
    elif not chain.get("entries"):
        audit_status, audit_observed = "partial", "Privileged audit log not yet populated."
    else:
        audit_status = "compliant"
        audit_observed = f"Privileged audit log has {chain.get('entries')} entries and its hash chain is intact."
    set_check(
        checks_by_id,
        "audit_logging_privileged_actions",
        audit_status,
        "medium",
        audit_observed,
        f"Verified the hash chain of {AUDIT_LOG}.",
        "Audit trail is missing, empty, or has been altered.",
        "Run privileged tasks via guarded_privileged_exec.py; if the chain is broken, investigate who edited the log.",
        "SecOps",
        due_in(21),
    )

    set_check(
        checks_by_id,
        "open_ports_approved",
        "partial" if unapproved_ports else "compliant",
        "medium",
        f"Unapproved listening ports: {len(unapproved_ports)}",
        "port_monitor.py report evaluated vs approved baseline.",
        "Listening ports are not fully approved.",
        "Generate and prune approved_ports.json; close unnecessary services.",
        "Network Security",
        due_in(14),
    )

    public_ports = [f for f in findings if isinstance(f, dict) and f.get("type") == "public-bind"]
    set_check(
        checks_by_id,
        "public_listeners_justified",
        "partial" if public_ports else "compliant",
        "medium",
        f"Services listening on all interfaces without approval: {len(public_ports)}",
        "port_monitor.py public-bind findings evaluated against allow_public rules in the approved baseline.",
        "Services are reachable from the network without a recorded justification.",
        "Bind each service to localhost, or set \"allow_public\": true on its rule in approved_ports.json "
        "if the exposure is intended.",
        "Network Security",
        due_in(14),
    )

    set_check(
        checks_by_id,
        "insecure_ports_remediated",
        "violation" if insecure else "compliant",
        "high",
        f"Insecure ports detected: {len(insecure)}",
        "port_monitor.py findings evaluated for insecure-port entries.",
        "Insecure ports are still in use.",
        "Migrate to secure alternatives or close the ports.",
        "Network Security",
        due_in(21),
    )

    allowlist_ok = isinstance(cfg_json, dict) and find_channel_allowlists(cfg_json)
    set_check(
        checks_by_id,
        "channel_allowlist_configured",
        "compliant" if allowlist_ok else "violation",
        "high",
        "Channel allowlists are configured." if allowlist_ok else "Channel allowlists not detected.",
        "Checked channels.*.allowFrom in openclaw.json.",
        "Inbound channel allowlists are missing, allowing unsolicited access.",
        "Set channels.<channel>.allowFrom to trusted sender IDs.",
        "Platform Security",
        due_in(7),
    )

    mention_ok = isinstance(cfg_json, dict) and group_mentions_required(cfg_json)
    set_check(
        checks_by_id,
        "group_mentions_required",
        "compliant" if mention_ok else "partial",
        "medium",
        "Group chats require explicit mentions." if mention_ok else "Group mention requirement not detected.",
        "Checked channels.*.groups.requireMention or messages.groupChat.mentionPatterns.",
        "Group chats can trigger the agent without explicit mention.",
        "Set requireMention true for group configs or define mentionPatterns.",
        "Platform Security",
        due_in(7),
    )

    loopback_ok = gateway_loopback_configured(cfg_json, cfg_text)
    set_check(
        checks_by_id,
        "gateway_loopback_only",
        "compliant" if loopback_ok else "violation",
        "high",
        "Gateway is configured for local/loopback with token auth." if loopback_ok else "Gateway exposure settings are weak.",
        "Checked gateway.mode, gateway.bind, and auth.mode in openclaw.json.",
        "Gateway may be exposed publicly or without token auth.",
        "Set gateway.mode=local, gateway.bind=loopback, auth.mode=token.",
        "Platform Security",
        due_in(7),
    )

    secrets_ok = bool(
        sig(
            "secrets_hardened",
            lambda: permissions_hardened(OPENCLAW_DIR) and permissions_hardened(OPENCLAW_DIR / "openclaw.json"),
        )
    )
    set_check(
        checks_by_id,
        "secrets_permissions_hardened",
        "compliant" if secrets_ok else "partial",
        "medium",
        "OpenClaw config directory and file permissions are hardened." if secrets_ok else "OpenClaw permissions are too open or unknown.",
        "Checked ~/.openclaw and ~/.openclaw/openclaw.json permissions.",
        "Secrets and configs may be readable by other users.",
        "chmod 700 ~/.openclaw; chmod 600 ~/.openclaw/openclaw.json",
        "SecOps",
        due_in(7),
    )

    on_path = sig("hook_on_gateway_path", lambda: hook_on_gateway_path(cfg_json if isinstance(cfg_json, dict) else None))
    if not hook_ok:
        hook_status, hook_observed = "violation", "Runtime privileged execution hook missing."
    elif on_path is False:
        hook_status, hook_observed = "partial", (
            "Hook is installed, but OpenClaw does not put ~/.openclaw/bin before the real sudo on its PATH, so it is not used."
        )
    elif on_path is None:
        hook_status, hook_observed = "partial", (
            "Hook is installed; the gateway's PATH could not be checked on this platform."
        )
    else:
        hook_status, hook_observed = "compliant", "Hook is installed and OpenClaw finds it before the real sudo."
    set_check(
        checks_by_id,
        "runtime_privilege_hook_installed",
        hook_status,
        "high",
        hook_observed,
        "Checked ~/.openclaw/bin/sudo, tools.exec.pathPrepend, and the gateway service's PATH.",
        "The gateway can reach the real sudo without passing through the approval guard.",
        "Run install-openclaw-runtime-hook.sh, then restart the OpenClaw gateway.",
        "Security Engineering",
        due_in(7),
    )

    passwordless = sig("passwordless_sudo", passwordless_sudo_available)
    if passwordless is True:
        alt_status, alt_observed = "violation", (
            "sudo runs commands without a password, so calling /usr/bin/sudo directly bypasses the approval guard."
        )
    elif passwordless is None:
        alt_status, alt_observed = "partial", "Could not determine whether sudo requires a password."
    else:
        alt_status, alt_observed = "compliant", (
            "sudo requires a password, so calling it directly still stops at a prompt the agent cannot answer."
        )
    set_check(
        checks_by_id,
        "alternate_privilege_paths_restricted",
        alt_status,
        "medium",
        alt_observed,
        "Ran sudo non-interactively with cached credentials ignored (sudo -n -k true).",
        "Privilege can be gained without going through the approval guard.",
        "Remove NOPASSWD rules for this user from sudoers, and restrict su/doas the same way.",
        "Security Engineering",
        due_in(14),
    )

    backup_ok = bool(sig("backup_configured", backup_configured))
    set_check(
        checks_by_id,
        "backup_configured",
        "compliant" if backup_ok else "partial",
        "low",
        "OpenClaw backups found." if backup_ok else "OpenClaw backups not detected.",
        "Checked ~/.openclaw/backups or ~/.openclaw/backup.",
        "Recovery posture may be weak without backups.",
        "Configure backup of ~/.openclaw and audit logs.",
        "Platform Security",
        due_in(30),
    )

    age = release_age_months(version_text, signals.get("today"))  # type: ignore[arg-type]
    if age is None:
        update_status = "violation"
        update_observed = f"OpenClaw version could not be determined ({version_text or 'unknown'})."
    elif age > MAX_RELEASE_AGE_MONTHS:
        update_status = "partial"
        update_observed = f"{version_text} was released about {age} months ago."
    else:
        update_status = "compliant"
        update_observed = f"{version_text} was released within the last {MAX_RELEASE_AGE_MONTHS} months."
    set_check(
        checks_by_id,
        "update_hygiene",
        update_status,
        "low",
        update_observed,
        "Read the release date from the date-based version reported by openclaw --version.",
        f"The installed OpenClaw release is more than {MAX_RELEASE_AGE_MONTHS} months old or unknown.",
        "Review the release notes and update OpenClaw.",
        "Platform Security",
        due_in(30),
    )

    prompt_policy = signals.get("prompt_policy") or {}
    prompt_ok = isinstance(prompt_policy, dict) and bool(prompt_policy.get("require_confirmation_for_untrusted"))
    set_check(
        checks_by_id,
        "prompt_injection_controls",
        "compliant" if prompt_ok else "partial",
        "high",
        "Untrusted content requires explicit confirmation." if prompt_ok else "Untrusted content confirmation policy not enabled.",
        "Checked ~/.openclaw/security/prompt-policy.json.",
        "Untrusted content sources may trigger privileged actions without explicit confirmation.",
        "Enable prompt-policy.json require_confirmation_for_untrusted.",
        "Security Engineering",
        due_in(14),
    )

    cmd_policy = signals.get("command_policy") or {}
    deny_rules = cmd_policy.get("deny") if isinstance(cmd_policy, dict) else []
    allow_rules = cmd_policy.get("allow") if isinstance(cmd_policy, dict) else []
    cmd_ok = bool((isinstance(deny_rules, list) and deny_rules) or (isinstance(allow_rules, list) and allow_rules))
    set_check(
        checks_by_id,
        "command_policy_enforced",
        "compliant" if cmd_ok else "partial",
        "high",
        "Command policy allow/deny rules configured." if cmd_ok else "Command policy rules not configured.",
        "Checked ~/.openclaw/security/command-policy.json.",
        "Privileged commands are not filtered by policy.",
        "Define deny/allow rules in command-policy.json.",
        "Security Engineering",
        due_in(14),
    )

    env_flags = signals.get("env_flags") or {}
    session_required = isinstance(env_flags, dict) and env_flags.get("OPENCLAW_REQUIRE_SESSION_ID") == "1"
    set_check(
        checks_by_id,
        "session_boundary_enforced",
        "compliant" if session_required else "partial",
        "medium",
        "Task session id enforcement enabled." if session_required else "Task session id enforcement not enabled.",
        "Checked ~/.openclaw/env, which guarded_privileged_exec.py reads, for OPENCLAW_REQUIRE_SESSION_ID.",
        "Approvals may carry across tasks without explicit session scoping.",
        "Set OPENCLAW_REQUIRE_SESSION_ID=1 and provide OPENCLAW_TASK_SESSION_ID per task.",
        "Security Engineering",
        due_in(14),
    )

    mfa_enabled = isinstance(env_flags, dict) and bool(env_flags.get("OPENCLAW_APPROVAL_TOKEN"))
    set_check(
        checks_by_id,
        "multi_factor_approval",
        "compliant" if mfa_enabled else "partial",
        "medium",
        "Approval token required for privileged actions." if mfa_enabled else "Approval token not configured.",
        "Checked ~/.openclaw/env, which guarded_privileged_exec.py reads, for OPENCLAW_APPROVAL_TOKEN.",
        "Privileged approvals rely on single-step confirmation.",
        "Set OPENCLAW_APPROVAL_TOKEN and require entry for approvals.",
        "Security Engineering",
        due_in(14),
    )

    egress_allowlist = signals.get("egress_allowlist") or []
    egress_ok = isinstance(egress_allowlist, list) and len(egress_allowlist) > 0
    set_check(
        checks_by_id,
        "egress_allowlist_configured",
        "compliant" if egress_ok else "partial",
        "medium",
        "Egress allowlist configured." if egress_ok else "Egress allowlist not configured.",
        "Checked ~/.openclaw/security/egress_allowlist.json.",
        "Outbound connections are not constrained by allowlist.",
        "Define allowed outbound destinations.",
        "Network Security",
        due_in(21),
    )

    egress_report = signals.get("egress_report") or {}
    egress_findings = egress_report.get("findings", []) if isinstance(egress_report, dict) else []
    egress_scan_ok = isinstance(egress_report, dict) and egress_report.get("status") == "ok"
    egress_summary = egress_report.get("summary") if isinstance(egress_report, dict) else None
    egress_evaluated = egress_summary.get("evaluated", 0) if isinstance(egress_summary, dict) else 0
    # A failed scan proves nothing, so it can never count as clean.
    egress_clean = egress_ok and egress_scan_ok and len(egress_findings) == 0
    if not egress_scan_ok:
        egress_observed = "Egress scan failed; outbound connections could not be checked."
        egress_gap = "Egress monitor did not complete."
    else:
        egress_observed = (
            f"Unapproved egress findings: {len(egress_findings)} "
            f"({egress_evaluated} outbound OpenClaw connection(s) evaluated)"
        )
        egress_gap = (
            "Unapproved outbound connections detected." if egress_ok else "Allowlist missing; cannot validate egress."
        )
    set_check(
        checks_by_id,
        "egress_connections_approved",
        "compliant" if egress_clean else "partial",
        "medium",
        egress_observed,
        "egress_monitor.py evaluated OpenClaw's outbound connections against the allowlist.",
        egress_gap,
        "Approve or block outbound destinations.",
        "Network Security",
        due_in(21),
    )

    assessment["checks"] = sorted(checks_by_id.values(), key=lambda c: str(c.get("check_id", "")))
    assessment.setdefault("metadata", {})
    assessment["metadata"]["generated_at_utc"] = utc_now()
    return assessment


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate live compliance assessment from current machine state")
    p.add_argument("--assessment-file", required=True, help="Path to assessment JSON to update")
    p.add_argument(
        "--port-monitor-script",
        default=str(Path(__file__).resolve().parent / "port_monitor.py"),
        help="Path to port monitor script",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    assessment_path = Path(args.assessment_file)
    assessment = load_json(assessment_path)
    signals = collect_runtime_signals(Path(args.port_monitor_script))
    updated = build_assessment(assessment, signals)
    write_json(assessment_path, updated)
    print(
        json.dumps(
            {
                "status": "ok",
                "assessment_file": str(assessment_path),
                "generated_at_utc": updated["metadata"]["generated_at_utc"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
