#!/usr/bin/env python3
"""Wait for a Dataify scraper task and print its final JSON result."""

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "https://scraperapi.dataify.com"
STATUS_ENDPOINT = BASE_URL + "/task_status"
DOWNLOAD_ENDPOINT = BASE_URL + "/download"
PROCESSING_STATUS = "处理中"
SUCCESS_STATUS = "成功"
FAILURE_STATUS = "失败"
DEFAULT_INTERVALS = (1, 2, 3, 5, 8, 10, 15)
DEFAULT_WAIT_TIMEOUT = 600
DEFAULT_MAX_INTERVAL = 15
TASK_REGISTRATION_GRACE = 30
LOGIN_URL = "https://dashboard.dataify.com/login?utm_source=skill"
ACCOUNT_URL = "https://dashboard.dataify.com?utm_source=skill"


def configure_utf8_output():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")


def request_json(endpoint, params, api_key, timeout):
    url = endpoint + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            text = content.decode(charset, errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        normalized = detail.lower()
        if "credit" in normalized or "balance" in normalized or "余额" in detail or "积分" in detail:
            raise RuntimeError(
                "Dataify account has insufficient credits. Review balance or recharge at {}.".format(ACCOUNT_URL)
            )
        if exc.code in (401, 403):
            raise RuntimeError(
                "DATAIFY_API_TOKEN was rejected. Review or rotate the API key at {}; a new registration is not required.".format(
                    ACCOUNT_URL
                )
            )
        raise RuntimeError(detail or "HTTP {}".format(exc.code))
    except urllib.error.URLError as exc:
        raise RuntimeError("Request failed: {}".format(exc.reason))

    if api_key:
        text = text.replace(api_key, "<redacted>")
    try:
        return json.loads(text)
    except ValueError:
        raise RuntimeError("Dataify returned a non-JSON response")


def extract_status(payload):
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        message = data if data is not None else payload
        raise RuntimeError("Unable to read task status: {}".format(message))
    status = data.get("status")
    if not status:
        raise RuntimeError("Task status is missing from the response")
    return status, data


def is_task_registration_delay(payload):
    if not isinstance(payload, dict):
        return False
    detail = payload.get("data")
    if not isinstance(detail, str):
        return False
    normalized = detail.strip().lower().replace("-", "_").replace(" ", "_")
    return "task_id" in normalized and "error" in normalized


def sleep_interval(attempt, max_interval):
    base = DEFAULT_INTERVALS[min(attempt, len(DEFAULT_INTERVALS) - 1)]
    base = min(float(base), max_interval)
    return max(0.1, base * random.uniform(0.9, 1.1))


def resume_command(task_id, timeout):
    script_path = os.path.abspath(__file__)
    return 'python3 "{}" --task-id "{}" --timeout {}'.format(script_path, task_id, int(timeout))


def wait_for_task(task_id, api_key, wait_timeout, request_timeout, max_interval, progress):
    started = time.monotonic()
    attempt = 0
    while True:
        payload = request_json(
            STATUS_ENDPOINT,
            {"api_key": api_key, "task_id": task_id},
            api_key,
            request_timeout,
        )
        try:
            status, data = extract_status(payload)
        except RuntimeError:
            elapsed = time.monotonic() - started
            if not is_task_registration_delay(payload) or elapsed >= min(wait_timeout, TASK_REGISTRATION_GRACE):
                raise
            if progress:
                print(
                    json.dumps(
                        {"task_id": task_id, "status": "registering", "elapsed_seconds": round(elapsed, 1)},
                        ensure_ascii=False,
                    ),
                    file=sys.stderr,
                )
            delay = min(sleep_interval(attempt, max_interval), max(0.1, wait_timeout - elapsed))
            time.sleep(delay)
            attempt += 1
            continue

        if status == SUCCESS_STATUS:
            return request_json(
                DOWNLOAD_ENDPOINT,
                {"api_key": api_key, "task_id": task_id, "type": "json"},
                api_key,
                request_timeout,
            )
        if status == FAILURE_STATUS:
            detail = data.get("message") or data.get("error") or data
            raise RuntimeError("Dataify task failed: {}".format(detail))
        if status != PROCESSING_STATUS:
            raise RuntimeError("Unknown Dataify task status: {}".format(status))

        elapsed = time.monotonic() - started
        if elapsed >= wait_timeout:
            raise TimeoutError(
                "Task {} is still processing after {:.0f}s. Resume with the same task ID; do not resubmit it.".format(
                    task_id, elapsed
                )
            )
        if progress:
            print(
                json.dumps(
                    {"task_id": task_id, "status": "running", "elapsed_seconds": round(elapsed, 1)},
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
        delay = min(sleep_interval(attempt, max_interval), max(0.1, wait_timeout - elapsed))
        time.sleep(delay)
        attempt += 1


def main():
    configure_utf8_output()
    parser = argparse.ArgumentParser(
        description="Wait for a Dataify scraper task, then download and print its final JSON result."
    )
    parser.add_argument("--task-id", required=True, help="Task ID returned by a Dataify scraper submission.")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_WAIT_TIMEOUT,
        help="Maximum total wait in seconds (default: 600).",
    )
    parser.add_argument("--request-timeout", type=float, default=60, help="Timeout per HTTP request (default: 60).")
    parser.add_argument(
        "--max-interval",
        type=float,
        default=DEFAULT_MAX_INTERVAL,
        help="Maximum polling interval (default: 15).",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress records on stderr.")
    parser.add_argument("--dry-run", action="store_true", help="Print the redacted status request without calling it.")
    args = parser.parse_args()

    task_id = str(args.task_id).strip()
    if not task_id:
        print("task-id cannot be empty", file=sys.stderr)
        return 2
    if args.timeout <= 0 or args.request_timeout <= 0 or args.max_interval <= 0:
        print("timeout and interval values must be greater than zero", file=sys.stderr)
        return 2

    if args.dry_run:
        print(json.dumps({
            "method": "GET",
            "status_url": STATUS_ENDPOINT + "?" + urllib.parse.urlencode({"api_key": "<redacted>", "task_id": task_id}),
            "on_success": "download JSON result",
            "resubmit": False,
        }, ensure_ascii=False, indent=2))
        return 0

    api_key = os.environ.get("DATAIFY_API_TOKEN", "").strip()
    if not api_key:
        print(
            "DATAIFY_API_TOKEN is not set. Log in or register at {} to obtain an API key. New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed.".format(LOGIN_URL),
            file=sys.stderr,
        )
        return 2

    try:
        result = wait_for_task(
            task_id, api_key, args.timeout, args.request_timeout, args.max_interval, not args.quiet
        )
        print(json.dumps({
            "ok": True,
            "task_id": task_id,
            "status": "succeeded",
            "data": result,
        }, ensure_ascii=False, indent=2))
        return 0
    except KeyboardInterrupt:
        print(
            "Monitoring interrupted. Do not resubmit the task.\nResume: {}".format(
                resume_command(task_id, args.timeout)
            ),
            file=sys.stderr,
        )
        return 130
    except TimeoutError as exc:
        print(
            "{}\nResume: {}".format(str(exc), resume_command(task_id, args.timeout)),
            file=sys.stderr,
        )
        return 3
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
