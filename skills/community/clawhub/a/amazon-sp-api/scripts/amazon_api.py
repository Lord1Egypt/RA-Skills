#!/usr/bin/env python3
"""Amazon SP-API CLI — lightweight wrapper for agent tool use.

Reads credentials from environment variables (set them in your shell, or via
your secrets manager of choice — 1Password CLI, direnv, systemd EnvFile, etc.):

  Required:
    AMAZON_SP_API_REFRESH_TOKEN        LWA refresh token
    AMAZON_SP_API_CLIENT_ID            LWA client id
    AMAZON_SP_API_CLIENT_SECRET        LWA client secret
    AMAZON_SP_API_AWS_ACCESS_KEY_ID    IAM access key for SigV4 signing
    AMAZON_SP_API_AWS_SECRET_ACCESS_KEY IAM secret key for SigV4 signing

  Optional:
    AMAZON_SP_API_MARKETPLACE_ID  Marketplace id (defaults to A1F83G8C2ARO7P / UK)
    AWS_REGION                    AWS region (defaults to eu-west-1)

Outputs JSON to stdout. Errors print to stdout as ``{"error": ...}`` with a
non-zero exit status so the agent can branch on success/failure cleanly.

See https://developer-docs.amazon.com/sp-api/ for the underlying API.
"""

from __future__ import annotations

import argparse
import datetime
import gzip
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse

import httpx

TIMEOUT = 30
MAX_RETRIES = 3
LWA_TOKEN_URL = "https://api.amazon.com/auth/o2/token"
DEFAULT_MARKETPLACE = "A1F83G8C2ARO7P"  # UK

# ── Env helpers ──────────────────────────────────────────────────────────

def _env(key: str, fallback: str = "") -> str:
    return os.environ.get(key, fallback)


def _require_env(*keys: str) -> dict[str, str]:
    vals = {k: _env(k) for k in keys}
    missing = [k for k, v in vals.items() if not v]
    if missing:
        _out(
            {
                "error": f"Missing env vars: {', '.join(missing)}",
                "hint": (
                    "Set the listed env vars in your shell or secrets manager. "
                    "Full list and details: see this skill's SKILL.md § 'Setup'."
                ),
            }
        )
        sys.exit(1)
    return vals


def _marketplace() -> str:
    return _env("AMAZON_SP_API_MARKETPLACE_ID", DEFAULT_MARKETPLACE)


def _region() -> str:
    return _env("AWS_REGION", "eu-west-1")


# ── Token management ─────────────────────────────────────────────────────

_cached_token: dict | None = None


def _get_access_token() -> str:
    global _cached_token

    if _cached_token and _cached_token["expires_at"] > time.time():
        return _cached_token["access_token"]

    env = _require_env(
        "AMAZON_SP_API_REFRESH_TOKEN",
        "AMAZON_SP_API_CLIENT_ID",
        "AMAZON_SP_API_CLIENT_SECRET",
    )

    with httpx.Client(timeout=TIMEOUT) as c:
        resp = c.post(LWA_TOKEN_URL, data={
            "grant_type": "refresh_token",
            "refresh_token": env["AMAZON_SP_API_REFRESH_TOKEN"],
            "client_id": env["AMAZON_SP_API_CLIENT_ID"],
            "client_secret": env["AMAZON_SP_API_CLIENT_SECRET"],
        })
    resp.raise_for_status()
    data = resp.json()
    _cached_token = {
        "access_token": data["access_token"],
        "expires_at": time.time() + data.get("expires_in", 3600) - 60,
    }
    return _cached_token["access_token"]


# ── AWS SigV4 signing ────────────────────────────────────────────────────

def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _get_signature_key(secret: str, date_stamp: str, region: str, service: str) -> bytes:
    k_date = _sign(("AWS4" + secret).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    return _sign(k_service, "aws4_request")


def _sigv4_headers(method: str, url: str, headers: dict, body: str = "") -> dict:
    access_key = _env("AMAZON_SP_API_AWS_ACCESS_KEY_ID")
    secret_key = _env("AMAZON_SP_API_AWS_SECRET_ACCESS_KEY")
    if not access_key or not secret_key:
        return headers

    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    path = parsed.path or "/"
    query = parsed.query

    region = _region()
    service = "execute-api"
    now = datetime.datetime.now(datetime.timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    query_params = urllib.parse.parse_qs(query, keep_blank_values=True)
    sorted_params = sorted(query_params.items())
    canonical_qs = "&".join(
        f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v[0], safe='')}"
        for k, v in sorted_params
    )

    payload_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    headers = {k.lower(): v for k, v in headers.items()}
    headers["host"] = host
    headers["x-amz-date"] = amz_date
    headers["x-amz-content-sha256"] = payload_hash

    signed_header_keys = sorted(headers)
    signed_headers = ";".join(signed_header_keys)
    canonical_headers = "".join(f"{k}:{headers[k]}\n" for k in signed_header_keys)

    canonical_request = "\n".join([
        method, path, canonical_qs, canonical_headers,
        signed_headers, payload_hash,
    ])

    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join([
        "AWS4-HMAC-SHA256", amz_date, credential_scope,
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
    ])

    signing_key = _get_signature_key(secret_key, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    headers["Authorization"] = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    return headers


# ── HTTP helpers ─────────────────────────────────────────────────────────

def _base_url() -> str:
    region = _region()
    region_map = {
        "us-east-1": "https://sellingpartnerapi-na.amazon.com",
        "eu-west-1": "https://sellingpartnerapi-eu.amazon.com",
        "us-west-2": "https://sellingpartnerapi-fe.amazon.com",
    }
    return region_map.get(region, "https://sellingpartnerapi-eu.amazon.com")


def _base_headers() -> dict:
    token = _get_access_token()
    return {
        "x-amz-access-token": token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _get(endpoint: str, params: dict | None = None) -> dict:
    url = f"{_base_url()}{endpoint}"
    full_url = f"{url}?{urllib.parse.urlencode(params)}" if params else url

    for _ in range(MAX_RETRIES):
        headers = _sigv4_headers("GET", full_url, _base_headers())
        with httpx.Client(timeout=TIMEOUT) as c:
            resp = c.get(full_url, headers=headers)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", "5")))
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Rate limit exceeded after retries")


def _post(endpoint: str, body: dict) -> dict:
    url = f"{_base_url()}{endpoint}"
    body_str = json.dumps(body)

    for _ in range(MAX_RETRIES):
        headers = _sigv4_headers("POST", url, _base_headers(), body_str)
        with httpx.Client(timeout=TIMEOUT) as c:
            resp = c.post(url, content=body_str, headers=headers)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", "5")))
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Rate limit exceeded after retries")


def _out(data):
    print(json.dumps(data, indent=2, default=str))


def _download_report_document(doc_id: str, output: str | None = None) -> None:
    """Fetch a report document by ID, decompress, parse TSV, output JSON."""
    data = _get(f"/reports/2021-06-30/documents/{doc_id}")
    url = data.get("url", "")
    compression = data.get("compressionAlgorithm", "")

    if not url:
        _out({"error": "No download URL in report document", "data": data})
        return

    with httpx.Client(timeout=60) as c:
        resp = c.get(url)
    resp.raise_for_status()
    content = resp.content

    if compression == "GZIP":
        content = gzip.decompress(content)

    text = content.decode("utf-8", errors="replace")
    lines = text.strip().split("\n")
    if len(lines) < 2:
        _out({"rows": 0, "raw": text})
        return

    headers = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        values = line.split("\t")
        rows.append({h: (values[i] if i < len(values) else "") for i, h in enumerate(headers)})

    if output:
        with open(output, "w") as f:
            f.write(text)
        _out({"rows": len(rows), "saved_to": output, "headers": headers})
    else:
        _out({"rows": len(rows), "headers": headers, "data": rows})


# ── Commands ─────────────────────────────────────────────────────────────

def cmd_orders(args):
    params = {"MarketplaceIds": _marketplace()}
    if args.status:
        params["OrderStatuses"] = args.status
    if args.since:
        params["CreatedAfter"] = args.since + "T00:00:00Z"
    if args.limit:
        params["MaxResultsPerPage"] = str(min(args.limit, 100))
    data = _get("/orders/v0/orders", params)
    orders = data.get("payload", {}).get("Orders", [])
    if args.summary:
        _out({"count": len(orders), "orders": [
            {
                "AmazonOrderId": o.get("AmazonOrderId"),
                "Status": o.get("OrderStatus"),
                "PurchaseDate": o.get("PurchaseDate"),
                "Total": o.get("OrderTotal", {}).get("Amount"),
                "Currency": o.get("OrderTotal", {}).get("CurrencyCode"),
                "FulfillmentChannel": o.get("FulfillmentChannel"),
                "NumberOfItemsShipped": o.get("NumberOfItemsShipped"),
                "NumberOfItemsUnshipped": o.get("NumberOfItemsUnshipped"),
            }
            for o in orders
        ]})
    else:
        _out({"count": len(orders), "orders": orders})


def cmd_order(args):
    data = _get(f"/orders/v0/orders/{args.order_id}")
    _out(data.get("payload", data))


def cmd_order_items(args):
    data = _get(f"/orders/v0/orders/{args.order_id}/orderItems")
    items = data.get("payload", {}).get("OrderItems", [])
    if args.summary:
        _out({"count": len(items), "items": [
            {
                "ASIN": it.get("ASIN"),
                "SellerSKU": it.get("SellerSKU"),
                "Title": it.get("Title"),
                "QuantityOrdered": it.get("QuantityOrdered"),
                "QuantityShipped": it.get("QuantityShipped"),
                "ItemPrice": it.get("ItemPrice", {}).get("Amount"),
            }
            for it in items
        ]})
    else:
        _out({"count": len(items), "items": items})


def cmd_catalog_item(args):
    params = {"MarketplaceIds": _marketplace()}
    data = _get(f"/catalog/2022-04-01/items/{args.asin}", params)
    _out(data)


def cmd_inventory(args):
    params = {
        "granularityType": "Marketplace",
        "granularityId": _marketplace(),
        "marketplaceIds": _marketplace(),
    }
    if args.skus:
        params["sellerSkus"] = args.skus
    data = _get("/fba/inventory/v1/summaries", params)
    summaries = data.get("payload", {}).get("inventorySummaries", [])
    if args.summary:
        _out({"count": len(summaries), "inventory": [
            {
                "sellerSku": s.get("sellerSku"),
                "asin": s.get("asin"),
                "fnSku": s.get("fnSku"),
                "productName": s.get("productName"),
                "totalQuantity": s.get("totalQuantity"),
            }
            for s in summaries
        ]})
    else:
        _out({"count": len(summaries), "inventory": summaries})


def cmd_reports(args):
    params = {}
    if args.type:
        params["reportTypes"] = args.type
    data = _get("/reports/2021-06-30/reports", params)
    reports = data.get("reports", [])
    if args.summary:
        _out({"count": len(reports), "reports": [
            {
                "reportId": r.get("reportId"),
                "reportType": r.get("reportType"),
                "processingStatus": r.get("processingStatus"),
                "createdTime": r.get("createdTime"),
            }
            for r in reports
        ]})
    else:
        _out({"count": len(reports), "reports": reports})


def cmd_create_report(args):
    body = {
        "reportType": args.type,
        "marketplaceIds": [_marketplace()],
    }
    if args.start:
        body["dataStartTime"] = args.start + "T00:00:00Z"
    if args.end:
        body["dataEndTime"] = args.end + "T23:59:59Z"
    data = _post("/reports/2021-06-30/reports", body)
    _out(data)


def cmd_get_report(args):
    data = _get(f"/reports/2021-06-30/reports/{args.report_id}")
    _out(data)


def cmd_get_report_document(args):
    _download_report_document(args.document_id, args.output)


def cmd_restock_report(args):
    """Create restock report, poll until done, download."""
    body = {
        "reportType": "GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT",
        "marketplaceIds": [_marketplace()],
    }
    create_resp = _post("/reports/2021-06-30/reports", body)
    report_id = create_resp.get("reportId", "")
    if not report_id:
        _out({"error": "Failed to create report", "response": create_resp})
        return

    print(json.dumps({"status": "created", "reportId": report_id}), file=sys.stderr)

    for i in range(60):
        time.sleep(10)
        status_resp = _get(f"/reports/2021-06-30/reports/{report_id}")
        processing = status_resp.get("processingStatus", "")
        print(json.dumps({"poll": i + 1, "status": processing}), file=sys.stderr)

        if processing == "DONE":
            doc_id = status_resp.get("reportDocumentId", "")
            if not doc_id:
                _out({"error": "Report done but no documentId", "data": status_resp})
                return
            _download_report_document(doc_id, args.output)
            return

        if processing in ("CANCELLED", "FATAL"):
            _out({"error": f"Report failed: {processing}", "data": status_resp})
            return

    _out({"error": "Timed out waiting for report", "reportId": report_id})


def cmd_finances(args):
    params = {}
    if args.order_id:
        data = _get(f"/finances/v0/orders/{args.order_id}/financialEvents")
    else:
        if args.since:
            params["PostedAfter"] = args.since + "T00:00:00Z"
        if args.limit:
            params["MaxResultsPerPage"] = str(min(args.limit, 100))
        data = _get("/finances/v0/financialEvents", params)
    _out(data.get("payload", data))


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Amazon SP-API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("orders")
    p.add_argument("--status", help="Filter: Unshipped, Shipped, Canceled, etc.")
    p.add_argument("--since", help="Created after date (YYYY-MM-DD)")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--summary", action="store_true")

    p = sub.add_parser("order")
    p.add_argument("order_id")

    p = sub.add_parser("order-items")
    p.add_argument("order_id")
    p.add_argument("--summary", action="store_true")

    p = sub.add_parser("catalog-item")
    p.add_argument("asin")

    p = sub.add_parser("inventory")
    p.add_argument("--skus", help="Comma-separated seller SKUs")
    p.add_argument("--summary", action="store_true")

    p = sub.add_parser("reports")
    p.add_argument("--type", help="Report type filter")
    p.add_argument("--summary", action="store_true")

    p = sub.add_parser("create-report")
    p.add_argument("--type", required=True)
    p.add_argument("--start", help="YYYY-MM-DD")
    p.add_argument("--end", help="YYYY-MM-DD")

    p = sub.add_parser("get-report")
    p.add_argument("report_id")

    p = sub.add_parser("get-report-document")
    p.add_argument("document_id")
    p.add_argument("--output", help="Save TSV to file path")

    p = sub.add_parser("restock-report")
    p.add_argument("--output", help="Save TSV to file path")

    p = sub.add_parser("finances")
    p.add_argument("--order-id")
    p.add_argument("--since", help="YYYY-MM-DD")
    p.add_argument("--limit", type=int, default=0)

    args = parser.parse_args()

    commands = {
        "orders": cmd_orders,
        "order": cmd_order,
        "order-items": cmd_order_items,
        "catalog-item": cmd_catalog_item,
        "inventory": cmd_inventory,
        "reports": cmd_reports,
        "create-report": cmd_create_report,
        "get-report": cmd_get_report,
        "get-report-document": cmd_get_report_document,
        "restock-report": cmd_restock_report,
        "finances": cmd_finances,
    }

    try:
        commands[args.command](args)
    except httpx.HTTPStatusError as e:
        _out({"error": f"HTTP {e.response.status_code}", "detail": e.response.text})
        sys.exit(1)
    except Exception as e:
        _out({"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
