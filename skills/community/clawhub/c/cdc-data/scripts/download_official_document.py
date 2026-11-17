#!/usr/bin/env python3
"""Download one verified China CDC PDF with deterministic validation/storage."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import BinaryIO


OFFICIAL_HOST = "www.chinacdc.cn"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/148.0.0.0 Safari/537.36"
)
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class DownloadError(RuntimeError):
    """A classified, user-safe download failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def validate_url(
    url: str,
    allowed_path_prefix: str,
    host: str = OFFICIAL_HOST,
    require_pdf: bool = False,
) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != host:
        raise DownloadError("url_out_of_scope", "URL must use HTTPS on the official China CDC host")
    if parsed.username or parsed.password or parsed.port not in (None, 443):
        raise DownloadError("url_out_of_scope", "URL contains disallowed authority components")
    if not allowed_path_prefix.startswith("/") or not parsed.path.startswith(allowed_path_prefix):
        raise DownloadError("url_out_of_scope", "URL path is outside the selected source adapter")
    if require_pdf and not parsed.path.lower().endswith(".pdf"):
        raise DownloadError("unsupported_document_type", "This downloader accepts PDF documents only")


class ScopedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed_path_prefix: str) -> None:
        self.allowed_path_prefix = allowed_path_prefix

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl, self.allowed_path_prefix, require_pdf=True)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def build_direct_opener(allowed_path_prefix: str) -> urllib.request.OpenerDirector:
    # An explicit empty ProxyHandler prevents urllib from consulting proxy env vars.
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        ScopedRedirectHandler(allowed_path_prefix),
    )


def stream_response(response: BinaryIO, temp_path: Path, max_bytes: int) -> tuple[int, str]:
    digest = hashlib.sha256()
    total = 0
    first = b""
    with temp_path.open("wb") as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            if not first:
                first = chunk[:8]
            total += len(chunk)
            if total > max_bytes:
                raise DownloadError("download_too_large", f"response exceeds {max_bytes} bytes")
            digest.update(chunk)
            output.write(chunk)
        output.flush()
        os.fsync(output.fileno())
    if total == 0:
        raise DownloadError("empty_response", "official response body is empty")
    if not first.startswith(b"%PDF-"):
        raise DownloadError("content_type_mismatch", "response does not have a PDF signature")
    return total, digest.hexdigest()


def deterministic_filename(args: argparse.Namespace, sha256: str) -> str:
    if args.week is not None:
        period = f"W{args.week:02d}"
    else:
        period = f"M{args.month:02d}"
    issue = str(args.issue) if args.issue is not None else "NA"
    return f"{args.report_type}_{args.year}_{period}_{issue}_{sha256[:8]}.pdf"


def place_without_overwrite(temp_path: Path, output_dir: Path, filename: str, sha256: str) -> tuple[Path, bool]:
    base = Path(filename).stem
    suffix = Path(filename).suffix
    sequence = 1
    while True:
        candidate = output_dir / (filename if sequence == 1 else f"{base}_{sequence}{suffix}")
        if not candidate.exists():
            os.replace(temp_path, candidate)
            return candidate, False
        existing_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if existing_hash == sha256:
            temp_path.unlink(missing_ok=True)
            return candidate, True
        sequence += 1


def download(args: argparse.Namespace, opener: urllib.request.OpenerDirector | None = None) -> dict[str, object]:
    validate_url(args.url, args.allowed_path_prefix, require_pdf=True)
    validate_url(args.referer, args.allowed_path_prefix)
    if not SAFE_ID.fullmatch(args.report_type):
        raise DownloadError("invalid_argument", "report type must be a safe ASCII identifier")
    if not (2000 <= args.year <= 2100):
        raise DownloadError("invalid_argument", "year is outside the supported range")
    if (args.week is None) == (args.month is None):
        raise DownloadError("invalid_argument", "provide exactly one of --week or --month")
    if args.week is not None and not 1 <= args.week <= 53:
        raise DownloadError("invalid_argument", "week must be 1-53")
    if args.month is not None and not 1 <= args.month <= 12:
        raise DownloadError("invalid_argument", "month must be 1-12")
    if args.issue is not None and args.issue <= 0:
        raise DownloadError("invalid_argument", "issue must be positive")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if not os.access(output_dir, os.W_OK):
        raise DownloadError("artifact_store_unavailable", "output directory is not writable")

    request = urllib.request.Request(
        args.url,
        headers={
            "User-Agent": args.user_agent,
            "Referer": args.referer,
            "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.1",
            "Accept-Encoding": "identity",
        },
        method="GET",
    )
    client = opener or build_direct_opener(args.allowed_path_prefix)
    temp_handle = tempfile.NamedTemporaryFile(prefix=".download-", suffix=".tmp", dir=output_dir, delete=False)
    temp_path = Path(temp_handle.name)
    temp_handle.close()
    try:
        with client.open(request, timeout=args.timeout) as response:
            final_url = response.geturl()
            validate_url(final_url, args.allowed_path_prefix, require_pdf=True)
            status = getattr(response, "status", 200)
            if status < 200 or status >= 300:
                raise DownloadError("http_status", f"official server returned HTTP {status}")
            content_type = response.headers.get_content_type().lower()
            if content_type not in {"application/pdf", "application/octet-stream"}:
                raise DownloadError("content_type_mismatch", f"unexpected content type: {content_type}")
            size, sha256 = stream_response(response, temp_path, args.max_bytes)
        filename = deterministic_filename(args, sha256)
        final_path, reused = place_without_overwrite(temp_path, output_dir, filename, sha256)
        return {
            "schema_version": "1.0",
            "status": "success",
            "path": str(final_path),
            "source_url": args.url,
            "final_url": final_url,
            "size_bytes": size,
            "sha256": sha256,
            "content_type": content_type,
            "reused": reused,
            "transport": "verified_http_download",
            "proxy_environment_ignored": True,
        }
    except DownloadError:
        raise
    except urllib.error.HTTPError as exc:
        raise DownloadError("http_status", f"official server returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError("network_error", str(exc.reason)) from exc
    except TimeoutError as exc:
        raise DownloadError("timeout", "download timed out") from exc
    finally:
        temp_path.unlink(missing_ok=True)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--referer", required=True)
    parser.add_argument("--allowed-path-prefix", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--report-type", required=True)
    parser.add_argument("--year", required=True, type=int)
    period = parser.add_mutually_exclusive_group(required=True)
    period.add_argument("--week", type=int)
    period.add_argument("--month", type=int)
    parser.add_argument("--issue", type=int)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--max-bytes", type=int, default=100 * 1024 * 1024)
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = download(args)
    except DownloadError as exc:
        print(json.dumps({"schema_version": "1.0", "status": "download_failed", "error": exc.code, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
