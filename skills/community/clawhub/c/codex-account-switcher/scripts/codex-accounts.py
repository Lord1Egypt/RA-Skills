#!/usr/bin/env python3
"""
Manage multiple OpenAI Codex accounts by swapping auth.json.
"""

import json
import os
import sys
import shutil
import base64
import argparse
from pathlib import Path

CODEX_DIR = Path.home() / ".codex"
AUTH_FILE = CODEX_DIR / "auth.json"
ACCOUNTS_DIR = CODEX_DIR / "accounts"
OPENCLAW_AUTH_PROFILES_FILE = (
    Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json"
)
OPENCLAW_AGENTS_DIR = Path.home() / ".openclaw" / "agents"

def ensure_dirs():
    if not ACCOUNTS_DIR.exists():
        ACCOUNTS_DIR.mkdir(parents=True)

def decode_jwt_payload(token):
    try:
        # JWT is header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            return {}
        
        payload = parts[1]
        # Add padding if needed
        payload += '=' * (-len(payload) % 4)
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception:
        return {}


def decode_jwt_segment(segment):
    try:
        segment += '=' * (-len(segment) % 4)
        decoded = base64.urlsafe_b64decode(segment)
        return json.loads(decoded)
    except Exception:
        return {}


def decode_jwt(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return {}

        return {
            "header": decode_jwt_segment(parts[0]),
            "payload": decode_jwt_segment(parts[1]),
        }
    except Exception:
        return {}


def _normalize_str(value) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None


def _get_tokens(data: dict) -> dict:
    tokens = data.get("tokens", {}) if isinstance(data, dict) else {}
    return tokens if isinstance(tokens, dict) else {}


def _read_access_token_auth_claims(data: dict) -> dict:
    access_token = _get_tokens(data).get("access_token")
    if not isinstance(access_token, str) or access_token.count(".") != 2:
        return {}

    payload = decode_jwt_payload(access_token)
    auth = payload.get("https://api.openai.com/auth")
    return auth if isinstance(auth, dict) else {}


def _read_access_token_profile_claims(data: dict) -> dict:
    access_token = _get_tokens(data).get("access_token")
    if not isinstance(access_token, str) or access_token.count(".") != 2:
        return {}

    payload = decode_jwt_payload(access_token)
    profile = payload.get("https://api.openai.com/profile")
    return profile if isinstance(profile, dict) else {}


def _read_codex_account_id(data: dict) -> str | None:
    auth = _read_access_token_auth_claims(data)
    account_id = _normalize_str(auth.get("chatgpt_account_id"))
    if account_id:
        return account_id
    return _normalize_str(data.get("account_id"))


def _read_codex_user_id(data: dict) -> str | None:
    auth = _read_access_token_auth_claims(data)
    return (
        _normalize_str(auth.get("user_id"))
        or _normalize_str(auth.get("chatgpt_user_id"))
        or _normalize_str(auth.get("chatgpt_account_user_id"))
    )


def _suggested_account_name(email: str | None, user_id: str | None) -> str:
    if isinstance(email, str) and "@" in email:
        suggested = email.split("@", 1)[0].strip()
        if suggested:
            return suggested
    if isinstance(user_id, str) and user_id.strip():
        return user_id.strip()
    return "account"


def _describe_identity(info: dict | None) -> str:
    info = info or {}
    user_id = _normalize_str(info.get("user_id"))
    email = _normalize_str(info.get("email"))
    account_id = _normalize_str(info.get("account_id"))

    if user_id and email and email not in ("unknown", "error"):
        return f"{user_id} ({email})"
    if user_id:
        return user_id
    if email and email not in ("unknown", "error"):
        return email
    if account_id:
        return f"account_id {account_id}"
    return "unknown"

def _read_token_exp_seconds(data: dict) -> int | None:
    """Try to extract an expiry timestamp (unix seconds) from known JWT fields.

    Note: access/id tokens are intentionally short-lived (minutes/hours).
    """
    try:
        tokens = data.get('tokens', {}) if isinstance(data, dict) else {}
        if not isinstance(tokens, dict):
            return None

        # Prefer id_token (has email claim), fall back to access_token.
        for key in ("id_token", "access_token"):
            tok = tokens.get(key)
            if isinstance(tok, str) and tok.count('.') == 2:
                payload = decode_jwt_payload(tok)
                exp = payload.get('exp')
                if isinstance(exp, (int, float)) and exp > 0:
                    return int(exp)
        return None
    except Exception:
        return None


def get_account_info(auth_path):
    """Return token-derived identity and diagnostics from an auth.json file."""
    if not auth_path.exists():
        return None

    try:
        with open(auth_path, 'r') as f:
            data = json.load(f)

        exp = _read_token_exp_seconds(data)
        last_refresh = data.get('last_refresh') if isinstance(data, dict) else None
        account_id = _read_codex_account_id(data)
        user_id = _read_codex_user_id(data)

        # Prefer id_token for human-readable identity, then fall back to access token profile claims.
        tokens = _get_tokens(data)
        id_token = tokens.get('id_token')
        email = 'unknown'
        name = None

        if isinstance(id_token, str) and id_token.count('.') == 2:
            payload = decode_jwt_payload(id_token)
            email = payload.get('email', email)
            name = payload.get('name')
        else:
            profile = _read_access_token_profile_claims(data)
            email = profile.get('email', email)

        return {
            'email': email,
            'name': name,
            'account_id': account_id,
            'user_id': user_id,
            'exp': exp,
            'last_refresh': last_refresh,
            'raw': data
        }
    except Exception as e:
        return {'email': 'error', 'error': str(e)}

def is_current(stored_path):
    """Check if the stored file matches the current auth.json."""
    if not AUTH_FILE.exists() or not stored_path.exists():
        return False
    
    # Simple content comparison
    with open(AUTH_FILE, 'rb') as f1, open(stored_path, 'rb') as f2:
        return f1.read() == f2.read()


# --- Account Activity Logging ---
# Tracks which account (user_id) is active at what time, enabling
# accurate attribution of sessions to accounts.

ACTIVITY_LOG = CODEX_DIR / "account-activity.jsonl"


def get_user_id_from_auth(auth_path=None):
    """Extract user_id from an auth.json file's JWT token."""
    if auth_path is None:
        auth_path = AUTH_FILE
    if not auth_path.exists():
        return None
    
    try:
        with open(auth_path, 'r') as f:
            data = json.load(f)

        return _read_codex_user_id(data)
    except Exception:
        return None


def log_account_switch(account_name, user_id=None):
    """Log an account switch to the activity log.
    
    This enables matching sessions to accounts by timestamp.
    """
    import time
    
    if user_id is None:
        user_id = get_user_id_from_auth()
    
    if not user_id:
        return  # Can't log without user_id
    
    entry = {
        "timestamp": int(time.time()),
        "account": account_name,
        "user_id": user_id
    }
    
    try:
        with open(ACTIVITY_LOG, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Non-critical, don't fail the switch


def get_account_for_timestamp(ts):
    """Look up which account was active at a given timestamp.
    
    Returns (account_name, user_id) or (None, None) if unknown.
    """
    if not ACTIVITY_LOG.exists():
        return None, None
    
    try:
        entries = []
        with open(ACTIVITY_LOG, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        
        # Sort by timestamp descending
        entries.sort(key=lambda e: e.get('timestamp', 0), reverse=True)
        
        # Find the first entry with timestamp <= ts
        for entry in entries:
            if entry.get('timestamp', 0) <= ts:
                return entry.get('account'), entry.get('user_id')
        
        # If ts is before all entries, use the earliest entry
        if entries:
            earliest = min(entries, key=lambda e: e.get('timestamp', float('inf')))
            return earliest.get('account'), earliest.get('user_id')
        
        return None, None
    except Exception:
        return None, None

def resolve_active_profile():
    """Return (name, email) for the currently active auth.json if it matches a saved profile."""
    if not AUTH_FILE.exists():
        return None

    for f in _iter_account_snapshot_files():
        if is_current(f):
            info = get_account_info(f) or {}
            return f.stem, info.get("email", "unknown")

    # Active but not saved
    info = get_account_info(AUTH_FILE) or {}
    return None, info.get("email", "unknown")


def _format_expiry(exp_seconds: int | None) -> str:
    """Format access/id token expiry (short-lived). Mostly useful for debugging."""
    if not exp_seconds:
        return ""
    try:
        import time
        now = int(time.time())
        delta = exp_seconds - now
        if delta <= 0:
            return "(token expired)"
        if delta < 60:
            return "(token <1m)"
        mins = delta // 60
        if mins < 120:
            return f"(token {mins}m)"
        hours = mins // 60
        rem_m = mins % 60
        if hours < 48:
            return f"(token {hours}h{rem_m:02d}m)"
        days = hours // 24
        return f"(token {days}d)"
    except Exception:
        return ""


def _format_refreshed(last_refresh: str | None, fallback_path: Path | None = None) -> str:
    """More useful than token exp: when this snapshot was last refreshed."""
    try:
        from datetime import datetime, timezone

        ts: datetime | None = None
        if isinstance(last_refresh, str) and last_refresh.strip():
            raw = last_refresh.strip()
            # Python doesn't like trailing Z with fromisoformat.
            if raw.endswith('Z'):
                raw = raw[:-1] + '+00:00'
            ts = datetime.fromisoformat(raw)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        elif fallback_path is not None and fallback_path.exists():
            ts = datetime.fromtimestamp(fallback_path.stat().st_mtime, tz=timezone.utc)

        if not ts:
            return "refreshed ?"

        now = datetime.now(timezone.utc)
        delta = now - ts
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return "refreshed just now"
        mins = seconds // 60
        if mins < 120:
            return f"refreshed {mins}m ago"
        hours = mins // 60
        rem_m = mins % 60
        if hours < 48:
            return f"refreshed {hours}h{rem_m:02d}m ago"
        days = hours // 24
        return f"refreshed {days}d ago"
    except Exception:
        return "refreshed ?"


def _parse_refresh_dt(last_refresh: str | None, fallback_path: Path | None = None):
    try:
        from datetime import datetime, timezone

        ts: datetime | None = None
        if isinstance(last_refresh, str) and last_refresh.strip():
            raw = last_refresh.strip()
            if raw.endswith('Z'):
                raw = raw[:-1] + '+00:00'
            ts = datetime.fromisoformat(raw)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
        elif fallback_path is not None and fallback_path.exists():
            ts = datetime.fromtimestamp(fallback_path.stat().st_mtime, tz=timezone.utc)
        return ts
    except Exception:
        return None


def cmd_list(verbose: bool = False, json_mode: bool = False):
    ensure_dirs()

    accounts = []
    max_name = 0

    for f in _iter_account_snapshot_files():
        name = f.stem
        max_name = max(max_name, len(name))
        active = is_current(f)
        info = get_account_info(f) or {}
        last_refresh = info.get('last_refresh')
        exp = info.get('exp')
        accounts.append((name, active, last_refresh, exp, f))

    if not accounts:
        if json_mode:
            print(json.dumps({"accounts": [], "active": None}, indent=2))
        else:
            print("(no accounts saved)")
        return

    if json_mode:
        from datetime import datetime, timezone
        import time

        now = datetime.now(timezone.utc)
        now_epoch = int(time.time())
        payload_accounts = []
        active_name = None

        for name, active, last_refresh, exp, path in accounts:
            if active:
                active_name = name
            ts = _parse_refresh_dt(last_refresh, fallback_path=path)
            age_s = int((now - ts).total_seconds()) if ts else None
            ttl_s = int(exp - now_epoch) if isinstance(exp, int) else None
            token_exp_iso = (
                datetime.fromtimestamp(exp, tz=timezone.utc).isoformat().replace('+00:00', 'Z')
                if isinstance(exp, int)
                else None
            )
            payload_accounts.append(
                {
                    "name": name,
                    "active": bool(active),
                    "last_refresh": last_refresh if isinstance(last_refresh, str) else None,
                    "refreshed_age_seconds": age_s,
                    "token_exp": token_exp_iso,
                    "token_ttl_seconds": ttl_s,
                }
            )

        print(
            json.dumps(
                {
                    "generated_at": now.isoformat(),
                    "active": active_name,
                    "accounts": payload_accounts,
                },
                indent=2,
            )
        )
        return

    lines = []
    for name, active, last_refresh, exp, path in accounts:
        display = f"**{name}**" if name else name

        if verbose:
            left = f"- {display.ljust(max_name + 4)}  {_format_refreshed(last_refresh, fallback_path=path)}"
            extra = _format_expiry(exp)
            if extra:
                left += f"  {extra}"
        else:
            left = f"- {display.ljust(max_name + 4)}"

        if active:
            left += "  ✅"
        lines.append(left)

    header = "Codex Accounts"
    underline = "—" * len(header)
    print(header + "\n" + underline + "\n" + "\n".join(lines))

def _resolve_matching_account_by_email(email: str) -> Path | None:
    """Find an existing saved account file whose stored email matches."""
    want = (email or "").strip().lower()
    if not want:
        return None

    matches: list[Path] = []
    for f in _iter_account_snapshot_files():
        info = get_account_info(f) or {}
        got = (info.get("email") or "").strip().lower()
        if got and got == want:
            matches.append(f)

    if not matches:
        return None

    # Prefer filename matching the local-part if present.
    local = want.split("@", 1)[0]
    for f in matches:
        if f.stem.strip().lower() == local:
            return f

    return matches[0]


def _resolve_matching_account_by_user_id(user_id: str) -> Path | None:
    """Find an existing saved account file whose token-derived user_id matches."""
    want = _normalize_str(user_id)
    if not want:
        return None

    matches: list[Path] = []
    for f in _iter_account_snapshot_files():
        info = get_account_info(f) or {}
        got = _normalize_str(info.get("user_id"))
        if got and got == want:
            matches.append(f)

    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    return sorted(matches)[0]


def _resolve_matching_account_by_account_id(account_id: str) -> Path | None:
    """Find a saved account file by accountId only when that match is unique."""
    want = _normalize_str(account_id)
    if not want:
        return None

    matches: list[Path] = []
    for f in _iter_account_snapshot_files():
        info = get_account_info(f) or {}
        got = _normalize_str(info.get("account_id"))
        if got and got == want:
            matches.append(f)

    if len(matches) == 1:
        return matches[0]
    return None


def _resolve_matching_account(account_id: str | None, user_id: str | None, email: str | None) -> Path | None:
    """Find the best matching saved account using token-derived identity first."""
    match = _resolve_matching_account_by_user_id(user_id or "")
    if match is not None:
        return match

    match = _resolve_matching_account_by_email(email or "")
    if match is not None:
        return match

    return _resolve_matching_account_by_account_id(account_id or "")


def _resolve_unique_name_path(base_name: str) -> tuple[str, Path]:
    base = (base_name or "account").strip() or "account"
    target = ACCOUNTS_DIR / f"{base}.json"
    if not target.exists():
        return base, target

    suffix = 2
    while True:
        candidate_name = f"{base}-{suffix}"
        candidate = ACCOUNTS_DIR / f"{candidate_name}.json"
        if not candidate.exists():
            return candidate_name, candidate
        suffix += 1


def _iter_account_snapshot_files():
    for path in sorted(ACCOUNTS_DIR.glob("*.json")):
        if path.name.startswith('.'):
            continue
        if path.name.endswith(".debug.json"):
            continue
        yield path


def cmd_add(name_override: str | None = None, sync_openclaw: bool = False, agent_names: list[str] | None = None):
    """Add accounts by ALWAYS running a fresh login flow.

    Behavior:
    - Always triggers a new browser login.
    - After login, detects token identity from ~/.codex/auth.json.
    - If we already have a saved account with that SAME token identity: update that file.
    - Otherwise: save a new file named from the email local-part, or userId when email is unavailable.

    Interactive (TTY): can repeat.
    Non-interactive (Clawdbot): single-shot.
    """
    ensure_dirs()

    interactive = bool(sys.stdin.isatty() and sys.stdout.isatty())

    while True:
        do_browser_login()

        if not AUTH_FILE.exists():
            print("❌ Login did not produce ~/.codex/auth.json.")
            if not interactive:
                return
            retry = input("Retry login? [Y/n] ").strip().lower()
            if retry == 'n':
                return
            continue

        info = get_account_info(AUTH_FILE) or {}
        email = info.get('email', 'unknown')
        account_id = info.get("account_id")
        user_id = info.get("user_id")
        identity_label = _describe_identity(info)
        current_email = (email or '').strip().lower() if isinstance(email, str) else ''
        print(f"Found active session for: {identity_label}")

        suggested = _suggested_account_name(email, user_id)

        # 1) If we already have this identity stored under ANY name, update that file.
        match = _resolve_matching_account(account_id, user_id, current_email)
        if match is not None:
            # Only overwrite if different.
            if is_current(match):
                print(f"ℹ️  '{match.stem}' already up to date for {identity_label}")
            else:
                print(f"ℹ️  Updating existing account '{match.stem}' ({identity_label})")
                safe_save_token(AUTH_FILE, match, force=False)
            print(f"✅ Saved '{match.stem}' ({identity_label})")
            if sync_openclaw:
                sync_to_openclaw(match.stem, match, agent_names=agent_names)
        else:
            # 2) Otherwise, create a new snapshot with default (or override) name.
            base_name = (name_override or suggested).strip() or suggested
            name, target = _resolve_unique_name_path(base_name)
            safe_save_token(AUTH_FILE, target, force=False)
            print(f"✅ Saved '{name}' ({identity_label})")
            if sync_openclaw:
                sync_to_openclaw(name, target, agent_names=agent_names)

        if not interactive:
            return

        more = input("\nAdd another account? [y/N] ").strip().lower()
        if more != 'y':
            return

def do_browser_login():
    import subprocess
    import time

    print("\n🚀 Starting browser login (codex logout && codex login)...")

    before_mtime = AUTH_FILE.stat().st_mtime if AUTH_FILE.exists() else 0

    subprocess.run(["codex", "logout"], capture_output=True)

    # This typically opens the system browser and completes via localhost callback.
    # Prevent auto-opening the default browser. This avoids instantly re-logging
    # into whatever account is already signed into your primary browser profile.
    # You'll open the printed URL in the browser/profile you want.
    env = dict(os.environ)
    env["BROWSER"] = "/usr/bin/false"

    process = subprocess.Popen(
        ["codex", "login"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env,
    )

    # Stream output (so you can see errors) and watch auth.json for changes.
    start = time.time()
    timeout_s = 15 * 60
    
    while True:
        # Non-blocking-ish read: poll process and attempt readline
        if process.stdout:
            line = process.stdout.readline()
            if line:
                print(line.rstrip())
                # Common device-auth policy message; helpful to surface
                if "device code" in line.lower() and "admin" in line.lower():
                    pass

        if AUTH_FILE.exists():
            mtime = AUTH_FILE.stat().st_mtime
            if mtime > before_mtime:
                # auth.json updated; likely success
                break

        if process.poll() is not None:
            # Process ended; if auth didn't change, it's likely failure
            break

        if time.time() - start > timeout_s:
            process.kill()
            print("\n❌ Login timed out after 15 minutes.")
            return

        time.sleep(0.2)

    process.wait(timeout=5)

    if AUTH_FILE.exists() and AUTH_FILE.stat().st_mtime > before_mtime:
        print("\n✅ Login successful (auth.json updated).")
    else:
        print("\n❌ Login did not update auth.json (may have failed).")


def do_device_login():
    import subprocess
    import re
    
    print("\n🚀 Starting Device Flow Login...")
    
    # 1. Logout first to be safe
    subprocess.run(["codex", "logout"], capture_output=True)
    
    # 2. Start login process
    process = subprocess.Popen(
        ["codex", "login", "--device-auth"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    url = None
    code = None
    
    print("Waiting for code...")
    
    # Read output line by line to find URL and code
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if not line:
            continue
            
        # print(f"DEBUG: {line.strip()}")
        
        # Capture URL
        if "https://auth.openai.com" in line:
            url = line.strip()
            # Remove ANSI color codes
            url = re.sub(r'\x1b\[[0-9;]*m', '', url)
        
        # Capture Code (usually 8 chars like ABCD-1234)
        # Regex for code: 4 chars - 5 chars (actually usually 4-4 or 4-5)
        # The output says: "Enter this one-time code"
        # Then next line has the code
        if "Enter this one-time code" in line:
            # The next line should be the code
            code_line = process.stdout.readline()
            code = code_line.strip()
            code = re.sub(r'\x1b\[[0-9;]*m', '', code)
            
            if url and code:
                print("\n" + "="*50)
                print(f"👉 OPEN THIS: {url}")
                print(f"🔑 ENTER CODE: {code}")
                print("="*50 + "\n")
                print("Waiting for you to complete login in browser...")
                break
    
    # Wait for process to finish (it exits after successful login)
    process.wait()
    
    if process.returncode == 0:
        print("\n✅ Login successful!")
    else:
        print("\n❌ Login failed or timed out.")

def _get_quota_cache_file(name):
    """Get path to quota cache file for an account."""
    return ACCOUNTS_DIR / f".{name}.quota.json"

def _save_quota_cache(name, limits):
    """Save quota to cache file."""
    import time
    cache_file = _get_quota_cache_file(name)
    try:
        with open(cache_file, 'w') as f:
            json.dump({
                'rate_limits': limits,
                'cached_at': time.time()
            }, f)
    except:
        pass

def _load_quota_cache(name, max_age_hours=24):
    """Load quota from cache if fresh enough.

    Supports both legacy formats:
    - { rate_limits: ..., cached_at: <epoch> }
    - { rate_limits: ..., collected_at: <epoch> }

    If neither timestamp exists, we fall back to the file mtime.
    """
    import time
    cache_file = _get_quota_cache_file(name)
    if not cache_file.exists():
        return None
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)

        cached_at = data.get('cached_at') or data.get('collected_at')
        if not isinstance(cached_at, (int, float)):
            cached_at = cache_file.stat().st_mtime

        if time.time() - float(cached_at) < max_age_hours * 3600:
            return data.get('rate_limits')
    except Exception:
        pass
    return None

def _extract_rate_limits_from_session_file(session_file: Path):
    """Extract the last valid rate_limits object from a Codex session file."""
    try:
        with open(session_file, 'r') as f:
            lines = f.readlines()

        for line in reversed(lines):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            payload = event.get('payload', {})
            if payload.get('type') != 'token_count':
                continue

            rate_limits = payload.get('rate_limits')
            primary = rate_limits.get('primary') if isinstance(rate_limits, dict) else None
            secondary = rate_limits.get('secondary') if isinstance(rate_limits, dict) else None
            if primary and secondary:
                return rate_limits
    except Exception:
        pass
    return None


def _find_recent_session_with_rate_limits(after_ts: float | None = None) -> tuple[Path, dict] | tuple[None, None]:
    """Find the newest recent session file containing valid rate limits."""
    from datetime import datetime

    sessions_dir = CODEX_DIR / "sessions"
    now = datetime.now()
    candidates: list[Path] = []

    for day_offset in range(2):
        date = datetime.fromordinal(now.toordinal() - day_offset)
        day_dir = sessions_dir / f"{date.year:04d}" / f"{date.month:02d}" / f"{date.day:02d}"
        if not day_dir.exists():
            continue
        candidates.extend(day_dir.glob("*.jsonl"))

    candidates = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
    for session_file in candidates:
        try:
            if after_ts is not None and session_file.stat().st_mtime < after_ts:
                continue
        except Exception:
            continue

        limits = _extract_rate_limits_from_session_file(session_file)
        if limits:
            return session_file, limits

    return None, None


def _get_quota_for_account(name):
    """Get quota info for an account by switching to it and probing Codex.

    Probe strategy mirrors codex-quota:
    1. Switch ~/.codex/auth.json to the target account.
    2. Run a lightweight `codex exec` probe.
    3. Prefer the exact session file if it contains rate limits.
    4. Otherwise fall back to the most recent session with valid rate limits.
    5. Finally fall back to the cached quota file.
    """
    import subprocess
    import time
    import re
    from datetime import datetime

    source = ACCOUNTS_DIR / f"{name}.json"
    if not source.exists():
        return None

    # Switch to account
    shutil.copy(source, AUTH_FILE)
    user_id = get_user_id_from_auth(source)
    log_account_switch(name, user_id)

    probe_started_at = time.time()

    # Probe codex to get a fresh session (for rate limit info)
    session_id = None
    try:
        result = subprocess.run(
            [
                "codex",
                "exec",
                "--skip-git-repo-check",
                "reply OK",
            ],
            cwd=str(Path.home()),
            capture_output=True,
            text=True,
            timeout=60,
        )
        match = re.search(r'session id:\s+([a-f0-9\-]+)', result.stderr)
        if match:
            session_id = match.group(1)
    except Exception:
        pass

    time.sleep(1)

    if session_id:
        sessions_dir = CODEX_DIR / "sessions"
        now = datetime.now()

        for day_offset in range(2):
            date = datetime.fromordinal(now.toordinal() - day_offset)
            day_dir = sessions_dir / f"{date.year:04d}" / f"{date.month:02d}" / f"{date.day:02d}"

            if not day_dir.exists():
                continue

            for session_file in day_dir.glob(f"*{session_id}.jsonl"):
                limits = _extract_rate_limits_from_session_file(session_file)
                if limits:
                    _save_quota_cache(name, limits)
                    return limits

    # Fallback: recent session with valid rate limits (codex-quota style)
    _, limits = _find_recent_session_with_rate_limits(after_ts=probe_started_at)
    if limits:
        _save_quota_cache(name, limits)
        return limits

    # No fresh rate_limits - try cached data
    cached = _load_quota_cache(name)
    if cached:
        return cached

    return None


def _normalize_rate_limit_bucket(bucket) -> dict | None:
    return bucket if isinstance(bucket, dict) else None


def _quota_summary(limits: dict) -> dict | None:
    if not isinstance(limits, dict):
        return None

    primary = _normalize_rate_limit_bucket(limits.get("primary"))
    secondary = _normalize_rate_limit_bucket(limits.get("secondary"))

    quota_bucket = secondary or primary
    if quota_bucket is None:
        return None

    used_percent = quota_bucket.get("used_percent")
    resets_at = quota_bucket.get("resets_at", 0)
    daily_used = primary.get("used_percent") if primary else None

    if not isinstance(used_percent, (int, float)):
        return None
    if daily_used is not None and not isinstance(daily_used, (int, float)):
        daily_used = None
    if not isinstance(resets_at, (int, float)):
        resets_at = 0

    daily_resets_at = primary.get("resets_at", 0) if primary else 0
    if not isinstance(daily_resets_at, (int, float)):
        daily_resets_at = 0

    return {
        "used_percent": float(used_percent),
        "daily_used": float(daily_used) if daily_used is not None else None,
        "daily_resets_at": int(daily_resets_at),
        "resets_at": int(resets_at),
        "source": "secondary" if secondary else "primary",
    }


def cmd_sync(account_names: list[str] | None = None, agent_names: list[str] | None = None, dry_run: bool = False):
    """Sync saved Codex snapshots into OpenClaw auth profiles."""
    ensure_dirs()
    synced = sync_saved_openclaw_profiles(account_names=account_names, agent_names=agent_names, dry_run=dry_run)
    if dry_run:
        print(f"✅ Dry run complete for {synced} account snapshot(s)")
    else:
        print(f"✅ Synced {synced} account snapshot(s) to OpenClaw")


def cmd_compare(name_a: str, name_b: str, json_mode: bool = False):
    path_a = ACCOUNTS_DIR / f"{name_a}.json"
    path_b = ACCOUNTS_DIR / f"{name_b}.json"

    if not path_a.exists():
        print(f"❌ Account snapshot not found for '{name_a}': {path_a}")
        return
    if not path_b.exists():
        print(f"❌ Account snapshot not found for '{name_b}': {path_b}")
        return

    with open(path_a, "r") as f:
        a = json.load(f)
    with open(path_b, "r") as f:
        b = json.load(f)

    decoded_a = a.get("decoded_tokens") or _build_decoded_token_fields(a)
    decoded_b = b.get("decoded_tokens") or _build_decoded_token_fields(b)

    flat_a = _flatten_json(decoded_a)
    flat_b = _flatten_json(decoded_b)
    all_keys = sorted(set(flat_a) | set(flat_b))

    diffs = []
    for key in all_keys:
        val_a = flat_a.get(key)
        val_b = flat_b.get(key)
        if val_a != val_b:
            diffs.append({
                "field": key,
                name_a: val_a,
                name_b: val_b,
            })

    result = {
        "left": name_a,
        "right": name_b,
        "left_file": str(path_a),
        "right_file": str(path_b),
        "diff_count": len(diffs),
        "diffs": diffs,
    }

    if json_mode:
        print(json.dumps(result, indent=2))
        return

    print(f"Comparing {name_a} vs {name_b}")
    print(f"Left:  {path_a}")
    print(f"Right: {path_b}")
    print(f"Differences: {len(diffs)}")
    if not diffs:
        return

    for diff in diffs:
        print(f"\n{diff['field']}")
        print(f"  {name_a}: {json.dumps(diff[name_a], ensure_ascii=False)}")
        print(f"  {name_b}: {json.dumps(diff[name_b], ensure_ascii=False)}")

def cmd_auto(json_mode=False, sync_openclaw: bool = False, agent_names: list[str] | None = None):
    """Switch to the account with the most quota available."""
    import time
    ensure_dirs()
    
    accounts = [f.stem for f in _iter_account_snapshot_files()]
    if not accounts:
        if json_mode:
            print('{"error": "No accounts found"}')
        else:
            print("❌ No accounts found")
        return
    
    # Save current account to restore if needed
    original_account = None
    if AUTH_FILE.exists():
        for acct_file in _iter_account_snapshot_files():
            if acct_file.read_bytes() == AUTH_FILE.read_bytes():
                original_account = acct_file.stem
                break
    
    if not json_mode:
        print(f"🔄 Checking quota for {len(accounts)} account(s)...\n")
    
    now = int(time.time())
    results = {}
    for name in accounts:
        if not json_mode:
            print(f"  → {name}...", end=" ", flush=True)
        
        limits = _get_quota_for_account(name)
        quota = _quota_summary(limits)
        
        if quota:
            weekly_pct = quota['used_percent']
            daily_pct = quota['daily_used']
            weekly_resets_at = quota['resets_at']
            
            # If quota has already reset, treat as 0% used
            effective_weekly_pct = 0 if now >= weekly_resets_at else weekly_pct
            
            daily_resets_at = quota.get('daily_resets_at', 0)
            effective_daily_pct = 0 if (daily_resets_at and now >= daily_resets_at) else (daily_pct or 0)

            results[name] = {
                'weekly_used': weekly_pct,
                'weekly_resets_at': weekly_resets_at,
                'effective_weekly_used': effective_weekly_pct,
                'daily_used': daily_pct,
                'daily_resets_at': daily_resets_at,
                'effective_daily_used': effective_daily_pct,
                'available': 100 - effective_weekly_pct,
                'quota_source': quota['source'],
            }
            if not json_mode:
                if effective_weekly_pct < weekly_pct:
                    print(f"weekly {weekly_pct:.0f}% used → RESET (now 0%)")
                else:
                    print(f"weekly {weekly_pct:.0f}% used")
        else:
            results[name] = {'error': 'could not get quota'}
            if not json_mode:
                print("❌ failed")
    
    # Find best account (lowest effective weekly usage, accounting for resets)
    valid = {k: v for k, v in results.items() if 'available' in v}
    
    if not valid:
        if original_account:
            shutil.copy(ACCOUNTS_DIR / f"{original_account}.json", AUTH_FILE)
        if json_mode:
            print(json.dumps({"error": "No valid quota data", "results": results}))
        else:
            print("\n❌ Could not get quota for any account")
        return
    
    # Sort by: 1) lowest effective usage, 2) earliest reset time (if both at 100%)
    def sort_key(k):
        """Budget-based scoring: prefer accounts under their ideal usage pace.

        Weekly budget: if you spread 100% evenly over 7 days, at any point
        you know where you *should* be: budget = (elapsed / 168h) * 100%.
        Score = actual% - budget%. Negative = under budget (good).

        5h penalty: if the 5h window is nearly maxed, the account is about
        to get blocked regardless of weekly headroom.
        """
        v = valid[k]
        weekly = v['effective_weekly_used']
        daily = v.get('effective_daily_used', 0)
        weekly_resets = v.get('weekly_resets_at', 0)
        daily_resets = v.get('daily_resets_at', 0)

        # Hard block: either window at 100% means the account is unusable
        if weekly >= 100:
            weekly_penalty = 500  # completely blocked on weekly
        else:
            weekly_penalty = 0

        # Weekly budget score (only meaningful if not blocked)
        weekly_window = 168 * 3600  # 7 days in seconds
        weekly_elapsed = weekly_window - max(0, weekly_resets - now)
        weekly_budget = (weekly_elapsed / weekly_window) * 100 if weekly_window > 0 else 0
        weekly_score = weekly - weekly_budget  # negative = under budget

        # 5h penalty: if daily is almost maxed, heavily penalize
        if daily >= 100:
            daily_penalty = 200   # blocked right now
        elif daily >= 90:
            daily_penalty = 50    # about to be blocked
        elif daily >= 75:
            daily_penalty = 10    # getting warm
        else:
            daily_penalty = 0     # fine

        return weekly_penalty + weekly_score + daily_penalty
    
    # Compute and attach scores for transparency
    for k in valid:
        valid[k]['_score'] = sort_key(k)

    best = min(valid.keys(), key=sort_key)
    
    # Check if already on best account
    already_active = (original_account == best)
    
    # Always restore auth.json to the best account.
    # Probing switches auth.json to each account in turn, so after
    # probing it points at the LAST probed account, not the best one.
    shutil.copy(ACCOUNTS_DIR / f"{best}.json", AUTH_FILE)
    if not already_active:
        log_account_switch(best, get_user_id_from_auth(ACCOUNTS_DIR / f"{best}.json"))

    if sync_openclaw:
        sync_saved_openclaw_profiles(account_names=[best], agent_names=agent_names)
    
    if json_mode:
        print(json.dumps({
            "switched_to": best,
            "already_active": already_active,
            "weekly_used": valid[best]['weekly_used'],
            "effective_weekly_used": valid[best]['effective_weekly_used'],
            "weekly_resets_at": valid[best].get('weekly_resets_at'),
            "available": valid[best]['available'],
            "all_accounts": results
        }, indent=2))
    else:
        from datetime import datetime
        if already_active:
            print(f"\n✅ Already on best account: {best}")
        else:
            print(f"\n✅ Switched to: {best}")
        
        # Show table sorted by score (best first)
        sorted_accounts = sorted(
            results.items(),
            key=lambda x: x[1].get('_score', 999) if '_score' in x[1] else 999
        )
        
        # Header
        print(f"\n{'Account':<12} {'7d':>5} {'5h':>5} {'Score':>7} {'7d Resets':>14} {'5h Resets':>14}")
        print(f"{'─' * 12} {'─' * 5} {'─' * 5} {'─' * 7} {'─' * 14} {'─' * 14}")
        
        for name, data in sorted_accounts:
            if 'error' in data:
                print(f"{name:<12} {'err':>5} {'':>5} {'':>7} {data['error']}")
                continue
            
            marker = " ←" if name == best else ""
            weekly = data.get('effective_weekly_used', data.get('weekly_used', 0))
            daily = data.get('effective_daily_used', data.get('daily_used', 0))
            score = data.get('_score', 0)
            resets_at = data.get('weekly_resets_at', 0)
            
            # Format weekly with reset indicator
            if data.get('effective_weekly_used', 999) < data.get('weekly_used', 0):
                weekly_str = "RST"
            elif weekly >= 100:
                weekly_str = "MAX"
            else:
                weekly_str = f"{weekly:.0f}%"
            
            # Format daily
            if daily >= 100:
                daily_str = "MAX"
            else:
                daily_str = f"{daily:.0f}%"
            
            # Format reset times
            reset_str = datetime.fromtimestamp(resets_at).strftime("%b %d %H:%M") if resets_at else "?"
            daily_resets = data.get('daily_resets_at', 0)
            if daily_resets and daily_resets > now:
                delta_s = int(daily_resets - now)
                h, m = delta_s // 3600, (delta_s % 3600) // 60
                daily_reset_str = f"in {h}h {m:02d}m"
            elif daily_resets:
                daily_reset_str = "reset"
            else:
                daily_reset_str = "?"
            
            print(f"{name:<12} {weekly_str:>5} {daily_str:>5} {score:>+7.1f} {reset_str:>14} {daily_reset_str:>14}{marker}")

def cmd_use(name, sync_openclaw: bool = False, agent_names: list[str] | None = None):
    ensure_dirs()
    source = ACCOUNTS_DIR / f"{name}.json"
    
    if not source.exists():
        print(f"❌ Account '{name}' not found.")
        print("Available accounts:")
        for f in _iter_account_snapshot_files():
            print(f" - {f.stem}")
        return
    
    # Backup current if it's not saved? 
    # Maybe risky to overwrite silently, but that's what a switcher does.
    
    shutil.copy2(source, AUTH_FILE)
    log_account_switch(name, get_user_id_from_auth(source))
    info = get_account_info(source)
    print(f"✅ Switched to account: {name} ({_describe_identity(info)})")

    if sync_openclaw:
        sync_saved_openclaw_profiles(account_names=[name], agent_names=agent_names)

def _extract_openclaw_token_payload(source_path):
    """Extract token fields from a Codex snapshot for OpenClaw sync."""
    with open(source_path, "r") as f:
        data = json.load(f)

    tokens = _get_tokens(data)
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    id_token = tokens.get("id_token")
    account_id = _read_codex_account_id(data) or ""

    if not access_token or not refresh_token:
        return None

    # Prefer access_token expiry (long-lived, used for API calls) over
    # id_token expiry (short-lived, only for identity).
    expires = 0
    for token_key in ("access_token", "id_token"):
        tok = tokens.get(token_key)
        if tok and "." in tok:
            try:
                seg = tok.split(".")[1]
                seg += '=' * (-len(seg) % 4)
                decoded = json.loads(base64.urlsafe_b64decode(seg))
                exp = int(decoded.get("exp", 0))
                if exp > 0:
                    candidate = exp * 1000
                    if candidate > expires:
                        expires = candidate
            except Exception:
                pass

    # Extract email from token for profile key
    email = None
    for token_key in ("id_token", "access_token"):
        tok = tokens.get(token_key)
        if tok and "." in tok:
            try:
                seg = tok.split(".")[1]
                seg += '=' * (-len(seg) % 4)
                decoded = json.loads(base64.urlsafe_b64decode(seg))
                profile = decoded.get("https://api.openai.com/profile", {})
                email = profile.get("email") or decoded.get("email")
                if email:
                    break
            except Exception:
                pass

    return {
        "access": access_token,
        "refresh": refresh_token,
        "expires": expires,
        "accountId": account_id,
        "email": email,
    }


def _selected_agent_dirs(agent_names: list[str] | None = None) -> list[Path]:
    if not OPENCLAW_AGENTS_DIR.is_dir():
        return []

    wanted = {name.strip() for name in (agent_names or []) if name and name.strip()}
    selected = []
    for agent_dir in sorted(OPENCLAW_AGENTS_DIR.iterdir()):
        if not agent_dir.is_dir():
            continue
        if wanted and agent_dir.name not in wanted:
            continue
        selected.append(agent_dir)
    return selected


def _sync_to_agent_auth_json(token_payload, quiet: bool = False, agent_names: list[str] | None = None, dry_run: bool = False):
    """Sync the active Codex token into selected OpenClaw agents' auth.json.

    Each agent has ~/.openclaw/agents/<id>/agent/auth.json with a top-level
    'openai-codex' key containing {type, access, refresh, expires}.
    """
    agent_dirs = _selected_agent_dirs(agent_names)
    if not agent_dirs:
        return []

    updated = []
    for agent_dir in agent_dirs:
        auth_file = agent_dir / "agent" / "auth.json"
        if not auth_file.exists():
            continue

        try:
            with open(auth_file, "r") as f:
                agent_data = json.load(f)

            if not isinstance(agent_data, dict):
                continue

            # Only update if there's already an openai-codex entry (don't inject into agents that don't use it)
            if "openai-codex" not in agent_data:
                continue

            agent_data["openai-codex"] = {
                "type": "oauth",
                "access": token_payload["access"],
                "refresh": token_payload["refresh"],
                "expires": token_payload["expires"],
            }

            if not dry_run:
                with open(auth_file, "w") as f:
                    json.dump(agent_data, f, indent=2)
                    f.write("\n")

            updated.append(agent_dir.name)
        except Exception:
            continue

    if updated and not quiet:
        prefix = "Would update" if dry_run else "Updated"
        print(f"✅ {prefix} auth.json for agent(s): {', '.join(updated)}", file=sys.stderr)

    return updated


def sync_to_openclaw(name, source_path, quiet: bool = False, agent_names: list[str] | None = None, dry_run: bool = False):
    try:
        token_payload = _extract_openclaw_token_payload(source_path)
        if not token_payload:
            return False

        # 1. Update auth-profiles.json for selected agents
        profile_paths = []
        for agent_dir in _selected_agent_dirs(agent_names):
            ap = agent_dir / "agent" / "auth-profiles.json"
            if ap.exists():
                profile_paths.append(ap)

        # Fallback to just main if nothing found and no filter was requested
        if not profile_paths and not agent_names:
            profile_paths = [OPENCLAW_AUTH_PROFILES_FILE]

        updated_agents = []
        email = token_payload.get("email") or name
        profile_id = f"openai-codex:{email}"

        for oc_path in profile_paths:
            try:
                with open(oc_path, "r") as f:
                    oc_data = json.load(f)

                if "profiles" not in oc_data:
                    oc_data["profiles"] = {}

                # Remove old name-based key if it exists (migration)
                old_key = f"openai-codex:{name}"
                if old_key in oc_data["profiles"] and old_key != profile_id:
                    del oc_data["profiles"][old_key]

                oc_data["profiles"][profile_id] = {
                    "type": "oauth",
                    "provider": "openai-codex",
                    "access": token_payload["access"],
                    "refresh": token_payload["refresh"],
                    "expires": token_payload["expires"],
                    "accountId": token_payload.get("accountId", ""),
                    "email": email,
                }

                if not dry_run:
                    with open(oc_path, "w") as f:
                        json.dump(oc_data, f, indent=2)

                updated_agents.append(oc_path.parent.parent.name)
            except Exception:
                continue

        if not quiet and updated_agents:
            prefix = "Would sync" if dry_run else "Synced"
            print(f"\u2705 {prefix} {name} token to OpenClaw auth-profiles.json ({', '.join(updated_agents)})", file=sys.stderr)

        # 2. Update every selected agent's auth.json that has an openai-codex entry
        _sync_to_agent_auth_json(token_payload, quiet=quiet, agent_names=agent_names, dry_run=dry_run)
        return True

    except Exception as e:
        if not quiet:
            print(f"⚠️ Failed to sync to OpenClaw: {e}", file=sys.stderr)

    return False


def sync_saved_openclaw_profiles(account_names: list[str] | None = None, agent_names: list[str] | None = None, dry_run: bool = False) -> int:
    """Ensure selected saved Codex snapshots are mirrored to OpenClaw profiles."""
    synced = 0
    wanted_accounts = set(account_names or [])
    try:
        for account_file in _iter_account_snapshot_files():
            if wanted_accounts and account_file.stem not in wanted_accounts:
                continue
            if sync_to_openclaw(account_file.stem, account_file, quiet=True, agent_names=agent_names, dry_run=dry_run):
                synced += 1
    except Exception:
        return synced
    return synced

def get_token_email(auth_path) -> str:
    """Extract email from a token file."""
    info = get_account_info(auth_path) or {}
    return (info.get("email") or "").strip().lower()


def _build_decoded_token_fields(data: dict) -> dict:
    tokens = _get_tokens(data)
    decoded = {}
    for key in ("id_token", "access_token", "refresh_token"):
        token = tokens.get(key)
        if isinstance(token, str) and token.count(".") == 2:
            decoded[key] = decode_jwt(token)
    return decoded


def _annotate_snapshot_file(path: Path) -> None:
    try:
        with open(path, "r") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return

        data["decoded_tokens"] = _build_decoded_token_fields(data)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
    except Exception:
        return


def _flatten_json(value, prefix="") -> dict[str, object]:
    items: dict[str, object] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            items.update(_flatten_json(value[key], child_prefix))
        return items
    if isinstance(value, list):
        if not value:
            items[prefix] = []
            return items
        for idx, item in enumerate(value):
            child_prefix = f"{prefix}[{idx}]"
            items.update(_flatten_json(item, child_prefix))
        return items
    items[prefix] = value
    return items


def safe_save_token(source_path: Path, target_path: Path, force: bool = False) -> tuple[bool, str]:
    """Safely save a token file, preventing overwrites with different token identities.
    
    Returns (success, message).
    """
    if not source_path.exists():
        return False, "Source token file does not exist"
    
    source_info = get_account_info(source_path) or {}
    source_email = (source_info.get("email") or "").strip().lower()
    source_account_id = _normalize_str(source_info.get("account_id"))
    source_user_id = _normalize_str(source_info.get("user_id"))

    if not source_user_id and not source_account_id and (not source_email or source_email in ("unknown", "error")):
        return False, "Could not determine identity from source token"
    
    # If target exists, verify token identities match.
    if target_path.exists():
        target_info = get_account_info(target_path) or {}
        target_email = (target_info.get("email") or "").strip().lower()
        target_account_id = _normalize_str(target_info.get("account_id"))
        target_user_id = _normalize_str(target_info.get("user_id"))

        mismatch = None
        if source_user_id and target_user_id and source_user_id != target_user_id:
            mismatch = f"target has user_id {target_user_id}, source has {source_user_id}"
        elif source_email and target_email and target_email not in ("unknown", "error") and source_email != target_email:
            mismatch = f"target has {target_email}, source has {source_email}"
        elif source_account_id and target_account_id and source_account_id != target_account_id:
            mismatch = f"target has account_id {target_account_id}, source has {source_account_id}"

        if mismatch:
            if not force:
                return False, f"Refusing to overwrite: {mismatch}"
            # Force mode: warn but proceed
            print(f"⚠️  Warning: overwriting despite identity mismatch ({mismatch}) (--force)")
    
    shutil.copy2(source_path, target_path)
    _annotate_snapshot_file(target_path)
    if source_user_id:
        return True, f"Saved token for user_id {source_user_id}"
    if source_email and source_email not in ("unknown", "error"):
        return True, f"Saved token for {source_email}"
    return True, f"Saved token for account_id {source_account_id}"


def cmd_save(name: str, force: bool = False, sync_openclaw: bool = False, agent_names: list[str] | None = None):
    """Save the current auth.json to a named account, with safety check."""
    ensure_dirs()
    
    if not AUTH_FILE.exists():
        print("❌ No current auth.json to save")
        return
    
    target = ACCOUNTS_DIR / f"{name}.json"
    success, message = safe_save_token(AUTH_FILE, target, force=force)
    
    if success:
        print(f"✅ {message} as '{name}'")
        if sync_openclaw:
            sync_to_openclaw(name, target, agent_names=agent_names)
    else:
        print(f"❌ {message}")


def sync_current_login_to_snapshot() -> None:
    """Persist the CURRENT ~/.codex/auth.json back into the matching named snapshot.

    This makes snapshots behave like "last known good refreshed token state".

    Rules:
    - If the current login's token identity matches an existing snapshot (any name), update that file.
    - If it doesn't match any snapshot, create a new snapshot using the email local-part, or userId if email is unavailable.
    - NEVER overwrite a snapshot with a different user's token (safety check).

    This runs silently (no prints) because it's executed on every invocation.
    """
    try:
        ensure_dirs()
        if not AUTH_FILE.exists():
            return

        info = get_account_info(AUTH_FILE) or {}
        account_id = info.get("account_id")
        user_id = info.get("user_id")
        email = (info.get("email") or "").strip().lower()
        if not user_id and (not email or email in ("unknown", "error")) and not account_id:
            return

        match = _resolve_matching_account(account_id, user_id, email)
        if match is not None:
            if not is_current(match):
                # Safety check: verify token identities match before overwriting
                safe_save_token(AUTH_FILE, match, force=False)
                # Silently ignore failures (e.g., identity mismatch)
            return

        # No match: create a new snapshot using email local-part or userId
        suggested = _suggested_account_name(email, user_id)
        name, target = _resolve_unique_name_path(suggested)
        safe_save_token(AUTH_FILE, target, force=False)
    except Exception:
        # Never fail the command because of sync.
        return


def main():
    parser = argparse.ArgumentParser(description="Codex Account Switcher")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List saved accounts")
    list_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show extra diagnostics (refresh age + token TTL)",
    )
    list_parser.add_argument(
        "--json",
        action="store_true",
        help="Output verbose information as JSON",
    )

    add_parser = subparsers.add_parser("add", help="Run a fresh login and save as an account")
    add_parser.add_argument(
        "--name",
        help="Optional account name (non-interactive default). If omitted, uses email local-part or userId.",
    )
    add_parser.add_argument("--sync", action="store_true", help="Also sync the saved token into OpenClaw after saving")
    add_parser.add_argument("--agent", action="append", help="Limit OpenClaw sync to a specific agent (repeatable)")

    use_parser = subparsers.add_parser("use", help="Switch to an account")
    use_parser.add_argument("name", help="Name of the account to switch to")
    use_parser.add_argument("--sync", action="store_true", help="Also sync this account into OpenClaw after switching")
    use_parser.add_argument("--agent", action="append", help="Limit OpenClaw sync to a specific agent (repeatable)")

    save_parser = subparsers.add_parser("save", help="Save current token to a named account")
    save_parser.add_argument("name", help="Name to save the account as")
    save_parser.add_argument("--force", action="store_true", help="Force overwrite even if emails don't match")
    save_parser.add_argument("--sync", action="store_true", help="Also sync the saved token into OpenClaw")
    save_parser.add_argument("--agent", action="append", help="Limit OpenClaw sync to a specific agent (repeatable)")

    auto_parser = subparsers.add_parser("auto", help="Switch to the account with most quota available")
    auto_parser.add_argument("--json", action="store_true", help="Output as JSON")
    auto_parser.add_argument("--sync", action="store_true", help="Also sync the selected account into OpenClaw")
    auto_parser.add_argument("--agent", action="append", help="Limit OpenClaw sync to a specific agent (repeatable)")

    compare_parser = subparsers.add_parser("compare", help="Compare decoded token claims between two saved accounts")
    compare_parser.add_argument("left", help="First account name")
    compare_parser.add_argument("right", help="Second account name")
    compare_parser.add_argument("--json", action="store_true", help="Output as JSON")

    sync_parser = subparsers.add_parser("sync", help="Explicitly sync saved accounts to OpenClaw auth profiles")
    sync_parser.add_argument("names", nargs="*", help="Optional saved account names to sync (defaults to all)")
    sync_parser.add_argument("--agent", action="append", help="Limit OpenClaw sync to a specific agent (repeatable)")
    sync_parser.add_argument("--dry-run", action="store_true", help="Show what would be synced without writing files")

    args = parser.parse_args()

    # Always persist the currently active login back into its named snapshot.
    sync_current_login_to_snapshot()

    if args.command == "add":
        cmd_add(
            name_override=getattr(args, "name", None),
            sync_openclaw=bool(getattr(args, "sync", False)),
            agent_names=getattr(args, "agent", None),
        )
    elif args.command == "use":
        cmd_use(
            args.name,
            sync_openclaw=bool(getattr(args, "sync", False)),
            agent_names=getattr(args, "agent", None),
        )
    elif args.command == "save":
        cmd_save(
            args.name,
            force=bool(getattr(args, "force", False)),
            sync_openclaw=bool(getattr(args, "sync", False)),
            agent_names=getattr(args, "agent", None),
        )
    elif args.command == "auto":
        cmd_auto(
            json_mode=bool(getattr(args, "json", False)),
            sync_openclaw=bool(getattr(args, "sync", False)),
            agent_names=getattr(args, "agent", None),
        )
    elif args.command == "compare":
        cmd_compare(args.left, args.right, json_mode=bool(getattr(args, "json", False)))
    elif args.command == "sync":
        cmd_sync(
            account_names=getattr(args, "names", None),
            agent_names=getattr(args, "agent", None),
            dry_run=bool(getattr(args, "dry_run", False)),
        )
    else:
        cmd_list(
            verbose=bool(getattr(args, "verbose", False)),
            json_mode=bool(getattr(args, "json", False)),
        )

if __name__ == "__main__":
    main()
