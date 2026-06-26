#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, OrderBy
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
CONFIG_DIR = Path.home() / ".config" / "openclaw"
DEFAULT_CLIENT_SECRET = CONFIG_DIR / "ga4-client.json"
DEFAULT_TOKEN_FILE = CONFIG_DIR / "ga4-token.json"


def get_env(name: str, default: str | None = None) -> str | None:
    val = os.environ.get(name)
    return val if val else default


def parse_args():
    p = argparse.ArgumentParser(description="Query GA4 Data API for OpenClaw")
    p.add_argument("--property-id", default=get_env("GA4_PROPERTY_ID"), help="GA4 property ID or set GA4_PROPERTY_ID")
    p.add_argument("--client-secret", default=str(DEFAULT_CLIENT_SECRET), help="Path to Desktop OAuth client JSON")
    p.add_argument("--token-file", default=str(DEFAULT_TOKEN_FILE), help="Path to OAuth token cache")
    p.add_argument("--start", default="7daysAgo", help="Start date, e.g. 7daysAgo or 2026-03-01")
    p.add_argument("--end", default="today", help="End date, e.g. today or 2026-03-12")
    p.add_argument("--metrics", required=True, help="Comma-separated metrics, e.g. activeUsers,sessions")
    p.add_argument("--dimensions", default="", help="Comma-separated dimensions, e.g. date,country")
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    return p.parse_args()


def load_creds(client_secret: str, token_file: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    creds = None
    token_path = Path(token_file)
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
        creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())
    return creds


def main():
    args = parse_args()
    if not args.property_id:
        print("Missing --property-id (or GA4_PROPERTY_ID)", file=sys.stderr)
        sys.exit(2)
    if not Path(args.client_secret).exists():
        print(f"Missing client secret JSON: {args.client_secret}", file=sys.stderr)
        sys.exit(2)

    creds = load_creds(args.client_secret, args.token_file)
    client = BetaAnalyticsDataClient(credentials=creds)

    metrics = [Metric(name=m.strip()) for m in args.metrics.split(",") if m.strip()]
    dimensions = [Dimension(name=d.strip()) for d in args.dimensions.split(",") if d.strip()]

    order_bys = []
    if dimensions:
        order_bys.append(OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name=dimensions[0].name)))

    request = RunReportRequest(
        property=f"properties/{args.property_id}",
        dimensions=dimensions,
        metrics=metrics,
        date_ranges=[DateRange(start_date=args.start, end_date=args.end)],
        order_bys=order_bys,
        limit=args.limit,
    )
    response = client.run_report(request)

    rows = []
    for row in response.rows:
        item = {}
        for i, d in enumerate(dimensions):
            item[d.name] = row.dimension_values[i].value
        for i, m in enumerate(metrics):
            item[m.name] = row.metric_values[i].value
        rows.append(item)

    out = {
        "property": args.property_id,
        "start": args.start,
        "end": args.end,
        "metrics": [m.name for m in metrics],
        "dimensions": [d.name for d in dimensions],
        "rows": rows,
    }
    if args.pretty:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
