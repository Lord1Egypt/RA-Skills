#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / 'src').resolve()))

import daily_strava_roast.cli as cli


def main() -> int:
    day = {
        'date': '2026-03-29',
        'count': 2,
        'sports': ['Ride', 'Tennis'],
        'names': ['Morning Ride', 'Evening Tennis'],
        'total_km': 60.5,
        'total_min': 190,
        'total_elev': 733,
        'total_kudos': 14,
        'indoor_count': 0,
        'summaries': [
            {
                'name': 'Morning Ride',
                'sport': 'Ride',
                'distance_km': 56.95,
                'moving_min': 150,
                'elev_m': 733,
                'kudos': 11,
                'avg_hr': 147,
                'max_hr': 189,
                'trainer': False,
            },
            {
                'name': 'Evening Tennis',
                'sport': 'Tennis',
                'distance_km': 3.55,
                'moving_min': 40,
                'elev_m': 0,
                'kudos': 3,
                'avg_hr': None,
                'max_hr': None,
                'trainer': False,
            },
        ],
    }

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'recent_roasts.json'
        cli.record_roast_state(path, day, 'playful', 3, 'Sample roast text', metadata={'joke_family': 'load-joke'})
        payload = json.loads(path.read_text())
        assert 'recent' in payload
        assert len(payload['recent']) == 1
        entry = payload['recent'][0]
        assert entry['date'] == '2026-03-29'
        assert entry['sports'] == ['Ride', 'Tennis']
        assert entry['distance_km'] == 60.5
        assert entry['moving_minutes'] == 190
        assert entry['elevation_m'] == 733
        assert entry['activity_names'] == ['Morning Ride', 'Evening Tennis']
        assert entry['dominant_sport'] == 'ride'
        assert entry['joke_family'] == 'load-joke'
        assert entry['roast'] == 'Sample roast text'

    print('roast state persistence test passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
