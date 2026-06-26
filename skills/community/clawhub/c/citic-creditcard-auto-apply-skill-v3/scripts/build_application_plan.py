#!/usr/bin/env python3
"""Build a safe prefill execution plan for the CITIC credit-card auto-apply skill.

This script does not control the browser. It prepares a JSON plan for the agent:
- candidate fields extracted from workspace files
- recommended card and official apply URL
- confirmed/required/blocked actions
- stop conditions before final submission
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit("缺少 PyYAML，请先安装 requirements.txt") from exc

from profile_extractor import build_candidates  # type: ignore
from citic_cc_advisor import recommend_json  # type: ignore

ROOT = Path(__file__).resolve().parents[1]


def load_profile(workspace: Path) -> Dict[str, Any]:
    profile_path = workspace / 'profiles' / 'applicant_profile.json'
    if not profile_path.exists():
        profile_path = workspace / 'profiles' / 'applicant_profile.template.json'
    if not profile_path.exists():
        return {}
    return json.loads(profile_path.read_text(encoding='utf-8'))


def load_workflow(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding='utf-8')) or {}


def main() -> None:
    parser = argparse.ArgumentParser(description='Build a safe browser prefill plan JSON')
    parser.add_argument('--workspace', default='.', help='Workspace root')
    parser.add_argument('--workflow', default='config/workflow.template.yaml', help='Workflow YAML path')
    parser.add_argument('--out', default='output/application_plan.json', help='Output JSON path')
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    workflow_path = workspace / args.workflow if not Path(args.workflow).is_absolute() else Path(args.workflow)
    out_path = workspace / args.out if not Path(args.out).is_absolute() else Path(args.out)

    workflow = load_workflow(workflow_path)
    profile = load_profile(workspace)
    recommendation = recommend_json(profile) if profile else {"top_cards": [], "recommended_card_slug": None}
    candidates = [c.__dict__ for c in build_candidates(workspace)]

    top_cards: List[Dict[str, Any]] = recommendation.get('top_cards', [])
    recommended = top_cards[0] if top_cards else {}

    plan = {
        'workflow_name': workflow.get('name'),
        'workspace': str(workspace),
        'browser_profile_default': (workflow.get('profiles') or {}).get('browser_profile_default', 'openclaw'),
        'browser_profile_existing_session': (workflow.get('profiles') or {}).get('browser_profile_existing_session', 'user'),
        'recommended_card': recommended,
        'backup_cards': top_cards[1:3],
        'candidate_fields': candidates,
        'confirmed_fields_required': [
            'full_name', 'phone', 'id_type', 'city', 'employer_name', 'monthly_income'
        ],
        'safe_prefill_fields': [
            'full_name', 'gender', 'birth_date', 'phone', 'email', 'city', 'residential_address',
            'mailing_address', 'employer_name', 'employer_city', 'job_title', 'education', 'monthly_income',
            'housing_status'
        ],
        'never_autofill_without_user_live_confirmation': [
            'id_number', 'sms_code', 'otp', 'face_verification', 'signature', 'agreement_consent', 'credit_authorization'
        ],
        'browser_sequence': [
            'open official page',
            'snapshot page refs',
            'open official apply page',
            'snapshot form refs',
            'type/select only confirmed fields',
            'stop before OTP / agreement / final submit'
        ],
        'stop_conditions': [
            'captcha shown',
            'otp or sms verification shown',
            'credit authorization or agreement shown',
            'final submit button shown',
            'required field missing or conflicting'
        ],
        'warning': 'This plan is for browser-assisted prefill only. The customer must review and complete the final submission personally.'
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
