from __future__ import annotations

import argparse

from ahtv_pk_lib import (
    AhtvClient,
    make_json_ready,
    parse_date_expression,
    resolve_dates,
    resolve_latest_date,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date-expr", required=True, help="User-provided 快乐无敌大PK date expression.")
    parser.add_argument(
        "--latest-date",
        help="Optional YYYY-MM-DD override for open ranges. Defaults to the latest discoverable AHTV episode date.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    client = AhtvClient()
    latest_date = resolve_latest_date(args.latest_date, client=client)
    parse_result = parse_date_expression(args.date_expr, latest_date=latest_date)

    payload = {
        "input_expr": args.date_expr,
        "mode": parse_result.mode,
        "latest_available_date": parse_result.latest_available_date,
        "expanded_dates": parse_result.normalized_dates,
        "parse_errors": parse_result.errors,
    }

    if parse_result.normalized_dates:
        payload.update(resolve_dates(parse_result.normalized_dates, client=client))
    else:
        payload.update(
            {
                "summary": {
                    "total": 0,
                    "ready": 0,
                    "not_found": 0,
                    "ambiguous": 0,
                    "video_url_missing": 0,
                    "error": 0,
                },
                "items": [],
            }
        )

    print(make_json_ready(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
