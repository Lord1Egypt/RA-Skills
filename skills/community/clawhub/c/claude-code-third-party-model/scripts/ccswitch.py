#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccswitch - switch Claude Code between model profiles in one command.

Usage:
    ccswitch.py <profile>     switch to a profile (e.g. deepseek | spacebunny)
                              add --no-gateway to change settings only
    ccswitch.py status        show current profile + gateway state
    ccswitch.py list          list available profiles
    ccswitch.py gateway       just make sure the gateway is running (no switch)

How it works:
    A profile is a JSON file in ~/.claude/profiles/<name>.json that fully
    describes Claude Code's settings.json for that upstream. Switching =
    copy profile -> ~/.claude/settings.json, then reconcile the gateway:

      * profile whose ANTHROPIC_BASE_URL points at 127.0.0.1:<gateway port>
        => local ccproxy gateway MUST be running -> start if down
      * any other profile (native Anthropic endpoint, e.g. DeepSeek)
        => gateway is not needed -> stop it to keep things clean

    The gateway child process is launched with proxy environment variables
    cleared and NO_PROXY set to the loopback addresses it serves, so the
    gateway always talks to its upstream directly.
"""

import json
import os
import secrets
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------- constants
HOME = Path(os.path.expanduser("~"))
CLAUDE_DIR = HOME / ".claude"
SETTINGS = CLAUDE_DIR / "settings.json"
PROFILES_DIR = CLAUDE_DIR / "profiles"
BACKUP_DIR = CLAUDE_DIR / "backups"

# Gateway = our own zero-dependency translation proxy (see ccproxy.py).
# History: claude-code-router 2.1.1 was tried first, but it emits malformed
# Anthropic SSE (every event duplicated, message_stop never sent), which made
# Claude Code report "The response stream was malformed". npm carries only
# 2.1.0/2.1.1 (no fix), so it was replaced by ccproxy.py.
#
# ccproxy.py is looked up next to this script first (repo layout), then one
# level up, then $HOME (flat layout). No hardcoded absolute paths anywhere,
# so a clone works on any machine.
_HERE = Path(__file__).resolve().parent


def _find_ccproxy():
    for cand in (_HERE / "ccproxy.py", _HERE.parent / "ccproxy.py", HOME / "ccproxy.py"):
        if cand.exists():
            return cand.resolve()
    return _HERE / "ccproxy.py"


CCPROXY = _find_ccproxy()
# Use the very interpreter running this script: always present, never a
# hardcoded path, and it keeps working inside virtualenvs.
PY_EXE = Path(sys.executable) if sys.executable else None
GATEWAY_LOG = HOME / ".claude-code-proxy.log"
GATEWAY_PIDFILE = HOME / ".claude-code-proxy.pid"
CCPROXY_CONFIG = HOME / ".claude-code-proxy.json"

# Gateway client tokens that are considered "not set" and must be replaced by a
# generated secret, so no local process can use the gateway unauthenticated.
PLACEHOLDER_TOKENS = {"", "router-local", "local", "changeme", "your-token"}

GW_HOST = "127.0.0.1"
GW_PORT = 3457

ALIASES = {
    "ds": "deepseek",
    "deepseek-flash": "deepseek",
    "bunny": "spacebunny",
    "sb": "spacebunny",
    "space-bunny": "spacebunny",
    "zen": "spacebunny",
    "opencode-zen": "spacebunny",
}

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
# Breakaway keeps the gateway alive after the launcher exits (otherwise it can
# be torn down together with the parent process), leaving Claude Code pointed
# at a dead port. DETACHED_PROCESS covers plain console launches.
DETACHED = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_BREAKAWAY_FROM_JOB

# ------------------------------------------------------------------- output
def out(msg=""):
    print(msg)


def die(msg, code=1):
    out("ERROR: " + msg)
    sys.exit(code)


# ------------------------------------------------------------------ helpers
def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def canonical(name):
    n = (name or "").strip().lower()
    return ALIASES.get(n, n)


def list_profiles():
    if not PROFILES_DIR.is_dir():
        return []
    return sorted(p.stem for p in PROFILES_DIR.glob("*.json"))


def profile_path(name):
    return PROFILES_DIR / (name + ".json")


def same_json(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def current_profile():
    """Return profile name matching current settings.json, else None."""
    if not SETTINGS.exists():
        return None
    try:
        cur = read_json(SETTINGS)
    except Exception:
        return None
    for name in list_profiles():
        try:
            if same_json(cur, read_json(profile_path(name))):
                return name
        except Exception:
            continue
    return None


def port_open(host=GW_HOST, port=GW_PORT, timeout=0.6):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def gateway_pid():
    """PID of the process listening on the gateway port, or None."""
    if os.name == "nt":
        try:
            cp = subprocess.run(["netstat", "-ano", "-p", "TCP"],
                                capture_output=True, text=True, timeout=15)
        except Exception:
            return None
        for line in cp.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 5 and parts[0].upper() == "TCP" and "LISTENING" in line.upper():
                local = parts[1]
                if local.endswith(":" + str(GW_PORT)):
                    return parts[-1]
        return None
    # POSIX: we recorded the pid at spawn time; verify it is still alive.
    try:
        pid = int(GATEWAY_PIDFILE.read_text(encoding="utf-8").strip())
        os.kill(pid, 0)
        return str(pid)
    except Exception:
        return None


def _clear_pidfile():
    try:
        GATEWAY_PIDFILE.unlink()
    except OSError:
        pass


def stop_gateway():
    pid = gateway_pid()
    if not pid:
        return False
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/PID", pid],
                       capture_output=True, text=True)
    else:
        try:
            os.kill(int(pid), signal.SIGTERM)
        except OSError:
            pass
    for _ in range(20):
        if not port_open():
            _clear_pidfile()
            return True
        time.sleep(0.25)
    _clear_pidfile()
    return not port_open()


def _read_gateway_config():
    try:
        return read_json(CCPROXY_CONFIG)
    except Exception:
        return {}


def shared_token():
    """The gateway's client token, or "" if none has been minted yet."""
    return str(_read_gateway_config().get("client_token") or "").strip()


def ensure_shared_token():
    """Give the gateway a real secret and make Claude Code send the same one.

    The gateway refuses requests that do not carry this token, so another local
    process cannot quietly spend the upstream credential. Returns the token.
    """
    cfg = _read_gateway_config()
    token = str(cfg.get("client_token") or "").strip()
    if token in PLACEHOLDER_TOKENS:
        token = secrets.token_urlsafe(24)
        cfg["client_token"] = token
        write_json(CCPROXY_CONFIG, cfg)
        out("Gateway   : minted a client token -> %s" % CCPROXY_CONFIG)

    # Claude Code sends x-api-key: keep it identical to the gateway's token.
    for path in _gateway_settings_paths():
        try:
            data = read_json(path)
        except Exception:
            continue
        if path != SETTINGS and not needs_gateway(data):
            continue
        env = data.setdefault("env", {})
        if str(env.get("ANTHROPIC_AUTH_TOKEN") or "").strip() in PLACEHOLDER_TOKENS:
            env["ANTHROPIC_AUTH_TOKEN"] = token
            write_json(path, data)
    return token


def _gateway_settings_paths():
    """settings.json plus every profile that points at the local gateway."""
    return [SETTINGS] + [profile_path(n) for n in list_profiles()]


def start_gateway():
    if PY_EXE is None or not PY_EXE.exists():
        die("cannot locate a python interpreter (sys.executable is empty)")
    if not CCPROXY.exists():
        die("ccproxy.py not found: " + str(CCPROXY))
    ensure_shared_token()
    GATEWAY_LOG.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
              "ALL_PROXY", "all_proxy"):
        env.pop(k, None)
    env["NO_PROXY"] = "127.0.0.1,localhost"
    env["no_proxy"] = "127.0.0.1,localhost"
    argv = [str(PY_EXE), str(CCPROXY), "--port", str(GW_PORT)]
    log = open(GATEWAY_LOG, "ab", buffering=0)
    kw = dict(cwd=str(CCPROXY.parent), stdin=subprocess.DEVNULL,
              stdout=log, stderr=log, env=env, close_fds=True)
    if os.name == "nt":
        # Keep the gateway running after this launcher exits, so Claude Code
        # is never left pointing at a dead port.
        try:
            proc = subprocess.Popen(argv, creationflags=DETACHED, **kw)
        except OSError:
            proc = subprocess.Popen(
                argv, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP, **kw)
    else:
        # New session == detached from our process group, same effect.
        proc = subprocess.Popen(argv, start_new_session=True, **kw)
    try:
        GATEWAY_PIDFILE.write_text(str(proc.pid), encoding="utf-8")
    except OSError:
        pass


def direct_opener():
    """urllib opener with no proxy handler, for 127.0.0.1 health checks."""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def wait_health(timeout=25.0):
    """Poll the gateway until it answers, return (ok, detail).

    The reply must identify itself as ccproxy (and accept our token), so a
    different program that happens to hold the port is reported rather than
    trusted -- otherwise it could collect prompts meant for the real gateway.
    """
    op = direct_opener()
    token = shared_token()
    req = urllib.request.Request("http://%s:%d/health" % (GW_HOST, GW_PORT))
    if token:
        req.add_header("x-api-key", token)
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        try:
            with op.open(req, timeout=3) as r:
                body = r.read().decode("utf-8", "replace")
                try:
                    info = json.loads(body)
                except Exception:
                    info = {}
                if info.get("service") != "ccproxy":
                    return False, "port %d is held by another process" % GW_PORT
                return True, "HTTP %d" % r.status
        except urllib.error.HTTPError as e:
            if e.code == 401:
                return False, ("gateway rejected our token - restart it with "
                               "`ccswitch gateway` to re-sync")
            return False, "HTTP %d" % e.code
        except Exception as e:
            last = str(e)
        time.sleep(0.4)
    return False, last or "timeout"


def needs_gateway(cfg):
    url = str((cfg.get("env") or {}).get("ANTHROPIC_BASE_URL", ""))
    return ("127.0.0.1:%d" % GW_PORT) in url or ("localhost:%d" % GW_PORT) in url


def backup_settings():
    if not SETTINGS.exists():
        return None
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = BACKUP_DIR / ("settings.json.bak-%s" % ts)
    shutil.copy2(SETTINGS, dest)
    return dest


def ensure_gateway(cfg):
    """Reconcile gateway state with what the profile needs. Returns note str."""
    want = needs_gateway(cfg)
    if want:
        ensure_shared_token()
        if port_open():
            ok, detail = wait_health(8)
            if ok:
                return "gateway already running (%s)" % detail
            # Do not kill an unknown listener: report it and let the user decide.
            return ("port %d unusable: %s - stop what holds it, then run "
                    "`ccswitch gateway`" % (GW_PORT, detail))
        start_gateway()
        ok, detail = wait_health(25)
        if not ok:
            return "gateway FAILED to start -> see %s (%s)" % (GATEWAY_LOG, detail)
        return "gateway started -> %s" % detail
    else:
        if port_open():
            stop_gateway()
            return "gateway stopped (not needed)"
        return "gateway not needed (left off)"


# ------------------------------------------------------------------ commands
def cmd_list():
    cur = current_profile()
    names = list_profiles()
    out("Available profiles (%s):" % PROFILES_DIR)
    if not names:
        out("  (none) - create %s/<name>.json" % PROFILES_DIR)
    for n in names:
        mark = " * active" if n == cur else ""
        url = ""
        try:
            url = (read_json(profile_path(n)).get("env") or {}).get("ANTHROPIC_BASE_URL", "")
        except Exception:
            pass
        out("  %-12s -> %s%s" % (n, url, mark))
    if cur is None and SETTINGS.exists():
        out("  (settings.json does not match any profile)")


def cmd_status():
    names = list_profiles()
    cur = current_profile()
    if cur:
        out("Profile   : %s" % cur)
    elif SETTINGS.exists():
        out("Profile   : (custom / unmatched)")
    else:
        out("Profile   : (no settings.json)")
    cfg = {}
    if SETTINGS.exists():
        try:
            cfg = read_json(SETTINGS)
        except Exception as e:
            out("settings  : UNREADABLE (%s)" % e)
    env = cfg.get("env") or {}
    out("Base URL  : %s" % env.get("ANTHROPIC_BASE_URL", "(unset)"))
    out("Model     : %s" % cfg.get("model", "(unset)"))
    want = needs_gateway(cfg)
    running = port_open()
    out("Gateway   : %s (port %d)" % ("RUNNING" if running else "stopped", GW_PORT))
    if want and not running:
        out("            !! this profile NEEDS the gateway -> run: ccswitch gateway")
    if running and not want:
        out("            (running but not needed by this profile)")
    if running:
        pid = gateway_pid()
        if pid:
            out("Gateway PID: %s" % pid)
    out("Profiles  : %s" % (", ".join(names) if names else "(none)"))


def cmd_switch(arg, no_gateway=False):
    name = canonical(arg)
    if not name:
        die("missing profile name")
    path = profile_path(name)
    if not path.exists():
        avail = ", ".join(list_profiles()) or "(none)"
        die("unknown profile '%s'. available: %s" % (arg, avail))

    cfg = read_json(path)
    prev = current_profile()

    if prev == name:
        out("Already on '%s' - reconciling gateway." % name)
    else:
        bak = backup_settings()
        if bak:
            out("Backed up current settings -> %s" % bak.name)
        write_json(SETTINGS, cfg)
        out("Settings switched: %s -> %s" % (prev or "(custom)", name))

    if no_gateway:
        out("Gateway   : left untouched (--no-gateway)")
    else:
        note = ensure_gateway(cfg)
        out("Gateway   : %s" % note)
    env = cfg.get("env") or {}
    out("Base URL  : %s" % env.get("ANTHROPIC_BASE_URL", "(unset)"))
    out("Model     : %s" % cfg.get("model", "(unset)"))
    out("")
    out("NOTE: already-running Claude Code sessions keep the OLD settings.")
    out("      Restart `claude` to pick this up.")
    if needs_gateway(cfg) and not port_open():
        out("      Gateway is NOT running -> run: ccswitch gateway")


def cmd_gateway():
    if port_open():
        ok, detail = wait_health(8)
        if ok:
            out("Gateway   : already running (%s)" % detail)
            return
        die("port %d is not served by ccproxy: %s - stop that process first"
            % (GW_PORT, detail))
    start_gateway()
    ok, detail = wait_health(25)
    if ok:
        out("Gateway   : started -> %s" % detail)
    else:
        die("gateway failed to start -> see %s" % GATEWAY_LOG)


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    raw = argv[1:]
    no_gateway = any(a in ("--no-gateway", "-n") for a in raw)
    args = [a for a in raw if not a.startswith("-")]
    if not args:
        if any(a in ("-h", "--help", "help") for a in raw):
            out(__doc__.strip())
        else:
            cmd_status()
        return 0
    cmd = args[0].lower()
    if cmd in ("status", "s", "current"):
        cmd_status()
    elif cmd in ("list", "ls"):
        cmd_list()
    elif cmd in ("gateway", "gw", "up"):
        cmd_gateway()
    elif cmd == "help":
        out(__doc__.strip())
    else:
        cmd_switch(args[0], no_gateway=no_gateway)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(130)
