"""
server/health_monitor.py — Connection health monitor for Friday Budgeting Pro.

Polls Plaid /item/get for each active bank_connection and updates
bank_connections.status accordingly.  No webhooks — polling only per
ARCHITECTURE.md § Security.

Designed to be called from sync() before iterating connections.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

import server.crypto

if TYPE_CHECKING:
    import sqlite3

logger = logging.getLogger(__name__)

# Plaid error codes that map to specific statuses
_REAUTH_CODES = {"ITEM_LOGIN_REQUIRED", "ITEM_LOCKED"}
_PENDING_EXP_CODES = {"PENDING_EXPIRATION"}


def check_all_connections(db_conn: "sqlite3.Connection", plaid_provider=None) -> dict:
    """Poll Plaid for each active bank_connection and update statuses.

    Parameters
    ----------
    db_conn:
        An open SQLite connection (caller owns open/close).
    plaid_provider:
        A PlaidProvider instance.  When provided it is used directly for all
        connections (e.g. passing the module-level singleton from server.main,
        or a test mock).  When None, per-connection providers are created from
        the ``plaid_config`` DB table (falling back to environment variables)
        so that multi-user deployments use the correct credentials per user.

    Returns
    -------
    dict
        {"checked": N, "active": A, "needs_reauth": R, "pending_expiration": P}
    """
    from server.providers.plaid import PlaidProvider

    # Determine query columns: need user_id and plaid_env only when we must
    # build per-connection providers (plaid_provider is None).
    if plaid_provider is None:
        rows = db_conn.execute(
            "SELECT id, plaid_access_token_encrypted, user_id, plaid_env "
            "FROM bank_connections WHERE status = 'active'"
        ).fetchall()
    else:
        rows = db_conn.execute(
            "SELECT id, plaid_access_token_encrypted "
            "FROM bank_connections WHERE status = 'active'"
        ).fetchall()

    checked = 0
    active_count = 0
    reauth_count = 0
    pending_exp_count = 0
    now = int(time.time())

    for row in rows:
        connection_id = row["id"]
        encrypted_token = row["plaid_access_token_encrypted"]

        try:
            access_token = server.crypto.decrypt(encrypted_token)
        except Exception as exc:
            logger.warning(
                "health_monitor: could not decrypt token for connection %s: %s",
                connection_id,
                exc,
            )
            continue

        # Resolve the provider: use the passed instance when available (test
        # mocks / module singleton), otherwise build one per-connection from
        # per-user DB credentials.
        if plaid_provider is not None:
            conn_provider = plaid_provider
        else:
            conn_user_id = row["user_id"]
            conn_plaid_env = row["plaid_env"] or "sandbox"
            from server.plaid_credentials import get_plaid_credentials

            cred_client_id, cred_secret, _ = get_plaid_credentials(conn_user_id)
            conn_provider = PlaidProvider(
                env=conn_plaid_env,
                client_id=cred_client_id,
                secret=cred_secret,
            )

        try:
            status_info = conn_provider.get_item_status(access_token)
        except Exception as exc:
            logger.warning(
                "health_monitor: Plaid error for connection %s: %s",
                connection_id,
                exc,
            )
            checked += 1
            continue

        error_code = status_info.get("error_code") if isinstance(status_info, dict) else None

        if error_code in _REAUTH_CODES:
            db_conn.execute(
                "UPDATE bank_connections SET status='needs_reauth' WHERE id=?",
                (connection_id,),
            )
            reauth_count += 1
        elif error_code in _PENDING_EXP_CODES:
            db_conn.execute(
                "UPDATE bank_connections SET status='pending_expiration' WHERE id=?",
                (connection_id,),
            )
            pending_exp_count += 1
        elif error_code is None:
            # No error — connection is healthy
            db_conn.execute(
                "UPDATE bank_connections SET status='active', last_synced_at=? WHERE id=?",
                (now, connection_id),
            )
            active_count += 1
        else:
            # Unknown/unexpected error code — log and leave status unchanged
            logger.warning(
                "health_monitor: unhandled Plaid error_code '%s' for connection %s",
                error_code,
                connection_id,
            )

        checked += 1

    db_conn.commit()

    return {
        "checked": checked,
        "active": active_count,
        "needs_reauth": reauth_count,
        "pending_expiration": pending_exp_count,
    }
