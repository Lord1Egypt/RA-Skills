#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / 'src').resolve()))

import daily_strava_roast.cli as cli


def main() -> int:
    activities = json.loads((ROOT / 'tests' / 'fixtures' / 'sample_activities.json').read_text())
    payload = cli.build_daily_payload(activities)
    assert payload['activity_count'] == 2
    assert payload['days'][0]['rollup']['count'] == 2

    roast = cli.roast_block(activities, 'playful', 2, target_date='2026-03-27')
    assert isinstance(roast, str) and len(roast) > 40
    assert 'Lunch Run' in roast or 'Evening Tennis' in roast
    assert 'Overall:' in roast

    print('smoke test passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
