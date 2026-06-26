#!/usr/bin/env python3
"""Build local WHO weight-for-age LMS CSV from official WHO Excel files.

Downloads from WHO are intentionally not embedded in the skill; store them under
the baby-tracker data directory's `who/` folder, then run this script to create
`who_weight_lms.csv`.
"""
from __future__ import annotations

import argparse
import csv
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

DEFAULT_DATA_DIR = Path(os.environ.get("BABY_TRACKER_DIR", Path.home() / ".openclaw" / "workspace" / "data" / "baby-tracker"))
DEFAULT_WHO_DIR = DEFAULT_DATA_DIR / 'who'
DEFAULT_OUT = DEFAULT_WHO_DIR / 'who_weight_lms.csv'
NS = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

FILES = [
    ('female', 'week', DEFAULT_WHO_DIR / 'girls_0_13_weeks.xlsx', 7.0, 'WHO weight-for-age girls 0-13 weeks z-scores/LMS'),
    ('male', 'week', DEFAULT_WHO_DIR / 'boys_0_13_weeks.xlsx', 7.0, 'WHO weight-for-age boys 0-13 weeks z-scores/LMS'),
    ('female', 'month', DEFAULT_WHO_DIR / 'girls_0_5_years.xlsx', 365.25/12, 'WHO weight-for-age girls 0-5 years z-scores/LMS'),
    ('male', 'month', DEFAULT_WHO_DIR / 'boys_0_5_years.xlsx', 365.25/12, 'WHO weight-for-age boys 0-5 years z-scores/LMS'),
]


def shared_strings(z: ZipFile) -> list[str]:
    root = ET.fromstring(z.read('xl/sharedStrings.xml'))
    out = []
    for si in root.findall('x:si', NS):
        out.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['x'])))
    return out


def cell_value(c, strings):
    v = c.find('x:v', NS)
    if v is None:
        return ''
    text = v.text or ''
    if c.attrib.get('t') == 's':
        return strings[int(text)]
    try:
        return float(text)
    except ValueError:
        return text


def read_xlsx(path: Path) -> list[dict]:
    with ZipFile(path) as z:
        strings = shared_strings(z)
        root = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        rows = []
        for row in root.findall('.//x:sheetData/x:row', NS):
            vals = []
            for c in row.findall('x:c', NS):
                vals.append(cell_value(c, strings))
            if vals:
                rows.append(vals)
    headers = [str(x) for x in rows[0]]
    return [dict(zip(headers, row)) for row in rows[1:]]


def build(out: Path, who_dir: Path = DEFAULT_WHO_DIR) -> int:
    records = []
    for sex, unit_name, path, multiplier, source in FILES:
        path = who_dir / path.name
        for row in read_xlsx(path):
            age_value = float(row['Week' if unit_name == 'week' else 'Month'])
            records.append({
                'sex': sex,
                'age_unit': unit_name,
                'age_value': f'{age_value:g}',
                'age_days': f'{age_value * multiplier:.6f}',
                'L': f"{float(row['L']):.12g}",
                'M': f"{float(row['M']):.12g}",
                'S': f"{float(row['S']):.12g}",
                'sd3neg': f"{float(row['SD3neg']):.12g}",
                'sd2neg': f"{float(row['SD2neg']):.12g}",
                'sd1neg': f"{float(row['SD1neg']):.12g}",
                'sd0': f"{float(row['SD0']):.12g}",
                'sd1': f"{float(row['SD1']):.12g}",
                'sd2': f"{float(row['SD2']):.12g}",
                'sd3': f"{float(row['SD3']):.12g}",
                'unit': 'kg',
                'source': source,
            })
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', newline='', encoding='utf-8') as f:
        fields = ['sex','age_unit','age_value','age_days','L','M','S','sd3neg','sd2neg','sd1neg','sd0','sd1','sd2','sd3','unit','source']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(records)
    print(out)
    print(f'rows={len(records)}')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--who-dir', type=Path, default=DEFAULT_WHO_DIR)
    ap.add_argument('--output', type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    return build(args.output, args.who_dir)

if __name__ == '__main__':
    raise SystemExit(main())
