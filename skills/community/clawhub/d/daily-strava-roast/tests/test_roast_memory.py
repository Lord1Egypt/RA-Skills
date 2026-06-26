#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str((ROOT / 'src').resolve()))

from daily_strava_roast.context_builder import build_roast_context
from daily_strava_roast.prompt_builder import build_roast_prompt


def main() -> int:
    day = {
        'date': '2026-03-29',
        'count': 1,
        'sports': ['Ride'],
        'names': ['Morning Ride'],
        'total_km': 56.95,
        'total_min': 150,
        'total_elev': 733,
        'total_kudos': 11,
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
            }
        ],
    }
    state = {
        'recent': [
            {
                'date': '2026-03-27',
                'sports': ['Ride'],
                'count': 1,
                'distance_km': 40.0,
                'moving_minutes': 110,
                'elevation_m': 500,
                'activity_names': ['Tempo Ride'],
                'dominant_sport': 'ride',
                'joke_family': 'naming-joke',
                'opening_style': 'name-based opener',
                'joke_targets': ['bland workout naming', 'public validation'],
            },
            {
                'date': '2026-03-28',
                'sports': ['Ride'],
                'count': 1,
                'distance_km': 42.0,
                'moving_minutes': 120,
                'elevation_m': 520,
                'activity_names': ['Morning Ride'],
                'dominant_sport': 'ride',
                'joke_family': 'kudos-joke',
                'opening_style': 'direct stat opener',
                'joke_targets': ['self-inflicted inconvenience'],
            },
        ]
    }
    context = build_roast_context(day, 'playful', 3, state)
    prompt = build_roast_prompt(context)
    assert context['roast_memory']['recent_families'] == ['naming-joke', 'kudos-joke']
    assert context['pattern_hints']['consecutive_same_sport_days'] == 2
    assert context['recent_activity_context']['last_day']['activity_names'] == ['Morning Ride']
    assert context['pattern_hints']['recent_load']['distance_vs_recent'] in {'above_recent', 'well_above_recent'}
    assert 'recent_joke_families_to_avoid: naming-joke, kudos-joke' in prompt
    assert 'recent_opening_styles_to_avoid: name-based opener, direct stat opener' in prompt
    assert 'Avoid repeating recent joke families, opening styles, and joke targets' in prompt
    assert 'When helpful, reference recent training context like repeated sport days' in prompt
    print('roast memory test passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
