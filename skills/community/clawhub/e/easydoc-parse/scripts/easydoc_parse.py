#!/usr/bin/env python3
"""
Submit files to EasyDoc parse API and poll until completion.

Usage examples:
  # China platform
  python3 easydoc_parse.py --platform cn --api-key "$EASYLINK_API_KEY" \
    --mode easydoc-parse-premium --file ./example.pdf --save ./result.json

  # Global platform
  python3 easydoc_parse.py --platform global --api-key "$EASYDOC_API_KEY" \
    --mode lite --file ./demo_document.pdf --save ./result.json
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from urllib import error, request


TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024
TERMINAL_STATES = {"SUCCESS", "ERROR", "FAILED", "COMPLETED", "DONE"}
PENDING_STATES = {"PENDING", "PROCESSING", "RUNNING", "IN_PROGRESS", "QUEUED"}

CN_EXTENSIONS = {
    ".pdf",
    ".dotm",
    ".docm",
    ".doc",
    ".dotx",
    ".docx",
    ".txt",
    ".html",
    ".dot",
    ".xltm",
    ".xlsm",
    ".xlsx",
    ".xls",
    ".xlt",
    ".potm",
    ".pptx",
    ".ppt",
    ".pot",
    ".pps",
    ".tif",
    ".png",
    ".jpg",
    ".bmp",
}

GLOBAL_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx",
    ".doc",
    ".pptx",
    ".ppt",
}

PLATFORM_CONFIGS: Dict[str, Dict[str, Any]] = {
    "cn": {
        "base_url": "https://api.easylink-ai.com",
        "submit_path": "/v1/easydoc/parse",
        "result_path": "/v1/easydoc/parse/{task_id}",
        "file_field": "files",
        "supported_extensions": CN_EXTENSIONS,
        "recommended_modes": ["easydoc-parse-flash", "easydoc-parse-premium"],
        "default_mode": "easydoc-parse-premium",
    },
    "global": {
        "base_url": "https://api.easydoc.sh",
        "submit_path": "/api/v1/parse",
        "result_path": "/api/v1/parse/{task_id}/result",
        "file_field": "file",
        "supported_extensions": GLOBAL_EXTENSIONS,
        "recommended_modes": ["lite"],
        "default_mode": "lite",
    },
}


class ApiError(Exception):
    """Raised when API communication fails."""


def onboarding_hint(platform: str) -> str:
    if platform == "global":
        return (
            "Missing API key for global platform.\n"
            "1) Sign up or log in at https://platform.easydoc.sh\n"
            "2) Create an API key in the platform API key page\n"
            "3) Retry with --api-key or export EASYDOC_API_KEY"
        )
    return (
        "Missing API key for cn platform.\n"
        "1) Sign up or log in at https://platform.easylink-ai.com\n"
        "2) Create an API key in the platform API key page\n"
        "3) Retry with --api-key or export EASYLINK_API_KEY"
    )


def resolve_api_key(cli_api_key: str, platform: str) -> str:
    if cli_api_key.strip():
        return cli_api_key.strip()

    if platform == "global":
        for key in ("EASYDOC_API_KEY", "EASYLINK_API_KEY"):
            value = os.getenv(key, "").strip()
            if value:
                return value
    else:
        for key in ("EASYLINK_API_KEY", "EASYDOC_API_KEY"):
            value = os.getenv(key, "").strip()
            if value:
                return value

    raise ApiError(onboarding_hint(platform))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit EasyDoc parse jobs and poll asynchronous status."
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="API key. If omitted, script reads env var by platform.",
    )
    parser.add_argument(
        "--platform",
        choices=["cn", "global"],
        default="cn",
        help="Target platform. cn=api.easylink-ai.com, global=api.easydoc.sh",
    )
    parser.add_argument(
        "--base-url",
        default="",
        help="Optional base URL override for selected platform.",
    )
    parser.add_argument(
        "--mode",
        default="",
        help="Parse mode. Example: cn=easydoc-parse-premium, global=lite",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Input file path. Repeatable for multi-file upload.",
    )
    parser.add_argument(
        "--task-id",
        default="",
        help="Existing task id. Use with --poll-only to fetch status/result.",
    )
    parser.add_argument(
        "--poll-only",
        action="store_true",
        help="Do not submit new task. Poll existing --task-id only.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=2.0,
        help="Polling interval in seconds. Default: 2.0",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Polling timeout in seconds. Default: 600",
    )
    parser.add_argument(
        "--no-poll",
        action="store_true",
        help="Submit only and print task creation response without polling.",
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional output file path to save final JSON response.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress logs and print JSON only.",
    )
    parser.add_argument(
        "--output-format",
        choices=["normalized", "raw"],
        default="normalized",
        help="Output normalized envelope or raw API payload. Default: normalized",
    )
    parser.add_argument(
        "--query-retries",
        type=int,
        default=3,
        help="Retries for GET polling on transient failures. Default: 3",
    )
    parser.add_argument(
        "--skip-local-checks",
        action="store_true",
        help="Skip local extension and file-size checks before upload.",
    )
    return parser.parse_args()


def ensure_inputs(args: argparse.Namespace) -> None:
    if args.poll_only:
        if not args.task_id:
            raise ApiError("--poll-only requires --task-id.")
        if args.file:
            raise ApiError("--poll-only cannot be combined with --file.")
        return

    if args.task_id and args.file:
        raise ApiError("Provide either --task-id or --file, not both.")
    if not args.task_id and not args.file:
        raise ApiError("At least one --file is required when submitting.")


def read_json_response(resp_bytes: bytes) -> Dict:
    try:
        return json.loads(resp_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ApiError(f"Invalid JSON response: {exc}") from exc


def http_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    body: bytes | None = None,
    timeout: int = 60,
    retries: int = 0,
    retry_backoff: float = 1.0,
) -> Dict:
    req = request.Request(url=url, data=body, method=method.upper(), headers=headers)
    retries = max(0, retries)
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                return read_json_response(resp.read())
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            should_retry = exc.code in TRANSIENT_HTTP_CODES and attempt < retries
            if should_retry:
                time.sleep(retry_backoff * (2**attempt))
                last_exc = exc
                continue
            raise ApiError(f"HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:
            if attempt < retries:
                time.sleep(retry_backoff * (2**attempt))
                last_exc = exc
                continue
            raise ApiError(f"Network error: {exc.reason}") from exc
    raise ApiError(f"Request failed after retries: {last_exc}")


def encode_multipart(
    fields: Iterable[Tuple[str, str]], files: Iterable[Tuple[str, Path]]
) -> Tuple[bytes, str]:
    boundary = f"----easylink-{uuid.uuid4().hex}"
    body = bytearray()

    for key, value in fields:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8")
        )
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    for field_name, file_path in files:
        filename = file_path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            (
                f'Content-Disposition: form-data; name="{field_name}"; '
                f'filename="{filename}"\r\n'
            ).encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(file_path.read_bytes())
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return bytes(body), boundary


def submit_task(
    api_key: str,
    base_url: str,
    submit_path: str,
    file_field: str,
    mode: str,
    file_paths: List[Path],
    timeout: int = 60,
) -> Dict:
    url = f"{base_url.rstrip('/')}{submit_path}"
    payload, boundary = encode_multipart(
        fields=[("mode", mode)],
        files=[(file_field, file_path) for file_path in file_paths],
    )
    headers = {
        "api-key": api_key,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    return http_json("POST", url, headers=headers, body=payload, timeout=timeout)


def query_task(
    api_key: str,
    base_url: str,
    result_path_template: str,
    task_id: str,
    timeout: int = 60,
    retries: int = 0,
) -> Dict:
    path = result_path_template.format(task_id=task_id)
    url = f"{base_url.rstrip('/')}{path}"
    headers = {"api-key": api_key}
    return http_json("GET", url, headers=headers, timeout=timeout, retries=retries)


def _first_str(container: Dict[str, Any], keys: Tuple[str, ...]) -> str:
    for key in keys:
        value = container.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _candidate_dicts(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    data = payload.get("data")
    if isinstance(data, dict):
        candidates.append(data)
    if isinstance(payload, dict):
        candidates.append(payload)
    return candidates


def extract_status(payload: Dict[str, Any]) -> str:
    for container in _candidate_dicts(payload):
        status = _first_str(container, ("status", "state", "task_status"))
        if status:
            return status.upper()
    return ""


def extract_task_id(payload: Dict[str, Any]) -> str:
    for container in _candidate_dicts(payload):
        task_id = _first_str(container, ("task_id", "taskId", "id"))
        if task_id:
            return task_id
    return ""


def extract_results(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    for container in _candidate_dicts(payload):
        for key in ("results", "result", "files"):
            value = container.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
            if isinstance(value, dict):
                nested_files = value.get("files")
                if isinstance(nested_files, list):
                    return [item for item in nested_files if isinstance(item, dict)]
                return [value]
    return []


def save_json(path: str, payload: Dict) -> None:
    out_path = Path(path).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def log(msg: str, quiet: bool) -> None:
    if not quiet:
        print(msg, file=sys.stderr)


def poll_until_terminal(
    api_key: str,
    base_url: str,
    result_path_template: str,
    task_id: str,
    poll_interval: float,
    timeout_seconds: int,
    query_retries: int,
    quiet: bool,
) -> Dict:
    deadline = time.time() + timeout_seconds
    last_status = ""
    while True:
        payload = query_task(
            api_key=api_key,
            base_url=base_url,
            result_path_template=result_path_template,
            task_id=task_id,
            timeout=60,
            retries=query_retries,
        )
        status = extract_status(payload)

        if status != last_status:
            log(f"[status] {status or 'UNKNOWN'}", quiet)
            last_status = status

        if status in TERMINAL_STATES:
            return payload

        if status and status not in PENDING_STATES:
            log("[warn] Unexpected status, continue polling", quiet)

        if time.time() >= deadline:
            raise ApiError(
                f"Polling timeout after {timeout_seconds}s for task_id={task_id}."
            )
        time.sleep(max(0.2, poll_interval))


def validate_files(
    file_paths: List[Path],
    supported_extensions: set[str],
    platform: str,
    skip_local_checks: bool,
) -> None:
    for path in file_paths:
        if not path.exists():
            raise ApiError(f"File not found: {path}")
        if not path.is_file():
            raise ApiError(f"Not a file: {path}")
        if skip_local_checks:
            continue

        ext = path.suffix.lower()
        if ext not in supported_extensions:
            allowed = ", ".join(sorted(supported_extensions))
            raise ApiError(
                f"Unsupported file extension '{ext}' for platform '{platform}': "
                f"{path.name}. Allowed: {allowed}"
            )

        size = path.stat().st_size
        if size > MAX_FILE_SIZE_BYTES:
            raise ApiError(f"File exceeds 100MB limit: {path} ({size} bytes).")


def normalize_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    task_id = extract_task_id(payload)
    status = extract_status(payload)
    files = []

    for item in extract_results(payload):
        file_name = _first_str(item, ("file_name", "filename", "name"))
        markdown = item.get("markdown")
        nodes = item.get("nodes")
        files.append(
            {
                "file_name": file_name,
                "markdown": markdown if isinstance(markdown, str) else None,
                "nodes": nodes if isinstance(nodes, list) else [],
            }
        )

    return {
        "task_id": task_id,
        "status": status,
        "files": files,
        "raw": payload,
    }


def main() -> int:
    args = parse_args()
    try:
        ensure_inputs(args)

        platform_config = PLATFORM_CONFIGS[args.platform]
        api_key = resolve_api_key(args.api_key, args.platform)
        base_url = args.base_url.strip() or platform_config["base_url"]
        submit_path = platform_config["submit_path"]
        result_path_template = platform_config["result_path"]
        file_field = platform_config["file_field"]
        supported_extensions = platform_config["supported_extensions"]
        recommended_modes = platform_config["recommended_modes"]
        default_mode = platform_config["default_mode"]

        file_paths = [Path(path).expanduser().resolve() for path in args.file]
        validate_files(
            file_paths=file_paths,
            supported_extensions=supported_extensions,
            platform=args.platform,
            skip_local_checks=args.skip_local_checks,
        )

        mode = args.mode.strip()
        if file_paths and not args.task_id and not args.poll_only and not mode:
            mode = default_mode
            log(f"[mode] platform={args.platform}, defaulting to '{mode}'", args.quiet)

        if mode and mode not in recommended_modes:
            recommended = ", ".join(recommended_modes)
            log(
                f"[warn] mode '{mode}' is not in recommended set for {args.platform}: "
                f"{recommended}",
                args.quiet,
            )

        if args.poll_only:
            task_id = args.task_id
            result = poll_until_terminal(
                api_key=api_key,
                base_url=base_url,
                result_path_template=result_path_template,
                task_id=task_id,
                poll_interval=args.poll_interval,
                timeout_seconds=args.timeout,
                query_retries=args.query_retries,
                quiet=args.quiet,
            )
        elif args.task_id:
            task_id = args.task_id
            result = query_task(
                api_key=api_key,
                base_url=base_url,
                result_path_template=result_path_template,
                task_id=task_id,
                timeout=60,
                retries=args.query_retries,
            )
        else:
            result = submit_task(
                api_key=api_key,
                base_url=base_url,
                submit_path=submit_path,
                file_field=file_field,
                mode=mode,
                file_paths=file_paths,
            )
            task_id = extract_task_id(result)
            if not task_id:
                raise ApiError(f"Missing task_id in submit response: {result}")
            if not args.no_poll:
                log(f"[submit] task_id={task_id}", args.quiet)
                result = poll_until_terminal(
                    api_key=api_key,
                    base_url=base_url,
                    result_path_template=result_path_template,
                    task_id=task_id,
                    poll_interval=args.poll_interval,
                    timeout_seconds=args.timeout,
                    query_retries=args.query_retries,
                    quiet=args.quiet,
                )

        output_payload = (
            normalize_result(result) if args.output_format == "normalized" else result
        )

        if args.save:
            save_json(args.save, output_payload)
            log(f"[save] {Path(args.save).expanduser().resolve()}", args.quiet)

        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
        return 0
    except ApiError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
