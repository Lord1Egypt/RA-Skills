"""
server/main.py — FastMCP server skeleton for Friday Budgeting Pro.

All tools are registered as stubs returning {'status': 'not_implemented'}.
Real implementations land in later tickets.
"""

from __future__ import annotations

import json as _json
import logging
import os
import secrets
import subprocess as _subprocess
import tempfile
import time as _time
import uuid
from datetime import datetime as _datetime
from pathlib import Path
from typing import List, Optional

import fastmcp

import server.crypto
import server.excel_export as excel_export
import server.health_monitor
import server.paths
from server.classifier import (
    apply_rules,
    classify_transaction,  # kept import for legacy callers / tests
)
from server.db import get_db
from server.db import transaction as db_txn
from server.providers.plaid import PlaidProvider
from server.sync_lock import LockBusy, sync_lock
from server.transfer_detect import get_transfer_hint
from ui.auth import (
    add_recovery_token,
    get_active_user_id,
    get_user_by_id,
    update_user_password,
    verify_password,
)

_plaid = PlaidProvider()

mcp = fastmcp.FastMCP("friday-budgeting-pro")


from server.plaid_credentials import get_plaid_credentials as _get_plaid_credentials

_logger = logging.getLogger(__name__)

# Project root — tests monkeypatch this to a tmp dir so .env writes stay isolated.
project_root: Path = Path(__file__).resolve().parent.parent

# OpenClaw home directory override — monkeypatched in tests to avoid writing
# to the real ~/.openclaw/ during unit tests.  None means use the default
# (Path.home() / ".openclaw").
_OPENCLAW_HOME: Path | None = None

# ---------------------------------------------------------------------------
# OpenClaw cron registration
# ---------------------------------------------------------------------------


def _get_local_tz() -> str:
    """Return the best-effort IANA timezone name for the local system.

    Tries to resolve the /etc/localtime symlink which on macOS and most Linux
    distros points into the zoneinfo directory tree.  Falls back to the
    abbreviated timezone name (e.g. ``'EDT'``) when the symlink is absent.
    """
    try:
        result = _subprocess.run(
            ["readlink", "/etc/localtime"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0:
            tz_str = result.stdout.strip()
            if "/zoneinfo/" in tz_str:
                return tz_str.split("/zoneinfo/")[-1]
    except Exception:  # noqa: BLE001
        pass
    # Fallback: abbreviated timezone name (e.g. 'EDT', 'UTC')
    return _datetime.now().astimezone().tzname() or "UTC"


def _register_openclaw_cron() -> bool:
    """Write the Friday Budgeting Pro sync cron spec to ~/.openclaw/cron/.

    Cron file: ``~/.openclaw/cron/friday-budgeting-pro-sync.json``

    The schedule runs a daily agent turn at 06:00 local time that calls the
    ``sync`` MCP tool and then notifies the user of any transactions needing
    review via ``get_needs_review``.

    Detection
    ---------
    If ``~/.openclaw/`` does not exist the user is running without OpenClaw.
    We log a warning and return ``False`` — the app continues to work, it
    just won't have scheduled syncs.

    Idempotent
    ----------
    Overwriting the same file on a repeated call is safe and intentional.

    Returns
    -------
    bool
        ``True`` if the cron file was written; ``False`` if OpenClaw is not
        installed (``~/.openclaw/`` absent).
    """
    oc_dir = _OPENCLAW_HOME if _OPENCLAW_HOME is not None else Path.home() / ".openclaw"

    if not oc_dir.exists():
        _logger.warning(
            "OpenClaw directory %s not found — skipping cron registration. "
            "The app will work without scheduled syncs; run apply_initial_setup "
            "again after installing OpenClaw to register the cron job.",
            oc_dir,
        )
        return False

    cron_dir = oc_dir / "cron"
    cron_dir.mkdir(parents=True, exist_ok=True)

    tz = _get_local_tz()
    spec = {
        "name": "friday-budgeting-pro-sync",
        "schedule": {"kind": "cron", "expr": "0 6 * * *", "tz": tz},
        "sessionTarget": "isolated",
        "payload": {
            "kind": "agentTurn",
            "message": (
                "Run friday-budgeting-pro daily tasks in order: "
                "1) Call get_connections_needing_attention — if any connections "
                "are returned, alert the user immediately with their suggested_message "
                "(e.g. '\u26a0\ufe0f 1 connection needs attention: BMO Bank of Montreal'). "
                "2) Call the sync MCP tool to pull new transactions. "
                "3) Call get_needs_review and notify the user about any "
                "transactions needing classification."
            ),
            "timeoutSeconds": 900,
        },
        "delivery": {"mode": "none"},
    }

    cron_file = cron_dir / "friday-budgeting-pro-sync.json"
    # Atomic-ish write: write to a sibling temp file then replace.
    tmp_file = cron_file.with_suffix(".json.tmp")
    try:
        tmp_file.write_text(_json.dumps(spec, indent=2))
        tmp_file.replace(cron_file)
    except Exception:  # noqa: BLE001
        try:
            tmp_file.unlink(missing_ok=True)
        except OSError:
            pass
        raise

    _logger.info("OpenClaw cron registered: %s", cron_file)
    return True


# ---------------------------------------------------------------------------
# Setup tools
# ---------------------------------------------------------------------------


@mcp.tool
def list_profiles() -> dict:
    """Return a list of local profiles (usernames).

    Does not require authentication.  Returns usernames only (no hashes).
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute(
            "SELECT id, username, created_at FROM users ORDER BY created_at"
        ).fetchall()
        return {
            "profiles": [
                {"id": r["id"], "username": r["username"], "created_at": r["created_at"]}
                for r in rows
            ]
        }
    finally:
        conn.close()


@mcp.tool
def setup_status() -> dict:
    """Return whether initial setup is not_started, in_progress, or complete.

    Status rules:
      - "not_started"  → 0 ledgers AND 0 bank_connections (for current user)
      - "in_progress"  → ≥1 ledger AND 0 bank_connections
                         (user picked a ledger but hasn't linked a bank yet)
      - "complete"     → ≥1 ledger AND ≥1 bank_connection
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            ledger_count = conn.execute(
                "SELECT COUNT(*) FROM ledgers WHERE user_id = ?", (uid,)
            ).fetchone()[0]
            bank_count = conn.execute(
                "SELECT COUNT(*) FROM bank_connections WHERE user_id = ?", (uid,)
            ).fetchone()[0]
        else:
            ledger_count = conn.execute("SELECT COUNT(*) FROM ledgers").fetchone()[0]
            bank_count = conn.execute("SELECT COUNT(*) FROM bank_connections").fetchone()[0]
    finally:
        conn.close()

    if ledger_count == 0 and bank_count == 0:
        status = "not_started"
    elif ledger_count >= 1 and bank_count == 0:
        status = "in_progress"
    else:
        status = "complete"

    return {"status": status}


@mcp.tool
def apply_initial_setup(
    banks_to_link: List = None,
    extra_ledgers: List = None,
    hints: List = None,
    rental_properties: List = None,
    investment_account_ids: List = None,
) -> dict:
    """Perform the whole first-run setup in one call.

    Parameters
    ----------
    banks_to_link : List[str], optional
        Human-readable bank names the user wants to connect.  NOTE: This tool
        does NOT run Plaid Link — that interactive flow lives in start_link /
        complete_link.  We simply acknowledge the requested banks and return
        them so the caller can chain start_link calls for each one.
    extra_ledgers : List[dict], optional
        Additional ledgers beyond "Personal".  Each entry is a dict like::

            {"name": "Business", "line_items": [{"name": "Office", "type": "expense"}, ...]}

        The built-in "Personal" ledger is always created (with the standard
        10 line items below) regardless of this parameter.
    hints : List[str], optional
        Natural-language classification hints; each becomes a row in
        ``classification_hints``.  De-duped on exact text.
    rental_properties : List[dict], optional
        Rental properties to create ledgers for.  Each entry is a dict like::

            {"name": "123 Main St", "description": "2-bed condo", "account_id": "<uuid>"}

        For each property a ledger is created via ``create_property_ledger``
        and the given bank account is linked via ``set_account_ledger``.
        ``account_id`` may be omitted or ``None`` to skip the account link.
    investment_account_ids : List[str], optional
        Bank account IDs to route to a shared "Investments" ledger.  If the
        list is non-empty a single "Investments" ledger is created (once) and
        every account in the list is linked to it via ``set_account_ledger``.

    Standard Personal line items (always created):
      Salary (income), Groceries (expense), Dining (expense),
      Transport (expense), Subscriptions (expense), Healthcare (expense),
      Travel (expense), Shopping (expense), Misc (expense), Other (expense)

    Idempotent: re-running will not duplicate ledgers, line items, or hints.

    Returns
    -------
    dict
        {"status": "ok", "ledgers_created": [...], "line_items_created": N,
         "hints_created": N, "banks_to_link": [...],
         "properties_created": N, "investment_ledger_id": str | None}
    """
    PERSONAL_LINE_ITEMS = [
        ("Salary", "income"),
        ("Groceries", "expense"),
        ("Dining", "expense"),
        ("Transport", "expense"),
        ("Subscriptions", "expense"),
        ("Healthcare", "expense"),
        ("Travel", "expense"),
        ("Shopping", "expense"),
        ("Misc", "expense"),
        ("Other", "expense"),
    ]

    # Build the full ledger spec: Personal first, then any extras.
    ledger_specs = [{"name": "Personal", "line_items": PERSONAL_LINE_ITEMS}]
    for el in extra_ledgers or []:
        items = [(li["name"], li["type"]) for li in el.get("line_items", [])]
        ledger_specs.append({"name": el["name"], "line_items": items})

    ledgers_created: list[str] = []
    line_items_created = 0
    hints_created = 0

    uid = get_active_user_id(server.paths.DB_PATH)

    conn = get_db(server.paths.DB_PATH)
    try:
        with db_txn(conn):
            for spec in ledger_specs:
                ledger_name = spec["name"]

                # Upsert ledger — skip if already present for this user.
                if uid:
                    existing_ledger = conn.execute(
                        "SELECT id FROM ledgers WHERE name = ? AND user_id = ?",
                        (ledger_name, uid),
                    ).fetchone()
                else:
                    existing_ledger = conn.execute(
                        "SELECT id FROM ledgers WHERE name = ?", (ledger_name,)
                    ).fetchone()
                if existing_ledger:
                    ledger_id = existing_ledger["id"]
                else:
                    ledger_id = str(uuid.uuid4())
                    conn.execute(
                        "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
                        (ledger_id, ledger_name, uid),
                    )
                    ledgers_created.append(ledger_name)

                # Upsert line items — skip if name+type already present in this ledger.
                for item_name, item_type in spec["line_items"]:
                    existing_item = conn.execute(
                        "SELECT id FROM line_items "
                        "WHERE ledger_id = ? AND name = ? AND item_type = ?",
                        (ledger_id, item_name, item_type),
                    ).fetchone()
                    if existing_item:
                        continue
                    conn.execute(
                        "INSERT INTO line_items (id, ledger_id, name, item_type) "
                        "VALUES (?, ?, ?, ?)",
                        (str(uuid.uuid4()), ledger_id, item_name, item_type),
                    )
                    line_items_created += 1

            # Upsert hints — de-dupe on exact text.
            for hint_text in hints or []:
                if uid:
                    existing_hint = conn.execute(
                        "SELECT id FROM classification_hints WHERE text = ? AND user_id = ?",
                        (hint_text, uid),
                    ).fetchone()
                else:
                    existing_hint = conn.execute(
                        "SELECT id FROM classification_hints WHERE text = ?",
                        (hint_text,),
                    ).fetchone()
                if existing_hint:
                    continue
                conn.execute(
                    "INSERT INTO classification_hints (id, text, user_id) VALUES (?, ?, ?)",
                    (str(uuid.uuid4()), hint_text, uid),
                )
                hints_created += 1
    finally:
        conn.close()

    cron_registered = _register_openclaw_cron()

    # ── Rental properties ─────────────────────────────────────────────────
    properties_created = 0
    for prop in rental_properties or []:
        prop_name = prop.get("name", "").strip()
        if not prop_name:
            continue
        result = create_property_ledger(
            name=prop_name,
            description=prop.get("description"),
        )
        if result.get("status") == "ok":
            ledgers_created.append(prop_name)
            properties_created += 1
            acct_id = prop.get("account_id")
            if acct_id:
                set_account_ledger(account_id=acct_id, ledger_id=result["ledger_id"])

    # ── Investment accounts ───────────────────────────────────────────────
    investment_ledger_id = None
    inv_ids = [aid for aid in (investment_account_ids or []) if aid]
    if inv_ids:
        inv_result = create_investment_ledger(name="Investments")
        if inv_result.get("status") == "ok":
            investment_ledger_id = inv_result["ledger_id"]
            ledgers_created.append("Investments")
            for acct_id in inv_ids:
                set_account_ledger(account_id=acct_id, ledger_id=investment_ledger_id)

    return {
        "status": "ok",
        "ledgers_created": ledgers_created,
        "line_items_created": line_items_created,
        "hints_created": hints_created,
        "banks_to_link": [*banks_to_link] if banks_to_link else [],
        "cron_registered": cron_registered,
        "properties_created": properties_created,
        "investment_ledger_id": investment_ledger_id,
    }


# ---------------------------------------------------------------------------
# Banks tools
# ---------------------------------------------------------------------------


@mcp.tool
def start_link(plaid_env: str | None = None) -> dict:
    """Return a URL to open Plaid Link.

    Calls PlaidProvider.create_link_token() and returns a URL pointing at
    the (future) UI link page (served by #14).

    Parameters
    ----------
    plaid_env : str or None
        Plaid environment for this link session: ``'sandbox'``,
        ``'development'``, or ``'production'``.  When *None* (the default)
        the value is read from the ``PLAID_ENV`` environment variable
        (falling back to ``'sandbox'`` if unset).
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    db_client_id, db_secret, db_env = _get_plaid_credentials(uid)
    resolved_env = plaid_env or db_env
    provider = PlaidProvider(env=resolved_env, client_id=db_client_id, secret=db_secret)
    link_token = provider.create_link_token()
    return {"url": f"http://127.0.0.1:6789/link?token={link_token}", "plaid_env": provider.env}


@mcp.tool
def complete_link(public_token: str, plaid_env: str | None = None) -> dict:
    """Exchange a Plaid public token and store the access token.

    Exchanges the public_token for a Plaid access_token + item_id, encrypts
    the access token via server.crypto, and inserts a new row into
    bank_connections.  Returns the new connection_id.

    institution_name is left NULL for now — fetching it requires
    Plaid /institutions/get_by_id which is out of scope; see issue #34.

    Parameters
    ----------
    plaid_env : str or None
        Plaid environment that was used for the Link session: ``'sandbox'``,
        ``'development'``, or ``'production'``.  When *None* (the default),
        the value is read from the ``PLAID_ENV`` environment variable
        (falling back to ``'sandbox'`` if unset).  Stored on the connection
        row so every subsequent sync uses the correct environment.
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    db_client_id, db_secret, db_env = _get_plaid_credentials(uid)
    resolved_env = plaid_env or db_env
    provider = PlaidProvider(env=resolved_env, client_id=db_client_id, secret=db_secret)
    result = provider.exchange_public_token(public_token)
    access_token = result["access_token"]
    item_id = result["item_id"]

    # Fetch institution name via /item/get + /institutions/get_by_id
    institution_name: str | None = None
    try:
        institution_name = provider.get_institution_name(access_token)
    except Exception as _inst_exc:  # noqa: BLE001
        import logging as _logging

        _logging.getLogger(__name__).warning(
            "complete_link: could not fetch institution name: %s", _inst_exc
        )

    encrypted_token = server.crypto.encrypt(access_token)
    connection_id = str(uuid.uuid4())

    conn = get_db(server.paths.DB_PATH)
    try:
        conn.execute(
            """
            INSERT INTO bank_connections
                (id, plaid_item_id, plaid_access_token_encrypted, institution_name,
                 status, user_id, plaid_env)
            VALUES (?, ?, ?, ?, 'active', ?, ?)
            """,
            (connection_id, item_id, encrypted_token, institution_name, uid, provider.env),
        )
        conn.commit()
    finally:
        conn.close()

    return {"connection_id": connection_id, "institution_name": institution_name}


@mcp.tool
def list_connections() -> dict:
    """List all saved bank connections for the current user.

    Returns id, institution_name, status, and last_synced_at for each
    connection.  The encrypted access token is NEVER included in the output.
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            rows = conn.execute(
                "SELECT id, institution_name, status, last_synced_at "
                "FROM bank_connections WHERE user_id = ? ORDER BY rowid",
                (uid,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, institution_name, status, last_synced_at "
                "FROM bank_connections ORDER BY rowid"
            ).fetchall()
        connections = [dict(r) for r in rows]
    finally:
        conn.close()

    return {"connections": connections}


@mcp.tool
def get_connections_needing_attention() -> dict:
    """Return bank connections that need user action (re-auth or pending expiration).

    A connection needs attention when:
      - ``status = 'needs_reauth'``  — credentials have expired / login required.
      - ``status = 'pending_expiration'`` — token will expire soon.
      - ``last_synced_at IS NULL`` — connection was added but never synced.

    For each connection returned, ``last_alerted_at`` is updated to the current
    Unix timestamp so repeated cron calls do not spam the user more often than
    once every 24 hours.

    Returns
    -------
    dict
        {"connections": [{"connection_id", "institution_name", "status",
                          "days_until_expiry", "suggested_message",
                          "last_alerted_at"}, ...]}
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    if uid is None:
        return {"connections": []}

    now = int(_time.time())
    alert_cooldown = 24 * 60 * 60  # 24 hours in seconds

    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute(
            """
            SELECT id, institution_name, status, last_synced_at,
                   last_alerted_at
            FROM bank_connections
            WHERE user_id = ?
              AND (
                    status IN ('needs_reauth', 'pending_expiration')
                    OR last_synced_at IS NULL
              )
            ORDER BY rowid
            """,
            (uid,),
        ).fetchall()

        result_connections = []
        for row in rows:
            connection_id = row["id"]
            institution_name = row["institution_name"] or "Your bank"
            status = row["status"]
            last_alerted_at = row["last_alerted_at"]

            # Throttle: skip if alerted within the last 24 hours.
            if last_alerted_at is not None and (now - last_alerted_at) < alert_cooldown:
                continue

            # Determine days_until_expiry for pending_expiration connections.
            # We don't have an explicit expiry date stored in the current schema;
            # report as None until a dedicated expiry field is added.
            days_until_expiry: Optional[int] = None

            # Build suggested message.
            if status == "pending_expiration":
                if days_until_expiry is not None:
                    suggested_message = (
                        f"Your {institution_name} connection expires in "
                        f"{days_until_expiry} days. "
                        f"Say 'reconnect {institution_name}' to refresh it."
                    )
                else:
                    suggested_message = (
                        f"Your {institution_name} connection expires soon. "
                        f"Say 'reconnect {institution_name}' to refresh it."
                    )
            else:
                # needs_reauth or never-synced
                suggested_message = (
                    f"Your {institution_name} connection needs re-authorization. "
                    f"Say 'reconnect {institution_name}' to open the re-auth flow."
                )

            # Update last_alerted_at to now.
            conn.execute(
                "UPDATE bank_connections SET last_alerted_at = ? WHERE id = ?",
                (now, connection_id),
            )

            result_connections.append(
                {
                    "connection_id": connection_id,
                    "institution_name": row["institution_name"],
                    "status": status,
                    "days_until_expiry": days_until_expiry,
                    "suggested_message": suggested_message,
                    "last_alerted_at": now,
                }
            )

        conn.commit()
    finally:
        conn.close()

    return {"connections": result_connections}


@mcp.tool
def refresh_connection(id: str) -> dict:
    """Trigger an Update Mode Plaid Link for an existing connection.

    Generates a new Plaid Link token for Update Mode.  The plaid-python SDK
    supports passing an access_token to create_link_token() for proper Update
    Mode, but our wrapper does not yet expose that parameter — see TODO below.

    TODO: Pass the decrypted access_token to create_link_token() for a true
    Update Mode link token (requires plaid_client.create_link_token to accept
    an optional access_token kwarg).  Tracked in issue #34.
    """
    # For now, generate a fresh link token (same as start_link)
    link_token = _plaid.create_link_token()
    return {"url": f"http://127.0.0.1:6789/link?token={link_token}"}


@mcp.tool
def disconnect(id: str) -> dict:
    """Disconnect and remove a Plaid bank connection.

    Removes the connection row and any associated sync_cursor row from the
    local database.  Calling Plaid's /item/remove endpoint to revoke the
    access token on Plaid's side is out of scope for this PR (the local
    database record is the authoritative store for this app).
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        conn.execute(
            "DELETE FROM sync_cursors WHERE connection_id = ?",
            (id,),
        )
        conn.execute(
            "DELETE FROM bank_connections WHERE id = ?",
            (id,),
        )
        conn.commit()
    finally:
        conn.close()

    return {"ok": True}


# ---------------------------------------------------------------------------
# Account tools
# ---------------------------------------------------------------------------


@mcp.tool
def set_account_description(account_id: str, description: str) -> dict:
    """Set a user-supplied description for a bank account.

    The description is stored in bank_accounts.description and is used as
    additional context when the LLM classifier decides how to route
    transactions from that account.

    Args:
        account_id: The internal bank_account id (not the Plaid account id).
        description: Free-text description, e.g. "Day-to-day spending" or
            "Business expenses - do not mix with personal".

    Returns:
        {"status": "ok", "account_id": account_id}
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        result = conn.execute(
            "UPDATE bank_accounts SET description = ? WHERE id = ?",
            (description, account_id),
        )
        conn.commit()
        if result.rowcount == 0:
            return {"status": "error", "message": f"account_id {account_id!r} not found"}
    finally:
        conn.close()

    return {"status": "ok", "account_id": account_id}


# ---------------------------------------------------------------------------
# Ledger tools
# ---------------------------------------------------------------------------


@mcp.tool
def list_ledgers() -> dict:
    """List all ledgers and their line items for the active user."""
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            ledger_rows = conn.execute(
                "SELECT id, name, type, description FROM ledgers "
                "WHERE user_id = ? OR user_id IS NULL ORDER BY name",
                (uid,),
            ).fetchall()
        else:
            return {"ledgers": []}
        ledgers = []
        for lr in ledger_rows:
            items = conn.execute(
                "SELECT id, name, item_type FROM line_items WHERE ledger_id = ? ORDER BY name",
                (lr["id"],),
            ).fetchall()
            ledgers.append(
                {
                    "id": lr["id"],
                    "name": lr["name"],
                    "type": lr["type"],
                    "description": lr["description"],
                    "items": [
                        {"id": i["id"], "name": i["name"], "type": i["item_type"]} for i in items
                    ],
                }
            )
        return {"ledgers": ledgers}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Shared helper: fetch a ledger + line items + classified transactions
# ---------------------------------------------------------------------------


def _build_ledger_drilldown(
    conn,
    ledger_row: dict,
    period: str | None = "this_month",
) -> dict:
    """Return a ledger dict with line_items + transactions per item and totals.

    Parameters
    ----------
    conn :
        Open DB connection (caller is responsible for closing).
    ledger_row :
        Row from the ``ledgers`` table with at least ``id``, ``name``,
        ``type``, and ``description``.
    period : str | None
        Date filter applied to ``transactions.date``:
        - ``"this_month"``  — current calendar month (default)
        - ``"last_month"``  — previous calendar month
        - ``"this_year"``   — current calendar year
        - ``None``          — all time
    """
    from datetime import datetime as _dt

    # Build date-range filter -------------------------------------------
    date_filter_sql = ""
    date_params: list = []

    if period is not None:
        now = _dt.now()
        if period == "this_month":
            start = _dt(now.year, now.month, 1).strftime("%Y-%m-%d")
            if now.month == 12:
                end = _dt(now.year + 1, 1, 1).strftime("%Y-%m-%d")
            else:
                end = _dt(now.year, now.month + 1, 1).strftime("%Y-%m-%d")
            date_filter_sql = " AND t.date >= ? AND t.date < ?"
            date_params = [start, end]
        elif period == "last_month":
            if now.month == 1:
                s_year, s_month = now.year - 1, 12
            else:
                s_year, s_month = now.year, now.month - 1
            start = _dt(s_year, s_month, 1).strftime("%Y-%m-%d")
            if s_month == 12:
                end = _dt(s_year + 1, 1, 1).strftime("%Y-%m-%d")
            else:
                end = _dt(s_year, s_month + 1, 1).strftime("%Y-%m-%d")
            date_filter_sql = " AND t.date >= ? AND t.date < ?"
            date_params = [start, end]
        elif period == "this_year":
            start = _dt(now.year, 1, 1).strftime("%Y-%m-%d")
            end = _dt(now.year + 1, 1, 1).strftime("%Y-%m-%d")
            date_filter_sql = " AND t.date >= ? AND t.date < ?"
            date_params = [start, end]
        elif period == "last_3_months":
            from datetime import timedelta as _td

            end_dt = _dt(now.year, now.month, 1)  # start of this month
            start_dt = end_dt - _td(days=90)
            start = start_dt.strftime("%Y-%m-%d")
            end = end_dt.strftime("%Y-%m-%d")
            date_filter_sql = " AND t.date >= ? AND t.date < ?"
            date_params = [start, end]
        elif period == "all":
            pass  # no filter — date_filter_sql stays empty
        # unknown period values → no filter (treat as None)

    # Fetch line items --------------------------------------------------
    item_rows = conn.execute(
        "SELECT id, name, item_type FROM line_items WHERE ledger_id = ? ORDER BY name",
        (ledger_row["id"],),
    ).fetchall()

    total_income = 0.0
    total_expenses = 0.0
    line_items_out = []

    for item in item_rows:
        txn_sql = (
            "SELECT t.id, t.date, t.merchant, te.amount_home, te.amount, "
            "       b.name AS account_name, t.pending "
            "FROM transaction_entries te "
            "JOIN transactions t ON te.transaction_id = t.id "
            "LEFT JOIN bank_accounts b ON t.bank_account_id = b.id "
            "WHERE te.line_item_id = ?" + date_filter_sql + " ORDER BY t.date DESC"
        )
        txn_rows = conn.execute(txn_sql, [item["id"]] + date_params).fetchall()

        transactions_out = []
        item_total = 0.0
        for tx in txn_rows:
            amt = tx["amount_home"] if tx["amount_home"] is not None else tx["amount"]
            item_total += amt
            transactions_out.append(
                {
                    "id": tx["id"],
                    "date": tx["date"],
                    "merchant": tx["merchant"] or "",
                    "amount": round(amt, 2),
                    "account_name": tx["account_name"] or "",
                    "pending": bool(tx["pending"]),
                }
            )

        item_total = round(item_total, 2)
        if item["item_type"] == "income":
            total_income += item_total
        else:
            total_expenses += item_total

        line_items_out.append(
            {
                "id": item["id"],
                "name": item["name"],
                "item_type": item["item_type"],
                "total": item_total,
                "transactions": transactions_out,
            }
        )

    return {
        "ledger": {
            "id": ledger_row["id"],
            "name": ledger_row["name"],
            "type": ledger_row["type"],
        },
        "line_items": line_items_out,
        "totals": {
            "income": round(total_income, 2),
            "expenses": round(total_expenses, 2),
            "net": round(total_income - total_expenses, 2),
        },
    }


@mcp.tool
def get_ledger(ledger_id: str, period: str = "this_month") -> dict:
    """Get a ledger with all line items and the transactions classified to each.

    Parameters
    ----------
    ledger_id : str
        ID of the ledger to retrieve.
    period : str | None
        Optional date filter:
        - ``"this_month"`` (default)
        - ``"last_month"``
        - ``"this_year"``
        - ``None`` / empty string → all time

    Returns
    -------
    dict
        ``{"ledger": {...}, "line_items": [...], "totals": {...}}`` on
        success, or ``{"status": "error", "message": ...}`` on failure.
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    if uid is None:
        return {"status": "error", "message": "No active user found"}

    # Normalise period
    if not period:
        period = None

    conn = get_db(server.paths.DB_PATH)
    try:
        ledger_row = conn.execute(
            "SELECT id, name, type, description FROM ledgers "
            "WHERE id = ? AND (user_id = ? OR user_id IS NULL)",
            (ledger_id, uid),
        ).fetchone()
        if ledger_row is None:
            return {"status": "error", "message": f"Ledger '{ledger_id}' not found"}

        return _build_ledger_drilldown(conn, ledger_row, period=period)
    finally:
        conn.close()


@mcp.tool
def add_ledger(name: str) -> dict:
    """Create a new ledger for the active user.

    Parameters
    ----------
    name : str
        Non-empty ledger name.  Returns an error if a ledger with this name
        already exists for the active user.
    """
    name = name.strip() if name else ""
    if not name:
        return {"status": "error", "message": "Ledger name must be non-empty"}

    uid = get_active_user_id(server.paths.DB_PATH)
    if uid is None:
        return {"status": "error", "message": "No active user"}

    conn = get_db(server.paths.DB_PATH)
    try:
        existing = conn.execute(
            "SELECT id FROM ledgers WHERE name = ? AND user_id = ?",
            (name, uid),
        ).fetchone()
        if existing:
            return {"status": "error", "message": f"Ledger '{name}' already exists"}
        ledger_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, name, uid),
        )
        conn.commit()
    finally:
        conn.close()

    return {"status": "ok", "ledger_id": ledger_id}


@mcp.tool
def add_line_item(ledger_id: str, name: str, item_type: str) -> dict:
    """Add a new line item to a ledger owned by the active user.

    Parameters
    ----------
    ledger_id : str
        ID of the target ledger.
    name : str
        Non-empty display name for the line item.
    item_type : str
        Must be ``'income'`` or ``'expense'``.
    """
    name = name.strip() if name else ""
    if not name:
        return {"status": "error", "message": "Line item name must be non-empty"}
    if item_type not in ("income", "expense"):
        return {"status": "error", "message": "item_type must be 'income' or 'expense'"}

    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            ledger_row = conn.execute(
                "SELECT id FROM ledgers WHERE id = ? AND (user_id = ? OR user_id IS NULL)",
                (ledger_id, uid),
            ).fetchone()
        else:
            ledger_row = conn.execute(
                "SELECT id FROM ledgers WHERE id = ?",
                (ledger_id,),
            ).fetchone()
        if ledger_row is None:
            return {
                "status": "error",
                "message": f"Ledger '{ledger_id}' not found or not owned by active user",
            }

        item_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (item_id, ledger_id, name, item_type),
        )
        conn.commit()
    finally:
        conn.close()

    return {"status": "ok", "item_id": item_id}


@mcp.tool
def remove_line_item(id: str) -> dict:
    """Remove a line item from a ledger.

    The active user must own the ledger the item belongs to.  If any
    ``transaction_entries`` reference this item the deletion is refused —
    delete the entries first or re-route those transactions.
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            row = conn.execute(
                """
                SELECT li.id FROM line_items li
                JOIN ledgers l ON l.id = li.ledger_id
                WHERE li.id = ? AND (l.user_id = ? OR l.user_id IS NULL)
                """,
                (id, uid),
            ).fetchone()
        else:
            row = conn.execute("SELECT id FROM line_items WHERE id = ?", (id,)).fetchone()
        if row is None:
            return {
                "status": "error",
                "message": f"Line item '{id}' not found or not owned by active user",
            }

        entry_count = conn.execute(
            "SELECT COUNT(*) FROM transaction_entries WHERE line_item_id = ?",
            (id,),
        ).fetchone()[0]
        if entry_count > 0:
            return {
                "status": "error",
                "message": "Line item has attached entries. Delete them first or re-route transactions.",
            }

        conn.execute("DELETE FROM line_items WHERE id = ?", (id,))
        conn.commit()
    finally:
        conn.close()

    return {"status": "ok"}


@mcp.tool
def set_account_ledger(account_id: str, ledger_id: str) -> dict:
    """Link a bank account to a default ledger for transaction routing.

    Transactions from this account will be routed to the specified ledger by
    default during classification.

    Parameters
    ----------
    account_id : str
        Internal bank_account id.
    ledger_id : str
        ID of the target ledger (must belong to the active user).

    Returns
    -------
    dict
        ``{"status": "ok"}`` on success or ``{"status": "error", ...}``.
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        # Verify account belongs to active user (via bank_connections.user_id)
        if uid:
            acct_row = conn.execute(
                """
                SELECT ba.id FROM bank_accounts ba
                JOIN bank_connections bc ON bc.id = ba.connection_id
                WHERE ba.id = ? AND bc.user_id = ?
                """,
                (account_id, uid),
            ).fetchone()
        else:
            acct_row = conn.execute(
                "SELECT id FROM bank_accounts WHERE id = ?", (account_id,)
            ).fetchone()

        if acct_row is None:
            return {
                "status": "error",
                "message": f"account_id {account_id!r} not found or not owned by active user",
            }

        # Verify ledger belongs to active user
        if uid:
            ledger_row = conn.execute(
                "SELECT id FROM ledgers WHERE id = ? AND (user_id = ? OR user_id IS NULL)",
                (ledger_id, uid),
            ).fetchone()
        else:
            ledger_row = conn.execute(
                "SELECT id FROM ledgers WHERE id = ?", (ledger_id,)
            ).fetchone()

        if ledger_row is None:
            return {
                "status": "error",
                "message": f"ledger_id {ledger_id!r} not found or not owned by active user",
            }

        conn.execute(
            "UPDATE bank_accounts SET default_ledger_id = ? WHERE id = ?",
            (ledger_id, account_id),
        )
        conn.commit()
    finally:
        conn.close()

    return {"status": "ok"}


@mcp.tool
def create_property_ledger(name: str, description: str = None) -> dict:
    """Create a ledger for a rental/investment property with default line items.

    Seeds 6 standard line items:
      Income: ``Rent income``
      Expenses: ``Mortgage``, ``Property tax``, ``Maintenance & repairs``,
                ``Insurance``, ``Utilities``

    Parameters
    ----------
    name : str
        Ledger name (e.g. "123 Main St").
    description : str, optional
        Optional address or label (e.g. "2-bed condo, downtown").

    Returns
    -------
    dict
        ``{"status": "ok", "ledger_id": "<uuid>"}``
    """
    name = name.strip() if name else ""
    if not name:
        return {"status": "error", "message": "Ledger name must be non-empty"}

    uid = get_active_user_id(server.paths.DB_PATH)
    if uid is None:
        return {"status": "error", "message": "No active user"}

    _PROPERTY_LINE_ITEMS = [
        ("Rent income", "income"),
        ("Mortgage", "expense"),
        ("Property tax", "expense"),
        ("Maintenance & repairs", "expense"),
        ("Insurance", "expense"),
        ("Utilities", "expense"),
    ]

    ledger_id = str(uuid.uuid4())
    conn = get_db(server.paths.DB_PATH)
    try:
        with db_txn(conn):
            conn.execute(
                "INSERT INTO ledgers (id, name, user_id, type, description) "
                "VALUES (?, ?, ?, 'property', ?)",
                (ledger_id, name, uid, description),
            )
            for item_name, item_type in _PROPERTY_LINE_ITEMS:
                conn.execute(
                    "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                    (str(uuid.uuid4()), ledger_id, item_name, item_type),
                )
    finally:
        conn.close()

    return {"status": "ok", "ledger_id": ledger_id}


@mcp.tool
def create_investment_ledger(name: str) -> dict:
    """Create a ledger for tracking investments with default line items.

    Seeds 2 standard line items:
      ``Contributions`` (expense), ``Dividends & Returns`` (income)

    Parameters
    ----------
    name : str
        Ledger name (e.g. "TFSA", "RRSP").

    Returns
    -------
    dict
        ``{"status": "ok", "ledger_id": "<uuid>"}``
    """
    name = name.strip() if name else ""
    if not name:
        return {"status": "error", "message": "Ledger name must be non-empty"}

    uid = get_active_user_id(server.paths.DB_PATH)
    if uid is None:
        return {"status": "error", "message": "No active user"}

    _INVESTMENT_LINE_ITEMS = [
        ("Contributions", "expense"),
        ("Dividends & Returns", "income"),
    ]

    ledger_id = str(uuid.uuid4())
    conn = get_db(server.paths.DB_PATH)
    try:
        with db_txn(conn):
            conn.execute(
                "INSERT INTO ledgers (id, name, user_id, type) VALUES (?, ?, ?, 'investment')",
                (ledger_id, name, uid),
            )
            for item_name, item_type in _INVESTMENT_LINE_ITEMS:
                conn.execute(
                    "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
                    (str(uuid.uuid4()), ledger_id, item_name, item_type),
                )
    finally:
        conn.close()

    return {"status": "ok", "ledger_id": ledger_id}


# ---------------------------------------------------------------------------
# Transaction tools
# ---------------------------------------------------------------------------


def classify_pending_transactions(user_id: str, limit: int | None = None) -> dict:
    """Classify all unclassified transactions for *user_id* and write entries.

    Finds transactions owned by *user_id* that have no row in
    ``transaction_entries``, then for each one:

    1. Builds a rich transaction dict (merchant, amount, date, account
       name/description, plaid_category).
    2. Calls :func:`get_transfer_hint` to check for possible internal
       transfers and passes the result as context to the LLM.
    3. Calls :func:`classify_with_rules` with the active
       ``classification_rules`` and the transfer hint.
    4. If ``classification_type == 'skip'`` → no entry is written; counted
       as skipped.
    5. If ``line_item_id`` is set → inserts a ``transaction_entries`` row
       linking the transaction to that line item.
    6. If ``line_item_id`` is None but the owning account has a
       ``default_ledger_id`` → picks a fallback line item from that ledger
       (first income item for 'income', first expense item for all others).
    7. If no fallback is found → transaction is left unrouted and counted
       as 'uncertain'.

    Already-classified transactions (any existing row in
    ``transaction_entries``) are always skipped → idempotent.

    Args:
        user_id: The user whose transactions to classify.

    Returns:
        ``{"classified": N, "skipped": M, "uncertain": K}``
    """
    classified = 0
    skipped = 0
    uncertain = 0

    if not user_id:
        return {"classified": classified, "skipped": skipped, "uncertain": uncertain}

    conn = get_db(server.paths.DB_PATH)
    try:
        # Fetch rules / ledger tree / hints ONCE — shared across all
        # transactions in this pass (issue #205 unified classifier).
        rules_result = list_rules()
        rules = rules_result.get("rules", [])

        from server.classifier import _build_ledger_tree, _fetch_hints

        ledger_tree_text = _build_ledger_tree(conn)
        hints_list = _fetch_hints(conn)

        # Fetch all unclassified, non-pending transactions for this user.
        unclassified = conn.execute(
            """
            SELECT t.id, t.merchant, t.amount, t.date,
                   t.plaid_category, t.bank_account_id
            FROM transactions t
            JOIN bank_accounts ba ON ba.id = t.bank_account_id
            JOIN bank_connections bc ON bc.id = ba.connection_id
            WHERE bc.user_id = ?
              AND t.pending = 0
              AND NOT EXISTS (
                SELECT 1 FROM transaction_entries te
                WHERE te.transaction_id = t.id
              )
            ORDER BY t.date DESC
            """,
            (user_id,),
        ).fetchall()
        if limit:
            unclassified = unclassified[: int(limit)]

        for row in unclassified:
            tx_id = row["id"]
            merchant = row["merchant"] or ""
            amount = row["amount"]
            date = row["date"]
            plaid_category = row["plaid_category"] or ""
            bank_account_id = row["bank_account_id"]

            # Enrich with account context.
            ba_row = conn.execute(
                "SELECT name, description, default_ledger_id FROM bank_accounts WHERE id = ?",
                (bank_account_id,),
            ).fetchone()
            account_name = ba_row["name"] if ba_row else None
            account_description = ba_row["description"] if ba_row else None
            default_ledger_id = ba_row["default_ledger_id"] if ba_row else None

            tx_dict = {
                "merchant": merchant,
                "amount": amount,
                "date": date,
                "account_name": account_name,
                "account_description": account_description,
                "plaid_category": plaid_category,
            }

            # Build transfer hint context.
            try:
                hint = get_transfer_hint(tx_id, str(server.paths.DB_PATH))
            except Exception:
                hint = None

            context: dict | None = None
            if hint and hint.get("is_possible_transfer"):
                context = {"possible_internal_transfer": True}

            # Run UNIFIED classifier — ONE LLM call per transaction with all
            # context (rules + ledger tree + hints + transfer hint + account).
            try:
                result = classify_transaction(
                    conn,
                    tx_dict,
                    rules,
                    ledger_tree=ledger_tree_text,
                    hints=hints_list,
                    context=context,
                )
            except Exception as exc:
                _logger.warning(
                    "classify_pending_transactions: classify_transaction failed for tx_id=%s: %s",
                    tx_id,
                    exc,
                )
                uncertain += 1
                continue

            classification_type = result.get("classification_type", "spending")
            line_item_id = result.get("line_item_id")
            confidence = float(result.get("confidence", 0.0))
            is_uncertain = bool(result.get("uncertain", False))
            reasoning = result.get("reasoning", "")

            # skip → don't write entry.
            if classification_type == "skip":
                # Still write a skip entry so we don't re-process.
                entry_id = str(uuid.uuid4())
                conn.execute(
                    "INSERT OR IGNORE INTO transaction_entries "
                    "(id, transaction_id, ledger_id, line_item_id, amount, "
                    " entry_type, source, confidence, uncertain, reasoning, reviewed) "
                    "VALUES (?, ?, NULL, NULL, ?, 'skip', 'llm', ?, ?, ?, 0)",
                    (entry_id, tx_id, amount, confidence, 1 if is_uncertain else 0, reasoning),
                )
                conn.commit()
                skipped += 1
                continue

            # Resolve ledger_id from line_item if we have one.
            ledger_id = None
            if line_item_id:
                li_row = conn.execute(
                    "SELECT ledger_id FROM line_items WHERE id = ?",
                    (line_item_id,),
                ).fetchone()
                if li_row:
                    ledger_id = li_row["ledger_id"]
                else:
                    # line_item_id is stale/invalid; clear it.
                    line_item_id = None

            # Derive classification_type from the resolved line item's
            # item_type so income line items always get entry_type='income'.
            if line_item_id:
                li_type_row = conn.execute(
                    "SELECT item_type FROM line_items WHERE id = ?",
                    (line_item_id,),
                ).fetchone()
                if li_type_row and li_type_row["item_type"] == "income":
                    classification_type = "income"
                elif classification_type not in ("transfer", "savings", "skip"):
                    classification_type = "spending"

            # Last resort: if still no line_item_id but account has a default
            # ledger, grab the first matching line item from that ledger.
            if line_item_id is None and default_ledger_id:
                item_type_filter = "income" if classification_type == "income" else "expense"
                fallback_row = conn.execute(
                    "SELECT id, ledger_id FROM line_items "
                    " WHERE ledger_id = ? AND item_type = ? ORDER BY name LIMIT 1",
                    (default_ledger_id, item_type_filter),
                ).fetchone()
                if fallback_row:
                    line_item_id = fallback_row["id"]
                    ledger_id = fallback_row["ledger_id"]

            if line_item_id is None:
                # Could not route — mark uncertain and leave unrouted entry so
                # get_needs_review() can surface it.
                entry_id = str(uuid.uuid4())
                conn.execute(
                    "INSERT OR IGNORE INTO transaction_entries "
                    "(id, transaction_id, ledger_id, line_item_id, amount, "
                    " entry_type, source, confidence, uncertain, reasoning, reviewed) "
                    "VALUES (?, ?, NULL, NULL, ?, ?, 'llm', ?, 1, ?, 0)",
                    (
                        entry_id,
                        tx_id,
                        amount,
                        classification_type,
                        confidence,
                        reasoning,
                    ),
                )
                conn.commit()
                uncertain += 1
                continue

            # Write the classified entry.
            # Normalise the stored amount to always be positive.
            # Plaid uses negative amounts for money coming IN (income, refunds,
            # transfers received, credit card payments). We always store ABS so
            # ledger totals are additive and display correctly regardless of
            # which direction the money flowed.
            stored_amount = abs(amount)
            entry_id = str(uuid.uuid4())
            conn.execute(
                "INSERT OR IGNORE INTO transaction_entries "
                "(id, transaction_id, ledger_id, line_item_id, amount, "
                " entry_type, source, confidence, uncertain, reasoning, reviewed) "
                "VALUES (?, ?, ?, ?, ?, ?, 'llm', ?, ?, ?, 0)",
                (
                    entry_id,
                    tx_id,
                    ledger_id,
                    line_item_id,
                    stored_amount,
                    classification_type,
                    confidence,
                    1 if is_uncertain else 0,
                    reasoning,
                ),
            )
            conn.commit()
            classified += 1

    finally:
        conn.close()

    return {"classified": classified, "skipped": skipped, "uncertain": uncertain}


@mcp.tool
def sync() -> dict:
    """Pull new transactions from Plaid, classify them, and return a summary."""

    def _get(obj, key, default=None):
        """Get a field from a dict or an SDK object."""
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def _is_reauth_error(exc: Exception) -> bool:
        """Return True when *exc* signals ITEM_LOGIN_REQUIRED."""
        body = getattr(exc, "body", None)
        if body:
            try:
                parsed = _json.loads(body)
                return parsed.get("error_code") == "ITEM_LOGIN_REQUIRED"
            except Exception:
                pass
        return False

    connections_synced = 0
    total_added = 0
    total_modified = 0
    total_removed = 0
    total_classified = 0

    health_check_result: dict = {}

    try:
        with sync_lock(timeout=0.0):
            db_conn = get_db(server.paths.DB_PATH)
            try:
                # Run health check first so stale/expired connections are
                # updated before we attempt to sync them.
                health_check_result = server.health_monitor.check_all_connections(
                    db_conn, plaid_provider=_plaid
                )

                active_conns = db_conn.execute(
                    "SELECT id, plaid_access_token_encrypted, plaid_env, user_id "
                    "FROM bank_connections WHERE status = 'active'"
                ).fetchall()

                for bc in active_conns:
                    connection_id = bc["id"]
                    encrypted_token = bc["plaid_access_token_encrypted"]
                    access_token = server.crypto.decrypt(encrypted_token)
                    conn_plaid_env = bc["plaid_env"] or "sandbox"
                    conn_user_id = bc["user_id"]

                    # Load per-user credentials from DB (falls back to env vars).
                    cred_client_id, cred_secret, _ = _get_plaid_credentials(conn_user_id)

                    # Per-connection provider locked to the stored env.
                    conn_provider = PlaidProvider(
                        env=conn_plaid_env,
                        client_id=cred_client_id,
                        secret=cred_secret,
                    )
                    if conn_provider.env != conn_plaid_env:
                        raise ValueError(
                            f"Environment mismatch: connection {connection_id!r} "
                            f"was linked in env '{conn_plaid_env}' but resolved "
                            f"provider env is '{conn_provider.env}'"
                        )

                    cursor_row = db_conn.execute(
                        "SELECT cursor FROM sync_cursors WHERE connection_id = ?",
                        (connection_id,),
                    ).fetchone()
                    cursor = cursor_row["cursor"] if cursor_row else None

                    try:
                        result = conn_provider.sync_transactions(access_token, cursor)
                    except Exception as e:
                        if _is_reauth_error(e):
                            with db_txn(db_conn):
                                db_conn.execute(
                                    "UPDATE bank_connections SET status='needs_reauth' WHERE id=?",
                                    (connection_id,),
                                )
                            continue
                        raise

                    added_txns = result.get("added", []) if isinstance(result, dict) else []
                    modified_txns = result.get("modified", []) if isinstance(result, dict) else []
                    removed_txns = result.get("removed", []) if isinstance(result, dict) else []
                    next_cursor = result.get("next_cursor") if isinstance(result, dict) else None
                    accounts_list = result.get("accounts", []) if isinstance(result, dict) else []

                    # Build a lookup map: plaid_account_id -> {name, type, currency}
                    # Use official_name if present, else fall back to name.
                    account_meta: dict[str, dict] = {}
                    for acct in accounts_list:
                        acct_id = _get(acct, "account_id")
                        if acct_id:
                            acct_name = _get(acct, "official_name") or _get(acct, "name")
                            acct_type = _get(acct, "type")
                            # type may come back as an enum object; coerce to string
                            if acct_type is not None and not isinstance(acct_type, str):
                                acct_type = str(acct_type)
                            # iso_currency_code from balances; fall back to 'CAD'
                            balances = _get(acct, "balances") or {}
                            acct_currency = _get(balances, "iso_currency_code") or "CAD"
                            account_meta[acct_id] = {
                                "name": acct_name,
                                "type": acct_type,
                                "currency": acct_currency,
                                "balance_current": _get(balances, "current"),
                                "balance_available": _get(balances, "available"),
                            }

                    now = int(_time.time())
                    conn_added = 0
                    conn_modified = 0
                    conn_removed = 0
                    conn_classified = 0

                    # Always upsert account rows and update names, types,
                    # currencies, and balances from the accounts list — even
                    # when no new transactions came back.  This ensures that
                    # bank_accounts is populated on the very first sync for
                    # accounts with no transaction history yet.
                    with db_txn(db_conn):
                        for plaid_acct_id, meta in account_meta.items():
                            # INSERT the row if it doesn't exist yet (first sync
                            # for an account that has no transactions).
                            db_conn.execute(
                                "INSERT OR IGNORE INTO bank_accounts "
                                "(id, connection_id, plaid_account_id) VALUES (?, ?, ?)",
                                (str(uuid.uuid4()), connection_id, plaid_acct_id),
                            )
                            db_conn.execute(
                                "UPDATE bank_accounts SET "
                                "name = COALESCE(NULLIF(name, ''), ?), "
                                "type = COALESCE(NULLIF(type, ''), ?), "
                                "currency = ?, "
                                "balance_current = ?, "
                                "balance_available = ? "
                                "WHERE plaid_account_id = ?",
                                (
                                    meta.get("name"),
                                    meta.get("type"),
                                    meta.get("currency") or "CAD",
                                    meta.get("balance_current"),
                                    meta.get("balance_available"),
                                    plaid_acct_id,
                                ),
                            )

                    with db_txn(db_conn):
                        # --- Added transactions ---
                        for txn in added_txns:
                            plaid_account_id = _get(txn, "account_id")
                            plaid_txn_id = _get(txn, "transaction_id")
                            date = _get(txn, "date")
                            # authorized_datetime is an ISO-8601 string with time (e.g.
                            # "2024-01-15T14:23:00Z"); fall back to datetime then None.
                            authorized_datetime = (
                                _get(txn, "authorized_datetime") or _get(txn, "datetime") or None
                            )
                            name = _get(txn, "name") or ""
                            merchant_name = _get(txn, "merchant_name") or ""
                            merchant = merchant_name if merchant_name else name
                            amount = _get(txn, "amount")
                            pending = bool(_get(txn, "pending", False))

                            # Upsert bank_account (INSERT OR IGNORE on plaid_account_id UNIQUE)
                            db_conn.execute(
                                "INSERT OR IGNORE INTO bank_accounts "
                                "(id, connection_id, plaid_account_id) VALUES (?, ?, ?)",
                                (str(uuid.uuid4()), connection_id, plaid_account_id),
                            )
                            ba_row = db_conn.execute(
                                "SELECT id FROM bank_accounts WHERE plaid_account_id = ?",
                                (plaid_account_id,),
                            ).fetchone()
                            bank_account_id = ba_row["id"]

                            # Populate name/type/currency from account metadata (idempotent —
                            # only overwrites when the incoming value is non-null so
                            # a second sync won't blank out rows with good data).
                            acct_currency = "CAD"  # default
                            if plaid_account_id in account_meta:
                                meta = account_meta[plaid_account_id]
                                if meta["name"] is not None:
                                    db_conn.execute(
                                        "UPDATE bank_accounts SET name = ? "
                                        "WHERE plaid_account_id = ? AND (name IS NULL OR name = '')",
                                        (meta["name"], plaid_account_id),
                                    )
                                if meta["type"] is not None:
                                    db_conn.execute(
                                        "UPDATE bank_accounts SET type = ? "
                                        "WHERE plaid_account_id = ? AND (type IS NULL OR type = '')",
                                        (meta["type"], plaid_account_id),
                                    )
                                # Always update currency + balances from Plaid (authoritative)
                                acct_currency = meta.get("currency") or "CAD"
                                db_conn.execute(
                                    "UPDATE bank_accounts SET currency = ?, "
                                    "balance_current = ?, balance_available = ? "
                                    "WHERE plaid_account_id = ?",
                                    (
                                        acct_currency,
                                        meta.get("balance_current"),
                                        meta.get("balance_available"),
                                        plaid_account_id,
                                    ),
                                )

                            txn_id = str(uuid.uuid4())
                            cur = db_conn.execute(
                                "INSERT OR IGNORE INTO transactions "
                                "(id, bank_account_id, plaid_transaction_id, date, authorized_datetime, merchant, amount, currency, pending) "
                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (
                                    txn_id,
                                    bank_account_id,
                                    plaid_txn_id,
                                    str(date) if date is not None else None,
                                    (
                                        str(authorized_datetime)
                                        if authorized_datetime is not None
                                        else None
                                    ),
                                    merchant,
                                    amount,
                                    acct_currency,
                                    1 if pending else 0,
                                ),
                            )

                            if cur.rowcount > 0:
                                # Newly inserted — count and attempt Tier-1 classification
                                conn_added += 1
                                txn_dict = {
                                    "id": txn_id,
                                    "merchant": merchant,
                                    "amount": amount,
                                    "bank_account_id": bank_account_id,
                                }
                                entry = apply_rules(db_conn, txn_dict)
                                if entry is not None:
                                    db_conn.execute(
                                        "INSERT OR IGNORE INTO transaction_entries "
                                        "(id, transaction_id, ledger_id, line_item_id, "
                                        " amount, source, confidence, reviewed) "
                                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                        (
                                            str(uuid.uuid4()),
                                            entry["transaction_id"],
                                            entry["ledger_id"],
                                            entry["line_item_id"],
                                            entry["amount"],
                                            entry["source"],
                                            entry["confidence"],
                                            entry["reviewed"],
                                        ),
                                    )
                                    conn_classified += 1

                                # NOTE (issue #205): the previous in-sync
                                # ``classify_with_rules`` debug-only call was
                                # removed because classification is now done
                                # post-sync by the unified ``classify_pending_transactions``
                                # pipeline (one LLM call per transaction, not
                                # two). Keeping it here would double the LLM
                                # spend for every synced transaction.

                        # --- Modified transactions ---
                        for txn in modified_txns:
                            plaid_txn_id = _get(txn, "transaction_id")
                            date = _get(txn, "date")
                            authorized_datetime = (
                                _get(txn, "authorized_datetime") or _get(txn, "datetime") or None
                            )
                            name = _get(txn, "name") or ""
                            merchant_name = _get(txn, "merchant_name") or ""
                            merchant = merchant_name if merchant_name else name
                            amount = _get(txn, "amount")
                            pending = bool(_get(txn, "pending", False))
                            db_conn.execute(
                                "UPDATE transactions "
                                "SET date=?, authorized_datetime=?, merchant=?, amount=?, pending=? "
                                "WHERE plaid_transaction_id=?",
                                (
                                    str(date) if date is not None else None,
                                    (
                                        str(authorized_datetime)
                                        if authorized_datetime is not None
                                        else None
                                    ),
                                    merchant,
                                    amount,
                                    1 if pending else 0,
                                    plaid_txn_id,
                                ),
                            )
                            conn_modified += 1

                        # --- Removed transactions ---
                        for txn in removed_txns:
                            plaid_txn_id = _get(txn, "transaction_id")
                            db_conn.execute(
                                "DELETE FROM transactions WHERE plaid_transaction_id = ?",
                                (plaid_txn_id,),
                            )
                            conn_removed += 1

                        # Upsert cursor — advances ONLY on full success of this batch
                        db_conn.execute(
                            "INSERT INTO sync_cursors (connection_id, cursor, last_synced_at) "
                            "VALUES (?, ?, ?) "
                            "ON CONFLICT(connection_id) DO UPDATE SET "
                            "    cursor = excluded.cursor, "
                            "    last_synced_at = excluded.last_synced_at",
                            (connection_id, next_cursor, now),
                        )

                        db_conn.execute(
                            "UPDATE bank_connections SET last_synced_at=? WHERE id=?",
                            (now, connection_id),
                        )

                    connections_synced += 1
                    total_added += conn_added
                    total_modified += conn_modified
                    total_removed += conn_removed
                    total_classified += conn_classified

                # After all connections are synced, run auto-classification on
                # any newly inserted (unclassified) transactions.  Errors are
                # caught so a classification failure never blocks sync.
                auto_classify_result = {"classified": 0, "skipped": 0, "uncertain": 0}
                try:
                    uid = get_active_user_id(server.paths.DB_PATH)
                    if uid:
                        auto_classify_result = classify_pending_transactions(uid)
                except Exception as _exc:
                    _logger.warning("Auto-classification after sync failed: %s", _exc)

            finally:
                db_conn.close()

    except LockBusy:
        return {"status": "already_running"}

    return {
        "status": "ok",
        "connections_synced": connections_synced,
        "added": total_added,
        "modified": total_modified,
        "removed": total_removed,
        "classified_by_rule": total_classified,
        "auto_classified": auto_classify_result.get("classified", 0),
        "auto_skipped": auto_classify_result.get("skipped", 0),
        "auto_uncertain": auto_classify_result.get("uncertain", 0),
        "health_check": health_check_result,
    }


@mcp.tool
def list(filters: Optional[dict] = None) -> dict:
    """Query transactions with optional filters.

    Supported filter keys (all optional):
      date_from    (str, ISO date, inclusive)
      date_to      (str, ISO date, inclusive)
      ledger_id    (str)
      line_item_id (str)
      reviewed     (bool)
      source       (str: "rule" | "llm" | "manual")
    """
    filters = filters or {}
    conditions: list[str] = []
    params: list = []

    if "date_from" in filters:
        conditions.append("t.date >= ?")
        params.append(filters["date_from"])
    if "date_to" in filters:
        conditions.append("t.date <= ?")
        params.append(filters["date_to"])
    if "ledger_id" in filters:
        conditions.append("te.ledger_id = ?")
        params.append(filters["ledger_id"])
    if "line_item_id" in filters:
        conditions.append("te.line_item_id = ?")
        params.append(filters["line_item_id"])
    if "reviewed" in filters:
        conditions.append("te.reviewed = ?")
        params.append(1 if filters["reviewed"] else 0)
    if "source" in filters:
        conditions.append("te.source = ?")
        params.append(filters["source"])

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    sql = f"""
        SELECT
            te.id,
            te.transaction_id,
            te.ledger_id,
            te.line_item_id,
            te.amount,
            te.source,
            te.confidence,
            te.reviewed,
            t.date,
            t.merchant,
            t.amount AS transaction_amount,
            t.currency
        FROM transaction_entries te
        JOIN transactions t ON t.id = te.transaction_id
        {where_clause}
        ORDER BY t.date DESC, te.id
    """

    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute(sql, params).fetchall()
        entries = [dict(r) for r in rows]
    finally:
        conn.close()

    return {"entries": entries}


@mcp.tool
def get_needs_review() -> dict:
    """Return transactions that need manual classification review.

    Returns transactions where the classifier was uncertain
    (``uncertain=1`` in ``transaction_entries``) OR where no
    ``line_item_id`` was assigned (unrouted), scoped to the active user.

    Returns
    -------
    dict
        ``{"transactions": [{id, merchant, amount, date, account_name,
        reasoning}, ...]}``
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    if not uid:
        return {"transactions": []}

    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute(
            """
            SELECT t.id, t.merchant, t.amount, t.date,
                   ba.name AS account_name,
                   te.reasoning
            FROM transaction_entries te
            JOIN transactions t ON t.id = te.transaction_id
            JOIN bank_accounts ba ON ba.id = t.bank_account_id
            JOIN bank_connections bc ON bc.id = ba.connection_id
            WHERE bc.user_id = ?
              AND te.reviewed = 0
              AND (
                te.uncertain = 1
                OR te.line_item_id IS NULL
              )
              AND te.entry_type != 'skip'
            ORDER BY t.date DESC
            """,
            (uid,),
        ).fetchall()
        return {
            "transactions": [
                {
                    "id": r["id"],
                    "merchant": r["merchant"],
                    "amount": r["amount"],
                    "date": r["date"],
                    "account_name": r["account_name"],
                    "reasoning": r["reasoning"] or "",
                }
                for r in rows
            ]
        }
    finally:
        conn.close()


@mcp.tool
def get_needs_review_summary() -> dict:
    """Return a pre-formatted batch summary of transactions needing manual review.

    Designed to be called immediately after ``sync`` so the agent can surface
    uncertain or unrouted transactions to the user in a single, readable
    message rather than one message per transaction.

    The summary is intentionally terse: merchant, amount, date, and the
    classifier's reasoning (when available) are included for each item so the
    user has just enough context to reply with the correct classification.

    Returns
    -------
    dict
        ``{"count": int, "summary": str, "transactions": [...]}``

        * ``count`` — number of transactions needing review (0 when none).
        * ``summary`` — human-readable batch message suitable for presenting
          directly to the user.  Empty string when ``count == 0``.
        * ``transactions`` — raw list (same shape as ``get_needs_review``) for
          downstream processing (corrections, rule proposals, etc.).
    """
    result = get_needs_review()
    transactions = result.get("transactions", [])
    count = len(transactions)

    if count == 0:
        return {"count": 0, "summary": "", "transactions": []}

    lines = [
        f"🔍 **{count} transaction{'s' if count != 1 else ''} need your review** after the latest sync:\n"
    ]
    for i, tx in enumerate(transactions, 1):
        amount = tx.get("amount", 0)
        merchant = tx.get("merchant") or "Unknown merchant"
        date = tx.get("date", "")
        account = tx.get("account_name", "")
        reasoning = tx.get("reasoning", "")

        amount_str = f"${abs(amount):.2f}" if amount is not None else "$?.??"
        line = f"{i}. **{merchant}** — {amount_str} on {date}"
        if account:
            line += f" ({account})"
        if reasoning:
            line += f"\n   _Classifier note: {reasoning}_"
        lines.append(line)

    lines.append(
        "\nReply with the correct category for each, or say 'skip' to leave them for later."
    )

    return {
        "count": count,
        "summary": "\n".join(lines),
        "transactions": transactions,
    }


@mcp.tool
def route(transaction_id: str, allocations: List) -> dict:
    """Manually route a transaction to one or more line items."""
    return {"status": "not_implemented"}


@mcp.tool
def add_hint(text: str) -> dict:
    """Save a natural-language classification hint for the current user."""
    cleaned = text.strip()
    if len(cleaned) < 1:
        raise ValueError("hint text must be non-empty")
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            existing = conn.execute(
                "SELECT id FROM classification_hints WHERE text = ? AND user_id = ?",
                (cleaned, uid),
            ).fetchone()
        else:
            existing = conn.execute(
                "SELECT id FROM classification_hints WHERE text = ?",
                (cleaned,),
            ).fetchone()
        if existing:
            return {"id": existing["id"], "text": cleaned, "created": False}
        new_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO classification_hints (id, text, user_id) VALUES (?, ?, ?)",
            (new_id, cleaned, uid),
        )
        conn.commit()
        return {"id": new_id, "text": cleaned, "created": True}
    finally:
        conn.close()


@mcp.tool
def list_hints() -> dict:
    """Return all classification hints for the current user."""
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            rows = conn.execute(
                "SELECT id, text FROM classification_hints WHERE user_id = ? ORDER BY rowid",
                (uid,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, text FROM classification_hints ORDER BY rowid"
            ).fetchall()
        return {"hints": [{"id": row["id"], "text": row["text"]} for row in rows]}
    finally:
        conn.close()


@mcp.tool
def remove_hint(id: str) -> dict:
    """Delete a classification hint by id."""
    conn = get_db(server.paths.DB_PATH)
    try:
        cursor = conn.execute(
            "DELETE FROM classification_hints WHERE id = ?",
            (id,),
        )
        conn.commit()
        return {"ok": True, "removed": cursor.rowcount > 0}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Onboarding tools (issue #206)
# ---------------------------------------------------------------------------


# Canonical question keys used by the guided onboarding flow.  Agents can
# call ``setup_interview`` with any string here — these are the
# recommended ones the SKILL.md onboarding hook will use.
SETUP_INTERVIEW_QUESTIONS: list[dict] = [
    {
        "key": "account_owners",
        "prompt": "Who's on these accounts? Just you, a partner, shared family accounts?",
    },
    {
        "key": "employer",
        "prompt": "Who is your employer? (So payroll deposits can be correctly identified.)",
    },
    {
        "key": "subscriptions",
        "prompt": "What subscriptions do you pay for? (Netflix, Disney+, Spotify, iCloud, etc.)",
    },
    {
        "key": "utilities",
        "prompt": "Who are your utility providers? (Hydro, gas, internet, phone.)",
    },
    {"key": "properties", "prompt": "Do you have any rental properties or investment accounts?"},
    {
        "key": "recurring_other",
        "prompt": "Anything else you pay regularly that might be hard to recognise? (Obscure merchant names, foreign currency, etc.)",
    },
]


@mcp.tool
def list_setup_interview_questions() -> dict:
    """Return the recommended onboarding interview questions.

    The guided onboarding hook in ``SKILL.md`` walks the user through these
    questions one at a time; answers are persisted via
    :func:`setup_interview`.  Agents are free to ask additional questions
    — the canonical list is purely a starting point so every install gets
    a consistent baseline.

    Returns
    -------
    dict
        ``{"questions": [{"key": str, "prompt": str}, ...]}``
    """
    return {"questions": [dict(q) for q in SETUP_INTERVIEW_QUESTIONS]}


@mcp.tool
def setup_interview(question_key: str, answer_text: str) -> dict:
    """Persist an onboarding interview answer for the active user.

    Stores the answer in the ``setup_interview`` table, scoped to the
    active user.  Re-answering the same ``question_key`` replaces the
    previous answer (the UNIQUE constraint on ``(user_id, question_key)``
    makes this an upsert).

    Parameters
    ----------
    question_key : str
        Short identifier for the question (e.g. ``"employer"``,
        ``"subscriptions"``).  Recommended keys live in
        ``SETUP_INTERVIEW_QUESTIONS``, but any non-empty string is allowed
        so agents can ask follow-ups.
    answer_text : str
        The user's answer in natural language.

    Returns
    -------
    dict
        ``{"id": <row id>, "question_key": str, "answer_text": str,
           "created": bool}``  — ``created`` is True for inserts and
        False for updates.
    """
    qk = (question_key or "").strip()
    ans = (answer_text or "").strip()
    if not qk:
        raise ValueError("question_key must be non-empty")
    if not ans:
        raise ValueError("answer_text must be non-empty")

    import time as _time

    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        existing = conn.execute(
            "SELECT id FROM setup_interview WHERE user_id IS ? AND question_key = ?",
            (uid, qk),
        ).fetchone()
        now = int(_time.time())
        if existing:
            conn.execute(
                "UPDATE setup_interview SET answer_text = ?, updated_at = ? WHERE id = ?",
                (ans, now, existing["id"]),
            )
            conn.commit()
            return {
                "id": existing["id"],
                "question_key": qk,
                "answer_text": ans,
                "created": False,
            }
        new_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO setup_interview "
            "(id, user_id, question_key, answer_text, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (new_id, uid, qk, ans, now, now),
        )
        conn.commit()
        return {
            "id": new_id,
            "question_key": qk,
            "answer_text": ans,
            "created": True,
        }
    finally:
        conn.close()


@mcp.tool
def list_setup_interview() -> dict:
    """Return all stored onboarding interview answers for the active user.

    Returns
    -------
    dict
        ``{"answers": [{"id", "question_key", "answer_text",
           "created_at", "updated_at"}, ...]}``
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            rows = conn.execute(
                "SELECT id, question_key, answer_text, created_at, updated_at "
                "FROM setup_interview WHERE user_id = ? ORDER BY created_at",
                (uid,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, question_key, answer_text, created_at, updated_at "
                "FROM setup_interview WHERE user_id IS NULL ORDER BY created_at"
            ).fetchall()
        return {
            "answers": [
                {
                    "id": r["id"],
                    "question_key": r["question_key"],
                    "answer_text": r["answer_text"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                }
                for r in rows
            ]
        }
    finally:
        conn.close()


@mcp.tool
def analyze_recurring_merchants(min_occurrences: int = 2, lookback_days: int = 90) -> dict:
    """Scan recent transactions and surface recurring merchants.

    The guided onboarding flow (#206) uses this to cross-reference the
    user's interview answers against what's actually in their accounts —
    e.g. confirming that a "Netflix" subscription answer is backed by a
    real recurring charge.

    A merchant is considered *recurring* when it appears at least
    ``min_occurrences`` times in the last ``lookback_days`` days.  Each
    returned entry also includes an inferred category derived from the
    most common Plaid category and current classification (when any).

    Parameters
    ----------
    min_occurrences : int
        Minimum number of transactions for a merchant to be returned.
        Defaults to 2.
    lookback_days : int
        How far back to look.  Defaults to 90 days.

    Returns
    -------
    dict
        ``{"merchants": [{"merchant": str, "occurrences": int,
          "avg_amount": float, "last_seen": str (ISO date),
          "plaid_category": str | None,
          "current_line_item": str | None,
          "current_ledger": str | None}, ...]}``
        Sorted by occurrences descending.
    """
    import datetime as _dt

    if min_occurrences < 1:
        raise ValueError("min_occurrences must be >= 1")
    if lookback_days < 1:
        raise ValueError("lookback_days must be >= 1")

    uid = get_active_user_id(server.paths.DB_PATH)
    cutoff = (_dt.date.today() - _dt.timedelta(days=lookback_days)).isoformat()

    conn = get_db(server.paths.DB_PATH)
    try:
        if uid:
            base_filter = (
                "  JOIN bank_accounts ba ON ba.id = t.bank_account_id\n"
                "  JOIN bank_connections bc ON bc.id = ba.connection_id\n"
                " WHERE bc.user_id = ?\n"
                "   AND t.merchant IS NOT NULL\n"
                "   AND TRIM(t.merchant) != ''\n"
                "   AND t.date >= ?\n"
            )
            params = (uid, cutoff)
        else:
            base_filter = (
                " WHERE t.merchant IS NOT NULL\n   AND TRIM(t.merchant) != ''\n   AND t.date >= ?\n"
            )
            params = (cutoff,)

        rows = conn.execute(
            f"""
            SELECT t.merchant,
                   COUNT(*) AS occurrences,
                   AVG(t.amount) AS avg_amount,
                   MAX(t.date) AS last_seen,
                   MAX(t.plaid_category) AS plaid_category
              FROM transactions t
              {base_filter}
             GROUP BY t.merchant
            HAVING COUNT(*) >= {int(min_occurrences)}
             ORDER BY occurrences DESC, last_seen DESC
            """,
            params,
        ).fetchall()

        merchants: list[dict] = []
        for r in rows:
            # Best-effort lookup of how this merchant is currently classified.
            cls_row = conn.execute(
                "SELECT li.name AS li_name, l.name AS ledger_name"
                "  FROM transaction_entries te"
                "  JOIN transactions t  ON t.id  = te.transaction_id"
                "  JOIN line_items   li ON li.id = te.line_item_id"
                "  JOIN ledgers      l  ON l.id  = te.ledger_id"
                " WHERE t.merchant = ?"
                " ORDER BY t.date DESC LIMIT 1",
                (r["merchant"],),
            ).fetchone()
            merchants.append(
                {
                    "merchant": r["merchant"],
                    "occurrences": int(r["occurrences"]),
                    "avg_amount": float(r["avg_amount"]) if r["avg_amount"] is not None else 0.0,
                    "last_seen": r["last_seen"],
                    "plaid_category": r["plaid_category"],
                    "current_line_item": cls_row["li_name"] if cls_row else None,
                    "current_ledger": cls_row["ledger_name"] if cls_row else None,
                }
            )
        return {"merchants": merchants}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Report tools
# ---------------------------------------------------------------------------


@mcp.tool
def summary(period: str) -> dict:
    """Return spending totals for a given period.

    Parameters
    ----------
    period : str
        One of:
          - ``"month"``  → current calendar month (YYYY-MM)
          - ``"year"``   → current calendar year (YYYY)
          - ``"ytd"``    → year-to-date (Jan 1 to today)
          - ``"YYYY-MM"`` → a specific month, e.g. ``"2026-05"``
          - ``"YYYY"``   → a specific year, e.g. ``"2026"``

    Returns
    -------
    dict
        ::

            {
              "period": str,
              "income": float,
              "expenses": float,
              "net": float,      # income - expenses
              "by_line_item": [
                {"line_item": str, "ledger": str, "type": str, "total": float},
                ...
              ]
            }

        ``by_line_item`` is sorted by ``total`` descending (most positive
        income first, then expenses sorted least-negative last — i.e. simple
        descending numeric sort on the raw total value).
    """
    import re as _re

    today = _datetime.now().date()
    today_str = today.isoformat()  # "YYYY-MM-DD"
    year_str = today_str[:4]  # "YYYY"
    month_prefix = today_str[:7]  # "YYYY-MM"

    # Build a WHERE clause fragment and params for ``transactions.date``.
    # We use LIKE patterns wherever possible (index-friendly for TEXT dates).
    _MONTH_RE = _re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
    _YEAR_RE = _re.compile(r"^\d{4}$")

    if period == "month":
        date_filter = "t.date LIKE ?"
        date_params: list = [f"{month_prefix}-%"]
    elif period == "year":
        date_filter = "t.date LIKE ?"
        date_params = [f"{year_str}-%"]
    elif period == "ytd":
        ytd_start = f"{year_str}-01-01"
        date_filter = "t.date >= ? AND t.date <= ?"
        date_params = [ytd_start, today_str]
    elif _MONTH_RE.match(period):
        date_filter = "t.date LIKE ?"
        date_params = [f"{period}-%"]
    elif _YEAR_RE.match(period):
        date_filter = "t.date LIKE ?"
        date_params = [f"{period}-%"]
    else:
        raise ValueError(
            f"Invalid period {period!r}. "
            "Expected 'month', 'year', 'ytd', an ISO month like '2026-05', "
            "or an ISO year like '2026'."
        )

    sql = f"""
        SELECT
            li.name        AS line_item_name,
            l.name         AS ledger_name,
            li.item_type   AS item_type,
            SUM(te.amount) AS total
        FROM transaction_entries te
        JOIN transactions   t  ON t.id  = te.transaction_id
        JOIN line_items     li ON li.id = te.line_item_id
        JOIN ledgers        l  ON l.id  = li.ledger_id
        WHERE {date_filter}
        GROUP BY te.line_item_id
        ORDER BY total DESC
    """

    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute(sql, date_params).fetchall()
    finally:
        conn.close()

    income: float = 0.0
    expenses: float = 0.0
    by_line_item: list[dict] = []

    for row in rows:
        total = float(row["total"] or 0.0)
        by_line_item.append(
            {
                "line_item": row["line_item_name"],
                "ledger": row["ledger_name"],
                "type": row["item_type"],
                "total": total,
            }
        )
        if row["item_type"] == "income":
            income += total
        else:
            expenses += total

    return {
        "period": period,
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "net": round(income - expenses, 2),
        "by_line_item": by_line_item,
    }


@mcp.tool
def export_excel(years: Optional[List] = None) -> dict:
    """Generate and return an Excel export of transactions."""
    server.paths.ensure_app_dir()
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"friday-bp-{timestamp}.xlsx"
    path = server.paths.EXPORTS_DIR / filename
    conn = get_db(server.paths.DB_PATH)
    try:
        excel_export.export_to_file(conn, path, years if years else None)
    finally:
        conn.close()
    return {"status": "ok", "path": str(path), "size_bytes": path.stat().st_size}


# ---------------------------------------------------------------------------
# Auto-promoted rules audit tools
# ---------------------------------------------------------------------------


@mcp.tool
def list_auto_promoted_rules() -> dict:
    """Return all auto-promoted routing rules with their audit log metadata.

    Each entry includes a ``rule_still_active`` boolean indicating whether the
    underlying ``routing_rule`` still exists in the database.
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute("""
            SELECT apl.id,
                   apl.rule_id,
                   apl.merchant,
                   apl.line_item_id,
                   apl.source_transaction_ids,
                   apl.created_at,
                   CASE WHEN rr.id IS NOT NULL THEN 1 ELSE 0 END AS rule_still_active
              FROM auto_promoted_rules_log apl
              LEFT JOIN routing_rules rr ON rr.id = apl.rule_id
             ORDER BY apl.created_at DESC
            """).fetchall()
        return {
            "rules": [
                {
                    "id": row["id"],
                    "rule_id": row["rule_id"],
                    "merchant": row["merchant"],
                    "line_item_id": row["line_item_id"],
                    "source_transaction_ids": _json.loads(row["source_transaction_ids"]),
                    "created_at": row["created_at"],
                    "rule_still_active": bool(row["rule_still_active"]),
                }
                for row in rows
            ]
        }
    finally:
        conn.close()


@mcp.tool
def undo_auto_promoted_rule(rule_id: str) -> dict:
    """Delete an auto-promoted routing rule and revert affected transaction entries.

    - Deletes the ``routing_rule`` (CASCADE removes the ``auto_promoted_rules_log`` row).
    - Resets ``reviewed = 0`` on every ``transaction_entry`` whose
      ``source = 'rule'`` and whose transaction's merchant matches the rule's
      ``merchant_pattern``.
    - The entire operation is wrapped in a single transaction for atomicity.

    Returns::

        {"ok": True, "rule_deleted": bool, "entries_reverted": int}
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        # Look up the rule before deleting so we know the merchant_pattern.
        rule_row = conn.execute(
            "SELECT id, merchant_pattern FROM routing_rules WHERE id = ?",
            (rule_id,),
        ).fetchone()

        if rule_row is None:
            return {"ok": True, "rule_deleted": False, "entries_reverted": 0}

        merchant_pattern: str = rule_row["merchant_pattern"]

        with db_txn(conn):
            # Revert affected transaction_entries (source='rule', merchant matches).
            cursor = conn.execute(
                """
                UPDATE transaction_entries
                   SET reviewed = 0
                 WHERE source = 'rule'
                   AND transaction_id IN (
                       SELECT id FROM transactions WHERE merchant = ?
                   )
                """,
                (merchant_pattern,),
            )
            entries_reverted: int = cursor.rowcount

            # Delete the routing rule (CASCADE deletes the log row too).
            conn.execute(
                "DELETE FROM routing_rules WHERE id = ?",
                (rule_id,),
            )

        return {"ok": True, "rule_deleted": True, "entries_reverted": entries_reverted}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Configuration tools
# ---------------------------------------------------------------------------


@mcp.tool
def configure_plaid(
    client_id: str,
    secret: str,
    env: str = "production",
) -> dict:
    """Write Plaid credentials to .env and update the running process environment.

    Parameters
    ----------
    client_id : str
        Plaid client ID (non-empty).
    secret : str
        Plaid secret for the target environment (non-empty).
    env : str
        One of ``sandbox``, ``development``, or ``production``.
        Defaults to ``production``.

    The .env file is written atomically (temp file + os.replace) with mode
    0o600.  If .env already exists it is fully replaced, not appended.
    os.environ is updated immediately so the next sync() call picks up the
    new credentials without a daemon restart.

    Returns
    -------
    dict
        ``{"ok": True, "env": <env>}``
    """
    _VALID_ENVS = {"sandbox", "development", "production"}

    if not client_id:
        raise ValueError("client_id must be non-empty")
    if not secret:
        raise ValueError("secret must be non-empty")
    if env not in _VALID_ENVS:
        raise ValueError(f"env must be one of {sorted(_VALID_ENVS)!r}, got {env!r}")

    import time as _time

    # --- Save to DB for the active user (primary, per-user storage) ---
    # Wrapped in a broad try/except so that callers in test environments
    # (where the DB may be uninitialised or have no tables yet) fall through
    # gracefully to the .env write below.  Production runs always have an
    # initialised DB and an active user, so the DB write succeeds there.
    try:
        uid = get_active_user_id(server.paths.DB_PATH)
        if uid:
            db_conn = get_db(server.paths.DB_PATH)
            try:
                now = int(_time.time())
                db_conn.execute(
                    """
                    INSERT INTO plaid_config (user_id, client_id, secret, plaid_env, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        client_id  = excluded.client_id,
                        secret     = excluded.secret,
                        plaid_env  = excluded.plaid_env,
                        updated_at = excluded.updated_at
                    """,
                    (uid, client_id, secret, env, now, now),
                )
                db_conn.commit()
                _logger.info(
                    "configure_plaid: saved credentials to DB for user %s (env=%s)", uid, env
                )
            finally:
                db_conn.close()
    except Exception as _db_exc:  # noqa: BLE001
        _logger.warning(
            "configure_plaid: could not save to DB (DB may be uninitialised) — "
            "credentials will only be written to .env.  Detail: %s",
            _db_exc,
        )

    # --- Also write .env as fallback for initial daemon startup ---
    env_path = project_root / ".env"
    content = f"PLAID_CLIENT_ID={client_id}\nPLAID_SECRET={secret}\nPLAID_ENV={env}\n"

    # Atomic write: write to a sibling temp file, then os.replace into place.
    env_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path_str = tempfile.mkstemp(dir=env_path.parent, prefix=".env.tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(content)
    except Exception:
        try:
            os.unlink(tmp_path_str)
        except OSError:
            pass
        raise

    os.replace(tmp_path_str, env_path)
    os.chmod(env_path, 0o600)

    # Update the running process so the next sync() call picks up new creds
    # (env vars are a fallback; DB credentials take priority at runtime).
    os.environ["PLAID_CLIENT_ID"] = client_id
    os.environ["PLAID_SECRET"] = secret
    os.environ["PLAID_ENV"] = env

    _logger.info("configure_plaid: wrote .env (env=%s)", env)

    return {"ok": True, "env": env}


# ---------------------------------------------------------------------------
# Password MCP tools
# ---------------------------------------------------------------------------


@mcp.tool
def set_ui_password(new_password: str, old_password: Optional[str] = None) -> dict:
    """Change the UI password for the currently active user.

    Parameters
    ----------
    new_password : str
        The new password.  Must be at least 8 characters.
    old_password : str, optional
        The current password.  Required whenever the user already has a
        password set (which is always true after first-run setup).

    Returns
    -------
    dict
        ``{"status": "ok"}`` on success, or
        ``{"status": "error", "message": "..."}`` on failure.
    """
    if len(new_password) < 8:
        return {"status": "error", "message": "Password too short"}

    user_id = get_active_user_id(server.paths.DB_PATH)
    if not user_id:
        return {"status": "error", "message": "Not logged in"}

    user = get_user_by_id(server.paths.DB_PATH, user_id)
    if user is None:
        return {"status": "error", "message": "Not logged in"}

    if old_password is not None:
        if not verify_password(old_password, user["password_hash"]):
            return {"status": "error", "message": "Old password does not match"}
    else:
        # In the multi-profile world, every user always has a password set.
        return {"status": "error", "message": "Old password required"}

    update_user_password(server.paths.DB_PATH, user_id, new_password)
    return {"status": "ok"}


@mcp.tool
def reset_ui_password() -> dict:
    """Generate a password-reset recovery token for the active user.

    Creates a 32-byte hex token, stores it in the shared in-memory recovery
    token store (same store used by the UI POST /forgot handler), writes it
    to ``~/.friday-bp/recovery.txt`` with mode 0600, and returns the reset
    URL.

    Returns
    -------
    dict
        ``{"status": "ok", "recovery_url": "http://127.0.0.1:<port>/reset?t=<token>"}``
        on success, or ``{"status": "error", "message": "..."}`` on failure.
    """
    user_id = get_active_user_id(server.paths.DB_PATH)
    if not user_id:
        return {"status": "error", "message": "Not logged in"}

    token = secrets.token_hex(32)
    add_recovery_token(token, user_id)

    recovery_path = server.paths.APP_DIR / "recovery.txt"
    try:
        server.paths.APP_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(
            str(recovery_path),
            os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
            0o600,
        )
        try:
            os.write(fd, token.encode())
        finally:
            os.close(fd)
        os.chmod(recovery_path, 0o600)
    except Exception:
        pass

    raw = os.environ.get("FRIDAY_BP_UI_PORT")
    try:
        port = int(raw) if raw is not None else 6789
    except ValueError:
        port = 6789

    recovery_url = f"http://127.0.0.1:{port}/reset?t={token}"
    return {"status": "ok", "recovery_url": recovery_url}


# ---------------------------------------------------------------------------
# Classification rules tools
# ---------------------------------------------------------------------------

_VALID_RULE_TYPES = {"transfer", "savings", "spending", "income", "skip"}


@mcp.tool
def list_rules() -> dict:
    """Return all classification rules sorted by priority ascending.

    Returns
    -------
    dict
        ``{"rules": [{id, name, description, rule_type, line_item_id,
        priority, is_default, enabled, created_at}, ...]}``
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute(
            "SELECT id, name, description, rule_type, line_item_id, "
            "priority, is_default, enabled, created_at "
            "FROM classification_rules ORDER BY priority ASC"
        ).fetchall()
        return {
            "rules": [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "description": row["description"],
                    "rule_type": row["rule_type"],
                    "line_item_id": row["line_item_id"],
                    "priority": row["priority"],
                    "is_default": bool(row["is_default"]),
                    "enabled": bool(row["enabled"]),
                    "created_at": row["created_at"],
                }
                for row in rows
            ]
        }
    finally:
        conn.close()


@mcp.tool
def add_rule(
    name: str,
    description: str,
    rule_type: str,
    line_item_id: str = None,
    priority: int = 100,
) -> dict:
    """Create a new classification rule.

    Parameters
    ----------
    name : str
        Short display name for the rule.
    description : str
        Natural language description of what this rule matches and does.
    rule_type : str
        One of ``'transfer'``, ``'savings'``, ``'spending'``, ``'income'``,
        or ``'skip'``.
    line_item_id : str, optional
        Target line item ID (optional).
    priority : int, optional
        Evaluation order — lower numbers run first.  Defaults to 100.

    Returns
    -------
    dict
        ``{"status": "ok", "rule_id": "<uuid>"}``
    """
    if rule_type not in _VALID_RULE_TYPES:
        raise ValueError(
            f"rule_type must be one of {sorted(_VALID_RULE_TYPES)!r}, got {rule_type!r}"
        )
    rule_id = str(uuid.uuid4())
    now = int(_time.time())
    conn = get_db(server.paths.DB_PATH)
    try:
        conn.execute(
            "INSERT INTO classification_rules "
            "(id, name, description, rule_type, line_item_id, priority, is_default, enabled, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, 0, 1, ?)",
            (rule_id, name.strip(), description.strip(), rule_type, line_item_id, priority, now),
        )
        conn.commit()
        return {"status": "ok", "rule_id": rule_id}
    finally:
        conn.close()


@mcp.tool
def update_rule(
    id: str,
    name: str = None,
    description: str = None,
    rule_type: str = None,
    priority: int = None,
    enabled: bool = None,
    line_item_id: str = None,
) -> dict:
    """Update one or more fields on an existing classification rule.

    Only the fields that are explicitly provided are changed.  Any field
    left as ``None`` is untouched.

    Returns
    -------
    dict
        ``{"status": "ok"}`` or ``{"status": "error", "message": "..."}``
    """
    if rule_type is not None and rule_type not in _VALID_RULE_TYPES:
        raise ValueError(
            f"rule_type must be one of {sorted(_VALID_RULE_TYPES)!r}, got {rule_type!r}"
        )
    updates = []
    params = []
    if name is not None:
        updates.append("name = ?")
        params.append(name.strip())
    if description is not None:
        updates.append("description = ?")
        params.append(description.strip())
    if rule_type is not None:
        updates.append("rule_type = ?")
        params.append(rule_type)
    if priority is not None:
        updates.append("priority = ?")
        params.append(priority)
    if enabled is not None:
        updates.append("enabled = ?")
        params.append(1 if enabled else 0)
    if line_item_id is not None:
        updates.append("line_item_id = ?")
        params.append(line_item_id)
    if not updates:
        return {"status": "ok"}  # nothing to do
    params.append(id)
    conn = get_db(server.paths.DB_PATH)
    try:
        cursor = conn.execute(
            f"UPDATE classification_rules SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        conn.commit()
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"Rule not found: {id}"}
        return {"status": "ok"}
    finally:
        conn.close()


@mcp.tool
def reorder_rules(rule_ids: list) -> dict:
    """Assign sequential priorities (10, 20, 30, …) to the supplied rule IDs.

    The first ID in the list gets priority 10, second gets 20, etc.  Any
    rules **not** in the list are left unchanged.

    Returns
    -------
    dict
        ``{"status": "ok"}``
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        with db_txn(conn):
            for i, rule_id in enumerate(rule_ids):
                conn.execute(
                    "UPDATE classification_rules SET priority = ? WHERE id = ?",
                    ((i + 1) * 10, rule_id),
                )
        return {"status": "ok"}
    finally:
        conn.close()


@mcp.tool
def disable_rule(id: str) -> dict:
    """Disable a classification rule so it is skipped during evaluation.

    Returns
    -------
    dict
        ``{"status": "ok"}`` or ``{"status": "error", "message": "..."}``
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        cursor = conn.execute("UPDATE classification_rules SET enabled = 0 WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"Rule not found: {id}"}
        return {"status": "ok"}
    finally:
        conn.close()


@mcp.tool
def enable_rule(id: str) -> dict:
    """Re-enable a previously disabled classification rule.

    Returns
    -------
    dict
        ``{"status": "ok"}`` or ``{"status": "error", "message": "..."}``
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        cursor = conn.execute("UPDATE classification_rules SET enabled = 1 WHERE id = ?", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"Rule not found: {id}"}
        return {"status": "ok"}
    finally:
        conn.close()


@mcp.tool
def delete_rule(id: str) -> dict:
    """Delete a user-created classification rule.

    Default rules (``is_default=1``) cannot be deleted — use
    :func:`disable_rule` to suppress them instead.

    Returns
    -------
    dict
        ``{"status": "ok"}`` or
        ``{"status": "error", "message": "Cannot delete default rule"}``
    """
    conn = get_db(server.paths.DB_PATH)
    try:
        row = conn.execute(
            "SELECT is_default FROM classification_rules WHERE id = ?", (id,)
        ).fetchone()
        if row is None:
            return {"status": "error", "message": f"Rule not found: {id}"}
        if row["is_default"]:
            return {"status": "error", "message": "Cannot delete default rule"}
        conn.execute("DELETE FROM classification_rules WHERE id = ?", (id,))
        conn.commit()
        return {"status": "ok"}
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Settings tools (#159)
# ---------------------------------------------------------------------------

_SETTING_KEYS = {"home_currency", "timezone"}
_SETTING_VALID_VALUES: dict[str, list[str]] = {
    "home_currency": ["CAD", "USD", "EUR", "GBP"],
    # timezone: any non-empty IANA string is valid; we enumerate common ones here
    # but do NOT restrict to this list (open-ended for power users).
    "timezone": [],  # empty = accept any non-empty value (validated in set_setting)
}


_SETTING_DEFAULTS = {
    "home_currency": "CAD",
    "timezone": "America/Toronto",
}


@mcp.tool
def get_setting(key: str) -> dict:
    """Get an app setting for the active user.

    Currently supported keys: 'home_currency', 'timezone'.

    Returns
    -------
    dict
        ``{"status": "ok", "key": key, "value": value}`` on success or
        ``{"status": "error", "message": ...}`` for unsupported keys.
    """
    if key not in _SETTING_KEYS:
        return {
            "status": "error",
            "message": f"Unknown setting key: {key!r}. Supported keys: {sorted(_SETTING_KEYS)!r}",
        }
    uid = get_active_user_id(server.paths.DB_PATH)
    if uid is None:
        return {"status": "error", "message": "No active user found"}
    conn = get_db(server.paths.DB_PATH)
    try:
        row = conn.execute(f"SELECT {key} FROM users WHERE id = ?", (uid,)).fetchone()  # noqa: S608
        value = row[key] if row and row[key] else _SETTING_DEFAULTS.get(key, "")
    finally:
        conn.close()
    return {"status": "ok", "key": key, "value": value}


@mcp.tool
def set_setting(key: str, value: str) -> dict:
    """Set an app setting for the active user.

    Currently supported keys:
    - 'home_currency' (allowed values: CAD, USD, EUR, GBP)
    - 'timezone' (any non-empty IANA timezone string, e.g. 'America/Toronto')

    Returns
    -------
    dict
        ``{"status": "ok", "key": key, "value": value}`` on success or
        ``{"status": "error", "message": ...}`` for unsupported keys/values.
    """
    if key not in _SETTING_KEYS:
        return {
            "status": "error",
            "message": f"Unknown setting key: {key!r}. Supported keys: {sorted(_SETTING_KEYS)!r}",
        }
    # For keys with an explicit allowed list, validate; timezone is open-ended.
    allowed = _SETTING_VALID_VALUES.get(key, [])
    if allowed and value not in allowed:
        return {
            "status": "error",
            "message": f"Invalid value {value!r} for {key!r}. Allowed: {allowed!r}",
        }
    if not value:
        return {
            "status": "error",
            "message": f"Value for {key!r} must not be empty.",
        }
    uid = get_active_user_id(server.paths.DB_PATH)
    if uid is None:
        return {"status": "error", "message": "No active user found"}
    conn = get_db(server.paths.DB_PATH)
    try:
        conn.execute(f"UPDATE users SET {key} = ? WHERE id = ?", (value, uid))  # noqa: S608
        conn.commit()
    finally:
        conn.close()
    return {"status": "ok", "key": key, "value": value}


# ---------------------------------------------------------------------------
# UI URL tool
# ---------------------------------------------------------------------------

_VALID_PAGES = {"accounts", "ledgers", "profile", "dashboard"}


@mcp.tool
def get_ui_url(page: str = None) -> dict:
    """Return the local UI URL, optionally deep-linked to a specific page.

    Parameters
    ----------
    page : str, optional
        One of ``'accounts'``, ``'ledgers'``, ``'profile'``, or
        ``'dashboard'``.  When provided the returned URL includes the page
        path so the user can navigate directly there.  Omit (or pass
        ``None``) to get the base URL.

    Returns
    -------
    dict
        ``{"url": "http://127.0.0.1:<port>[/<page>]"}``
    """
    raw = os.environ.get("FRIDAY_BP_UI_PORT")
    try:
        port = int(raw) if raw is not None else 6789
    except ValueError:
        port = 6789

    base = f"http://127.0.0.1:{port}"

    if page is None:
        return {"url": base}

    if page not in _VALID_PAGES:
        raise ValueError(f"page must be one of {sorted(_VALID_PAGES)!r}, got {page!r}")

    return {"url": f"{base}/{page}"}


# ---------------------------------------------------------------------------
# Natural-language corrections (#173)
# ---------------------------------------------------------------------------


@mcp.tool
def find_transactions(
    merchant: str = None,
    date: str = None,
    amount: float = None,
    account: str = None,
    days_window: int = 7,
) -> dict:
    """Fuzzy search for transactions matching natural-language hints.

    Parameters
    ----------
    merchant : str, optional
        Partial merchant name (case-insensitive substring match).
    date : str, optional
        ISO date ``YYYY-MM-DD`` — transactions within ±``days_window`` days
        of this date are included.
    amount : float, optional
        Absolute transaction amount — transactions within ±$0.50 of this
        value are included.
    account : str, optional
        Partial bank account or institution name (case-insensitive).
    days_window : int, optional
        Number of days either side of ``date`` to search.  Default 7.

    Returns
    -------
    dict
        ``{"transactions": [{id, merchant, date, amount, account_name,
        current_classification, line_item_id, entry_id}, ...]}``
        Up to 10 matches sorted by date descending.
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    if not uid:
        return {"transactions": [], "error": "not_authenticated"}

    conditions: list[str] = [
        "bc.user_id = ?",
        "t.pending = 0",
    ]
    params: list = [uid]

    if merchant is not None:
        conditions.append("LOWER(COALESCE(t.merchant, '')) LIKE LOWER(?)")
        params.append(f"%{merchant}%")

    if date is not None:
        import datetime as _dt

        try:
            pivot = _dt.date.fromisoformat(date)
        except ValueError:
            return {"transactions": [], "error": f"invalid date: {date!r}"}
        lo = (pivot - _dt.timedelta(days=days_window)).isoformat()
        hi = (pivot + _dt.timedelta(days=days_window)).isoformat()
        conditions.append("t.date BETWEEN ? AND ?")
        params.extend([lo, hi])

    if amount is not None:
        conditions.append("ABS(t.amount - ?) <= 0.50")
        params.append(amount)

    if account is not None:
        conditions.append(
            "(LOWER(COALESCE(ba.name, '')) LIKE LOWER(?)"
            " OR LOWER(COALESCE(bc.institution_name, '')) LIKE LOWER(?))"
        )
        params.extend([f"%{account}%", f"%{account}%"])

    where_clause = " AND ".join(conditions)
    sql = f"""
        SELECT
            t.id,
            t.merchant,
            t.date,
            t.amount,
            ba.name        AS account_name,
            te.id          AS entry_id,
            te.line_item_id,
            te.entry_type  AS current_classification
        FROM transactions t
        JOIN bank_accounts ba     ON ba.id = t.bank_account_id
        JOIN bank_connections bc  ON bc.id = ba.connection_id
        LEFT JOIN transaction_entries te ON te.transaction_id = t.id
        WHERE {where_clause}
        ORDER BY t.date DESC
        LIMIT 10
    """

    conn = get_db(server.paths.DB_PATH)
    try:
        rows = conn.execute(sql, params).fetchall()
        return {
            "transactions": [
                {
                    "id": r["id"],
                    "merchant": r["merchant"],
                    "date": r["date"],
                    "amount": r["amount"],
                    "account_name": r["account_name"],
                    "entry_id": r["entry_id"],
                    "line_item_id": r["line_item_id"],
                    "current_classification": r["current_classification"],
                }
                for r in rows
            ]
        }
    finally:
        conn.close()


@mcp.tool
def correct_transaction(
    transaction_id: str,
    line_item_id: str,
    create_rule: bool = False,
    rule_description: str = None,
) -> dict:
    """Reclassify a transaction and optionally create a matching rule.

    Parameters
    ----------
    transaction_id : str
        ID of the transaction to reclassify.
    line_item_id : str
        New line item ID to assign.
    create_rule : bool, optional
        When ``True``, also call :func:`add_rule` so future transactions
        from the same merchant are automatically classified the same way.
    rule_description : str, optional
        Custom description for the new rule.  If omitted an auto-generated
        description based on the merchant name is used.

    Returns
    -------
    dict
        ``{"status": "ok", "transaction_id": ..., "new_line_item_id": ...,
        "rule_created": bool}``
    """
    uid = get_active_user_id(server.paths.DB_PATH)
    if not uid:
        return {"status": "error", "error": "not_authenticated"}

    conn = get_db(server.paths.DB_PATH)
    try:
        # Verify transaction belongs to this user.
        tx_row = conn.execute(
            """
            SELECT t.id, t.merchant
            FROM transactions t
            JOIN bank_accounts ba    ON ba.id = t.bank_account_id
            JOIN bank_connections bc ON bc.id = ba.connection_id
            WHERE t.id = ? AND bc.user_id = ?
            """,
            (transaction_id, uid),
        ).fetchone()
        if not tx_row:
            return {"status": "error", "error": f"transaction {transaction_id!r} not found"}

        merchant = tx_row["merchant"] or "Unknown"
        now = int(_time.time())

        # Check for an existing entry.
        entry_row = conn.execute(
            "SELECT id, line_item_id FROM transaction_entries WHERE transaction_id = ?",
            (transaction_id,),
        ).fetchone()

        if entry_row:
            old_line_item_id = entry_row["line_item_id"]
            conn.execute(
                """
                UPDATE transaction_entries
                SET line_item_id = ?,
                    source = 'manual',
                    reviewed = 1,
                    corrected_from_line_item_id = ?,
                    corrected_at = ?
                WHERE transaction_id = ?
                """,
                (line_item_id, old_line_item_id, now, transaction_id),
            )
        else:
            # No entry yet — insert one.
            conn.execute(
                """
                INSERT INTO transaction_entries
                    (id, transaction_id, line_item_id, amount, source, reviewed, corrected_at)
                SELECT ?, t.id, ?, t.amount, 'manual', 1, ?
                FROM transactions t WHERE t.id = ?
                """,
                (str(uuid.uuid4()), line_item_id, now, transaction_id),
            )

        conn.commit()
    finally:
        conn.close()

    rule_created = False
    if create_rule:
        desc = rule_description or (
            f"Transactions from {merchant!r} should be classified under this line item"
        )
        add_rule(
            name=f"Custom: {merchant}",
            description=desc,
            rule_type="spending",
            line_item_id=line_item_id,
            priority=80,
        )
        rule_created = True

    # -----------------------------------------------------------------------
    # Post-correction rule evaluation (issue #209)
    # Detect conflicting routing_rules and suggest new rules when appropriate.
    # -----------------------------------------------------------------------
    rule_suggestions: list[dict] = []
    conn2 = get_db(server.paths.DB_PATH)
    try:
        # 1. Find routing_rules whose merchant_pattern matches this merchant
        #    but would route to a *different* line_item (i.e. incorrect).
        rr_rows = conn2.execute(
            "SELECT id, merchant_pattern, line_item_id FROM routing_rules"
        ).fetchall()
        conflicting_rules: list[dict] = []
        for rr in rr_rows:
            pattern = (rr["merchant_pattern"] or "").lower()
            if pattern and pattern in merchant.lower():
                if rr["line_item_id"] != line_item_id:
                    conflicting_rules.append(
                        {
                            "rule_id": rr["id"],
                            "merchant_pattern": rr["merchant_pattern"],
                            "current_line_item_id": rr["line_item_id"],
                        }
                    )

        for bad_rule in conflicting_rules:
            rule_suggestions.append(
                {
                    "action": "update_or_disable_rule",
                    "rule_id": bad_rule["rule_id"],
                    "merchant_pattern": bad_rule["merchant_pattern"],
                    "current_line_item_id": bad_rule["current_line_item_id"],
                    "suggested_line_item_id": line_item_id,
                    "reason": (
                        f"Routing rule for pattern {bad_rule['merchant_pattern']!r} would "
                        f"mis-classify future transactions from {merchant!r}. "
                        "Consider updating or disabling it."
                    ),
                }
            )

        # 2. If no conflicting routing_rule exists and merchant appears 2+ times,
        #    suggest creating a new rule tagged [from-correction].
        if not conflicting_rules and not create_rule:
            merchant_count = conn2.execute(
                "SELECT COUNT(*) FROM transactions t "
                "JOIN bank_accounts ba ON ba.id = t.bank_account_id "
                "JOIN bank_connections bc ON bc.id = ba.connection_id "
                "WHERE bc.user_id = ? AND LOWER(t.merchant) = LOWER(?)",
                (uid, merchant),
            ).fetchone()[0]

            if merchant_count >= 2:
                rule_suggestions.append(
                    {
                        "action": "create_rule",
                        "merchant": merchant,
                        "suggested_line_item_id": line_item_id,
                        "occurrence_count": merchant_count,
                        "suggested_description": (
                            f"[from-correction] Transactions from {merchant!r} should be "
                            "classified under this line item"
                        ),
                        "reason": (
                            f"{merchant!r} has appeared {merchant_count} times. "
                            "Creating a rule will auto-classify future transactions."
                        ),
                    }
                )
    finally:
        conn2.close()

    return {
        "status": "ok",
        "transaction_id": transaction_id,
        "new_line_item_id": line_item_id,
        "rule_created": rule_created,
        "rule_suggestions": rule_suggestions,
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
