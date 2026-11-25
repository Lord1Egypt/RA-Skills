#!/usr/bin/env python3
"""
setup_auth.py — Get both Apple Music tokens in one step.

  1. Developer token: reuses APPLE_MUSIC_DEV_TOKEN if it still has 14+ days left, otherwise signs
     a new one from your MusicKit key (--key-id/--team-id/--key-path, the APPLE_KEY_ID /
     APPLE_TEAM_ID / APPLE_PRIVATE_KEY_PATH variables, or prompts). Needs PyJWT + cryptography.
  2. Music User Token: opens a page on 127.0.0.1 in your browser; you click "Connect Apple Music"
     and sign in with Apple, and the page hands the token back to this script.
  3. Prints the `export` lines (or, with --env-file, writes them to an owner-only file).

Run it yourself in a terminal: it opens a browser and prints your tokens. Nothing is sent
anywhere except Apple's own sign-in; the local page is served only to this machine, behind a
random one-time URL, and the server stops as soon as the token arrives (or after --timeout).

Usage:
  python3 scripts/setup_auth.py [--key-id ID --team-id ID --key-path AuthKey.p8]
                                [--env-file PATH] [--no-browser] [--timeout 300]
  python3 scripts/setup_auth.py status      # how long the current tokens have left
"""

import sys
if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import contextlib
import html
import json
import os
import secrets
import shlex
import threading
import webbrowser
import socketserver
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from _common import check_token_expiry, check_user_token_age, record_user_token, write_private
from generate_dev_token import TokenError, make_dev_token


class LoopbackHTTPServer(ThreadingHTTPServer):
    """ThreadingHTTPServer without HTTPServer.server_bind's socket.getfqdn() reverse-DNS lookup.

    The server only binds 127.0.0.1, and on some macOS setups that lookup hangs ~35 s before failing.
    """

    def server_bind(self):
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]


MUSICKIT_JS = "https://js-cdn.music.apple.com/musickit/v3/musickit.js"
MAX_TOKEN_BYTES = 8192

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Connect Apple Music · Apple Music DJ</title>
<style>
  :root {{ color-scheme: light dark; --bg:#f5f5f7; --card:#fff; --fg:#1d1d1f; --muted:#6e6e73; --accent:#fa2d48; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --bg:#000; --card:#1c1c1e; --fg:#f5f5f7; --muted:#a1a1a6; }} }}
  body {{ margin:0; min-height:100vh; display:grid; place-items:center; background:var(--bg); color:var(--fg);
         font:16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; padding:16px; box-sizing:border-box; }}
  main {{ background:var(--card); border-radius:18px; padding:32px; max-width:420px; text-align:center;
          box-shadow:0 8px 30px rgba(0,0,0,.08); }}
  h1 {{ font-size:22px; margin:8px 0; }} p {{ color:var(--muted); }}
  button {{ background:var(--accent); color:#fff; border:0; border-radius:999px; padding:12px 28px; font-size:16px;
            font-weight:600; cursor:pointer; }} button:disabled {{ opacity:.5; cursor:default; }}
  #status {{ min-height:1.5em; margin-top:16px; }}
</style></head>
<body><main>
  <div style="font-size:40px">🎧</div>
  <h1>Connect Apple Music</h1>
  <p>Sign in with your Apple ID so {app} can read your listening history. Your token goes only to the
     setup script running on this computer.</p>
  <button id="go" disabled>Loading MusicKit…</button>
  <div id="status" role="status"></div>
</main>
<script>
  const DEV_TOKEN = {dev_token};
  const go = document.getElementById("go"), status = document.getElementById("status");
  const say = (msg) => {{ status.textContent = msg; }};
  setTimeout(() => {{ if (go.disabled && !status.textContent)
    say("Couldn't load MusicKit from Apple (js-cdn.music.apple.com). Check your connection or content blocker, then reload."); }}, 15000);
  document.addEventListener("musickitloaded", async () => {{
    try {{
      await MusicKit.configure({{ developerToken: DEV_TOKEN, app: {{ name: "Apple Music DJ", build: "{version}" }} }});
      go.disabled = false; go.textContent = "Connect Apple Music";
    }} catch (e) {{ say("MusicKit didn't accept the developer token: " + e); }}
  }});
  go.addEventListener("click", async () => {{
    go.disabled = true; say("Waiting for Apple sign-in…");
    try {{
      const userToken = await MusicKit.getInstance().authorize();
      const r = await fetch("token", {{ method: "POST", headers: {{ "Content-Type": "application/json" }},
                                        body: JSON.stringify({{ token: userToken }}) }});
      say(r.ok ? "✅ Connected. You can close this tab and go back to the terminal." : "Something went wrong (" + r.status + ").");
    }} catch (e) {{ go.disabled = false; say("Sign-in didn't finish: " + e); }}
  }});
</script>
<script src="{musickit}" async></script>
</body></html>
"""


def render_page(dev_token: str, version: str = "3") -> bytes:
    # json.dumps makes a JS string literal; escaping "<" keeps "</script>" from closing the tag
    token_js = json.dumps(dev_token).replace("<", "\\u003c")
    return PAGE.format(app="Apple Music DJ", dev_token=token_js, version=html.escape(version),
                       musickit=MUSICKIT_JS).encode()


class TokenCatcher:
    """A one-shot server on 127.0.0.1 that serves the sign-in page and receives the user token.

    Only requests for the random one-time path, with a loopback Host header (no DNS rebinding) and,
    for the POST, a same-origin Origin header, are answered. The first valid token wins.
    """

    def __init__(self, dev_token: str, port: int = 0):
        # A one-time path segment, so only the browser tab we open (or the user pastes) finds the page
        self.nonce = secrets.token_urlsafe(24)
        self.page = render_page(dev_token)
        self.token: str | None = None
        self.done = threading.Event()
        self._lock = threading.Lock()  # the server is threaded; two POSTs must not both "win"
        catcher = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _reply(self, status: int, body: bytes = b"", ctype: str = "text/plain; charset=utf-8"):
                self.send_response(status)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("Referrer-Policy", "no-referrer")
                self.end_headers()
                self.wfile.write(body)

            def _host_ok(self) -> bool:
                return self.headers.get("Host", "") in catcher.hosts

            def do_GET(self):
                if self._host_ok() and self.path == f"/{catcher.nonce}/":
                    self._reply(200, catcher.page, "text/html; charset=utf-8")
                else:
                    self._reply(404, b"not found")

            def do_POST(self):
                status, body = catcher.accept(self)
                self._reply(status, body)

        self._server = LoopbackHTTPServer(("127.0.0.1", port), Handler)
        bound = self._server.server_address[1]
        self.hosts = {f"127.0.0.1:{bound}", f"localhost:{bound}"}
        self.origins = {f"http://{h}" for h in self.hosts}
        self.url = f"http://127.0.0.1:{bound}/{self.nonce}/"

    def accept(self, req: BaseHTTPRequestHandler) -> tuple[int, bytes]:
        """Validate a token POST; the first valid token wins."""
        if (req.headers.get("Host", "") not in self.hosts or req.path != f"/{self.nonce}/token"
                or req.headers.get("Origin") not in self.origins):
            return 403, b"forbidden"
        length = int(req.headers.get("Content-Length") or 0)
        if not 0 < length <= MAX_TOKEN_BYTES:
            return 400, b"bad request"
        try:
            token = json.loads(req.rfile.read(length)).get("token")
        except (ValueError, AttributeError):
            token = None
        if not isinstance(token, str) or not token.strip() or any(c.isspace() for c in token):
            return 400, b"no token"
        with self._lock:
            if not self.done.is_set():
                self.token = token
                self.done.set()
        return 200, b"ok"

    def start(self) -> "TokenCatcher":
        # A short poll interval keeps stop() fast: shutdown() waits for the next poll (default 0.5 s).
        threading.Thread(target=self._server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True).start()
        return self

    def wait(self, timeout: float) -> str | None:
        self.done.wait(timeout)
        return self.token

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()


# ── Developer token ──────────────────────────────────────────────

def _ask(label: str) -> str:
    if not sys.stdin.isatty():
        return ""
    return input(f"  {label}: ").strip()


def get_dev_token(args) -> str:
    existing = os.environ.get("APPLE_MUSIC_DEV_TOKEN", "")
    if existing and not args.new_dev_token:
        status = check_token_expiry()
        if status and not status["warning"]:
            print(f"1/2  Developer token: reusing the one in APPLE_MUSIC_DEV_TOKEN ({status['days_remaining']} days left).",
                  file=sys.stderr)
            return existing
    print("1/2  Developer token: signing a new one with your MusicKit key.", file=sys.stderr)
    print("     (Apple Developer → Keys → a key with Media Services; see references/auth-setup.md)", file=sys.stderr)
    key_id = args.key_id or os.environ.get("APPLE_KEY_ID") or _ask("Key ID (10 characters)")
    team_id = args.team_id or os.environ.get("APPLE_TEAM_ID") or _ask("Team ID (10 characters)")
    key_path = args.key_path or os.environ.get("APPLE_PRIVATE_KEY_PATH") or _ask("Path to AuthKey_XXXX.p8")
    missing = [n for n, v in (("--key-id", key_id), ("--team-id", team_id), ("--key-path", key_path)) if not v]
    if missing:
        raise TokenError(f"Missing {', '.join(missing)} (or the APPLE_KEY_ID / APPLE_TEAM_ID / "
                         f"APPLE_PRIVATE_KEY_PATH variables).")
    return make_dev_token(key_id, team_id, str(Path(key_path).expanduser()))


# ── Output ───────────────────────────────────────────────────────

def env_lines(dev_token: str, user_token: str) -> str:
    return (f"export APPLE_MUSIC_DEV_TOKEN={shlex.quote(dev_token)}\n"
            f"export APPLE_MUSIC_USER_TOKEN={shlex.quote(user_token)}\n")


OPENCLAW_HINT = """\
To make them available to OpenClaw, either add the export lines to your shell profile, or put
them in ~/.openclaw/openclaw.json under the skill's entry:

  "skills": { "entries": { "apple-music-dj": { "env": {
      "APPLE_MUSIC_DEV_TOKEN": "…", "APPLE_MUSIC_USER_TOKEN": "…" } } } }

Then check everything with: scripts/verify_setup.sh"""


def cmd_setup(args) -> int:
    print("🎧 Apple Music DJ — token setup\n", file=sys.stderr)
    try:
        dev_token = get_dev_token(args)
    except TokenError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("\n2/2  Music User Token: sign in with Apple in your browser.", file=sys.stderr)
    catcher = TokenCatcher(dev_token, args.port).start()
    try:
        opened = not args.no_browser and webbrowser.open(catcher.url)
        if not opened:
            # The link is a loopback address with a one-time path; it's only useful on this machine
            print(f"     Open this link in your browser:\n     {catcher.url}", file=sys.stderr)
        print(f"     Waiting up to {args.timeout}s… (Ctrl-C to cancel)", file=sys.stderr)
        user_token = catcher.wait(args.timeout)
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130
    finally:
        catcher.stop()
    if not user_token:
        print("ERROR: no sign-in arrived before the timeout. Run it again when you're ready.", file=sys.stderr)
        return 1

    with contextlib.suppress(OSError):
        record_user_token(user_token)  # remembers today's date by fingerprint, for the renewal reminder
    lines = env_lines(dev_token, user_token)
    print("\n✅ Both tokens ready.\n", file=sys.stderr)
    if args.env_file:
        path = Path(args.env_file).expanduser()
        write_private(path, "# Apple Music DJ tokens — keep private (mode 600)\n" + lines)
        print(f"Wrote {path} (owner-only). Load it with:  source {shlex.quote(str(path))}\n", file=sys.stderr)
    else:
        print(lines)
    print(OPENCLAW_HINT, file=sys.stderr)
    return 0


def cmd_status(_args) -> int:
    dev = check_token_expiry()
    user = check_user_token_age()
    if not os.environ.get("APPLE_MUSIC_DEV_TOKEN"):
        print("❌ APPLE_MUSIC_DEV_TOKEN is not set")
    else:
        print(dev["message"] if dev else "⚠️  Dev token set, but its expiry couldn't be read")
    if not os.environ.get("APPLE_MUSIC_USER_TOKEN"):
        print("❌ APPLE_MUSIC_USER_TOKEN is not set")
    elif user:
        print(user["message"])
    else:
        print("⚠️  User token set, but its age couldn't be read or recorded "
              "(check ~/.apple-music-dj/user_token_seen.json)")
    bad = (not dev or dev["warning"]) or (not user or user["warning"])
    if bad:
        print("Renew with: python3 scripts/setup_auth.py")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Get your Apple Music developer and user tokens in one step.")
    parser.add_argument("command", nargs="?", choices=["setup", "status"], default="setup")
    parser.add_argument("--key-id", help="MusicKit key ID (or APPLE_KEY_ID)")
    parser.add_argument("--team-id", help="Apple Developer Team ID (or APPLE_TEAM_ID)")
    parser.add_argument("--key-path", help="Path to the AuthKey_XXXX.p8 file (or APPLE_PRIVATE_KEY_PATH)")
    parser.add_argument("--new-dev-token", action="store_true", help="Sign a new developer token even if one is set")
    parser.add_argument("--env-file", help="Write the export lines to this file (mode 600) instead of printing them")
    parser.add_argument("--no-browser", action="store_true", help="Print the sign-in link instead of opening it")
    parser.add_argument("--port", type=int, default=0, help="Local port for the sign-in page (default: any free port)")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds to wait for sign-in (default: 300)")
    args = parser.parse_args(argv)
    return cmd_status(args) if args.command == "status" else cmd_setup(args)


if __name__ == "__main__":
    sys.exit(main())
