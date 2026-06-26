#!/usr/bin/env python3
"""Claude Code status line renderer.

Reads JSON from stdin (provided by Claude Code), outputs a colored status line.
Format: user@host:dir (branch ↑N↓M) | Model | In:X Out:Y Cache:Z [████░░ 23%]

Dynamic 2-line split when output exceeds terminal width.
Configuration loaded from ~/.claude/statusline.config if it exists (perms 600/400).
"""

import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

MAX_INPUT_SIZE = 1_048_576  # 1 MB

CONFIG_FILE = Path.home() / ".claude" / "statusline.config"

# ANSI escape helpers
RESET = "\033[0m"
GREEN = "\033[32m"
BLUE = "\033[34m"
CYAN = "\033[36m"
DIM = "\033[90m"

# Defaults (overridden by config file)
DEFAULTS = {
    "TOKEN_DISPLAY": "separate",
    "THRESHOLD_YELLOW": 40,
    "THRESHOLD_ORANGE": 50,
    "THRESHOLD_RED": 70,
    "COLOR_GREEN": "\033[32m",
    "COLOR_YELLOW": "\033[33m",
    "COLOR_ORANGE": "\033[38;5;208m",
    "COLOR_RED": "\033[31m",
}

# Config variable whitelist for safe parsing
ALLOWED_CONFIG_KEYS = {
    "TOKEN_DISPLAY", "THRESHOLD_YELLOW", "THRESHOLD_ORANGE", "THRESHOLD_RED",
    "COLOR_GREEN", "COLOR_YELLOW", "COLOR_ORANGE", "COLOR_RED",
}

COLOR_NAMES = {
    "green": "32", "yellow": "33", "orange": "38;5;208", "red": "31",
    "blue": "34", "cyan": "36", "magenta": "35", "purple": "35",
    "white": "37", "pink": "38;5;213",
    "bright-green": "92", "bright-yellow": "93", "bright-red": "91",
    "bright-blue": "94", "bright-cyan": "96", "bright-magenta": "95",
}


def load_config(config_path=None):
    """Load and validate config file. Returns dict of settings.

    Security: only accepts specific keys, validates all values,
    requires file perms 600 or 400, rejects symlinks.
    """
    path = Path(config_path) if config_path else CONFIG_FILE
    cfg = dict(DEFAULTS)

    if not path.exists() or path.is_symlink():
        return cfg

    # Check ownership and permissions
    try:
        st = path.stat()
        perms = oct(st.st_mode & 0o777)
        if perms not in ("0o600", "0o400"):
            return cfg
        if st.st_uid != os.getuid():
            return cfg
    except OSError:
        return cfg

    try:
        text = path.read_text()
    except OSError:
        return cfg

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip("'\"")

        if key not in ALLOWED_CONFIG_KEYS:
            continue

        if key == "TOKEN_DISPLAY" and val in ("separate", "combined"):
            cfg[key] = val
        elif key.startswith("THRESHOLD_"):
            try:
                n = int(val)
                if 0 <= n <= 100:
                    cfg[key] = n
            except ValueError:
                pass
        elif key.startswith("COLOR_"):
            ansi = _parse_color(val)
            if ansi:
                cfg[key] = ansi

    # Validate threshold ordering; reset to defaults if invalid
    if not (cfg["THRESHOLD_YELLOW"] <= cfg["THRESHOLD_ORANGE"] <= cfg["THRESHOLD_RED"]):
        cfg["THRESHOLD_YELLOW"] = DEFAULTS["THRESHOLD_YELLOW"]
        cfg["THRESHOLD_ORANGE"] = DEFAULTS["THRESHOLD_ORANGE"]
        cfg["THRESHOLD_RED"] = DEFAULTS["THRESHOLD_RED"]

    return cfg


def _parse_color(val):
    """Convert color name or code to ANSI escape sequence. Returns str or None."""
    low = val.lower()
    if low in COLOR_NAMES:
        return f"\033[{COLOR_NAMES[low]}m"
    # Accept raw escape sequences like \033[32m
    if val.startswith("\\033[") and val.endswith("m"):
        inner = val[5:-1]
        if re.match(r"^[0-9;]+$", inner):
            return f"\033[{inner}m"
    # Accept raw numeric codes like "32" or "38;5;208"
    if re.match(r"^[0-9;]+$", val):
        return f"\033[{val}m"
    return None


def format_tokens(n):
    """Format token count: 1500 -> '1.5K', 800 -> '800'."""
    if not isinstance(n, int) or n < 0:
        return "0"
    if n >= 1000:
        thousands = n // 1000
        decimal = (n % 1000) // 100
        return f"{thousands}.{decimal}K"
    return str(n)


def get_git_branch(cwd):
    """Get current git branch or short hash. Returns str or empty string."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "symbolic-ref", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if result.returncode == 0:
            return _sanitize(result.stdout.strip(), 128)
        # Detached HEAD -- try short hash
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if result.returncode == 0:
            return _sanitize(result.stdout.strip(), 128)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return ""


def get_git_ahead_behind(cwd):
    """Get ahead/behind counts vs upstream. Returns e.g. '↑2↓1', '↑3', '↓1', or ''."""
    git_env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        # Check upstream exists
        check = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "@{u}"],
            capture_output=True, text=True, timeout=5, env=git_env,
        )
        if check.returncode != 0:
            return ""

        ahead_result = subprocess.run(
            ["git", "-C", cwd, "rev-list", "HEAD...@{u}", "--left-only", "--count"],
            capture_output=True, text=True, timeout=5, env=git_env,
        )
        behind_result = subprocess.run(
            ["git", "-C", cwd, "rev-list", "HEAD...@{u}", "--right-only", "--count"],
            capture_output=True, text=True, timeout=5, env=git_env,
        )
        ahead = int(ahead_result.stdout.strip()) if ahead_result.returncode == 0 else 0
        behind = int(behind_result.stdout.strip()) if behind_result.returncode == 0 else 0

        parts = []
        if ahead > 0:
            parts.append(f"↑{ahead}")
        if behind > 0:
            parts.append(f"↓{behind}")
        return "".join(parts)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError, ValueError):
        pass
    return ""


def visible_len(s):
    """Return visible length of string after stripping ANSI escape sequences."""
    return len(re.sub(r"\033\[[0-9;]*[a-zA-Z]", "", s))


def render_progress_bar(pct, cfg, width=20):
    """Render a colored progress bar like [████████░░ 23%]."""
    pct = max(0, min(pct, 100))
    filled = round(pct * width / 100)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    color = get_pct_color(pct, cfg)
    return f"{color}[{bar} {pct}%]{RESET}"


def _sanitize(s, max_len=1024):
    """Remove control characters and ANSI escape sequences, truncate."""
    # Strip ANSI escape sequences
    s = re.sub(r"\033\[[0-9;]*[a-zA-Z]", "", s)
    # Strip other control chars (keep printable + space)
    s = "".join(c for c in s if c == "\t" or c == "\n" or (ord(c) >= 32 and ord(c) != 127))
    return s[:max_len]


def _safe_int(data, *keys, default=0):
    """Extract nested int from dict, returning default on any failure."""
    obj = data
    for k in keys:
        if not isinstance(obj, dict):
            return default
        obj = obj.get(k)
        if obj is None:
            return default
    if not isinstance(obj, (int, float)):
        return default
    n = int(obj)
    return n if n >= 0 else default


def _safe_str(data, *keys, default=""):
    """Extract nested string from dict, returning default on any failure."""
    obj = data
    for k in keys:
        if not isinstance(obj, dict):
            return default
        obj = obj.get(k)
        if obj is None:
            return default
    if not isinstance(obj, str):
        return default
    return _sanitize(obj)


def get_pct_color(pct, cfg):
    """Return ANSI color code for a given context usage percentage."""
    if pct >= cfg["THRESHOLD_RED"]:
        return cfg["COLOR_RED"]
    if pct >= cfg["THRESHOLD_ORANGE"]:
        return cfg["COLOR_ORANGE"]
    if pct >= cfg["THRESHOLD_YELLOW"]:
        return cfg["COLOR_YELLOW"]
    return cfg["COLOR_GREEN"]


def render(data, cfg):
    """Render the status line string from parsed JSON and config."""
    # Working directory
    cwd = _safe_str(data, "workspace", "current_dir", default=str(Path.home()))
    resolved = str(Path(cwd).resolve()) if cwd else str(Path.home())

    # User and host
    user = _sanitize(os.environ.get("USER", "user"), 64)
    try:
        host = _sanitize(socket.gethostname().split(".")[0], 64)
    except Exception:
        host = "localhost"

    # Directory display
    home = str(Path.home())
    if resolved == home:
        dir_display = "~"
    else:
        dir_display = _sanitize(Path(resolved).name, 256) or "/"

    # Git branch + dirty + ahead/behind
    git_part = ""
    branch = get_git_branch(resolved)
    if branch:
        ahead_behind = get_git_ahead_behind(resolved)
        git_part = f" ({branch}{ahead_behind})"

    # Model
    model = _safe_str(data, "model", "display_name", default="unknown")

    # Tokens
    input_tokens = _safe_int(data, "context_window", "current_usage", "input_tokens")
    output_tokens = _safe_int(data, "context_window", "current_usage", "output_tokens")
    cache_creation = _safe_int(data, "context_window", "current_usage", "cache_creation_input_tokens")
    cache_read = _safe_int(data, "context_window", "current_usage", "cache_read_input_tokens")
    ctx_size = _safe_int(data, "context_window", "context_window_size", default=1)

    token_info = ""
    pct = 0
    progress_bar = ""
    if any((input_tokens, output_tokens, cache_creation, cache_read)):
        cache_total = cache_creation + cache_read
        current = input_tokens + cache_creation + cache_read
        if ctx_size <= 0:
            ctx_size = 1
        pct = min(current * 100 // ctx_size, 100)
        pct_color = get_pct_color(pct, cfg)
        progress_bar = " " + render_progress_bar(pct, cfg)

        if cfg["TOKEN_DISPLAY"] == "combined":
            total = input_tokens + output_tokens + cache_total
            token_info = (
                f" {DIM}|{RESET} Tokens:{format_tokens(total)}"
            )
        else:
            token_info = (
                f" {DIM}|{RESET}"
                f" In:{format_tokens(input_tokens)}"
                f" Out:{format_tokens(output_tokens)}"
                f" Cache:{format_tokens(cache_total)}"
            )

    base = (
        f"{GREEN}{user}@{host}{RESET}"
        f":{BLUE}{dir_display}{RESET}"
        f"{git_part}"
        f" {DIM}|{RESET}"
        f" {CYAN}{model}{RESET}"
        f"{token_info}"
    )

    if not progress_bar:
        return base

    # Dynamic layout: single line if fits, two lines if too wide
    full_line = base + progress_bar
    try:
        term_width = os.get_terminal_size().columns
    except (ValueError, OSError):
        term_width = 120

    if visible_len(full_line) <= term_width:
        return full_line

    # Two-line layout: base with compact [pct%] on line 1, progress bar on line 2
    pct_color = get_pct_color(pct, cfg)
    compact_pct = f" {pct_color}[{pct}%]{RESET}"
    return base + compact_pct + "\n  " + render_progress_bar(pct, cfg)


def main():
    raw = sys.stdin.buffer.read(MAX_INPUT_SIZE)
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        print(f"\033[31mInvalid JSON input\033[0m", end="")
        sys.exit(1)

    cfg = load_config()
    print(render(data, cfg), end="")


if __name__ == "__main__":
    main()
