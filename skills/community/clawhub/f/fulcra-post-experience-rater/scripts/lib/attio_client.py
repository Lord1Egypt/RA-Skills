#!/usr/bin/env python3
"""Minimal Attio REST client for the Fulcra concierge skills.

stdlib-only (urllib) so it runs under any `uv run`/python without extra installs,
mirroring the Fulcra annotation helper. It is BOTH a library (import the functions)
and a CLI (skills shell out to it). Every write supports --dry-run, and the token is
loaded via concierge_secrets (env ATTIO_API_KEY or ~/.fulcra-concierge/secrets.json) and
never printed.

Attio shapes used (verify against the live API; envelopes are the documented ones):
  - query:   POST /v2/objects/{object}/records/query   {"filter": {...}, "limit": N}
  - create:  POST /v2/objects/{object}/records         {"data": {"values": {...}}}
  - assert:  PUT  /v2/objects/{object}/records?matching_attribute=slug
  - update:  PATCH /v2/objects/{object}/records/{id}   {"data": {"values": {...}}}
  - note:    POST /v2/notes  {"data": {"parent_object","parent_record_id","title",
                                        "format":"plaintext","content"}}
Record id lives at response["data"]["id"]["record_id"].
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from concierge_secrets import get_secret  # noqa: E402

API_BASE = os.environ.get("ATTIO_API_BASE", "https://api.attio.com").rstrip("/")


def fail(message: str, code: int = 1) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2), file=sys.stderr)
    raise SystemExit(code)


def _request(method: str, path: str, payload: Any | None = None,
             params: dict[str, str] | None = None) -> tuple[int, Any]:
    token = get_secret("ATTIO_API_KEY", required=True)
    url = API_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode() or "{}"
            return resp.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw": body[:600]}
        return exc.code, parsed


# ---- reads -------------------------------------------------------------------

def list_objects() -> list[dict[str, Any]]:
    status, body = _request("GET", "/v2/objects")
    if status != 200:
        fail(f"list_objects failed: HTTP {status}: {json.dumps(body)[:400]}")
    return body.get("data", []) if isinstance(body, dict) else []


def query_records(object_slug: str, filter_: dict | None = None, limit: int = 25,
                  sorts: list | None = None) -> list[dict[str, Any]]:
    payload: dict[str, Any] = {"limit": limit}
    if filter_:
        payload["filter"] = filter_
    if sorts:
        payload["sorts"] = sorts
    elif not filter_:
        # Attio rejects a query with neither a filter nor a sort. Default to
        # newest-first so "list recent records" works without a filter.
        payload["sorts"] = [{"attribute": "created_at", "direction": "desc"}]
    status, body = _request("POST", f"/v2/objects/{object_slug}/records/query", payload)
    if status != 200:
        fail(f"query {object_slug} failed: HTTP {status}: {json.dumps(body)[:400]}")
    return body.get("data", []) if isinstance(body, dict) else []


def find_people(name: str | None = None, email: str | None = None, limit: int = 25) -> list[dict[str, Any]]:
    flt: dict[str, Any] = {}
    if email:
        flt["email_addresses"] = email
    if name:
        flt["name"] = name
    return query_records("people", flt or None, limit=limit)


def find_companies(name: str | None = None, limit: int = 25) -> list[dict[str, Any]]:
    flt = {"name": name} if name else None
    return query_records("companies", flt, limit=limit)


# ---- writes ------------------------------------------------------------------

def people_values(*, first: str | None = None, last: str | None = None,
                  full_name: str | None = None, email: str | None = None,
                  job_title: str | None = None, description: str | None = None,
                  phone: str | None = None) -> dict[str, Any]:
    values: dict[str, Any] = {}
    if first or last or full_name:
        nm: dict[str, str] = {}
        if first:
            nm["first_name"] = first
        if last:
            nm["last_name"] = last
        nm["full_name"] = full_name or " ".join(p for p in [first, last] if p)
        values["name"] = [nm]
    if email:
        values["email_addresses"] = [email]
    if phone:
        values["phone_numbers"] = [phone]
    if job_title:
        values["job_title"] = job_title
    if description:
        values["description"] = description
    return values


def record_id_of(record: dict[str, Any]) -> str | None:
    rid = record.get("id")
    if isinstance(rid, dict):
        return rid.get("record_id")
    return rid if isinstance(rid, str) else None


def create_record(object_slug: str, values: dict, dry_run: bool = False) -> dict[str, Any]:
    payload = {"data": {"values": values}}
    if dry_run:
        return {"ok": True, "dry_run": True, "method": "POST", "object": object_slug, "payload": payload}
    status, body = _request("POST", f"/v2/objects/{object_slug}/records", payload)
    if status not in (200, 201):
        fail(f"create {object_slug} failed: HTTP {status}: {json.dumps(body)[:400]}")
    return {"ok": True, "record_id": record_id_of(body.get("data", {})), "data": body.get("data")}


def assert_record(object_slug: str, values: dict, matching_attribute: str,
                  dry_run: bool = False) -> dict[str, Any]:
    payload = {"data": {"values": values}}
    if dry_run:
        return {"ok": True, "dry_run": True, "method": "PUT", "object": object_slug,
                "matching_attribute": matching_attribute, "payload": payload}
    status, body = _request("PUT", f"/v2/objects/{object_slug}/records", payload,
                            params={"matching_attribute": matching_attribute})
    if status not in (200, 201):
        fail(f"assert {object_slug} failed: HTTP {status}: {json.dumps(body)[:400]}")
    return {"ok": True, "record_id": record_id_of(body.get("data", {})), "data": body.get("data")}


def update_record(object_slug: str, record_id: str, values: dict, dry_run: bool = False) -> dict[str, Any]:
    payload = {"data": {"values": values}}
    if dry_run:
        return {"ok": True, "dry_run": True, "method": "PATCH", "object": object_slug,
                "record_id": record_id, "payload": payload}
    status, body = _request("PATCH", f"/v2/objects/{object_slug}/records/{record_id}", payload)
    if status != 200:
        fail(f"update {object_slug}/{record_id} failed: HTTP {status}: {json.dumps(body)[:400]}")
    return {"ok": True, "record_id": record_id, "data": body.get("data")}


def delete_record(object_slug: str, record_id: str, dry_run: bool = False) -> dict[str, Any]:
    """Delete a record. Deleting a person also removes notes attached to it."""
    if dry_run:
        return {"ok": True, "dry_run": True, "method": "DELETE", "object": object_slug, "record_id": record_id}
    status, body = _request("DELETE", f"/v2/objects/{object_slug}/records/{record_id}")
    if status not in (200, 204):
        fail(f"delete {object_slug}/{record_id} failed: HTTP {status}: {json.dumps(body)[:400]}")
    return {"ok": True, "deleted": record_id}


def list_notes(parent_object: str, parent_record_id: str, limit: int = 10) -> list[dict[str, Any]]:
    """List notes attached to a record (newest first), normalized to plain fields."""
    status, body = _request("GET", "/v2/notes", params={
        "parent_object": parent_object, "parent_record_id": parent_record_id, "limit": str(limit)})
    if status != 200:
        fail(f"list_notes failed: HTTP {status}: {json.dumps(body)[:400]}")
    out: list[dict[str, Any]] = []
    for n in (body.get("data", []) if isinstance(body, dict) else []):
        nid = n.get("id", {})
        out.append({
            "note_id": nid.get("note_id") if isinstance(nid, dict) else nid,
            "title": n.get("title"),
            "created_at": n.get("created_at"),
            "content": n.get("content_plaintext") or n.get("content_markdown") or n.get("content"),
        })
    out.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return out


def add_note(parent_object: str, parent_record_id: str, title: str, content: str,
             dry_run: bool = False) -> dict[str, Any]:
    payload = {"data": {"parent_object": parent_object, "parent_record_id": parent_record_id,
                        "title": title, "format": "plaintext", "content": content}}
    if dry_run:
        return {"ok": True, "dry_run": True, "method": "POST", "endpoint": "/v2/notes", "payload": payload}
    status, body = _request("POST", "/v2/notes", payload)
    if status not in (200, 201):
        fail(f"add_note failed: HTTP {status}: {json.dumps(body)[:400]}")
    note = body.get("data", {}) if isinstance(body, dict) else {}
    nid = note.get("id", {})
    return {"ok": True, "note_id": nid.get("note_id") if isinstance(nid, dict) else nid}


# ---- CLI ---------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Attio client for the Fulcra concierge")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("objects", help="List objects (connection + schema test)")

    fp = sub.add_parser("find-person")
    fp.add_argument("--name")
    fp.add_argument("--email")
    fp.add_argument("--limit", type=int, default=25)

    fc = sub.add_parser("find-company")
    fc.add_argument("--name")
    fc.add_argument("--limit", type=int, default=25)

    up = sub.add_parser("upsert-person", help="Assert (create-or-update) a person by email")
    up.add_argument("--first")
    up.add_argument("--last")
    up.add_argument("--full-name")
    up.add_argument("--email", required=True, help="Matching attribute for the upsert")
    up.add_argument("--job-title")
    up.add_argument("--description")
    up.add_argument("--phone")
    up.add_argument("--dry-run", action="store_true")

    rc = sub.add_parser("recent", help="List most-recently-created records of an object")
    rc.add_argument("--object", default="people")
    rc.add_argument("--limit", type=int, default=10)
    rc.add_argument("--slugs-only", action="store_true",
                    help="Print only the value attribute slugs of the first record")

    dl = sub.add_parser("delete-record")
    dl.add_argument("--object", default="people")
    dl.add_argument("--record-id", required=True)
    dl.add_argument("--dry-run", action="store_true")

    nls = sub.add_parser("notes", help="List notes attached to a record (newest first)")
    nls.add_argument("--object", default="people")
    nls.add_argument("--record-id", required=True)
    nls.add_argument("--limit", type=int, default=10)

    nt = sub.add_parser("note")
    nt.add_argument("--object", default="people")
    nt.add_argument("--record-id", required=True)
    nt.add_argument("--title", required=True)
    nt.add_argument("--content", required=True)
    nt.add_argument("--dry-run", action="store_true")

    upd = sub.add_parser("update")
    upd.add_argument("--object", default="people")
    upd.add_argument("--record-id", required=True)
    upd.add_argument("--values-json", required=True, help="Raw Attio values dict as JSON")
    upd.add_argument("--dry-run", action="store_true")

    args = p.parse_args()
    if args.command == "objects":
        objs = list_objects()
        result = {"ok": True, "count": len(objs),
                  "objects": [{"slug": o.get("api_slug"), "name": (o.get("singular_noun") or o.get("plural_noun"))}
                              for o in objs]}
    elif args.command == "find-person":
        if not args.name and not args.email:
            fail("find-person needs --name or --email")
        people = find_people(args.name, args.email, args.limit)
        result = {"ok": True, "count": len(people),
                  "people": [{"record_id": record_id_of(r), "values": r.get("values", {})} for r in people]}
    elif args.command == "recent":
        recs = query_records(args.object, None, limit=args.limit)
        if args.slugs_only:
            slugs = sorted((recs[0].get("values") or {}).keys()) if recs else []
            result = {"ok": True, "object": args.object, "count": len(recs), "value_slugs": slugs}
        else:
            result = {"ok": True, "object": args.object, "count": len(recs),
                      "records": [{"record_id": record_id_of(r), "values": r.get("values", {})} for r in recs]}
    elif args.command == "delete-record":
        result = delete_record(args.object, args.record_id, dry_run=args.dry_run)
    elif args.command == "find-company":
        cos = find_companies(args.name, args.limit)
        result = {"ok": True, "count": len(cos),
                  "companies": [{"record_id": record_id_of(r), "values": r.get("values", {})} for r in cos]}
    elif args.command == "upsert-person":
        values = people_values(first=args.first, last=args.last, full_name=args.full_name,
                               email=args.email, job_title=args.job_title,
                               description=args.description, phone=args.phone)
        result = assert_record("people", values, "email_addresses", dry_run=args.dry_run)
    elif args.command == "notes":
        notes = list_notes(args.object, args.record_id, args.limit)
        result = {"ok": True, "count": len(notes), "notes": notes}
    elif args.command == "note":
        result = add_note(args.object, args.record_id, args.title, args.content, dry_run=args.dry_run)
    elif args.command == "update":
        try:
            values = json.loads(args.values_json)
        except json.JSONDecodeError as exc:
            fail(f"--values-json is not valid JSON: {exc}")
        result = update_record(args.object, args.record_id, values, dry_run=args.dry_run)
    else:
        fail("unknown command")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
