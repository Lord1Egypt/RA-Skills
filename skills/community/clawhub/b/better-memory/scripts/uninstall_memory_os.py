#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from memory_os_common import (
    MANAGED_AGENT_BLOCK_END,
    MANAGED_AGENT_BLOCK_START,
    MANAGED_HEARTBEAT_BLOCK_END,
    MANAGED_HEARTBEAT_BLOCK_START,
    MANAGED_MEMORY_BLOCK_END,
    MANAGED_MEMORY_BLOCK_START,
    remove_marked_block,
    sidecar_dir,
)


def strip_block(path: Path, start: str, end: str) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8")
    updated = remove_marked_block(original, start, end)
    if updated == original:
        return False
    if updated:
        path.write_text(updated, encoding="utf-8")
    else:
        path.unlink()
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Uninstall Better Memory additive wiring.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--keep-sidecar", action="store_true", help="Keep .openclaw-memory-os artifacts")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    changed: list[str] = []

    if strip_block(workspace / "AGENTS.md", MANAGED_AGENT_BLOCK_START, MANAGED_AGENT_BLOCK_END):
        changed.append(str(workspace / "AGENTS.md"))
    if strip_block(workspace / "MEMORY.md", MANAGED_MEMORY_BLOCK_START, MANAGED_MEMORY_BLOCK_END):
        changed.append(str(workspace / "MEMORY.md"))
    if strip_block(workspace / "HEARTBEAT.md", MANAGED_HEARTBEAT_BLOCK_START, MANAGED_HEARTBEAT_BLOCK_END):
        changed.append(str(workspace / "HEARTBEAT.md"))

    sidecar = sidecar_dir(workspace)
    if sidecar.exists() and not args.keep_sidecar:
        shutil.rmtree(sidecar)
        changed.append(str(sidecar))

    print(f"Workspace: {workspace}")
    if changed:
        print("Removed Memory OS managed integration from:")
        for path in changed:
            print(f"- {path}")
    else:
        print("No managed integration found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
