#!/usr/bin/env python3
"""
Telegram Bot Commands management for bee-push-email.

Handles registration, verification, and unregistration of /beemail* commands
in the Telegram bot menu. Used by setup.py and uninstall.sh.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

OPENCLAW_CONFIG_PATHS = ['/root/.openclaw/openclaw.json']

if os.environ.get('OPENCLAW_HOME'):
    OPENCLAW_CONFIG_PATHS.insert(
        0, os.path.join(os.environ['OPENCLAW_HOME'], 'openclaw.json')
    )

BEE_COMMANDS = [
    {"command": "beemail", "description": "Email push status & recent emails"},
    {"command": "beemail_start", "description": "Start IMAP email watcher"},
    {"command": "beemail_stop", "description": "Stop IMAP email watcher"},
    {"command": "beemail_status", "description": "Detailed watcher service status"},
    {"command": "beemail_test", "description": "Send test email to verify push"},
    {"command": "beemail_reply", "description": "Show current auto-reply mode"},
    {"command": "beemail_reply_off", "description": "Disable auto-reply (never reply to senders)"},
    {"command": "beemail_reply_ask", "description": "Ask for approval before replying to senders"},
    {"command": "beemail_reply_on", "description": "Enable auto-reply (agent decides — use with caution)"},
]


def get_telegram_bot_token():
    """Find the Telegram bot token from OpenClaw config.

    Searches multiple config locations and JSON structures.
    Returns the token string or None.
    """
    home = os.path.expanduser('~')
    candidates = list(OPENCLAW_CONFIG_PATHS) + [
        os.path.join(home, '.openclaw', 'openclaw.json'),
    ]

    # Deduplicate preserving order
    seen = set()
    paths = []
    for p in candidates:
        if p not in seen:
            seen.add(p)
            paths.append(p)

    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                data = json.load(f)

            # Try multiple known JSON structures
            tg_candidates = [
                data.get('channels', {}).get('telegram', {}),
                data.get('providers', {}).get('telegram', {}),
                data.get('telegram', {}),
            ]
            for tg in tg_candidates:
                if not isinstance(tg, dict):
                    continue
                token = tg.get('botToken') or tg.get('token') or tg.get('bot_token')
                if token:
                    return token

        except (json.JSONDecodeError, KeyError, TypeError, PermissionError) as e:
            print(f"  ⚠ Could not read {path}: {e}")
            continue

    return None


def bot_api_request(token, method, data=None, retries=3, retry_delay=2):
    """Make a Telegram Bot API request with retry on transient network errors.

    - HTTP errors (bad token, bad params): logged and returned immediately, no retry.
    - Network/timeout errors: retried up to `retries` times with `retry_delay` seconds.
    - API ok=false: logged with description, returned immediately.

    Returns a dict with at least an 'ok' key.
    """
    url = f"https://api.telegram.org/bot{token}/{method}"
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            if data:
                payload = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(
                    url, data=payload,
                    headers={'Content-Type': 'application/json'},
                )
            else:
                req = urllib.request.Request(url)

            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode('utf-8'))

            if not result.get('ok'):
                desc = result.get('description', 'unknown error')
                err_code = result.get('error_code', '?')
                print(f"  ⚠ Telegram API error [{method}] ({err_code}): {desc}")
            return result

        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            try:
                result = json.loads(body)
                desc = result.get('description', str(e))
            except json.JSONDecodeError:
                desc = f"HTTP {e.code}: {body[:200]}"
            print(f"  ⚠ Telegram HTTP error [{method}]: {desc}")
            # HTTP errors indicate token/param problems — don't retry
            return {'ok': False, 'description': desc}

        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_error = str(e)
            if attempt < retries:
                print(f"  ⚠ Network error (attempt {attempt}/{retries}): {e} — retrying in {retry_delay}s…")
                time.sleep(retry_delay)
            else:
                print(f"  ✗ Network error after {retries} attempts: {e}")

    return {'ok': False, 'description': f"Network error: {last_error}"}


def get_current_bot_commands(token):
    """Get current bot commands from Telegram.

    Returns (commands_list, success_bool).
    Distinguishes between 'empty list' (ok=True, result=[]) and 'API failure' (ok=False).
    This is critical: returning [] on failure would wipe existing commands on setMyCommands.
    """
    result = bot_api_request(token, 'getMyCommands')
    if result.get('ok'):
        return result.get('result', []), True
    return [], False


def set_bot_commands(token, commands):
    """Set bot commands (replaces all). Returns True on success."""
    result = bot_api_request(token, 'setMyCommands', {'commands': commands})
    return result.get('ok', False)


def _print_botfather_instructions():
    """Print manual registration instructions via BotFather."""
    print("  Register manually via @BotFather → /setcommands:")
    for cmd in BEE_COMMANDS:
        print(f"    {cmd['command']} — {cmd['description']}")


def register_bee_commands(verbose=True):
    """Add beemail commands to Telegram bot menu without removing existing ones.

    Safe: fetches current commands first. If fetch fails, aborts rather than
    calling setMyCommands with an empty list (which would wipe all commands).

    Also updates descriptions if they changed between versions.

    Returns True if commands are now registered, False otherwise.
    """
    if verbose:
        print("\n📱 Registering bot commands…")

    token = get_telegram_bot_token()
    if not token:
        if verbose:
            print("  ⚠ Telegram bot token not found in OpenClaw config")
            print("    Searched: $OPENCLAW_HOME, ~/.openclaw/openclaw.json, /root/.openclaw/openclaw.json")
            _print_botfather_instructions()
        return False

    if verbose:
        print(f"  ✓ Bot token found (***{token[-6:]})")

    # CRITICAL: distinguish between empty list and API failure.
    # If fetch fails, abort — don't call setMyCommands with [] which would wipe existing commands.
    current, fetch_ok = get_current_bot_commands(token)
    if not fetch_ok:
        if verbose:
            print("  ✗ Could not fetch current bot commands — aborting to avoid overwriting them")
            print("    Check your bot token and network, then retry:")
            print("    python3 setup.py --register-commands")
        return False

    if verbose:
        print(f"  ✓ Fetched {len(current)} existing command(s)")

    current_map = {c['command']: c for c in current}
    added = 0
    updated = 0

    for cmd in BEE_COMMANDS:
        if cmd['command'] not in current_map:
            current.append(cmd)
            added += 1
        elif current_map[cmd['command']].get('description') != cmd['description']:
            # Update description if it changed between versions
            current_map[cmd['command']]['description'] = cmd['description']
            updated += 1

    if added == 0 and updated == 0:
        if verbose:
            print(f"  ✓ All {len(BEE_COMMANDS)} beemail commands already registered and up to date")
        return True

    ok = set_bot_commands(token, current)
    if ok:
        if verbose:
            parts = []
            if added:
                parts.append(f"{added} added")
            if updated:
                parts.append(f"{updated} updated")
            print(f"  ✓ Bot commands registered ({', '.join(parts)})")
        return True

    if verbose:
        print("  ✗ setMyCommands failed — commands not registered")
        print("    Retry: python3 setup.py --register-commands")
        _print_botfather_instructions()
    return False


def verify_bee_commands(verbose=True):
    """Verify that all beemail commands are registered in Telegram.

    Returns True if all commands are present, False otherwise.
    """
    token = get_telegram_bot_token()
    if not token:
        return False

    current, fetch_ok = get_current_bot_commands(token)
    if not fetch_ok:
        if verbose:
            print("  ⚠ Could not verify commands — API unavailable")
        return False

    registered = {c['command'] for c in current}
    expected = {c['command'] for c in BEE_COMMANDS}
    missing = expected - registered

    if not missing:
        if verbose:
            print(f"  ✓ All {len(BEE_COMMANDS)} beemail commands verified in Telegram")
        return True

    if verbose:
        print(f"  ⚠ Missing commands after registration: {', '.join(sorted(missing))}")
    return False


def unregister_bee_commands(verbose=True):
    """Remove beemail commands from Telegram bot menu, keeping everything else.

    Safe: fetches current list first. If fetch fails, skips rather than
    wiping all commands with setMyCommands([]).
    """
    token = get_telegram_bot_token()
    if not token:
        if verbose:
            print("  ⚠ Bot token not found — skipping command unregistration")
            print("    Remove beemail commands manually via @BotFather → /setcommands")
        return

    current, fetch_ok = get_current_bot_commands(token)
    if not fetch_ok:
        if verbose:
            print("  ⚠ Could not fetch current bot commands — skipping unregistration")
            print("    Remove beemail commands manually via @BotFather → /setcommands")
        return

    bee_set = {c['command'] for c in BEE_COMMANDS}
    filtered = [c for c in current if c['command'] not in bee_set]
    removed = len(current) - len(filtered)

    if removed == 0:
        if verbose:
            print('  ✓ No beemail commands to remove')
        return

    ok = set_bot_commands(token, filtered)
    if ok:
        if verbose:
            print(f'  ✓ Removed {removed} beemail command(s) from Telegram menu')
    else:
        if verbose:
            print(f'  ⚠ Failed to unregister {removed} beemail command(s)')
            print('    Remove manually via @BotFather → /setcommands')
