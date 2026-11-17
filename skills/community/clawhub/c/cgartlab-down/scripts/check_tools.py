#!/usr/bin/env python3
"""Tool availability checker for the `down` skill.

Usage:
    python check_tools.py                                  # 全量检查
    python check_tools.py --tool curl                      # 只查一个
    python check_tools.py --required yt-dlp aria2c         # 指定必需集
    python check_tools.py --json                           # 结构化输出

Emits a JSON object on stdout describing which tools are available.
Exit code 0 always (except on bad usage) — caller inspects the JSON
and decides whether to prompt user to install missing tools.

Design notes:
  * Read-only. Never installs, never modifies PATH permanently.
  * Zero third-party deps — stdlib only, Python 3.9+.
  * No network calls — checks local filesystem only.
  * Windows: automatically extends PATH to %LOCALAPPDATA%\\.local\\bin
    (where `uv tool install` places binaries). POSIX: also checks
    ~/.local/bin for consistency.
  * On tool missing, returns install_hint text — caller decides
    whether to prompt the user (per SKILL.md rule 1: 不静默安装).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


# --- Tool metadata -----------------------------------------------------------

TOOL_REGISTRY: dict[str, dict] = {
    "curl": {
        "required_for": "direct_file (and all HTTP downloads)",
        "version_cmd": ["curl", "--version"],
        "expected_version_regex": r"\d+\.\d+\.\d+",
        "fallback": "系统通常自带；缺失时需手动安装",
    },
    "yt-dlp": {
        "required_for": "platform_video (YouTube / X / Bilibili / ...)",
        "version_cmd": ["yt-dlp", "--version"],
        "expected_version_regex": r"\d{4}\.\d{2}\.\d{2}",
        "install_hint": {
            "windows": "uv tool install yt-dlp",
            "linux": "uv tool install yt-dlp  (or pipx install yt-dlp)",
            "macos": "uv tool install yt-dlp  (or brew install yt-dlp)",
        },
        "expected_size_mb": 3,
    },
    "aria2c": {
        "required_for": "torrent/magnet content (rare — usually only for .torrent files, which now use curl)",
        "version_cmd": ["aria2c", "--version"],
        "expected_version_regex": r"\d+\.\d+\.\d+",
        "install_hint": {
            "windows": "winget install -e --id aria2.aria2",
            "linux": "apt install -y aria2  (or dnf install -y aria2)",
            "macos": "brew install aria2",
        },
        "expected_size_mb": 4,
    },
}


# --- Platform detection ------------------------------------------------------

def detect_platform() -> str:
    """Return 'windows' / 'linux' / 'macos'."""
    sys_name = platform.system().lower()
    if sys_name == "windows":
        return "windows"
    if sys_name == "darwin":
        return "macos"
    return "linux"


# --- PATH extension ----------------------------------------------------------

def get_extended_path(platform_name: str) -> tuple[list[str], bool]:
    """Extend PATH with common tool locations.

    Returns (extra_dirs, was_extended).
    """
    extra = []
    home = os.path.expanduser("~")

    if platform_name == "windows":
        # uv tool install 默认位置：%LOCALAPPDATA%\.local\bin
        local_appdata = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        extra.append(str(Path(local_appdata) / ".local" / "bin"))
        # pipx 位置：%LOCALAPPDATA%\\Programs\\Python\\Scripts 或类似
        extra.append(str(Path(local_appdata) / "Programs" / "Python" / "Scripts"))
        # 用户级 git-bash 路径（少见）
        extra.append(str(Path.home() / ".local" / "bin"))
    else:
        # POSIX: ~/.local/bin
        extra.append(str(Path(home) / ".local" / "bin"))
        # /usr/local/bin（一般已在 PATH，但保险）
        extra.append("/usr/local/bin")

    return extra, True


# --- Version extraction ------------------------------------------------------

def run_version_cmd(cmd: list[str], timeout: float = 3.0) -> tuple[str | None, str | None]:
    """Run a version command and return (stdout, stderr).

    Never raises — returns (None, error_msg) on failure.
    """
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        return (r.stdout or "").strip(), (r.stderr or "").strip()
    except FileNotFoundError:
        return None, "binary not found"
    except subprocess.TimeoutExpired:
        return None, f"timeout after {timeout}s"
    except OSError as e:
        return None, str(e)


# --- Main check --------------------------------------------------------------

def check_tool(name: str, platform_name: str) -> dict:
    """Check a single tool's availability."""
    meta = TOOL_REGISTRY.get(name)
    if meta is None:
        return {"name": name, "available": False, "error": "unknown tool"}

    # Try without extension first (POSIX), then with .exe (Windows)
    candidates = [name] if platform_name != "windows" else [name, f"{name}.exe"]
    path = None
    for c in candidates:
        p = shutil.which(c)
        if p:
            path = p
            break

    if path is None:
        return {
            "name": name,
            "available": False,
            "path": None,
            "version": None,
            "required_for": meta["required_for"],
            "install_hint": meta.get("install_hint"),
            "expected_size_mb": meta.get("expected_size_mb"),
        }

    stdout, stderr = run_version_cmd(meta["version_cmd"])
    version = None
    if stdout:
        # Take first line, strip to fit
        version = stdout.splitlines()[0][:200]

    return {
        "name": name,
        "available": True,
        "path": path,
        "version": version,
        "required_for": meta["required_for"],
        "error": None,
    }


# --- Entry point -------------------------------------------------------------

def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description="Check download tool availability for the `down` skill."
    )
    p.add_argument("--tool", action="append",
                   help="Tool name to check (repeatable). Default: all tools.")
    p.add_argument("--required", nargs="*",
                   help="Tools that must be available (for verdict calculation).")
    p.add_argument("--json", action="store_true",
                   help="Emit JSON (default; kept for clarity)")
    args = p.parse_args(argv)

    platform_name = detect_platform()

    # Ensure extended PATH is visible to shutil.which
    extra_dirs, _ = get_extended_path(platform_name)
    for d in extra_dirs:
        if d not in os.environ.get("PATH", "").split(os.pathsep):
            if Path(d).is_dir():
                os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")

    # Determine which tools to check
    if args.tool:
        tool_names = args.tool
    else:
        tool_names = list(TOOL_REGISTRY.keys())

    tools_result = {t: check_tool(t, platform_name) for t in tool_names}

    missing = [t for t, r in tools_result.items() if not r["available"]]
    missing_required = [
        t for t in (args.required or [])
        if t in tools_result and not tools_result[t]["available"]
    ]

    # Verdict: pass / partial / fail
    if args.required:
        verdict = "pass" if not missing_required else "fail"
    else:
        verdict = "pass" if not missing else "partial"

    output = {
        "platform": platform_name,
        "path_extended": True,
        "extra_dirs_checked": [d for d in extra_dirs if Path(d).is_dir()],
        "tools": tools_result,
        "missing": missing,
        "missing_required": missing_required,
        "verdict": verdict,
    }

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
