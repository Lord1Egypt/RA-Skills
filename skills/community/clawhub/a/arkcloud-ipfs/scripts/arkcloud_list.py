#!/usr/bin/env python3
"""List uploads from an ARKCloud logged-in client session."""

from __future__ import annotations

import argparse

from arkcloud_common import base_url, endpoint, print_json, request_json, require_env


def main() -> None:
    parser = argparse.ArgumentParser(description="List ARKCloud IPFS uploads.")
    parser.add_argument("--base-url", default=None, help="ARKCloud base URL")
    args = parser.parse_args()

    cookie = require_env(
        "ARKCLOUD_CLIENT_COOKIE",
        "Listing uploads requires ARKCLOUD_CLIENT_COOKIE from a logged-in client session",
    )

    payload = request_json(
        "GET",
        endpoint(base_url(args.base_url), "/api/client/uploads"),
        headers={"Cookie": cookie},
    )
    print_json({"ok": True, "uploads": payload})


if __name__ == "__main__":
    main()
