#!/usr/bin/env python3
"""Odoo production scheduling (MRP) operations.

Implements the `/agent_api/v1/production/*` surface: pull a planning snapshot,
inspect batches and workcenters, and write schedule decisions back.

Usage:
    python3 scripts/production.py <action>   # JSON args on stdin

Actions:
    overview            One-shot planning snapshot (batches, workcenters,
                        production_centers, decoration_methods, open_batch_total).
                        Input (all optional): {"batch_detail": false,
                        "batch_limit": 200, "unscheduled_only": false}
    list-batches        List open batches (summary). Input (all optional):
                        {"unscheduled_only": false, "limit": 50, "offset": 0}
    get-batch           Full batch detail. Input: {"batch_id": 142}
    schedule            Apply scheduling fields to one batch (partial updates
                        allowed; >=1 field required). Honors ODOO_DRY_RUN.
                        Input: {"batch_id": 142, "primary_workcenter_id": 3,
                        "production_center_id": 2,
                        "date_planned_start": "2026-06-10T14:00:00",
                        "date_planned_finished": "...",
                        "activity_message": "..."}
    plan                Run Odoo's native button_plan(). Input: {"batch_id": 142}
    bulk-schedule       Apply many edits. Honors ODOO_DRY_RUN.
                        Input: {"atomic": true, "updates": [{"batch_id": 1,
                        "primary_workcenter_id": 3}, ...]}
    list-workcenters    List machines with scheduled load.
                        Input (optional): {"active_only": true}
    get-workcenter      Single workcenter. Input: {"workcenter_id": 3}
    production-centers   List production centers.
    decoration-methods   List active decoration methods.
"""

from __future__ import annotations

from typing import Any

from _cli import run
from odoo_client import OdooClient


def _require_int(args: dict[str, Any], key: str) -> int:
    if key not in args:
        raise ValueError(f"`{key}` is required.")
    return int(args[key])


def _overview(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.get_overview(
        batch_detail=bool(args.get("batch_detail", False)),
        batch_limit=int(args.get("batch_limit", 200)),
        unscheduled_only=bool(args.get("unscheduled_only", False)),
    )


def _list_batches(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.get_batches(
        unscheduled_only=bool(args.get("unscheduled_only", False)),
        limit=int(args.get("limit", 50)),
        offset=int(args.get("offset", 0)),
    )


def _get_batch(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.get_batch(_require_int(args, "batch_id"))


def _schedule(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.schedule_batch(
        _require_int(args, "batch_id"),
        primary_workcenter_id=args.get("primary_workcenter_id"),
        production_center_id=args.get("production_center_id"),
        date_planned_start=args.get("date_planned_start"),
        date_planned_finished=args.get("date_planned_finished"),
        activity_message=args.get("activity_message", ""),
    )


def _plan(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.plan_batch(_require_int(args, "batch_id"))


def _bulk_schedule(client: OdooClient, args: dict[str, Any]) -> Any:
    updates = args.get("updates")
    if not isinstance(updates, list) or not updates:
        raise ValueError("`updates` must be a non-empty array.")
    return client.bulk_schedule(updates, atomic=bool(args.get("atomic", True)))


def _list_workcenters(client: OdooClient, args: dict[str, Any]) -> Any:
    return {
        "workcenters": client.get_workcenters(
            active_only=bool(args.get("active_only", True))
        )
    }


def _get_workcenter(client: OdooClient, args: dict[str, Any]) -> Any:
    return client.get_workcenter(_require_int(args, "workcenter_id"))


def _production_centers(client: OdooClient, _args: dict[str, Any]) -> Any:
    return {"production_centers": client.get_production_centers()}


def _decoration_methods(client: OdooClient, _args: dict[str, Any]) -> Any:
    return {"decoration_methods": client.get_decoration_methods()}


ACTIONS = {
    "overview": _overview,
    "list-batches": _list_batches,
    "get-batch": _get_batch,
    "schedule": _schedule,
    "plan": _plan,
    "bulk-schedule": _bulk_schedule,
    "list-workcenters": _list_workcenters,
    "get-workcenter": _get_workcenter,
    "production-centers": _production_centers,
    "decoration-methods": _decoration_methods,
}


if __name__ == "__main__":
    run(
        ACTIONS,
        usage=(
            "production.py <overview|list-batches|get-batch|schedule|plan|"
            "bulk-schedule|list-workcenters|get-workcenter|production-centers|"
            "decoration-methods>"
        ),
    )
