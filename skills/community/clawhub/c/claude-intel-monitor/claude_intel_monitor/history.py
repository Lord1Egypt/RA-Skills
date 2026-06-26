"""History storage using SQLite for benchmark runs.

Stores each run's scores for trend analysis and degradation detection.
"""

import json
import sqlite3
import time
from pathlib import Path
from dataclasses import asdict
from typing import Optional

from .evaluator import BenchmarkReport, CategoryScore

DEFAULT_DB_PATH = Path.home() / ".claude-intel-monitor" / "history.db"


def _ensure_db(db_path: Path = DEFAULT_DB_PATH):
    """Create database and tables if they don't exist."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            provider TEXT NOT NULL,
            timestamp REAL NOT NULL,
            overall_score REAL NOT NULL,
            total_questions INTEGER,
            total_passed INTEGER,
            total_latency_ms REAL,
            degradation_detected INTEGER,
            alerts TEXT,  -- JSON array
            categories TEXT  -- JSON array of CategoryScore
        )
    """)
    conn.commit()
    return conn


def save_report(report: BenchmarkReport, provider: str, db_path: Path = DEFAULT_DB_PATH):
    """Save a benchmark report to history."""
    conn = _ensure_db(db_path)
    categories_json = json.dumps([
        {
            "category": cs.category,
            "total": cs.total,
            "passed": cs.passed,
            "weighted_score": cs.weighted_score,
            "total_weight": cs.total_weight,
            "status": cs.status,
            "delta_vs_baseline": cs.delta_vs_baseline,
        }
        for cs in report.categories
    ], ensure_ascii=False)
    alerts_json = json.dumps(report.alerts, ensure_ascii=False)

    conn.execute(
        """INSERT INTO runs (model, provider, timestamp, overall_score,
           total_questions, total_passed, total_latency_ms,
           degradation_detected, alerts, categories)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            report.model, provider, report.timestamp, report.overall_score,
            report.total_questions, report.total_passed, report.total_latency_ms,
            int(report.degradation_detected), alerts_json, categories_json,
        )
    )
    conn.commit()
    conn.close()


def get_history(model: Optional[str] = None, limit: int = 20,
                db_path: Path = DEFAULT_DB_PATH) -> list[dict]:
    """Get benchmark run history, optionally filtered by model."""
    conn = _ensure_db(db_path)
    if model:
        rows = conn.execute(
            "SELECT * FROM runs WHERE model = ? ORDER BY timestamp DESC LIMIT ?",
            (model, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM runs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "model": row[1],
            "provider": row[2],
            "timestamp": row[3],
            "overall_score": row[4],
            "total_questions": row[5],
            "total_passed": row[6],
            "total_latency_ms": row[7],
            "degradation_detected": bool(row[8]),
            "alerts": json.loads(row[9]) if row[9] else [],
            "categories": json.loads(row[10]) if row[10] else [],
        })
    return results


def get_baseline(model: str, db_path: Path = DEFAULT_DB_PATH) -> Optional[dict]:
    """Get the first (oldest) run as baseline for a model."""
    conn = _ensure_db(db_path)
    row = conn.execute(
        "SELECT overall_score, categories FROM runs WHERE model = ? ORDER BY timestamp ASC LIMIT 1",
        (model,)
    ).fetchone()
    conn.close()

    if row is None:
        return None

    baseline = {"overall": row[0]}
    categories = json.loads(row[1]) if row[1] else []
    for cat in categories:
        baseline[cat["category"]] = cat["weighted_score"]
    return baseline
