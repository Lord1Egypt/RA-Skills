#!/usr/bin/env python3
from __future__ import annotations

import ctypes
import json
import os
import shutil
import subprocess
import sys
import winreg
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_ROOT = SCRIPT_PATH.parent
SKILL_ROOT = SCRIPT_ROOT.parent
REPO_ROOT = SKILL_ROOT.parents[1]
REFERENCE_PS1 = SKILL_ROOT / "references" / "everything-cli.ps1.txt"
CACHE_ROOT = Path(os.environ.get("LOCALAPPDATA") or os.environ.get("TEMP") or str(Path.home())) / "agent-everything.exe"
RUNTIME_ROOT = CACHE_ROOT / "runtime"
RUNTIME_PS1 = RUNTIME_ROOT / "everything-cli.ps1"


def find_powershell() -> str:
    for candidate in ("pwsh.exe", "powershell.exe"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise RuntimeError("PowerShell is required but pwsh.exe and powershell.exe were not found on PATH.")


def materialize_runtime_script() -> Path:
    source = REFERENCE_PS1.read_text(encoding="utf-8")
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    if not RUNTIME_PS1.exists() or RUNTIME_PS1.read_text(encoding="utf-8") != source:
        RUNTIME_PS1.write_text(source, encoding="utf-8")
    return RUNTIME_PS1


def run_runtime(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    runtime_script = materialize_runtime_script()
    powershell = find_powershell()
    env = os.environ.copy()
    env["EVERYTHING_CLI_SKILL_ROOT"] = str(SKILL_ROOT)
    env["EVERYTHING_CLI_REPO_ROOT"] = str(REPO_ROOT)
    env["EVERYTHING_CLI_CACHE_ROOT"] = str(CACHE_ROOT)
    return subprocess.run(
        [
            powershell,
            "-NoLogo",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(runtime_script),
            *arguments,
        ],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


def normalize_path(path_text: str | os.PathLike[str]) -> str:
    return os.path.normcase(os.path.normpath(str(path_text)))


def choose_default_shim_dir() -> Path:
    env_override = os.environ.get("EVERYTHING_CLI_SHIM_DIR")
    if env_override:
        return Path(env_override).expanduser()
    return Path.home() / ".local" / "bin"


def render_cmd_shim(script_path: Path) -> str:
    quoted_script = str(script_path)
    return (
        "@echo off\r\n"
        "setlocal\r\n"
        f"set \"SCRIPT={quoted_script}\"\r\n"
        "where py.exe >nul 2>&1\r\n"
        "if %ERRORLEVEL% EQU 0 (\r\n"
        "  py -3 \"%SCRIPT%\" %*\r\n"
        "  exit /b %ERRORLEVEL%\r\n"
        ")\r\n"
        "where python.exe >nul 2>&1\r\n"
        "if %ERRORLEVEL% EQU 0 (\r\n"
        "  python \"%SCRIPT%\" %*\r\n"
        "  exit /b %ERRORLEVEL%\r\n"
        ")\r\n"
        "where python3.exe >nul 2>&1\r\n"
        "if %ERRORLEVEL% EQU 0 (\r\n"
        "  python3 \"%SCRIPT%\" %*\r\n"
        "  exit /b %ERRORLEVEL%\r\n"
        ")\r\n"
        "echo Python 3 is required.>&2\r\n"
        "exit /b 1\r\n"
    )


def read_user_path() -> str:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
            value, _ = winreg.QueryValueEx(key, "Path")
            return value
    except FileNotFoundError:
        return ""


def write_user_path(value: str) -> None:
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, value)


def broadcast_environment_change() -> None:
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_size_t()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        "Environment",
        SMTO_ABORTIFHUNG,
        5000,
        ctypes.byref(result),
    )


def ensure_user_path_contains(shim_dir: Path) -> bool:
    shim_norm = normalize_path(shim_dir)
    current_value = read_user_path()
    parts = [part.strip() for part in current_value.split(";") if part.strip()]
    if any(normalize_path(part) == shim_norm for part in parts):
        return False
    parts.append(str(shim_dir))
    write_user_path(";".join(parts))
    os.environ["PATH"] = f"{shim_dir};{os.environ.get('PATH', '')}"
    broadcast_environment_change()
    return True


def install_shims(shim_dir: Path) -> dict[str, object]:
    shim_dir.mkdir(parents=True, exist_ok=True)
    ev_cmd = shim_dir / "ev.cmd"
    explicit_cmd = shim_dir / "everything-cli.cmd"
    explicit_cmd.write_text(render_cmd_shim(SCRIPT_PATH), encoding="utf-8", newline="")
    ev_cmd.write_text('@echo off\r\ncall "%~dp0everything-cli.cmd" %*\r\n', encoding="utf-8", newline="")
    path_updated = ensure_user_path_contains(shim_dir)
    return {
        "installed": True,
        "shimDir": str(shim_dir),
        "pathUpdated": path_updated,
        "evCmd": str(ev_cmd),
        "everythingCliCmd": str(explicit_cmd),
    }


def parse_ensure_install_options(arguments: list[str]) -> tuple[bool, Path | None]:
    install_shim = False
    shim_dir: Path | None = None
    index = 0
    while index < len(arguments):
        token = arguments[index]
        if token == "--install-shim":
            install_shim = True
        elif token == "--shim-dir":
            if index + 1 >= len(arguments):
                raise RuntimeError("Missing value for --shim-dir.")
            shim_dir = Path(arguments[index + 1]).expanduser()
            index += 1
        index += 1
    return install_shim, shim_dir


def print_passthrough(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)


def main() -> int:
    arguments = sys.argv[1:]
    command = arguments[0].lower() if arguments else "help"

    if command == "ensure":
        install_shim, requested_shim_dir = parse_ensure_install_options(arguments[1:])
        result = run_runtime(arguments)
        if result.returncode != 0:
            print_passthrough(result)
            return result.returncode

        if not install_shim:
            print_passthrough(result)
            return 0

        shim_info = install_shims(requested_shim_dir or choose_default_shim_dir())
        payload = json.loads(result.stdout) if result.stdout.strip() else {"ok": True}
        payload["shim"] = shim_info
        print(json.dumps(payload, indent=2))
        return 0

    result = run_runtime(arguments)
    print_passthrough(result)
    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
