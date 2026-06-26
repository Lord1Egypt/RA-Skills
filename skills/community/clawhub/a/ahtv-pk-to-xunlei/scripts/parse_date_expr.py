from __future__ import annotations

from ahtv_pk_lib import AhtvClient, make_json_ready, parse_args, parse_date_expression, resolve_latest_date


def main() -> int:
    args = parse_args()
    client = AhtvClient()
    latest_date = resolve_latest_date(args.latest_date, client=client)
    result = parse_date_expression(args.date_expr, latest_date=latest_date)
    print(make_json_ready(result.__dict__))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
