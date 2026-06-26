#!/usr/bin/env python3
"""context-doctor.py — Visualize OpenClaw context window usage.

Scans workspace files, installed skills, and estimates token budget allocation.
Designed for terminal display and image export (chat sharing).

Usage:
    python3 context-doctor.py                          # terminal output
    python3 context-doctor.py --png /tmp/output.png    # PNG image
    python3 context-doctor.py --json                   # structured JSON
    python3 context-doctor.py --workspace ~/my-ws      # custom workspace
    python3 context-doctor.py --ctx-size 128000         # non-200k models

MIT License — https://github.com/jzOcb/context-doctor
"""

import argparse
import io
import json
import os
import select
import signal
import subprocess
import sys
import time

# ── ANSI colors ──────────────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

NO_COLOR = False


def c(color_code: str, text: str) -> str:
    """Apply color if colors are enabled."""
    if NO_COLOR:
        return str(text)
    # Re-apply outer color after any nested reset sequences in text.
    rendered = str(text).replace(RESET, f"{RESET}{color_code}")
    return f"{color_code}{rendered}{RESET}"


# ── Config ───────────────────────────────────────────────────────────────────

BOOTSTRAP_FILES = [
    "AGENTS.md", "SOUL.md", "TOOLS.md", "IDENTITY.md", "USER.md",
    "HEARTBEAT.md", "BOOTSTRAP.md", "MEMORY.md",
]
EXPECTED_MISSING = {"BOOTSTRAP.md"}

# Default max limits (OpenClaw defaults)
MAX_CHARS_PER_FILE = 20_000
MAX_CHARS_TOTAL = 150_000

# Default bootstrap overhead estimates (tokens) — calibrated from typical setups
DEFAULT_OVERHEAD = {
    "System Prompt (framework)": 3900,
    "Skills List": 1000,
    "Tool Schemas (JSON)": 4500,
    "Tool List + Summaries": 1850,
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def count_chars(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return len(f.read())
    except (OSError, IOError):
        return 0


def estimate_tokens(chars: int) -> int:
    return max(1, int(chars / 4)) if chars > 0 else 0


def bar(value: int, max_val: int, width: int = 20, color: str = GREEN) -> str:
    if max_val <= 0:
        return c(DIM, "░" * width)
    filled = int(value / max_val * width)
    filled = max(1, min(filled, width)) if value > 0 else 0
    return c(color, "█" * filled) + c(DIM, "░" * (width - filled))


def status_badge(s: str) -> str:
    if s == "OK":
        return c(BOLD + GREEN, "✓ OK")
    elif s == "MISSING":
        return c(DIM + RED, "✗ MISSING")
    elif s == "TRUNCATED":
        return c(BOLD + RED, "⚠ TRUNCATED")
    return s


def fmt_tok(chars: int, tok: int) -> str:
    return (
        f"{c(BRIGHT_WHITE, f'{chars:>6,}')} {c(DIM, 'chars')}  "
        f"{c(CYAN, f'{tok:>5,}')} {c(DIM, 'tok')}"
    )


def section(title: str, icon: str = "") -> None:
    print(f"\n  {c(BOLD + BRIGHT_CYAN, f'{icon} {title}')}")
    print(f"  {c(DIM, '─' * 60)}")


def get_version() -> str:
    try:
        r = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True, text=True, timeout=5,
        )
        if r.stdout.strip():
            return r.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return "unknown"


def find_workspace() -> str:
    """Resolve workspace path from env or default."""
    if os.environ.get("OPENCLAW_WORKSPACE"):
        return os.environ["OPENCLAW_WORKSPACE"]
    # Try openclaw config
    try:
        r = subprocess.run(
            ["openclaw", "config", "get"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0:
            cfg = json.loads(r.stdout)
            ws = cfg.get("workspace", {}).get("path")
            if ws:
                return os.path.expanduser(ws)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    return os.path.expanduser("~/.openclaw/workspace")


def find_skills(workspace: str) -> list:
    """Discover installed skills from system + workspace dirs."""
    dirs_to_scan = []

    # System skills
    system_candidates = [
        "/opt/homebrew/lib/node_modules/openclaw/skills",
        "/usr/local/lib/node_modules/openclaw/skills",
        "/usr/lib/node_modules/openclaw/skills",
    ]
    for d in system_candidates:
        if os.path.isdir(d):
            dirs_to_scan.append(("system", d))
            break

    # Workspace skills
    ws_skills = os.path.join(workspace, "skills")
    if os.path.isdir(ws_skills):
        dirs_to_scan.append(("workspace", ws_skills))

    # Home skills
    home_skills = os.path.expanduser("~/.agents/skills")
    if os.path.isdir(home_skills):
        dirs_to_scan.append(("global", home_skills))

    skills = []
    seen = set()
    for source, base_dir in dirs_to_scan:
        try:
            for name in sorted(os.listdir(base_dir)):
                if name in seen:
                    continue
                skill_md = os.path.join(base_dir, name, "SKILL.md")
                if os.path.isfile(skill_md):
                    chars = count_chars(skill_md)
                    tok = estimate_tokens(chars)
                    skills.append((name, source, chars, tok))
                    seen.add(name)
        except OSError:
            pass
    return skills


# ── Main ─────────────────────────────────────────────────────────────────────

def scan_workspace(workspace: str) -> list:
    """Scan workspace bootstrap files. Returns list of (name, status, chars, tok)."""
    files = []
    for name in BOOTSTRAP_FILES:
        path = os.path.join(workspace, name)
        is_link = os.path.islink(path)
        exists = os.path.exists(path)

        if exists:
            chars = count_chars(path)
            tok = estimate_tokens(chars)
            status = "OK"
            if chars >= MAX_CHARS_PER_FILE:
                status = "TRUNCATED"
            files.append((name, status, chars, tok))
        elif is_link:
            files.append((name, "MISSING", 0, 0))
        else:
            files.append((name, "MISSING", 0, 0))
    return files


def render_terminal(workspace: str, ctx_size: int) -> None:
    """Render the full context doctor report to terminal."""
    version = get_version()
    files = scan_workspace(workspace)
    skills = find_skills(workspace)

    total_chars = sum(f[2] for f in files)
    total_tok = sum(f[3] for f in files)
    max_chars = max((f[2] for f in files), default=1)

    # ── Header ──
    print()
    print(f"  {c(BOLD + BRIGHT_CYAN, '🧠 OpenClaw Context Window Breakdown')}  {c(DIM, f'({version})')}")
    print(f"  {c(DIM, '━' * 60)}")
    print(f"""
  {c(DIM, 'Workspace')}    {c(WHITE, workspace)}
  {c(DIM, 'Max/file')}     {c(YELLOW, f'{MAX_CHARS_PER_FILE:,}')} chars
  {c(DIM, 'Max/total')}    {c(YELLOW, f'{MAX_CHARS_TOTAL:,}')} chars""")

    # ── Workspace Files ──
    section("Workspace Files", "📁")
    for name, status, chars, tok in files:
        if status == "MISSING" and name in EXPECTED_MISSING:
            continue
        badge = status_badge(status)
        if status == "MISSING":
            print(f"  {c(DIM, f'{name:<15}')} {badge}")
        else:
            b = bar(chars, max_chars)
            print(f"  {c(BRIGHT_WHITE, f'{name:<15}')} {badge}  {b}  {fmt_tok(chars, tok)}")

    print(f"  {c(DIM, '─' * 60)}")
    label = "Total"
    print(f"  {c(BOLD, f'{label:<15}')}               {'':>20}  {fmt_tok(total_chars, total_tok)}")

    # ── Health warnings ──
    truncated = [f for f in files if f[1] == "TRUNCATED"]
    missing = [f for f in files if f[1] == "MISSING" and f[0] not in EXPECTED_MISSING]
    if truncated or missing:
        section("⚠️  Warnings", "")
        for name, status, chars, tok in truncated:
            print(f"  {c(BRIGHT_RED, f'🔴 {name}')} is TRUNCATED ({chars:,} chars > {MAX_CHARS_PER_FILE:,} limit)")
            print(f"     {c(DIM, 'Instructions may be silently cut. Reduce file size or split content.')}")
        for name, status, chars, tok in missing:
            print(f"  {c(BRIGHT_YELLOW, f'🟡 {name}')} is MISSING")
            print(f"     {c(DIM, 'Check if file was deleted or symlink target moved.')}")

    # ── Skills ──
    section("Installed Skills", "🔧")
    if skills:
        max_s = max(s[2] for s in skills) if skills else 1
        display_count = 12
        for name, source, chars, tok in skills[:display_count]:
            src_tag = c(DIM, f"[{source[:3]}]")
            b = bar(chars, max_s, 15, MAGENTA)
            print(f"  {c(WHITE, f'{name:<22}')} {src_tag} {b}  {fmt_tok(chars, tok)}")
        if len(skills) > display_count:
            print(f"  {c(DIM, f'… (+{len(skills) - display_count} more)')}")
        sk_total = sum(s[2] for s in skills)
        print(f"  {c(DIM, f'Total: {len(skills)} skills, {sk_total:,} chars on disk (loaded on-demand, not in bootstrap)')}")
    else:
        print(f"  {c(DIM, 'No skills found')}")

    # ── Token Budget ──
    section("Token Budget", "📊")

    segments = [
        ("System Prompt (framework)", DEFAULT_OVERHEAD["System Prompt (framework)"], BLUE),
        ("Workspace Files", total_tok, GREEN),
        ("Skills List", DEFAULT_OVERHEAD["Skills List"], MAGENTA),
        ("Tool Schemas (JSON)", DEFAULT_OVERHEAD["Tool Schemas (JSON)"], YELLOW),
        ("Tool List + Summaries", DEFAULT_OVERHEAD["Tool List + Summaries"], CYAN),
    ]
    grand_tok = sum(s[1] for s in segments)

    print(f"\n  {'Component':<30} {'Tokens':>8}  {'%':>5}  Visual")
    print(f"  {c(DIM, '─' * 60)}")
    for name, tok, color in segments:
        pct = tok / ctx_size * 100
        b = bar(tok, ctx_size, 25, color)
        print(f"  {c(WHITE, f'{name:<30}')} {c(BRIGHT_WHITE, f'{tok:>6,}')}  {c(DIM, f'{pct:>4.1f}%')}  {b}")

    print(f"  {c(DIM, '─' * 60)}")
    used_pct = grand_tok / ctx_size * 100
    free = ctx_size - grand_tok
    bt_label = "Bootstrap Total"
    free_label = "Free for conversation"
    print(f"  {c(BOLD, f'{bt_label:<30}')} {c(BRIGHT_WHITE, f'{grand_tok:>6,}')}  "
          f"{c(BRIGHT_GREEN, f'{used_pct:>4.1f}%')}  {c(DIM, f'of {ctx_size:,} ctx')}")
    print(f"  {c(BOLD + GREEN, f'{free_label:<30}')} {c(BRIGHT_GREEN, f'{free:>6,}')}  "
          f"{c(BRIGHT_GREEN, f'{100 - used_pct:>4.1f}%')}")

    # ── Health score ──
    print()
    if used_pct < 10:
        print(f"  {c(BRIGHT_GREEN, '🟢 Healthy')} — bootstrap uses {used_pct:.1f}% of context window")
    elif used_pct < 15:
        print(f"  {c(BRIGHT_YELLOW, '🟡 Moderate')} — bootstrap uses {used_pct:.1f}%, consider trimming workspace files")
    else:
        print(f"  {c(BRIGHT_RED, '🔴 Heavy')} — bootstrap uses {used_pct:.1f}%, agent may lose conversation context early")

    if truncated:
        print(f"  {c(BRIGHT_RED, f'🔴 {len(truncated)} file(s) TRUNCATED')} — agent is flying blind on cut instructions")

    print(f"\n  {c(DIM, f'OpenClaw {version} • context-doctor')}")
    print()


def generate_summary(workspace: str, ctx_size: int) -> str:
    """Generate a concise text summary of context window health."""
    files = scan_workspace(workspace)
    skills = find_skills(workspace)
    version = get_version()

    total_chars = sum(f[2] for f in files)
    total_tok = sum(f[3] for f in files)
    grand_tok = total_tok + sum(DEFAULT_OVERHEAD.values())
    used_pct = grand_tok / ctx_size * 100
    free_pct = 100 - used_pct

    truncated = [f for f in files if f[1] == "TRUNCATED"]
    missing = [f for f in files if f[1] == "MISSING" and f[0] not in EXPECTED_MISSING]
    ok_files = [f for f in files if f[1] == "OK"]

    lines = []
    lines.append(f"🧠 Context Doctor — OpenClaw {version}")
    lines.append("")

    # Health verdict
    if used_pct < 10:
        lines.append(f"🟢 Healthy — bootstrap {used_pct:.1f}%, conversation space {free_pct:.1f}%")
    elif used_pct < 15:
        lines.append(f"🟡 Moderate — bootstrap {used_pct:.1f}%, consider trimming")
    else:
        lines.append(f"🔴 Heavy — bootstrap {used_pct:.1f}%, agent may lose context early")
    lines.append("")

    # Files summary
    lines.append(f"📁 Workspace: {len(ok_files)} files OK, {total_chars:,} chars ({total_tok:,} tok)")
    if truncated:
        for f in truncated:
            lines.append(f"  ⚠️ {f[0]} TRUNCATED ({f[2]:,} chars) — instructions silently cut!")
    if missing:
        for f in missing:
            lines.append(f"  ❌ {f[0]} MISSING")

    # Top 3 largest files
    sorted_files = sorted([f for f in files if f[1] == "OK"], key=lambda x: x[2], reverse=True)
    if sorted_files:
        top3 = sorted_files[:3]
        lines.append(f"  📊 Largest: {', '.join(f'{f[0]}({f[3]}tok)' for f in top3)}")

    lines.append("")

    # Budget breakdown
    lines.append(f"📊 Token Budget ({ctx_size:,} ctx window):")
    lines.append(f"  Bootstrap: {grand_tok:,} tok ({used_pct:.1f}%)")
    lines.append(f"  Free: {ctx_size - grand_tok:,} tok ({free_pct:.1f}%)")
    lines.append("")
    lines.append(f"🔧 {len(skills)} skills installed (loaded on-demand, not in bootstrap)")

    return "\n".join(lines)


def render_png(workspace: str, ctx_size: int, output_path: str) -> None:
    """Render the visualization as a PNG image (for chat/share use).

    Uses Rich to capture ANSI output → SVG, then converts to PNG.
    Requires: rich (Python), rsvg-convert (brew) or cairosvg (pip).
    """
    try:
        from rich.console import Console as RichConsole
        from rich.text import Text as RichText
    except ImportError:
        print("Error: 'rich' package required for PNG output. Install: pip3 install rich", file=sys.stderr)
        sys.exit(1)

    # Capture the terminal output via PTY to preserve ANSI codes
    import pty as pty_mod

    script_path = os.path.abspath(__file__)
    env = {
        **os.environ,
        "FORCE_COLOR": "1",
        "TERM": "xterm-256color",
        "PYTHONIOENCODING": "utf-8",
        "COLUMNS": "85",
        "LINES": "60",
    }
    if workspace:
        env["OPENCLAW_WORKSPACE"] = workspace

    output_path = os.path.abspath(os.path.expanduser(output_path))
    if output_path.endswith(os.sep) or os.path.isdir(output_path):
        print(f"Error: output path must be a file, got directory: {output_path}", file=sys.stderr)
        sys.exit(1)
    base, _ext = os.path.splitext(output_path)
    if not base:
        print(f"Error: invalid output path: {output_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = os.path.dirname(output_path) or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)
    svg_path = base + ".svg"

    raw = b""
    pid = -1
    fd = -1
    capture_timeout_sec = 30
    start = time.monotonic()
    try:
        pid, fd = pty_mod.fork()
        if pid == 0:
            # Child — run ourselves in terminal mode (no --png to avoid recursion)
            os.environ.update(env)
            cmd = [sys.executable, script_path]
            if workspace:
                cmd += ["--workspace", workspace]
            cmd += ["--ctx-size", str(ctx_size)]
            os.execvp(sys.executable, cmd)
            os._exit(127)

        while True:
            if time.monotonic() - start > capture_timeout_sec:
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
                print("Error: timed out while capturing terminal output for PNG rendering", file=sys.stderr)
                sys.exit(1)

            readable, _, _ = select.select([fd], [], [], 0.5)
            if not readable:
                try:
                    waited_pid, _ = os.waitpid(pid, os.WNOHANG)
                    if waited_pid == pid:
                        break
                except ChildProcessError:
                    break
                continue

            try:
                data = os.read(fd, 4096)
                if not data:
                    break
                raw += data
            except OSError:
                # PTY EOF commonly surfaces as OSError(EIO).
                break
    finally:
        if fd >= 0:
            try:
                os.close(fd)
            except OSError:
                pass
        if pid > 0:
            try:
                os.waitpid(pid, 0)
            except (ChildProcessError, OSError):
                pass

    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "")

    # Render with Rich — capture to StringIO so ANSI noise stays off stdout
    console = RichConsole(record=True, width=85, force_terminal=True, file=io.StringIO())
    console.print(RichText.from_ansi(text))
    svg = console.export_svg(title="context-doctor")

    # Write SVG
    with open(svg_path, "w") as f:
        f.write(svg)

    # Convert SVG → PNG (try multiple backends)
    converted = False

    # Try rsvg-convert
    try:
        subprocess.run(
            ["rsvg-convert", svg_path, "-o", output_path, "-z", "2"],
            check=True, capture_output=True,
        )
        converted = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # Try cairosvg
    if not converted:
        try:
            import cairosvg
            cairosvg.svg2png(url=svg_path, write_to=output_path, scale=2)
            converted = True
        except (ImportError, Exception):
            pass

    if converted:
        # Clean up SVG
        try:
            os.remove(svg_path)
        except OSError:
            pass
        print(output_path)
    else:
        # Fall back to SVG
        if svg_path != output_path:
            os.rename(svg_path, base + ".svg")
        print(
            f"Warning: could not convert to PNG (install rsvg-convert or cairosvg). SVG saved.",
            file=sys.stderr,
        )
        print(svg_path)


def render_json(workspace: str, ctx_size: int) -> None:
    """Output structured JSON for programmatic use."""
    files = scan_workspace(workspace)
    skills = find_skills(workspace)
    total_tok = sum(f[3] for f in files)
    grand_tok = total_tok + sum(DEFAULT_OVERHEAD.values())

    result = {
        "version": get_version(),
        "workspace": workspace,
        "ctx_size": ctx_size,
        "files": [
            {"name": f[0], "status": f[1], "chars": f[2], "tokens": f[3]}
            for f in files
        ],
        "skills": [
            {"name": s[0], "source": s[1], "chars": s[2], "tokens": s[3]}
            for s in skills
        ],
        "budget": {
            "bootstrap_tokens": grand_tok,
            "bootstrap_pct": round(grand_tok / ctx_size * 100, 1),
            "free_tokens": ctx_size - grand_tok,
            "free_pct": round((ctx_size - grand_tok) / ctx_size * 100, 1),
            "components": {
                **DEFAULT_OVERHEAD,
                "Workspace Files": total_tok,
            },
        },
        "warnings": {
            "truncated": [f[0] for f in files if f[1] == "TRUNCATED"],
            "missing": [f[0] for f in files if f[1] == "MISSING" and f[0] not in EXPECTED_MISSING],
        },
    }
    print(json.dumps(result, indent=2))


def main():
    global NO_COLOR

    parser = argparse.ArgumentParser(
        description="Visualize OpenClaw context window usage",
    )
    parser.add_argument(
        "--workspace", "-w",
        help="Workspace path (default: auto-detect)",
    )
    parser.add_argument(
        "--ctx-size", "-c",
        type=int, default=200_000,
        help="Context window size in tokens (default: 200000)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of terminal visualization",
    )
    parser.add_argument(
        "--png", metavar="PATH",
        help="Render as PNG image to PATH (for sharing in chat)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a concise text summary (use with --png for image + text)",
    )
    args = parser.parse_args()

    if args.ctx_size <= 0:
        print("Error: --ctx-size must be > 0", file=sys.stderr)
        sys.exit(1)
    if args.png and args.json:
        print("Error: --png and --json cannot be used together", file=sys.stderr)
        sys.exit(2)

    NO_COLOR = args.no_color or not sys.stdout.isatty()

    workspace = args.workspace or find_workspace()
    workspace = os.path.expanduser(workspace)

    if not os.path.isdir(workspace):
        print(f"Error: workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)

    if args.png:
        render_png(workspace, args.ctx_size, args.png)
        if args.summary:
            print("---")
            print(generate_summary(workspace, args.ctx_size))
    elif args.json:
        render_json(workspace, args.ctx_size)
    elif args.summary:
        print(generate_summary(workspace, args.ctx_size))
    else:
        render_terminal(workspace, args.ctx_size)


if __name__ == "__main__":
    main()
