#!/usr/bin/env python3
"""Delete or unpublish an ARKCloud upload from a logged-in client session."""

from __future__ import annotations

import argparse
from urllib.parse import quote

from arkcloud_common import base_url, endpoint, print_json, request_json, require_env


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete an ARKCloud IPFS upload.")
    parser.add_argument("upload_id", help="Upload ID to delete")
    parser.add_argument("--base-url", default=None, help="ARKCloud base URL")
    args = parser.parse_args()

    cookie = require_env(
        "ARKCLOUD_CLIENT_COOKIE",
        "Delete requires ARKCLOUD_CLIENT_COOKIE and ARKCLOUD_CSRF_TOKEN from a logged-in client session",
    )
    csrf = require_env(
        "ARKCLOUD_CSRF_TOKEN",
        "Delete requires ARKCLOUD_CLIENT_COOKIE and ARKCLOUD_CSRF_TOKEN from a logged-in client session",
    )

    upload_id = quote(args.upload_id, safe="")
    payload = request_json(
        "DELETE",
        endpoint(base_url(args.base_url), f"/api/client/uploads/{upload_id}"),
        headers={
            "Cookie": cookie,
            "X-CSRF-Token": csrf,
        },
    )
    print_json({"ok": True, **payload})


if __name__ == "__main__":
    main()
