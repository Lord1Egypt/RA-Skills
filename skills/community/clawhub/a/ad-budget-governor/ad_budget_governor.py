"""
ad_budget_governor.py — Cross-platform rolling ad-spend cap for AI agents.

Per-platform tools (Meta, TikTok, Google, etc.) typically only enforce their
OWN daily cap. If an agent operates ad spend across multiple platforms, the
platforms have no idea about each other — total spend can exceed what the
operator actually intended even when every individual platform "cap" is
respected. This module adds a single rolling-window cap that sums spend
across ALL configured platform ledgers and blocks any action that would
push the combined total over the limit, regardless of which platform is
asking.

Design principle: fail CLOSED. If a ledger file exists but cannot be read
(corrupted, permissions, unexpected format), this treats that platform's
spend as UNKNOWN — not zero — and blocks new spend until it's resolved.
A spend governor that silently treats unreadable data as "$0 spent" is a
liability risk, not just a bug: it would let real overspend through exactly
when something is already wrong.

SETUP
-----
1. Edit LEDGER_PATHS below to point at your own spend-tracking files. Each
   ledger is a JSON file containing a list of records shaped like:
     {"timestamp": "2026-06-22T14:00:00Z", "amount_usd": 12.50, ...}
   (Any extra fields are ignored — this only reads "timestamp" and
   "amount_usd".) If your agent doesn't already write spend records in this
   shape, add a call to whatever logs a spend event in your platform
   wrapper(s) before calling check_rolling_budget().
2. Call check_rolling_budget(amount_usd) BEFORE every spend action, on every
   platform. If it returns (False, reason), do not spend — surface the
   reason to the operator instead.
3. Default cap is $0 until you call set_cap() — this is intentional, so the
   governor never silently allows spend before someone has actually decided
   on a number.

PUBLIC API
----------
check_rolling_budget(amount_usd) -> (ok: bool, reason: str | None)
rolling_spend_usd(window_days=30) -> (total: float, had_read_error: bool)
get_status() -> dict
set_cap(new_cap_usd, note="") -> dict
"""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Optional

_log = logging.getLogger("ad_budget_governor")
_HERE = Path(__file__).resolve().parent

# ── EDIT THIS: point at your own platform spend ledgers ──────────────────
LEDGER_PATHS = [
    _HERE / "platform_a_spend.json",
    _HERE / "platform_b_spend.json",
]

_STATE_FILE = _HERE / "ad_budget_state.json"
_ROLLING_WINDOW_DAYS = 30
_DEFAULT_CAP_USD = 0.0  # intentionally zero until set_cap() is called


def _load_state() -> dict[str, Any]:
    if _STATE_FILE.exists():
        try:
            return json.loads(_STATE_FILE.read_text())
        except Exception as exc:
            _log.warning(f"could not load budget state: {exc}")
    return {
        "cap_usd": _DEFAULT_CAP_USD,
        "set_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "history": [],
    }


def _save_state(state: dict[str, Any]) -> None:
    try:
        _STATE_FILE.write_text(json.dumps(state, indent=2))
    except Exception as exc:
        _log.warning(f"could not save budget state: {exc}")


def rolling_spend_usd(window_days: int = _ROLLING_WINDOW_DAYS) -> tuple[float, bool]:
    """Sum spend across ALL configured ledgers in the trailing N days.

    Returns (total, had_read_error). A missing ledger file is treated as
    $0 spent there (legitimate — nothing has been spent on that platform
    yet). A ledger that EXISTS but fails to parse is treated as UNKNOWN
    spend, not zero — see module docstring for why this distinction matters."""
    cutoff = time.time() - window_days * 86400
    total = 0.0
    had_read_error = False
    for ledger_path in LEDGER_PATHS:
        if not ledger_path.exists():
            continue
        try:
            records = json.loads(ledger_path.read_text())
        except Exception as exc:
            _log.error(f"ledger unreadable, failing closed: {ledger_path} — {exc}")
            had_read_error = True
            continue
        for r in records:
            ts = r.get("timestamp", "")
            try:
                rec_time = time.mktime(time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"))
            except Exception:
                continue
            if rec_time >= cutoff:
                total += float(r.get("amount_usd", 0) or 0)
    return round(total, 2), had_read_error


def get_status() -> dict[str, Any]:
    state = _load_state()
    cap = float(state.get("cap_usd", _DEFAULT_CAP_USD))
    spent, had_read_error = rolling_spend_usd()
    return {
        "ok": True,
        "window_days": _ROLLING_WINDOW_DAYS,
        "cap_usd": cap,
        "spent_usd": spent,
        "remaining_usd": round(cap - spent, 2),
        "at_cap": spent >= cap,
        "set_at": state.get("set_at"),
        "ledger_read_error": had_read_error,
    }


def check_rolling_budget(amount_usd: float) -> tuple[bool, Optional[str]]:
    """Gate for any spend action on any platform. Call BEFORE spending."""
    status = get_status()
    if status["ledger_read_error"]:
        return False, (
            "Spend ledger unreadable — true spend cannot be verified. "
            "Failing closed: blocking this spend until the ledger is repaired."
        )
    if status["cap_usd"] <= 0:
        return False, "No budget cap has been set yet. Call set_cap() first."
    if status["at_cap"]:
        return False, (
            f"Rolling {_ROLLING_WINDOW_DAYS}-day cap reached "
            f"(${status['spent_usd']:.2f} / ${status['cap_usd']:.2f})."
        )
    if amount_usd > status["remaining_usd"]:
        return False, (
            f"This spend (${amount_usd:.2f}) would exceed the rolling cap. "
            f"Remaining: ${status['remaining_usd']:.2f} of ${status['cap_usd']:.2f}."
        )
    return True, None


def set_cap(new_cap_usd: float, note: str = "") -> dict[str, Any]:
    """Raise or lower the rolling-window cap."""
    state = _load_state()
    state["cap_usd"] = float(new_cap_usd)
    state["set_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    state.setdefault("history", []).append({
        "cap_usd": float(new_cap_usd),
        "set_at": state["set_at"],
        "note": note,
    })
    _save_state(state)
    _log.info(f"Budget cap set to ${new_cap_usd:.2f} — {note}")
    return get_status()


def get_actions() -> dict:
    return {
        "ad_budget_status": get_status,
        "ad_budget_set_cap": set_cap,
        "ad_budget_check": check_rolling_budget,
    }
