#!/usr/bin/env python3
"""Deterministically upload a binary to Odoo — no base64 arg, no chunking, no truncation.

Works for decoration production files AND **storefront product web images**
(``product.template.image_1920`` / ``product.product.image_variant_1920``):
writing a real product photo as a base64 MCP *argument* is clipped by the
tool-arg size cap (it arrives truncated), so this multipart upload is the
byte-exact path for product images too.

POSTs a **local file by path** straight to the drivethru_mcp upload endpoint
(``POST /drivethru_mcp/v1/upload``). The Odoo server base64-encodes and writes
the binary field (running the same whitelist + 20 MB guard + CDN offload as the
``decoration_set_image`` MCP tool), so the bytes never pass through the agent's
token stream. Prefer it for a real (large) production file when ``ODOO_MCP_URL`` /
``ODOO_MCP_TOKEN`` are set; otherwise stream the field through the chunked
``decoration_set_image`` MCP tool (which needs no extra env). Both enforce the
same 20 MB server guard.

Usage (decoration production file):
    python3 scripts/upload_production_file.py \
        --file /tmp/dtf_production.png \
        --record-id 18 \
        [--field dtf_production_png] [--model decoration] \
        [--base-url https://baconco.odoo.com/drivethru_mcp/v1] [--api-key <key>] [--timeout 60]

Usage (storefront product web image):
    python3 scripts/upload_production_file.py \
        --file /tmp/web_image.jpg \
        --model product.template --field image_1920 --record-id 22577
    # per-color variant image:
    python3 scripts/upload_production_file.py \
        --file /tmp/web_image.jpg \
        --model product.product --field image_variant_1920 --record-id 271696

``--base-url`` / ``--api-key`` default to the ``ODOO_MCP_URL`` /
``ODOO_MCP_TOKEN`` environment variables (the same credentials the other
drivethru-* skills use). ``ODOO_MCP_URL`` is the full MCP endpoint
(``.../drivethru_mcp/v1``); the upload route is that endpoint + ``/upload``.
Prints the server's JSON result
(``present``, ``cdn_url``/``web_url``, ``bytes_received``) on success; exits
non-zero with the server's error on failure.

Requires ``requests`` (``pip install requests``). TLS trust is taken from the
standard ``REQUESTS_CA_BUNDLE`` environment variable when set (e.g. a proxy CA),
so no ``verify`` override is needed.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path


def build_upload_url(base_url: str) -> str:
    """Return the deterministic upload URL for an ``ODOO_MCP_URL`` value.

    ``ODOO_MCP_URL`` is the full MCP endpoint (``.../drivethru_mcp/v1``), the
    same value the other drivethru-* skills consume; the upload route is that
    endpoint + ``/upload``. A bare Odoo root (no ``/drivethru_mcp/v1``) or an
    already-complete upload URL is accepted and normalized too, so the script
    works whichever form the environment provides.
    """
    base = base_url.rstrip("/")
    if base.endswith("/upload"):
        return base
    if not base.endswith("/drivethru_mcp/v1"):
        base += "/drivethru_mcp/v1"
    return base + "/upload"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload a local production file to a decoration binary field")
    parser.add_argument("--file", required=True, help="Path to the file to upload")
    parser.add_argument("--record-id", required=True,
                        help="Target record id (decoration / decoration.request / "
                             "product.template / product.product)")
    parser.add_argument("--field", default="dtf_production_png",
                        help="Binary field to write. Decoration: dtf_production_png "
                             "(default), image, ... Product web image: image_1920 "
                             "(product.template) or image_variant_1920 (product.product).")
    parser.add_argument("--model", default="decoration",
                        choices=["decoration", "decoration.request",
                                 "product.template", "product.product"])
    parser.add_argument("--base-url", default=os.environ.get("ODOO_MCP_URL", ""),
                        help="Odoo MCP endpoint, e.g. https://host/drivethru_mcp/v1 "
                             "(or set ODOO_MCP_URL)")
    parser.add_argument("--api-key", default=os.environ.get("ODOO_MCP_TOKEN", ""),
                        help="drivethru.mcp_key (or set ODOO_MCP_TOKEN)")
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    if not args.base_url:
        print("ERROR: --base-url (or ODOO_MCP_URL) is required", file=sys.stderr)
        sys.exit(1)
    if not args.api_key:
        print("ERROR: --api-key (or ODOO_MCP_TOKEN) is required", file=sys.stderr)
        sys.exit(1)

    try:
        import requests
    except ImportError:
        print("ERROR: this script needs 'requests' (pip install requests)", file=sys.stderr)
        sys.exit(1)

    url = build_upload_url(args.base_url)
    mimetype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"

    with path.open("rb") as fh:
        try:
            resp = requests.post(
                url,
                headers={"Authorization": f"Bearer {args.api_key}"},
                data={"model": args.model, "record_id": str(args.record_id),
                      "field": args.field},
                files={"file": (path.name, fh, mimetype)},
                timeout=args.timeout,
            )
        except requests.RequestException as exc:
            print(f"ERROR: request failed: {exc}", file=sys.stderr)
            sys.exit(1)

    try:
        body = resp.json()
    except ValueError:
        print(f"ERROR: non-JSON response ({resp.status_code}): {resp.text[:500]}",
              file=sys.stderr)
        sys.exit(1)

    if resp.status_code == 200 and body.get("success"):
        print(json.dumps(body.get("data", {})))
        return
    print(f"ERROR: upload failed ({resp.status_code}): "
          f"{body.get('error') or body}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
