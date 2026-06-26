#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import uuid
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

import requests

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)
SCHEMA_RE = re.compile(r"https://schema\.org/([A-Za-z]+)", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Check Costco inventory by product and ZIP")
    p.add_argument("--product", action="append", required=True, help="<id>|<name>|<url>")
    p.add_argument("--zip", action="append", dest="zip_codes", required=True)
    p.add_argument("--proxy-url", required=True)
    p.add_argument("--timeout", type=int, default=45)
    p.add_argument("--retries", type=int, default=2)
    p.add_argument("--output-jsonl", required=True)
    p.add_argument("--state-file", required=True)
    p.add_argument("--report-file", required=True)
    return p.parse_args()


def parse_product(spec: str) -> dict:
    parts = spec.split("|", 2)
    if len(parts) != 3:
        raise ValueError(f"Invalid --product: {spec}")
    pid, name, url = [x.strip() for x in parts]
    return {"id": pid, "name": name, "url": url}


def with_zip(url: str, zip_code: str) -> str:
    u = urlparse(url)
    q = dict(parse_qsl(u.query, keep_blank_values=True))
    q["zipcode"] = zip_code
    new_query = urlencode(q)
    return urlunparse((u.scheme, u.netloc, u.path, u.params, new_query, u.fragment))


def availability_from_html(html: str) -> tuple[str, str]:
    m = SCHEMA_RE.search(html)
    token = m.group(1).lower() if m else ""
    if token == "instock":
        return "in_stock", "schema.org/InStock"
    if token == "outofstock":
        return "out_of_stock", "schema.org/OutOfStock"
    if token == "limitedavailability":
        return "limited_stock", "schema.org/LimitedAvailability"
    if token == "preorder":
        return "limited_stock", "schema.org/PreOrder"

    low = html.lower()
    if "out of stock" in low:
        return "out_of_stock", "keyword:out of stock"
    if "in stock" in low:
        return "in_stock", "keyword:in stock"
    return "unknown", "no-availability-signal"


def load_state(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_json(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def append_jsonl(path: str, rows: list[dict]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    args = parse_args()
    products = [parse_product(s) for s in args.product]
    zip_codes = sorted(set(args.zip_codes))

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    run_fingerprint = f"run-{uuid.uuid4()}"

    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    session.proxies = {"http": args.proxy_url, "https": args.proxy_url}

    rows: list[dict] = []
    for p in products:
        for z in zip_codes:
            check_url = with_zip(p["url"], z)
            rec = {
                "timestamp_utc": now,
                "run_fingerprint": run_fingerprint,
                "product_id": p["id"],
                "product_name": p["name"],
                "product_url": p["url"],
                "zip_code": z,
                "source": "html",
            }
            last_error = None
            attempts = max(1, args.retries)
            for attempt in range(1, attempts + 1):
                try:
                    r = session.get(check_url, timeout=args.timeout)
                    rec["http_status"] = r.status_code
                    if r.status_code != 200:
                        rec["availability"] = "unknown"
                        rec["raw_excerpt"] = f"http_status={r.status_code}"
                    else:
                        availability, signal = availability_from_html(r.text)
                        rec["availability"] = availability
                        rec["raw_excerpt"] = signal
                    last_error = None
                    break
                except Exception as e:
                    last_error = e
                    if attempt < attempts:
                        time.sleep(1.0)
            if last_error is not None:
                rec["availability"] = "unknown"
                rec["http_status"] = None
                rec["raw_excerpt"] = f"request_error={type(last_error).__name__}: {last_error}"
            rows.append(rec)

    append_jsonl(args.output_jsonl, rows)

    old_state = load_state(args.state_file)
    new_state = {f"{r['product_id']}|{r['zip_code']}": r["availability"] for r in rows}
    save_json(args.state_file, new_state)

    changed = []
    for key, new_val in new_state.items():
        old_val = old_state.get(key)
        if old_val != new_val:
            changed.append((key, old_val, new_val))

    lines = []
    lines.append(f"[costco-monitor] {now} run={run_fingerprint}")
    for r in rows:
        lines.append(
            f"- {r['product_id']} {r['zip_code']}: {r['availability']} "
            f"(http={r.get('http_status')}, signal={r.get('raw_excerpt','')})"
        )
    if changed:
        lines.append("changes:")
        for key, old_val, new_val in changed:
            lines.append(f"- {key}: {old_val} -> {new_val}")
    else:
        lines.append("changes: none")

    report = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(args.report_file), exist_ok=True)
    with open(args.report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
