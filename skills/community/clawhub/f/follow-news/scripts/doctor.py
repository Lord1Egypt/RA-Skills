#!/usr/bin/env python3
"""Project-level preflight diagnostics for follow-news."""

from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


SCRIPTS_DIR = Path(__file__).resolve().parent
OPENCLI_DEFAULT_MIN_VERSION = "1.7.22"


def _load_script_module(module_name: str, file_name: str):
    """Load a sibling script module with hyphenated filename."""
    path = SCRIPTS_DIR / file_name
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module '{module_name}' from {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


_fetch_twitter = _load_script_module("doctor_fetch_twitter", "fetch-twitter.py")
_fetch_web = _load_script_module("doctor_fetch_web", "fetch-web.py")


def setup_logging(verbose: bool) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger(__name__)


def _run_opencli_command(args: List[str], timeout: int) -> subprocess.CompletedProcess:
    """Run an OpenCLI command and return a CompletedProcess object."""
    command = _fetch_twitter.resolve_opencli_bin()
    try:
        return subprocess.run(
            [command] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=os.environ,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=[command] + args,
            returncode=75,
            stdout="",
            stderr=f"OpenCLI command timed out: {exc}",
        )
    except Exception as exc:  # pragma: no cover - defensive
        return subprocess.CompletedProcess(
            args=[command] + args,
            returncode=1,
            stdout="",
            stderr=str(exc),
        )


def _classify_opencli_failure(returncode: int, stderr: str, stdout: str = "") -> str:
    return _fetch_twitter._classify_opencli_failure(returncode, stderr or stdout)


def _diagnostic(
    name: str,
    status: str,
    message: str,
    code: str = "",
    details: Optional[Dict[str, Any]] = None,
    action: str = "",
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "name": name,
        "status": status,
        "message": message,
    }
    if code:
        payload["code"] = code
    if details is not None:
        payload["details"] = details
    if action:
        payload["action"] = action
    return payload


def _extract_snippet(text: str, limit: int = 140) -> str:
    value = (text or "").strip()
    if not value:
        return ""
    return value if len(value) <= limit else f"{value[:limit - 3]}..."


def _parse_opencli_version(value: str) -> Optional[List[int]]:
    """Extract a semantic version tuple from an OpenCLI version string."""
    match = re.search(r"\bv?(\d+)\.(\d+)(?:\.(\d+))?\b", value or "")
    if not match:
        return None
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3) or 0)
    return [major, minor, patch]


def _min_opencli_version() -> List[int]:
    raw_value = os.getenv("OPENCLI_MIN_VERSION", OPENCLI_DEFAULT_MIN_VERSION).strip()
    parsed = _parse_opencli_version(raw_value)
    if parsed:
        return parsed
    logging.warning("Invalid OPENCLI_MIN_VERSION=%r; using default %s", raw_value, OPENCLI_DEFAULT_MIN_VERSION)
    return _parse_opencli_version(OPENCLI_DEFAULT_MIN_VERSION) or [0, 0, 0]


def _get_opencli_version() -> Optional[str]:
    """Probe OpenCLI version from common CLI flags."""
    for args in (["--version"], ["version"], ["-v"], ["-V"]):
        result = _run_opencli_command(args, timeout=10)
        if result.returncode != 0:
            continue
        version_text = f"{result.stdout}\n{result.stderr}".strip()
        parsed = _parse_opencli_version(version_text)
        if parsed is None:
            continue
        return ".".join(str(item) for item in parsed)
    return None


def _version_to_str(version: List[int]) -> str:
    return ".".join(map(str, version))


def _check_opencli_version() -> Optional[Dict[str, Any]]:
    """Return a warning diagnostic if local OpenCLI version is too old or unknown."""
    version = _get_opencli_version()
    minimum = _min_opencli_version()

    if version is None:
        return {
            "status": "warning",
            "code": "opencli_version_unknown",
            "message": "Could not determine OpenCLI version.",
            "details": {
                "minimum": _version_to_str(minimum),
            },
            "action": f"Run `opencli --version` and ensure it is >= {_version_to_str(minimum)}.",
        }

    current = _parse_opencli_version(version)
    if current is None:
        return {
            "status": "warning",
            "code": "opencli_version_unknown",
            "message": "Could not parse OpenCLI version output.",
            "details": {
                "minimum": _version_to_str(minimum),
                "version": version,
            },
            "action": "Run `opencli --version` and ensure it is a semantic version.",
        }

    if current < minimum:
        return {
            "status": "warning",
            "code": "opencli_version_too_old",
            "message": "OpenCLI version is older than required.",
            "details": {
                "current": version,
                "minimum": _version_to_str(minimum),
            },
            "action": "Upgrade OpenCLI and retry.",
        }

    return {
        "status": "ok",
        "version": version,
    }


def check_opencli_availability() -> Dict[str, Any]:
    """Verify OpenCLI binary exists and exposes the Twitter backend."""
    try:
        binary = _fetch_twitter.resolve_opencli_bin()
    except _fetch_twitter.OpenCliBackendError as exc:
        return _diagnostic(
            name="opencli",
            status="warning",
            code=exc.code,
            message="OpenCLI binary is not discoverable.",
            details={"hint": "Set OPENCLI_BIN or install opencli on PATH"},
            action=(
                "OpenCLI is not installed. Install it (or set OPENCLI_BIN), "
                "or configure a Twitter API fallback yourself using "
                "GETX_API_KEY, TWITTERAPI_IO_KEY, or X_BEARER_TOKEN."
            ),
        )

    version_check = _check_opencli_version()
    if version_check is not None and version_check.get("status") != "ok":
        return _diagnostic(
            name="opencli",
            status="warning",
            code=version_check.get("code", "opencli_version_unknown"),
            message=version_check.get("message", "OpenCLI version check failed."),
            details={
                "binary": binary,
                "minimum_version": _min_opencli_version() if version_check else None,
                **(version_check.get("details") or {}),
            },
            action=version_check.get("action", "Upgrade OpenCLI before continuing."),
        )

    list_result = _run_opencli_command(["list", "-f", "json"], timeout=30)
    if list_result.returncode != 0:
        code = _classify_opencli_failure(
            list_result.returncode,
            list_result.stderr,
            list_result.stdout,
        )
        return _diagnostic(
            name="opencli",
            status="warning",
            code=code,
            message="OpenCLI binary exists but command inspection failed.",
            details={
                "binary": binary,
                "stderr": _extract_snippet(list_result.stderr, 180),
                "returncode": list_result.returncode,
            },
            action="Run `opencli list -f json` manually and check OpenCLI installation.",
        )

    payload = None
    try:
        payload = json.loads(list_result.stdout or "null")
    except json.JSONDecodeError:
        payload = None

    if not _fetch_twitter.opencli_has_twitter_tweets(payload):
        return _diagnostic(
            name="opencli",
            status="warning",
            code="opencli_capability_missing",
            message="OpenCLI is installed but does not expose twitter tweets command.",
            details={
                "binary": binary,
                "raw": _extract_snippet((list_result.stdout or list_result.stderr), 200),
            },
            action="Install a build that contains `twitter tweets` and run `opencli doctor`.",
        )

    return _diagnostic(
        name="opencli",
        status="ok",
        code="opencli_ok",
        message="OpenCLI binary and twitter capability are available.",
        details={"binary": binary},
    )


def _skip_due_to_opencli_unavailable() -> Dict[str, Any]:
    return _diagnostic(
        name="dependency",
        status="warning",
        code="dependency_unavailable",
        message="Skipped this check because OpenCLI is unavailable.",
        action=(
            "OpenCLI is unavailable. Install it (or set OPENCLI_BIN), "
            "or configure a Twitter API fallback yourself using "
            "GETX_API_KEY, TWITTERAPI_IO_KEY, or X_BEARER_TOKEN."
        ),
    )


def check_opencli_browser_bridge(opencli_ok: bool) -> Dict[str, Any]:
    """Verify the OpenCLI browser bridge can list tabs."""
    if not opencli_ok:
        skipped = _skip_due_to_opencli_unavailable()
        skipped["name"] = "opencli_browser_bridge"
        return skipped

    result = _run_opencli_command(["browser", "tab", "list", "-f", "json"], timeout=15)
    if result.returncode != 0:
        code = _classify_opencli_failure(
            result.returncode,
            result.stderr,
            result.stdout,
        )
        return _diagnostic(
            name="opencli_browser_bridge",
            status="warning",
            code=code,
            message="OpenCLI browser bridge is not healthy.",
            details={
                "returncode": result.returncode,
                "stderr": _extract_snippet(result.stderr, 180),
            },
            action="OpenCLI should report an active browser bridge; restart browser/extension and retry.",
        )

    try:
        payload = json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        return _diagnostic(
            name="opencli_browser_bridge",
            status="warning",
            code="opencli_bridge_parse_error",
            message="OpenCLI browser bridge returns non-JSON output.",
            details={"snippet": _extract_snippet(result.stdout, 180)},
            action="Run `opencli browser tab list -f json` manually to inspect bridge output.",
        )

    if isinstance(payload, list):
        open_tabs = len(payload)
    elif isinstance(payload, dict):
        open_tabs = len(payload.get("tabs", []))
    else:
        open_tabs = 0

    return _diagnostic(
        name="opencli_browser_bridge",
        status="ok",
        code="opencli_bridge_ok",
        message="OpenCLI browser bridge can report tabs.",
        details={"open_tabs": open_tabs},
    )


def check_x_login_readiness(opencli_ok: bool) -> Dict[str, Any]:
    """Run opencli doctor and surface X login readiness issues."""
    if not opencli_ok:
        skipped = _skip_due_to_opencli_unavailable()
        skipped["name"] = "opencli_x_login"
        return skipped

    result = _run_opencli_command(["doctor"], timeout=30)
    if result.returncode == 0:
        return _diagnostic(
            name="opencli_x_login",
            status="ok",
            code="opencli_doctor_ok",
            message="OpenCLI doctor passed; X login state is likely ready.",
            details={"doctor_output": _extract_snippet(result.stdout or result.stderr, 220)},
        )

    code = _classify_opencli_failure(result.returncode, result.stderr, result.stdout)
    action = (
        "Run `opencli doctor` and re-authenticate X in the OpenCLI browser context."
        if code == "opencli_auth_required"
        else "Check OpenCLI bridge and re-run doctor."
    )
    return _diagnostic(
        name="opencli_x_login",
        status="warning",
        code=code,
        message="OpenCLI doctor indicates X/browser issues.",
        details={
            "returncode": result.returncode,
            "stderr": _extract_snippet(result.stderr, 180),
            "stdout": _extract_snippet(result.stdout, 180),
        },
        action=action,
    )


def check_brave_readiness() -> Dict[str, Any]:
    """Check Brave Search readiness by resolving keys and probing limits."""
    keys = _fetch_web.get_brave_api_keys()
    if not keys:
        return _diagnostic(
            name="web_brave",
            status="warning",
            code="brave_key_missing",
            message="BRAVE key is not configured.",
            action="Set BRAVE_API_KEYS (preferred) or BRAVE_API_KEY.",
        )

    selected_key, qps, workers = _fetch_web.select_brave_key_and_limits(keys)
    if not selected_key:
        return _diagnostic(
            name="web_brave",
            status="warning",
            code="brave_no_usable_key",
            message="No Brave key can be selected for this run.",
            details={"keys": len(keys)},
            action="Rotate Brave keys or verify quota and network connectivity.",
        )

    return _diagnostic(
        name="web_brave",
        status="ok",
        code="brave_ok",
        message="Brave Search key is ready.",
        details={
            "keys": len(keys),
            "selected_key_prefix": selected_key[:4],
            "max_qps": qps,
            "max_workers": workers,
        },
    )


def check_tavily_readiness() -> Dict[str, Any]:
    """Check Tavily readiness with a lightweight probe."""
    key = _fetch_web.get_tavily_api_key()
    if not key:
        return _diagnostic(
            name="web_tavily",
            status="warning",
            code="tavily_key_missing",
            message="TAVILY key is not configured.",
            action="Set TAVILY_API_KEY.",
        )

    probe = _fetch_web.search_tavily("OpenAI", key, topic="news", max_results=1, days=2)
    if probe.get("status") == "ok":
        return _diagnostic(
            name="web_tavily",
            status="ok",
            code="tavily_ok",
            message="Tavily Search API probe succeeded.",
            details={"result_count": probe.get("total", 0)},
        )

    return _diagnostic(
        name="web_tavily",
        status="warning",
        code="tavily_probe_failed",
        message="Tavily Search probe failed.",
        details={
            "status": probe.get("status"),
            "error": probe.get("error"),
        },
        action="Verify TAVILY_API_KEY and network connectivity.",
    )


def run_doctor() -> Dict[str, Any]:
    """Run all preflight checks and return machine-readable report."""
    checks = [check_opencli_availability()]
    opencli_ok = checks[0]["status"] == "ok"

    checks.append(check_opencli_browser_bridge(opencli_ok))
    checks.append(check_x_login_readiness(opencli_ok))
    checks.append(check_brave_readiness())
    checks.append(check_tavily_readiness())

    if any(check["status"] == "error" for check in checks):
        status = "error"
    elif any(check["status"] == "warning" for check in checks):
        status = "warning"
    else:
        status = "ok"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "checks": checks,
    }


def _render_human(report: Dict[str, Any]) -> str:
    icons = {
        "ok": "[OK]",
        "warning": "[WARN]",
        "error": "[ERR]",
        "skipped": "[SKIP]",
    }

    lines = [
        "Follow-News Doctor Report",
        f"Overall status: {report['status']}",
        "",
    ]
    for check in report["checks"]:
        icon = icons.get(check["status"], "*")
        line = f"{icon} {check['name']}: {check['status']} - {check['message']}"
        if "code" in check:
            line += f" ({check['code']})"
        lines.append(line)
        if "action" in check:
            lines.append(f"  - Action: {check['action']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run follow-news preflight checks.")
    parser.add_argument("--json", action="store_true", help="Print JSON only.")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    setup_logging(args.verbose)
    report = run_doctor()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not args.json:
        print()
        print(_render_human(report))

    if report["status"] in {"error", "warning"}:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
