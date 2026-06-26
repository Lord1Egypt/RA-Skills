#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BV_PATTERN = re.compile(r"(BV[0-9A-Za-z]+)", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Bilibili mindmap workflow.")
    parser.add_argument("--source", required=True, help="Bilibili video URL or BV number")
    parser.add_argument("--output-dir", help="Pipeline output directory")
    parser.add_argument("--xmind-output", help="Explicit output .xmind path")
    parser.add_argument("--login-if-needed", action="store_true", help="Run `bili login` when needed")
    parser.add_argument("--transcribe-if-needed", action="store_true", help="Use ASR fallback when subtitles are unavailable")
    parser.add_argument(
        "--workflow",
        choices=["host", "local"],
        default="host",
        help="`host` prepares context for the host LLM and renders when outline.md already exists; `local` uses the script fallback outline generator.",
    )
    parser.add_argument(
        "--asr-provider",
        choices=["auto", "moonshine", "parakeet", "aliyun"],
        default="auto",
        help="ASR provider selection. `auto` tries moonshine, parakeet, then aliyun.",
    )
    return parser.parse_args()


def make_utf8_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONLEGACYWINDOWSSTDIO", "1")
    return env


def run(command: list[str]) -> None:
    result = subprocess.run(command, check=False, env=make_utf8_env())
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def format_for_console(value: str) -> str:
    encoding = (getattr(sys.stdout, "encoding", None) or "").lower()
    if "utf" in encoding:
        return value
    return value.encode("unicode_escape").decode("ascii")


def extract_bv(source: str) -> str | None:
    match = BV_PATTERN.search(source)
    if match:
        return match.group(1)
    return None


def slugify_source(source: str) -> str:
    bv = extract_bv(source)
    if bv:
        return bv
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "-", source).strip("-")
    return cleaned[:80] or "bilibili-mindmap"


def resolve_context_dir(source: str, output_dir: str | None) -> Path:
    if output_dir:
        return Path(output_dir).resolve()
    return (Path("output") / slugify_source(source)).resolve()


def read_video_title(context_dir: Path) -> str | None:
    details_path = context_dir / "video_details.json"
    if not details_path.exists():
        return None

    try:
        payload = json.loads(details_path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return None

    title = str(payload.get("title") or "").strip()
    return title or None


def read_outline_title(outline_path: Path) -> str | None:
    if not outline_path.exists():
        return None

    for line in outline_path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            return title or None
    return None


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\|?*]+', "_", name).strip(" .")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:120] or "bilibili-mindmap"


def choose_xmind_output(context_dir: Path, outline_path: Path, explicit_output: str | None) -> Path:
    if explicit_output:
        return Path(explicit_output).resolve()

    title = read_outline_title(outline_path) or read_video_title(context_dir)
    xmind_name = f"{sanitize_filename(title)}.xmind" if title else f"{context_dir.name}.xmind"
    return context_dir / xmind_name


def render_xmind(root: Path, outline_path: Path, xmind_output: Path) -> None:
    run([
        sys.executable,
        str(root / "scripts" / "render_xmind.py"),
        "--outline",
        str(outline_path),
        "--output",
        str(xmind_output),
    ])


def maybe_prepare_context(root: Path, args: argparse.Namespace, context_dir: Path, outline_path: Path) -> bool:
    if args.workflow == "host" and outline_path.exists():
        return False

    prepare_cmd = [
        sys.executable,
        str(root / "scripts" / "prepare_bili_context.py"),
        "--source",
        args.source,
        "--output",
        str(context_dir),
        "--asr-provider",
        args.asr_provider,
    ]
    if args.login_if_needed:
        prepare_cmd.append("--login-if-needed")
    if args.transcribe_if_needed:
        prepare_cmd.append("--transcribe-if-needed")
    run(prepare_cmd)
    return True


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    context_dir = resolve_context_dir(args.source, args.output_dir)
    outline_path = context_dir / "outline.md"
    host_prompt_path = context_dir / "host_outline_prompt.md"

    prepared_context = maybe_prepare_context(root, args, context_dir, outline_path)

    if args.workflow == "local":
        run([
            sys.executable,
            str(root / "scripts" / "generate_outline.py"),
            "--context-dir",
            str(context_dir),
            "--output",
            str(outline_path),
        ])
    elif not outline_path.exists():
        print("workflow=host")
        print(f"context={format_for_console(str(context_dir / 'context.md'))}")
        print(f"prompt={format_for_console(str(host_prompt_path))}")
        print(f"outline_expected={format_for_console(str(outline_path))}")
        print("next_step=Use the host LLM to read host_outline_prompt.md and write outline.md, then rerun this command to render the XMind file.")
        return 0

    xmind_output = choose_xmind_output(context_dir, outline_path, args.xmind_output)
    render_xmind(root, outline_path, xmind_output)

    if args.workflow == "host":
        state = "reused_existing_outline" if not prepared_context else "rendered_after_prepare"
        print(f"host_state={state}")
    print(f"outline={format_for_console(str(outline_path))}")
    print(f"xmind={format_for_console(str(xmind_output))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
