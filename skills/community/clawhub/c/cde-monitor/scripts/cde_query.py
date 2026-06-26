from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Sequence

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from cde_client import CDEClient, CDEQueryError


MIN_IN_REVIEW_YEAR = 2016
MAX_IN_REVIEW_YEAR = 2026
DEFAULT_IN_REVIEW_YEARS = list(range(2016, 2027))


def _parse_in_review_year(value: str) -> int:
    try:
        year = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid year: {value}") from exc
    if year < MIN_IN_REVIEW_YEAR or year > MAX_IN_REVIEW_YEAR:
        raise argparse.ArgumentTypeError(
            f"year must be between {MIN_IN_REVIEW_YEAR} and {MAX_IN_REVIEW_YEAR}: {value}"
        )
    return year


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query live public data from the CDE website")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--show-browser", action="store_true", help="Run with a visible Chrome window")
    common.add_argument("--timeout", type=int, default=25, help="Selenium wait timeout in seconds")
    common.add_argument("--pretty", action="store_true", help="Print a compact human-readable summary")
    common.add_argument("--max-pages", type=int, default=None, help="Optional pagination cap for debugging")

    for action in common._actions:
        if action.dest == "help":
            continue
        parser._add_action(action)

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("breakthrough-announcements", parents=[common], add_help=False)

    bt_company = subparsers.add_parser("breakthrough-included-by-company", parents=[common], add_help=False)
    bt_company.add_argument("--company", required=True)

    bt_drug = subparsers.add_parser("breakthrough-included-by-drug", parents=[common], add_help=False)
    bt_drug.add_argument("--drug", required=True)

    subparsers.add_parser("priority-announcements", parents=[common], add_help=False)

    pr_company = subparsers.add_parser("priority-included-by-company", parents=[common], add_help=False)
    pr_company.add_argument("--company", required=True)

    pr_drug = subparsers.add_parser("priority-included-by-drug", parents=[common], add_help=False)
    pr_drug.add_argument("--drug", required=True)

    in_review_company = subparsers.add_parser("in-review-by-company", parents=[common], add_help=False)
    in_review_company.add_argument("--company", required=True)
    in_review_company.add_argument("--years", nargs="+", type=_parse_in_review_year, default=DEFAULT_IN_REVIEW_YEARS)

    in_review_drug = subparsers.add_parser("in-review-by-drug", parents=[common], add_help=False)
    in_review_drug.add_argument("--drug", required=True)
    in_review_drug.add_argument("--years", nargs="+", type=_parse_in_review_year, default=DEFAULT_IN_REVIEW_YEARS)

    review_status = subparsers.add_parser("review-status-by-acceptance-no", parents=[common], add_help=False)
    review_status.add_argument("--acceptance-no", required=True)

    return parser


def _pretty_print(payload: Dict[str, Any]) -> None:
    if payload.get("command") == "review-status-by-acceptance-no":
        print(f"command: {payload.get('command')}")
        print(f"acceptance_no: {payload.get('acceptance_no')}")
        print(f"inferred_year: {payload.get('inferred_year')}")
        print(f"basic_info_found: {payload.get('basic_info_found')}")
        print(f"review_status_found: {payload.get('review_status_found')}")
        basic_info = payload.get("basic_info") or {}
        if basic_info:
            print(
                f"basic_info: 药品={basic_info.get('drug_name') or 'N/A'} | 药品类型={basic_info.get('drug_type') or 'N/A'} | 申请类型={basic_info.get('application_type') or 'N/A'}"
            )
        review_status = payload.get("review_status") or {}
        if review_status:
            print(
                f"review_status: 状态={review_status.get('review_state') or 'N/A'} | 进入中心时间={review_status.get('entered_center_at') or 'N/A'}"
            )
            for stage, details in (review_status.get("stages") or {}).items():
                print(f"  - {stage}: {details.get('label')}")
        return

    metadata = payload.get("metadata", {})
    print(f"command: {payload.get('command')}")
    print(f"total_records: {metadata.get('total_records', 0)}")
    print(f"pages_visited: {metadata.get('pages_visited', 0)}")
    years = metadata.get("years_queried") or []
    if years:
        print(f"years_queried: {', '.join(str(year) for year in years)}")
    filters = metadata.get("applied_filters") or {}
    if filters:
        print(f"applied_filters: {json.dumps(filters, ensure_ascii=False)}")
    for index, record in enumerate(payload.get("records", [])[:10], start=1):
        normalized = record.get("normalized", {})
        print(
            f"{index}. 药品={normalized.get('drug_name') or 'N/A'} | 企业={normalized.get('company_name') or 'N/A'} | 受理号={normalized.get('acceptance_no') or 'N/A'}"
        )


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    client = CDEClient(headless=not args.show_browser, timeout=args.timeout, max_pages=args.max_pages)
    try:
        if args.command == "breakthrough-announcements":
            payload = client.query_breakthrough_announcements()
        elif args.command == "breakthrough-included-by-company":
            payload = client.query_breakthrough_included_by_company(args.company)
        elif args.command == "breakthrough-included-by-drug":
            payload = client.query_breakthrough_included_by_drug(args.drug)
        elif args.command == "priority-announcements":
            payload = client.query_priority_announcements()
        elif args.command == "priority-included-by-company":
            payload = client.query_priority_included_by_company(args.company)
        elif args.command == "priority-included-by-drug":
            payload = client.query_priority_included_by_drug(args.drug)
        elif args.command == "in-review-by-company":
            payload = client.query_in_review_by_company(args.company, args.years)
        elif args.command == "in-review-by-drug":
            payload = client.query_in_review_by_drug(args.drug, args.years)
        elif args.command == "review-status-by-acceptance-no":
            payload = client.query_review_status_by_acceptance_no(args.acceptance_no)
        else:
            parser.error(f"Unsupported command: {args.command}")
            return 2
    except CDEQueryError as exc:
        print(
            json.dumps(
                {"ok": False, "error": str(exc), "command": getattr(args, "command", None)},
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1

    if args.pretty:
        _pretty_print(payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())