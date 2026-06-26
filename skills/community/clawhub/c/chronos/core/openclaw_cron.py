"""Helpers for constructing OpenClaw cron commands."""
from __future__ import annotations

from typing import List

from .paths import OPENCLAW_BIN


def build_cron_add_command(*, job_name: str, at_iso: str, message: str, chat_id: str) -> List[str]:
    return [
        OPENCLAW_BIN, "cron", "add",
        "--name", job_name,
        "--at", at_iso,
        "--message", message,
        "--session", "isolated",
        "--announce",
        "--to", chat_id,
    ]


def build_cron_remove_command(job_name: str) -> List[str]:
    return [OPENCLAW_BIN, "cron", "remove", job_name]
