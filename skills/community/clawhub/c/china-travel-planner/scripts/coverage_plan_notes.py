#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, List


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate simple line-coverage planning notes from subway JSON.")
    parser.add_argument("--subway", required=True, help="Path to subway JSON from fetch_subway_data.py")
    parser.add_argument("--hotel-station", help="Anchor station, e.g. 黄土岭")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        with open(args.subway, 'r', encoding='utf-8') as f:
            data = json.load(f)

        lines = data.get('lines', [])
        notes: List[Dict[str, Any]] = []
        for line in lines:
            stations = line.get('stations', [])
            station_names = [s['name'] if isinstance(s, dict) else str(s) for s in stations]
            anchor_on_line = args.hotel_station in station_names if args.hotel_station else False
            notes.append({
                'line': line.get('name', ''),
                'station_count': line.get('station_count', len(station_names)),
                'hotel_anchor_on_line': anchor_on_line,
                'suggested_use': (
                    '可作为酒店出发/回程主线' if anchor_on_line else '适合与周边景点或跨城出行顺路覆盖'
                ),
                'sample_boarding': station_names[:2],
                'sample_alighting': station_names[-2:] if len(station_names) >= 2 else station_names,
            })

        result = {
            'city': data.get('city'),
            'hotel_station': args.hotel_station,
            'line_count': len(notes),
            'coverage_notes': notes,
        }
        if args.pretty:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
