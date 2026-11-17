#!/usr/bin/env python3
"""
airtable_cli.py — CLI tool for Airtable REST API

Commands:
  list-bases       List all accessible bases
  list-tables      List tables and schema for a base
  schema           Show table field schema
  list-records     List records (with filter, sort, view, limit, offset)
  get-record       Get a single record by ID
  create-record    Create one or more records
  update-record    Update a record by ID
  delete-record    Delete one or more records
  batch-create     Batch create records from a JSON file
  batch-delete     Batch delete up to 10 records by ID
  upsert           Upsert records by a merge field
  search           Search records by field value
  count            Count records (optional filter by formula)
  export           Export all records as JSON or CSV
  version          Show version info

Environment:
  AIRTABLE_API_KEY   Required. Personal Access Token (pat...) or legacy API key.

Stdlib only — no pip install required.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

__version__ = "1.1.0"
VERSION_STRING = f"airtable-cli v{__version__} (Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})"

API_BASE = "https://api.airtable.com/v0"
META_BASE = "https://api.airtable.com/v0/meta"

# ── ANSI helpers ──────────────────────────────────────────────────────

def _green(text):
    return f"\033[92m{text}\033[0m"

def _red(text):
    return f"\033[91m{text}\033[0m"

def _yellow(text):
    return f"\033[93m{text}\033[0m"

def _cyan(text):
    return f"\033[96m{text}\033[0m"

def _bold(text):
    return f"\033[1m{text}\033[0m"

USE_COLOR = sys.stdout.isatty()


def _maybe_color(fn, text):
    return fn(text) if USE_COLOR else text


# ── Auth ──────────────────────────────────────────────────────────────

def get_api_key():
    """Return the Airtable API key from environment, or exit."""
    key = os.environ.get("AIRTABLE_API_KEY")
    if not key:
        print(
            _maybe_color(
                _red,
                "ERROR: AIRTABLE_API_KEY environment variable not set.\n"
                "  export AIRTABLE_API_KEY=pat_your_token_here",
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    if key.startswith("key") and len(key) == 17:
        print(
            _maybe_color(
                _yellow,
                "WARNING: Legacy API keys (key...) were deprecated Feb 2024.\n"
                "  Create a Personal Access Token at https://airtable.com/create/tokens",
            ),
            file=sys.stderr,
        )
    return key


# ── HTTP Client ───────────────────────────────────────────────────────

def _build_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _request(url, api_key, method="GET", data=None, retries=3):
    """Make an HTTP request with retry on 429 rate-limit."""
    headers = _build_headers(api_key)
    body = json.dumps(data).encode("utf-8") if data is not None else None

    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            status = exc.code
            resp_body = exc.read().decode("utf-8", errors="replace")
            if status == 429 and attempt < retries:
                retry_after = int(exc.headers.get("Retry-After", str(2 ** attempt)))
                print(
                    _maybe_color(
                        _yellow,
                        f"  Rate limited. Retrying in {retry_after}s "
                        f"(attempt {attempt}/{retries})…",
                    ),
                    file=sys.stderr,
                )
                time.sleep(retry_after)
                continue
            # Try to extract Airtable error
            try:
                err_data = json.loads(resp_body)
                err_msg = err_data.get("error", {}).get("type", "") + ": " + err_data.get("error", {}).get("message", resp_body)
            except (json.JSONDecodeError, AttributeError):
                err_msg = resp_body.strip() or f"HTTP {status}"
            print(
                _maybe_color(_red, f"ERROR [{status}]: {err_msg}"),
                file=sys.stderr,
            )
            sys.exit(1)
        except urllib.error.URLError as exc:
            print(
                _maybe_color(_red, f"ERROR: Network error — {exc.reason}"),
                file=sys.stderr,
            )
            sys.exit(1)
    # Shouldn't reach here
    print(_maybe_color(_red, "ERROR: Max retries exceeded"), file=sys.stderr)
    sys.exit(1)


def _paginate(url, api_key, params=None):
    """Generator that yields all records across paginated responses."""
    if params is None:
        params = {}
    # Default page size to 100 (Airtable max)
    params.setdefault("pageSize", 100)
    offset = None

    while True:
        url_params = dict(params)
        if offset:
            url_params["offset"] = offset
        qs = urllib.parse.urlencode(url_params, doseq=True)
        full_url = f"{url}?{qs}" if qs else url

        resp = _request(full_url, api_key)
        for rec in resp.get("records", []):
            yield rec
        offset = resp.get("offset")
        if not offset:
            break


def _build_record_table(records, fields=None, max_col_width=48):
    """Render records as a simple text table. Returns a list of lines."""
    if not records:
        return ["(no records)"]

    # Gather all field names
    all_fields = []
    for rec in records:
        for k in rec.get("fields", {}):
            if k not in all_fields:
                all_fields.append(k)
    if fields:
        all_fields = [f for f in all_fields if f in fields]

    # Build rows
    rows = []
    for rec in records:
        row = {"id": rec.get("id", "?")}
        row["createdTime"] = rec.get("createdTime", "")
        for f in all_fields:
            val = rec.get("fields", {}).get(f, "")
            row[f] = _fmt_field(val, max_col_width)
        rows.append(row)

    # Column widths
    col_widths = {"id": 18, "createdTime": 24}
    for f in all_fields:
        col_widths[f] = len(f)
    for row in rows:
        for col, val in row.items():
            w = len(str(val)) if not isinstance(val, str) else len(val)
            col_widths[col] = max(col_widths.get(col, 0), w)

    # Clamp width
    for col in col_widths:
        col_widths[col] = min(col_widths[col], max_col_width)

    # Header
    headers = ["id", "createdTime"] + all_fields
    sep = "-" * (sum(col_widths.get(h, 10) for h in headers) + len(headers) * 3 + 1)
    lines = [sep]
    header_line = "| "
    for h in headers:
        w = col_widths.get(h, 10)
        header_line += h.ljust(w) + " | "
    lines.append(header_line)
    lines.append(sep)

    for row in rows:
        line = "| "
        for h in headers:
            w = col_widths.get(h, 10)
            val = str(row.get(h, ""))
            if len(val) > w:
                val = val[: w - 3] + "..."
            line += val.ljust(w) + " | "
        lines.append(line)
    lines.append(sep)
    lines.append(f"  {len(records)} record(s)")
    return lines


def _fmt_field(val, max_width=48):
    """Format a field value for table display."""
    if val is None:
        return ""
    if isinstance(val, bool):
        return str(val)
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, list):
        strs = []
        for item in val[:5]:
            if isinstance(item, dict):
                strs.append(item.get("filename", item.get("url", str(item))[:40]))
            else:
                strs.append(str(item))
        s = ", ".join(strs)
        if len(val) > 5:
            s += f", …({len(val)} total)"
        return s if len(s) <= max_width else s[: max_width - 3] + "..."
    if isinstance(val, dict):
        s = json.dumps(val, ensure_ascii=False)
        return s if len(s) <= max_width else s[: max_width - 3] + "..."
    s = str(val)
    return s if len(s) <= max_width else s[: max_width - 3] + "..."


# ── Commands ──────────────────────────────────────────────────────────

def cmd_list_bases(args, api_key):
    """List all bases the token can access."""
    url = f"{META_BASE}/bases"
    resp = _request(url, api_key)
    bases = resp.get("bases", [])
    if not bases:
        print("No bases found (token may lack schema.bases:read scope).")
        return
    print(_maybe_color(_bold, f"Found {len(bases)} base(s):\n"))
    for b in bases:
        pid = b.get("id", "?")
        name = b.get("name", "(unnamed)")
        perm = b.get("permissionLevel", "unknown")
        print(f"  {_maybe_color(_cyan, pid)}  {_maybe_color(_green, name)}  [{perm}]")


def cmd_list_tables(args, api_key):
    """List tables and their schema for a base."""
    url = f"{META_BASE}/bases/{args.base_id}/tables"
    resp = _request(url, api_key)
    tables = resp.get("tables", [])
    if not tables:
        print("No tables found.")
        return
    print(_maybe_color(_bold, f"Base {_cyan(args.base_id)} — {len(tables)} table(s):\n"))
    for t in tables:
        tid = t.get("id", "?")
        name = t.get("name", "(unnamed)")
        desc = t.get("description", "")
        fields = t.get("fields", [])
        primary = t.get("primaryFieldId", "")
        primary_name = ""
        for f in fields:
            if f.get("id") == primary:
                primary_name = f.get("name", "")
                break
        print(f"  {_maybe_color(_cyan, tid)}  {_maybe_color(_green, name)}")
        if desc:
            print(f"       Description: {desc}")
        print(f"       Fields: {len(fields)}  |  Primary: {primary_name}")
        # Show field summary
        for f in fields:
            fname = f.get("name", "?")
            ftype = f.get("type", "?")
            opts = f.get("options", {})
            extra = ""
            if ftype in ("select", "multipleSelects"):
                choices = opts.get("choices", [])
                extra = f" [{len(choices)} options]"
            elif ftype == "linkedRecord":
                linked = opts.get("linkedTableId", "")
                extra = f" → tbl:{linked}"
            print(f"         {_maybe_color(_yellow, fname)} ({ftype}){extra}")
        print()


def cmd_schema(args, api_key):
    """Show detailed schema for a specific table."""
    url = f"{META_BASE}/bases/{args.base_id}/tables"
    resp = _request(url, api_key)
    tables = resp.get("tables", [])
    target = next((t for t in tables if t.get("id") == args.table or t.get("name") == args.table), None)
    if not target:
        print(_maybe_color(_red, f"Table '{args.table}' not found in base {args.base_id}."), file=sys.stderr)
        # Show available tables
        print("Available tables:")
        for t in tables:
            print(f"  {_maybe_color(_cyan, t['id'])}  {_maybe_color(_green, t.get('name', ''))}")
        sys.exit(1)

    print(_maybe_color(_bold, f"Table: {_green(target.get('name', ''))}  ({_cyan(target.get('id', ''))})"))
    print(f"Description: {target.get('description', '(none)')}")
    primary_id = target.get("primaryFieldId", "")
    print(f"Primary field ID: {primary_id}\n")

    fields = target.get("fields", [])
    print(f"{_maybe_color(_bold, f'Fields ({len(fields)}):')}")
    for f in fields:
        fid = f.get("id", "?")
        fname = f.get("name", "?")
        ftype = f.get("type", "?")
        fdesc = f.get("description", "")
        is_primary = "★" if fid == primary_id else " "
        print(f"  {is_primary} {_maybe_color(_cyan, fid)}  {_maybe_color(_green, fname)}  ({ftype})")
        if fdesc:
            print(f"       desc: {fdesc}")
        opts = f.get("options", {})
        if opts:
            choices = opts.get("choices", [])
            if choices:
                print(f"       options ({len(choices)}):")
                for c in choices:
                    c_name = c.get("name", "?")
                    c_id = c.get("id", "")
                    c_color = c.get("color", "")
                    print(f"         - {_maybe_color(_yellow, c_name)}  [{c_id}]  color={c_color}")
            linked = opts.get("linkedTableId", "")
            if linked:
                print(f"       linked table: {linked}")
            reverse = opts.get("isReversed", False)
            if reverse:
                print(f"       reversed: true")
            pref = opts.get("preferredDateFormat", "")
            if pref:
                print(f"       date format: {pref}")
        print()


def cmd_list_records(args, api_key):
    """List records with optional filter, sort, view, limit, offset."""
    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}"
    params = {}
    if args.limit:
        params["maxRecords"] = args.limit
    if args.offset:
        params["offset"] = args.offset
    if args.filter:
        params["filterByFormula"] = args.filter
    if args.view:
        params["view"] = args.view
    if args.fields:
        params["fields"] = args.fields
    if args.sort:
        # sort expected as "field1:asc,field2:desc"
        for i, s in enumerate(args.sort):
            parts = s.split(":")
            field = parts[0]
            direction = parts[1] if len(parts) > 1 else "asc"
            params[f"sort[{i}][field]"] = field
            params[f"sort[{i}][direction]"] = direction

    if args.all:
        records = list(_paginate(url, api_key, params))
    else:
        limit = args.limit or 100
        params["maxRecords"] = limit
        qs = urllib.parse.urlencode(params, doseq=True)
        full_url = f"{url}?{qs}" if qs else url
        resp = _request(full_url, api_key)
        records = resp.get("records", [])
        offset = resp.get("offset")
        if offset:
            print(
                _maybe_color(_yellow, f"  (More records available. Use --all to fetch all, or --offset {offset})"),
                file=sys.stderr,
            )

    if args.raw:
        # Compact JSON per line
        for rec in records:
            print(json.dumps(rec, ensure_ascii=False, separators=(",", ":")))
    elif args.pretty:
        print(json.dumps(records, ensure_ascii=False, indent=2))
    else:
        for line in _build_record_table(records, fields=args.fields):
            print(line)


def cmd_get_record(args, api_key):
    """Get a single record by ID."""
    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}/{args.record_id}"
    resp = _request(url, api_key)
    if args.pretty or args.raw:
        print(json.dumps(resp, ensure_ascii=False, indent=None if args.raw else 2))
    else:
        for line in _build_record_table([resp]):
            print(line)


def cmd_create_record(args, api_key):
    """Create one or more records."""
    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}"

    if args.data:
        fields = json.loads(args.data)
        body = {"fields": fields, "typecast": args.typecast}
        resp = _request(url, api_key, method="POST", data=body)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, dict):
            # Single record {fields: …}
            raw["typecast"] = raw.get("typecast", args.typecast)
            resp = _request(url, api_key, method="POST", data=raw)
        elif isinstance(raw, list):
            # Batch: list of {fields: …}
            body = {
                "records": raw,
                "typecast": args.typecast,
            }
            resp = _request(url, api_key, method="POST", data=body)
        else:
            print(_maybe_color(_red, "ERROR: File must contain a JSON object or array."), file=sys.stderr)
            sys.exit(1)
    else:
        print(_maybe_color(_red, "ERROR: Provide --data or --file."), file=sys.stderr)
        sys.exit(1)

    created = resp.get("records", [resp]) if "records" in resp else [resp]
    print(_maybe_color(_green, f"Created {len(created)} record(s):"))
    if args.pretty:
        print(json.dumps(created, ensure_ascii=False, indent=2))
    else:
        for rec in created:
            print(f"  {_maybe_color(_cyan, rec.get('id', '?'))}  {rec.get('createdTime', '')}")


def cmd_update_record(args, api_key):
    """Update a record by ID."""
    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}/{args.record_id}"
    fields = json.loads(args.data)
    body = {"fields": fields, "typecast": args.typecast}
    resp = _request(url, api_key, method="PATCH", data=body)
    print(_maybe_color(_green, f"Updated: {_cyan(resp.get('id', '?'))}"))
    if args.pretty:
        print(json.dumps(resp, ensure_ascii=False, indent=2))
    else:
        updated_fields = resp.get("fields", {})
        for k, v in list(updated_fields.items())[:10]:
            print(f"  {_maybe_color(_yellow, k)}: {_fmt_field(v)}")
        if len(updated_fields) > 10:
            print(f"  … ({len(updated_fields)} fields total)")


def cmd_delete_record(args, api_key):
    """Delete one or more records."""
    table_quoted = urllib.parse.quote(args.table, safe="")

    if args.ids:
        # Batch delete
        ids = json.loads(args.ids) if isinstance(args.ids, str) else args.ids
        if len(ids) > 10:
            print(_maybe_color(_red, "ERROR: Max 10 records per batch delete."), file=sys.stderr)
            sys.exit(1)
        params = urllib.parse.urlencode([("records[]", rid) for rid in ids], doseq=True)
        url = f"{API_BASE}/{args.base_id}/{table_quoted}?{params}"
        resp = _request(url, api_key, method="DELETE")
        deleted = resp.get("records", [])
        print(_maybe_color(_green, f"Deleted {len(deleted)} record(s):"))
        for rec in deleted:
            print(f"  {_maybe_color(_cyan, rec.get('id', '?'))}  deleted={rec.get('deleted', False)}")
    else:
        url = f"{API_BASE}/{args.base_id}/{table_quoted}/{args.record_id}"
        resp = _request(url, api_key, method="DELETE")
        rid = resp.get("id", args.record_id)
        deleted = resp.get("deleted", False)
        if deleted:
            print(_maybe_color(_green, f"Deleted: {_cyan(rid)}"))
        else:
            print(_maybe_color(_yellow, f"Record {_cyan(rid)} may not exist or was already deleted."))


def cmd_batch_create(args, api_key):
    """Batch create records from a JSON file (max 10 per request, auto-paginated)."""
    if not args.file:
        print(_maybe_color(_red, "ERROR: --file is required."), file=sys.stderr)
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        records_data = json.load(f)

    if isinstance(records_data, dict):
        records_data = [records_data]
    if not isinstance(records_data, list):
        print(_maybe_color(_red, "ERROR: File must contain a JSON array of objects or a single object."), file=sys.stderr)
        sys.exit(1)

    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}"
    total = len(records_data)
    created_count = 0

    print(f"Batch creating {total} record(s) in chunks of up to 10…")
    for i in range(0, total, 10):
        chunk = records_data[i : i + 10]
        body = {"records": [{"fields": r} if not r.get("fields") else r for r in chunk], "typecast": args.typecast}
        resp = _request(url, api_key, method="POST", data=body)
        batch = resp.get("records", [])
        created_count += len(batch)
        print(f"  Chunk {i // 10 + 1}: created {len(batch)} record(s)")
        for rec in batch:
            print(f"    {_maybe_color(_cyan, rec.get('id', '?'))}")
        if i + 10 < total:
            time.sleep(0.25)  # Stay under 5 req/s

    print(_maybe_color(_green, f"Done. Created {created_count}/{total} record(s)."))


def cmd_batch_delete(args, api_key):
    """Batch delete records by IDs (max 10 at a time, auto-paginated)."""
    if not args.ids:
        print(_maybe_color(_red, "ERROR: --ids is required (JSON array of record IDs)."), file=sys.stderr)
        sys.exit(1)

    ids = json.loads(args.ids) if isinstance(args.ids, str) else args.ids
    if not isinstance(ids, list):
        print(_maybe_color(_red, "ERROR: --ids must be a JSON array."), file=sys.stderr)
        sys.exit(1)

    table_quoted = urllib.parse.quote(args.table, safe="")
    total = len(ids)
    deleted_count = 0

    print(f"Batch deleting {total} record(s) in chunks of up to 10…")
    for i in range(0, total, 10):
        chunk = ids[i : i + 10]
        params = urllib.parse.urlencode([("records[]", rid) for rid in chunk], doseq=True)
        url = f"{API_BASE}/{args.base_id}/{table_quoted}?{params}"
        resp = _request(url, api_key, method="DELETE")
        batch = resp.get("records", [])
        deleted_count += len(batch)
        print(f"  Chunk {i // 10 + 1}: deleted {len(batch)} record(s)")
        for rec in batch:
            print(f"    {_maybe_color(_cyan, rec.get('id', '?'))}  deleted={rec.get('deleted', False)}")
        if i + 10 < total:
            time.sleep(0.25)

    print(_maybe_color(_green, f"Done. Deleted {deleted_count}/{total} record(s)."))


def cmd_upsert(args, api_key):
    """Upsert records by a merge field."""
    if not args.merge_on:
        print(_maybe_color(_red, "ERROR: --merge-on (fieldsToMergeOn) is required."), file=sys.stderr)
        sys.exit(1)
    if not args.file and not args.data:
        print(_maybe_color(_red, "ERROR: Provide --file or --data with record fields."), file=sys.stderr)
        sys.exit(1)

    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}"

    if args.data:
        records_data = [json.loads(args.data)]
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            records_data = json.load(f)
        if isinstance(records_data, dict):
            records_data = [records_data]

    merge_fields = [m.strip() for m in args.merge_on.split(",")]

    body = {
        "performUpsert": {"fieldsToMergeOn": merge_fields},
        "records": [{"fields": r} for r in records_data],
        "typecast": args.typecast,
    }
    resp = _request(url, api_key, method="PATCH", data=body)
    created = resp.get("createdRecords", [])
    updated = resp.get("updatedRecords", [])
    records_out = resp.get("records", [])

    print(_maybe_color(_green, f"Upsert complete: {len(created)} created, {len(updated)} updated."))
    if args.pretty:
        print(json.dumps(records_out, ensure_ascii=False, indent=2))
    else:
        for rec in records_out[:20]:
            print(f"  {_maybe_color(_cyan, rec.get('id', '?'))}")
        if len(records_out) > 20:
            print(f"  … ({len(records_out)} total records)")


def cmd_search(args, api_key):
    """Search for records where a field equals a value."""
    formula = f"{{{args.field}}}='{args.value}'"
    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}"

    params = {"filterByFormula": formula}
    if args.limit:
        params["maxRecords"] = args.limit

    qs = urllib.parse.urlencode(params, doseq=True)
    full_url = f"{url}?{qs}"
    resp = _request(full_url, api_key)
    records = resp.get("records", [])

    print(_maybe_color(_bold, f"Search: {_cyan(args.field)} = '{_green(args.value)}'  →  {len(records)} match(es)\n"))
    if args.raw:
        for rec in records:
            print(json.dumps(rec, ensure_ascii=False, separators=(",", ":")))
    elif args.pretty:
        print(json.dumps(records, ensure_ascii=False, indent=2))
    else:
        for line in _build_record_table(records, fields=args.fields):
            print(line)


def cmd_count(args, api_key):
    """Count records with optional filter formula."""
    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}"
    params = {"maxRecords": 1}
    if args.filter:
        params["filterByFormula"] = args.filter

    qs = urllib.parse.urlencode(params, doseq=True)
    full_url = f"{url}?{qs}"
    resp = _request(full_url, api_key)
    total = len(resp.get("records", []))

    # If there's an offset, there are more records — but Airtable doesn't
    # return a total count. We'll paginate to count exactly.
    if resp.get("offset") or total == 1:
        # Count by paginating through all records
        all_records = list(_paginate(url, api_key, params))
        total = len(all_records)

    filter_label = f" (filter: {args.filter})" if args.filter else ""
    print(f"Record count: {_maybe_color(_bold, str(total))}{filter_label}")
    return total


def cmd_export(args, api_key):
    """Export all records as JSON lines or CSV."""
    url = f"{API_BASE}/{args.base_id}/{urllib.parse.quote(args.table, safe='')}"
    params = {}
    if args.filter:
        params["filterByFormula"] = args.filter
    if args.view:
        params["view"] = args.view

    print(_maybe_color(_yellow, f"Fetching all records…"), file=sys.stderr)
    records = list(_paginate(url, api_key, params))
    print(_maybe_color(_green, f"Fetched {len(records)} records."), file=sys.stderr)

    fields = args.fields  # optional field subset
    fmt = args.format or "json"

    if fmt == "json":
        # JSON lines — one object per line
        for rec in records:
            out = {"id": rec.get("id"), "createdTime": rec.get("createdTime")}
            flds = rec.get("fields", {})
            if fields:
                out["fields"] = {k: flds.get(k) for k in fields if k in flds}
            else:
                out["fields"] = flds
            print(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    elif fmt == "csv":
        # Gather all field names across all records
        all_fields = list(fields) if fields else []
        if not all_fields:
            seen = set()
            for rec in records:
                for k in rec.get("fields", {}):
                    if k not in seen:
                        all_fields.append(k)
                        seen.add(k)
        writer = csv.writer(sys.stdout)
        writer.writerow(["id", "createdTime"] + all_fields)
        for rec in records:
            row = [rec.get("id", ""), rec.get("createdTime", "")]
            flds = rec.get("fields", {})
            for f in all_fields:
                val = flds.get(f, "")
                row.append(_csv_val(val))
            writer.writerow(row)
    else:
        print(_maybe_color(_red, f"Unsupported format: {fmt}. Use 'json' or 'csv'."), file=sys.stderr)
        sys.exit(1)


def _csv_val(val):
    """Convert a field value to a CSV-safe string."""
    if val is None:
        return ""
    if isinstance(val, (bool, int, float)):
        return str(val)
    if isinstance(val, list):
        return "; ".join(str(v) if not isinstance(v, dict) else v.get("url", json.dumps(v, ensure_ascii=False)) for v in val)
    if isinstance(val, dict):
        return json.dumps(val, ensure_ascii=False)
    return str(val)


def cmd_version(args=None, api_key=None):
    """Print version info."""
    print(VERSION_STRING)
    print(f"Platform: {sys.platform}")
    print(f"API Base: {API_BASE}")


# ── Argument parser ───────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="airtable_cli.py",
        description=f"{_maybe_color(_bold, 'Airtable CLI')} — Read, create, update, delete, and search Airtable records.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Environment:\n"
            "  AIRTABLE_API_KEY    Required. Personal Access Token (pat...) or legacy API key.\n"
            "\n"
            "Examples:\n"
            "  python airtable_cli.py list-bases\n"
            "  python airtable_cli.py list-records appXXXXX tblXXXXX --limit 10\n"
            "  python airtable_cli.py create-record appXXXXX tblXXXXX --data '{\"Name\":\"Hello\"}'\n"
            "  python airtable_cli.py search appXXXXX tblXXXXX Email user@example.com\n"
            "  python airtable_cli.py export appXXXXX tblXXXXX --format csv > data.csv\n"
        ),
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit")

    sub = parser.add_subparsers(dest="command", title="Commands")

    # ── list-bases ──
    p_bases = sub.add_parser("list-bases", help="List all accessible bases")
    p_bases.set_defaults(func=cmd_list_bases)

    # ── list-tables ──
    p_tables = sub.add_parser("list-tables", help="List tables and schema for a base")
    p_tables.add_argument("base_id", help="Base ID (appXXXXXXXXXXXXXX)")
    p_tables.set_defaults(func=cmd_list_tables)

    # ── schema ──
    p_schema = sub.add_parser("schema", help="Show detailed field schema for a table")
    p_schema.add_argument("base_id", help="Base ID")
    p_schema.add_argument("table", help="Table ID (tblXXX) or name")
    p_schema.set_defaults(func=cmd_schema)

    # ── list-records ──
    p_list = sub.add_parser("list-records", help="List records (with optional filter, sort, view)")
    p_list.add_argument("base_id", help="Base ID")
    p_list.add_argument("table", help="Table ID or name")
    p_list.add_argument("--limit", type=int, default=0, help="Max records (default: 100, use with --all for unlimited)")
    p_list.add_argument("--offset", help="Pagination offset token")
    p_list.add_argument("--filter", help="filterByFormula (e.g. \"{Status}='Todo'\")")
    p_list.add_argument("--view", help="Named view to apply")
    p_list.add_argument("--fields", nargs="+", help="Fields to include (space-separated)")
    p_list.add_argument("--sort", action="append", help="Sort: 'field:asc' or 'field:desc' (repeatable)")
    p_list.add_argument("--all", action="store_true", help="Fetch ALL records (auto-paginate)")
    p_list.add_argument("--raw", action="store_true", help="JSON lines output")
    p_list.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    p_list.set_defaults(func=cmd_list_records)

    # ── get-record ──
    p_get = sub.add_parser("get-record", help="Get a single record by ID")
    p_get.add_argument("base_id", help="Base ID")
    p_get.add_argument("table", help="Table ID or name")
    p_get.add_argument("record_id", help="Record ID (recXXXXXXXXXXXXXX)")
    p_get.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    p_get.add_argument("--raw", action="store_true", help="Compact JSON output")
    p_get.set_defaults(func=cmd_get_record)

    # ── create-record ──
    p_create = sub.add_parser("create-record", help="Create one or more records")
    p_create.add_argument("base_id", help="Base ID")
    p_create.add_argument("table", help="Table ID or name")
    p_create.add_argument("--data", help="JSON string of fields: '{\"Name\":\"Test\"}'")
    p_create.add_argument("--file", help="JSON file with record(s) (array or object)")
    p_create.add_argument("--typecast", action="store_true", help="Auto-convert values / create options")
    p_create.add_argument("--pretty", action="store_true", help="Pretty-print result JSON")
    p_create.set_defaults(func=cmd_create_record)

    # ── update-record ──
    p_update = sub.add_parser("update-record", help="Update a record by ID")
    p_update.add_argument("base_id", help="Base ID")
    p_update.add_argument("table", help="Table ID or name")
    p_update.add_argument("record_id", help="Record ID")
    p_update.add_argument("--data", required=True, help="JSON string of fields to update: '{\"Status\":\"Done\"}'")
    p_update.add_argument("--typecast", action="store_true", help="Auto-convert values")
    p_update.add_argument("--pretty", action="store_true", help="Pretty-print result JSON")
    p_update.set_defaults(func=cmd_update_record)

    # ── delete-record ──
    p_delete = sub.add_parser("delete-record", help="Delete one or more records")
    p_delete.add_argument("base_id", help="Base ID")
    p_delete.add_argument("table", help="Table ID or name")
    p_delete.add_argument("record_id", nargs="?", help="Single record ID to delete")
    p_delete.add_argument("--ids", help="JSON array of record IDs (batch): '[\"rec1\",\"rec2\"]'")
    p_delete.set_defaults(func=cmd_delete_record)

    # ── batch-create ──
    p_bc = sub.add_parser("batch-create", help="Batch create records from a JSON file (auto-chunked)")
    p_bc.add_argument("base_id", help="Base ID")
    p_bc.add_argument("table", help="Table ID or name")
    p_bc.add_argument("--file", required=True, help="JSON file with records (array of field objects)")
    p_bc.add_argument("--typecast", action="store_true", help="Auto-convert values")
    p_bc.set_defaults(func=cmd_batch_create)

    # ── batch-delete ──
    p_bd = sub.add_parser("batch-delete", help="Batch delete records by IDs (auto-chunked)")
    p_bd.add_argument("base_id", help="Base ID")
    p_bd.add_argument("table", help="Table ID or name")
    p_bd.add_argument("--ids", required=True, help="JSON array of record IDs")
    p_bd.set_defaults(func=cmd_batch_delete)

    # ── upsert ──
    p_up = sub.add_parser("upsert", help="Upsert records by merge field(s)")
    p_up.add_argument("base_id", help="Base ID")
    p_up.add_argument("table", help="Table ID or name")
    p_up.add_argument("--merge-on", required=True, help="Field name(s) to merge on (comma-separated)")
    p_up.add_argument("--data", help="JSON string of fields for a single record")
    p_up.add_argument("--file", help="JSON file with records (array of field objects)")
    p_up.add_argument("--typecast", action="store_true", help="Auto-convert values")
    p_up.add_argument("--pretty", action="store_true", help="Pretty-print result JSON")
    p_up.set_defaults(func=cmd_upsert)

    # ── search ──
    p_search = sub.add_parser("search", help="Search records by field = value")
    p_search.add_argument("base_id", help="Base ID")
    p_search.add_argument("table", help="Table ID or name")
    p_search.add_argument("field", help="Field name to search")
    p_search.add_argument("value", help="Exact value to match")
    p_search.add_argument("--limit", type=int, default=0, help="Max results (default: all)")
    p_search.add_argument("--fields", nargs="+", help="Fields to display")
    p_search.add_argument("--raw", action="store_true", help="JSON lines output")
    p_search.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    p_search.set_defaults(func=cmd_search)

    # ── count ──
    p_count = sub.add_parser("count", help="Count records (optional filter formula)")
    p_count.add_argument("base_id", help="Base ID")
    p_count.add_argument("table", help="Table ID or name")
    p_count.add_argument("--filter", help="filterByFormula")
    p_count.set_defaults(func=cmd_count)

    # ── export ──
    p_export = sub.add_parser("export", help="Export all records as JSON or CSV")
    p_export.add_argument("base_id", help="Base ID")
    p_export.add_argument("table", help="Table ID or name")
    p_export.add_argument("--format", choices=["json", "csv"], default="json", help="Output format (default: json)")
    p_export.add_argument("--filter", help="filterByFormula")
    p_export.add_argument("--view", help="Named view")
    p_export.add_argument("--fields", nargs="+", help="Fields to export (default: all)")
    p_export.set_defaults(func=cmd_export)

    # ── version (subcommand) ──
    p_ver = sub.add_parser("version", help="Show version info")
    p_ver.set_defaults(func=cmd_version)

    return parser


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Handle --version flag before any subcommand check
    if hasattr(args, "version") and args.version:
        cmd_version()
        return

    if not args.command:
        parser.print_help()
        sys.exit(1)

    api_key = get_api_key()
    args.func(args, api_key)


if __name__ == "__main__":
    main()
