"""Usage statistics + hardware-aware performance control."""
from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


def get_hardware_info() -> Dict[str, Any]:
    """Detect CPU cores and available memory (cross-platform, no external deps)."""
    info: Dict[str, Any] = {"cpu_cores": 0, "memory_mb": 0}
    try:
        info["cpu_cores"] = os.cpu_count() or 0
    except Exception:
        pass
    try:
        if hasattr(os, "sysconf"):
            # Linux/macOS
            if "SC_PAGE_SIZE" in os.sysconf_names and "SC_PHYS_PAGES" in os.sysconf_names:
                page_size = os.sysconf("SC_PAGE_SIZE")
                phys_pages = os.sysconf("SC_PHYS_PAGES")
                info["memory_mb"] = int(page_size * phys_pages / 1024 / 1024)
    except Exception:
        pass
    # Windows fallback via environment
    if info["memory_mb"] == 0:
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            info["memory_mb"] = int(stat.ullTotalPhys / 1024 / 1024)
        except Exception:
            pass
    return info


def compute_concurrency_limit(hw: Dict[str, Any]) -> int:
    """Dynamically compute max concurrent model calls based on hardware."""
    cores = hw.get("cpu_cores", 0)
    mem_mb = hw.get("memory_mb", 0)
    # Conservative: 1 concurrent call per 2 cores, max 4; memory < 4GB → limit to 1
    if mem_mb < 4096:
        return 1
    if cores <= 2:
        return 1
    if cores <= 4:
        return 2
    return min(4, cores // 2)


class Monitor:
    """Tracks usage statistics and enforces concurrency limits."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = str(Path.home() / ".cn-model-gateway" / "usage.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
        self._hardware = get_hardware_info()
        self._concurrency_limit = compute_concurrency_limit(self._hardware)
        self._active_calls = 0

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            # Enable WAL mode for concurrent multi-process access (v1.4.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    tool_name TEXT,
                    provider TEXT,
                    model TEXT,
                    prompt_tokens INTEGER DEFAULT 0,
                    completion_tokens INTEGER DEFAULT 0,
                    duration_ms INTEGER DEFAULT 0,
                    success INTEGER DEFAULT 1
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    total_calls INTEGER DEFAULT 0,
                    total_prompt_tokens INTEGER DEFAULT 0,
                    total_completion_tokens INTEGER DEFAULT 0,
                    total_duration_ms INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def record_call(self, tool_name: str, args: Dict[str, Any], result: str) -> None:
        """Record a tool call to the database."""
        now = time.time()
        today = time.strftime("%Y-%m-%d", time.localtime(now))
        provider = args.get("provider", "auto")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO usage_log (timestamp, tool_name, provider, model, success) "
                "VALUES (?, ?, ?, ?, 1)",
                (now, tool_name, provider, args.get("model", "")),
            )
            conn.execute(
                "INSERT INTO daily_stats (date, total_calls, total_duration_ms) "
                "VALUES (?, 1, 0) ON CONFLICT(date) DO UPDATE SET total_calls = total_calls + 1",
                (today,),
            )
            conn.commit()

    def get_stats(self) -> Dict[str, Any]:
        """Return usage statistics."""
        today = time.strftime("%Y-%m-%d")
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            today_row = conn.execute(
                "SELECT * FROM daily_stats WHERE date = ?", (today,)
            ).fetchone()
            total_row = conn.execute(
                "SELECT SUM(total_calls) as calls, SUM(total_prompt_tokens) as pt, "
                "SUM(total_completion_tokens) as ct FROM daily_stats"
            ).fetchone()
            by_provider = conn.execute(
                "SELECT provider, COUNT(*) as cnt FROM usage_log GROUP BY provider"
            ).fetchall()
        return {
            "today": dict(today_row) if today_row else {"date": today, "total_calls": 0},
            "total": {
                "calls": total_row["calls"] or 0,
                "prompt_tokens": total_row["pt"] or 0,
                "completion_tokens": total_row["ct"] or 0,
            },
            "by_provider": {r["provider"]: r["cnt"] for r in by_provider},
            "hardware": self._hardware,
            "concurrency_limit": self._concurrency_limit,
        }

    def generate_weekly_report(self) -> str:
        """Generate a text-based weekly usage report."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM daily_stats WHERE date >= date('now', '-7 days') ORDER BY date"
            ).fetchall()
        lines = ["📊 本周使用统计\n"]
        total_calls = 0
        for row in rows:
            lines.append(f"  {row['date']}: {row['total_calls']} 次调用")
            total_calls += row["total_calls"]
        lines.append(f"\n合计: {total_calls} 次调用")
        lines.append(f"硬件: {self._hardware.get('cpu_cores', '?')} 核 / {self._hardware.get('memory_mb', '?')} MB")
        lines.append(f"并发限制: {self._concurrency_limit}")
        return "\n".join(lines)

    @property
    def concurrency_limit(self) -> int:
        return self._concurrency_limit
