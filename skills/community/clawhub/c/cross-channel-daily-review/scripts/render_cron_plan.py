#!/usr/bin/env python3
import json
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print('usage: render_cron_plan.py <timezone>', file=sys.stderr)
        return 2
    tz = sys.argv[1]
    plan = {
        'timezone': tz,
        'jobs': [
            {'name': 'daily-review-generate', 'expr': '0 3 * * *', 'purpose': 'generate daily raw+synthesized+index'},
            {'name': 'daily-review-boss-push', 'expr': '20 3 * * *', 'purpose': 'push daily boss summary'},
            {'name': 'weekly-review-rollup', 'expr': '40 3 * * 0', 'purpose': 'generate weekly summary and update index'},
            {'name': 'monthly-review-rollup', 'expr': '50 3 1 * *', 'purpose': 'generate monthly summary and update index'},
            {'name': 'retention-archive-run', 'expr': '0 4 2 * *', 'purpose': 'run retention planner, readiness check, and archive eligible daily layer'}
        ],
        'delete_policy_default': 'disabled'
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
