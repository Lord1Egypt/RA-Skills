#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional


DEFAULT_SERVICE_URL = "http://localhost:8033"
DEFAULT_WAIT_SECONDS = 300
DEFAULT_REPORT_WAIT_SECONDS = 1800
DEFAULT_POLL_INTERVAL = 2.0


def service_url() -> str:
    return os.getenv("FAST_CLAW_SERVICE_URL", DEFAULT_SERVICE_URL).rstrip("/")


def api_key_path() -> Path:
    override = os.getenv("FAST_CLAW_API_KEY_PATH") or os.getenv("FAST_CLAW_TOKEN_PATH")
    if override:
        return Path(override).expanduser()
    default_path = Path.home() / ".fast-claw" / "api-key.json"
    legacy_path = Path.home() / ".fast-claw" / "token.json"
    if not default_path.exists() and legacy_path.exists():
        return legacy_path
    return default_path


def token_path() -> Path:
    return api_key_path()


def read_local_api_key() -> Optional[Dict[str, str]]:
    path = api_key_path()
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "api_key" not in payload and "token" in payload:
        payload["api_key"] = payload["token"]
    return payload


def read_local_token() -> Optional[Dict[str, str]]:
    return read_local_api_key()


def write_local_api_key(api_key: str) -> None:
    path = api_key_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "api_key": api_key,
                "token": api_key,
                "service_url": service_url(),
                "saved_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def write_local_token(token: str) -> None:
    write_local_api_key(token)


def clear_local_api_key() -> None:
    path = api_key_path()
    if path.exists():
        path.unlink()


def clear_local_token() -> None:
    clear_local_api_key()


def mask_api_key(api_key: str) -> str:
    if len(api_key) <= 12:
        return api_key
    return f"{api_key[:6]}...{api_key[-4:]}"


def mask_token(token: str) -> str:
    return mask_api_key(token)


def request_json(
    method: str,
    path: str,
    payload: Optional[Dict[str, object]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, object]:
    headers = {"Accept": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["X-API-Key"] = api_key
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(
        f"{service_url()}{path}",
        data=data,
        headers=headers,
        method=method.upper(),
    )
    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8")
        try:
            detail_obj = json.loads(detail)
            detail = detail_obj.get("detail", detail)
        except json.JSONDecodeError:
            pass
        raise SystemExit(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Could not reach Fast Claw service at {service_url()}: {exc.reason}") from exc


def require_api_key() -> str:
    saved = read_local_api_key()
    if not saved or "api_key" not in saved:
        raise SystemExit(
            "No local API key found. Run `purchase` first or save an existing one with `set-api-key`."
        )
    return str(saved["api_key"])


def require_token() -> str:
    return require_api_key()


def print_json(data: dict[str, object]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def wait_for_completion(session_id: str, wait_seconds: int, poll_interval: float) -> Dict[str, object]:
    deadline = time.time() + wait_seconds
    while True:
        session = request_json("GET", f"/v1/checkout-sessions/{session_id}")
        if session.get("status") == "completed":
            return session
        if time.time() >= deadline:
            raise SystemExit(
                "Checkout is still pending. Re-run `wait --session-id "
                f"{session_id}` after the user finishes the checkout page."
            )
        time.sleep(poll_interval)


def wait_for_report(job_id: str, api_key: str, wait_seconds: int, poll_interval: float) -> Dict[str, object]:
    deadline = time.time() + wait_seconds
    while True:
        job = request_json("GET", f"/v1/report-jobs/{job_id}", api_key=api_key)
        if job.get("status") in {"completed", "failed"}:
            return job
        if time.time() >= deadline:
            raise SystemExit(
                "Report job is still running. Re-run `wait-report --job-id "
                f"{job_id}` to continue polling."
            )
        time.sleep(poll_interval)


def cmd_status(_: argparse.Namespace) -> None:
    saved = read_local_api_key()
    print(f"Service URL: {service_url()}")
    print(f"API key path: {api_key_path()}")
    if not saved:
        print("Local API key: missing")
        return
    api_key = str(saved["api_key"])
    print(f"Local API key: {mask_api_key(api_key)}")
    remote_status = request_json("GET", "/v1/account", api_key=api_key)
    print_json(remote_status)


def cmd_purchase(args: argparse.Namespace) -> None:
    session = request_json(
        "POST",
        "/v1/checkout-sessions",
        {
            "account_name": args.account_name,
            "credits": args.credits,
            "success_url": args.success_url,
        },
    )
    run_checkout_wait(session, args)


def cmd_topup(args: argparse.Namespace) -> None:
    session = request_json(
        "POST",
        "/v1/checkout-sessions",
        {
            "api_key": require_api_key(),
            "credits": args.credits,
            "success_url": args.success_url,
        },
    )
    run_checkout_wait(session, args)


def run_checkout_wait(session: Dict[str, object], args: argparse.Namespace) -> None:
    session_id = str(session["session_id"])
    checkout_url = str(session["checkout_url"])
    print(f"Checkout session: {session_id}")
    print(f"Checkout URL: {checkout_url}")
    if args.open_browser:
        webbrowser.open(checkout_url)
    completed = wait_for_completion(session_id, args.wait_seconds, args.poll_interval)
    api_key = completed.get("api_key") or completed.get("token")
    if api_key:
        write_local_api_key(str(api_key))
        print(f"Saved API key to {api_key_path()}")
    print_json(completed)


def cmd_wait(args: argparse.Namespace) -> None:
    completed = wait_for_completion(args.session_id, args.wait_seconds, args.poll_interval)
    api_key = completed.get("api_key") or completed.get("token")
    if api_key:
        write_local_api_key(str(api_key))
        print(f"Saved API key to {api_key_path()}")
    print_json(completed)


def cmd_invoke(args: argparse.Namespace) -> None:
    response = request_json(
        "POST",
        "/v1/invoke",
        {"prompt": args.prompt},
        api_key=require_api_key(),
    )
    print_json(response)


def cmd_report(args: argparse.Namespace) -> None:
    api_key = require_api_key()
    job = request_json(
        "POST",
        "/v1/report-jobs",
        {"prompt": args.prompt},
        api_key=api_key,
    )
    print(f"Report job: {job['job_id']}")
    print(f"Poll URL: {job['poll_url']}")
    if args.no_wait:
        print_json(job)
        return
    completed = wait_for_report(job["job_id"], api_key, args.wait_seconds, args.poll_interval)
    if completed.get("status") == "failed":
        raise SystemExit(f"Report job failed: {completed.get('error', 'unknown error')}")
    print_json(completed)


def cmd_wait_report(args: argparse.Namespace) -> None:
    completed = wait_for_report(
        args.job_id,
        require_api_key(),
        args.wait_seconds,
        args.poll_interval,
    )
    if completed.get("status") == "failed":
        raise SystemExit(f"Report job failed: {completed.get('error', 'unknown error')}")
    print_json(completed)


def cmd_set_api_key(args: argparse.Namespace) -> None:
    if not args.api_key:
        raise SystemExit("Provide --api-key.")
    write_local_api_key(args.api_key)
    print(f"Saved API key to {api_key_path()}")


def cmd_set_token(args: argparse.Namespace) -> None:
    write_local_api_key(args.token)
    print(f"Saved API key to {api_key_path()}")


def cmd_clear_token(_: argparse.Namespace) -> None:
    clear_local_api_key()
    print(f"Cleared API key file at {api_key_path()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fast Claw demo service client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Inspect the saved API key and remote balance")
    status_parser.set_defaults(func=cmd_status)

    purchase_parser = subparsers.add_parser("purchase", help="Start a purchase for a new account API key")
    purchase_parser.add_argument("--account-name", required=True, help="Account name to create")
    purchase_parser.add_argument("--credits", type=int, default=10, help="Credits to buy")
    purchase_parser.add_argument("--success-url", help="Optional redirect URL after payment")
    purchase_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_WAIT_SECONDS,
        help="How long to poll for checkout completion",
    )
    purchase_parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL,
        help="Polling interval in seconds",
    )
    purchase_parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the checkout page in the default browser",
    )
    purchase_parser.set_defaults(func=cmd_purchase)

    topup_parser = subparsers.add_parser("topup", help="Recharge credits for the saved API key")
    topup_parser.add_argument("--credits", type=int, default=10, help="Credits to add")
    topup_parser.add_argument("--success-url", help="Optional redirect URL after payment")
    topup_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_WAIT_SECONDS,
        help="How long to poll for checkout completion",
    )
    topup_parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL,
        help="Polling interval in seconds",
    )
    topup_parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the checkout page in the default browser",
    )
    topup_parser.set_defaults(func=cmd_topup)

    wait_parser = subparsers.add_parser("wait", help="Wait for an existing checkout session to complete")
    wait_parser.add_argument("--session-id", required=True, help="Checkout session to poll")
    wait_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_WAIT_SECONDS,
        help="How long to poll before giving up",
    )
    wait_parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL,
        help="Polling interval in seconds",
    )
    wait_parser.set_defaults(func=cmd_wait)

    invoke_parser = subparsers.add_parser("invoke", help="Call the authenticated Fast Claw endpoint")
    invoke_parser.add_argument("--prompt", required=True, help="Prompt to send to the service")
    invoke_parser.set_defaults(func=cmd_invoke)

    report_parser = subparsers.add_parser("report", help="Start an async analysis report and poll for completion")
    report_parser.add_argument("--prompt", required=True, help="Prompt to send to the report worker")
    report_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_REPORT_WAIT_SECONDS,
        help="How long to poll for report completion",
    )
    report_parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL,
        help="Polling interval in seconds",
    )
    report_parser.add_argument(
        "--no-wait",
        action="store_true",
        help="Only create the report job and print the job id",
    )
    report_parser.set_defaults(func=cmd_report)

    wait_report_parser = subparsers.add_parser("wait-report", help="Wait for an existing report job to complete")
    wait_report_parser.add_argument("--job-id", required=True, help="Report job to poll")
    wait_report_parser.add_argument(
        "--wait-seconds",
        type=int,
        default=DEFAULT_REPORT_WAIT_SECONDS,
        help="How long to poll before giving up",
    )
    wait_report_parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL,
        help="Polling interval in seconds",
    )
    wait_report_parser.set_defaults(func=cmd_wait_report)

    set_api_key_parser = subparsers.add_parser(
        "set-api-key",
        aliases=["set-token"],
        help="Manually save an API key",
    )
    set_api_key_parser.add_argument("--api-key", dest="api_key", required=False, help="API key to save")
    set_api_key_parser.add_argument("--token", required=False, help="Legacy alias for API key")
    set_api_key_parser.set_defaults(
        func=lambda args: cmd_set_api_key(
            argparse.Namespace(api_key=args.api_key or args.token)
        )
    )

    clear_token_parser = subparsers.add_parser(
        "clear-api-key",
        aliases=["clear-token"],
        help="Delete the saved API key file",
    )
    clear_token_parser.set_defaults(func=cmd_clear_token)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
