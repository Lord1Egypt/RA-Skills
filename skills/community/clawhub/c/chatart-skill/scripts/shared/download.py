import sys

import requests
import os


def download_file(url: str, output_path: str, quiet: bool = False) -> None:
    """Download a file from URL to a local path."""
    if not quiet:
        print(f"Downloading {url} -> {output_path}...", file=sys.stderr)

    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    if not quiet:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Downloaded: {output_path} ({size_mb:.1f} MB)", file=sys.stderr)