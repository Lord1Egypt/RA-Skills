#!/usr/bin/env python3
"""HTTP REST bridge for agent-to-agent communication.

Agent A sends via POST /api/send.
Agent B reads via GET /api/inbox, replies via POST /api/reply.
Agent A reads replies via GET /api/recv.

Env vars (required):
  ACP_BRIDGE_TOKEN  — auth token. Server refuses to start without it.

Env vars (optional):
  ACP_BRIDGE_PORT   — listen port (default 18790)
  ACP_BRIDGE_DIR    — data directory (default /tmp/acp_bridge)
"""
import json, os, sys, time, fcntl
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

AUTH_TOKEN = os.environ.get("ACP_BRIDGE_TOKEN", "")
if not AUTH_TOKEN:
    print("FATAL: ACP_BRIDGE_TOKEN is required. Generate one: openssl rand -hex 16", file=sys.stderr, flush=True)
    sys.exit(1)

BRIDGE_DIR = Path(os.environ.get("ACP_BRIDGE_DIR", "/tmp/acp_bridge"))
BRIDGE_DIR.mkdir(exist_ok=True)
INBOX = BRIDGE_DIR / "inbox.jsonl"    # A → B
OUTBOX = BRIDGE_DIR / "outbox.jsonl"  # B → A


def append_jsonl(path, obj):
    with open(path, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(obj) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)


def read_jsonl(path, after_ts=0):
    msgs = []
    if path.exists():
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if msg.get("ts", 0) > after_ts:
                    msgs.append(msg)
    return msgs


class BridgeHandler(BaseHTTPRequestHandler):
    def check_auth(self):
        if not AUTH_TOKEN:
            return True  # no token configured = open (dev mode)
        auth = self.headers.get("Authorization", "")
        if auth != f"Bearer {AUTH_TOKEN}":
            self.send_error(401, "Unauthorized")
            return False
        return True

    def do_POST(self):
        if not self.check_auth():
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        text = body.get("message", "") or body.get("text", "")
        sender = body.get("from", "unknown")
        msg = {"id": int(time.time() * 1000), "ts": time.time(), "from": sender, "text": text}

        if self.path == "/api/send":
            append_jsonl(INBOX, msg)
            self.send_json({"ok": True, "id": msg["id"]})
        elif self.path == "/api/reply":
            append_jsonl(OUTBOX, msg)
            self.send_json({"ok": True, "id": msg["id"]})
        else:
            self.send_error(404)

    def do_GET(self):
        if not self.check_auth():
            return
        after = self._parse_after()

        if self.path.startswith("/api/inbox"):
            msgs = read_jsonl(INBOX, after)
            self.send_json({"messages": msgs, "count": len(msgs)})
        elif self.path.startswith("/api/recv"):
            msgs = read_jsonl(OUTBOX, after)
            self.send_json({"messages": msgs, "count": len(msgs)})
        elif self.path == "/api/health":
            self.send_json({"ok": True, "ts": time.time()})
        elif self.path == "/api/clear":
            for f in [INBOX, OUTBOX]:
                if f.exists():
                    f.unlink()
            self.send_json({"ok": True, "cleared": True})
        else:
            self.send_error(404)

    def _parse_after(self):
        if "?" not in self.path:
            return 0.0
        for param in self.path.split("?", 1)[1].split("&"):
            if param.startswith("after="):
                try:
                    return float(param.split("=", 1)[1])
                except ValueError:
                    pass
        return 0.0

    def send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # suppress access logs


if __name__ == "__main__":
    port = int(os.environ.get("ACP_BRIDGE_PORT", "18790"))
    server = HTTPServer(("0.0.0.0", port), BridgeHandler)
    print(f"ACP Bridge listening on :{port}", flush=True)
    server.serve_forever()
