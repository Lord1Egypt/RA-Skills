#!/usr/bin/env python3
"""Submit and query BytePlus MediaKit video-highlights-llm tasks."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from uuid import uuid4


DEFAULT_ENDPOINT = "https://mediakit.ap-southeast-1.bytepluses.com"
MEDIA_URL_PREFIXES = ("http://", "https://")
SUPPORTED_PRESETS = ("football",)
MAX_TARGET_DURATIONS = 5


def _load_json(value: str, field_name: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON for {field_name}: {exc}") from exc


def _read_text(value: str | None, file_value: str | None, field_name: str) -> str | None:
    if value and file_value:
        raise SystemExit(f"Use either --{field_name.replace('_', '-')} or --{field_name.replace('_', '-')}-file, not both")
    if file_value:
        return Path(file_value).read_text(encoding="utf-8")
    return value


def _config() -> dict[str, Any]:
    config_path = os.environ.get("BYTEPLUS_MEDIAKIT_CONFIG") or os.environ.get("MEDIAKIT_CONFIG") or os.path.expanduser("~/.mediakit/config.json")
    try:
        return json.loads(Path(config_path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _first_config_value(config: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = config.get(key)
        if value:
            return value
    return None


def _env_value(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _parse_header_pair(raw: str) -> tuple[str, str]:
    key, sep, value = raw.partition(":")
    if not sep:
        raise SystemExit(f"Invalid header '{raw}'. Use the form 'Header-Name: value'.")
    key = key.strip()
    if not key:
        raise SystemExit(f"Invalid header '{raw}'. Header name must not be empty.")
    return key, value.strip()


def _custom_headers(args: argparse.Namespace) -> dict[str, str]:
    """Collect user-supplied headers from --header flags and BYTEPLUS_MEDIAKIT_HEADERS.

    Users who need an internal environment (for example PPE) configure the required
    headers such as ``x-use-ppe`` and ``x-tt-env`` themselves. Nothing is injected by
    default; the production endpoint is used with no extra headers.
    """
    headers: dict[str, str] = {}
    env_headers = _env_value("BYTEPLUS_MEDIAKIT_HEADERS", "MEDIAKIT_HEADERS")
    if env_headers:
        parsed = _load_json(env_headers, "BYTEPLUS_MEDIAKIT_HEADERS")
        if not isinstance(parsed, dict):
            raise SystemExit("BYTEPLUS_MEDIAKIT_HEADERS must be a JSON object of header name/value pairs.")
        for key, value in parsed.items():
            headers[str(key)] = str(value)
    for raw in getattr(args, "header", None) or []:
        key, value = _parse_header_pair(raw)
        headers[key] = value
    return headers


def _api_key(args: argparse.Namespace) -> str:
    key = _optional_api_key(args)
    if not key:
        raise SystemExit(_missing_api_key_message())
    return key


def _optional_api_key(args: argparse.Namespace) -> str | None:
    config = _config()
    return (
        args.api_key
        or _env_value("BYTEPLUS_MEDIAKIT_API_KEY", "MEDIAKIT_API_KEY")
        or _first_config_value(config, "api_key", "apiKey", "token", "access_token")
    )


def _missing_api_key_message() -> str:
    return (
        "Missing MediaKit API key. Configure it outside the chat before submitting/querying: "
        "set BYTEPLUS_MEDIAKIT_API_KEY, pass --api-key for one-off local use, or configure "
        "~/.mediakit/config.json. Legacy MEDIAKIT_API_KEY is still accepted as a fallback. "
        "Do not paste the raw key into the conversation."
    )


def _headers(args: argparse.Namespace) -> dict[str, str]:
    config = _config()
    headers = {
        "Authorization": f"Bearer {_api_key(args)}",
        "Content-Type": "application/json",
        "x-surface": "cli/skill",
        "x-runtime": _env_value("BYTEPLUS_MEDIAKIT_RUNTIME", "MEDIAKIT_RUNTIME") or _first_config_value(config, "runtime") or "codex",
    }
    # Default is the production environment: no environment-specific headers are added.
    # To target an internal environment, set BYTEPLUS_MEDIAKIT_TT_ENV and/or
    # BYTEPLUS_MEDIAKIT_USE_PPE (or pass equivalents via --header /
    # BYTEPLUS_MEDIAKIT_HEADERS). Nothing is injected unless the caller sets it.
    tt_env = _env_value("BYTEPLUS_MEDIAKIT_TT_ENV", "MEDIAKIT_TT_ENV")
    if tt_env:
        headers["x-tt-env"] = tt_env
    use_ppe = _env_value("BYTEPLUS_MEDIAKIT_USE_PPE", "MEDIAKIT_USE_PPE")
    if use_ppe:
        headers["x-use-ppe"] = str(use_ppe)
    # Custom headers take precedence over the dedicated environment variables above.
    headers.update(_custom_headers(args))
    return headers


def _request(args: argparse.Namespace, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    config = _config()
    endpoint = (args.endpoint or _env_value("BYTEPLUS_MEDIAKIT_ENDPOINT", "MEDIAKIT_ENDPOINT") or _first_config_value(config, "endpoint", "base_url", "baseUrl") or DEFAULT_ENDPOINT).rstrip("/")
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(f"{endpoint}{path}", data=data, headers=_headers(args), method=method)
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"error": body}
        guidance = None
        if exc.code in {401, 403}:
            guidance = "Authentication or permission failed. Verify the MediaKit API key and endpoint. If you are targeting an internal environment, confirm your custom headers (for example x-use-ppe / x-tt-env) are correct. If the key is missing or expired, obtain/refresh it from the MediaKit or BytePlus console and configure it outside the chat."
        raise SystemExit(json.dumps({"ok": False, "status": exc.code, "response": parsed, "guidance": guidance}, ensure_ascii=False, indent=2))
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc}") from exc
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"raw": body}


def _validate_media_urls(value: Any, field_name: str, *, min_items: int = 0) -> list[str]:
    if not isinstance(value, list):
        raise SystemExit(f"{field_name} must be a JSON array")
    if len(value) < min_items:
        raise SystemExit(f"{field_name} must contain at least {min_items} item(s)")
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.startswith(MEDIA_URL_PREFIXES):
            raise SystemExit(
                f"{field_name}[{index}] must be a URL starting with one of: "
                f"{', '.join(prefix[:-3] for prefix in MEDIA_URL_PREFIXES)}"
            )
    return value


def _normalize_duration(value: Any) -> Any:
    if isinstance(value, bool):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _validate_target_duration(value: Any) -> list[Any]:
    """Validate target_duration as a list of output durations in seconds.

    target_duration is an array: even a single output must be passed as a list,
    for example [60]. At most 5 items, each a number >= 1, with no duplicates.
    Each item must also be smaller than the combined input duration, but that is
    enforced server-side and not checked here.
    """
    if not isinstance(value, list):
        raise SystemExit("target_duration must be a JSON array of seconds, for example [60] or [60, 90]")
    if not value:
        raise SystemExit("target_duration must contain at least 1 item")
    if len(value) > MAX_TARGET_DURATIONS:
        raise SystemExit(f"target_duration must contain at most {MAX_TARGET_DURATIONS} items")
    normalized: list[Any] = []
    seen: set[Any] = set()
    for index, item in enumerate(value):
        if not isinstance(item, (int, float)) or isinstance(item, bool) or item < 1:
            raise SystemExit(f"target_duration[{index}] must be a number >= 1")
        item = _normalize_duration(item)
        if item in seen:
            raise SystemExit("target_duration items must not be duplicated")
        seen.add(item)
        normalized.append(item)
    return normalized


def _validate_submit_payload(payload: dict[str, Any]) -> None:
    _validate_media_urls(payload.get("video_urls"), "video_urls", min_items=1)
    payload["target_duration"] = _validate_target_duration(payload.get("target_duration"))
    preset = payload.get("preset")
    if preset is not None and preset not in SUPPORTED_PRESETS:
        raise SystemExit(
            f"preset must be one of: {', '.join(SUPPORTED_PRESETS)}. Got {preset!r}."
        )
    for unsupported in ("story_prompt", "background_music_urls"):
        if unsupported in payload:
            raise SystemExit(f"{unsupported} is not supported by this skill; remove it from the request.")
    client_token = payload.get("client_token")
    if client_token is not None and (not isinstance(client_token, str) or len(client_token) > 64):
        raise SystemExit("client_token must be a string no longer than 64 characters")


def _build_submit_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.request_json:
        payload = _load_json(Path(args.request_json).read_text(encoding="utf-8"), "request_json")
    else:
        if not args.video_urls:
            raise SystemExit("Missing --video-urls. Pass a JSON array of video URLs, for example '[\"https://example.com/match.mp4\"]', or use --request-json.")
        video_urls = _load_json(args.video_urls, "video_urls")
        _validate_media_urls(video_urls, "video_urls", min_items=1)

        if args.target_duration is not None:
            durations = _load_json(args.target_duration, "target_duration")
        else:
            durations = [60]

        payload = {
            "video_urls": video_urls,
            "target_duration": durations,
            "client_token": args.client_token or f"vh-{uuid4().hex[:20]}",
        }

    scoring_prompt = _read_text(args.scoring_prompt, args.scoring_prompt_file, "scoring_prompt")
    analysis_prompt = _read_text(args.analysis_prompt, args.analysis_prompt_file, "analysis_prompt")
    if args.preset:
        payload["preset"] = args.preset
    if scoring_prompt:
        payload["scoring_prompt"] = scoring_prompt
    if analysis_prompt:
        payload["analysis_prompt"] = analysis_prompt
    if not any(payload.get(key) for key in ("preset", "scoring_prompt")):
        payload["preset"] = "football"

    if args.callback_url:
        payload["callback_url"] = args.callback_url
    if args.callback_args:
        payload["callback_args"] = args.callback_args
    _validate_submit_payload(payload)
    return payload


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def submit(args: argparse.Namespace) -> int:
    payload = _build_submit_payload(args)
    if args.dry_run:
        _print_json(payload)
        return 0
    _print_json(_request(args, "POST", "/api/v1/tools/video-highlights-llm", payload))
    return 0


def query(args: argparse.Namespace) -> dict[str, Any]:
    return _request(args, "GET", f"/api/v1/tasks/{args.task_id}")


def query_command(args: argparse.Namespace) -> int:
    _print_json(query(args))
    return 0


def _api_key_source(args: argparse.Namespace, config: dict[str, Any]) -> str | None:
    if args.api_key:
        return "arg"
    if os.environ.get("BYTEPLUS_MEDIAKIT_API_KEY"):
        return "BYTEPLUS_MEDIAKIT_API_KEY"
    if os.environ.get("MEDIAKIT_API_KEY"):
        return "MEDIAKIT_API_KEY"
    if _first_config_value(config, "api_key", "apiKey", "token", "access_token"):
        return "config"
    return None


def doctor(args: argparse.Namespace) -> int:
    config = _config()
    probe_args = argparse.Namespace(**vars(args))
    probe_args.api_key = _optional_api_key(args) or "probe-key"
    headers = _headers(probe_args)
    endpoint = args.endpoint or _env_value("BYTEPLUS_MEDIAKIT_ENDPOINT", "MEDIAKIT_ENDPOINT") or _first_config_value(config, "endpoint", "base_url", "baseUrl") or DEFAULT_ENDPOINT
    api_key_present = bool(_optional_api_key(args))
    result = {
        "ok": api_key_present,
        "api_key": {
            "present": api_key_present,
            "source": _api_key_source(args, config),
        },
        "endpoint": endpoint,
        "environment": "prod",
        "headers": {key: value for key, value in headers.items() if key != "Authorization"},
    }
    if not result["ok"]:
        result["guidance"] = _missing_api_key_message()
    _print_json(result)
    return 0 if result["ok"] else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Submit/query video-highlights-llm tasks.")
    root.add_argument("--api-key", help="API key. Defaults to BYTEPLUS_MEDIAKIT_API_KEY, then legacy MEDIAKIT_API_KEY.")
    root.add_argument("--endpoint", help=f"API endpoint. Defaults to the production endpoint {DEFAULT_ENDPOINT}.")
    root.add_argument(
        "--header",
        action="append",
        metavar="NAME: VALUE",
        help=(
            "Custom request header in 'Name: value' form. Repeat for multiple headers. "
            "Use this (or BYTEPLUS_MEDIAKIT_HEADERS) to override any header. "
            "To target an internal environment, prefer the dedicated environment "
            "variables BYTEPLUS_MEDIAKIT_TT_ENV (sets x-tt-env) and "
            "BYTEPLUS_MEDIAKIT_USE_PPE (sets x-use-ppe)."
        ),
    )
    root.add_argument("--timeout", type=float, default=60.0)

    sub = root.add_subparsers(dest="command", required=True)

    doctor_parser = sub.add_parser("doctor", help="Check credential/config/header readiness without printing secrets.")
    doctor_parser.set_defaults(func=doctor)

    submit_parser = sub.add_parser("submit", help="Submit a highlight generation task.")
    submit_parser.add_argument("--request-json", help="Path to a full JSON payload file.")
    submit_parser.add_argument("--video-urls", help="video_urls: JSON array of input video URLs, for example '[\"https://example.com/match.mp4\"]'. Must contain at least one item.")
    submit_parser.add_argument("--target-duration", help="target_duration: JSON array of output durations in seconds, for example '[60]' or '[60, 90]'. Up to 5 unique values, each >= 1. Defaults to [60].")
    submit_parser.add_argument("--preset", help="Scene preset. Only 'football' is supported.")
    submit_parser.add_argument("--scoring-prompt")
    submit_parser.add_argument("--scoring-prompt-file")
    submit_parser.add_argument("--analysis-prompt")
    submit_parser.add_argument("--analysis-prompt-file")
    submit_parser.add_argument("--callback-url")
    submit_parser.add_argument("--callback-args")
    submit_parser.add_argument("--client-token")
    submit_parser.add_argument("--dry-run", action="store_true")
    submit_parser.set_defaults(func=submit)

    query_parser = sub.add_parser("query", help="Query a task by task_id.")
    query_parser.add_argument("--task-id", required=True)
    query_parser.set_defaults(func=query_command)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
