#!/usr/bin/env python3
"""Refresh the local CN market-tape theme cache from the configured public source.

The script updates only the local skill cache. It keeps a stamp file and skips
network access when the cached files are fresh enough, defaulting to 7 days.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://daytrading.monster/themes"
ASSET_FILES = ("theme-data.json", "theme-label-i18n.json")
STAMP_FILE = ".last_refresh.json"
REQUIRED_DATA_KEYS = {"market", "code", "theme", "weight"}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_theme_data(path: Path) -> None:
    data = load_json(path)
    rows = data.get("rows") if isinstance(data, dict) else data
    if not isinstance(rows, list) or not rows:
        raise SystemExit(f"{path} must contain a non-empty rows[] list")
    sample = next((row for row in rows if isinstance(row, dict)), None)
    if sample is None:
        raise SystemExit(f"{path} does not contain object rows")
    missing = REQUIRED_DATA_KEYS - set(sample)
    if missing:
        raise SystemExit(f"{path} is missing required fields: {', '.join(sorted(missing))}")


def validate_labels(path: Path) -> None:
    labels = load_json(path)
    if not isinstance(labels, dict) or not labels:
        raise SystemExit(f"{path} must contain a non-empty object")
    has_zh = any(isinstance(value, dict) and value.get("zh") for value in labels.values())
    if not has_zh:
        raise SystemExit(f"{path} must contain at least one zh label")


def validate_assets(target_dir: Path) -> None:
    validate_theme_data(target_dir / "theme-data.json")
    validate_labels(target_dir / "theme-label-i18n.json")


def is_cache_fresh(target_dir: Path, max_age_days: int) -> bool:
    asset_paths = [target_dir / filename for filename in ASSET_FILES]
    if not all(path.exists() for path in asset_paths):
        return False

    stamp_path = target_dir / STAMP_FILE
    if not stamp_path.exists():
        return False
    try:
        stamp = load_json(stamp_path)
    except Exception:
        return False
    fetched_at = parse_time(stamp.get("fetchedAt")) if isinstance(stamp, dict) else None
    if fetched_at is None:
        return False
    age_seconds = (utc_now() - fetched_at).total_seconds()
    if age_seconds > max_age_days * 86400:
        return False
    oldest_asset_mtime = min(datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) for path in asset_paths)
    if (utc_now() - oldest_asset_mtime).total_seconds() > max_age_days * 86400:
        return False
    try:
        validate_assets(target_dir)
    except Exception:
        return False
    return True


def download_json(url: str, dest: Path) -> dict[str, str | None]:
    req = Request(url, headers={"User-Agent": "codex-market-skills/refresh-theme-assets"})
    try:
        with urlopen(req, timeout=30) as response:
            body = response.read()
            headers = response.headers
    except (HTTPError, URLError, TimeoutError) as exc:
        raise SystemExit(f"failed to download {url}: {exc}") from exc

    # Parse before writing so HTML error pages never replace valid assets.
    try:
        json.loads(body.decode("utf-8"))
    except Exception as exc:
        raise SystemExit(f"{url} did not return valid JSON") from exc

    with tempfile.NamedTemporaryFile("wb", delete=False, dir=str(dest.parent), prefix=dest.name, suffix=".tmp") as tmp:
        tmp.write(body)
        tmp_path = Path(tmp.name)
    tmp_path.replace(dest)
    return {
        "url": url,
        "etag": headers.get("ETag"),
        "lastModified": headers.get("Last-Modified"),
        "contentLength": headers.get("Content-Length"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh the local A-share theme mapping cache from the configured public source.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL that serves theme-data.json and theme-label-i18n.json")
    parser.add_argument("--target-dir", type=Path, default=Path(__file__).resolve().parents[1] / "assets" / "themes", help="Directory to update; defaults to this skill's local assets/themes cache")
    parser.add_argument("--max-age-days", type=int, default=7, help="Skip refresh when local assets are fresher than this many days")
    parser.add_argument("--force", action="store_true", help="Refresh even when the local cache is still fresh")
    parser.add_argument("--dry-run", action="store_true", help="Validate whether refresh would run, without writing files")
    args = parser.parse_args()

    target_dir = args.target_dir.expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    if not args.force and is_cache_fresh(target_dir, args.max_age_days):
        print(f"theme assets are fresh; skip refresh ({target_dir})")
        return 0

    if args.dry_run:
        print(f"theme assets would refresh into {target_dir}")
        return 0

    base_url = args.base_url.rstrip("/")
    file_meta: dict[str, dict[str, str | None]] = {}
    for filename in ASSET_FILES:
        url = f"{base_url}/{filename}"
        file_meta[filename] = download_json(url, target_dir / filename)

    validate_assets(target_dir)

    stamp = {
        "fetchedAt": utc_now().isoformat().replace("+00:00", "Z"),
        "baseUrl": base_url,
        "maxAgeDays": args.max_age_days,
        "files": file_meta,
    }
    (target_dir / STAMP_FILE).write_text(json.dumps(stamp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"refreshed {target_dir / 'theme-data.json'}")
    print(f"refreshed {target_dir / 'theme-label-i18n.json'}")
    print(f"wrote {target_dir / STAMP_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
