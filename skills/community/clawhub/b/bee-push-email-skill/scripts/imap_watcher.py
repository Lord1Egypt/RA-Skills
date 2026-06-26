#!/usr/bin/env python3
"""
IMAP IDLE watcher — push real de emails nuevos a OpenClaw agent.
Mantiene conexion IMAP IDLE persistente, cuando llega un email nuevo
ejecuta openclaw agent para que lo procese y notifique al usuario.

Config: /opt/imap-watcher/watcher.conf (JSON)
State: /opt/imap-watcher/last_seen_uids.json
Logs:  /var/log/imap-watcher.log + journalctl
"""

import imapclient
import subprocess
import time
import json
import os
import sys
import logging
import signal
from datetime import datetime

# --- Config loading ---
CONFIG_PATH = '/opt/imap-watcher/watcher.conf'
STATE_PATH = '/opt/imap-watcher/last_seen_uids.json'
LOG_PATH = '/var/log/imap-watcher.log'

# Reconnection backoff: starts at 10s, doubles up to MAX
RECONNECT_INITIAL_DELAY = 10
RECONNECT_MAX_DELAY = 300  # 5 minutes

# Max IDLE cycle duration before forced reconnect (IMAP servers drop idle after ~30 min)
IDLE_TIMEOUT = 1740  # 29 minutes

def _build_logger():
    """Build logger with FileHandler + stdout. Creates log file if missing.
    Falls back to stdout-only if the log file cannot be created (e.g. wrong permissions).
    Stdout is always captured by journald when running under systemd.
    """
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handlers = [logging.StreamHandler(sys.stdout)]
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, 'a'):
            pass
        handlers.append(logging.FileHandler(LOG_PATH))
    except OSError as e:
        sys.stderr.write(f"WARNING: Could not open log file {LOG_PATH}: {e} — logging to stdout only\n")
    logger = logging.getLogger('imap-watcher')
    logger.setLevel(logging.INFO)
    for h in handlers:
        h.setFormatter(fmt)
        logger.addHandler(h)
    return logger

log = _build_logger()

# --- Graceful shutdown ---
_shutdown = False

# --- Session cache (60s TTL to avoid hammering openclaw sessions on email bursts) ---
_session_cache = {'result': None, 'timestamp': 0}
SESSION_CACHE_TTL = 60

# --- Security-critical config fields introduced per version.
# If absent from watcher.conf, watcher logs [SECURITY] WARNING and notifies the agent.
SECURITY_CRITICAL_FIELDS = [
    {
        'field': 'auto_reply_mode',
        'since': '1.4.0',
        'description': 'Controls whether the agent may reply to email senders.',
        'default': 'false',
        'values': ('false', 'ask', 'true'),
    },
    {
        'field': 'openclaw_token',
        'since': '1.5.2',
        'description': 'Gateway auth token for openclaw agent --deliver (required when running as non-root).',
        'default': None,
        'values': None,
    },
]

def _handle_signal(signum, frame):
    global _shutdown
    log.info(f"Received signal {signum}, shutting down gracefully...")
    _shutdown = True

signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGINT, _handle_signal)


def load_config():
    """Load watcher config from JSON file."""
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        config.setdefault('poll_interval', 60)
        config.setdefault('state_file', STATE_PATH)
        config.setdefault('ssl', True)
        config.setdefault('port', 993)
        return config
    except FileNotFoundError:
        log.error(f"Config file not found: {CONFIG_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        log.error(f"Invalid config JSON: {e}")
        sys.exit(1)


def load_state(state_file):
    try:
        with open(state_file) as f:
            data = json.load(f)
            return data.get('last_uid', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def check_security_config(config):
    """Check for missing security-critical config fields.

    For each missing field: logs [SECURITY] WARNING and notifies the OpenClaw
    agent so it can alert the user to run --reconfigure.
    Does NOT stop the watcher — uses safe defaults and continues.
    """
    missing = [
        m for m in SECURITY_CRITICAL_FIELDS
        if m['field'] not in config
    ]
    if not missing:
        return

    for m in missing:
        log.warning(
            f"[SECURITY] Field '{m['field']}' missing from config (introduced in v{m['since']}). "
            f"{m['description']} "
            f"Defaulting to '{m['default']}'. "
            f"Run: python3 <skill_dir>/scripts/setup.py --reconfigure"
        )

    # Notify the agent so it can alert the user
    fields_list = ', '.join(f"'{m['field']}'" for m in missing)
    message = (
        f"[SECURITY] bee-push-email has {len(missing)} missing security config field(s): "
        f"{fields_list}. "
        f"Safe defaults are active, but explicit configuration is required. "
        f"Please run: python3 <skill_dir>/scripts/setup.py --reconfigure — "
        f"then restart: systemctl restart imap-watcher"
    )
    try:
        cmd = ['openclaw', 'agent', '--deliver', '--message', message]
        session = get_active_session(config)
        if session and session.get('session_id'):
            cmd.extend(['--session-id', session['session_id']])
        elif session and session.get('channel'):
            cmd.extend(['--channel', session['channel']])
            if session.get('target'):
                cmd.extend(['--to', session['target']])
        subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        log.info("[SECURITY] Agent notified about missing config fields.")
    except Exception as e:
        log.warning(f"[SECURITY] Could not notify agent about missing fields: {e}")


def save_state(state_file, last_uid):
    tmp = state_file + '.tmp'
    try:
        with open(tmp, 'w') as f:
            json.dump({'last_uid': last_uid, 'updated': datetime.utcnow().isoformat()}, f)
        os.replace(tmp, state_file)  # atomic write
    except OSError as e:
        log.warning(f"Could not save state: {e}")
        # Clean up .tmp to avoid stale file accumulation
        try:
            os.unlink(tmp)
        except OSError:
            pass


def get_active_session(config):
    """Resolve active OpenClaw session dynamically (with 60s cache)."""
    import re

    # Cache to avoid hammering openclaw sessions on email bursts
    now = time.monotonic()
    if _session_cache['result'] is not None and (now - _session_cache['timestamp']) < SESSION_CACHE_TTL:
        return _session_cache['result']

    def _cache_and_return(result):
        _session_cache['result'] = result
        _session_cache['timestamp'] = time.monotonic()
        return result

    if config.get('channel') and config.get('target'):
        return _cache_and_return({'channel': config['channel'], 'target': config['target']})

    preferred_channel = config.get('preferred_channel', 'telegram')

    try:
        cmd_result = subprocess.run(
            ['openclaw', 'sessions'],
            capture_output=True,
            text=True,
            timeout=15
        )
        output = cmd_result.stdout
        lines = output.strip().split('\n')

        uuid_re = re.compile(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', re.I)

        # Look for direct session matching preferred channel
        for line in lines:
            if preferred_channel.lower() in line.lower() and 'direct' in line.lower():
                match = uuid_re.search(line)
                if match:
                    log.info(f"Resolved active session: {match.group(1)}")
                    return _cache_and_return({'session_id': match.group(1)})

        # Fallback: any UUID found
        for line in lines:
            match = uuid_re.search(line)
            if match:
                log.info(f"Using fallback session: {match.group(1)}")
                return _cache_and_return({'session_id': match.group(1)})

        log.warning("No active session found via 'openclaw sessions'")
        _session_cache['result'] = None
        _session_cache['timestamp'] = time.monotonic()
        return None

    except FileNotFoundError:
        log.error("openclaw binary not found in PATH")
        return None
    except subprocess.TimeoutExpired:
        log.error("openclaw sessions timed out")
        return None
    except Exception as e:
        log.error(f"Failed to resolve session: {e}")
        return None


def fetch_email_metadata(uids, config):
    """Fetch From and Subject for a set of UIDs using himalaya CLI.

    Returns a list of dicts: [{'uid': int, 'from': str, 'subject': str}, ...]
    Returns empty list if himalaya is unavailable or fails — caller degrades gracefully.
    """
    import shutil, tempfile, atexit

    himalaya = shutil.which('himalaya')
    if not himalaya:
        log.debug("himalaya not found — skipping email metadata fetch")
        return []

    # Build a minimal himalaya config from watcher.conf
    tmpdir = tempfile.mkdtemp(prefix='bee-meta-')
    tmp_config = os.path.join(tmpdir, 'config.toml')
    atexit.register(lambda: __import__('shutil').rmtree(tmpdir, ignore_errors=True))

    try:
        enc_type = 'tls' if config.get('ssl', True) else 'none'
        toml_content = (
            '[accounts."watcher"]\n'
            + 'email = "' + config['email'] + '"\n'
            + 'default = true\n'
            + 'backend.type = "imap"\n'
            + 'backend.host = "' + config['host'] + '"\n'
            + 'backend.port = ' + str(config['port']) + '\n'
            + 'backend.encryption.type = "' + enc_type + '"\n'
            + 'backend.login = "' + config['email'] + '"\n'
            + 'backend.auth.type = "password"\n'
            + 'backend.auth.raw = "' + config['password'] + '"\n'
        )
        with open(tmp_config, 'w') as f:
            f.write(toml_content)

        folder = config.get('folder', 'INBOX')
        results = []

        for uid in sorted(uids):
            try:
                result = subprocess.run(
                    ['himalaya', '-c', tmp_config, '-a', 'watcher',
                     '-f', folder, 'message', 'read', str(uid),
                     '--preview'],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode != 0:
                    log.debug(f"himalaya read uid={uid} failed: {result.stderr.strip()[:100]}")
                    results.append({'uid': uid, 'from': None, 'subject': None})
                    continue

                # Parse From and Subject from output headers
                from_val = None
                subject_val = None
                for line in result.stdout.splitlines():
                    low = line.lower()
                    if low.startswith('from:') and from_val is None:
                        from_val = line[5:].strip()
                    elif low.startswith('subject:') and subject_val is None:
                        subject_val = line[8:].strip()
                    if from_val and subject_val:
                        break

                results.append({'uid': uid, 'from': from_val, 'subject': subject_val})
                log.debug(f"Metadata uid={uid}: from={from_val!r} subject={subject_val!r}")

            except subprocess.TimeoutExpired:
                log.warning(f"himalaya timed out reading uid={uid}")
                results.append({'uid': uid, 'from': None, 'subject': None})
            except Exception as e:
                log.warning(f"Error fetching metadata for uid={uid}: {e}")
                results.append({'uid': uid, 'from': None, 'subject': None})

        return results

    except Exception as e:
        log.warning(f"Could not build himalaya config for metadata fetch: {e}")
        return []
    finally:
        try:
            os.unlink(tmp_config)
            os.rmdir(tmpdir)
        except OSError:
            pass


def _format_email_summary(metadata):
    """Format a list of email metadata dicts into a readable summary string."""
    lines = []
    for m in metadata:
        uid = m.get('uid', '?')
        from_val = m.get('from') or 'unknown sender'
        subject_val = m.get('subject') or '(no subject)'
        lines.append(f"  UID {uid} | From: {from_val} | Subject: {subject_val}")
    return '\n'.join(lines)


def notify_openclaw(config, new_uids=None):
    """Trigger OpenClaw agent to check email.

    new_uids: set of new UIDs just detected — used to fetch metadata for
              enriched messages. Pass None to skip metadata fetch.
    """
    session = get_active_session(config)

    cmd = ['openclaw', 'agent', '--deliver']

    # Pass the gateway token so the watcher can authenticate as non-root user.
    # The token is read from the OpenClaw config during install and stored in watcher.conf.
    token = config.get('openclaw_token')
    if token:
        cmd.extend(['--token', token])
    else:
        log.warning("[SECURITY] openclaw_token not set in watcher.conf — delivery may fail. "
                    "Run setup.py --reconfigure to fix.")

    if session and session.get('session_id'):
        cmd.extend(['--session-id', session['session_id']])
    elif session and session.get('channel'):
        cmd.extend(['--channel', session['channel']])
        if session.get('target'):
            cmd.extend(['--to', session['target']])
    else:
        log.warning("No active session resolved; delivering without explicit session")

    folder = config.get('folder', 'INBOX')

    # Build delivery message — respects auto_reply_mode config.
    # auto_reply_mode values:
    #   'false' (default) — never reply to sender
    #   'ask'             — ask the user for explicit approval before replying
    #   'true'            — agent may reply if it deems appropriate
    if 'message' in config:
        # User has a fully custom message — use it as-is
        message = config['message']
    else:
        mode = str(config.get('auto_reply_mode', 'false')).lower()

        # Fetch email metadata for enriched messages
        metadata = []
        if new_uids:
            metadata = fetch_email_metadata(new_uids, config)

        # Build email context block (used in all modes when metadata is available)
        email_context = _format_email_summary(metadata) if metadata else None

        if mode == 'true':
            reply_instruction = "You may reply to the sender if you deem it appropriate."
            if email_context:
                message = (
                    "New email(s) received in " + folder + ":\n" + email_context + "\n\n"
                    "Analyze if important and notify the user. "
                    + reply_instruction + " "
                    "If it's an automated alert, move it to the appropriate folder."
                )
            else:
                message = (
                    "New email received in " + folder + ". "
                    "Analyze if important and notify the user. "
                    + reply_instruction + " "
                    "If it's an automated alert, move it to the appropriate folder."
                )

        elif mode == 'ask':
            if metadata:
                approval_blocks = []
                for m in metadata:
                    uid = m.get('uid', '?')
                    from_val = m.get('from') or 'unknown sender'
                    subject_val = m.get('subject') or '(no subject)'
                    approval_blocks.append(
                        "  📨 New email — UID " + str(uid) + "\n"
                        + "  From: " + from_val + "\n"
                        + "  Subject: " + subject_val + "\n"
                        + "  → Ask the user: 'Do you want me to reply to this email "
                        + "from " + from_val + " (subject: " + subject_val + ")? [Yes / No]'\n"
                        + "  Only reply if the user explicitly confirms. "
                        + "If yes, use himalaya to reply to UID " + str(uid) + "."
                    )
                message = (
                    "New email(s) received in " + folder + ". "
                    "DO NOT reply yet — ask the user for explicit approval for each one:\n\n"
                    + ("\n\n").join(approval_blocks)
                )
            else:
                message = (
                    "New email received in " + folder + ". "
                    "DO NOT reply to the sender yet. "
                    "Use himalaya to read the email, then ask the user via their active channel: "
                    "'Do you want me to reply to this email from [sender] (subject: [subject])? [Yes / No]' "
                    "Only reply if the user explicitly confirms."
                )
            log.info("[ASK MODE] Approval request sent for UIDs: " + str(sorted(new_uids) if new_uids else 'unknown'))

        else:  # 'false' or any unrecognised value — safe default
            if mode not in ('false',):
                log.warning(
                    "[SECURITY] Unknown auto_reply_mode '" + mode + "' — defaulting to 'false' (no reply)."
                )
            reply_instruction = (
                "DO NOT reply to the sender under any circumstances. "
                "Notify the user via their active channel only."
            )
            if email_context:
                message = (
                    "New email(s) received in " + folder + ":\n" + email_context + "\n\n"
                    "Analyze if important and notify the user. "
                    + reply_instruction + " "
                    "If it's an automated alert, move it to the appropriate folder."
                )
            else:
                message = (
                    "New email received in " + folder + ". "
                    "Analyze if important and notify the user. "
                    + reply_instruction + " "
                    "If it's an automated alert, move it to the appropriate folder."
                )

    cmd.extend(['--message', message])

    try:
        log.info(f"Triggering OpenClaw agent: {' '.join(cmd[:6])}...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        log.info(f"OpenClaw agent triggered. Exit code: {result.returncode}")
        if result.stdout:
            log.info(f"OpenClaw stdout: {result.stdout[:500]}")
        if result.stderr:
            log.warning(f"OpenClaw stderr: {result.stderr[:500]}")
    except subprocess.TimeoutExpired:
        log.error("OpenClaw agent timed out (120s)")
    except Exception as e:
        log.error(f"Failed to notify OpenClaw: {e}")


def check_new_mail(client, folder, last_uid):
    """Check for new messages by UID — doesn't rely on SEEN flag."""
    client.select_folder(folder)
    uids = client.search('ALL')
    if not uids:
        return set(), max(last_uid, 0)
    current_max = max(uids)
    new_uids = set(u for u in uids if u > last_uid)
    return new_uids, current_max


def connect(config):
    """Create and return an authenticated IMAP client."""
    client = imapclient.IMAPClient(
        config['host'],
        port=config['port'],
        ssl=config['ssl']
    )
    client.login(config['email'], config['password'])
    client.select_folder(config.get('folder', 'INBOX'))
    log.info(f"IMAP connected to {config['host']} as {config['email']}")
    return client


def idle_loop(client, config, last_uid):
    """
    Run the IMAP IDLE loop until a reconnect is needed.
    Returns updated last_uid.

    If the server does not support IMAP IDLE, falls back to pure polling
    for the entire connection lifetime (no repeated idle() attempts).
    """
    folder = config.get('folder', 'INBOX')
    idle_start = time.monotonic()
    poll_interval = config.get('poll_interval', 60)

    # --- polling fallback (set to True if server reports IDLEUnsupported) ---
    use_polling = False

    while not _shutdown:
        # Force reconnect after IDLE_TIMEOUT to avoid server-side drops
        if time.monotonic() - idle_start > IDLE_TIMEOUT:
            log.info("IDLE timeout reached — reconnecting to keep session fresh")
            break

        # --- Polling mode (server does not support IDLE) ---
        if use_polling:
            time.sleep(poll_interval)
            try:
                new, last_uid = check_new_mail(client, folder, last_uid)
                if new:
                    log.info(f"Poll: found {len(new)} new email(s)")
                    notify_openclaw(config, new_uids=new)
                    save_state(config['state_file'], last_uid)
            except Exception as e:
                log.warning(f"Poll error: {e}")
                break
            continue

        # --- IDLE mode ---
        try:
            client.idle()
            responses = client.idle_check(timeout=30)

            if responses:
                log.info(f"IMAP IDLE got {len(responses)} response(s): {responses[:5]}")
                client.idle_done()

                new, last_uid = check_new_mail(client, folder, last_uid)
                if new:
                    log.info(f"Found {len(new)} new email(s) (UIDs: {sorted(new)})")
                    notify_openclaw(config, new_uids=new)
                    save_state(config['state_file'], last_uid)
                else:
                    log.debug("IDLE response with no new UIDs (flag change or EXISTS update)")
            else:
                client.idle_done()
                log.debug("IDLE 30s timeout, re-entering IDLE...")

        except imapclient.exceptions.IDLEUnsupported:
            log.warning("IMAP IDLE not supported by server — switching to polling mode")
            try:
                client.idle_done()
            except Exception:
                pass
            use_polling = True  # stay in polling for the rest of this connection

        except (ConnectionError, ConnectionResetError, BrokenPipeError) as e:
            log.warning(f"IMAP connection lost: {e}")
            try:
                client.idle_done()
            except Exception:
                pass
            break

        except Exception as e:
            log.error(f"IDLE error: {type(e).__name__}: {e}")
            try:
                client.idle_done()
            except Exception:
                pass
            break

    return last_uid


def main():
    config = load_config()
    folder = config.get('folder', 'INBOX')
    reconnect_delay = RECONNECT_INITIAL_DELAY

    log.info(f"Starting IMAP watcher for {config['email']} on {folder}")
    last_uid = load_state(config['state_file'])
    log.info(f"Last seen UID: {last_uid}")

    # Check for missing security-critical fields — warns and notifies agent if any
    check_security_config(config)

    while not _shutdown:
        client = None
        try:
            client = connect(config)
            reconnect_delay = RECONNECT_INITIAL_DELAY  # reset backoff on success

            # Initial check for emails missed while disconnected
            new, last_uid = check_new_mail(client, folder, last_uid)
            if new:
                log.info(f"Catch-up: found {len(new)} email(s) missed while disconnected")
                notify_openclaw(config, new_uids=new)
                save_state(config['state_file'], last_uid)

            last_uid = idle_loop(client, config, last_uid)

        except imapclient.exceptions.LoginError as e:
            log.error(f"IMAP login failed: {e} — check credentials in {CONFIG_PATH}")
            # Don't hammer the server on auth failure — wait longer
            reconnect_delay = min(reconnect_delay * 2, RECONNECT_MAX_DELAY)

        except Exception as e:
            log.error(f"Connection error: {type(e).__name__}: {e}")
            reconnect_delay = min(reconnect_delay * 2, RECONNECT_MAX_DELAY)

        finally:
            if client:
                try:
                    client.logout()
                except Exception:
                    pass

        if _shutdown:
            break

        log.info(f"Reconnecting in {reconnect_delay}s...")
        time.sleep(reconnect_delay)

    log.info("IMAP watcher stopped.")


if __name__ == '__main__':
    main()
