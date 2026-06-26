#!/usr/bin/env python3
"""BillClaw CLI: JSON in / JSON out for Agent integration."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from db import (
    add_user_category,
    delete_by_ids,
    get_connection,
    insert_transaction,
    list_user_categories,
    query_transactions,
    update_category_for_ids,
    user_category_exists,
)
from parser import parse_natural_bundle, validate_record_fields
from report import build_report, highlights_json_for_agent


def _db_path_from_env() -> Path | None:
    p = os.environ.get("BILLCLAW_DB_PATH")
    return Path(p) if p else None


def _load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        raw = Path(args.json).read_text(encoding="utf-8")
    elif args.json_string:
        raw = args.json_string
    else:
        if sys.stdin.isatty():
            return {}
        raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return json.loads(raw)


def _out(obj: dict[str, Any]) -> None:
    print(json.dumps(obj, ensure_ascii=False))


def cmd_add(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    parse_text = payload.get("parse_text")
    now = datetime.now()
    if parse_text:
        bundle = parse_natural_bundle(str(parse_text), now)
        if not payload.get("date") and bundle.get("time", {}).get("date"):
            payload["date"] = bundle["time"]["date"]
        if payload.get("amount") is None and bundle.get("amount", {}).get("value") is not None:
            payload["amount"] = bundle["amount"]["value"]
        if not payload.get("type") and bundle.get("type_hint", {}).get("type"):
            payload["type"] = bundle["type_hint"]["type"]
        if not payload.get("category") and bundle.get("category_hint", {}).get("category"):
            payload["category"] = bundle["category_hint"]["category"]
        if not payload.get("note"):
            payload["note"] = str(parse_text).strip()[:500]

    for k in ("date", "type", "category", "amount"):
        if k not in payload or payload[k] is None:
            return {"ok": False, "error": f"缺少字段: {k}", "data": {}}

    date_str = str(payload["date"])
    type_ = str(payload["type"])
    category = str(payload["category"])
    amount = float(payload["amount"])
    note = payload.get("note")

    check = validate_record_fields(
        date_str=date_str, type_=type_, category=category, amount=amount, note=note
    )
    if not check.get("valid", True):
        return {
            "ok": False,
            "error": "; ".join(check.get("issues") or []),
            "data": {},
        }
    extra: dict[str, Any] = {}
    if check.get("suspicious"):
        extra["suspicious"] = True
        extra["suspicious_reason"] = check.get("reason")

    with get_connection(db_path) as conn:
        tid = insert_transaction(
            conn,
            date=date_str[:10],
            type_=type_,
            category=category,
            amount=amount,
            note=str(note) if note is not None else None,
            source=str(payload.get("source") or "manual"),
        )
    data = {"id": tid, **extra}
    return {"ok": True, "error": None, "data": data}


def cmd_query(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    with get_connection(db_path) as conn:
        rows = query_transactions(
            conn,
            date_from=payload.get("date_from"),
            date_to=payload.get("date_to"),
            type_=payload.get("type"),
            category=payload.get("category"),
            category_like=payload.get("category_like"),
            note_like=payload.get("note_like"),
            keyword_in_note=payload.get("keyword_in_note"),
            limit=payload.get("limit", 500),
        )
    return {"ok": True, "error": None, "data": {"rows": rows, "count": len(rows)}}


def cmd_delete_preview(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    with get_connection(db_path) as conn:
        rows = query_transactions(
            conn,
            date_from=payload.get("date_from"),
            date_to=payload.get("date_to"),
            type_=payload.get("type"),
            category=payload.get("category"),
            category_like=payload.get("category_like"),
            note_like=payload.get("note_like"),
            keyword_in_note=payload.get("keyword_in_note"),
            limit=payload.get("limit", 500),
        )
    ids = [int(r["id"]) for r in rows]
    return {
        "ok": True,
        "error": None,
        "data": {
            "preview_rows": rows,
            "ids": ids,
            "count": len(ids),
            "hint": "请用户确认后使用 delete-confirm 并传入 ids",
        },
    }


def cmd_delete_confirm(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    ids = payload.get("ids")
    if not ids or not isinstance(ids, list):
        return {"ok": False, "error": "需要 ids 数组", "data": {}}
    ids_int = [int(x) for x in ids]
    with get_connection(db_path) as conn:
        n = delete_by_ids(conn, ids_int)
    return {"ok": True, "error": None, "data": {"deleted": n}}


def cmd_merge_preview(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    with get_connection(db_path) as conn:
        rows = query_transactions(
            conn,
            date_from=payload.get("date_from"),
            date_to=payload.get("date_to"),
            type_=payload.get("type") or "支出",
            category=payload.get("old_category"),
            category_like=payload.get("old_category_like"),
            note_like=payload.get("note_like"),
            keyword_in_note=payload.get("keyword_in_note"),
            limit=payload.get("limit", 500),
        )
    ids = [int(r["id"]) for r in rows]
    return {
        "ok": True,
        "error": None,
        "data": {
            "preview_rows": rows,
            "ids": ids,
            "count": len(ids),
            "hint": "请用户确认后使用 merge-confirm 传入 ids 与 new_category",
        },
    }


def cmd_merge_confirm(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    ids = payload.get("ids")
    new_cat = payload.get("new_category")
    if not ids or not isinstance(ids, list) or not new_cat:
        return {"ok": False, "error": "需要 ids 与 new_category", "data": {}}
    ids_int = [int(x) for x in ids]
    with get_connection(db_path) as conn:
        n = update_category_for_ids(conn, ids_int, str(new_cat))
    return {"ok": True, "error": None, "data": {"updated": n, "new_category": new_cat}}


def cmd_category_add(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    name = payload.get("name")
    kind = payload.get("kind")
    if not name or kind not in ("收入", "支出"):
        return {"ok": False, "error": "需要 name 与 kind(收入|支出)", "data": {}}
    with get_connection(db_path) as conn:
        if user_category_exists(conn, str(name)):
            return {"ok": False, "error": "分类已存在", "data": {}}
        cid = add_user_category(conn, str(name), str(kind))
    return {"ok": True, "error": None, "data": {"id": cid, "name": name, "kind": kind}}


def cmd_category_list(_payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    with get_connection(db_path) as conn:
        rows = list_user_categories(conn)
    return {"ok": True, "error": None, "data": {"user_categories": rows}}


def cmd_report(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    out_dir = payload.get("output_dir")
    rep = build_report(
        db_path=db_path,
        date_from=payload.get("date_from"),
        date_to=payload.get("date_to"),
        output_dir=out_dir,
    )
    rep["agent_json"] = highlights_json_for_agent(rep)
    return {"ok": True, "error": None, "data": rep}


def cmd_export_csv(payload: dict[str, Any], db_path: Path | None) -> dict[str, Any]:
    path = Path(payload.get("path") or "billclaw_export.csv")
    with get_connection(db_path) as conn:
        rows = query_transactions(
            conn,
            date_from=payload.get("date_from"),
            date_to=payload.get("date_to"),
            type_=payload.get("type"),
            category=payload.get("category"),
            limit=payload.get("limit", 10000),
        )
    if not rows:
        path.write_text("", encoding="utf-8")
        return {"ok": True, "error": None, "data": {"path": str(path.resolve()), "rows": 0}}

    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    return {"ok": True, "error": None, "data": {"path": str(path.resolve()), "rows": len(rows)}}


def cmd_parse(payload: dict[str, Any]) -> dict[str, Any]:
    text = payload.get("text") or payload.get("parse_text") or ""
    now_s = payload.get("now")
    now = datetime.fromisoformat(now_s) if now_s else datetime.now()
    bundle = parse_natural_bundle(str(text), now)
    return {"ok": True, "error": None, "data": bundle}


def cmd_serve(payload: dict[str, Any], db_path: Path | None) -> None:
    from web import run_server

    host = str(payload.get("host") or "127.0.0.1")
    port = int(payload.get("port") or 8000)
    run_server(host=host, port=port, db_path=db_path)


HANDLERS = {
    "add": cmd_add,
    "query": cmd_query,
    "delete-preview": cmd_delete_preview,
    "delete-confirm": cmd_delete_confirm,
    "merge-preview": cmd_merge_preview,
    "merge-confirm": cmd_merge_confirm,
    "category-add": cmd_category_add,
    "category-list": cmd_category_list,
    "report": cmd_report,
    "export-csv": cmd_export_csv,
    "parse": cmd_parse,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="BillClaw 记账 CLI")
    ap.add_argument(
        "command",
        choices=[
            *HANDLERS.keys(),
            "serve",
        ],
    )
    ap.add_argument("--json", metavar="FILE", help="从文件读取 JSON 参数")
    ap.add_argument("--json-string", dest="json_string", help="JSON 字符串")
    args = ap.parse_args()
    db_path = _db_path_from_env()

    try:
        payload = _load_payload(args)
    except json.JSONDecodeError as e:
        _out({"ok": False, "error": f"JSON 无效: {e}", "data": {}})
        return 1

    if args.command == "serve":
        cmd_serve(payload, db_path)
        return 0

    handler = HANDLERS[args.command]
    try:
        if args.command == "parse":
            result = handler(payload)
        else:
            result = handler(payload, db_path)
    except Exception as e:
        _out({"ok": False, "error": str(e), "data": {}})
        return 1

    _out(result)
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
