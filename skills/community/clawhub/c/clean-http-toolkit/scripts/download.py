#!/usr/bin/env python3
"""
download.py - Stream a large file from a URL to disk with progress, retries,
and optional checksum verification.

Pure Python 3 stdlib (urllib). Designed for AI agents pulling datasets,
models, or attachments. Streams in chunks so memory stays bounded even on
multi-gigabyte downloads.

Usage:
    download.py URL OUTPUT [options]

Options:
    --header 'Name: V'   custom header (may repeat)
    --bearer TOKEN       Authorization: Bearer ...
    --timeout SECONDS    per-request timeout (default: 60)
    --retries N          retry on 5xx / 429 / connection error (default: 3)
    --chunk-size N       bytes per chunk (default: 65536)
    --resume             resume an incomplete download (uses Range: header
                         and existing file size as the start offset)
    --insecure           skip TLS verification
    --sha256 HEX         verify the downloaded file's SHA-256 matches HEX
                         (exits 1 on mismatch)
    --md5 HEX            verify MD5
    --quiet              suppress the progress line on stderr
    --json-summary       emit a machine-readable summary on stderr at the end
    -h, --help           show this help

Exit codes:
    0   download complete (and checksum matches if --sha256/--md5 set)
    1   download finished but checksum mismatch
    2   bad arguments / unsafe path / bad URL / network error /
        non-2xx HTTP response
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

from _common import (DEFAULT_USER_AGENT, parse_headers, safe_path, safe_url)


def _human(n: int) -> str:
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if n < 1024:
            return f"{n:.1f}{unit}" if isinstance(n, float) else f"{n}{unit}"
        n /= 1024
    return f"{n:.1f}PiB"


def main() -> int:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("url", nargs="?")
    p.add_argument("output", nargs="?")
    p.add_argument("--header", action="append", default=[])
    p.add_argument("--bearer")
    p.add_argument("--timeout", type=float, default=60.0)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--chunk-size", dest="chunk_size", type=int, default=65536)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--insecure", action="store_true")
    p.add_argument("--sha256")
    p.add_argument("--md5")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--json-summary", dest="json_summary", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    args = p.parse_args()

    if args.help or not args.url or not args.output:
        print(__doc__)
        return 0 if args.help else 2

    try:
        url = safe_url(args.url)
        out_path = safe_path(args.output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    try:
        headers = parse_headers(args.header)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    headers.setdefault("User-Agent", DEFAULT_USER_AGENT)
    if args.bearer:
        headers["Authorization"] = f"Bearer {args.bearer}"

    # Resume support
    start_offset = 0
    if args.resume and out_path.exists():
        start_offset = out_path.stat().st_size
        if start_offset > 0:
            headers["Range"] = f"bytes={start_offset}-"

    # TLS
    handlers = []
    if args.insecure:
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            handlers.append(urllib.request.HTTPSHandler(context=ctx))
        except Exception:
            pass
    opener = urllib.request.build_opener(*handlers)

    last_err = None
    for attempt in range(args.retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            resp = opener.open(req, timeout=args.timeout)
            status = resp.status
            if status not in (200, 206):
                resp.close()
                print(f"Error: HTTP {status} (expected 200 or 206)",
                      file=sys.stderr)
                return 2

            total_size: int = 0
            cl = resp.headers.get("Content-Length")
            if cl is not None:
                try:
                    total_size = int(cl)
                except ValueError:
                    total_size = 0
            if status == 206:
                total_size += start_offset

            mode = "ab" if (args.resume and start_offset > 0 and status == 206) else "wb"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            downloaded = start_offset if mode == "ab" else 0
            t0 = time.time()
            last_print = 0.0

            hash_sha256 = hashlib.sha256() if args.sha256 else None
            hash_md5 = hashlib.md5() if args.md5 else None
            # If we're resuming, we need to also feed existing bytes through
            # the hasher; otherwise the final hash won't match.
            if mode == "ab" and (hash_sha256 or hash_md5):
                with out_path.open("rb") as f:
                    while True:
                        chunk = f.read(args.chunk_size)
                        if not chunk:
                            break
                        if hash_sha256: hash_sha256.update(chunk)
                        if hash_md5: hash_md5.update(chunk)

            with out_path.open(mode) as f:
                while True:
                    chunk = resp.read(args.chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    if hash_sha256: hash_sha256.update(chunk)
                    if hash_md5: hash_md5.update(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if not args.quiet and (now - last_print) >= 0.25:
                        elapsed = now - t0 or 0.001
                        rate = (downloaded - start_offset) / elapsed
                        if total_size > 0:
                            pct = 100.0 * downloaded / total_size
                            sys.stderr.write(
                                f"\rdownload: {_human(downloaded)}/"
                                f"{_human(total_size)} "
                                f"({pct:5.1f}%) @ {_human(int(rate))}/s"
                            )
                        else:
                            sys.stderr.write(
                                f"\rdownload: {_human(downloaded)} "
                                f"@ {_human(int(rate))}/s"
                            )
                        sys.stderr.flush()
                        last_print = now
            resp.close()
            if not args.quiet:
                sys.stderr.write("\n")
                sys.stderr.flush()

            # Checksums
            checksum_ok = True
            actual_sha256 = hash_sha256.hexdigest() if hash_sha256 else None
            actual_md5 = hash_md5.hexdigest() if hash_md5 else None
            if args.sha256 and actual_sha256.lower() != args.sha256.lower():
                print(f"Error: SHA-256 mismatch.\n  expected: {args.sha256}\n"
                      f"  got:      {actual_sha256}", file=sys.stderr)
                checksum_ok = False
            if args.md5 and actual_md5.lower() != args.md5.lower():
                print(f"Error: MD5 mismatch.\n  expected: {args.md5}\n"
                      f"  got:      {actual_md5}", file=sys.stderr)
                checksum_ok = False

            if args.json_summary:
                summary = {
                    "url": url, "output": str(out_path), "status": status,
                    "bytes": downloaded, "elapsed_s": round(time.time() - t0, 3),
                    "sha256": actual_sha256, "md5": actual_md5,
                    "checksum_ok": checksum_ok,
                }
                print(json.dumps(summary, indent=2), file=sys.stderr)
            elif not args.quiet:
                elapsed = time.time() - t0 or 0.001
                rate = (downloaded - start_offset) / elapsed
                print(f"download: {_human(downloaded)} in {elapsed:.1f}s "
                      f"({_human(int(rate))}/s) -> {out_path}",
                      file=sys.stderr)

            return 0 if checksum_ok else 1

        except urllib.error.HTTPError as e:
            status = e.code
            if status in (408, 429, 500, 502, 503, 504) and attempt < args.retries:
                time.sleep(0.5 * (2 ** attempt))
                continue
            print(f"Error: HTTP {status}: {e.reason}", file=sys.stderr)
            return 2
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
            if attempt < args.retries:
                if not args.quiet:
                    sys.stderr.write(f"\ndownload: retry {attempt+1}/{args.retries} "
                                      f"after error: {e}\n")
                time.sleep(0.5 * (2 ** attempt))
                continue
            print(f"Error: network error: {e}", file=sys.stderr)
            return 2

    print(f"Error: retries exhausted ({last_err})", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
