#!/usr/bin/env python3
"""
Prepare a clean ClawHub publish folder from the development repo.

Purpose:
- keep the repository useful for development and dogfooding
- emit a curated publish surface with only the files the public skill needs
- avoid hand-curated last-minute publish mistakes
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "dist" / "durable-task-runner"

INCLUDE = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "ATTRIBUTION.md",
    "config/defaults.json",
    "references/control-levels.md",
    "references/quickstart.md",
    "references/subagent-return-protocol.md",
    "references/task-schema.md",
    "scripts/task_ctl.py",
    "scripts/task_continue.py",
    "scripts/task_install_tick_cron.sh",
    "scripts/task_maybe_send_now.py",
    "scripts/task_reconcile.py",
    "scripts/task_auto_continue.py",
    "scripts/task_status_snapshot.py",
    "scripts/task_user_steer.py",
    "scripts/task_control_reply.py",
    "scripts/task_context_guard.py",
    "scripts/task_report.py",
    "scripts/task_resume_apply.py",
    "scripts/task_resume_bootstrap.py",
    "scripts/task_resume_queue.py",
    "scripts/task_send_status.py",
    "scripts/task_should_report.py",
    "scripts/task_status_tick.sh",
    "scripts/task_tick_all.py",
    "scripts/task_subagent_ctl.py",
    "scripts/task_subagent_run.py",
    "scripts/task_subagent_spawn.py",
    "scripts/task_ticker.py",
]


def copy_item(rel: str, out_root: Path) -> None:
    src = ROOT / rel
    dst = out_root / rel
    if not src.exists():
        raise SystemExit(f"missing required publish file: {rel}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output folder for the clean publish bundle")
    args = ap.parse_args()

    out_root = Path(args.out).expanduser().resolve()
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    for rel in INCLUDE:
        copy_item(rel, out_root)

    print(f"Prepared clean publish bundle: {out_root}")
    print("Included files:")
    for rel in INCLUDE:
        print(f"- {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
