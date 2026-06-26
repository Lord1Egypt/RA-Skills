#!/usr/bin/env python3
import argparse
import json
import os
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def load_local_env() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or os.getenv(key):
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ[key] = value


def env_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"missing environment variable: {name}")
    return value


def build_base_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "X-API-Key": env_required("FLIGHT_SCOUT_API_KEY"),
    }


def parse_quota_headers(headers) -> dict:
    mapping = {
        "plan_code": ("X-Flight-Scout-Plan-Code", "string"),
        "status": ("X-Flight-Scout-Quota-Status", "string"),
        "used_units": ("X-Flight-Scout-Quota-Used-Units", "int"),
        "included_units": ("X-Flight-Scout-Quota-Included-Units", "int"),
        "remaining_units": ("X-Flight-Scout-Quota-Remaining-Units", "int"),
        "overage_units": ("X-Flight-Scout-Quota-Overage-Units", "int"),
        "window_started_at": ("X-Flight-Scout-Quota-Window-Start", "string"),
        "window_ends_at": ("X-Flight-Scout-Quota-Window-End", "string"),
        "limit_enforced": ("X-Flight-Scout-Quota-Limit-Enforced", "bool"),
        "usage_billing_enabled": ("X-Flight-Scout-Quota-Usage-Billing-Enabled", "bool"),
    }
    quota = {}
    for key, (header_name, value_type) in mapping.items():
        raw_value = headers.get(header_name)
        if raw_value in {None, ""}:
            continue
        if value_type == "int":
            try:
                quota[key] = int(raw_value)
            except (TypeError, ValueError):
                continue
        elif value_type == "bool":
            quota[key] = str(raw_value).strip().lower() == "true"
        else:
            quota[key] = str(raw_value)
    return quota


def normalize_api_payload(payload: dict | None, *, status_code: int, headers) -> dict:
    envelope = dict(payload or {})
    meta = dict(envelope.get("meta") or {})
    quota = parse_quota_headers(headers)
    if quota:
        merged_quota = dict(quota)
        if isinstance(meta.get("quota"), dict):
            merged_quota.update(meta["quota"])
        meta["quota"] = merged_quota
    meta.setdefault("http_status", status_code)
    return {
        "request_id": str(envelope.get("request_id") or headers.get("X-Request-ID") or ""),
        "data": envelope.get("data"),
        "meta": meta,
        "error": envelope.get("error"),
    }


def parse_json_envelope(raw: str, *, status_code: int, headers) -> dict | None:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return normalize_api_payload(payload, status_code=status_code, headers=headers)


def request_json(method: str, path: str, *, body: dict | None = None, query: dict | None = None, idempotency_key: str | None = None) -> dict:
    base_url = env_required("FLIGHT_SCOUT_API_BASE_URL").rstrip("/")
    timeout = int(os.getenv("FLIGHT_SCOUT_API_TIMEOUT_SECONDS", "30"))
    url = f"{base_url}{path}"
    if query:
        url = f"{url}?{urlencode(query)}"
    headers = build_base_headers()
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            parsed = parse_json_envelope(raw, status_code=getattr(resp, "status", 200), headers=resp.headers)
            if parsed is not None:
                return parsed
            return {
                "request_id": str(resp.headers.get("X-Request-ID") or ""),
                "data": raw,
                "meta": {"http_status": getattr(resp, "status", 200)},
                "error": None,
            }
    except HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        parsed = parse_json_envelope(payload, status_code=exc.code, headers=exc.headers)
        if parsed is not None:
            return parsed
        return {
            "request_id": str(exc.headers.get("X-Request-ID") or ""),
            "data": None,
            "meta": {"http_status": exc.code},
            "error": {
                "code": "http_error",
                "message": payload,
            },
        }
    except URLError as exc:
        return {
            "request_id": "",
            "data": None,
            "meta": {},
            "error": {
                "code": "network_error",
                "message": str(exc),
            },
        }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="flight-scout-call")
    sub = p.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search")
    search.add_argument("--from", dest="origin", required=True)
    search.add_argument("--to", dest="destination", required=True)
    search.add_argument("--date", required=True)
    search.add_argument("--return-date")
    search.add_argument("--passengers", type=int, default=1)
    search.add_argument("--cabin-class", default="economy")
    search.add_argument("--sort-by", default="best")
    search.add_argument("--locale", default="zh-CN")
    search.add_argument("--with-booking-summary", action="store_true")
    search.add_argument("--booking-summary-limit", type=int, default=0)

    calendar = sub.add_parser("calendar")
    calendar.add_argument("--from", dest="origin", required=True)
    calendar.add_argument("--to", dest="destination", required=True)
    calendar.add_argument("--date-start", required=True)
    calendar.add_argument("--date-end", required=True)
    calendar.add_argument("--passengers", type=int, default=1)
    calendar.add_argument("--cabin-class", default="economy")
    calendar.add_argument("--locale", default="zh-HK")
    calendar.add_argument("--currency", default="CNY")
    calendar.add_argument("--window-days", dest="window_days", type=int, default=30)

    airport_search = sub.add_parser("airport-search")
    airport_search.add_argument("--query", required=True)
    airport_search.add_argument("--locale", default="zh-CN")

    hidden_sync = sub.add_parser("hidden-city-sync")
    hidden_sync.add_argument("--from", dest="origin", required=True)
    hidden_sync.add_argument("--to", dest="destination", required=True)
    hidden_sync.add_argument("--date", required=True)
    hidden_sync.add_argument("--passengers", type=int, default=1)
    hidden_sync.add_argument("--cabin-class", default="economy")
    hidden_sync.add_argument("--max-destinations", type=int, default=10)
    hidden_sync.add_argument("--min-savings", type=float, default=0)
    hidden_sync.add_argument("--locale", default="zh-CN")

    hidden_job = sub.add_parser("hidden-city-job-create")
    hidden_job.add_argument("--from", dest="origin", required=True)
    hidden_job.add_argument("--to", dest="destination", required=True)
    hidden_job.add_argument("--date", required=True)
    hidden_job.add_argument("--passengers", type=int, default=1)
    hidden_job.add_argument("--cabin-class", default="economy")
    hidden_job.add_argument("--max-destinations", type=int, default=10)
    hidden_job.add_argument("--min-savings", type=float, default=0)
    hidden_job.add_argument("--locale", default="zh-CN")
    hidden_job.add_argument("--with-booking-summary", action="store_true")
    hidden_job.add_argument("--booking-summary-limit", type=int, default=0)

    job_status = sub.add_parser("job-status")
    job_status.add_argument("--job-id", required=True)

    usage = sub.add_parser("usage")
    usage.add_argument("--period", default="all", choices=["all", "day", "month"])

    return p


def main() -> int:
    load_local_env()
    args = parser().parse_args()
    idem = str(uuid.uuid4())
    if args.command == "search":
        payload = {
            "origin": args.origin,
            "destination": args.destination,
            "date": args.date,
            "return_date": args.return_date,
            "passengers": args.passengers,
            "cabin_class": args.cabin_class,
            "sort_by": args.sort_by,
            "locale": args.locale,
            "with_booking_summary": args.with_booking_summary,
            "booking_summary_limit": args.booking_summary_limit,
        }
        result = request_json("POST", "/v1/flights/search", body=payload, idempotency_key=idem)
    elif args.command == "calendar":
        payload = {
            "origin": args.origin,
            "destination": args.destination,
            "date_start": args.date_start,
            "date_end": args.date_end,
            "passengers": args.passengers,
            "cabin_class": args.cabin_class,
            "locale": args.locale,
            "currency": args.currency,
            "window_days": args.window_days,
        }
        result = request_json("POST", "/v1/flights/calendar", body=payload, idempotency_key=idem)
    elif args.command == "airport-search":
        result = request_json("GET", "/v1/airports/search", query={"q": args.query, "locale": args.locale})
    elif args.command == "hidden-city-sync":
        payload = {
            "origin": args.origin,
            "destination": args.destination,
            "date": args.date,
            "passengers": args.passengers,
            "cabin_class": args.cabin_class,
            "max_destinations": args.max_destinations,
            "min_savings": args.min_savings,
            "locale": args.locale,
        }
        result = request_json("POST", "/v1/flights/hidden-city/search", body=payload, idempotency_key=idem)
    elif args.command == "hidden-city-job-create":
        payload = {
            "origin": args.origin,
            "destination": args.destination,
            "date": args.date,
            "passengers": args.passengers,
            "cabin_class": args.cabin_class,
            "max_destinations": args.max_destinations,
            "min_savings": args.min_savings,
            "locale": args.locale,
            "with_booking_summary": args.with_booking_summary,
            "booking_summary_limit": args.booking_summary_limit,
        }
        result = request_json("POST", "/v1/flights/hidden-city/jobs", body=payload, idempotency_key=idem)
    elif args.command == "job-status":
        result = request_json("GET", f"/v1/jobs/{args.job_id}")
    else:
        result = request_json("GET", "/v1/account/usage", query={"period": args.period})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
