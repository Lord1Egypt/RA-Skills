#!/usr/bin/env python3
"""
remove_worker.py —— 移除员工（纯 Python 版）
用法: python3 remove_worker.py <worker_id>
"""
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from deerflow_runtime import worker_home

OFFICE_DIR = Path(os.environ.get("HERMES_OFFICE_DIR", Path.home() / ".hermes" / "office"))
STATE_FILE = OFFICE_DIR / "state" / "office_state.json"


def load_state():
    if not STATE_FILE.exists():
        return {"workers": {}, "port_pool": {"used": [], "available": []}}
    with open(STATE_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_state(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_worker_by_name_or_id(identifier: str, state: dict):
    """支持用名字或工号查找"""
    # 直接 ID 匹配
    if identifier in state.get("workers", {}):
        return identifier, state["workers"][identifier]

    # name 匹配
    for wid, w in state.get("workers", {}).items():
        if w.get("name") == identifier:
            return wid, w

    return None, None


def main():
    if len(sys.argv) < 2:
        print("❌ 用法: python3 remove_worker.py <worker_id或名字>")
        sys.exit(1)

    identifier = sys.argv[1]
    state = load_state()
    wid, worker = find_worker_by_name_or_id(identifier, state)

    if not worker:
        print(f"❌ 找不到员工: {identifier}")
        available = list(state.get("workers", {}).keys())
        if available:
            print(f"   可用员工: {', '.join(available)}")
        sys.exit(1)

    name = worker.get("name", wid)
    port = worker.get("port")
    engine = worker.get("engine", "unknown")

    # ── 停止进程 ──────────────────────────────────────
    if port:
        try:
            r = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True, text=True, timeout=5
            )
            for pid_str in r.stdout.strip().split("\n"):
                if pid_str:
                    try:
                        os.kill(int(pid_str), signal.SIGTERM)
                        print(f"✅ 进程已停止 (PID: {pid_str})")
                    except ProcessLookupError:
                        pass
        except Exception:
            pass

    # ── 注销 openclaw agent ───────────────────────────
    if engine in ("openclaw", "hermes"):
        try:
            subprocess.run(
                ["openclaw", "agents", "remove", wid],
                capture_output=True, timeout=10
            )
            print(f"✅ openclaw agent 已注销: {wid}")
        except Exception:
            pass

    # ── 删除目录 ──────────────────────────────────────
    worker_dir = OFFICE_DIR / "workers" / wid
    if worker_dir.exists():
        import shutil
        shutil.rmtree(worker_dir)
        print(f"✅ 目录已删除: {worker_dir}")

    if engine == "deerflow":
        home_dir = Path(worker.get("deerflow_home") or worker_home(wid))
        if home_dir.exists():
            import shutil
            shutil.rmtree(home_dir)
            print(f"✅ DeerFlow home 已删除: {home_dir}")

    # ── 更新 state ─────────────────────────────────────
    if wid in state.get("workers", {}):
        del state["workers"][wid]

    if port and port not in state.get("port_pool", {}).get("available", []):
        used = state.get("port_pool", {}).get("used", [])
        if port in used:
            used.remove(port)
        state["port_pool"]["available"] = sorted(
            set(state["port_pool"].get("available", []) + [port])
        )

    save_state(state)
    print(f"✅ {name} 已离职，端口 {port} 已释放")


if __name__ == "__main__":
    main()
