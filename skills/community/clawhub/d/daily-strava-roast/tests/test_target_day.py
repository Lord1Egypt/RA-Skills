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
    daily = cli.build_daily_payload(activities)

    target_day = cli.select_target_day(daily, '2026-03-28')
    assert target_day is None

    empty_day = cli.build_empty_day('2026-03-28')
    assert empty_day['date'] == '2026-03-28'
    assert empty_day['count'] == 0

    roast = cli.roast_block(activities, 'playful', 3, target_date='2026-03-28')
    assert 'No Strava activity today' in roast

    last_activity = cli.find_last_activity(activities, '2026-03-28')
    assert last_activity is not None
    assert last_activity['name'] in {'Evening Tennis', 'Lunch Run'}

    print('target day test passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
