#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import shlex
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser

try:
    from i18n import add_locale_argument, resolve_locale, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, resolve_locale, t


DEFAULT_STATE = pathlib.Path(".codex/design-guide/preview.json")
REMOTE_ENV_MARKERS = (
    "CI",
    "CODESPACES",
    "REMOTE_CONTAINERS",
    "SSH_CLIENT",
    "SSH_CONNECTION",
    "SSH_TTY",
)


def process_start_marker(pid: int) -> str | None:
    stat_path = pathlib.Path(f"/proc/{pid}/stat")
    try:
        stat_text = stat_path.read_text(encoding="utf-8")
    except OSError:
        stat_text = ""
    # The parenthesized command can contain spaces, so parse fields after its closing paren.
    fields_after_command = stat_text.rsplit(")", 1)[-1].split() if ")" in stat_text else []
    if len(fields_after_command) > 19:
        return f"proc:{fields_after_command[19]}"
    if os.name != "nt":
        try:
            result = subprocess.run(
                ["ps", "-o", "lstart=", "-p", str(pid)],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        marker = result.stdout.strip()
        return f"ps:{marker}" if result.returncode == 0 and marker else None
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"(Get-Process -Id {pid}).StartTime.ToUniversalTime().Ticks",
            ],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    marker = result.stdout.strip()
    return f"win:{marker}" if result.returncode == 0 and marker else None


def process_matches(state: dict) -> bool:
    pid = state.get("pid")
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    expected = state.get("processStart")
    actual = process_start_marker(pid)
    return bool(expected and actual and expected == actual)


def write_state(path: pathlib.Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    try:
        temporary.chmod(0o600)
    except OSError:
        pass
    temporary.replace(path)


def load_state(path: pathlib.Path) -> dict:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"No preview state at {path}") from exc
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"Invalid preview state at {path}: {exc}") from exc
    if not isinstance(state, dict):
        raise RuntimeError(f"Invalid preview state at {path}: expected an object")
    return state


def health_check(url: str, timeout: float = 1.5) -> tuple[bool, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "design-guide-preview/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 400, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except (OSError, urllib.error.URLError) as exc:
        return False, str(exc)


def wait_until_healthy(url: str, process: subprocess.Popen, timeout: float) -> str:
    deadline = time.monotonic() + timeout
    last_message = "not checked"
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"preview command exited with code {process.returncode}")
        healthy, last_message = health_check(url)
        if healthy:
            return last_message
        time.sleep(0.1)
    raise RuntimeError(f"health check timed out ({last_message})")


def browser_allowed(policy: str) -> tuple[bool, str]:
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


def open_browser(url: str, policy: str) -> str:
    allowed, reason = browser_allowed(policy)
    if not allowed:
        return f"skipped ({reason})"
    try:
        return f"open request sent ({reason})" if webbrowser.open(url, new=2) else "no browser accepted the URL"
    except Exception as exc:
        return f"open request failed ({exc})"


def terminate(state: dict, timeout: float = 5.0) -> bool:
    if not process_matches(state):
        return False
    pid = state["pid"]
    try:
        if os.name == "nt":
            os.kill(pid, signal.CTRL_BREAK_EVENT)
        else:
            os.killpg(pid, signal.SIGTERM)
    except (OSError, ProcessLookupError):
        return False
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if not process_matches(state):
            return True
        time.sleep(0.05)
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                capture_output=True,
                timeout=5,
                check=False,
            )
        else:
            os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    return True


def terminate_spawned_process(process: subprocess.Popen) -> None:
    marker = process_start_marker(process.pid)
    if marker:
        terminate({"pid": process.pid, "processStart": marker}, timeout=2)
    elif process.poll() is None:
        process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def command_start(args: argparse.Namespace) -> int:
    state_path = pathlib.Path(args.state).expanduser().resolve()
    cwd = pathlib.Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        print(t("Preview working directory does not exist: {path}", args.locale, path=cwd), file=sys.stderr)
        return 1
    if state_path.exists():
        try:
            existing = load_state(state_path)
        except RuntimeError:
            existing = {}
        if process_matches(existing):
            print(t("A preview is already running (PID {pid}).", args.locale, pid=existing["pid"]), file=sys.stderr)
            return 1
        state_path.unlink(missing_ok=True)

    command = shlex.split(args.command, posix=os.name != "nt")
    if not command:
        print(t("Preview command cannot be empty", args.locale), file=sys.stderr)
        return 1
    log_path = pathlib.Path(args.log).expanduser().resolve() if args.log else state_path.with_suffix(".log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["BROWSER"] = "none"
    with log_path.open("ab", buffering=0) as log_file:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            close_fds=True,
            start_new_session=os.name != "nt",
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        )
    try:
        health = wait_until_healthy(args.health_url, process, args.wait)
    except RuntimeError as exc:
        terminate_spawned_process(process)
        print(t("Failed to start preview: {error}. Log: {log}", args.locale, error=exc, log=log_path), file=sys.stderr)
        return 1

    process_marker = process_start_marker(process.pid)
    if not process_marker:
        terminate_spawned_process(process)
        print(t("Failed to start preview: could not establish a safe process identity", args.locale), file=sys.stderr)
        return 1
    state = {
        "version": 1,
        "pid": process.pid,
        "processStart": process_marker,
        "command": command,
        "cwd": str(cwd),
        "url": args.url,
        "healthUrl": args.health_url,
        "log": str(log_path),
        "startedAt": int(time.time()),
    }
    write_state(state_path, state)
    print(t("Preview: running", args.locale))
    print(f"PID: {process.pid}")
    print(f"URL: {args.url}")
    print(f"Health: {health}")
    print(f"{t('State', args.locale)}: {state_path}")
    print(f"{t('Log', args.locale)}: {log_path}")
    print(f"{t('Browser', args.locale)}: {open_browser(args.url, args.browser)}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    state_path = pathlib.Path(args.state).expanduser().resolve()
    try:
        state = load_state(state_path)
    except RuntimeError as exc:
        print(t("Preview: not running ({error})", args.locale, error=exc))
        return 1
    if not process_matches(state):
        print(t("Preview: not running (stale state)", args.locale))
        return 1
    healthy, message = health_check(state["healthUrl"])
    print(t("Preview: running", args.locale) if healthy else t("Preview: process running, health check failed", args.locale))
    print(f"PID: {state['pid']}")
    print(f"URL: {state['url']}")
    print(f"Health: {message}")
    print(f"Log: {state['log']}")
    return 0 if healthy else 1


def command_stop(args: argparse.Namespace) -> int:
    state_path = pathlib.Path(args.state).expanduser().resolve()
    if not state_path.exists():
        print(t("Preview: no active state at {path}", args.locale, path=state_path))
        return 0
    try:
        state = load_state(state_path)
    except RuntimeError as exc:
        print(t("Preview: cannot stop safely ({error})", args.locale, error=exc), file=sys.stderr)
        return 1
    stopped = terminate(state)
    state_path.unlink(missing_ok=True)
    print(t("Preview: stopped", args.locale) if stopped else t("Preview: stale state removed", args.locale))
    return 0


def add_state_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--state", default=str(DEFAULT_STATE), help=t("Preview state file"))


def parse_args() -> argparse.Namespace:
    locale = resolve_locale()
    parser = argparse.ArgumentParser(description=t("Start, inspect, and stop a managed frontend preview.", locale))
    add_locale_argument(parser)
    subparsers = parser.add_subparsers(dest="action", required=True)

    start = subparsers.add_parser("start", help=t("Start a preview command and wait for health", locale))
    add_locale_argument(start, suppress_default=True)
    start.add_argument("--command", required=True, help=t("Command parsed without a shell", locale))
    start.add_argument("--url", required=True, help=t("URL to open for the user", locale))
    start.add_argument("--health-url", help=t("Health URL; defaults to --url", locale))
    start.add_argument("--cwd", default=".")
    start.add_argument("--log")
    start.add_argument("--wait", type=float, default=30.0)
    start.add_argument("--browser", choices=("auto", "always", "never"), default="auto")
    add_state_option(start)
    start.set_defaults(handler=command_start)

    status = subparsers.add_parser("status", help=t("Inspect the managed preview", locale))
    add_locale_argument(status, suppress_default=True)
    add_state_option(status)
    status.set_defaults(handler=command_status)

    stop = subparsers.add_parser("stop", help=t("Stop the managed preview", locale))
    add_locale_argument(stop, suppress_default=True)
    add_state_option(stop)
    stop.set_defaults(handler=command_stop)
    args = parser.parse_args()
    if args.action == "start" and not args.health_url:
        args.health_url = args.url
    return args


def main() -> int:
    args = parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
