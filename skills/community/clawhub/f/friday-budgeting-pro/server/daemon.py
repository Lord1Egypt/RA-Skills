"""
server/daemon.py — Friday Budgeting Pro standalone daemon entry point.

Run via:
    python3 -m server.daemon

Lifecycle (in order):
  1. Ensure ~/.friday-bp/ exists with correct permissions (server.paths)
  2. Initialise the SQLite database (server.db)
  3. Load Plaid credentials from the ``plaid_config`` DB table into
     ``os.environ`` so any module-level PlaidProvider() (and other env-reading
     code) picks up the authoritative per-user credentials even if ``.env``
     is absent, stale, or has been deleted.  Falls back gracefully.
  4. Attempt to initialise encryption via Keychain (server.crypto).
     In headless/CI environments the Keychain may not be available.
     Rather than crash here, we log a clear WARNING and continue booting.
     Trade-off: the daemon boots, and the server is reachable for health
     checks and setup flows — but any operation that calls encrypt() or
     decrypt() will still raise at that point (the guard lives inside those
     functions, not here).  This allows #38's refuse-to-start guard to stay
     at the correct boundary (encrypt/decrypt) while letting daemon startup
     succeed in test/CI environments without a real Keychain.
  5. Start the FastAPI UI app on 127.0.0.1:6789 (overridable via FRIDAY_BP_UI_PORT)
     using uvicorn.
  6. Handle SIGTERM/SIGINT for clean shutdown.

Scheduled syncs are managed by OpenClaw cron (registered via apply_initial_setup).
See issue #105.

launchd plist installation is OUT OF SCOPE for this module — it lives in
issue #59 (ClawHub installer).  This module is what #59 will hook into.
"""

from __future__ import annotations

import asyncio
import logging
import os
import signal
import sys
from pathlib import Path

import uvicorn

import server.crypto as _crypto
import server.db as _db
import server.paths as _paths
from ui.server import app  # noqa: F401 — imported so callers can reference it

__all__ = ["main"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

_DEFAULT_HOST = os.environ.get(
    "FRIDAY_BP_UI_HOST", "127.0.0.1"
)  # localhost-only by default; override via FRIDAY_BP_UI_HOST
_DEFAULT_PORT = 6789


def _load_plaid_config_from_db() -> None:
    """Load Plaid credentials from ``plaid_config`` into ``os.environ``.

    Runs after DB init so the plaid_config table is guaranteed to exist.
    DB values take precedence over whatever .env already loaded — the
    per-user row written by configure_plaid() is always authoritative.

    Gracefully no-ops if:
    - The DB doesn't exist yet (first run before init_db).
    - ``plaid_config`` has no rows (credentials not yet configured).
    - Any unexpected exception (logged as WARNING; daemon continues).
    """
    try:
        import sqlite3 as _sqlite3

        if not _paths.DB_PATH.exists():
            log.debug("_load_plaid_config_from_db: DB not found yet — skipping.")
            return

        conn = _sqlite3.connect(str(_paths.DB_PATH))
        conn.row_factory = _sqlite3.Row
        try:
            row = conn.execute(
                "SELECT client_id, secret, plaid_env "
                "FROM plaid_config ORDER BY updated_at DESC LIMIT 1"
            ).fetchone()
        finally:
            conn.close()

        if row is None:
            log.debug("_load_plaid_config_from_db: plaid_config is empty — skipping.")
            return

        os.environ["PLAID_CLIENT_ID"] = row["client_id"]
        os.environ["PLAID_SECRET"] = row["secret"]
        os.environ["PLAID_ENV"] = row["plaid_env"]
        log.info(
            "_load_plaid_config_from_db: Plaid credentials loaded from DB (env=%s).",
            row["plaid_env"],
        )
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "_load_plaid_config_from_db: could not load Plaid config from DB — "
            "falling back to .env / environment variables.  Detail: %s",
            exc,
        )


def _get_port() -> int:
    """Return the UI port, honouring the FRIDAY_BP_UI_PORT env override."""
    raw = os.environ.get("FRIDAY_BP_UI_PORT")
    if raw is not None:
        try:
            return int(raw)
        except ValueError:
            log.warning(
                "FRIDAY_BP_UI_PORT=%r is not a valid integer; using default %d.",
                raw,
                _DEFAULT_PORT,
            )
    return _DEFAULT_PORT


async def _run() -> None:
    """Async main — starts uvicorn server."""
    port = _get_port()

    config = uvicorn.Config(
        app=app,
        host=_DEFAULT_HOST,
        port=port,
        log_level="info",
    )
    server = uvicorn.Server(config)

    loop = asyncio.get_running_loop()

    # --- Shutdown handler ---------------------------------------------------
    shutdown_event = asyncio.Event()

    def _request_shutdown(signum: int, _frame: object) -> None:  # noqa: ANN001
        sig_name = signal.Signals(signum).name
        log.info("Received %s — initiating clean shutdown.", sig_name)
        shutdown_event.set()
        # Ask uvicorn to exit after it finishes in-flight requests.
        server.should_exit = True

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _request_shutdown, sig, None)

    # -----------------------------------------------------------------------

    log.info(
        "Friday Budgeting Pro daemon starting on http://%s:%d",
        _DEFAULT_HOST,
        port,
    )

    await server.serve()

    log.info("Daemon exited cleanly.")


def main() -> None:
    """Entry point called by ``python3 -m server.daemon``."""
    # 0. Load .env from project root (no-op if file doesn't exist).
    #    Imported inline so that test patches on dotenv.load_dotenv are
    #    intercepted correctly (module-level import would bind the name before
    #    the patch is applied).
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).parent.parent / ".env")

    # 1. Filesystem setup
    _paths.ensure_app_dir()
    _paths.audit_permissions()

    # 2. Database initialisation
    _db.init_db(_paths.DB_PATH)

    # 3. Load Plaid credentials from DB into os.environ.  Must run AFTER
    #    init_db (plaid_config table must exist) and AFTER load_dotenv (.env
    #    provides the baseline; DB values override it).  Ensures sync() works
    #    immediately after a daemon restart without calling configure_plaid.
    _load_plaid_config_from_db()

    # 4. Crypto initialisation (graceful fallback for headless/CI environments).
    #    See module docstring for the trade-off rationale.
    try:
        _crypto.init_crypto()
        log.info("Crypto initialised — Keychain is available.")
    except RuntimeError as exc:
        # In a fully deployed production environment this would be a hard
        # error (the user should fix their Keychain and restart).  We log at
        # WARNING so that CI pipelines and headless test runners can boot the
        # daemon without a Keychain configured.  Any attempt to encrypt or
        # decrypt actual tokens will still raise at that boundary (#38).
        log.warning(
            "Keychain not available — crypto is NOT initialised.  "
            "Token encryption/decryption will fail until the Keychain is "
            "configured and the daemon is restarted.  Detail: %s",
            exc,
        )

    # 5-6. Start uvicorn (asyncio loop)
    asyncio.run(_run())


if __name__ == "__main__":
    main()
