"""
ui/server.py — FastAPI application for Friday Budgeting Pro.

Implements all UI routes defined in issue #14.

Auth is handled by ui.auth (PBKDF2 placeholder — argon2id lands in #37).
Templates live in ui/templates/.  Static files in ui/static/.

Design Constraint #6: this module is transport-agnostic (127.0.0.1 binding
is configured in server.daemon via uvicorn.Config, not here).

Route overview
──────────────
  GET  /              redirect hub based on setup/auth state
  GET  /healthz       liveness probe (from #52 — preserved)
  GET  /setup         first-run wizard
  POST /setup/<step>  advance wizard step (final step: complete setup)
  GET  /login         password login form
  POST /login         verify password, create session
  POST /logout        delete session, clear cookie
  GET  /forgot        password recovery placeholder (#60)
  POST /forgot        write recovery token file placeholder (#60)
  GET  /reset         password reset form placeholder (#60)
  POST /reset         password reset action placeholder (#60)
  GET  /profile       settings + linked-accounts placeholder (#47)
  POST /profile       save settings to app_config
  GET  /ledgers       read-only ledger tree
  GET  /link          Plaid Link JS embed
  GET  /static/<path> static file serving
"""

from __future__ import annotations

import os
import secrets
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Load .env before any server imports so Plaid credentials are available
try:
    import pathlib as _pathlib

    from dotenv import load_dotenv as _load_dotenv

    _load_dotenv(_pathlib.Path(__file__).parent.parent / ".env")
except ImportError:
    pass

import server.paths as _paths
from server.db import get_db, init_db
from server.main import list_rules as _list_rules

# ── Recovery token store (in-memory, 10-min TTL) ──────────────────────────
# Shared with the MCP tools (reset_ui_password) via ui.auth so both operate
# on the same in-memory map.  Tokens do not survive daemon restarts.
from ui.auth import (
    SESSION_COOKIE,
    _recovery_tokens,
    add_recovery_token,
    check_session,
    create_session,
    create_user,
    delete_session,
    get_password_hash,
    get_session_user_id,
    get_user_by_id,
    get_user_by_username,
    has_any_user,
    hash_password,
    list_users,
    set_password_hash,
    update_user_password,
    verify_password,
)

# ── App setup ───────────────────────────────────────────────────────────────

# Run DB migrations on startup so schema is always up to date
# (safe to call repeatedly — all operations are idempotent)
init_db(_paths.DB_PATH)

app = FastAPI(title="Friday Budgeting Pro UI", version="0.1.0")

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_STATIC_DIR = Path(__file__).parent / "static"

templates = Jinja2Templates(directory=str(_TEMPLATE_DIR))

app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")


_SETUP_COMPLETE_COOKIE = "friday_bp_setup"

# ── Helpers ─────────────────────────────────────────────────────────────────


def _db_path() -> Path:
    """Return the active DB path (test-overridable via server.paths.DB_PATH)."""
    return _paths.DB_PATH


def _password_is_set() -> bool:
    """Legacy check: True if any user exists (or app_config has a password hash)."""
    return has_any_user(_db_path()) or bool(get_password_hash(_db_path()))


def _is_authenticated(request: Request) -> bool:
    return check_session(request, _db_path())


def _current_user_id(request: Request) -> Optional[str]:
    """Return the user_id from the current session, or None."""
    return get_session_user_id(request, _db_path())


def _check_raw_session(db_path, token: str) -> bool:
    """Validate a raw session token without a Request object."""
    from ui.auth import _SESSION_TTL, _now

    conn = get_db(db_path)
    try:
        row = conn.execute("SELECT expires_at FROM sessions WHERE id = ?", (token,)).fetchone()
        if row is None:
            return False
        now = _now()
        if now > row["expires_at"]:
            conn.execute("DELETE FROM sessions WHERE id = ?", (token,))
            conn.commit()
            return False
        conn.execute(
            "UPDATE sessions SET last_seen_at=?, expires_at=? WHERE id=?",
            (now, now + _SESSION_TTL, token),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def _redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url=url, status_code=302)


_CHANNEL_TO_PREF = {"openclaw_chat": "openclaw", "in_ui": "ui", "macos": "macos"}
_PREF_TO_CHANNEL = {
    "openclaw": "openclaw_chat",
    "ui": "in_ui",
    "macos": "macos",
    "openclaw_chat": "openclaw_chat",
    "in_ui": "in_ui",
}


def _get_username(user_id: Optional[str] = None) -> str:
    """Return the username for *user_id* (or first user if not specified)."""
    conn = get_db(_db_path())
    try:
        if user_id:
            row = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
            if row and row["username"]:
                return row["username"]
        # Fallback: first user or app_config
        row2 = conn.execute("SELECT username FROM users ORDER BY created_at LIMIT 1").fetchone()
        if row2 and row2["username"]:
            return row2["username"]
        try:
            row3 = conn.execute("SELECT username FROM app_config WHERE id=1").fetchone()
            if row3 and row3["username"]:
                return row3["username"]
        except Exception:
            pass
        return "User"
    except Exception:
        return "User"
    finally:
        conn.close()


def _get_notification_channel() -> str:
    conn = get_db(_db_path())
    try:
        try:
            row = conn.execute("SELECT notification_channel FROM app_config WHERE id=1").fetchone()
            if row and row["notification_channel"]:
                return row["notification_channel"]
        except Exception:
            pass
        try:
            row = conn.execute("SELECT notification_pref FROM app_config WHERE id=1").fetchone()
            if row and row["notification_pref"]:
                return _PREF_TO_CHANNEL.get(row["notification_pref"], row["notification_pref"])
        except Exception:
            pass
        return "openclaw_chat"
    finally:
        conn.close()


def _get_notification_pref() -> str:
    return _CHANNEL_TO_PREF.get(_get_notification_channel(), "openclaw")


def _set_notification_channel(channel: str) -> None:
    conn = get_db(_db_path())
    try:
        try:
            conn.execute("ALTER TABLE app_config ADD COLUMN notification_channel TEXT")
            conn.commit()
        except Exception:
            pass
        conn.execute(
            "INSERT INTO app_config (id, notification_channel) VALUES (1,?) "
            "ON CONFLICT(id) DO UPDATE SET notification_channel=excluded.notification_channel",
            (channel,),
        )
        conn.commit()
    finally:
        conn.close()


def _set_notification_pref(pref: str) -> None:
    _set_notification_channel(_PREF_TO_CHANNEL.get(pref, pref))


def _get_ledgers(
    user_id: Optional[str] = None,
    with_drilldown: bool = False,
    period: Optional[str] = "this_month",
) -> list[dict]:
    """Query ledgers + line_items from the DB and return a list of dicts.

    Parameters
    ----------
    user_id :
        When supplied only ledgers owned by this user (plus legacy NULL-user
        rows) are returned.
    with_drilldown :
        When ``True`` each line-item dict includes ``total`` and
        ``transactions`` keys (used by the /ledgers page drilldown UI).
    period :
        Date filter applied to transactions: ``"this_month"``, ``"last_month"``,
        ``"last_3_months"``, ``"this_year"``, ``"all"``, or ``None`` (all time).
    """
    from server.main import _build_ledger_drilldown

    # Normalise: "all" sentinel → None so drilldown skips date filter
    drilldown_period: Optional[str] = None if period == "all" else period

    conn = get_db(_db_path())
    try:
        if user_id:
            # Include rows owned by user_id AND unowned rows (NULL user_id = legacy/migration)
            ledger_rows = conn.execute(
                "SELECT id, name, type, description FROM ledgers "
                "WHERE user_id = ? OR user_id IS NULL ORDER BY name",
                (user_id,),
            ).fetchall()
        else:
            ledger_rows = conn.execute(
                "SELECT id, name, type, description FROM ledgers ORDER BY name"
            ).fetchall()
        ledgers = []
        for lr in ledger_rows:
            if with_drilldown:
                drilldown = _build_ledger_drilldown(conn, lr, period=drilldown_period)
                ledgers.append(
                    {
                        "id": lr["id"],
                        "name": lr["name"],
                        "line_items": drilldown["line_items"],
                        "totals": drilldown["totals"],
                    }
                )
            else:
                items = conn.execute(
                    "SELECT id, name, item_type FROM line_items WHERE ledger_id = ? ORDER BY name",
                    (lr["id"],),
                ).fetchall()
                ledgers.append(
                    {
                        "id": lr["id"],
                        "name": lr["name"],
                        "line_items": [
                            {"id": i["id"], "name": i["name"], "item_type": i["item_type"]}
                            for i in items
                        ],
                    }
                )
        return ledgers
    finally:
        conn.close()


# ── Wizard state helpers ─────────────────────────────────────────────────────
# Setup wizard tracks progress in app_config.setup_step (0 = not started,
# 1–3 = in-progress, 4 = waiting on bank link, 5 = complete).
# We store it inline with the password write so no extra column is needed for
# steps 1–3; we just track completion by whether the password hash is set.

# Wizard session data is stored in a small in-process dict keyed by a
# short-lived wizard token cookie.  Alternatively, steps could round-trip
# form data; here we use a plain dict for simplicity.  This is reset on
# daemon restart, which is fine for a one-time wizard.
_wizard_state: dict[str, dict] = {}


def _get_wizard_token(request: Request) -> Optional[str]:
    return request.cookies.get("friday_bp_wizard")


def _wizard_data(request: Request) -> dict:
    token = _get_wizard_token(request)
    if token and token in _wizard_state:
        return _wizard_state[token]
    return {}


def _update_wizard(response: Response, token: str, data: dict) -> None:
    _wizard_state[token] = data
    response.set_cookie(
        "friday_bp_wizard",
        token,
        httponly=True,
        samesite="strict",
        max_age=3600,
    )


def _clear_wizard(response: Response, token: Optional[str]) -> None:
    if token and token in _wizard_state:
        del _wizard_state[token]
    response.delete_cookie("friday_bp_wizard")


# ── Routes ────────────────────────────────────────────────────────────────────

# ── /healthz ─────────────────────────────────────────────────────────────────


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Liveness probe — returns 200 OK when the daemon is running."""
    return {"status": "ok"}


# ── / ────────────────────────────────────────────────────────────────────────


@app.get("/")
def index(request: Request):
    """Redirect hub.

    - No password set  → /setup
    - Not authenticated → /login
    - Authenticated    → /profile
    """
    if not _password_is_set():
        return _redirect("/setup")
    if not _is_authenticated(request):
        return _redirect("/login")
    return _redirect("/dashboard")


# ── /setup ───────────────────────────────────────────────────────────────────


def _openclaw_home_exists() -> bool:
    return Path(os.path.expanduser("~/.openclaw")).is_dir()


@app.get("/setup", response_class=HTMLResponse)
def setup_get(request: Request):
    if _password_is_set():
        return HTMLResponse(status_code=404, content="Setup already complete.")
    tok = _get_wizard_token(request) or secrets.token_hex(16)
    dch = "openclaw_chat" if _openclaw_home_exists() else "macos"
    resp = templates.TemplateResponse(
        request, "setup.html", {"step": 1, "error": None, "default_channel": dch}
    )
    _update_wizard(resp, tok, {"step": 1, "wizard_active": False})
    return resp


@app.post("/setup/{step}", response_class=HTMLResponse)
async def setup_post(request: Request, step: int):
    tok = _get_wizard_token(request) or secrets.token_hex(16)
    state = _wizard_state.get(tok, {})
    wip = bool(state) and state.get("wizard_active", False)
    if _password_is_set() and not wip:
        return HTMLResponse(status_code=404, content="Setup already complete.")
    form = await request.form()
    if step == 1:
        username = (form.get("username") or "").strip() or "default"
        pw = (form.get("password") or "").strip()
        cf = (form.get("password_confirm") or "").strip()
        dch = "openclaw_chat" if _openclaw_home_exists() else "macos"
        if len(pw) < 8:
            err = "Password must be at least 8 characters."
            resp = templates.TemplateResponse(
                request, "setup.html", {"step": 1, "error": err, "default_channel": dch}
            )
            _update_wizard(resp, tok, {"step": 1, "wizard_active": False, "error": err})
            return resp
        if pw != cf:
            err = "Passwords do not match."
            resp = templates.TemplateResponse(
                request, "setup.html", {"step": 1, "error": err, "default_channel": dch}
            )
            _update_wizard(resp, tok, {"step": 1, "wizard_active": False, "error": err})
            return resp

        # Create user in users table (or update existing default user's password).
        password_hash = hash_password(pw)
        existing_user = get_user_by_username(_db_path(), username)
        if existing_user:
            # Update existing user's password
            from ui.auth import update_user_password

            update_user_password(_db_path(), existing_user["id"], pw)
            new_user_id = existing_user["id"]
        else:
            # Check if there's a default user to update (migration scenario)
            _conn = get_db(_db_path())
            try:
                default_row = _conn.execute(
                    "SELECT id FROM users WHERE id = 'default-user-id'"
                ).fetchone()
            finally:
                _conn.close()
            if default_row:
                # Update the migrated default user
                _conn2 = get_db(_db_path())
                try:
                    _conn2.execute(
                        "UPDATE users SET username = ?, password_hash = ? WHERE id = 'default-user-id'",
                        (username, password_hash),
                    )
                    _conn2.commit()
                finally:
                    _conn2.close()
                new_user_id = "default-user-id"
            else:
                new_user_id = create_user(_db_path(), username, pw)

        # Also save to app_config for legacy compat.
        set_password_hash(_db_path(), password_hash)
        _conn3 = get_db(_db_path())
        try:
            try:
                _conn3.execute("ALTER TABLE app_config ADD COLUMN username TEXT")
            except:
                pass
            _conn3.execute(
                "INSERT INTO app_config (id, username) VALUES (1, ?) "
                "ON CONFLICT(id) DO UPDATE SET username=excluded.username",
                (username,),
            )
            _conn3.commit()
        finally:
            _conn3.close()

        ua = request.headers.get("user-agent")
        stoken = create_session(_db_path(), user_agent=ua, user_id=new_user_id)
        ns = {
            "step": 2,
            "wizard_active": True,
            "session_token": stoken,
            "user_id": new_user_id,
            "error": None,
        }
        resp = templates.TemplateResponse(
            request, "setup.html", {"step": 2, "error": None, "default_channel": dch}
        )
        _update_wizard(resp, tok, ns)
        # Set the real session cookie at step 1 so the user is logged in for the
        # rest of the wizard and lands authenticated on /profile at the end.
        # (Matches the spec in tests/test_setup_wizard.py which asserts
        # friday_bp_session is set after POST /setup/1.)
        resp.set_cookie(SESSION_COOKIE, stoken, httponly=True, samesite="strict")
        return resp
    elif step == 2:
        raw = form.get("notification_channel") or form.get("notification_pref") or "openclaw_chat"
        ch = _PREF_TO_CHANNEL.get(raw, raw)
        _set_notification_channel(ch)
        # Try to generate a Plaid link token for step 3.
        link_token = None
        try:
            import server.main as _sm_link

            result = _sm_link.start_link()
            url = result.get("url", "")
            if "token=" in url:
                link_token = url.split("token=", 1)[1]
        except Exception:
            pass
        ns = {**state, "step": 3, "notification_channel": ch, "error": None}
        resp = templates.TemplateResponse(
            request, "setup.html", {"step": 3, "error": None, "link_token": link_token}
        )
        _update_wizard(resp, tok, ns)
        return resp
    elif step == 3:
        # Final wizard step — bank linked (via Plaid) or skipped.
        # Either way: run apply_initial_setup and go to the dashboard.
        action = (form.get("action") or "").strip()
        if action == "bank_linked":
            public_token = (form.get("public_token") or "").strip()
            if public_token:
                try:
                    import server.main as _sm_cl

                    _sm_cl.complete_link(public_token=public_token)
                except Exception:
                    pass
                # Trigger an initial sync to populate bank_accounts immediately.
                try:
                    import server.main as _sm_sync_setup

                    _sm_sync_setup.sync()
                except Exception:
                    pass
        import server.main as _sm

        _sm.apply_initial_setup(
            banks_to_link=[],
            extra_ledgers=[],
            hints=[],
            rental_properties=[],
            investment_account_ids=[],
        )
        redir = _redirect("/dashboard")
        st = state.get("session_token")
        if st:
            redir.set_cookie(
                _SETUP_COMPLETE_COOKIE, st, httponly=True, samesite="strict", max_age=300
            )
        _clear_wizard(redir, tok)
        return redir
    return HTMLResponse(status_code=404, content="Unknown step.")


def _ensure_ledger(name: str, user_id: Optional[str] = None) -> None:
    """Create a ledger row if one with this name doesn't already exist."""
    import uuid as _uuid

    conn = get_db(_db_path())
    try:
        existing = conn.execute("SELECT id FROM ledgers WHERE name = ?", (name,)).fetchone()
        if existing is None:
            conn.execute(
                "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
                (str(_uuid.uuid4()), name, user_id),
            )
            conn.commit()
    finally:
        conn.close()


# ── /login ───────────────────────────────────────────────────────────────────


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    """Render login form.  If no users exist, redirect to /setup."""
    if not _password_is_set():
        return _redirect("/setup")
    profiles = list_users(_db_path())
    prefill_username = request.query_params.get("username", "")
    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": None, "profiles": profiles, "prefill_username": prefill_username},
    )


@app.post("/login")
async def login_post(request: Request):
    """Verify username+password; on success create session and redirect to /profile.

    Username is optional when there is only one user (backward compat).
    On failure: re-render login.html with an error.
    No rate limiting — single-user local app (per d4403c0).
    """
    if not _password_is_set():
        return _redirect("/setup")

    form = await request.form()
    username = (form.get("username") or "").strip()
    password = form.get("password") or ""

    profiles = list_users(_db_path())

    # If username not supplied, try to resolve it from the single-user case.
    user = None
    if username:
        user = get_user_by_username(_db_path(), username)
    elif len(profiles) == 1:
        # Backward compat: single user, no username required
        user = get_user_by_id(_db_path(), profiles[0]["id"])
    elif len(profiles) == 0:
        # Should never happen (guarded above), but be safe
        return _redirect("/setup")
    # else: multiple users, username required — user stays None → error below

    success = user is not None and verify_password(password, user["password_hash"])

    if not success:
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "error": "Incorrect username or password.",
                "profiles": profiles,
                "prefill_username": username,
            },
            status_code=200,
        )
    # Clear any pending setup session.
    st = request.cookies.get(_SETUP_COMPLETE_COOKIE)
    if st:
        delete_session(_db_path(), st)

    # Create session with user_id.
    ua = request.headers.get("user-agent")
    token = create_session(_db_path(), user_agent=ua, user_id=user["id"])

    response = _redirect("/dashboard")
    response.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="strict")
    response.delete_cookie(_SETUP_COMPLETE_COOKIE)
    return response


# ── /logout ──────────────────────────────────────────────────────────────────


@app.get("/logout")
@app.post("/logout")
def logout(request: Request):
    """Delete session row(s) and clear cookies."""
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        delete_session(_db_path(), token)
    st = request.cookies.get(_SETUP_COMPLETE_COOKIE)
    if st:
        delete_session(_db_path(), st)
    response = _redirect("/login")
    response.delete_cookie(SESSION_COOKIE)
    response.delete_cookie(_SETUP_COMPLETE_COOKIE)
    return response


# ── /forgot ──────────────────────────────────────────────────────────────────


@app.get("/forgot", response_class=HTMLResponse)
def forgot_get(request: Request):
    """Render the forgot-password form (username input)."""
    return templates.TemplateResponse(
        request,
        "forgot.html",
        {"sent": False, "error": None},
    )


@app.post("/forgot", response_class=HTMLResponse)
async def forgot_post(request: Request):
    """Generate a recovery token and write it to ~/.friday-bp/recovery.txt.

    Accepts: username (form field)
    Behaviour:
      - Looks up user by username in the users table
      - Generates a 32-byte random hex token with 10-minute TTL
      - Stores token in the in-memory _recovery_tokens dict
      - Writes token to ~/.friday-bp/recovery.txt with mode 0600
      - Returns the same success page whether or not the username exists
        (prevents username enumeration)
    """
    form = await request.form()
    username = (form.get("username") or "").strip()

    user = get_user_by_username(_db_path(), username) if username else None

    if user:
        token = secrets.token_hex(32)
        add_recovery_token(token, user["id"])

        recovery_path = _paths.APP_DIR / "recovery.txt"
        try:
            _paths.APP_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
            # Write with O_CREAT|O_WRONLY|O_TRUNC so mode is applied atomically
            fd = os.open(
                str(recovery_path),
                os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
                0o600,
            )
            try:
                os.write(fd, token.encode())
            finally:
                os.close(fd)
            # Ensure mode is correct even if the file already existed
            os.chmod(recovery_path, 0o600)
        except Exception:
            pass

    # Always return success page to avoid leaking which usernames exist.
    return templates.TemplateResponse(
        request,
        "forgot.html",
        {"sent": True, "error": None},
    )


# ── /reset ───────────────────────────────────────────────────────────────────


@app.get("/reset", response_class=HTMLResponse)
def reset_get(request: Request):
    """Render the password-reset form (token + new password)."""
    return templates.TemplateResponse(
        request,
        "reset.html",
        {"error": None, "success": False},
    )


@app.post("/reset", response_class=HTMLResponse)
async def reset_post(request: Request):
    """Validate recovery token and update the user's password.

    Accepts: token, new_password (form fields)
    On success:
      - Hashes new_password with argon2id via update_user_password
      - Deletes recovery.txt
      - Invalidates all sessions for that user (forces re-login)
      - Redirects to /login?reset=1
    On failure:
      - Re-renders reset.html with an error message
    """
    form = await request.form()
    token = (form.get("token") or "").strip()
    new_password = form.get("new_password") or ""

    if len(new_password) < 8:
        return templates.TemplateResponse(
            request,
            "reset.html",
            {"error": "Password must be at least 8 characters.", "success": False},
        )

    entry = _recovery_tokens.get(token)
    if entry is None:
        return templates.TemplateResponse(
            request,
            "reset.html",
            {"error": "Invalid or expired recovery token.", "success": False},
        )

    user_id, expiry = entry
    if time.time() > expiry:
        # Clean up the expired token
        _recovery_tokens.pop(token, None)
        return templates.TemplateResponse(
            request,
            "reset.html",
            {"error": "Recovery token has expired. Please request a new one.", "success": False},
        )

    # Update the password
    update_user_password(_db_path(), user_id, new_password)

    # Delete recovery.txt
    recovery_path = _paths.APP_DIR / "recovery.txt"
    try:
        recovery_path.unlink(missing_ok=True)
    except Exception:
        pass

    # Invalidate all sessions for this user (force re-login after reset)
    conn_db = get_db(_db_path())
    try:
        conn_db.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        conn_db.commit()
    finally:
        conn_db.close()

    # Remove token from in-memory store
    _recovery_tokens.pop(token, None)

    # Redirect to login with a success flash
    return _redirect("/login?reset=1")


# ── /dashboard ──────────────────────────────────────────────────────────────


def _get_last_synced_at() -> Optional[str]:
    """Return MAX(last_synced_at) from sync_cursors as a human-readable string,
    or None if the table is empty or the DB has no sync history."""
    import datetime

    conn = get_db(_db_path())
    try:
        row = conn.execute("SELECT MAX(last_synced_at) FROM sync_cursors").fetchone()
        ts = row[0] if row else None
    except Exception:
        ts = None
    finally:
        conn.close()
    if not ts:
        return None
    try:
        return datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)


@app.post("/api/sync")
def api_sync(request: Request):
    """AJAX sync — returns JSON, no redirect."""
    if not _is_authenticated(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    import server.main as _sm

    try:
        result = _sm.sync()
        return JSONResponse(result)
    except Exception as exc:
        import logging

        logging.getLogger(__name__).error("api_sync: %s", exc)
        return JSONResponse({"status": "error", "detail": str(exc)}, status_code=500)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_get(request: Request):
    """Main dashboard page.  Requires authentication."""
    if not _is_authenticated(request):
        return _redirect("/login")
    last_synced = _get_last_synced_at()
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "current_page": "dashboard",
            "last_synced_at": last_synced,
            "action_result": None,
        },
    )


# ── /accounts (#158) ────────────────────────────────────────────────────────


def _get_accounts_grouped(user_id: Optional[str] = None) -> dict:
    """Return bank accounts grouped by institution, with balances.

    Returns a dict of {institution_name: {connection_id: str, accounts: [...]}}.
    """
    conn = get_db(_db_path())
    try:
        if user_id:
            rows = conn.execute(
                "SELECT ba.id, ba.name, ba.mask, ba.type, ba.subtype,"
                "       ba.balance_current, ba.balance_available, ba.description,"
                "       COALESCE(ba.currency, 'CAD') AS currency,"
                "       bc.id AS connection_id, bc.institution_name"
                "  FROM bank_accounts ba"
                "  JOIN bank_connections bc ON bc.id = ba.connection_id"
                " WHERE bc.user_id = ?"
                " ORDER BY bc.institution_name, ba.name",
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT ba.id, ba.name, ba.mask, ba.type, ba.subtype,"
                "       ba.balance_current, ba.balance_available, ba.description,"
                "       COALESCE(ba.currency, 'CAD') AS currency,"
                "       bc.id AS connection_id, bc.institution_name"
                "  FROM bank_accounts ba"
                "  JOIN bank_connections bc ON bc.id = ba.connection_id"
                " ORDER BY bc.institution_name, ba.name"
            ).fetchall()
        grouped: dict = {}
        for r in rows:
            inst = r["institution_name"] or "Unknown Institution"
            if inst not in grouped:
                grouped[inst] = {"connection_id": r["connection_id"], "accounts": []}
            grouped[inst]["accounts"].append(dict(r))
        return grouped
    except Exception:
        return {}
    finally:
        conn.close()


@app.get("/accounts", response_class=HTMLResponse)
def accounts_get(request: Request):
    """Accounts page — bank accounts grouped by institution with balances (#158)."""
    if not _is_authenticated(request):
        return _redirect("/login")
    uid = _current_user_id(request)
    grouped = _get_accounts_grouped(uid)
    return templates.TemplateResponse(
        request,
        "accounts.html",
        {"current_page": "accounts", "grouped_accounts": grouped},
    )


@app.get("/accounts/{account_id}/transactions")
def account_transactions_get(request: Request, account_id: str, limit: int = 50):
    """Return recent transactions for an account with classification info.

    Requires authentication.  Returns JSON:
    {"transactions": [{id, date, merchant, amount, currency, entry_type,
                        source, uncertain, line_item_name, ledger_name}, ...]}
    """
    if not _is_authenticated(request):
        return JSONResponse({"error": "not authenticated"}, status_code=401)
    conn = get_db(_db_path())
    try:
        rows = conn.execute(
            """
            SELECT t.id, t.date, t.authorized_datetime, t.merchant, t.amount,
                   t.pending,
                   COALESCE(t.currency, 'CAD') AS currency,
                   te.entry_type, te.source, te.uncertain,
                   li.name AS line_item_name,
                   l.name  AS ledger_name
              FROM transactions t
              LEFT JOIN transaction_entries te ON te.transaction_id = t.id
              LEFT JOIN line_items li ON li.id = te.line_item_id
              LEFT JOIN ledgers    l  ON l.id  = te.ledger_id
             WHERE t.bank_account_id = ?
             ORDER BY
               t.pending DESC,
               COALESCE(t.authorized_datetime, t.date) DESC,
               t.rowid DESC
             LIMIT ?
            """,
            (account_id, limit),
        ).fetchall()
        return JSONResponse({"transactions": [dict(r) for r in rows]})
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)
    finally:
        conn.close()


@app.patch("/accounts/{account_id}/name")
async def accounts_name_patch(request: Request, account_id: str):
    """Update the display name for a bank account (inline rename).  Requires auth.

    Reads JSON body: {"name": "<new name>"}.
    Returns {"status": "ok", "account_id": ..., "name": ...} or 404.
    """
    if not _is_authenticated(request):
        return JSONResponse({"error": "not authenticated"}, status_code=401)
    body = await request.json()
    name = (body.get("name") or "").strip()
    if not name:
        return JSONResponse({"error": "name is required"}, status_code=400)
    conn = get_db(_db_path())
    try:
        result = conn.execute(
            "UPDATE bank_accounts SET name = ? WHERE id = ?",
            (name, account_id),
        )
        conn.commit()
        if result.rowcount == 0:
            return JSONResponse({"error": f"account {account_id!r} not found"}, status_code=404)
    finally:
        conn.close()
    return JSONResponse({"status": "ok", "account_id": account_id, "name": name})


# ── /settings (#159, #161) ───────────────────────────────────────────────────

_VALID_CURRENCIES = ["CAD", "USD", "EUR", "GBP"]
_VALID_TIMEZONES = [
    "America/Toronto",
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Berlin",
    "Asia/Tokyo",
    "UTC",
]


@app.get("/settings", response_class=HTMLResponse)
def settings_get(request: Request):
    """Settings page.  Requires authentication."""
    if not _is_authenticated(request):
        return _redirect("/login")
    uid = _current_user_id(request)
    conn = get_db(_db_path())
    try:
        row = conn.execute(
            "SELECT home_currency, timezone FROM users WHERE id = ?", (uid,)
        ).fetchone()
        home_currency = row["home_currency"] if row and row["home_currency"] else "CAD"
        timezone = row["timezone"] if row and row["timezone"] else "America/Toronto"
    finally:
        conn.close()
    saved = request.query_params.get("saved") == "1"
    # Load classification rules (gracefully degrade if DB not ready)
    try:
        rules = _list_rules().get("rules", [])
    except Exception:
        rules = []
    return templates.TemplateResponse(
        request,
        "settings.html",
        {
            "current_page": "settings",
            "home_currency": home_currency,
            "currencies": _VALID_CURRENCIES,
            "timezone": timezone,
            "timezones": _VALID_TIMEZONES,
            "saved": saved,
            "rules": rules,
        },
    )


@app.post("/settings", response_class=HTMLResponse)
async def settings_post(request: Request):
    """Save settings.  Requires authentication."""
    if not _is_authenticated(request):
        return _redirect("/login")
    uid = _current_user_id(request)
    form = await request.form()
    home_currency = (form.get("home_currency") or "").strip().upper()
    # timezone is optional in the form: if not submitted keep the existing value
    submitted_tz = (form.get("timezone") or "").strip()

    # Load current values for fallback + error re-render
    conn = get_db(_db_path())
    try:
        row = conn.execute(
            "SELECT home_currency, timezone FROM users WHERE id = ?", (uid,)
        ).fetchone()
        current_currency = row["home_currency"] if row and row["home_currency"] else "CAD"
        current_tz = row["timezone"] if row and row["timezone"] else "America/Toronto"
    finally:
        conn.close()

    # Use submitted timezone if provided, otherwise keep existing value
    timezone = submitted_tz if submitted_tz else current_tz

    # Validate
    errors = []
    if home_currency not in _VALID_CURRENCIES:
        errors.append(f"Invalid currency: {home_currency!r}. Choose one of {_VALID_CURRENCIES}.")
    if not timezone:
        errors.append("Timezone must not be empty.")

    if errors:
        return templates.TemplateResponse(
            request,
            "settings.html",
            {
                "current_page": "settings",
                "home_currency": current_currency,
                "currencies": _VALID_CURRENCIES,
                "timezone": current_tz,
                "timezones": _VALID_TIMEZONES,
                "saved": False,
                "error": " ".join(errors),
            },
        )
    conn = get_db(_db_path())
    try:
        conn.execute(
            "UPDATE users SET home_currency = ?, timezone = ? WHERE id = ?",
            (home_currency, timezone, uid),
        )
        conn.commit()
    finally:
        conn.close()
    return _redirect("/settings?saved=1")


# ── /profile ─────────────────────────────────────────────────────────────────


def _fmt_last_synced(ts) -> str:
    """Convert a Unix timestamp integer to a human-readable string, or 'Never'.

    Kept as a server-side fallback (e.g. for tests / non-JS contexts).
    The UI renders timestamps client-side via data-utc spans instead.
    """
    from datetime import datetime

    if not ts:
        return "Never"
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%b %-d, %Y %-I:%M %p")
    except Exception:
        return "Never"


def _get_connections(user_id: Optional[str] = None) -> list[dict]:
    """Query bank_connections for *user_id* and return a list of dicts."""
    conn = get_db(_db_path())
    try:
        if user_id:
            rows = conn.execute(
                "SELECT id, institution_name, status, last_synced_at "
                "FROM bank_connections WHERE user_id = ? ORDER BY rowid",
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, institution_name, status, last_synced_at "
                "FROM bank_connections ORDER BY rowid"
            ).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            # Keep last_synced_at as raw UTC integer; profile template renders
            # it client-side via .datetime-local[data-utc] JS.  Zero / None → 0.
            raw = d.get("last_synced_at")
            d["last_synced_at"] = int(raw) if raw else 0
            result.append(d)
        return result
    finally:
        conn.close()


def _get_accounts(user_id: Optional[str] = None) -> list[dict]:
    """Query bank_accounts joined with their connection and return list of dicts."""
    conn = get_db(_db_path())
    try:
        if user_id:
            rows = conn.execute(
                "SELECT ba.id, ba.name, ba.mask, ba.type, ba.subtype, ba.description,"
                "       bc.institution_name"
                "  FROM bank_accounts ba"
                "  JOIN bank_connections bc ON bc.id = ba.connection_id"
                " WHERE bc.user_id = ?"
                " ORDER BY bc.institution_name, ba.name",
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT ba.id, ba.name, ba.mask, ba.type, ba.subtype, ba.description,"
                "       bc.institution_name"
                "  FROM bank_accounts ba"
                "  JOIN bank_connections bc ON bc.id = ba.connection_id"
                " ORDER BY bc.institution_name, ba.name"
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []
    finally:
        conn.close()


@app.get("/profile", response_class=HTMLResponse)
def profile_get(request: Request):
    """Settings page.  Requires authentication."""
    if _is_authenticated(request):
        uid = _current_user_id(request)
        pref = _get_notification_pref()
        connections = _get_connections(uid)
        accounts = _get_accounts(uid)
        return templates.TemplateResponse(
            request,
            "profile.html",
            {
                "current_page": "profile",
                "notification_pref": pref,
                "saved": False,
                "connections": connections,
                "accounts": accounts,
                "action_result": None,
            },
        )
    st = request.cookies.get(_SETUP_COMPLETE_COOKIE)
    if st and _check_raw_session(_db_path(), st):
        pref = _get_notification_pref()
        uid = None
        conn_db = get_db(_db_path())
        try:
            row = conn_db.execute("SELECT user_id FROM sessions WHERE id = ?", (st,)).fetchone()
            if row:
                uid = row["user_id"]
        except Exception:
            pass
        finally:
            conn_db.close()
        connections = _get_connections(uid)
        accounts = _get_accounts(uid)
        resp = templates.TemplateResponse(
            request,
            "profile.html",
            {
                "current_page": "profile",
                "notification_pref": pref,
                "saved": False,
                "connections": connections,
                "accounts": accounts,
                "action_result": None,
            },
        )
        resp.set_cookie(SESSION_COOKIE, st, httponly=True, samesite="strict")
        resp.delete_cookie(_SETUP_COMPLETE_COOKIE)
        return resp
    resp2 = _redirect("/login")
    if request.cookies.get(_SETUP_COMPLETE_COOKIE):
        resp2.delete_cookie(_SETUP_COMPLETE_COOKIE)
    return resp2


@app.post("/profile", response_class=HTMLResponse)
async def profile_post(request: Request):
    """Save settings and handle linked-account actions.  Requires authentication.

    Actions (via hidden 'action' field):
      - (none / save_settings): save notification_pref
      - sync_now: trigger server.main.sync()
      - export_now: trigger server.main.export_excel()
      - disconnect_bank: delete bank_connection by bank_id
      - reconnect_bank: call server.main.refresh_connection(id=bank_id)
    """
    if not _is_authenticated(request):
        return _redirect("/login")
    uid = _current_user_id(request)
    form = await request.form()
    action = (form.get("action") or "").strip()
    pref = _get_notification_pref()
    connections = _get_connections(uid)
    accounts = _get_accounts(uid)
    action_result: dict | None = None

    if action == "sync_now":
        import server.main as _sm

        try:
            result = _sm.sync()
            action_result = {"ok": True, "message": "Sync complete.", "detail": result}
        except Exception as exc:
            action_result = {"ok": False, "message": f"Sync failed: {exc}"}

    elif action == "export_now":
        import server.main as _sm

        try:
            result = _sm.export_excel()
            path = result.get("path", "")
            action_result = {"ok": True, "message": f"Export saved to: {path}"}
        except Exception as exc:
            action_result = {"ok": False, "message": f"Export failed: {exc}"}

    elif action == "disconnect_bank":
        bank_id = (form.get("bank_id") or "").strip()
        if not bank_id:
            action_result = {"ok": False, "message": "No bank_id provided."}
        else:
            import server.main as _sm

            try:
                _sm.disconnect(id=bank_id)
                # Redirect to /accounts, or /setup if no connections remain
                remaining = _get_connections(uid)
                if remaining:
                    return _redirect("/accounts")
                else:
                    return _redirect("/setup")
            except Exception as exc:
                action_result = {"ok": False, "message": f"Disconnect failed: {exc}"}

    elif action == "reconnect_bank":
        bank_id = (form.get("bank_id") or "").strip()
        if not bank_id:
            action_result = {"ok": False, "message": "No bank_id provided."}
        else:
            import server.main as _sm

            try:
                result = _sm.refresh_connection(id=bank_id)
                url = result.get("url", "")
                action_result = {"ok": True, "message": f"Reconnect here: {url}", "url": url}
            except Exception as exc:
                action_result = {"ok": False, "message": f"Reconnect failed: {exc}"}

    else:
        # Default: save notification_pref
        pref = form.get("notification_pref") or "openclaw"
        _set_notification_pref(pref)
        return templates.TemplateResponse(
            request,
            "profile.html",
            {
                "current_page": "profile",
                "notification_pref": pref,
                "saved": True,
                "connections": connections,
                "accounts": accounts,
                "action_result": None,
            },
        )

    return templates.TemplateResponse(
        request,
        "profile.html",
        {
            "current_page": "profile",
            "notification_pref": pref,
            "saved": False,
            "connections": connections,
            "accounts": accounts,
            "action_result": action_result,
        },
    )


# ── /profile/accounts/{account_id}/description ──────────────────────────────────────────────────


@app.patch("/profile/accounts/{account_id}/description")
async def account_description_patch(request: Request, account_id: str):
    """Save a user-supplied description for a bank account.

    Requires authentication.  Reads JSON body: {"description": "<text>"}.
    Returns {"status": "ok", "account_id": ...} or 404 if not found.
    """
    from fastapi.responses import JSONResponse

    if not _is_authenticated(request):
        return JSONResponse({"error": "not authenticated"}, status_code=401)

    body = await request.json()
    description = (body.get("description") or "").strip() or None

    conn = get_db(_db_path())
    try:
        result = conn.execute(
            "UPDATE bank_accounts SET description = ? WHERE id = ?",
            (description, account_id),
        )
        conn.commit()
        if result.rowcount == 0:
            return JSONResponse({"error": f"account_id {account_id!r} not found"}, status_code=404)
    finally:
        conn.close()

    return JSONResponse({"status": "ok", "account_id": account_id})


# ── /ledgers ─────────────────────────────────────────────────────────────────


@app.get("/export/excel")
def export_excel_download(request: Request):
    """Stream an Excel export as a browser download."""
    if not _is_authenticated(request):
        return _redirect("/login")

    import datetime

    from fastapi.responses import Response as _Response

    from server.excel_export import export_excel_bytes

    with get_db(_db_path()) as conn:
        data = export_excel_bytes(conn)

    filename = f"friday-budget-{datetime.date.today().strftime('%Y-%m')}.xlsx"
    return _Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


_VALID_PERIODS = {"this_month", "last_month", "last_3_months", "this_year", "all"}


@app.get("/ledgers", response_class=HTMLResponse)
def ledgers_get(request: Request, period: str = "this_month"):
    """Read-only ledger tree with optional date-range filter.  Requires authentication.

    Queries the DB directly because server.main.list_ledgers() is still a
    stub returning {'status': 'not_implemented'}.  A minimal editor is #48.

    Query params
    ------------
    period : str
        One of ``this_month`` (default), ``last_month``, ``last_3_months``,
        ``this_year``, ``all``.
    """
    if not _is_authenticated(request):
        return _redirect("/login")
    # Reject unknown period values and fall back to default
    if period not in _VALID_PERIODS:
        period = "this_month"
    uid = _current_user_id(request)
    ledgers = _get_ledgers(uid, with_drilldown=True, period=period)
    return templates.TemplateResponse(
        request,
        "ledgers.html",
        {"current_page": "ledgers", "ledgers": ledgers, "period": period},
    )


# -- /ledgers CRUD (issue #48) -------------------------------------------------

import uuid as _uuid


@app.post("/ledgers")
async def ledgers_create(request: Request):
    """Create a new ledger. JSON body: {name: str}."""
    if not _is_authenticated(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    uid = _current_user_id(request)
    body = await request.json()
    name = (body.get("name") or "").strip()
    if not name:
        return JSONResponse({"error": "name is required"}, status_code=400)
    ledger_id = str(_uuid.uuid4())
    conn = get_db(_db_path())
    try:
        conn.execute(
            "INSERT INTO ledgers (id, name, user_id) VALUES (?, ?, ?)",
            (ledger_id, name, uid),
        )
        conn.commit()
    finally:
        conn.close()
    return JSONResponse({"id": ledger_id, "name": name}, status_code=201)


@app.delete("/ledgers/{ledger_id}")
def ledgers_delete(request: Request, ledger_id: str):
    """Delete a ledger. Returns 409 if it is the only ledger."""
    if not _is_authenticated(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    conn = get_db(_db_path())
    try:
        count = conn.execute("SELECT COUNT(*) FROM ledgers").fetchone()[0]
        if count <= 1:
            return JSONResponse({"error": "Cannot delete the only ledger"}, status_code=409)
        conn.execute("DELETE FROM line_items WHERE ledger_id = ?", (ledger_id,))
        conn.execute("DELETE FROM ledgers WHERE id = ?", (ledger_id,))
        conn.commit()
    finally:
        conn.close()
    return JSONResponse({"deleted": ledger_id})


@app.patch("/ledgers/{ledger_id}")
async def ledgers_rename(request: Request, ledger_id: str):
    """Rename a ledger. JSON body: {name: str}."""
    if not _is_authenticated(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    body = await request.json()
    name = (body.get("name") or "").strip()
    if not name:
        return JSONResponse({"error": "name is required"}, status_code=400)
    conn = get_db(_db_path())
    try:
        row = conn.execute("SELECT id FROM ledgers WHERE id = ?", (ledger_id,)).fetchone()
        if row is None:
            return JSONResponse({"error": "Ledger not found"}, status_code=404)
        conn.execute("UPDATE ledgers SET name = ? WHERE id = ?", (name, ledger_id))
        conn.commit()
    finally:
        conn.close()
    return JSONResponse({"id": ledger_id, "name": name})


@app.post("/ledgers/{ledger_id}/items")
async def ledger_items_create(request: Request, ledger_id: str):
    """Add a line item. JSON body: {name: str, section: 'income'|'expenses'}."""
    if not _is_authenticated(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    body = await request.json()
    name = (body.get("name") or "").strip()
    section = (body.get("section") or "expenses").strip().lower()
    if not name:
        return JSONResponse({"error": "name is required"}, status_code=400)
    # Map 'expenses' -> 'expense', 'income' -> 'income'
    item_type = "income" if section == "income" else "expense"
    conn = get_db(_db_path())
    try:
        row = conn.execute("SELECT id FROM ledgers WHERE id = ?", (ledger_id,)).fetchone()
        if row is None:
            return JSONResponse({"error": "Ledger not found"}, status_code=404)
        item_id = str(_uuid.uuid4())
        conn.execute(
            "INSERT INTO line_items (id, ledger_id, name, item_type) VALUES (?, ?, ?, ?)",
            (item_id, ledger_id, name, item_type),
        )
        conn.commit()
    finally:
        conn.close()
    return JSONResponse(
        {"id": item_id, "ledger_id": ledger_id, "name": name, "item_type": item_type},
        status_code=201,
    )


@app.patch("/ledgers/{ledger_id}/items/{item_id}")
async def ledger_items_rename(request: Request, ledger_id: str, item_id: str):
    """Rename a line item. JSON body: {name: str}."""
    if not _is_authenticated(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    body = await request.json()
    name = (body.get("name") or "").strip()
    if not name:
        return JSONResponse({"error": "name is required"}, status_code=400)
    conn = get_db(_db_path())
    try:
        row = conn.execute(
            "SELECT id FROM line_items WHERE id = ? AND ledger_id = ?",
            (item_id, ledger_id),
        ).fetchone()
        if row is None:
            return JSONResponse({"error": "Item not found"}, status_code=404)
        conn.execute("UPDATE line_items SET name = ? WHERE id = ?", (name, item_id))
        conn.commit()
    finally:
        conn.close()
    return JSONResponse({"id": item_id, "name": name})


@app.delete("/ledgers/{ledger_id}/items/{item_id}")
def ledger_items_delete(request: Request, ledger_id: str, item_id: str):
    """Delete a line item.  Returns 409 if transaction_entries are attached
    unless ?confirm=true is supplied."""
    if not _is_authenticated(request):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    confirm = request.query_params.get("confirm", "").lower() == "true"
    conn = get_db(_db_path())
    try:
        row = conn.execute(
            "SELECT id FROM line_items WHERE id = ? AND ledger_id = ?",
            (item_id, ledger_id),
        ).fetchone()
        if row is None:
            return JSONResponse({"error": "Item not found"}, status_code=404)
        # Check for attached entries
        entry_count = conn.execute(
            "SELECT COUNT(*) FROM transaction_entries WHERE line_item_id = ?",
            (item_id,),
        ).fetchone()[0]
        if entry_count > 0 and not confirm:
            return JSONResponse(
                {
                    "error": "Item has attached transaction entries",
                    "entry_count": entry_count,
                    "hint": "Add ?confirm=true to force delete",
                },
                status_code=409,
            )
        if entry_count > 0 and confirm:
            conn.execute("DELETE FROM transaction_entries WHERE line_item_id = ?", (item_id,))
        conn.execute("DELETE FROM line_items WHERE id = ?", (item_id,))
        conn.commit()
    finally:
        conn.close()
    return JSONResponse({"deleted": item_id})


# ── /link/start ──────────────────────────────────────────────────────────────


@app.get("/link/start")
def link_start(request: Request, back: Optional[str] = None):
    """Generate a Plaid link token and redirect to /link?token=..."""
    if not _is_authenticated(request):
        return _redirect("/login")
    import server.main as _sm

    result = _sm.start_link()
    # start_link returns {"url": "http://127.0.0.1:6789/link?token=<token>"}
    url = result.get("url", "")
    if not url or "token=" not in url:
        return _redirect("/profile?error=link_token_failed")
    token = url.split("token=", 1)[1]
    back_param = f"&back={back}" if back else ""
    return _redirect(f"/link?token={token}{back_param}")


# ── /link ─────────────────────────────────────────────────────────────────────


@app.get("/link", response_class=HTMLResponse)
def link_get(request: Request, token: Optional[str] = None, back: Optional[str] = None):
    """Plaid Link JS embed.

    Accepts ?token=<link_token> from whoever generates the link token
    (setup wizard, profile page, or an MCP-issued URL).

    Loopback-only binding is enforced by daemon.py; this route just renders
    the embed.
    """
    if not _is_authenticated(request):
        return _redirect("/login")
    back_url = back or "/accounts"
    return templates.TemplateResponse(
        request,
        "link.html",
        {
            "link_token": token,
            "complete_url": "/link/complete",
            "back_url": back_url,
        },
    )


@app.post("/link/complete")
async def link_complete(request: Request):
    """Receive the Plaid public_token after a successful Link flow and exchange it.

    Called by the Plaid Link success callback via a hidden form POST.
    Stores the bank connection, triggers an initial sync to populate
    bank_accounts, then redirects to /accounts.
    """
    if not _is_authenticated(request):
        return _redirect("/login")
    form = await request.form()
    public_token = (form.get("public_token") or "").strip()
    if not public_token:
        return _redirect("/accounts?error=missing_token")
    try:
        import server.main as _sm_cl

        _sm_cl.complete_link(public_token=public_token)
    except Exception as exc:  # noqa: BLE001
        import logging

        logging.getLogger(__name__).error("complete_link failed: %s", exc)
        return _redirect("/accounts?error=link_failed")
    # Trigger an initial sync so bank_accounts gets populated immediately.
    # Errors here are non-fatal — the connection is already stored.
    try:
        import server.main as _sm_sync

        _sm_sync.sync()
    except Exception as exc:  # noqa: BLE001
        import logging

        logging.getLogger(__name__).warning("post-link sync failed: %s", exc)
    return _redirect("/accounts?linked=1")
