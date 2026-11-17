#!/usr/bin/env python3
"""Task status lookup.

Every async submit returns a workspace_id. This module reads it back, either
once, in bulk, or by blocking until the task settles.
"""

from __future__ import annotations

import argparse

from shared.client import run_cli

STATUSES = "pending / processing / completed / failed"


def cmd_status(client, args) -> dict:
    """One task. `status` is pending / processing / completed / failed."""
    return client.work_status(args.workspace_id)


def cmd_batch(client, args) -> dict:
    return client.batch_work_status(args.workspace_ids)


def cmd_wait(client, args) -> dict:
    """Block until the task completes or fails."""
    return client.poll(args.workspace_id, timeout=args.timeout, interval=args.interval)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AdsTurbo task status")
    sub = parser.add_subparsers(dest="command")

    status = sub.add_parser("status", help=f"one task; status is {STATUSES}")
    status.add_argument("--workspace-id", required=True)

    batch = sub.add_parser("batch", help="several tasks in one call")
    batch.add_argument("--workspace-ids", nargs="+", required=True)

    wait = sub.add_parser("wait", help="block until the task settles")
    wait.add_argument("--workspace-id", required=True)
    wait.add_argument("--timeout", type=float, default=900)
    wait.add_argument("--interval", type=float, default=10)

    return parser


HANDLERS = {
    "status": cmd_status,
    "batch": cmd_batch,
    "wait": cmd_wait,
}

if __name__ == "__main__":
    run_cli(build_parser(), HANDLERS)
