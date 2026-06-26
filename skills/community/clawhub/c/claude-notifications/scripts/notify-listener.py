#!/usr/bin/env python3
"""Local HTTP listener for devpod notifications via SSH reverse tunnel.
Receives POST requests on port 19876 and calls terminal-notifier.
Started automatically via launchd on macOS."""

import json
import os
import shutil
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 19876
# Replaced by setup script with actual path; falls back to shutil.which
_CONFIGURED_PATH = "__TERMINAL_NOTIFIER_PATH__"
TERMINAL_NOTIFIER = (
    _CONFIGURED_PATH if os.path.isfile(_CONFIGURED_PATH)
    else shutil.which("terminal-notifier") or _CONFIGURED_PATH
)


MAX_BODY = 4096


class NotifyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > MAX_BODY:
                self.send_response(413)
                self.end_headers()
                return

            data = json.loads(self.rfile.read(length)) if length else {}

            message = data.get("message", "Claude Code needs attention")
            title = data.get("title", "Claude Code")
            sound = data.get("sound", "Glass")
            bundle_id = data.get("bundle_id")

            cmd = [TERMINAL_NOTIFIER,
                   "-message", message,
                   "-title", title,
                   "-sound", sound]
            if bundle_id:
                cmd.extend(["-activate", bundle_id])

            result = subprocess.run(cmd, timeout=5, capture_output=True)
            if result.returncode != 0:
                print(f"terminal-notifier failed: {result.stderr.decode()}", file=sys.stderr, flush=True)
                self.send_response(500)
            else:
                self.send_response(200)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr, flush=True)
            self.send_response(500)

        self.end_headers()

    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    if not os.path.isfile(TERMINAL_NOTIFIER):
        sys.exit(f"terminal-notifier not found at: {TERMINAL_NOTIFIER}. Run setup-notifications.sh first.")
    server = HTTPServer(("127.0.0.1", PORT), NotifyHandler)
    print(f"Notify listener running on 127.0.0.1:{PORT} (notifier: {TERMINAL_NOTIFIER})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
