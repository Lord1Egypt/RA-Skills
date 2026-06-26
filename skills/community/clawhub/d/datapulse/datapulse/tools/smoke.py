"""End-to-end smoke suite for platform-level coverage checks."""

from __future__ import annotations

import argparse
import asyncio

from datapulse.core.utils import resolve_env_with_local_context
from datapulse.reader import DataPulseReader

SMOKE_SCENARIOS = {
    "twitter": {
        "env": "DATAPULSE_SMOKE_TWITTER_URL",
        "note": "X/Twitter single status URL",
    },
    "reddit": {
        "env": "DATAPULSE_SMOKE_REDDIT_URL",
        "note": "Reddit post URL",
    },
    "youtube": {
        "env": "DATAPULSE_SMOKE_YOUTUBE_URL",
        "note": "YouTube video URL",
    },
    "bilibili": {
        "env": "DATAPULSE_SMOKE_BILIBILI_URL",
        "note": "Bilibili video URL",
    },
    "telegram": {
        "env": "DATAPULSE_SMOKE_TELEGRAM_URL",
        "note": "Telegram public/channel URL",
    },
    "rss": {
        "env": "DATAPULSE_SMOKE_RSS_URL",
        "note": "RSS/Atom feed URL",
    },
    "wechat": {
        "env": "DATAPULSE_SMOKE_WECHAT_URL",
        "note": "WeChat public article URL",
    },
    "xhs": {
        "env": "DATAPULSE_SMOKE_XHS_URL",
        "note": "Xiaohongshu note URL",
    },
}


async def _run_scenario(name: str, url: str, min_confidence: float) -> tuple[str, bool, str]:
    try:
        item = await DataPulseReader().read(url, min_confidence=min_confidence)
        return name, True, f"{item.source_type.value}:{item.confidence:.3f}:{item.title[:80]}"
    except Exception as exc:
        return name, False, str(exc)


async def _run_feed_probe(min_confidence: float, profile: str = "default", limit: int = 5) -> tuple[bool, str]:
    reader = DataPulseReader()
    try:
        payload = reader.build_json_feed(profile=profile, limit=limit, min_confidence=min_confidence)
        return True, f"feed_items={len(payload.get('items', []))}"
    except Exception as exc:
        return False, f"feed_probe_error={exc}"


def _run_source_catalog_probe() -> tuple[bool, str]:
    try:
        sources = DataPulseReader().list_sources(public_only=True)
        packs = DataPulseReader().list_packs(public_only=True)
        return True, f"sources={len(sources)} packs={len(packs)}"
    except Exception as exc:
        return False, f"catalog_error={exc}"


def _plan(selected_platforms: set[str]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    planned = []
    missing = []
    local_key = "DATAPULSE_LOCAL_TEST_CONTEXT"
    for platform in selected_platforms:
        env_name = SMOKE_SCENARIOS[platform]["env"]
        url = resolve_env_with_local_context(env_name, local_key)
        if url:
            planned.append((platform, url))
        else:
            missing.append((platform, env_name))
    return planned, missing


async def main_async(platforms: list[str], min_confidence: float, require_all: bool, list_only: bool) -> int:
    selected = set(platforms)
    planned, missing = _plan(selected)

    if list_only:
        for platform in sorted(selected):
            env_name = SMOKE_SCENARIOS[platform]["env"]
            url = resolve_env_with_local_context(env_name, "DATAPULSE_LOCAL_TEST_CONTEXT")
            if url:
                print(f"- {platform:10s} OK  {env_name}={url}")
            else:
                note = SMOKE_SCENARIOS[platform]["note"]
                print(f"- {platform:10s} MISSING  set {env_name} for 1 {note}")
        return 0 if missing else 0

    if not planned:
        print("No smoke URLs configured.")
        for platform, env_name in missing:
            note = SMOKE_SCENARIOS[platform]["note"]
            print(f"- {platform:10s}: export {env_name}=\"<your-{platform}-url>\"  ({note})")
        return 0 if not require_all else 1

    if missing:
        print("Missing smoke URLs:")
        for platform, env_name in missing:
            note = SMOKE_SCENARIOS[platform]["note"]
            print(f"- {platform:10s}: {env_name} missing ({note})")
        if require_all:
            return 1

    print(f"Running DataPulse smoke scenarios: {len(planned)}")
    results = await asyncio.gather(*[_run_scenario(p, u, min_confidence) for p, u in planned])
    failed = 0
    for platform, ok, message in results:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {platform:10s} {message}")
        if not ok:
            failed += 1

    catalog_ok, catalog_msg = _run_source_catalog_probe()
    if catalog_ok:
        print(f"[PASS] source-catalog {catalog_msg}")
    else:
        print(f"[WARN] source-catalog {catalog_msg}")

    feed_ok, feed_msg = await _run_feed_probe(min_confidence=min_confidence)
    if feed_ok:
        print(f"[PASS] feed-probe {feed_msg}")
    else:
        failed += 1
        print(f"[FAIL] feed-probe {feed_msg}")

    return 1 if failed else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run DataPulse smoke scenarios.")
    parser.add_argument(
        "--platforms",
        nargs="+",
        default=sorted(SMOKE_SCENARIOS.keys()),
        help="Platform filters to run (default: all)",
    )
    parser.add_argument("--min-confidence", type=float, default=0.0, help="Minimum accepted confidence")
    parser.add_argument("--require-all", action="store_true", help="Fail if any platform URL is not configured")
    parser.add_argument("--list", action="store_true", help="Only show required env vars and exit")
    args = parser.parse_args()

    valid = {name for name in args.platforms if name in SMOKE_SCENARIOS}
    invalid = set(args.platforms) - valid
    if invalid:
        unknown = ", ".join(sorted(invalid))
        raise SystemExit(f"Unknown platforms: {unknown}")

    raise SystemExit(asyncio.run(main_async(sorted(valid), args.min_confidence, args.require_all, args.list)))


if __name__ == "__main__":
    main()
