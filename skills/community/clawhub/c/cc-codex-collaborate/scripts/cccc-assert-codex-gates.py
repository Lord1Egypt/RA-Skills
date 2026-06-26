#!/usr/bin/env python3
"""
Assert Codex gate conditions before proceeding.

Usage:
  cccc-assert-codex-gates.py assert-plan-approved
  cccc-assert-codex-gates.py assert-milestone-approved
  cccc-assert-codex-gates.py assert-final-approved

Each assertion fails closed - returns non-zero if conditions not met.
"""
import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def assert_plan_approved(state_path: Path) -> bool:
    """Assert Codex plan review has passed."""
    state = load_json(state_path)

    plan_status = state.get('codex_plan_review_status', 'not_run')
    roadmap_status = state.get('roadmap_status', 'not_reviewed')
    review_file = state.get('last_codex_plan_review_file')

    if plan_status != 'pass':
        print("ERROR: Codex plan review is required before implementation.", file=sys.stderr)
        print(f"  codex_plan_review_status = {plan_status} (expected: pass)", file=sys.stderr)
        return False

    if roadmap_status != 'codex_approved':
        print("ERROR: Roadmap must be codex_approved before implementation.", file=sys.stderr)
        print(f"  roadmap_status = {roadmap_status} (expected: codex_approved)", file=sys.stderr)
        return False

    if review_file and Path(review_file).exists():
        return True
    else:
        print("ERROR: Codex plan review file missing.", file=sys.stderr)
        print(f"  last_codex_plan_review_file = {review_file}", file=sys.stderr)
        return False


def assert_milestone_approved(state_path: Path) -> bool:
    """Assert current milestone has passed Codex review."""
    state = load_json(state_path)

    milestone_id = state.get('current_milestone_id')
    if not milestone_id:
        print("ERROR: No current milestone set.", file=sys.stderr)
        return False

    review_status = state.get('current_milestone_codex_review_status', 'not_run')
    review_file = state.get('current_milestone_codex_review_file')

    if review_status != 'pass':
        print("ERROR: Codex milestone review is required before marking milestone passed.", file=sys.stderr)
        print(f"  milestone = {milestone_id}", file=sys.stderr)
        print(f"  codex_review_status = {review_status} (expected: pass)", file=sys.stderr)
        return False

    if review_file and Path(review_file).exists():
        # Verify the review file contains status = pass
        try:
            review_data = json.loads(Path(review_file).read_text())
            file_status = review_data.get('status', 'unknown')
            if file_status != 'pass':
                print(f"ERROR: Review file status = {file_status}, expected pass.", file=sys.stderr)
                return False
        except Exception as e:
            print(f"ERROR: Cannot read review file: {e}", file=sys.stderr)
            return False
        return True
    else:
        print("ERROR: Codex milestone review file missing.", file=sys.stderr)
        print(f"  codex_review_file = {review_file}", file=sys.stderr)
        return False


def assert_final_approved(state_path: Path) -> bool:
    """Assert Codex final review has passed."""
    state = load_json(state_path)

    final_status = state.get('codex_final_review_status', 'not_run')
    review_file = state.get('last_codex_final_review_file')

    if final_status != 'pass':
        print("ERROR: Codex final review is required before marking task completed.", file=sys.stderr)
        print(f"  codex_final_review_status = {final_status} (expected: pass)", file=sys.stderr)
        return False

    if review_file and Path(review_file).exists():
        return True
    else:
        print("ERROR: Codex final review file missing.", file=sys.stderr)
        print(f"  last_codex_final_review_file = {review_file}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Assert Codex gate conditions")
    parser.add_argument('command', choices=[
        'assert-plan-approved',
        'assert-milestone-approved',
        'assert-final-approved'
    ])
    parser.add_argument('--state', default='docs/cccc/state.json')
    args = parser.parse_args()

    state_path = Path(args.state)

    if not state_path.exists():
        print(f"ERROR: State file missing: {state_path}", file=sys.stderr)
        sys.exit(1)

    success = False
    if args.command == 'assert-plan-approved':
        success = assert_plan_approved(state_path)
    elif args.command == 'assert-milestone-approved':
        success = assert_milestone_approved(state_path)
    elif args.command == 'assert-final-approved':
        success = assert_final_approved(state_path)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()