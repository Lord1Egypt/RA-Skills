#!/usr/bin/env python3
"""List image files created after an adaptive handoff pack was prepared."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from handoff_common import IMAGE_EXTENSIONS, image_info, load_json, save_json, sha256_file, utc_now


def parse_time(value: str) -> float:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", required=True, type=Path)
    parser.add_argument("--downloads", type=Path, default=Path.home() / "Downloads")
    parser.add_argument("--all", action="store_true", help="Include images older than the handoff")
    args = parser.parse_args()

    handoff = args.handoff.expanduser().resolve()
    downloads = args.downloads.expanduser().resolve()
    state = load_json(handoff / "jobs.json")
    if not downloads.is_dir():
        raise SystemExit(f"Download directory not found: {downloads}")

    since = 0.0 if args.all else parse_time(state["created_at"])
    imported_hashes = {
        job.get("import", {}).get("source_sha256")
        for job in state.get("jobs", [])
        if job.get("import", {}).get("source_sha256")
    }
    candidates: list[dict[str, Any]] = []
    for path in downloads.iterdir():
        if not path.is_file() or path.name.startswith(".") or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        stat = path.stat()
        if stat.st_mtime < since:
            continue
        try:
            info = image_info(path)
            checksum = sha256_file(path)
        except Exception as error:
            candidates.append({"path": str(path), "error": str(error), "modified_at": stat.st_mtime})
            continue
        candidates.append(
            {
                "path": str(path),
                "filename": path.name,
                "modified_at": stat.st_mtime,
                "size_bytes": stat.st_size,
                "sha256": checksum,
                "already_imported": checksum in imported_hashes,
                **info,
            }
        )

    candidates.sort(key=lambda item: item["modified_at"])
    report = {
        "run_id": state["run_id"],
        "scanned_at": utc_now(),
        "downloads_directory": str(downloads),
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    output = handoff / "reports" / "download-candidates.json"
    save_json(output, report)
    print(output)
    for candidate in candidates:
        if candidate.get("error"):
            print(f"ERROR\t{candidate['path']}\t{candidate['error']}")
        else:
            print(
                f"{candidate['width']}x{candidate['height']}\t"
                f"{candidate['sha256'][:12]}\t{candidate['path']}"
            )


if __name__ == "__main__":
    main()
