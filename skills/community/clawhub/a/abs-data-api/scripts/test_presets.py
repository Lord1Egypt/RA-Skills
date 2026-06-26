#!/usr/bin/env python3
"""
test_presets.py — Validate that each preset returns live data from the ABS API.

Iterates over all presets in presets.json, fetches the latest observation,
and reports pass/fail for each.

Usage:
    python3 scripts/test_presets.py
    python3 scripts/test_presets.py --preset cpi-annual-change   # single preset
    python3 scripts/test_presets.py --verbose                    # show values

Uses stdlib only.
"""

import json
import sys
import time
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
PRESETS_FILE = SKILL_DIR / "presets.json"
BASE_URL = "https://data.api.abs.gov.au/rest"


def _get_version_from_presets(dataflow_id: str, all_presets: dict) -> str:
    """Look up version from any preset using this dataflow, else default 1.0.0."""
    cache_dir = Path.home() / ".cache" / "abs-data-api"
    meta_file = cache_dir / "metadata.generated.json"
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text())
            v = meta.get(dataflow_id, {}).get("version")
            if v:
                return v
        except Exception:
            pass
    catalog_file = cache_dir / "catalog.json"
    if catalog_file.exists():
        try:
            catalog = json.loads(catalog_file.read_text())
            v = catalog.get(dataflow_id, {}).get("version")
            if v:
                return v
        except Exception:
            pass
    return "1.0.0"


def fetch_latest(dataflow_id: str, key: str, version: str) -> tuple:
    """
    Fetch latest observation for a dataflow/key.
    Returns (success: bool, value, period, error_msg)
    """
    if not key or key.lower() == "all":
        key = "all"
    url = (
        f"{BASE_URL}/data/ABS,{dataflow_id},{version}/{key}"
        f"?dimensionAtObservation=TIME_PERIOD&lastNObservations=1"
    )
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())

        datasets = data.get("dataSets", [])
        if not datasets:
            return False, None, None, "No dataSets in response"

        dataset = datasets[0]
        value = None
        period = None

        # Series format
        if "series" in dataset:
            for series_key, series_data in dataset["series"].items():
                obs = series_data.get("observations", {})
                for obs_key, obs_vals in obs.items():
                    if obs_vals and obs_vals[0] is not None:
                        value = obs_vals[0]
                        # Get period from structure
                        try:
                            obs_dims = data.get("structure", {}).get("dimensions", {}).get("observation", [])
                            tp_dim = next((d for d in obs_dims if d.get("id") == "TIME_PERIOD"), None)
                            if tp_dim:
                                idx = int(obs_key)
                                period = tp_dim["values"][idx]["id"] if idx < len(tp_dim["values"]) else obs_key
                        except Exception:
                            period = obs_key
                        break
                if value is not None:
                    break

        # AllDimensions format
        elif "observations" in dataset:
            for obs_key, obs_vals in dataset["observations"].items():
                if obs_vals and obs_vals[0] is not None:
                    value = obs_vals[0]
                    break

        if value is None:
            return False, None, None, "No non-null observations found"

        return True, value, period, None

    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:200]
        return False, None, None, f"HTTP {e.code}: {body}"
    except Exception as e:
        return False, None, None, str(e)


def run_tests(target_preset: str = None, verbose: bool = False) -> int:
    """Run preset validation. Returns exit code (0=all pass, 1=some fail)."""
    if not PRESETS_FILE.exists():
        print(f"ERROR: presets.json not found at {PRESETS_FILE}")
        return 1

    try:
        presets = json.loads(PRESETS_FILE.read_text())
    except Exception as e:
        print(f"ERROR: could not parse presets.json: {e}")
        return 1

    if target_preset:
        if target_preset not in presets:
            print(f"ERROR: preset '{target_preset}' not found")
            print(f"Available: {', '.join(presets.keys())}")
            return 1
        presets = {target_preset: presets[target_preset]}

    total = len(presets)
    passed = 0
    failed = 0
    results = []

    print(f"Testing {total} preset(s) against live ABS API ...\n")

    for name, preset in presets.items():
        dataflow_id = preset.get("dataflow", "")
        key = preset.get("key", "all")
        version = _get_version_from_presets(dataflow_id, presets)

        # Get version from preset note if available
        note = preset.get("note", "")
        desc = preset.get("description", "")

        start = time.time()
        ok, value, period, error = fetch_latest(dataflow_id, key, version)
        elapsed = time.time() - start

        if ok:
            passed += 1
            status = "PASS"
            detail = f"{value} ({period})" if period else str(value)
            if verbose:
                detail += f"  [{elapsed:.1f}s]"
        else:
            failed += 1
            status = "FAIL"
            detail = error or "unknown error"

        pad = max(0, 36 - len(name))
        print(f"  [{status}]  {name}{' ' * pad}  {detail}")
        results.append({"preset": name, "status": status, "detail": detail})

    print()
    print(f"{'─' * 50}")
    print(f"Results: {passed}/{total} passed, {failed} failed")

    if failed > 0:
        print()
        print("Failed presets:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  - {r['preset']}: {r['detail']}")
        return 1

    return 0


def main():
    args = sys.argv[1:]
    target_preset = None
    verbose = False

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--preset" and i + 1 < len(args):
            target_preset = args[i + 1]
            i += 2
        elif a == "--verbose":
            verbose = True
            i += 1
        elif a in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            i += 1

    exit_code = run_tests(target_preset=target_preset, verbose=verbose)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
