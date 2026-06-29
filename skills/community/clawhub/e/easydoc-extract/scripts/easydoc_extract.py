#!/usr/bin/env python3
"""
Submit files to EasyLink extraction API and poll until completion.

Modes:
  easydoc-extract       Universal extraction (open / closed / prompt-driven)
  easydoc-extract-flash Universal extraction with bounding-box output (closed only)
  bl-extract            Business license (fixed fields, no schema needed)
  occ-extract           Org-code certificate (fixed fields, no schema needed)

Usage examples:
  # Open extraction (auto-detect all fields)
  python3 easydoc_extract.py --file ./doc.pdf --mode easydoc-extract

  # Closed extraction with custom schema
  python3 easydoc_extract.py --file ./doc.pdf --mode easydoc-extract \
    --fields "姓名" "日期" "金额"

  # Flash mode (closed, returns bounding boxes)
  python3 easydoc_extract.py --file ./doc.pdf --mode easydoc-extract-flash \
    --fields "姓名" "金额"

  # Custom prompt
  python3 easydoc_extract.py --file ./doc.pdf --mode easydoc-extract \
    --prompt "提取所有金额和日期"

  # Business license (fixed fields)
  python3 easydoc_extract.py --file ./license.jpg --mode bl-extract

  # Org-code certificate (fixed fields)
  python3 easydoc_extract.py --file ./cert.jpg --mode occ-extract

  # Poll existing task
  python3 easydoc_extract.py --poll-only --task-id "b_extract_xxx"
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

SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

# Modes that accept json_schema / prompt_cus
UNIVERSAL_MODES = {"easydoc-extract", "easydoc-extract-flash"}
# Modes that only support closed extraction via json_schema
FLASH_MODES = {"easydoc-extract-flash"}
# Modes with fixed system-defined fields (no schema)
FIXED_FIELD_MODES = {"bl-extract", "occ-extract"}

ALL_MODES = UNIVERSAL_MODES | FIXED_FIELD_MODES

BASE_URL = "https://api.easylink-ai.com"
SUBMIT_PATH = "/v1/easydoc/extract"
RESULT_PATH = "/v1/easydoc/extract/{task_id}"
FILE_FIELD = "files"


class ApiError(Exception):
    """Raised when API communication fails."""


def onboarding_hint() -> str:
    return (
        "Missing API key.\n"
        "1) Sign up or log in at https://platform.easylink-ai.com\n"
        "2) Create an API key in the platform API key page\n"
        "3) Retry with --api-key or export EASYLINK_API_KEY"
    )


def resolve_api_key(cli_api_key: str) -> str:
    if cli_api_key.strip():
        return cli_api_key.strip()
    value = os.getenv("EASYLINK_API_KEY", "").strip()
    if value:
        return value
    raise ApiError(onboarding_hint())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit EasyLink extraction jobs and poll asynchronous status."
    )
    parser.add_argument("--api-key", default="",
                        help="API key. Reads EASYLINK_API_KEY from env if omitted.")
    parser.add_argument("--base-url", default="", help="Optional base URL override.")
    parser.add_argument("--file", action="append", default=[],
                        help="Input file path. Repeatable for multi-file upload.")
    parser.add_argument(
        "--mode",
        choices=sorted(ALL_MODES),
        default="easydoc-extract",
        help=(
            "Extraction mode. "
            "easydoc-extract: universal (open/closed/prompt). "
            "easydoc-extract-flash: universal with bbox, closed only. "
            "bl-extract: business license (fixed fields). "
            "occ-extract: org-code certificate (fixed fields). "
            "Default: easydoc-extract"
        ),
    )
    parser.add_argument(
        "--fields", nargs="+", default=[], metavar="FIELD",
        help=(
            "Fields to extract (universal modes only). "
            "Enables closed extraction. "
            "Required for easydoc-extract-flash."
        ),
    )
    parser.add_argument(
        "--prompt", default="",
        help=(
            "Custom extraction prompt (easydoc-extract only). "
            "Used when --fields is not provided."
        ),
    )
    parser.add_argument("--task-id", default="",
                        help="Existing task id for --poll-only or single query.")
    parser.add_argument("--poll-only", action="store_true",
                        help="Do not submit. Poll existing --task-id only.")
    parser.add_argument("--poll-interval", type=float, default=2.0,
                        help="Polling interval in seconds. Default: 2.0")
    parser.add_argument("--timeout", type=int, default=600,
                        help="Polling timeout in seconds. Default: 600")
    parser.add_argument("--no-poll", action="store_true",
                        help="Submit only and print task creation response.")
    parser.add_argument("--save", default="",
                        help="Optional output file path to save final JSON response.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress progress logs and print JSON only.")
    parser.add_argument("--output-format", choices=["normalized", "raw"],
                        default="normalized",
                        help="Output normalized envelope or raw API payload. Default: normalized")
    parser.add_argument("--query-retries", type=int, default=3,
                        help="Retries for GET polling on transient failures. Default: 3")
    parser.add_argument("--skip-local-checks", action="store_true",
                        help="Skip local extension and file-size checks before upload.")
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

    if args.mode in FLASH_MODES and not args.fields:
        raise ApiError(f"--mode {args.mode} requires --fields (closed extraction only).")

    if args.fields and args.mode in FIXED_FIELD_MODES:
        raise ApiError(f"--mode {args.mode} uses fixed system-defined fields; --fields is not supported.")

    if args.prompt and args.mode in FIXED_FIELD_MODES:
        raise ApiError(f"--mode {args.mode} does not support --prompt.")

    if args.prompt and args.mode in FLASH_MODES:
        raise ApiError(f"--mode {args.mode} does not support --prompt (closed extraction only).")


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
        body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode("utf-8"))
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    for field_name, file_path in files:
        filename = file_path.name
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend((
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode("utf-8"))
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(file_path.read_bytes())
        body.extend(b"\r\n")

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return bytes(body), boundary


def submit_task(
    api_key: str,
    base_url: str,
    file_paths: List[Path],
    mode: str,
    custom_fields: List[str],
    custom_prompt: str,
    timeout: int = 60,
) -> Dict:
    url = f"{base_url.rstrip('/')}{SUBMIT_PATH}"

    form_fields: List[Tuple[str, str]] = [("mode", mode)]

    if mode in UNIVERSAL_MODES:
        if custom_fields:
            properties = {field: {"type": "string"} for field in custom_fields}
            schema = json.dumps(
                {"type": "object", "properties": properties}, ensure_ascii=False
            )
            form_fields.append(("json_schema", schema))
        elif custom_prompt:
            form_fields.append(("prompt_cus", custom_prompt))
        # else: open extraction — no extra params

    payload, boundary = encode_multipart(
        fields=form_fields,
        files=[(FILE_FIELD, fp) for fp in file_paths],
    )
    headers = {
        "api-key": api_key,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    return http_json("POST", url, headers=headers, body=payload, timeout=timeout)


def query_task(
    api_key: str,
    base_url: str,
    task_id: str,
    timeout: int = 60,
    retries: int = 0,
) -> Dict:
    path = RESULT_PATH.format(task_id=task_id)
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


def extract_pages(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return per-page extraction results from the API response."""
    for container in _candidate_dicts(payload):
        results = container.get("results")
        if not isinstance(results, list):
            continue
        pages = []
        for page in results:
            if not isinstance(page, dict):
                continue
            page_number = page.get("page_number")
            fields: Dict[str, Any] = {}
            for entry in page.get("extract_data") or []:
                if not isinstance(entry, dict):
                    continue
                ef = entry.get("extracted_fields")
                if isinstance(ef, dict):
                    fields.update(ef)
            pages.append({"page_number": page_number, "fields": fields})
        return pages
    return []


def normalize_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "task_id": extract_task_id(payload),
        "status": extract_status(payload),
        "results": extract_pages(payload),
        "raw": payload,
    }


def save_json(path: str, payload: Dict) -> None:
    out_path = Path(path).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def log(msg: str, quiet: bool) -> None:
    if not quiet:
        print(msg, file=sys.stderr)


def validate_files(file_paths: List[Path], skip_local_checks: bool) -> None:
    for path in file_paths:
        if not path.exists():
            raise ApiError(f"File not found: {path}")
        if not path.is_file():
            raise ApiError(f"Not a file: {path}")
        if skip_local_checks:
            continue
        ext = path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            allowed = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise ApiError(
                f"Unsupported file extension '{ext}': {path.name}. Allowed: {allowed}"
            )
        size = path.stat().st_size
        if size > MAX_FILE_SIZE_BYTES:
            raise ApiError(f"File exceeds 100MB limit: {path} ({size} bytes).")


def poll_until_terminal(
    api_key: str,
    base_url: str,
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


def main() -> int:
    args = parse_args()
    try:
        ensure_inputs(args)

        api_key = resolve_api_key(args.api_key)
        base_url = args.base_url.strip() or BASE_URL
        file_paths = [Path(p).expanduser().resolve() for p in args.file]

        if file_paths:
            validate_files(file_paths, skip_local_checks=args.skip_local_checks)

        if args.poll_only:
            result = poll_until_terminal(
                api_key=api_key,
                base_url=base_url,
                task_id=args.task_id,
                poll_interval=args.poll_interval,
                timeout_seconds=args.timeout,
                query_retries=args.query_retries,
                quiet=args.quiet,
            )
        elif args.task_id:
            result = query_task(
                api_key=api_key,
                base_url=base_url,
                task_id=args.task_id,
                timeout=60,
                retries=args.query_retries,
            )
        else:
            result = submit_task(
                api_key=api_key,
                base_url=base_url,
                file_paths=file_paths,
                mode=args.mode,
                custom_fields=args.fields,
                custom_prompt=args.prompt,
            )
            task_id = extract_task_id(result)
            if not task_id:
                raise ApiError(f"Missing task_id in submit response: {result}")
            if not args.no_poll:
                log(f"[submit] task_id={task_id}", args.quiet)
                result = poll_until_terminal(
                    api_key=api_key,
                    base_url=base_url,
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
