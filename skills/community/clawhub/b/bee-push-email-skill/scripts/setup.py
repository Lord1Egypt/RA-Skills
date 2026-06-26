#!/usr/bin/env python3
"""
Email Push setup — non-interactive mode.
Accepts all config as JSON via --config or positional argument.
Designed to be called by an OpenClaw agent on behalf of the user.

Usage:
  python3 setup.py --deps                    # check system dependencies
  python3 setup.py --test <json-config>      # test IMAP+SMTP (no install)
  python3 setup.py --test                    # test current installed config
  python3 setup.py --show                    # show current config (password hidden)
  python3 setup.py --register-commands       # register beemail Telegram bot commands only
  python3 setup.py --reconfigure             # add missing config fields to existing install
  python3 setup.py --reply-status            # show current auto_reply_mode
  python3 setup.py --reply-off               # set auto_reply_mode=false + restart service
  python3 setup.py --reply-ask               # set auto_reply_mode=ask  + restart service
  python3 setup.py --reply-on                # set auto_reply_mode=true + restart service
  python3 setup.py --force <json-config>     # reinstall without confirmation
  python3 setup.py <json-config>            # full install (deps + test + install + verify)

JSON schema:
{
  "host": "imap.example.com",
  "port": 993,
  "ssl": true,
  "email": "user@example.com",
  "password": "app-password",
  "folder": "INBOX",
  "preferred_channel": "telegram",
  "channel": "telegram",
  "target": "CHAT_ID_HERE",
  "auto_reply_mode": "false"
}
"""

import json
import os
import subprocess
import sys
import shutil
import time

INSTALL_DIR = '/opt/imap-watcher'
WATCHER_USER = 'imap-watcher'
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHER_SCRIPT = os.path.join(SKILL_DIR, 'scripts', 'imap_watcher.py')
SERVICE_TEMPLATE = os.path.join(SKILL_DIR, 'assets', 'imap-watcher.service')
CONFIG_PATH = os.path.join(INSTALL_DIR, 'watcher.conf')
LOG_PATH = '/var/log/imap-watcher.log'

# Import Telegram commands module from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from telegram_commands import register_bee_commands, verify_bee_commands


def run(cmd, check=True, capture_output=False):
    """Run a shell command."""
    is_shell = isinstance(cmd, str)
    print(f"  $ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd, shell=is_shell, capture_output=capture_output, text=capture_output
    )
    if check and result.returncode != 0:
        out = result.stderr.strip() if capture_output else ''
        print(f"  ✗ Failed (exit {result.returncode}){': ' + out if out else ''}")
        sys.exit(1)
    return result


def load_config(args):
    """Load config from file argument or stdin."""
    config_data = None

    if '--config' in args:
        idx = args.index('--config')
        path = args[idx + 1] if idx + 1 < len(args) else None
        if not path or not os.path.exists(path):
            print("✗ --config requires a valid file path")
            sys.exit(1)
        with open(path) as f:
            config_data = f.read()
    elif len(args) > 1 and not args[1].startswith('--'):
        config_data = args[1]
        if os.path.exists(args[1]):
            with open(args[1]) as f:
                config_data = f.read()
    else:
        config_data = sys.stdin.read()

    try:
        return json.loads(config_data)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        sys.exit(1)


def validate_config(config):
    """Validate required config fields and set defaults."""
    required = ['host', 'port', 'ssl', 'email', 'password']
    for field in required:
        if field not in config:
            print(f"✗ Missing required field: {field}")
            sys.exit(1)

    # Validate non-empty password
    if not config['password'] or not config['password'].strip():
        print("✗ Password cannot be empty")
        sys.exit(1)

    config.setdefault('folder', 'INBOX')
    config.setdefault('poll_interval', 60)
    config.setdefault('preferred_channel', 'telegram')

    # ask_auto_reply only in interactive full-install flow (stdin.isatty guard is inside)
    if 'auto_reply_mode' not in config:
        config['auto_reply_mode'] = ask_auto_reply_mode()

    # Read OpenClaw gateway token so the watcher can call --deliver as non-root user
    if 'openclaw_token' not in config:
        token, source = read_openclaw_gateway_token()
        if token:
            config['openclaw_token'] = token
            print(f"  ✓ OpenClaw gateway token found ({source})")
        else:
            print("  ⚠ OpenClaw gateway token not found — watcher may fail to deliver notifications")
            print("    Searched: $OPENCLAW_HOME, /root/.openclaw/openclaw.json, ~/.openclaw/openclaw.json")
            print("    You can add it manually: set 'openclaw_token' in /opt/imap-watcher/watcher.conf")

    return config


def check_himalaya():
    """Check if himalaya is installed."""
    return shutil.which('himalaya') is not None


def install_himalaya():
    """Install himalaya CLI."""
    print("\n📦 Installing himalaya…")

    arch = os.uname().machine
    if arch in ('x86_64', 'amd64'):
        arch_suffix = 'linux-x86_64'
    elif arch in ('aarch64', 'arm64'):
        arch_suffix = 'linux-arm64'
    elif arch in ('armv7l', 'armhf'):
        arch_suffix = 'linux-armv7'
    else:
        arch_suffix = 'linux-x86_64'
        print(f"  ⚠ Unknown arch {arch}, trying x86_64")

    url = f'https://github.com/pimalaya/himalaya/releases/latest/download/himalaya-{arch_suffix}.tar.gz'
    result = run(f'curl -sSfL {url} | tar -xz -C /usr/local/bin/ himalaya', check=False)
    if shutil.which('himalaya'):
        print(f"  ✓ himalaya installed ({arch_suffix})")
        return True
    print("  ⚠️  Could not install himalaya automatically")
    return False


def ensure_system_user():
    """Create the imap-watcher system user if it doesn't exist."""
    print("\n👤 Setting up system user…")
    result = run(f'id {WATCHER_USER}', check=False, capture_output=True)
    if result.returncode == 0:
        print(f"  ✓ User '{WATCHER_USER}' already exists")
        return

    run(f'useradd -r -s /sbin/nologin -d {INSTALL_DIR} {WATCHER_USER}')
    print(f"  ✓ System user '{WATCHER_USER}' created")


def create_venv():
    """Create Python venv and install imapclient."""
    print("\n🐍 Setting up Python venv…")
    venv_python = os.path.join(INSTALL_DIR, 'bin', 'python3')
    if not os.path.exists(venv_python):
        run(['python3', '-m', 'venv', INSTALL_DIR])
    run([venv_python, '-m', 'pip', 'install', '--quiet', 'imapclient'])
    print("  ✓ venv ready with imapclient")
    return venv_python


def save_config(config):
    """Save config to disk, backing up existing config."""
    os.makedirs(INSTALL_DIR, exist_ok=True)
    if os.path.exists(CONFIG_PATH):
        backup = CONFIG_PATH + '.bak'
        shutil.copy2(CONFIG_PATH, backup)
        print(f"  ✓ Backed up existing config to {backup}")
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_PATH, 0o600)
    print(f"  ✓ Config saved to {CONFIG_PATH}")


def fix_permissions():
    """Set correct ownership and permissions for all installed files."""
    print("\n🔒 Setting permissions…")
    run(f'chown -R {WATCHER_USER}:{WATCHER_USER} {INSTALL_DIR}')
    run(f'chmod 700 {INSTALL_DIR}')
    # Ensure config stays 600
    if os.path.exists(CONFIG_PATH):
        os.chmod(CONFIG_PATH, 0o600)
    # Ensure log file exists and is owned by watcher
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'a'):
            pass
    run(f'chown {WATCHER_USER}:{WATCHER_USER} {LOG_PATH}')
    run(f'chmod 640 {LOG_PATH}')
    print(f"  ✓ Permissions set (owner: {WATCHER_USER})")


def install_service():
    """Install and enable systemd service."""
    print("\n🔧 Installing systemd service…")

    ensure_system_user()

    # Copy watcher script
    dest_watcher = os.path.join(INSTALL_DIR, 'imap_watcher.py')
    shutil.copy2(WATCHER_SCRIPT, dest_watcher)
    os.chmod(dest_watcher, 0o755)
    print(f"  ✓ Watcher → {dest_watcher}")

    # Copy service unit
    service_unit = '/etc/systemd/system/imap-watcher.service'
    with open(SERVICE_TEMPLATE) as f:
        content = f.read()
    with open(service_unit, 'w') as f:
        f.write(content)
    print(f"  ✓ Service → {service_unit}")

    run('systemctl daemon-reload')
    run('systemctl enable imap-watcher')
    run('systemctl restart imap-watcher')
    print("  ✓ Service started and enabled")


def verify():
    """Post-install verification: service running + IMAP connected + agent reachable."""
    print("\n🧪 Post-install verification…")

    all_ok = True

    # 1. Service running?
    print("  [1/5] Service status…")
    result = run('systemctl is-active imap-watcher', check=False, capture_output=True)
    if result.stdout.strip() == 'active':
        print("    ✓ Service is running")
    else:
        print("    ✗ Service not running")
        return False

    # 2. Logs show IMAP connected?
    print("  [2/5] IMAP connection…")
    result = run('journalctl -u imap-watcher --since "30 sec ago" --no-pager',
                 check=False, capture_output=True)
    logs = result.stdout
    if 'IMAP connected' in logs or 'IDLE started' in logs or 'IDLE started, waiting' in logs:
        print("    ✓ IMAP IDLE connected")
    else:
        print("    ⚠ IMAP IDLE not confirmed in recent logs (may need a few seconds)")
        time.sleep(3)
        result = run('journalctl -u imap-watcher --since "10 sec ago" --no-pager',
                     check=False, capture_output=True)
        if 'IMAP connected' in result.stdout or 'IDLE started' in result.stdout:
            print("    ✓ IMAP IDLE connected (on retry)")

    # 3. Config file?
    print("  [3/5] Config file…")
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
            required = ['host', 'email', 'password']
            missing = [f for f in required if f not in cfg]
            if not missing:
                print(f"    ✓ Config valid ({cfg['email']})")
            else:
                print(f"    ✗ Config missing fields: {missing}")
                all_ok = False
        except json.JSONDecodeError as e:
            print(f"    ✗ Config invalid JSON: {e}")
            all_ok = False
    else:
        print(f"    ✗ Config not found at {CONFIG_PATH}")
        all_ok = False

    # 4. openclaw agent reachable?
    print("  [4/5] OpenClaw agent reachable…")
    result = run('openclaw sessions', check=False, capture_output=True)
    if result.returncode == 0 and ('telegram' in result.stdout or 'direct' in result.stdout):
        print("    ✓ OpenClaw agent reachable")
    else:
        print("    ⚠ OpenClaw sessions not listing — agent may not be able to deliver")
        all_ok = False

    # Show recent logs
    print("\n  Recent logs:")
    result = run('journalctl -u imap-watcher -n 5 --no-pager', check=False, capture_output=True)
    for line in result.stdout.strip().split('\n'):
        print(f"    {line}")

    # 5. Test openclaw agent --deliver with the stored token
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    deliver_ok, deliver_msg = verify_openclaw_deliver(cfg)
    if not deliver_ok:
        print(f"    ⚠ --deliver test failed: {deliver_msg}")
        print("      Check that openclaw gateway is running and the token is correct.")
        all_ok = False

    if all_ok:
        print(f"\n  📧 End-to-end test:")
        with open(CONFIG_PATH) as f:
            email = json.load(f)['email']
        print(f"     Send an email to {email}")
        print(f"     Watch for the agent notification in your chat.")
        print(f"     Check logs: journalctl -u imap-watcher -f")

    return all_ok


def show_config(config, label="Current"):
    """Display config with password hidden."""
    safe = {k: ('********' if k == 'password' else v) for k, v in config.items()}
    print(f"\n╔══════════════════════════════════════╗")
    print(f"║   📨 Email Push — {label + ' Config':<17}║")
    print(f"╚══════════════════════════════════════╝")
    print(f"\n  Email:    {safe.get('email', '—')}")
    print(f"  Host:     {safe.get('host', '—')}:{safe.get('port', '—')}")
    print(f"  SSL:      {safe.get('ssl', '—')}")
    print(f"  Folder:   {safe.get('folder', '—')}")
    print(f"  Password: {safe.get('password', '—')}")
    if safe.get('channel'):
        print(f"  Channel:  {safe.get('channel')} → {safe.get('target')}")
    else:
        print(f"  Channel:  auto ({safe.get('preferred_channel', 'telegram')})")
    print(f"  Poll:     {safe.get('poll_interval', 60)}s (fallback)")
    print()


def get_imapclient():
    """Try to import imapclient from system or venv."""
    try:
        import imapclient
        return imapclient
    except ImportError:
        venv_python = os.path.join(INSTALL_DIR, 'bin', 'python3')
        if os.path.exists(venv_python):
            result = subprocess.run(
                [venv_python, '-c', 'import imapclient; print(imapclient.__file__)'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                sys.path.insert(0, os.path.dirname(os.path.dirname(result.stdout.strip())))
                import imapclient
                return imapclient
    return None


def test_imap(config):
    """Test IMAP connection and authentication."""
    imapclient = get_imapclient()
    if not imapclient:
        return False, "imapclient not installed — run setup.py first or install it manually"
    try:
        client = imapclient.IMAPClient(
            config['host'],
            port=config['port'],
            ssl=config.get('ssl', True)
        )
        client.login(config['email'], config['password'])
        client.select_folder(config.get('folder', 'INBOX'))
        uids = client.search('ALL')
        client.logout()
        return True, f"OK — {len(uids)} messages in {config.get('folder', 'INBOX')}"
    except imapclient.exceptions.LoginError as e:
        return False, f"Login failed: {e}"
    except Exception as e:
        return False, f"Connection error: {e}"


def test_smtp(config):
    """Test SMTP connection and authentication."""
    try:
        import smtplib

        smtp_host = config.get('smtp_host', config['host'])
        smtp_port = config.get('smtp_port', 587)
        smtp_ssl = config.get('smtp_ssl', False)

        if smtp_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(config['email'], config['password'])
        server.quit()
        return True, "OK — SMTP auth successful"
    except Exception as e:
        return False, f"SMTP error: {e}"


def test_himalaya(config):
    """Test that himalaya can list envelopes using the provided config."""
    himalaya = shutil.which('himalaya')
    if not himalaya:
        return None, "himalaya not installed (optional, agent needs it to read emails)"

    import tempfile
    import atexit
    tmpdir = tempfile.mkdtemp(prefix='bee-push-email-test-')
    tmp_config = os.path.join(tmpdir, 'config.toml')
    atexit.register(lambda: shutil.rmtree(tmpdir, ignore_errors=True))
    try:
        enc_type = 'tls' if config.get('ssl', True) else 'none'
        with open(tmp_config, 'w') as f:
            f.write(f'[accounts."test"]\n')
            f.write(f'email = "{config["email"]}"\n')
            f.write(f'default = true\n')
            f.write(f'backend.type = "imap"\n')
            f.write(f'backend.host = "{config["host"]}"\n')
            f.write(f'backend.port = {config["port"]}\n')
            f.write(f'backend.encryption.type = "{enc_type}"\n')
            f.write(f'backend.login = "{config["email"]}"\n')
            f.write(f'backend.auth.type = "password"\n')
            f.write(f'backend.auth.raw = "{config["password"]}"\n')

        result = subprocess.run(
            ['himalaya', 'envelope', 'list', '--page-size', '1', '--config', tmp_config],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return True, "OK — himalaya can read inbox"
        return False, f"himalaya error: {result.stderr.strip()[:100]}"
    finally:
        try:
            os.remove(tmp_config)
            os.rmdir(tmpdir)
        except OSError:
            pass


def run_test(config, label="Testing"):
    """Run all connection tests."""
    print(f"\n🧪 {label} email configuration…")
    print(f"  Email: {config['email']}\n")

    all_ok = True

    print("  [1/3] IMAP connection…")
    ok, msg = test_imap(config)
    status = "✓" if ok else "✗"
    print(f"    {status} {msg}")
    all_ok = all_ok and ok

    print("  [2/3] SMTP connection…")
    ok, msg = test_smtp(config)
    status = "✓" if ok else "✗"
    print(f"    {status} {msg}")
    all_ok = all_ok and ok

    print("  [3/3] Himalaya CLI…")
    ok, msg = test_himalaya(config)
    if ok is None:
        print(f"    ⚠ {msg}")
    else:
        status = "✓" if ok else "✗"
        print(f"    {status} {msg}")
        all_ok = all_ok and ok

    print()
    if all_ok:
        print("  ✅ All tests passed — configuration is valid!")
    else:
        print("  ❌ Some tests failed — fix the issues above before installing.")

    return all_ok


def check_deps():
    """Check all system dependencies needed for bee-push-email."""
    print("🔍 Checking system dependencies…\n")
    all_ok = True

    # Python 3
    py = shutil.which('python3')
    if py:
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        print(f"  ✓ python3 — {result.stdout.strip()}")
    else:
        print("  ✗ python3 — NOT FOUND (required)")
        all_ok = False

    # venv module
    result = subprocess.run(['python3', '-m', 'venv', '--help'], capture_output=True, timeout=5)
    if result.returncode == 0:
        print(f"  ✓ venv module — available")
    else:
        print(f"  ✗ venv module — NOT FOUND (required, install: apt install python3-venv)")
        all_ok = False

    # pip
    pip = shutil.which('pip3') or shutil.which('pip')
    if pip:
        print(f"  ✓ pip — {pip}")
    else:
        print(f"  ⚠ pip — not found (venv pip will be used instead)")

    # himalaya
    him = shutil.which('himalaya')
    if him:
        result = subprocess.run(['himalaya', '--version'], capture_output=True, text=True)
        print(f"  ✓ himalaya — {result.stdout.strip()}")
    else:
        print(f"  ⚠ himalaya — NOT FOUND (optional but recommended, setup.py can install it)")

    # openclaw CLI
    oc = shutil.which('openclaw')
    if oc:
        result = subprocess.run(['openclaw', '--version'], capture_output=True, text=True)
        print(f"  ✓ openclaw — {result.stdout.strip()}")
    else:
        print(f"  ✗ openclaw — NOT FOUND (required, the watcher triggers openclaw agent)")
        all_ok = False

    # systemd
    sd = shutil.which('systemctl')
    if sd:
        print(f"  ✓ systemd — available")
    else:
        print(f"  ✗ systemd — NOT FOUND (required for service management)")
        all_ok = False

    # useradd (for creating dedicated user)
    ua = shutil.which('useradd')
    if ua:
        print(f"  ✓ useradd — available")
    else:
        print(f"  ⚠ useradd — not found (will run service as root)")

    # curl
    curl = shutil.which('curl')
    if curl:
        print(f"  ✓ curl — {curl}")
    else:
        print(f"  ⚠ curl — not found (needed for automatic himalaya install)")

    # Root check — warn, don't require
    if os.geteuid() == 0:
        print(f"  ⚠ Running as root — service will run as dedicated user '{WATCHER_USER}' (more secure)")
    else:
        print(f"  ⚠ Not root — may need sudo for systemctl and /opt/ install")

    print()
    if all_ok:
        print("  ✅ All required dependencies present!")
    else:
        print("  ❌ Missing required dependencies — install them before running setup.py")

    return all_ok


def set_auto_reply_mode(mode):
    """Update auto_reply_mode in watcher.conf and restart the service.

    Called by the agent when the user sends /beemail_reply_off/ask/on.
    Valid modes: 'false', 'ask', 'true'.
    Returns (success: bool, message: str).
    """
    VALID_MODES = ('false', 'ask', 'true')
    mode = str(mode).lower().strip()
    if mode not in VALID_MODES:
        return False, f"Invalid mode '{mode}'. Valid values: {', '.join(VALID_MODES)}"

    if not os.path.exists(CONFIG_PATH):
        return False, f"Config not found at {CONFIG_PATH} — is bee-push-email installed?"

    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return False, f"Could not read config: {e}"

    previous = config.get('auto_reply_mode', 'not set')
    config['auto_reply_mode'] = mode

    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        os.chmod(CONFIG_PATH, 0o600)
    except OSError as e:
        return False, f"Could not write config: {e}"

    # Restart service to apply the change
    result = subprocess.run(
        ['systemctl', 'restart', 'imap-watcher'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return False, (
            f"Config updated (was: {previous} → now: {mode}) "
            f"but service restart failed: {result.stderr.strip()}"
        )

    labels = {
        'false': '🔒 Auto-reply DISABLED — agent will never reply to senders.',
        'ask':   '❓ Auto-reply set to ASK — agent will request your approval before replying.',
        'true':  '⚠️  Auto-reply ENABLED — agent may reply to senders without asking.',
    }
    return True, f"{labels[mode]} (was: {previous})"


def get_auto_reply_mode():
    """Read current auto_reply_mode from watcher.conf.
    Returns (mode: str, error: str|None).
    """
    if not os.path.exists(CONFIG_PATH):
        return None, f"Config not found at {CONFIG_PATH}"
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        mode = config.get('auto_reply_mode', 'not set')
        return mode, None
    except (json.JSONDecodeError, OSError) as e:
        return None, f"Could not read config: {e}"


def read_openclaw_gateway_token():
    """Read gateway.auth.token from the OpenClaw config file.

    Searches standard OpenClaw config locations as root.
    Returns (token: str, source_path: str) or (None, None) if not found.
    """
    home = os.path.expanduser('~')
    candidates = []
    if os.environ.get('OPENCLAW_HOME'):
        candidates.append(os.path.join(os.environ['OPENCLAW_HOME'], 'openclaw.json'))
    candidates += [
        '/root/.openclaw/openclaw.json',
        os.path.join(home, '.openclaw', 'openclaw.json'),
    ]

    for path in candidates:
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                data = json.load(f)

            # Try multiple known structures for gateway.auth.token
            token = (
                data.get('gateway', {}).get('auth', {}).get('token')
                or data.get('gateway', {}).get('authToken')
                or data.get('gatewayToken')
            )
            if token:
                return token, path
        except (json.JSONDecodeError, OSError, TypeError):
            continue

    return None, None


def verify_openclaw_deliver(config):
    """Verify that openclaw agent --deliver works with the configured token.

    Sends a minimal test delivery and checks the exit code.
    Returns (success: bool, message: str).
    """
    print("  [5/5] OpenClaw agent --deliver…")
    cmd = ['openclaw', 'agent', '--deliver', '--message',
           'bee-push-email install verification ping. Ignore this message.']

    token = config.get('openclaw_token')
    if token:
        cmd.extend(['--token', token])

    # Try to resolve a session
    preferred = config.get('preferred_channel', 'telegram')
    try:
        result = subprocess.run(
            ['openclaw', 'sessions'], capture_output=True, text=True, timeout=10
        )
        import re
        uuid_re = re.compile(
            r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', re.I
        )
        session_id = None
        for line in result.stdout.splitlines():
            if preferred.lower() in line.lower() and 'direct' in line.lower():
                m = uuid_re.search(line)
                if m:
                    session_id = m.group(1)
                    break
        if not session_id:
            for line in result.stdout.splitlines():
                m = uuid_re.search(line)
                if m:
                    session_id = m.group(1)
                    break
        if session_id:
            cmd.extend(['--session-id', session_id])
    except Exception:
        pass

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("    ✓ openclaw agent --deliver succeeded")
            return True, "OK"
        else:
            err = (result.stderr or result.stdout or '').strip()[:200]
            print(f"    ✗ openclaw agent --deliver failed (exit {result.returncode}): {err}")
            return False, err
    except subprocess.TimeoutExpired:
        print("    ✗ openclaw agent --deliver timed out")
        return False, "timeout"
    except Exception as e:
        print(f"    ✗ openclaw agent --deliver error: {e}")
        return False, str(e)


# --- New config fields introduced in each version.
# Used by --reconfigure to detect and fill missing fields interactively.
CONFIG_MIGRATIONS = [
    {
        'version': '1.4.0',
        'field': 'auto_reply_mode',
        'security_critical': True,
        'default': 'false',
        'ask': (
            "Auto-reply mode — how should the agent handle replies to email senders?\n"
            "  false  — NEVER reply (recommended, safest)\n"
            "  ask    — ask YOU for explicit approval before replying\n"
            "  true   — agent decides whether to reply\n"
            "  WARNING: 'true' exposes that the system is active and may reveal\n"
            "  internal details to senders including spam/phishing sources.\n"
            "  Enter false/ask/true [false]: "
        ),
        'parse': lambda v: v.strip().lower() if v.strip().lower() in ('false', 'ask', 'true') else 'false',
    },
    {
        'version': '1.5.2',
        'field': 'openclaw_token',
        'security_critical': True,
        'default': None,
        'ask': (
            "OpenClaw gateway token — needed so the watcher (running as non-root user)\n"
            "  can authenticate when calling openclaw agent --deliver.\n"
            "  Found automatically from /root/.openclaw/openclaw.json if left blank.\n"
            "  Press Enter to auto-detect, or paste the token manually: "
        ),
        'parse': lambda v: v.strip() if v.strip() else (read_openclaw_gateway_token()[0]),
    },
]


def ask_auto_reply_mode():
    """Ask the user interactively for the auto_reply_mode setting.
    Returns 'false' (safe default) if input cannot be read (non-interactive).
    """
    if not sys.stdin.isatty():
        print("  ℹ Non-interactive mode — auto_reply_mode set to 'false' (recommended).")
        return 'false'

    print()
    print("  ⚠️  Auto-reply mode:")
    print("     How should the agent handle replies to email senders?")
    print()
    print("     false  — NEVER reply to senders (recommended, safest)")
    print("     ask    — ask YOU for explicit approval before each reply")
    print("     true   — agent decides whether to reply (least safe)")
    print()
    print("     WARNING: 'true' exposes that the system is active and may reveal")
    print("     internal details to senders, including spam and phishing sources.")
    print()
    answer = input("  auto_reply_mode [false/ask/true, default: false]: ").strip().lower()
    mode = answer if answer in ('false', 'ask', 'true') else 'false'
    labels = {
        'false': '✓ NEVER reply — agent will notify you via Telegram only.',
        'ask':   '✓ ASK mode — agent will request your approval before replying.',
        'true':  '⚠  AUTO mode — agent may reply to senders without asking.',
    }
    print(f"  {labels[mode]}")
    return mode


def reconfigure():
    """Detect missing config fields in the existing installation and add them interactively.

    Preserves all existing values. Only asks about fields that are absent.
    Intended to be run after a skill update: python3 setup.py --reconfigure
    """
    print("\n🔧 Reconfigure — checking for new config fields…\n")

    if not os.path.exists(CONFIG_PATH):
        print(f"  ✗ No config found at {CONFIG_PATH}")
        print("  Run a full install first: python3 setup.py <json-config>")
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    missing = [m for m in CONFIG_MIGRATIONS if m['field'] not in config]

    if not missing:
        print("  ✓ Config is up to date — no new fields to configure.")
        return

    print(f"  Found {len(missing)} new field(s) to configure:\n")

    for migration in missing:
        print(f"  [{migration['version']}] New field: {migration['field']}")
        if sys.stdin.isatty():
            raw = input(f"  {migration['ask']}")
            value = migration['parse'](raw) if raw.strip() else migration['default']
        else:
            print(f"  Non-interactive — using default: {migration['default']}")
            value = migration['default']
        config[migration['field']] = value
        print(f"  ✓ {migration['field']} = {value}\n")

    # Save updated config, preserving permissions
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_PATH, 0o600)
    print(f"  ✓ Config updated at {CONFIG_PATH}")
    print("  Restart the watcher to apply: systemctl restart imap-watcher")


def main():
    args = sys.argv

    # --deps mode
    if '--deps' in args:
        check_deps()
        return

    # --register-commands mode
    if '--register-commands' in args:
        ok = register_bee_commands()
        if ok:
            verify_bee_commands()
        return

    # --reconfigure mode
    if '--reconfigure' in args:
        reconfigure()
        return

    # --reply-status / --reply-off / --reply-ask / --reply-on
    # Called by the agent when the user sends a /beemail_reply* Telegram command
    if '--reply-status' in args:
        mode, err = get_auto_reply_mode()
        if err:
            print(f"  ✗ {err}")
            sys.exit(1)
        labels = {
            'false': '🔒 DISABLED — agent never replies to senders',
            'ask':   '❓ ASK — agent requests your approval before replying',
            'true':  '⚠️  ENABLED — agent may reply without asking',
            'not set': '⚠️  NOT SET — safe default (false) is active; run --reconfigure',
        }
        label = labels.get(mode, f"unknown ({mode})")
        print(f"  auto_reply_mode: {mode}  →  {label}")
        return

    for flag, mode in (('--reply-off', 'false'), ('--reply-ask', 'ask'), ('--reply-on', 'true')):
        if flag in args:
            if mode == 'true':
                print("  ⚠️  WARNING: enabling auto-reply exposes system activity to senders.")
                print("     This includes spam and phishing sources.")
            ok, msg = set_auto_reply_mode(mode)
            print(f"  {'✓' if ok else '✗'} {msg}")
            sys.exit(0 if ok else 1)

    # --show mode
    if '--show' in args:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                config = json.load(f)
            show_config(config)
        else:
            print(f"  No config found at {CONFIG_PATH}")
            print("  Pass a JSON config to show: setup.py --show '{{...}}'")
        return

    # --test mode
    if '--test' in args:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                config = json.load(f)
            run_test(config, label="Testing current")
        else:
            if sys.stdin.isatty():
                print("  No installed config found and no JSON provided.")
                print("  Usage:")
                print("    setup.py --test                  # test current config")
                print("    echo '{...}' | setup.py --test  # test provided config")
                sys.exit(1)
            config = load_config(args)
            config = validate_config(config)
            run_test(config, label="Testing provided")
        return

    # Full install mode
    print("╔══════════════════════════════════════╗")
    print("║   📨 Email Push — IMAP IDLE Setup   ║")
    print("╚══════════════════════════════════════╝")

    # Load and validate config
    if sys.stdin.isatty() and len(args) <= 1:
        print("  No config provided.")
        print("  Usage: echo '{...}' | setup.py")
        print("     or: setup.py '{...}'")
        sys.exit(1)
    config = load_config(args)
    config = validate_config(config)

    show_config(config, label="Installing")

    # Check existing installation
    if os.path.exists(CONFIG_PATH) and '--force' not in args:
        print(f"\n⚠️  Existing config found at {CONFIG_PATH} — updating")

    # Check deps first
    if not check_deps():
        print("  ✗ Fix missing dependencies and try again.")
        sys.exit(1)

    # Himalaya
    if not check_himalaya():
        if not install_himalaya():
            print("  ⚠️  himalaya not installed — agent won't be able to read emails")

    # Pre-install test
    print("\n🧪 Pre-install connection test…")
    if not run_test(config, label="Pre-install"):
        print("  ✗ Fix the issues above and try again. Nothing was installed.")
        sys.exit(1)

    # Python venv
    create_venv()

    # Save config
    save_config(config)

    # Install service (creates user, copies files, enables systemd)
    install_service()

    # Fix permissions (chown everything to watcher user)
    fix_permissions()

    # Verify
    ok = verify()

    # Register Telegram bot commands (non-critical — never fails the install)
    bot_ok = register_bee_commands()
    if bot_ok:
        verify_bee_commands()

    if ok:
        print("\n✅ Email Push setup complete!")
        print(f"   Config:    {CONFIG_PATH}")
        print(f"   Logs:      journalctl -u imap-watcher -f")
        print(f"   Status:    systemctl status imap-watcher")
        print(f"   Uninstall: bash {os.path.join(SKILL_DIR, 'scripts', 'uninstall.sh')}")
        if not bot_ok:
            print(f"\n   ⚠️  Bot commands were not registered — see instructions above")
        print(f"\n📧 Send a test email to {config['email']} to verify end-to-end.")
    else:
        print("\n⚠️  Setup finished but verification failed. Check logs above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
