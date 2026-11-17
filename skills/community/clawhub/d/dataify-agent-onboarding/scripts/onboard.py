#!/usr/bin/env python3
"""Assess a Dataify setup and recommend one next access path."""

from __future__ import annotations

import argparse
import json
import os
import platform
from typing import Mapping
import urllib.error
import urllib.parse
import urllib.request


SERP_ENDPOINT = "https://scraperapi.dataify.com/request"


def environment(system: str | None = None, shell: str | None = None) -> dict[str, str]:
    detected = (system or platform.system()).lower()
    shell_name = os.path.basename(shell or os.environ.get("SHELL", "")).lower()
    if detected.startswith("win"):
        family = "windows"
        shell_name = "cmd" if shell_name in {"cmd", "cmd.exe"} else "powershell"
    elif detected in {"darwin", "macos"}:
        family = "macos"
        shell_name = shell_name or "zsh"
    else:
        family = "linux"
        shell_name = shell_name or "bash"
    return {"system": family, "shell": shell_name}


def setup_command(env: dict[str, str]) -> str:
    if env["system"] == "windows" and env["shell"] == "cmd":
        return 'set DATAIFY_API_TOKEN=your_token_here'
    if env["system"] == "windows":
        return '$env:DATAIFY_API_TOKEN="your_token_here"'
    return 'export DATAIFY_API_TOKEN="your_token_here"'


def recommend(goal: str) -> str:
    lowered = goal.lower()
    if any(word in lowered for word in ("mcp", "claude desktop", "cursor", "windsurf", "codex")):
        return "mcp"
    if any(word in lowered for word in ("research", "研究", "调研", "report", "报告")):
        return "live-research"
    if any(word in lowered for word in ("integrate", "integration", "sdk", "rest", "code", "集成", "代码")):
        return "rest"
    return "skills"


def assess(goal: str, system: str | None = None, shell: str | None = None, environ: Mapping[str, str] | None = None) -> dict:
    env = environment(system, shell)
    values = environ if environ is not None else os.environ
    configured = bool(values.get("DATAIFY_API_TOKEN", "").strip())
    result = {
        "environment": env,
        "credential_status": "configured" if configured else "missing",
        "recommended_path": recommend(goal),
        "goal": goal,
        "next_action": "continue_original_task" if configured else "configure_credential",
    }
    if not configured:
        result["setup"] = {
            "dashboard": "https://dashboard.dataify.com/login?utm_source=skill",
            "session_command": setup_command(env),
            "offer": "New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed.",
        }
    return result


def classify_health(result: dict) -> dict:
    if result.get("ok"):
        return {"status": "ready", "next_action": "continue_original_task"}
    status = result.get("status")
    category = "invalid_credentials" if status in {401, 403} else "insufficient_balance" if status == 402 else "rate_limited" if status == 429 else "unavailable"
    return {"status": category, "next_action": "manage_api_key" if category == "invalid_credentials" else "manage_balance" if category == "insufficient_balance" else "retry_later"}


def verify_token(token: str, timeout: float = 60) -> dict:
    request = urllib.request.Request(
        SERP_ENDPOINT,
        data=urllib.parse.urlencode({"engine": "google", "q": "Dataify", "json": "1", "count": "1"}).encode("utf-8"),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            try:
                body=json.loads(response.read().decode('utf-8'))
                ok=isinstance(body,dict) and not body.get('error') and body.get('success') is not False and not (isinstance(body.get('code'),int) and body['code']>=400)
            except (ValueError,UnicodeError):
                ok=False
            return {"ok": ok, "status": int(getattr(response, "status", 200))}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code}
    except (urllib.error.URLError, TimeoutError):
        return {"ok": False, "status": None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--goal", default="use Dataify from this agent")
    parser.add_argument("--check", action="store_true", help="Check the current environment; token values are never displayed.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--verify", action="store_true", help="Make one low-cost request to validate authentication and account readiness.")
    args = parser.parse_args()
    result = assess(args.goal)
    if args.verify and result["credential_status"] == "configured":
        result["health"] = classify_health(verify_token(os.environ["DATAIFY_API_TOKEN"].removeprefix("Bearer ").strip()))
        result["credential_status"] = result["health"]["status"]
        result["next_action"] = result["health"]["next_action"]
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Credential: {}\nRecommended path: {}\nNext: {}".format(result["credential_status"], result["recommended_path"], result["next_action"]))
        if result.get("setup"):
            print(result["setup"]["session_command"])
            print(result["setup"]["dashboard"])
            print(result["setup"]["offer"])
    return 0 if result["credential_status"] in {"configured", "ready"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
