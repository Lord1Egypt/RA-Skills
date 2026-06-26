"""
server/transfer_detect.py — Internal transfer detection for Friday Budgeting Pro.

Identifies pairs of transactions that look like internal transfers between
accounts owned by the same user (same amount, different accounts, within 3 days).
"""

from __future__ import annotations

import sqlite3

# ---------------------------------------------------------------------------
# Known investment institution substrings (case-insensitive match)
# ---------------------------------------------------------------------------

_INVESTMENT_INSTITUTIONS = [
    "wealthsimple",
    "questrade",
    "robinhood",
    "vanguard",
    "fidelity",
    "schwab",
]


def is_investment_account(account: dict) -> bool:
    """Return True if the account is at a known investment platform.

    Matches on ``institution_name`` as a case-insensitive substring check.

    Args:
        account: A dict (or sqlite3.Row) with an ``institution_name`` key.

    Returns:
        True if the institution name contains a known investment platform name.
    """
    name: str = (account.get("institution_name") or "").lower()
    return any(inst in name for inst in _INVESTMENT_INSTITUTIONS)


# ---------------------------------------------------------------------------
# Core transfer detection
# ---------------------------------------------------------------------------


def detect_internal_transfers(
    db_conn: sqlite3.Connection,
    user_id: str,
    lookback_days: int = 7,
) -> list[dict]:
    """Find pairs of transactions that look like internal transfers.

    Matching criteria:
    - Same user (transactions belong to bank_accounts whose connections share
      user_id)
    - Different bank accounts
    - One outflow (positive amount) and one inflow (negative amount, i.e. credit)
    - |outflow.amount - |inflow.amount|| < 0.01
    - |outflow.date - inflow.date| <= 3 days

    Args:
        db_conn:      An open sqlite3 connection (row_factory may be set or not).
        user_id:      The user whose accounts to search across.
        lookback_days: How many days back to consider (default 7).

    Returns:
        List of dicts, each containing::

            {
                "outflow_tx_id": str,
                "inflow_tx_id":  str,
                "amount":        float,   # the outflow amount
                "days_apart":    int,
                "account_a":     str,     # bank_account_id of the outflow
                "account_b":     str,     # bank_account_id of the inflow
            }
    """
    # Fetch all recent transactions for accounts belonging to this user.
    # Positive amount = outflow (money leaving the account).
    # Negative amount = inflow (money arriving, e.g. credit/deposit from bank's POV).
    cursor = db_conn.execute(
        """
        SELECT
            t.id          AS tx_id,
            t.bank_account_id,
            t.date,
            t.amount
        FROM transactions t
        JOIN bank_accounts ba ON ba.id = t.bank_account_id
        JOIN bank_connections bc ON bc.id = ba.connection_id
        WHERE bc.user_id = ?
          AND t.date >= date('now', ? || ' days')
          AND t.pending = 0
        ORDER BY t.date ASC
        """,
        (user_id, f"-{lookback_days}"),
    )

    rows = cursor.fetchall()

    # Separate into outflows (positive) and inflows (negative).
    outflows = []
    inflows = []
    for row in rows:
        if isinstance(row, sqlite3.Row):
            tx_id, account_id, date, amount = (
                row["tx_id"],
                row["bank_account_id"],
                row["date"],
                row["amount"],
            )
        else:
            tx_id, account_id, date, amount = row

        if amount > 0:
            outflows.append((tx_id, account_id, date, amount))
        elif amount < 0:
            inflows.append((tx_id, account_id, date, amount))

    # Match pairs.
    matched_pairs: list[dict] = []
    used_outflows: set[str] = set()
    used_inflows: set[str] = set()

    for out_id, out_account, out_date, out_amount in outflows:
        if out_id in used_outflows:
            continue

        for in_id, in_account, in_date, in_amount in inflows:
            if in_id in used_inflows:
                continue

            # Must be different accounts.
            if out_account == in_account:
                continue

            # Amount tolerance: |out_amount - |in_amount|| < 0.01
            if abs(out_amount - abs(in_amount)) >= 0.01:
                continue

            # Date distance: <= 3 days.
            days_apart = _date_diff_days(out_date, in_date)
            if days_apart > 3:
                continue

            matched_pairs.append(
                {
                    "outflow_tx_id": out_id,
                    "inflow_tx_id": in_id,
                    "amount": out_amount,
                    "days_apart": days_apart,
                    "account_a": out_account,
                    "account_b": in_account,
                }
            )
            used_outflows.add(out_id)
            used_inflows.add(in_id)
            break  # One-to-one matching: move to next outflow.

    return matched_pairs


# ---------------------------------------------------------------------------
# Per-transaction helper
# ---------------------------------------------------------------------------


def get_transfer_hint(tx_id: str, db_path: str) -> dict | None:
    """Return a transfer hint dict if this transaction may be part of an internal transfer.

    Opens a fresh connection to *db_path*, fetches the transaction's user_id,
    then calls :func:`detect_internal_transfers` and checks whether *tx_id*
    appears in any detected pair.

    Args:
        tx_id:   The transaction ID to look up.
        db_path: Path to the SQLite database file.

    Returns:
        ``{"is_possible_transfer": True, "matched_account": str,
           "matched_amount": float}``
        if the transaction is part of a detected transfer pair, otherwise ``None``.
    """
    from server.db import get_db

    conn = get_db(db_path)
    try:
        # Resolve the user that owns this transaction.
        row = conn.execute(
            """
            SELECT bc.user_id, t.bank_account_id
            FROM transactions t
            JOIN bank_accounts ba ON ba.id = t.bank_account_id
            JOIN bank_connections bc ON bc.id = ba.connection_id
            WHERE t.id = ?
            """,
            (tx_id,),
        ).fetchone()

        if row is None:
            return None

        user_id = row["user_id"]

        pairs = detect_internal_transfers(conn, user_id, lookback_days=7)

        for pair in pairs:
            if pair["outflow_tx_id"] == tx_id:
                return {
                    "is_possible_transfer": True,
                    "matched_account": pair["account_b"],
                    "matched_amount": pair["amount"],
                }
            if pair["inflow_tx_id"] == tx_id:
                return {
                    "is_possible_transfer": True,
                    "matched_account": pair["account_a"],
                    "matched_amount": pair["amount"],
                }
    finally:
        conn.close()

    return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _date_diff_days(date_a: str, date_b: str) -> int:
    """Return the absolute number of days between two YYYY-MM-DD date strings."""
    from datetime import date as _date

    a = _date.fromisoformat(date_a)
    b = _date.fromisoformat(date_b)
    return abs((a - b).days)
