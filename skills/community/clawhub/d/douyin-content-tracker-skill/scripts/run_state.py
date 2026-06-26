"""
run_state.py
维护当前运行上下文，避免跨批次数据互相污染。
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from storage import DATA_DIR
STATE_FILE = DATA_DIR / "_current_run.json"


def current_run_id() -> str:
    return os.getenv("RUN_ID", "").strip()


def write_current_run(run_id: str, cleaned_files: list[Path | str]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    resolved = []
    for f in cleaned_files:
        p = Path(f)
        if p.exists():
            resolved.append(str(p.resolve()))
        else:
            print(f"  警告：文件不存在，未注册到当前运行：{p}")

    payload = {
        "run_id": run_id,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "cleaned_files": resolved,
    }
    STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_current_run() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def resolve_cleaned_files() -> list[Path]:
    state = read_current_run()
    run_id = current_run_id()
    state_run_id = str(state.get("run_id", "")).strip()

    if state.get("cleaned_files"):
        if run_id and state_run_id and state_run_id != run_id:
            return []
        files = [Path(p) for p in state["cleaned_files"] if Path(p).exists()]
        if files:
            return files

    return sorted(DATA_DIR.glob("cleaned_*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
