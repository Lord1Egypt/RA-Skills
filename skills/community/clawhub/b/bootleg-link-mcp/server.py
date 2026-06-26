#!/usr/bin/env python3
"""
Bootleg-Link MCP Server v0.9 — thin proxy to daemon.
All download logic lives in daemon.py (standalone background process).
"""
import sys, json, os, time, threading, urllib.request, urllib.parse
from collections import deque

DAEMON_URL = "http://127.0.0.1:8765"
DAEMON_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daemon.py")
PYTHON = sys.executable

# ── Auto-start daemon ───────────────────────────────────
def _ensure_daemon():
    """Start daemon if not running. Uses systemd on Linux, direct spawn on others."""
    # Quick health check first
    try:
        urllib.request.urlopen(f"{DAEMON_URL}/health", timeout=0.5)
        return True
    except: pass

    if os.name == 'nt':
        import subprocess
        subprocess.Popen([PYTHON, DAEMON_SCRIPT],
                       creationflags=0x00000008 if hasattr(subprocess, 'DETACHED_PROCESS') else 0,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif os.name == 'posix':
        # Try systemctl first, fallback to direct spawn
        import subprocess
        r = subprocess.run(["systemctl","--user","start","bootleg-daemon.service"],
                         capture_output=True, timeout=5)
        if r.returncode != 0:
            # Merge PATH with nvm/bun to ensure JS runtimes for yt-dlp
            env = os.environ.copy()
            extra_paths = [
                os.path.expanduser("~/.bun/bin"),
                os.path.expanduser("~/.nvm/versions/node/v24.16.0/bin"),
            ]
            current = env.get("PATH", "")
            for p in extra_paths:
                if os.path.isdir(p) and p not in current:
                    current = p + ":" + current
            env["PATH"] = current
            subprocess.Popen([PYTHON, DAEMON_SCRIPT, "--no-daemon"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           start_new_session=True, env=env)

    # Wait for daemon to become healthy
    for _ in range(10):
        try:
            urllib.request.urlopen(f"{DAEMON_URL}/health", timeout=0.5)
            return True
        except: pass
        time.sleep(0.5)
    return False

_ensure_daemon()

def _api(method, path, body=None):
    """Call daemon HTTP API. Auto-restarts daemon on connection failure."""
    for attempt in range(2):
        try:
            data = json.dumps(body).encode() if body else None
            req = urllib.request.Request(f"{DAEMON_URL}{path}", data=data, method=method)
            req.add_header("Content-Type", "application/json") if data else None
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt == 0:
                _ensure_daemon()  # try restart once, then retry
            else:
                return {"error": str(e)[:200]}

# ── Tool name → (HTTP method, path, body_builder) ────────
ROUTES = {
    "submit_download_task": ("POST", "/submit", lambda a: {
        "url": a.get("url",""), "quality": a.get("quality","320"),
        "outputDir": a.get("outputDir","")}),
    "download_single":     ("POST", "/submit", lambda a: {
        "url": a.get("url",""), "quality": a.get("quality","320"),
        "outputDir": a.get("outputDir","")}),
    "query_progress":      ("GET",  "/progress", lambda a: {"taskId": a.get("taskId","")}),
    "list_tasks":          ("GET",  "/tasks",    lambda a: {"status": a.get("status","all"), "limit": a.get("limit",50)}),
    "cancel_task":         ("POST", "/cancel",   lambda a: {"taskId": a.get("taskId","")}),
    "clear_completed":     ("POST", "/clear",    lambda a: {}),
    "clear_database":      ("POST", "/clear-all",lambda a: {}),
    "get_queue_status":    ("GET",  "/queue",    lambda a: {}),
    "youtube_login":       ("POST", "/login",    lambda a: {"email": a.get("email",""), "password": a.get("password","")}),
    "youtube_auth_status": ("GET",  "/auth",     lambda a: {}),
    "youtube_logout":      ("POST", "/logout",   lambda a: {}),
    # Qobuz / Beatport — pass through to daemon
    "qobuz_login":         ("POST", "/qobuz/login",    lambda a: {"email": a.get("email",""), "password": a.get("password","")}),
    "qobuz_search":        ("GET",  "/qobuz/search",   lambda a: {"query": a.get("query",""), "type": a.get("type","track"), "limit": a.get("limit",10)}),
    "qobuz_download":      ("POST", "/qobuz/download", lambda a: {"trackId": a.get("trackId",""), "quality": a.get("quality",6), "outputDir": a.get("outputDir","")}),
    "qobuz_my_purchases":  ("GET",  "/qobuz/purchases",lambda a: {"limit": a.get("limit",20)}),
    "beatport_login":      ("POST", "/beatport/login",  lambda a: {"email": a.get("email",""), "password": a.get("password","")}),
    "beatport_search":     ("GET",  "/beatport/search", lambda a: {"query": a.get("query",""), "limit": a.get("limit",10)}),
    "beatport_download":   ("POST", "/beatport/download",lambda a: {"url": a.get("url",""), "outputDir": a.get("outputDir","")}),
}

TOOLS = [
    {"name":"submit_download_task","description":"Submit a YouTube download task (batch/queue)",
     "inputSchema":{"type":"object","properties":{"url":{"type":"string","description":"YouTube URL"},"quality":{"type":"string","default":"320"},"outputDir":{"type":"string","description":"Output directory"}},"required":["url"]}},
    {"name":"download_single","description":"Download a single YouTube video (non-blocking, returns task ID immediately)",
     "inputSchema":{"type":"object","properties":{"url":{"type":"string","description":"YouTube video URL or search query"},"quality":{"type":"string","default":"320"},"outputDir":{"type":"string","description":"Output directory"}},"required":["url"]}},
    {"name":"query_progress","description":"Query task progress",
     "inputSchema":{"type":"object","properties":{"taskId":{"type":"string","description":"Task ID"}},"required":["taskId"]}},
    {"name":"list_tasks","description":"List all tasks",
     "inputSchema":{"type":"object","properties":{"status":{"type":"string","default":"all"}},"required":[]}},
    {"name":"cancel_task","description":"Cancel a task",
     "inputSchema":{"type":"object","properties":{"taskId":{"type":"string","description":"Task ID"}},"required":["taskId"]}},
    {"name":"clear_completed","description":"Clear completed tasks",
     "inputSchema":{"type":"object","properties":{},"required":[]}},
    {"name":"clear_database","description":"Clear ALL tasks and videos from database",
     "inputSchema":{"type":"object","properties":{},"required":[]}},
    {"name":"get_queue_status","description":"Get queue status",
     "inputSchema":{"type":"object","properties":{},"required":[]}},
    {"name":"youtube_login","description":"Login to YouTube via Google account (headless browser automation). Check your phone for 2FA prompt.",
     "inputSchema":{"type":"object","properties":{"email":{"type":"string","description":"Google account email"},"password":{"type":"string","description":"Google account password"}},"required":["email","password"]}},
    {"name":"youtube_auth_status","description":"Check YouTube authentication status (cookies)",
     "inputSchema":{"type":"object","properties":{},"required":[]}},
    {"name":"youtube_logout","description":"Logout from YouTube (clear cookies)",
     "inputSchema":{"type":"object","properties":{},"required":[]}},
    {"name":"qobuz_login","description":"Login to Qobuz with email and password",
     "inputSchema":{"type":"object","properties":{"email":{"type":"string","description":"Qobuz account email"},"password":{"type":"string","description":"Qobuz account password"}},"required":["email","password"]}},
    {"name":"qobuz_search","description":"Search Qobuz for tracks, albums, or artists",
     "inputSchema":{"type":"object","properties":{"query":{"type":"string","description":"Search query"},"type":{"type":"string","enum":["track","album","artist"],"default":"track"},"limit":{"type":"integer","default":"10"}},"required":["query"]}},
    {"name":"qobuz_download","description":"Download a track from Qobuz by ID or URL",
     "inputSchema":{"type":"object","properties":{"trackId":{"type":"string","description":"Track ID or URL"},"quality":{"type":"integer","description":"5=MP3 320, 6=CD FLAC, 7=Hi-Res 96k, 27=Hi-Res 192k","default":6},"outputDir":{"type":"string","description":"Output directory"}},"required":["trackId"]}},
    {"name":"qobuz_my_purchases","description":"List your purchased/favorite tracks from Qobuz",
     "inputSchema":{"type":"object","properties":{"limit":{"type":"integer","default":"20"}},"required":[]}},
    {"name":"beatport_login","description":"Login to Beatport via browser automation (Playwright)",
     "inputSchema":{"type":"object","properties":{"email":{"type":"string","description":"Beatport account email"},"password":{"type":"string","description":"Beatport account password"}},"required":["email","password"]}},
    {"name":"beatport_search","description":"Search Beatport for tracks",
     "inputSchema":{"type":"object","properties":{"query":{"type":"string","description":"Search query"},"limit":{"type":"integer","default":"10"}},"required":["query"]}},
    {"name":"beatport_download","description":"Download a track from Beatport by URL (must own it)",
     "inputSchema":{"type":"object","properties":{"url":{"type":"string","description":"Beatport track/release URL"},"outputDir":{"type":"string","description":"Output directory"}},"required":["url"]}},
]

# ── MCP JSON-RPC ────────────────────────────────────────
req_q = deque()
readers = threading.Condition()

def send(m):
    sys.stdout.write(json.dumps(m) + "\n")
    sys.stdout.flush()

def read_stdin():
    for line in sys.stdin.buffer:
        line = line.rstrip(b'\r\n')
        if not line: continue
        try:
            msg = json.loads(line.decode("utf-8", errors="replace"))
            with readers:
                req_q.append(msg)
                readers.notify_all()
        except json.JSONDecodeError: pass

stdin_thread = threading.Thread(target=read_stdin, daemon=True)
stdin_thread.start()

def handle(msg):
    rid = msg.get("id"); m = msg.get("method",""); r = None
    try:
        if m == "initialize":
            send({"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2024-11-05",
                "serverInfo":{"name":"bootleg-link-mcp","version":"0.9"},
                "capabilities":{"tools":{}}}})
            return
        elif m == "tools/list":
            send({"jsonrpc":"2.0","id":rid,"result":{"tools":TOOLS}})
            return
        elif m == "tools/call":
            p = msg.get("params",{}); tname = p.get("name",""); a = p.get("arguments",{})
            if tname not in ROUTES:
                send({"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":f"Unknown tool: {tname}"}})
                return
            method, path, builder = ROUTES[tname]
            body = builder(a)
            if method == "GET":
                qs = urllib.parse.urlencode({k: v for k, v in body.items() if v})
                result = _api("GET", f"{path}?{qs}")
            else:
                result = _api("POST", path, body)
            r = {"content":[{"type":"text","text":json.dumps(result)}]}
        elif m == "shutdown":
            send({"jsonrpc":"2.0","id":rid,"result":None})
            sys.exit(0)
        else:
            send({"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":f"Unknown method: {m}"}})
        if r is not None:
            send({"jsonrpc":"2.0","id":rid,"result":r})
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        send({"jsonrpc":"2.0","id":rid,"error":{"code":-32603,"message":str(e)[:200]}})

import traceback
while True:
    with readers:
        while not req_q:
            readers.wait(timeout=0.5)
        msg = req_q.popleft()
    handle(msg)
