#!/usr/bin/env python3
"""
AI Launch Pipeline — one-click end-to-end workflow.

Stages:
  1. RSS Monitor   — fetch new AI product launch posts
  2. Product Search — enrich each launch with DuckDuckGo results
  3. Screenshot     — capture product page screenshots (optional, needs playwright)
  4. Trend Analysis — generate insights report

Usage:
  python run_pipeline.py                    # full pipeline
  python run_pipeline.py --skip-screenshot  # skip screenshot stage
  python run_pipeline.py --stage search     # run single stage
"""

import argparse, json, os, sys, time

# Resolve script directory so imports work regardless of cwd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Default paths (overridable via env vars)
BASE_DIR = os.environ.get("PIPELINE_BASE_DIR", os.path.dirname(SCRIPT_DIR))
DATA_DIR = os.environ.get("PIPELINE_DATA_DIR", os.path.join(BASE_DIR, "data"))
SCREENSHOT_DIR = os.environ.get("PIPELINE_SCREENSHOT_DIR", os.path.join(BASE_DIR, "screenshots"))
ANALYSIS_DIR = os.environ.get("PIPELINE_ANALYSIS_DIR", os.path.join(BASE_DIR, "analysis"))
CONFIG_PATH = os.environ.get("PIPELINE_CONFIG", os.path.join(BASE_DIR, "config", "rss_feeds.yaml"))

# Ensure data dirs exist
for d in [DATA_DIR, SCREENSHOT_DIR, ANALYSIS_DIR]:
    os.makedirs(d, exist_ok=True)


def stage_rss():
    from rss_monitor import run as rss_run
    print("\n" + "=" * 60)
    print("STAGE 1/4 — RSS Monitor")
    print("=" * 60)
    items = rss_run(CONFIG_PATH)
    print(f"  ✓ {len(items)} new launches found")
    return items


def stage_search(launches):
    from product_search import run as search_run
    print("\n" + "=" * 60)
    print("STAGE 2/4 — Product Search")
    print("=" * 60)
    enriched = search_run(launches)
    print(f"  ✓ {len(enriched)} items enriched")
    return enriched


def stage_screenshot(launches):
    from screenshot_capture import run as screenshot_run
    print("\n" + "=" * 60)
    print("STAGE 3/4 — Screenshot Capture")
    print("=" * 60)
    results = screenshot_run(launches)
    print(f"  ✓ {len(results)} screenshots attempted")
    return results


def stage_analysis(launches):
    from trend_analyzer import run as analysis_run
    print("\n" + "=" * 60)
    print("STAGE 4/4 — Trend Analysis")
    print("=" * 60)
    trends = analysis_run(launches)
    print(f"  ✓ Analysis complete")
    return trends


def run_full(skip_screenshot=False):
    t0 = time.time()
    print("╔══════════════════════════════════════════════╗")
    print("║   AI Launch Pipeline — One-Click Execution   ║")
    print("╚══════════════════════════════════════════════╝")

    # Stage 1
    items = stage_rss()
    if not items:
        print("\n  No new launches found. Pipeline complete.")
        return

    # Stage 2
    enriched = stage_search(items)

    # Stage 3 (optional)
    if skip_screenshot:
        print("\n  ⏭ Screenshot stage skipped")
        with_screenshots = enriched
    else:
        with_screenshots = stage_screenshot(enriched)

    # Stage 4
    stage_analysis(with_screenshots)

    elapsed = time.time() - t0
    print("\n" + "=" * 60)
    print(f"Pipeline complete in {elapsed:.1f}s")
    print(f"  Data:       {DATA_DIR}/")
    print(f"  Screenshots: {SCREENSHOT_DIR}/")
    print(f"  Analysis:   {ANALYSIS_DIR}/")
    print("=" * 60)


def run_single(stage: str):
    stages = {
        "rss": lambda: stage_rss(),
        "search": lambda: stage_search(json.load(open(os.path.join(DATA_DIR, "raw_launches.json")))),
        "screenshot": lambda: stage_screenshot(json.load(open(os.path.join(DATA_DIR, "enriched_launches.json")))),
        "analysis": lambda: stage_analysis(json.load(open(os.path.join(DATA_DIR, "enriched_launches.json")))),
    }
    if stage not in stages:
        print(f"Unknown stage: {stage}. Choose from: {', '.join(stages.keys())}")
        sys.exit(1)
    stages[stage]()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="AI Launch Pipeline — one-click execution")
    p.add_argument("--skip-screenshot", action="store_true", help="Skip screenshot capture stage")
    p.add_argument("--stage", choices=["rss", "search", "screenshot", "analysis"], help="Run a single stage only")
    args = p.parse_args()

    if args.stage:
        run_single(args.stage)
    else:
        run_full(skip_screenshot=args.skip_screenshot)
