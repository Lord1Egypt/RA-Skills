#!/usr/bin/env python3
"""Extract candidate credit-card application fields from an OpenClaw workspace.

Safety model:
- Prefer structured JSON in profiles/applicant_profile.json
- Then read USER.md / MEMORY.md / memory/*.md for candidate values
- Treat extracted values as candidates only; never auto-submit based on them
- Avoid guessing sensitive values that are not explicitly present
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

FIELD_PATTERNS = {
    "full_name": [r"(?:姓名|名字|name)[:：]\s*(.+)"],
    "gender": [r"(?:性别|gender)[:：]\s*(男|女|male|female)"],
    "birth_date": [r"(?:出生日期|生日|birth(?:\s+date)?)[:：]\s*([0-9]{4}[-/.年][0-9]{1,2}[-/.月][0-9]{1,2}日?)"],
    "phone": [r"(?:手机号|手机|联系电话|phone)[:：]\s*(1[3-9]\d{9})"],
    "email": [r"(?:邮箱|电子邮箱|email)[:：]\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})"],
    "city": [r"(?:城市|所在城市|city)[:：]\s*(.+)"],
    "residential_address": [r"(?:居住地址|住宅地址|家庭住址|address)[:：]\s*(.+)"],
    "mailing_address": [r"(?:邮寄地址|通讯地址)[:：]\s*(.+)"],
    "employer_name": [r"(?:工作单位|单位名称|公司名称|employer)[:：]\s*(.+)"],
    "employer_city": [r"(?:单位城市|工作城市)[:：]\s*(.+)"],
    "job_title": [r"(?:职位|岗位|职务|job\s*title)[:：]\s*(.+)"],
    "education": [r"(?:学历|education)[:：]\s*(.+)"],
    "monthly_income": [r"(?:月收入|税前月薪|income)[:：]\s*(.+)"],
    "housing_status": [r"(?:住房情况|居住情况)[:：]\s*(.+)"],
    # Full ID number is intentionally only accepted from structured JSON, not free-text memory.
    "id_last4": [r"(?:身份证后四位|证件号后四位)[:：]\s*(\d{4}|[0-9Xx]{4})"],
}

PREFERRED_JSON = Path('profiles/applicant_profile.json')
TEMPLATE_JSON = Path('profiles/applicant_profile.template.json')

@dataclass
class Candidate:
    field: str
    value: str
    source: str
    confidence: str
    masked_preview: str


def mask_value(field: str, value: str) -> str:
    v = value.strip()
    if not v:
        return v
    if field == 'phone' and len(v) >= 7:
        return v[:3] + '****' + v[-4:]
    if field == 'email' and '@' in v:
        name, domain = v.split('@', 1)
        head = name[:2] if len(name) >= 2 else name[:1]
        return head + '***@' + domain
    if field in {'residential_address', 'mailing_address'} and len(v) > 8:
        return v[:6] + '***' + v[-2:]
    if field == 'full_name' and len(v) >= 2:
        return v[0] + '*' * (len(v)-1)
    return v


def load_json_profile(workspace: Path) -> Dict[str, str]:
    for rel in (PREFERRED_JSON, TEMPLATE_JSON):
        p = workspace / rel
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding='utf-8'))
                if isinstance(data, dict):
                    return data
            except Exception:
                pass
    return {}


def scan_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''


def collect_text_sources(workspace: Path) -> List[tuple[str, str]]:
    files: List[tuple[str, str]] = []
    for rel in ('USER.md', 'MEMORY.md'):
        p = workspace / rel
        if p.exists():
            files.append((rel, scan_text_file(p)))
    mem_dir = workspace / 'memory'
    if mem_dir.exists():
        for p in sorted(mem_dir.glob('*.md')):
            files.append((str(p.relative_to(workspace)), scan_text_file(p)))
    return files


def extract_from_text(field: str, text: str) -> Optional[str]:
    for pattern in FIELD_PATTERNS.get(field, []):
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            val = m.group(1).strip()
            val = re.sub(r'\s+$', '', val)
            return val
    return None


def build_candidates(workspace: Path) -> List[Candidate]:
    candidates: List[Candidate] = []
    json_profile = load_json_profile(workspace)

    # Structured JSON is preferred and can include high-sensitivity fields explicitly provided by the user.
    for field, value in json_profile.items():
        if value in ('', None, [], {}):
            continue
        if field.startswith('consent_') or field == 'notes':
            continue
        if isinstance(value, (list, dict, bool, int, float)):
            value_str = json.dumps(value, ensure_ascii=False)
        else:
            value_str = str(value)
        candidates.append(Candidate(
            field=field,
            value=value_str,
            source='profiles/applicant_profile.json or template',
            confidence='high',
            masked_preview=mask_value(field, value_str),
        ))

    existing_fields = {c.field for c in candidates}
    for source_name, text in collect_text_sources(workspace):
        for field in FIELD_PATTERNS:
            if field in existing_fields:
                continue
            extracted = extract_from_text(field, text)
            if extracted:
                candidates.append(Candidate(
                    field=field,
                    value=extracted,
                    source=source_name,
                    confidence='medium',
                    masked_preview=mask_value(field, extracted),
                ))
                existing_fields.add(field)
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract candidate applicant profile fields from OpenClaw workspace files.')
    parser.add_argument('--workspace', default='.', help='Path to the OpenClaw workspace root')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of markdown-like text')
    parser.add_argument('--out', help='Optional path to write the JSON payload')
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    candidates = build_candidates(workspace)
    payload = {
        'workspace': str(workspace),
        'warning': 'Candidates only. Confirm every field with the user before filling the official application form. Do not auto-submit.',
        'candidates': [asdict(c) for c in candidates],
    }

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print('# 候选申请资料（待确认）')
    print()
    print(payload['warning'])
    print()
    for item in payload['candidates']:
        print(f"- {item['field']}: {item['masked_preview']}  [source={item['source']}; confidence={item['confidence']}]")


if __name__ == '__main__':
    main()
