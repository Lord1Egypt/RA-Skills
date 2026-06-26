#!/usr/bin/env python3
"""Check ARKCloud API health."""

from __future__ import annotations

import argparse

from arkcloud_common import base_url, endpoint, print_json, request_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Check ARKCloud API health.")
    parser.add_argument("--base-url", default=None, help="ARKCloud base URL")
    args = parser.parse_args()

    root = base_url(args.base_url)
    payload = request_json("GET", endpoint(root, "/api/health"), timeout=30)
    print_json({"ok": True, "base_url": root, "health": payload})


if __name__ == "__main__":
    main()
