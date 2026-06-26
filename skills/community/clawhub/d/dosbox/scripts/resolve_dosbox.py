#!/usr/bin/env python3
"""Detect DOSBox/DOSBox-X and print example launch commands."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

COMMON_WINDOWS_PATHS = [
    r"C:\Program Files\DOSBox-X\dosbox-x.exe",
    r"C:\Program Files (x86)\DOSBox-X\dosbox-x.exe",
    r"C:\Program Files\DOSBox-0.74-3\DOSBox.exe",
    r"C:\Program Files (x86)\DOSBox-0.74-3\DOSBox.exe",
    r"C:\Program Files\DOSBox Staging\dosbox.exe",
    r"C:\Program Files (x86)\DOSBox Staging\dosbox.exe",
]


def find_binaries() -> list[str]:
    found: list[str] = []
    for name in ("dosbox-x", "dosbox"):
        path = shutil.which(name)
        if path and path not in found:
            found.append(path)
    for path in COMMON_WINDOWS_PATHS:
        if os.path.exists(path) and path not in found:
            found.append(path)
    return found


def quote(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def build_folder_command(binary: str, game_path: Path) -> str:
    return (
        f"{quote(binary)} "
        f"-c \"mount c {game_path}\" "
        f"-c \"c:\" "
        f"-c \"dir\""
    )


def build_iso_command(binary: str, game_path: Path | None, iso_path: Path) -> str:
    parts = [quote(binary)]
    if game_path:
        parts.append(f'-c "mount c {game_path}"')
    parts.append(f'-c "imgmount d {iso_path} -t iso"')
    if game_path:
        parts.append('-c "c:"')
    else:
        parts.append('-c "d:"')
    parts.append('-c "dir"')
    return " ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect DOSBox executables and suggest commands.")
    parser.add_argument("--game-path", help="Folder to mount as C:")
    parser.add_argument("--iso", help="ISO image to mount as D:")
    args = parser.parse_args()

    binaries = find_binaries()
    if not binaries:
        print("No DOSBox executable found on PATH or in common Windows install locations.")
        return 1

    preferred = next((b for b in binaries if "dosbox-x" in b.lower()), binaries[0])
    print(f"Preferred binary: {preferred}")
    print("Detected binaries:")
    for binary in binaries:
        print(f"- {binary}")

    game_path = Path(args.game_path).resolve() if args.game_path else None
    iso_path = Path(args.iso).resolve() if args.iso else None

    if game_path:
        print("\nFolder launch example:")
        print(build_folder_command(preferred, game_path))

    if iso_path:
        print("\nISO launch example:")
        print(build_iso_command(preferred, game_path, iso_path))

    if not game_path and not iso_path:
        print("\nTip: pass --game-path and/or --iso to generate example commands.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
