#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feishu Bitable CLI - SQL-like interface for Feishu multidimensional tables.

Usage:
  python3 feishu_bitable.py <command> [options]

Commands:
  list-tables    List all tables in a Bitable app
  describe       Get table schema (field names, types)
  select         Query records with filtering, sorting, pagination
  insert         Create a new record
  update         Update records by record_id or filter
  delete         Delete records by record_id or filter
  count          Count records (with optional filter)
  aggregate      Aggregate data (SUM, AVG, MIN, MAX, GROUP BY)
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import urllib.request
import urllib.error

DEFAULT_HOST = os.getenv("FEISHU_API_HOST", "https://open.feishu.cn")
DEFAULT_CACHE = os.getenv(
    "FEISHU_TOKEN_CACHE",
    str(Path.home() / ".cache" / "openclaw" / "feishu_tenant_token.json")
)

TOKEN_URL = f"{DEFAULT_HOST}/open-apis/auth/v3/tenant_access_token/internal"


def log_debug(msg: str) -> None:
    if os.getenv("FEISHU_DEBUG"):
        print(f"[DEBUG] {msg}", file=sys.stderr)


def _http_json(method: str, url: str, headers: Dict[str, str], body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers = {**headers, "Content-Type": "application/json"}
    req = urllib.request.Request(url=url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            return json.loads(raw)
        except:
            return {"code": e.code, "msg": raw}


def _load_cached_token(cache_path: str) -> Optional[str]:
    try:
        p = Path(cache_path)
        if not p.exists():
            return None
        obj = json.loads(p.read_text("utf-8"))
        token = obj.get("tenant_access_token")
        expires_at = obj.get("expires_at", 0)
        if token and time.time() < (expires_at - 60):
            return token
        return None
    except Exception:
        return None


def _save_cached_token(cache_path: str, token: str, expire_seconds: int) -> None:
    p = Path(cache_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    obj = {
        "tenant_access_token": token,
        "expires_at": int(time.time()) + int(expire_seconds),
    }
    p.write_text(json.dumps(obj, ensure_ascii=False), "utf-8")


def get_tenant_token() -> str:
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise RuntimeError("Missing env: FEISHU_APP_ID / FEISHU_APP_SECRET")

    cached = _load_cached_token(DEFAULT_CACHE)
    if cached:
        log_debug("Using cached token")
        return cached

    resp = _http_json("POST", TOKEN_URL, headers={}, body={"app_id": app_id, "app_secret": app_secret})
    if resp.get("code") != 0:
        raise RuntimeError(f"Token error: {resp}")
    token = resp["tenant_access_token"]
    expire = resp.get("expire", 3600)
    _save_cached_token(DEFAULT_CACHE, token, expire)
    log_debug("Token refreshed")
    return token


def _api_get(url: str) -> Dict[str, Any]:
    token = get_tenant_token()
    return _http_json("GET", url, headers={"Authorization": f"Bearer {token}"})


def _api_post(url: str, body: Dict[str, Any]) -> Dict[str, Any]:
    token = get_tenant_token()
    return _http_json("POST", url, headers={"Authorization": f"Bearer {token}"}, body=body)


def _api_put(url: str, body: Dict[str, Any]) -> Dict[str, Any]:
    token = get_tenant_token()
    return _http_json("PUT", url, headers={"Authorization": f"Bearer {token}"}, body=body)


def _api_delete(url: str) -> Dict[str, Any]:
    token = get_tenant_token()
    return _http_json("DELETE", url, headers={"Authorization": f"Bearer {token}"})


# ============================================================================
# API Operations
# ============================================================================

def api_list_tables(app_token: str) -> Dict[str, Any]:
    """List all tables in a Bitable app."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables"
    return _api_get(url)


def api_get_fields(app_token: str, table_id: str) -> Dict[str, Any]:
    """Get all fields in a table (schema)."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    return _api_get(url)


def api_list_views(app_token: str, table_id: str) -> Dict[str, Any]:
    """List all views in a table."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/views"
    return _api_get(url)


def api_search_records(
    app_token: str,
    table_id: str,
    *,
    page_size: int = 100,
    page_token: Optional[str] = None,
    view_id: Optional[str] = None,
    filter_expr: Optional[str] = None,
    sort: Optional[List[Dict[str, Any]]] = None,
    field_names: Optional[List[str]] = None,
    automatic_fields: bool = False,
) -> Dict[str, Any]:
    """Search records with advanced filtering and sorting."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
    body: Dict[str, Any] = {
        "page_size": min(max(page_size, 1), 500),
    }
    if page_token:
        body["page_token"] = page_token
    if view_id:
        body["view_id"] = view_id
    if filter_expr:
        # Use the new filter_expression format (Feishu OpenAPI v1)
        body["filter_expression"] = filter_expr
    if sort:
        body["sort"] = sort
    if field_names:
        body["field_names"] = field_names
    if automatic_fields:
        body["automatic_fields"] = automatic_fields

    log_debug(f"API request: POST {url}")
    log_debug(f"Request body: {json.dumps(body, ensure_ascii=False)}")
    result = _api_post(url, body)
    log_debug(f"API response code: {result.get('code')}")
    return result


def api_get_record(app_token: str, table_id: str, record_id: str) -> Dict[str, Any]:
    """Get a single record by ID."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    return _api_get(url)


def api_create_record(app_token: str, table_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new record."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    body = {"fields": fields}
    return _api_post(url, body)


def api_create_records_batch(app_token: str, table_id: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create multiple records (batch)."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
    body = {"records": [{"fields": r} for r in records]}
    return _api_post(url, body)


def api_update_record(app_token: str, table_id: str, record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
    """Update a single record."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    body = {"fields": fields}
    return _api_put(url, body)


def api_update_records_batch(app_token: str, table_id: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update multiple records (batch). Each record must have 'record_id' and 'fields'."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
    body = {"records": records}
    return _api_post(url, body)


def api_delete_record(app_token: str, table_id: str, record_id: str) -> Dict[str, Any]:
    """Delete a single record."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    return _api_delete(url)


def api_delete_records_batch(app_token: str, table_id: str, record_ids: List[str]) -> Dict[str, Any]:
    """Delete multiple records (batch)."""
    url = f"{DEFAULT_HOST}/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete"
    body = {"records": record_ids}
    return _api_post(url, body)


# ============================================================================
# High-level Operations
# ============================================================================

def fetch_all_records(
    app_token: str,
    table_id: str,
    *,
    view_id: Optional[str] = None,
    filter_expr: Optional[str] = None,
    sort: Optional[List[Dict[str, Any]]] = None,
    field_names: Optional[List[str]] = None,
    max_records: int = 10000,
) -> List[Dict[str, Any]]:
    """Fetch all records with automatic pagination."""
    all_items = []
    page_token = None

    while len(all_items) < max_records:
        resp = api_search_records(
            app_token,
            table_id,
            page_size=500,
            page_token=page_token,
            view_id=view_id,
            filter_expr=filter_expr,
            sort=sort,
            field_names=field_names,
        )
        if resp.get("code") != 0:
            raise RuntimeError(f"API error: {resp}")

        data = resp.get("data", {})
        items = data.get("items", [])
        all_items.extend(items)

        if not data.get("has_more"):
            break
        page_token = data.get("page_token")
        if not page_token:
            break

    return all_items[:max_records]


def build_filter_expression(conditions: List[Dict[str, Any]]) -> str:
    """
    Build Feishu filter expression from conditions.

    Condition format: {"field": "Status", "op": "=", "value": "Done"}
    Supported ops: =, !=, >, <, >=, <=, contains, starts_with, ends_with, is_empty, is_not_empty, in, not_in

    Example result: 'CurrentValue.[Status] = "Done" AND CurrentValue.[Priority] > 3'
    """
    parts = []
    for cond in conditions:
        field = cond.get("field", "")
        op = cond.get("op", "=")
        value = cond.get("value")

        # Escape field name
        field_ref = f'CurrentValue.[{field}]'

        if op == "is_empty":
            parts.append(f'{field_ref} = ""')
        elif op == "is_not_empty":
            parts.append(f'{field_ref} != ""')
        elif op == "contains":
            parts.append(f'{field_ref}.Contains("{value}")')
        elif op == "starts_with":
            parts.append(f'{field_ref}.StartsWith("{value}")')
        elif op == "ends_with":
            parts.append(f'{field_ref}.EndsWith("{value}")')
        elif op == "in":
            if isinstance(value, list):
                vals = ', '.join(f'"{v}"' for v in value)
                parts.append(f'{field_ref} IN ({vals})')
        elif op == "not_in":
            if isinstance(value, list):
                vals = ', '.join(f'"{v}"' for v in value)
                parts.append(f'{field_ref} NOT IN ({vals})')
        elif isinstance(value, str):
            parts.append(f'{field_ref} {op} "{value}"')
        elif isinstance(value, (int, float)):
            parts.append(f'{field_ref} {op} {value}')
        elif value is None:
            parts.append(f'{field_ref} {op} ""')
        else:
            parts.append(f'{field_ref} {op} "{value}"')

    return " AND ".join(parts)


def aggregate_records(
    records: List[Dict[str, Any]],
    *,
    group_by: Optional[str] = None,
    aggregations: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Aggregate records like SQL GROUP BY.

    aggregations format: [{"field": "amount", "op": "SUM", "as": "total_amount"}]
    Supported ops: COUNT, SUM, AVG, MIN, MAX
    """
    if not aggregations:
        aggregations = [{"op": "COUNT", "as": "count"}]

    # Group records
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for record in records:
        fields = record.get("fields", {})
        if group_by:
            key = str(fields.get(group_by, "__null__"))
        else:
            key = "__all__"
        if key not in groups:
            groups[key] = []
        groups[key].append(record)

    # Calculate aggregations
    result = []
    for key, group_records in groups.items():
        row = {}
        if group_by:
            row[group_by] = None if key == "__null__" else key

        for agg in aggregations:
            field = agg.get("field")
            op = agg.get("op", "COUNT").upper()
            as_name = agg.get("as", f"{op.lower()}_{field}" if field else op.lower())

            if op == "COUNT":
                row[as_name] = len(group_records)
            else:
                values = []
                for r in group_records:
                    v = r.get("fields", {}).get(field)
                    if isinstance(v, (int, float)):
                        values.append(v)
                    elif isinstance(v, str) and v.replace(".", "").replace("-", "").isdigit():
                        values.append(float(v))

                if not values:
                    row[as_name] = None
                elif op == "SUM":
                    row[as_name] = sum(values)
                elif op == "AVG":
                    row[as_name] = sum(values) / len(values)
                elif op == "MIN":
                    row[as_name] = min(values)
                elif op == "MAX":
                    row[as_name] = max(values)

        result.append(row)

    return {"groups": result, "total_groups": len(result)}


# ============================================================================
# CLI Commands
# ============================================================================

def cmd_list_tables(args):
    """List all tables in a Bitable app."""
    resp = api_list_tables(args.app_token)
    if resp.get("code") != 0:
        return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}

    tables = resp.get("data", {}).get("items", [])
    result = []
    for t in tables:
        result.append({
            "table_id": t.get("table_id"),
            "name": t.get("name"),
            "revision": t.get("revision"),
        })
    return {"ok": True, "tables": result}


def cmd_describe(args):
    """Get table schema (fields and views)."""
    # Get fields
    fields_resp = api_get_fields(args.app_token, args.table_id)
    if fields_resp.get("code") != 0:
        return {"ok": False, "error": fields_resp.get("msg", str(fields_resp))}

    fields = []
    for f in fields_resp.get("data", {}).get("items", []):
        fields.append({
            "field_id": f.get("field_id"),
            "field_name": f.get("field_name"),
            "type": f.get("type"),
            "property": f.get("property"),
        })

    # Get views
    views_resp = api_list_views(args.app_token, args.table_id)
    views = []
    if views_resp.get("code") == 0:
        for v in views_resp.get("data", {}).get("items", []):
            views.append({
                "view_id": v.get("view_id"),
                "view_name": v.get("view_name"),
                "view_type": v.get("view_type"),
            })

    return {
        "ok": True,
        "table_id": args.table_id,
        "fields": fields,
        "views": views,
    }


def cmd_select(args):
    """Query records with filtering, sorting, pagination."""
    # Build filter expression
    filter_expr = args.filter
    if args.where:
        # Parse simple WHERE conditions and convert to Feishu filter_expression
        # Format: "field = value" or "field > value" etc.
        conditions = []
        parts = re.split(r'\s+AND\s+', args.where, flags=re.IGNORECASE)
        for part in parts:
            matched = False
            for op_pattern, op_name in [
                (r'!=', '!='),
                (r'>=', '>='),
                (r'<=', '<='),
                (r'>', '>'),
                (r'<', '<'),
                (r'=', '='),
            ]:
                if op_pattern in part:
                    idx = part.find(op_pattern)
                    field = part[:idx].strip()
                    value = part[idx + len(op_pattern):].strip().strip('"\'')
                    conditions.append((field, op_name, value))
                    matched = True
                    break
            if not matched:
                # Try contains, starts_with, ends_with
                for op_pattern, op_name in [
                    (r'\s+contains\s+', 'contains'),
                    (r'\s+starts_with\s+', 'starts_with'),
                    (r'\s+ends_with\s+', 'ends_with'),
                ]:
                    match = re.search(op_pattern, part, re.IGNORECASE)
                    if match:
                        idx = match.start()
                        field = part[:idx].strip()
                        value = part[match.end():].strip().strip('"\'')
                        conditions.append((field, op_name, value))
                        matched = True
                        break

        if conditions:
            filter_parts = []
            for field, op, value in conditions:
                field_ref = f'CurrentValue.[{field}]'
                if op == 'contains':
                    filter_parts.append(f'{field_ref}.Contains("{value}")')
                elif op == 'starts_with':
                    filter_parts.append(f'{field_ref}.StartsWith("{value}")')
                elif op == 'ends_with':
                    filter_parts.append(f'{field_ref}.EndsWith("{value}")')
                else:
                    filter_parts.append(f'{field_ref} {op} "{value}"')
            filter_expr = " AND ".join(filter_parts)
            log_debug(f"Generated filter expression: {filter_expr}")

    # Build sort
    sort = None
    if args.order_by:
        sort = []
        for part in args.order_by.split(","):
            part = part.strip()
            if part.upper().endswith(" DESC"):
                sort.append({"field_name": part[:-5].strip(), "desc": True})
            else:
                field = part.replace(" ASC", "").replace(" asc", "").strip()
                sort.append({"field_name": field, "desc": False})

    # Parse field names
    field_names = None
    if args.fields:
        field_names = [f.strip() for f in args.fields.split(",")]

    # Fetch records
    try:
        if args.limit and args.limit <= 500:
            # Single page
            resp = api_search_records(
                args.app_token,
                args.table_id,
                page_size=args.limit,
                view_id=args.view_id,
                filter_expr=filter_expr,
                sort=sort,
                field_names=field_names,
            )
            if resp.get("code") != 0:
                return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}
            items = resp.get("data", {}).get("items", [])
        else:
            # Fetch all with pagination
            items = fetch_all_records(
                args.app_token,
                args.table_id,
                view_id=args.view_id,
                filter_expr=filter_expr,
                sort=sort,
                field_names=field_names,
                max_records=args.limit or 10000,
            )
    except Exception as e:
        return {"ok": False, "error": str(e)}

    # Format output
    records = []
    for item in items:
        records.append({
            "record_id": item.get("record_id"),
            "fields": item.get("fields", {}),
        })

    result = {"ok": True, "count": len(records), "records": records}
    if args.format == "table":
        result["_format"] = "table"
    return result


def cmd_count(args):
    """Count records with optional filter."""
    filter_expr = args.filter
    if args.where:
        conditions = []
        for part in args.where.split(" AND "):
            for op in ["!=", ">=", "<=", ">", "<", "=", " contains "]:
                if op in part:
                    idx = part.lower().find(op.lower())
                    if idx > 0:
                        field = part[:idx].strip()
                        value = part[idx + len(op):].strip().strip('"\'')
                        conditions.append({"field": field, "op": op.strip(), "value": value})
                        break
        if conditions:
            filter_expr = build_filter_expression(conditions)

    # Just get record IDs to minimize data transfer
    items = fetch_all_records(
        args.app_token,
        args.table_id,
        view_id=args.view_id,
        filter_expr=filter_expr,
        field_names=["__record_id__"],  # minimal
        max_records=100000,
    )

    return {"ok": True, "count": len(items)}


def cmd_aggregate(args):
    """Aggregate data (SUM, AVG, MIN, MAX, GROUP BY)."""
    # Parse aggregations
    aggregations = []
    if args.agg:
        # Format: "SUM(amount)", "AVG(score) as avg_score"
        for part in args.agg.split(","):
            part = part.strip()
            as_name = None
            if " as " in part.lower():
                idx = part.lower().find(" as ")
                as_name = part[idx + 4:].strip()
                part = part[:idx].strip()

            for op in ["SUM", "AVG", "MIN", "MAX", "COUNT"]:
                if part.upper().startswith(op + "("):
                    field = part[len(op) + 1:-1].strip()
                    aggregations.append({
                        "op": op,
                        "field": field if field else None,
                        "as": as_name or f"{op.lower()}_{field}" if field else op.lower(),
                    })
                    break

    if not aggregations:
        aggregations = [{"op": "COUNT", "as": "count"}]

    # Fetch records
    field_names = None
    if args.group_by:
        field_names = [args.group_by]
    for agg in aggregations:
        if agg.get("field") and agg["field"] not in (field_names or []):
            if field_names is None:
                field_names = []
            field_names.append(agg["field"])

    filter_expr = args.filter
    if args.where:
        filter_expr = filter_expr or args.where

    items = fetch_all_records(
        args.app_token,
        args.table_id,
        view_id=args.view_id,
        filter_expr=filter_expr,
        field_names=field_names,
        max_records=args.limit or 50000,
    )

    # Aggregate
    result = aggregate_records(items, group_by=args.group_by, aggregations=aggregations)
    return {"ok": True, **result}


def cmd_insert(args):
    """Create a new record."""
    fields = json.loads(args.data)
    resp = api_create_record(args.app_token, args.table_id, fields)
    if resp.get("code") != 0:
        return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}

    return {
        "ok": True,
        "record_id": resp.get("data", {}).get("record", {}).get("record_id"),
        "record": resp.get("data", {}).get("record"),
    }


def cmd_insert_batch(args):
    """Create multiple records."""
    records = json.loads(args.data)
    if not isinstance(records, list):
        records = [records]

    resp = api_create_records_batch(args.app_token, args.table_id, records)
    if resp.get("code") != 0:
        return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}

    return {
        "ok": True,
        "created_count": len(resp.get("data", {}).get("records", [])),
        "records": resp.get("data", {}).get("records", []),
    }


def cmd_update(args):
    """Update records by record_id or filter."""
    fields = json.loads(args.data)

    if args.record_id:
        # Update by ID
        resp = api_update_record(args.app_token, args.table_id, args.record_id, fields)
        if resp.get("code") != 0:
            return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}
        return {
            "ok": True,
            "record_id": args.record_id,
            "record": resp.get("data", {}).get("record"),
        }
    elif args.filter or args.where:
        # Update by filter - find records first
        filter_expr = args.filter
        if args.where:
            filter_expr = args.where

        items = fetch_all_records(
            args.app_token,
            args.table_id,
            filter_expr=filter_expr,
            field_names=None,
            max_records=args.limit or 500,
        )

        if not items:
            return {"ok": True, "updated_count": 0, "message": "No records matched filter"}

        # Batch update
        records = [{"record_id": item["record_id"], "fields": fields} for item in items]
        resp = api_update_records_batch(args.app_token, args.table_id, records)
        if resp.get("code") != 0:
            return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}

        return {
            "ok": True,
            "updated_count": len(resp.get("data", {}).get("records", [])),
            "record_ids": [r.get("record_id") for r in resp.get("data", {}).get("records", [])],
        }
    else:
        return {"ok": False, "error": "Either --record-id or --filter/--where is required"}


def cmd_delete(args):
    """Delete records by record_id or filter."""
    if args.record_id:
        # Delete by ID
        resp = api_delete_record(args.app_token, args.table_id, args.record_id)
        if resp.get("code") != 0:
            return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}
        return {"ok": True, "deleted": True, "record_id": args.record_id}

    elif args.record_ids:
        # Delete by IDs (batch)
        ids = [x.strip() for x in args.record_ids.split(",")]
        resp = api_delete_records_batch(args.app_token, args.table_id, ids)
        if resp.get("code") != 0:
            return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}
        return {"ok": True, "deleted_count": len(ids), "record_ids": ids}

    elif args.filter or args.where:
        # Delete by filter - find records first
        filter_expr = args.filter
        if args.where:
            filter_expr = args.where

        items = fetch_all_records(
            args.app_token,
            args.table_id,
            filter_expr=filter_expr,
            field_names=None,
            max_records=args.limit or 500,
        )

        if not items:
            return {"ok": True, "deleted_count": 0, "message": "No records matched filter"}

        ids = [item["record_id"] for item in items]
        resp = api_delete_records_batch(args.app_token, args.table_id, ids)
        if resp.get("code") != 0:
            return {"ok": False, "error": resp.get("msg", str(resp)), "code": resp.get("code")}

        return {"ok": True, "deleted_count": len(ids), "record_ids": ids}
    else:
        return {"ok": False, "error": "Either --record-id, --record-ids, or --filter/--where is required"}


def parse_url(url: str) -> Dict[str, str]:
    """
    Parse Feishu Bitable URL to extract app_token, table_id, view_id.

    URL format: https://xxx.feishu.cn/base/<app_token>?table=<table_id>&view=<view_id>

    Returns dict with: app_token, table_id, view_id (if present)
    """
    import urllib.parse

    result = {}

    # Extract app_token from path
    # Pattern: /base/<app_token>
    match = re.search(r'/base/([a-zA-Z0-9]+)', url)
    if match:
        result["app_token"] = match.group(1)

    # Extract table_id and view_id from query params
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)

    if "table" in params:
        result["table_id"] = params["table"][0]
    if "view" in params:
        result["view_id"] = params["view"][0]

    return result


def main():
    ap = argparse.ArgumentParser(
        description="Feishu Bitable CLI - SQL-like interface for multidimensional tables",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True, help="Command to execute")

    # parse-url
    pu = sub.add_parser("parse-url", help="Parse Feishu URL to extract app_token, table_id, view_id")
    pu.add_argument("url", help="Feishu Bitable URL")

    # list-tables
    lt = sub.add_parser("list-tables", help="List all tables in a Bitable app")
    lt.add_argument("--app-token", help="Bitable app token (or use --url)")
    lt.add_argument("--url", help="Feishu Bitable URL to extract app_token from")

    # describe
    desc = sub.add_parser("describe", help="Get table schema (fields and views)")
    desc.add_argument("--app-token", help="Bitable app token (or use --url)")
    desc.add_argument("--table-id", help="Table ID (or use --url)")
    desc.add_argument("--url", help="Feishu Bitable URL to extract params from")

    # select
    sel = sub.add_parser("select", help="Query records (SQL SELECT)")
    sel.add_argument("--app-token", help="Bitable app token (or use --url)")
    sel.add_argument("--table-id", help="Table ID (or use --url)")
    sel.add_argument("--url", help="Feishu Bitable URL to extract params from")
    sel.add_argument("--view-id", help="View ID to filter by")
    sel.add_argument("--fields", help="Comma-separated field names to return")
    sel.add_argument("--filter", help="Feishu filter expression (e.g., 'CurrentValue.[Status] = \"Done\"')")
    sel.add_argument("--where", help="Simple WHERE clause (e.g., 'Status = Done AND Priority > 3')")
    sel.add_argument("--order-by", help="Sort order (e.g., 'created_time DESC, name ASC')")
    sel.add_argument("--limit", type=int, default=100, help="Max records to return (default: 100)")
    sel.add_argument("--format", choices=["json", "table"], default="json", help="Output format")

    # count
    cnt = sub.add_parser("count", help="Count records")
    cnt.add_argument("--app-token", help="Bitable app token (or use --url)")
    cnt.add_argument("--table-id", help="Table ID (or use --url)")
    cnt.add_argument("--url", help="Feishu Bitable URL to extract params from")
    cnt.add_argument("--view-id", help="View ID to filter by")
    cnt.add_argument("--filter", help="Feishu filter expression")
    cnt.add_argument("--where", help="Simple WHERE clause")

    # aggregate
    agg = sub.add_parser("aggregate", help="Aggregate data (SUM, AVG, MIN, MAX, GROUP BY)")
    agg.add_argument("--app-token", help="Bitable app token (or use --url)")
    agg.add_argument("--table-id", help="Table ID (or use --url)")
    agg.add_argument("--url", help="Feishu Bitable URL to extract params from")
    agg.add_argument("--view-id", help="View ID to filter by")
    agg.add_argument("--group-by", help="Field to group by (like SQL GROUP BY)")
    agg.add_argument("--agg", help="Aggregations (e.g., 'SUM(amount), AVG(score) as avg_score')")
    agg.add_argument("--filter", help="Feishu filter expression")
    agg.add_argument("--where", help="Simple WHERE clause")
    agg.add_argument("--limit", type=int, help="Max records to process")

    # insert
    ins = sub.add_parser("insert", help="Create a new record (SQL INSERT)")
    ins.add_argument("--app-token", help="Bitable app token (or use --url)")
    ins.add_argument("--table-id", help="Table ID (or use --url)")
    ins.add_argument("--url", help="Feishu Bitable URL to extract params from")
    ins.add_argument("--data", required=True, help="JSON object with field values")

    # insert-batch
    insb = sub.add_parser("insert-batch", help="Create multiple records")
    insb.add_argument("--app-token", help="Bitable app token (or use --url)")
    insb.add_argument("--table-id", help="Table ID (or use --url)")
    insb.add_argument("--url", help="Feishu Bitable URL to extract params from")
    insb.add_argument("--data", required=True, help="JSON array of field objects")

    # update
    upd = sub.add_parser("update", help="Update records (SQL UPDATE)")
    upd.add_argument("--app-token", help="Bitable app token (or use --url)")
    upd.add_argument("--table-id", help="Table ID (or use --url)")
    upd.add_argument("--url", help="Feishu Bitable URL to extract params from")
    upd.add_argument("--record-id", help="Record ID to update")
    upd.add_argument("--filter", help="Feishu filter expression to match records")
    upd.add_argument("--where", help="Simple WHERE clause to match records")
    upd.add_argument("--data", required=True, help="JSON object with field values to update")
    upd.add_argument("--limit", type=int, help="Max records to update when using filter")

    # delete
    dlt = sub.add_parser("delete", help="Delete records (SQL DELETE)")
    dlt.add_argument("--app-token", help="Bitable app token (or use --url)")
    dlt.add_argument("--table-id", help="Table ID (or use --url)")
    dlt.add_argument("--url", help="Feishu Bitable URL to extract params from")
    dlt.add_argument("--record-id", help="Single record ID to delete")
    dlt.add_argument("--record-ids", help="Comma-separated record IDs to delete")
    dlt.add_argument("--filter", help="Feishu filter expression to match records")
    dlt.add_argument("--where", help="Simple WHERE clause to match records")
    dlt.add_argument("--limit", type=int, help="Max records to delete when using filter")

    args = ap.parse_args()

    # Handle --url parameter to extract app_token and table_id
    if hasattr(args, 'url') and args.url:
        parsed = parse_url(args.url)
        if hasattr(args, 'app_token') and not args.app_token and 'app_token' in parsed:
            args.app_token = parsed['app_token']
        if hasattr(args, 'table_id') and not args.table_id and 'table_id' in parsed:
            args.table_id = parsed['table_id']
        if hasattr(args, 'view_id') and not getattr(args, 'view_id', None) and 'view_id' in parsed:
            args.view_id = parsed['view_id']

    # Validate required params
    if args.cmd == "parse-url":
        result = {"ok": True, **parse_url(args.url)}
    elif args.cmd == "list-tables":
        if not args.app_token:
            result = {"ok": False, "error": "--app-token or --url is required"}
        else:
            result = cmd_list_tables(args)
    elif args.cmd == "describe":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_describe(args)
    elif args.cmd == "select":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_select(args)
    elif args.cmd == "count":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_count(args)
    elif args.cmd == "aggregate":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_aggregate(args)
    elif args.cmd == "insert":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_insert(args)
    elif args.cmd == "insert-batch":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_insert_batch(args)
    elif args.cmd == "update":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_update(args)
    elif args.cmd == "delete":
        if not args.app_token or not args.table_id:
            result = {"ok": False, "error": "--app-token and --table-id (or --url) are required"}
        else:
            result = cmd_delete(args)
    else:
        result = {"ok": False, "error": f"Unknown command: {args.cmd}"}

    # Output result
    print(json.dumps(result, ensure_ascii=False, indent=2 if os.getenv("FEISHU_PRETTY") else None))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        if os.getenv("FEISHU_DEBUG"):
            raise
