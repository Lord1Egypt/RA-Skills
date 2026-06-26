#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_SUBDIR = "akshare-workbench"
RUNTIME_DIRNAME = ".skill-runtime"
BACKEND_PORT = int(os.environ.get("AKSHARE_BACKEND_PORT", "8000"))
FRONTEND_PORT = int(os.environ.get("AKSHARE_FRONTEND_PORT", "5173"))


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def bundled_project() -> Path:
    return skill_root() / "assets" / PROJECT_SUBDIR


def is_project_root(path: Path) -> bool:
    return (
        (path / "backend" / "app" / "main.py").exists()
        and (path / "backend" / "app" / "catalog" / "indicators.yaml").exists()
        and (path / "frontend" / "package.json").exists()
    )


def find_project_root(explicit: str | None = None, *, required: bool = True) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("AKSHARE_WORKBENCH_ROOT"):
        candidates.append(Path(os.environ["AKSHARE_WORKBENCH_ROOT"]).expanduser())
    cwd = Path.cwd()
    candidates.extend([cwd, *cwd.parents])

    for candidate in candidates:
        resolved = candidate.resolve()
        if is_project_root(resolved):
            return resolved
        nested = resolved / PROJECT_SUBDIR
        if is_project_root(nested):
            return nested

    if required:
        raise SystemExit(
            "Cannot find AKShare workbench project root. Run `init-project`, "
            "run from an existing workbench, or pass --root /path/to/akshare-workbench."
        )
    return None


def runtime_dir(root: Path) -> Path:
    path = root / RUNTIME_DIRNAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def pid_path(root: Path, name: str) -> Path:
    return runtime_dir(root) / f"{name}.pid"


def log_path(root: Path, name: str) -> Path:
    return runtime_dir(root) / f"{name}.log"


def read_pid(path: Path) -> int | None:
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return None


def is_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def python_bin(root: Path) -> str:
    if os.name == "nt":
        candidate = root / "backend" / ".venv" / "Scripts" / "python.exe"
    else:
        candidate = root / "backend" / ".venv" / "bin" / "python"
    return str(candidate if candidate.exists() else sys.executable)


def conservative_env(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("AKSHARE_WORKBENCH_ROOT", str(root))
    env.setdefault("AKSHARE_PROXY_MODE", "auto")
    env.setdefault("AKSHARE_MAX_CONCURRENT", "1")
    env.setdefault("AKSHARE_EASTMONEY_INTERVAL_SECONDS", "12")
    env.setdefault("AKSHARE_EASTMONEY_HTTP_RETRIES", "2")
    env.setdefault("AKSHARE_EASTMONEY_CALL_ATTEMPTS", "1")
    env.setdefault("AKSHARE_EASTMONEY_CACHE_TTL_SECONDS", "1800")
    env.setdefault("AKSHARE_RESULT_CACHE_TTL_SECONDS", "900")
    env.setdefault("AKSHARE_ENRICH_NAMES", "0")
    env.setdefault("AKSHARE_BACKEND_URL", f"http://127.0.0.1:{BACKEND_PORT}")
    env.setdefault(
        "AKSHARE_CORS_ORIGINS",
        f"http://localhost:{FRONTEND_PORT},http://127.0.0.1:{FRONTEND_PORT}",
    )
    return env


def popen_kwargs() -> dict:
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def run_checked(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    print(f"$ {' '.join(command)}")
    subprocess.run(command, cwd=str(cwd), env=env, check=True)


def ignore_runtime_files(_: str, names: list[str]) -> set[str]:
    ignored = {
        ".git",
        ".DS_Store",
        ".venv",
        "node_modules",
        "dist",
        ".cache",
        ".skill-runtime",
        ".pytest_cache",
        "__pycache__",
        ".env",
    }
    return {name for name in names if name in ignored or name.endswith(".pyc")}


def init_project(target: Path, *, force: bool = False) -> Path:
    source = bundled_project()
    if not is_project_root(source):
        raise SystemExit(f"Bundled project is missing or invalid: {source}")

    target = target.expanduser().resolve()
    if target.exists():
        if is_project_root(target) and not force:
            print(f"Project already exists: {target}")
            return target
        if any(target.iterdir()) and not force:
            nested = target / PROJECT_SUBDIR
            if is_project_root(nested):
                print(f"Project already exists: {nested}")
                return nested
            raise SystemExit(
                f"Target is not empty: {target}. Pass --force to replace it."
            )
        if force:
            shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=ignore_runtime_files)
    print(f"Created AKShare workbench project from bundled assets: {target}")
    return target


def setup(root: Path) -> None:
    backend = root / "backend"
    frontend = root / "frontend"
    venv_dir = backend / ".venv"

    if not venv_dir.exists():
        run_checked([sys.executable, "-m", "venv", ".venv"], backend)

    run_checked([python_bin(root), "-m", "pip", "install", "--upgrade", "pip"], backend)
    run_checked([python_bin(root), "-m", "pip", "install", "-r", "requirements.txt"], backend)

    if (frontend / "package-lock.json").exists():
        run_checked(["npm", "ci"], frontend)
    else:
        run_checked(["npm", "install"], frontend)


def doctor(root: Path, quiet: bool = False) -> bool:
    problems: list[str] = []
    if not is_project_root(root):
        problems.append(f"not an AKShare workbench root: {root}")
    if not (root / "backend" / ".venv").exists():
        problems.append("backend/.venv is missing; run setup")
    if not (root / "frontend" / "node_modules").exists():
        problems.append("frontend/node_modules is missing; run setup")
    if shutil.which("npm") is None:
        problems.append("npm is not on PATH")

    backend_pid = read_pid(pid_path(root, "backend"))
    frontend_pid = read_pid(pid_path(root, "frontend"))
    if port_open(BACKEND_PORT) and not is_alive(backend_pid):
        problems.append(f"port {BACKEND_PORT} is already in use by another process")
    if port_open(FRONTEND_PORT) and not is_alive(frontend_pid):
        problems.append(f"port {FRONTEND_PORT} is already in use by another process")

    if not quiet:
        if problems:
            print("doctor: problems found")
            for problem in problems:
                print(f"- {problem}")
        else:
            print("doctor: ok")
    if problems and quiet:
        for problem in problems:
            print(f"doctor: {problem}", file=sys.stderr)
    return not problems


def start_process(root: Path, name: str, cwd: Path, command: list[str]) -> None:
    existing = read_pid(pid_path(root, name))
    if is_alive(existing):
        print(f"{name} already running (pid {existing})")
        return

    log_file = log_path(root, name).open("ab")
    proc = subprocess.Popen(
        command,
        cwd=str(cwd),
        env=conservative_env(root),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        **popen_kwargs(),
    )
    pid_path(root, name).write_text(str(proc.pid), encoding="utf-8")
    print(f"started {name} pid={proc.pid}, log={log_path(root, name)}")


def start(root: Path) -> None:
    if not doctor(root, quiet=True):
        raise SystemExit("Start aborted. Run setup or resolve doctor findings first.")
    start_process(
        root,
        "backend",
        root / "backend",
        [
            python_bin(root),
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(BACKEND_PORT),
        ],
    )
    start_process(
        root,
        "frontend",
        root / "frontend",
        ["npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", str(FRONTEND_PORT)],
    )
    time.sleep(1.5)
    status(root)


def stop_process(root: Path, name: str) -> None:
    path = pid_path(root, name)
    pid = read_pid(path)
    if not is_alive(pid):
        print(f"{name} not running")
        path.unlink(missing_ok=True)
        return
    assert pid is not None
    try:
        if os.name == "nt":
            os.kill(pid, signal.CTRL_BREAK_EVENT)
        else:
            os.killpg(pid, signal.SIGTERM)
    except OSError:
        os.kill(pid, signal.SIGTERM)
    path.unlink(missing_ok=True)
    print(f"stopped {name} pid={pid}")


def stop(root: Path) -> None:
    stop_process(root, "frontend")
    stop_process(root, "backend")


def restart(root: Path) -> None:
    stop(root)
    time.sleep(0.8)
    start(root)


def http_ok(url: str) -> bool:
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(url, timeout=2) as response:
            return 200 <= response.status < 300
    except (OSError, urllib.error.URLError):
        return False


def status(root: Path) -> None:
    print(f"root: {root}")
    for name in ("backend", "frontend"):
        pid = read_pid(pid_path(root, name))
        state = "running" if is_alive(pid) else "stopped"
        suffix = f" pid={pid}" if pid else ""
        print(f"{name}: {state}{suffix}")
    print(
        "backend health: "
        f"{'ok' if http_ok(f'http://127.0.0.1:{BACKEND_PORT}/api/health') else 'unreachable'}"
    )
    print(f"frontend: http://127.0.0.1:{FRONTEND_PORT}")


def test(root: Path) -> None:
    run_checked([python_bin(root), "-m", "pytest"], root / "backend")
    run_checked(["npm", "run", "build"], root / "frontend")


def clear_cache(root: Path) -> None:
    cache_dir = root / "backend" / ".cache" / "results"
    count = 0
    if cache_dir.exists():
        for path in cache_dir.glob("*.pkl"):
            path.unlink(missing_ok=True)
            count += 1
    print(f"removed {count} cached result files from {cache_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Control the bundled AKShare workbench.")
    parser.add_argument(
        "action",
        choices=[
            "init-project",
            "setup",
            "doctor",
            "start",
            "stop",
            "restart",
            "status",
            "test",
            "clear-cache",
        ],
    )
    parser.add_argument("--root", help="AKShare workbench project root")
    parser.add_argument(
        "--target",
        default="akshare-workbench",
        help="Target directory for init-project (default: ./akshare-workbench)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace the target directory during init-project.",
    )
    args = parser.parse_args()

    if args.action == "init-project":
        init_project(Path(args.target), force=args.force)
        return 0

    root = find_project_root(args.root)
    assert root is not None

    if args.action == "setup":
        setup(root)
    elif args.action == "doctor":
        return 0 if doctor(root) else 1
    elif args.action == "start":
        start(root)
    elif args.action == "stop":
        stop(root)
    elif args.action == "restart":
        restart(root)
    elif args.action == "status":
        status(root)
    elif args.action == "test":
        test(root)
    elif args.action == "clear-cache":
        clear_cache(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
