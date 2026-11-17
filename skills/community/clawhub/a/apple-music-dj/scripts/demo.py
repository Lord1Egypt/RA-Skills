#!/usr/bin/env python3
"""
demo.py — Try Apple Music DJ without an Apple Developer account or any tokens.

Runs the skill's real scripts against a local stand-in for the Apple Music API: a fictional
listener and a small sample catalog, served on 127.0.0.1 only for as long as the command runs.
Nothing is sent to Apple and nothing touches your Apple Music account. Demo data lives in
~/.apple-music-dj-demo/, apart from your real data.

Usage:
  python3 scripts/demo.py tour                    # a guided tour: taste profile, card, playlists
  python3 scripts/demo.py run <script> [args...]  # any skill script in demo mode
  python3 scripts/demo.py serve [--port 8765]     # just the mock API (for development)
  python3 scripts/demo.py reset                   # delete the demo data folder

In `run`, the word DEMO_PROFILE stands for the demo listener's taste profile:
  python3 scripts/demo.py run taste_card.py DEMO_PROFILE --format text
  python3 scripts/demo.py run strategy_engine.py --strategy similar --similar-to Radiohead --profile DEMO_PROFILE

The same server backs the end-to-end tests (tests/test_integration_mock_api.py), which assert on
every request it records. Response shapes follow Apple's documentation but are NOT verified
against the real service.
"""

import sys
if sys.version_info < (3, 10):
    sys.exit(
        f"ERROR: Python 3.10+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import contextlib
import os
import re
import shutil
import subprocess
from pathlib import Path
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

# ── Fixed catalog ────────────────────────────────────────────────

ARTISTS = {
    "a1": {"name": "Radiohead", "genres": ["Alternative", "Music"]},
    "a2": {"name": "Oasis", "genres": ["Rock", "Alternative", "Music"]},
    "a3": {"name": "Björk", "genres": ["Electronic", "Music"]},
    "a4": {"name": "Muse", "genres": ["Alternative", "Music"]},
}

# id, name, artist id, genres, release date, album id, isrc
_SONGS = [
    ("s1", "Karma Police", "a1", ["Alternative"], "1997-05-21", "alb1", "GBAYE9700001"),
    ("s2", "Paranoid Android", "a1", ["Alternative"], "1997-05-21", "alb1", "GBAYE9700002"),
    ("s3", "Let Down", "a1", ["Alternative"], "1997-05-21", "alb1", "GBAYE9700003"),
    ("s4", "Idioteque", "a1", ["Alternative", "Electronic"], "2000-10-02", "alb2", "GBAYE0000004"),
    ("s5", "Everything In Its Right Place", "a1", ["Alternative"], "2000-10-02", "alb2", "GBAYE0000005"),
    ("s6", "Wonderwall", "a2", ["Rock"], "1995-10-02", "alb3", "GBAYE9500006"),
    ("s7", "Champagne Supernova", "a2", ["Rock"], "1995-10-02", "alb3", "GBAYE9500007"),
    ("s8", "Don't Look Back in Anger", "a2", ["Rock"], "1995-10-02", "alb3", "GBAYE9500008"),
    ("s9", "Starlight", "a4", ["Alternative"], "2006-06-19", "alb4", "GBAYE0600009"),
    ("s10", "Supermassive Black Hole", "a4", ["Alternative", "Rock"], "2006-06-19", "alb4", "GBAYE0600010"),
    ("s11", "Jóga", "a3", ["Electronic"], "1997-09-22", "alb5", "GBAYE9700011"),
    ("s12", "Bachelorette", "a3", ["Electronic"], "1997-09-22", "alb5", "GBAYE9700012"),
]
ALBUMS = {
    "alb1": ("OK Computer", "a1", "1997-05-21"),
    "alb2": ("Kid A", "a1", "2000-10-02"),
    "alb3": ("(What's the Story) Morning Glory?", "a2", "1995-10-02"),
    "alb4": ("Black Holes and Revelations", "a4", "2006-06-19"),
    "alb5": ("Homogenic", "a3", "1997-09-22"),
}
SIMILAR = {"a1": ["a2", "a4"], "a2": ["a1"], "a3": ["a1"], "a4": ["a1", "a2"]}
LIBRARY_SONGS = ["s1", "s4"]
RATINGS = {"s5": 1, "s11": -1}
RECENT_TRACKS = ["s1", "s2", "s6"]


def song(sid: str) -> dict:
    row = next(r for r in _SONGS if r[0] == sid)
    _, name, aid, genres, date, alb, isrc = row
    return {
        "id": sid, "type": "songs",
        "attributes": {
            "name": name, "artistName": ARTISTS[aid]["name"], "genreNames": genres + ["Music"],
            "releaseDate": date, "albumName": ALBUMS[alb][0], "isrc": isrc, "trackNumber": 1,
        },
        "relationships": {"artists": {"data": [{"id": aid, "type": "artists"}]},
                          "albums": {"data": [{"id": alb, "type": "albums"}]}},
    }


def artist(aid: str) -> dict:
    a = ARTISTS[aid]
    return {"id": aid, "type": "artists", "attributes": {"name": a["name"], "genreNames": a["genres"]}}


def album(alb_id: str) -> dict:
    name, aid, date = ALBUMS[alb_id]
    return {"id": alb_id, "type": "albums",
            "attributes": {"name": name, "artistName": ARTISTS[aid]["name"], "releaseDate": date,
                           "isSingle": False, "trackCount": sum(1 for r in _SONGS if r[5] == alb_id),
                           "genreNames": ARTISTS[aid]["genres"]}}


# ── Server ───────────────────────────────────────────────────────

class MockAppleMusic:
    """Start with .start(); read .url; inspect .requests; stop with .stop()."""

    def __init__(self, port: int = 0):
        self.requests: list[dict] = []
        self.playlists: list[dict] = []
        self._port = port
        self._server: ThreadingHTTPServer | None = None

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self._server.server_address[1]}"

    def start(self) -> "MockAppleMusic":
        mock = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):  # keep test output quiet
                pass

            def _send(self, status: int, body: dict | None = None):
                payload = b"" if body is None else json.dumps(body).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def _handle(self, method: str):
                url = urlparse(self.path)
                query = parse_qs(url.query)
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length).decode() if length else ""
                try:
                    body = json.loads(raw) if raw else None
                except json.JSONDecodeError:
                    body = raw
                auth = self.headers.get("Authorization", "").startswith("Bearer ")
                user = bool(self.headers.get("Music-User-Token"))
                mock.requests.append({"method": method, "path": unquote(url.path), "query": query,
                                      "body": body, "auth": auth, "user_token": user})
                if not auth:
                    status, payload = 401, {"errors": [{"status": "401"}]}
                elif "/me/" in url.path + "/" and not user:
                    status, payload = 403, {"errors": [{"status": "403"}]}
                else:
                    status, payload = mock.route(method, unquote(url.path), query, body)
                self._send(status, payload)

            def do_GET(self):
                self._handle("GET")

            def do_POST(self):
                self._handle("POST")

            def do_PUT(self):
                self._handle("PUT")

            def do_DELETE(self):
                self._handle("DELETE")

        self._server = ThreadingHTTPServer(("127.0.0.1", self._port), Handler)
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        return self

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()

    def writes(self) -> list[dict]:
        return [r for r in self.requests if r["method"] != "GET"]

    # ── Routing ──────────────────────────────────────────────────

    def route(self, method: str, path: str, q: dict, body) -> tuple[int, dict | None]:
        parts = [p for p in path.split("/") if p]  # v1, ...
        if parts[:1] != ["v1"]:
            return 404, {"errors": [{"status": "404"}]}
        rest = parts[1:]

        if method == "GET":
            if rest == ["storefronts", "us"] or rest == ["me", "storefront"]:
                return 200, {"data": [{"id": "us", "type": "storefronts"}]}
            if rest == ["me", "recent", "played", "tracks"]:
                offset = int(q.get("offset", ["0"])[0])
                return 200, {"data": [song(s) for s in RECENT_TRACKS] if offset == 0 else []}
            if rest == ["me", "history", "heavy-rotation"] or rest == ["me", "recommendations"]:
                return 200, {"data": []}
            if rest == ["me", "recent", "played"]:
                return 200, {"data": []}
            if rest == ["me", "ratings", "songs"]:
                return 200, {"data": [{"id": sid, "type": "ratings", "attributes": {"value": v}}
                                      for sid, v in RATINGS.items()]}
            if rest == ["me", "music-summaries"] or rest == ["me", "music-summaries", "milestones"]:
                return 404, {"errors": [{"status": "404", "title": "Replay not available"}]}
            if rest == ["me", "library", "artists"]:
                offset = int(q.get("offset", ["0"])[0])
                return 200, {"data": [{"id": f"r.{a}", "type": "library-artists",
                                       "attributes": {"name": ARTISTS[a]["name"]}}
                                      for a in ("a1", "a2")] if offset == 0 else []}
            if rest == ["me", "library", "songs"]:
                offset = int(q.get("offset", ["0"])[0])
                out = []
                for sid in LIBRARY_SONGS if offset == 0 else []:
                    s = song(sid)
                    s["id"] = f"i.{sid}"
                    s["type"] = "library-songs"
                    s["relationships"]["catalog"] = {"data": [{"id": sid, "type": "songs"}]}
                    out.append(s)
                return 200, {"data": out}
            if rest == ["me", "library", "recently-added"]:
                return 200, {"data": [
                    {"id": "l.alb4", "type": "library-albums",
                     "attributes": {"name": ALBUMS["alb4"][0], "artistName": "Muse",
                                    "genreNames": ["Alternative"], "releaseDate": "2006-06-19"}},
                    {"id": "p.1", "type": "library-playlists", "attributes": {"name": "Road Trip"}},
                ]}
            if rest == ["me", "recent", "radio-stations"]:
                return 200, {"data": [
                    {"id": "ra.1", "type": "stations", "attributes": {"name": "Alternative Radio"}},
                    {"id": "ra.2", "type": "stations", "attributes": {"name": "Radiohead Station"}},
                ]}
            if rest == ["me", "library", "playlists"]:
                return 200, {"data": self.playlists}
            if rest[:3] == ["me", "library", "playlists"] and rest[-1] == "tracks":
                return 200, {"data": []}
            if rest[:1] == ["catalog"]:
                return self._catalog(rest[2:], q)
            return 404, {"errors": [{"status": "404", "detail": f"no mock for GET {path}"}]}

        if method == "POST":
            if rest == ["me", "library", "playlists"]:
                attrs = (body or {}).get("attributes", {})
                pl = {"id": f"p.{len(self.playlists) + 1}", "type": "library-playlists",
                      "attributes": {"name": attrs.get("name", "")}}
                self.playlists.append(pl)
                return 201, {"data": [pl]}
            if rest == ["me", "library"] or rest == ["me", "favorites"]:
                return 202, None
            if rest[:3] == ["me", "library", "playlists"] and rest[-1] == "tracks":
                return 204, None
        if method == "PUT" and rest[:3] == ["me", "ratings", "songs"] and len(rest) == 4:
            value = ((body or {}).get("attributes") or {}).get("value")
            return 200, {"data": [{"id": rest[3], "type": "ratings", "attributes": {"value": value}}]}
        if method == "DELETE" and rest[:3] == ["me", "ratings", "songs"] and len(rest) == 4:
            return 204, None
        if method == "DELETE" and rest[:3] == ["me", "library", "playlists"] and rest[-1] == "tracks":
            return 204, None
        return 404, {"errors": [{"status": "404", "detail": f"no mock for {method} {path}"}]}

    def _catalog(self, rest: list[str], q: dict) -> tuple[int, dict]:
        if rest == ["charts"]:
            return 200, {"results": {"songs": [{"name": "Top Songs", "data": [song("s9"), song("s12")]}]}}
        if rest == ["search"]:
            term = (q.get("term", [""])[0]).lower()
            types = (q.get("types", ["songs"])[0]).split(",")
            results: dict = {}
            if "artists" in types:
                results["artists"] = {"data": [artist(a) for a, v in ARTISTS.items() if v["name"].lower() in term
                                               or term in v["name"].lower()]}
            if "songs" in types:
                results["songs"] = {"data": [song(r[0]) for r in _SONGS
                                             if r[1].lower() in term or term in r[1].lower()
                                             or ARTISTS[r[2]]["name"].lower() in term]}
            if "albums" in types:
                results["albums"] = {"data": [album(a) for a, v in ALBUMS.items() if term in v[0].lower()]}
            return 200, {"results": results}
        if rest == ["songs"]:
            wanted = set((q.get("filter[isrc]", [""])[0]).split(","))
            return 200, {"data": [song(r[0]) for r in _SONGS if r[6] in wanted]}
        if len(rest) == 2 and rest[0] == "songs":
            if not any(r[0] == rest[1] for r in _SONGS):
                return 404, {"errors": [{"status": "404", "detail": f"no song {rest[1]}"}]}
            return 200, {"data": [song(rest[1])]}
        if rest[:1] == ["artists"] and len(rest) >= 2 and rest[1] in ARTISTS:
            aid = rest[1]
            if rest[2:] == ["view", "similar-artists"]:
                return 200, {"data": [artist(a) for a in SIMILAR.get(aid, [])]}
            if rest[2:] == ["albums"]:
                return 200, {"data": [album(a) for a, v in ALBUMS.items() if v[1] == aid]}
            if len(rest) == 2 and "top-songs" in (q.get("views", [""])[0]):
                tops = [song(r[0]) for r in _SONGS if r[2] == aid][:2]
                a = artist(aid)
                a["views"] = {"top-songs": {"data": tops}}
                return 200, {"data": [a]}
            if len(rest) == 2:
                return 200, {"data": [artist(aid)]}
        if len(rest) == 2 and rest[0] == "albums" and rest[1] in ALBUMS:
            a = album(rest[1])
            a["relationships"] = {"tracks": {"data": [song(r[0]) for r in _SONGS if r[5] == rest[1]]}}
            return 200, {"data": [a]}
        return 404, {"errors": [{"status": "404", "detail": f"no mock for catalog/{'/'.join(rest)}"}]}


# ── Demo mode ────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_HOME = Path.home() / ".apple-music-dj-demo"
REAL_APP_DIR = Path.home() / ".apple-music-dj"
PROFILE_TOKEN = "DEMO_PROFILE"
BANNER = ("🎧 Demo mode: a fictional listener and a small sample catalog. "
          "Nothing here touches your Apple Music account.")
# Scripts that act outside the sandbox (the system crontab, real credentials) or are not tools
NOT_IN_DEMO = {"demo.py", "setup_cron.py", "setup_auth.py", "generate_dev_token.py", "_common.py"}


def demo_profile_path() -> Path:
    return DEMO_HOME / ".apple-music-dj" / "taste_profile.json"


def demo_env(api_url: str) -> dict:
    """The child's environment: real Apple credentials removed, demo ones and a sandbox HOME set."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("APPLE_")}
    env.update({
        "HOME": str(DEMO_HOME),
        "APPLE_MUSIC_API_BASE": api_url,
        "APPLE_MUSIC_DEV_TOKEN": "demo-dev-token",
        "APPLE_MUSIC_USER_TOKEN": "demo-user-token",
        "APPLE_MUSIC_STOREFRONT": "us",
        "APPLE_MUSIC_DJ_DEMO": "1",
    })
    return env


def script_command(name: str) -> list[str]:
    """Resolve a skill script by bare name; anything else is refused."""
    if "/" in name or name in NOT_IN_DEMO or not (SCRIPT_DIR / name).is_file() or not name.endswith((".py", ".sh")):
        allowed = sorted(p.name for p in SCRIPT_DIR.iterdir()
                         if p.suffix in (".py", ".sh") and p.name not in NOT_IN_DEMO)
        raise SystemExit(f"ERROR: '{name}' can't run in demo mode. Pick one of: {', '.join(allowed)}")
    path = str(SCRIPT_DIR / name)
    return ["bash", path] if name.endswith(".sh") else [sys.executable, path]


def _points_into_real_data(value: str) -> bool:
    """True if `value`, read as a path (with `..` and symlinks resolved), is in the real data folder."""
    if not value:
        return False
    try:
        resolved = Path(value).expanduser().resolve()
        real = REAL_APP_DIR.resolve()
    except (OSError, RuntimeError, ValueError):
        return False
    return resolved == real or real in resolved.parents


def check_args(args: list[str]) -> list[str]:
    """Swap DEMO_PROFILE for the demo profile and refuse paths into the real data folder."""
    real_text = re.compile(re.escape(str(REAL_APP_DIR)) + r"(?=/|$)")
    out = []
    for a in args:
        value = a.split("=", 1)[1] if a.startswith("--") and "=" in a else a
        if real_text.search(a) or _points_into_real_data(value):
            raise SystemExit(f"ERROR: demo mode won't read or write your real data ({REAL_APP_DIR}). "
                             f"Use {PROFILE_TOKEN} for the demo profile.")
        out.append(a.replace(PROFILE_TOKEN, str(demo_profile_path())))
    return out


def _run(cmd: list[str], env: dict, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, env=env, text=True, capture_output=capture, timeout=300)


def ensure_profile(env: dict) -> None:
    if demo_profile_path().is_file():
        return
    r = _run(script_command("taste_profiler.py") + ["--output", str(demo_profile_path()), "--skip-replay"],
             env, capture=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit("ERROR: could not build the demo taste profile.")


def prepare_demo_home() -> None:
    """Create the sandbox, refusing a symlinked one (it could alias the real data folder)."""
    inner = DEMO_HOME / ".apple-music-dj"
    for d in (DEMO_HOME, inner):
        if d.is_symlink():
            raise SystemExit(f"ERROR: {d} is a symlink; demo mode needs a real folder there. "
                             f"Remove the link and try again.")
    DEMO_HOME.mkdir(mode=0o700, exist_ok=True)
    if DEMO_HOME.resolve() == REAL_APP_DIR.resolve() or REAL_APP_DIR.resolve() in DEMO_HOME.resolve().parents:
        raise SystemExit(f"ERROR: {DEMO_HOME} resolves into {REAL_APP_DIR}; refusing to run the demo there.")


def start_server() -> MockAppleMusic:
    prepare_demo_home()
    return MockAppleMusic().start()


def cmd_run(script: str, args: list[str]) -> int:
    cmd = script_command(script) + check_args(args)
    print(BANNER, file=sys.stderr)
    srv = start_server()
    try:
        env = demo_env(srv.url)
        if any(PROFILE_TOKEN in a for a in args):
            ensure_profile(env)
        return _run(cmd, env).returncode
    finally:
        srv.stop()


TOUR = [
    ("Your Taste DNA card", ["taste_card.py", PROFILE_TOKEN, "--format", "text"]),
    ('"Songs like Radiohead" (a preview; in real use you approve before anything is created)',
     ["strategy_engine.py", "--strategy", "similar", "--similar-to", "Radiohead", "--profile", PROFILE_TOKEN,
      "--size", "8"]),
    ('"Make me a 90s throwback"',
     ["strategy_engine.py", "--strategy", "era", "--decade", "1990s", "--profile", PROFILE_TOKEN, "--size", "8"]),
    ('"Give me one song for today"', ["daily_pick.py", "daily", PROFILE_TOKEN, "us"]),
    ('"How compatible am I with Björk?"', ["compatibility.py", "artist", PROFILE_TOKEN, "us", "Björk"]),
]


def pretty(stdout: str) -> str:
    """Playlists read as a numbered list with reasons; anything else is passed through."""
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return stdout.rstrip()
    if isinstance(data, dict) and isinstance(data.get("tracks"), list):
        rows = [f"{data.get('name', 'Playlist')}"]
        width = max((len(f"{t.get('name')} — {t.get('artist')}") for t in data["tracks"]), default=0)
        for i, t in enumerate(data["tracks"], 1):
            label = f"{t.get('name')} — {t.get('artist')}"
            rows.append(f"{i:>2}. {label.ljust(width)}   {t.get('reason', '')}".rstrip())
        return "\n".join(rows)
    if isinstance(data, dict) and isinstance(data.get("message"), str):
        return data["message"]
    if isinstance(data, dict) and "compatibility_pct" in data:
        return f"{data.get('artist')}: {data['compatibility_pct']}% — {data.get('verdict', '')}".rstrip(" —")
    return json.dumps(data, indent=2, ensure_ascii=False)


def cmd_tour() -> int:
    print(BANNER + "\n")
    srv = start_server()
    try:
        env = demo_env(srv.url)
        print("── Building a taste profile from the demo listener's history ──\n")
        ensure_profile(env)
        failed = []
        for title, (script, *args) in TOUR:
            print(f"\n── {title} ──\n", flush=True)
            r = _run(script_command(script) + check_args(args), env, capture=True)
            if r.returncode == 0:
                print(pretty(r.stdout))
            else:
                failed.append(script)
                print(r.stderr.rstrip() or f"({script} exited {r.returncode})")
    finally:
        srv.stop()
    if failed:
        print(f"\n⚠️  {len(failed)} demo step(s) failed: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("\n── That's the demo ──")
    print("Ready for your own music? Run: python3 scripts/setup_auth.py  (see references/auth-setup.md)")
    return 0


def cmd_serve(port: int) -> int:
    srv = MockAppleMusic(port).start()
    print(f"Mock Apple Music API on {srv.url}  (Ctrl-C to stop)", flush=True)
    try:
        with contextlib.suppress(KeyboardInterrupt):  # Ctrl-C is the normal way to stop
            threading.Event().wait()
    finally:
        srv.stop()
    return 0


def cmd_reset() -> int:
    if DEMO_HOME.is_dir() and not DEMO_HOME.is_symlink():
        shutil.rmtree(DEMO_HOME)
        print(f"Removed {DEMO_HOME}")
    else:
        print("No demo data to remove.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Try Apple Music DJ with a fictional listener — no tokens needed.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tour", help="Guided tour: taste profile, card, playlists, compatibility")
    run = sub.add_parser("run", help="Run one skill script in demo mode (DEMO_PROFILE = demo profile path)")
    run.add_argument("script", help="Script name in scripts/, e.g. strategy_engine.py")
    run.add_argument("args", nargs=argparse.REMAINDER, help="Arguments passed to the script")
    serve = sub.add_parser("serve", help="Serve the mock API on 127.0.0.1 (development)")
    serve.add_argument("--port", type=int, default=8765)
    sub.add_parser("reset", help=f"Delete the demo data folder ({DEMO_HOME})")
    a = parser.parse_args(argv)
    if a.cmd == "tour":
        return cmd_tour()
    if a.cmd == "run":
        return cmd_run(a.script, a.args)
    if a.cmd == "serve":
        return cmd_serve(a.port)
    return cmd_reset()


if __name__ == "__main__":
    sys.exit(main())
