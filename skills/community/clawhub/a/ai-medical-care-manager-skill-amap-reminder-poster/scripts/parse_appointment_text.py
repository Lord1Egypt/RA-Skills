#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

DT_PATTERNS = [
    (re.compile(r'(20\d{2})[-/.年](\d{1,2})[-/.月](\d{1,2})[日\sT]*(\d{1,2})[:：](\d{2})'), '%04d-%02d-%02d %02d:%02d'),
]


def normalize(s: str) -> str:
    if s is None:
        return ''
    s = str(s).strip()
    return '' if s.lower() == 'nan' else s


def load_candidates(csv_path: str):
    hospitals, departments, doctors = set(), set(), set()
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hospitals.add(normalize(row.get('hospital_name')))
            departments.add(normalize(row.get('department_name')))
            doctors.add(normalize(row.get('doctor_name')))
    hospitals.discard(''); departments.discard(''); doctors.discard('')
    return sorted(hospitals, key=len, reverse=True), sorted(departments, key=len, reverse=True), sorted(doctors, key=len, reverse=True)


def find_first(text: str, candidates: List[str]) -> Optional[str]:
    for item in candidates:
        if item and item in text:
            return item
    return None


def extract_datetime(text: str) -> Optional[str]:
    text = text.replace('上午', ' ').replace('下午', ' ')
    for patt, fmt in DT_PATTERNS:
        m = patt.search(text)
        if m:
            y, mo, d, h, mi = map(int, m.groups())
            return fmt % (y, mo, d, h, mi)
    return None


def main() -> int:
    p = argparse.ArgumentParser(description='Extract appointment fields from booking text or OCR text')
    p.add_argument('--csv', required=True)
    p.add_argument('--text', required=True)
    args = p.parse_args()

    hospitals, departments, doctors = load_candidates(args.csv)
    text = normalize(args.text)

    result: Dict[str, Optional[str]] = {
        'hospital_name': find_first(text, hospitals),
        'department_name': find_first(text, departments),
        'doctor_name': find_first(text, doctors),
        'appointment_datetime': extract_datetime(text),
    }
    missing = [k for k, v in result.items() if not v]
    confidence = 1.0 - (len(missing) / len(result))
    output = {
        'parsed': result,
        'missing_fields': missing,
        'confidence': round(confidence, 2),
        'note': '如字段缺失，请让用户手动补充医院、科室、医生或就诊时间。',
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
