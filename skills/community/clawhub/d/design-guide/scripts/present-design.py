#!/usr/bin/env python3
import argparse
import functools
import http.server
import json
import os
import pathlib
import secrets
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from urllib.parse import quote, unquote, urlsplit

try:
    from i18n import add_locale_argument, resolve_locale, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, resolve_locale, t


DEFAULT_STATE = pathlib.Path(".codex/design/presentation.json")
REMOTE_ENV_MARKERS = (
    "CI",
    "CODESPACES",
    "REMOTE_CONTAINERS",
    "SSH_CLIENT",
    "SSH_CONNECTION",
    "SSH_TTY",
)
CONTROL_PREFIX = "/__f_design__/"


def add_browser_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--browser",
        choices=("auto", "always", "never"),
        default="auto",
        help=t("Browser behavior; auto skips remote or headless environments"),
    )


def add_state_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--state",
        default=str(DEFAULT_STATE),
        help=t("Presentation state file"),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    if argv and argv[0] == "_serve":
        internal_parser = argparse.ArgumentParser(add_help=False)
        internal_parser.add_argument("--root", required=True)
        internal_parser.add_argument("--state", required=True)
        internal_parser.add_argument("--token", required=True)
        internal_parser.add_argument("--port", type=int, required=True)
        internal_parser.add_argument("targets", nargs="+")
        internal_args = internal_parser.parse_args(argv[1:])
        internal_args.command = "_serve"
        return internal_args

    commands = {"open", "serve", "status", "stop"}
    if argv and argv[0] not in commands and not argv[0].startswith("-"):
        argv = ["open", *argv]

    locale = resolve_locale(argv)
    parser = argparse.ArgumentParser(
        description=t("Present local HTML design artifacts for user review.", locale)
    )
    add_locale_argument(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    open_parser = subparsers.add_parser(
        "open",
        help=t("Open standalone HTML files and return immediately", locale),
    )
    add_locale_argument(open_parser, suppress_default=True)
    open_parser.add_argument("targets", nargs="+", help=t("HTML artifact paths", locale))
    add_browser_option(open_parser)

    serve_parser = subparsers.add_parser(
        "serve",
        help=t("Start a managed background HTTP server", locale),
    )
    add_locale_argument(serve_parser, suppress_default=True)
    serve_parser.add_argument("targets", nargs="+", help=t("HTML artifact paths", locale))
    serve_parser.add_argument("--port", type=int, default=0, help=t("Port; 0 picks a free port", locale))
    serve_parser.add_argument(
        "--open-wait",
        type=float,
        default=5.0,
        help=t("Seconds to wait for browser requests", locale),
    )
    add_browser_option(serve_parser)
    add_state_option(serve_parser)

    status_parser = subparsers.add_parser("status", help=t("Show server status", locale))
    add_locale_argument(status_parser, suppress_default=True)
    add_state_option(status_parser)

    stop_parser = subparsers.add_parser("stop", help=t("Stop the background server", locale))
    add_locale_argument(stop_parser, suppress_default=True)
    add_state_option(stop_parser)

    return parser.parse_args(argv)


def resolve_targets(
    values: list[str],
    require_same_parent: bool = False,
) -> list[pathlib.Path]:
    targets = [pathlib.Path(value).expanduser().resolve() for value in values]
    for target in targets:
        if not target.is_file():
            raise SystemExit(f"Design artifact not found: {target}")
        if target.suffix.lower() not in {".html", ".htm"}:
            raise SystemExit(f"Expected an HTML design artifact: {target}")

    parent = targets[0].parent
    if require_same_parent and any(target.parent != parent for target in targets[1:]):
        raise SystemExit("All review artifacts must be in the same directory")
    return targets


def browser_decision(policy: str) -> tuple[bool, str]:
    if policy == "always":
        return True, "forced"
    if policy == "never":
        return False, "disabled"

    marker = next((name for name in REMOTE_ENV_MARKERS if os.environ.get(name)), None)
    if marker:
        return False, f"remote/headless marker {marker} is set"
    if sys.platform.startswith("linux") and not (
        os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    ):
        return False, "no DISPLAY or WAYLAND_DISPLAY"
    return True, "local desktop detected"


def open_urls(urls: list[str], policy: str) -> tuple[bool, str]:
    allowed, reason = browser_decision(policy)
    if not allowed:
        return False, f"skipped ({reason})"

    results = []
    for url in urls:
        try:
            results.append(webbrowser.open(url, new=2))
        except Exception as exc:
            return False, f"open request failed ({exc})"
    if all(results):
        return True, f"open requests sent ({reason})"
    return False, "no browser accepted every open request"


def load_state(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"No active presentation state: {path}") from exc
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"Invalid presentation state: {path} ({exc})") from exc


def write_state(path: pathlib.Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    try:
        temp_path.chmod(0o600)
    except OSError:
        pass
    temp_path.replace(path)


def control_url(state: dict, action: str) -> str:
    return f"http://127.0.0.1:{state['port']}{CONTROL_PREFIX}{action}"


def request_json(url: str, token: str, timeout: float = 1.5) -> dict:
    request = urllib.request.Request(url, headers={"X-F-Design-Token": token})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def query_server(state: dict) -> dict:
    return request_json(control_url(state, "status"), state["token"])


def state_is_active(path: pathlib.Path) -> bool:
    try:
        query_server(load_state(path))
    except urllib.error.HTTPError as exc:
        return exc.code in {401, 403}
    except (RuntimeError, OSError, urllib.error.URLError, KeyError, ValueError):
        return False
    return True


def print_artifacts(targets: list[pathlib.Path], urls: list[str], locale: str) -> None:
    for target, url in zip(targets, urls):
        print(f"{t('Artifact', locale)}: {target}")
        print(f"{t('Review URL', locale)}: {url}")


def command_open(args: argparse.Namespace) -> int:
    targets = resolve_targets(args.targets)
    urls = [target.as_uri() for target in targets]
    print_artifacts(targets, urls, args.locale)
    opened, message = open_urls(urls, args.browser)
    print(f"{t('Browser', args.locale)}: {message}")
    if not opened:
        print(t("Fallback: attach screenshots or provide a host-accessible artifact link.", args.locale))
    return 0


def detached_process_args() -> dict:
    if os.name == "nt":
        return {
            "creationflags": subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.DETACHED_PROCESS
        }
    return {"start_new_session": True}


def wait_for_state(
    state_path: pathlib.Path,
    token: str,
    process: subprocess.Popen,
    timeout: float = 5.0,
) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Presentation server exited with code {process.returncode}")
        try:
            state = load_state(state_path)
            if state.get("token") == token:
                query_server(state)
                return state
        except (RuntimeError, OSError, urllib.error.URLError, KeyError, ValueError):
            pass
        time.sleep(0.05)
    raise RuntimeError("Presentation server did not become ready")


def terminate_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def wait_for_browser_requests(state: dict, expected: set[str], timeout: float) -> bool:
    deadline = time.monotonic() + max(timeout, 0)
    while time.monotonic() < deadline:
        try:
            status = query_server(state)
        except (OSError, urllib.error.URLError, KeyError, ValueError):
            return False
        if expected.issubset(set(status.get("requested", []))):
            return True
        time.sleep(0.1)
    return False


def command_serve(args: argparse.Namespace) -> int:
    targets = resolve_targets(args.targets, require_same_parent=True)
    state_path = pathlib.Path(args.state).expanduser().resolve()
    if state_path.exists():
        if state_is_active(state_path):
            raise SystemExit(
                f"A presentation server is already active. Stop it with:\n"
                f"  {pathlib.Path(__file__).resolve()} stop --state {state_path}"
            )
        state_path.unlink()

    token = secrets.token_urlsafe(24)
    root = targets[0].parent
    names = [target.name for target in targets]
    log_path = state_path.with_suffix(".log")
    command = [
        sys.executable,
        str(pathlib.Path(__file__).resolve()),
        "_serve",
        "--root",
        str(root),
        "--state",
        str(state_path),
        "--token",
        token,
        "--port",
        str(args.port),
        *names,
    ]

    state_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("ab", buffering=0) as log_file:
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            close_fds=True,
            **detached_process_args(),
        )

    try:
        state = wait_for_state(state_path, token, process)
    except RuntimeError as exc:
        terminate_process(process)
        try:
            stale = load_state(state_path)
        except RuntimeError:
            stale = {}
        if stale.get("token") == token:
            state_path.unlink(missing_ok=True)
        raise SystemExit(f"Failed to start presentation server: {exc}. Log: {log_path}")

    urls = state["urls"]
    print_artifacts(targets, urls, args.locale)
    print(f"{t('State', args.locale)}: {state_path}")
    print(f"{t('Log', args.locale)}: {log_path}")
    opened, message = open_urls(urls, args.browser)
    if opened:
        requested = wait_for_browser_requests(state, set(names), args.open_wait)
        message = "all artifact pages requested" if requested else f"{message}; requests not observed"
    print(f"{t('Browser', args.locale)}: {message}")
    if not opened:
        print(t("Fallback: loopback URLs are agent-local unless the host exposes them.", args.locale))
        print(t("Fallback: attach screenshots or provide a host-accessible artifact link.", args.locale))
    print(t("Server: running in background", args.locale))
    return 0


def command_status(args: argparse.Namespace) -> int:
    state_path = pathlib.Path(args.state).expanduser().resolve()
    try:
        state = load_state(state_path)
        status = query_server(state)
    except (RuntimeError, OSError, urllib.error.URLError, KeyError, ValueError) as exc:
        print(t("Server: not reachable ({error})", args.locale, error=exc))
        return 1

    print(t("Server: running", args.locale))
    print(f"PID: {state.get('pid')}")
    print(f"{t('State', args.locale)}: {state_path}")
    for url in state.get("urls", []):
        print(f"{t('Review URL', args.locale)}: {url}")
    for name in status.get("requested", []):
        print(f"Requested: {name}")
    return 0


def command_stop(args: argparse.Namespace) -> int:
    state_path = pathlib.Path(args.state).expanduser().resolve()
    if not state_path.exists():
        print(t("Server: no active state at {path}", args.locale, path=state_path))
        return 0

    try:
        state = load_state(state_path)
        request_json(control_url(state, "stop"), state["token"])
    except urllib.error.HTTPError as exc:
        print(t("Server: stop rejected with HTTP {code}; state preserved", args.locale, code=exc.code))
        return 1
    except (RuntimeError, OSError, urllib.error.URLError, KeyError, ValueError) as exc:
        print(t("Server: not reachable; removing stale state ({error})", args.locale, error=exc))
        state_path.unlink(missing_ok=True)
        return 0

    deadline = time.monotonic() + 5
    while state_path.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    if state_path.exists():
        print(t("Server: stop requested but state remains at {path}", args.locale, path=state_path))
        return 1
    print(t("Server: stopped", args.locale))
    return 0


def send_json(handler: http.server.BaseHTTPRequestHandler, status: int, data: dict) -> None:
    body = json.dumps(data).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def command_internal_serve(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).resolve()
    state_path = pathlib.Path(args.state).resolve()
    allowed = set(args.targets)
    requested: set[str] = set()
    requested_lock = threading.Lock()

    class ReviewHandler(http.server.SimpleHTTPRequestHandler):
        current_target: str | None = None

        def do_GET(self) -> None:
            parsed = urlsplit(self.path)
            if parsed.path.startswith(CONTROL_PREFIX):
                supplied = self.headers.get("X-F-Design-Token", "")
                if not secrets.compare_digest(supplied, args.token):
                    send_json(self, 403, {"error": "forbidden"})
                    return
                action = parsed.path.removeprefix(CONTROL_PREFIX)
                if action == "status":
                    with requested_lock:
                        seen = sorted(requested)
                    send_json(self, 200, {"status": "running", "requested": seen})
                    return
                if action == "stop":
                    send_json(self, 200, {"status": "stopping"})
                    threading.Thread(target=self.server.shutdown, daemon=True).start()
                    return
                send_json(self, 404, {"error": "unknown action"})
                return

            name = unquote(parsed.path).lstrip("/")
            self.current_target = name if name in allowed else None
            super().do_GET()

        def send_response(self, code: int, message: str | None = None) -> None:
            if self.current_target and 200 <= code < 400:
                with requested_lock:
                    requested.add(self.current_target)
            super().send_response(code, message)

    handler = functools.partial(ReviewHandler, directory=str(root))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    server.daemon_threads = True
    port = server.server_address[1]
    urls = [f"http://127.0.0.1:{port}/{quote(name)}" for name in args.targets]
    state = {
        "pid": os.getpid(),
        "port": port,
        "root": str(root),
        "targets": args.targets,
        "urls": urls,
        "token": args.token,
        "started_at": time.time(),
    }
    write_state(state_path, state)

    try:
        server.serve_forever()
    finally:
        server.server_close()
        try:
            current = load_state(state_path)
        except RuntimeError:
            current = {}
        if current.get("token") == args.token:
            state_path.unlink(missing_ok=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    commands = {
        "open": command_open,
        "serve": command_serve,
        "status": command_status,
        "stop": command_stop,
        "_serve": command_internal_serve,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
