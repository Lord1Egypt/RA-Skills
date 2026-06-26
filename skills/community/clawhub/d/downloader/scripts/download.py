#!/usr/bin/env python3
"""Download a file from a URL and save it locally.

Dependencies:
    pip install requests
"""

import argparse
import json
import os
import sys
from urllib.parse import unquote, urlparse

import requests


def download_file(url: str, save_path: str) -> str:
    """Download a file from url and save to save_path. Returns the absolute path."""
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

    resp = requests.get(url, stream=True, timeout=120)
    resp.raise_for_status()

    with open(save_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    return os.path.abspath(save_path)


def _filename_from_url(url: str) -> str:
    """Extract a filename from the URL path."""
    path = urlparse(url).path
    name = os.path.basename(unquote(path))
    return name if name else "downloaded_file"


def main():
    parser = argparse.ArgumentParser(description="Download a file from a URL and save it locally")
    parser.add_argument("--url", required=True, help="URL of the file to download")
    parser.add_argument("--save_path", default=None, help="Local path to save the file (optional)")
    args = parser.parse_args()

    if args.save_path:
        save_path = args.save_path
    else:
        save_path = os.path.join(".", _filename_from_url(args.url))

    try:
        abs_path = download_file(args.url, save_path)
    except Exception as e:
        print(json.dumps({"code": 1, "message": str(e), "data": ""}))
        sys.exit(1)

    print(json.dumps({"code": 0, "message": "success", "data": abs_path}))


if __name__ == "__main__":
    main()
