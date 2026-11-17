#!/usr/bin/env python3
"""Download YouTube media with yt-dlp, installing/updating yt-dlp first."""

from __future__ import annotations

import argparse
import os
import platform
import site
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_TEMPLATE = "%(title).200B [%(id)s].%(ext)s"


Command = list[str]


def run(cmd: Command, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, text=True, check=check)


def pip_install_or_upgrade() -> None:
    run([sys.executable, "-m", "pip", "install", "--user", "-U", "yt-dlp"])


def user_bin_dirs() -> list[Path]:
    scripts_dir = "Scripts" if os.name == "nt" else "bin"
    candidates = [Path(site.USER_BASE) / scripts_dir]

    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(Path(appdata) / "Python" / "Scripts")
    else:
        candidates.append(Path.home() / ".local" / "bin")

    return list(dict.fromkeys(candidates))


def executable_names() -> list[str]:
    names = ["yt-dlp"]
    if os.name == "nt":
        names.extend(["yt-dlp.exe", "yt-dlp.cmd"])
    return names


def find_user_yt_dlp() -> Command | None:
    for bin_dir in user_bin_dirs():
        for name in executable_names():
            user_bin = bin_dir / name
            if user_bin.exists():
                return [str(user_bin)]

    return None


def yt_dlp_module_available() -> bool:
    return subprocess.run(
        [sys.executable, "-c", "import yt_dlp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    ).returncode == 0


def find_yt_dlp(*, prefer_user: bool = False) -> Command | None:
    if prefer_user:
        user_yt_dlp = find_user_yt_dlp()
        if user_yt_dlp:
            return user_yt_dlp

    found = shutil.which("yt-dlp")
    if found:
        return [found]

    user_yt_dlp = find_user_yt_dlp()
    if user_yt_dlp:
        return user_yt_dlp

    if yt_dlp_module_available():
        return [sys.executable, "-m", "yt_dlp"]

    return None


def ensure_yt_dlp(*, skip_update: bool) -> Command:
    yt_dlp = find_yt_dlp()
    if yt_dlp is None:
        print("yt-dlp not found; installing latest yt-dlp with pip.", flush=True)
        pip_install_or_upgrade()
        yt_dlp = find_yt_dlp(prefer_user=True)

    if yt_dlp is None:
        raise SystemExit(
            "yt-dlp installation completed, but yt-dlp was not found as an executable "
            "or importable Python module."
        )

    if skip_update:
        return yt_dlp

    update = subprocess.run([*yt_dlp, "-U"], text=True)
    if update.returncode != 0:
        print("yt-dlp self-update failed or is disabled; upgrading with pip instead.", flush=True)
        pip_install_or_upgrade()
        yt_dlp = find_yt_dlp(prefer_user=True) or yt_dlp

    return yt_dlp


def build_command(args: argparse.Namespace, yt_dlp: Command) -> Command:
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(output_dir / args.output_template)
    cmd = [*yt_dlp, "--newline", "-o", output_template]

    if not args.playlist:
        cmd.append("--no-playlist")

    if args.format:
        cmd.extend(["-f", args.format])

    if args.audio:
        cmd.extend(["-x", "--audio-format", args.audio_format])

    if args.subtitles:
        cmd.extend(["--write-subs", "--write-auto-subs", "--sub-langs", args.subtitle_languages])

    if args.thumbnail:
        cmd.append("--write-thumbnail")

    if args.cookies:
        cmd.extend(["--cookies", args.cookies])

    if args.cookies_from_browser:
        cmd.extend(["--cookies-from-browser", args.cookies_from_browser])

    cmd.extend(args.extra)
    cmd.append(args.url)
    return cmd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"Install/update yt-dlp, then download YouTube media on {platform.system()}."
    )
    parser.add_argument("url", help="YouTube video, channel, or playlist URL")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="youtube-downloads",
        help="Directory for downloaded files. Default: youtube-downloads",
    )
    parser.add_argument(
        "--output-template",
        default=DEFAULT_TEMPLATE,
        help="yt-dlp output template relative to output-dir.",
    )
    parser.add_argument("--format", help="yt-dlp format selector, for example 'bv*+ba/b'.")
    parser.add_argument("--playlist", action="store_true", help="Allow playlist downloads.")
    parser.add_argument("--audio", action="store_true", help="Extract audio only.")
    parser.add_argument("--audio-format", default="mp3", help="Audio format when using --audio.")
    parser.add_argument("--subtitles", action="store_true", help="Write manual and auto subtitles.")
    parser.add_argument(
        "--subtitle-languages",
        default="en.*,zh.*",
        help="Subtitle language selector for --subtitles.",
    )
    parser.add_argument("--thumbnail", action="store_true", help="Write video thumbnail.")
    parser.add_argument("--cookies", help="Path to a Netscape-format cookies file.")
    parser.add_argument(
        "--cookies-from-browser",
        help="Browser name for yt-dlp cookies, for example chrome, safari, firefox, edge.",
    )
    parser.add_argument(
        "--skip-update",
        action="store_true",
        help="Do not update yt-dlp before downloading.",
    )
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Additional yt-dlp arguments after '--'.",
    )

    args = parser.parse_args()
    if args.extra and args.extra[0] == "--":
        args.extra = args.extra[1:]
    return args


def main() -> None:
    args = parse_args()
    yt_dlp = ensure_yt_dlp(skip_update=args.skip_update)
    cmd = build_command(args, yt_dlp)
    env_path = os.environ.get("PATH", "")
    path_parts = env_path.split(os.pathsep)
    missing_user_bins = [str(path) for path in user_bin_dirs() if str(path) not in path_parts]
    if missing_user_bins:
        os.environ["PATH"] = os.pathsep.join(missing_user_bins + [env_path])
    run(cmd)


if __name__ == "__main__":
    main()
