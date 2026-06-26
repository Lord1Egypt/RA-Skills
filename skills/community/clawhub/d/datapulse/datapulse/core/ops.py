"""Daemon heartbeat, metrics, and static status page utilities."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .utils import watch_status_html_path_from_env, watch_status_path_from_env


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class WatchStatusStore:
    """JSON + HTML status output for the watch daemon."""

    def __init__(self, path: str | None = None, html_path: str | None = None):
        self.path = Path(path or watch_status_path_from_env()).expanduser()
        self.html_path = Path(html_path or watch_status_html_path_from_env()).expanduser()
        self.status = self._load()

    def _default_payload(self) -> dict[str, Any]:
        return {
            "updated_at": "",
            "state": "idle",
            "heartbeat_at": "",
            "started_at": "",
            "last_cycle_started_at": "",
            "last_cycle_finished_at": "",
            "last_error": "",
            "metrics": {
                "cycles_total": 0,
                "due_total": 0,
                "runs_total": 0,
                "success_total": 0,
                "error_total": 0,
                "alerts_total": 0,
            },
            "last_result": {},
        }

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return self._default_payload()
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return self._default_payload()
        if not isinstance(payload, dict):
            return self._default_payload()
        base = self._default_payload()
        base.update(payload)
        if not isinstance(base.get("metrics"), dict):
            base["metrics"] = self._default_payload()["metrics"]
        return base

    def _persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.status, ensure_ascii=False, indent=2), encoding="utf-8")
        self._write_html()

    def _write_html(self) -> None:
        self.html_path.parent.mkdir(parents=True, exist_ok=True)
        metrics = self.status.get("metrics", {})
        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DataPulse Watch Status</title>
  <style>
    :root {{
      --bg: #f3efe5;
      --panel: #fff8ea;
      --ink: #1c2a1f;
      --accent: #0a7f5a;
      --warn: #b04b2d;
      --line: #d6cbb4;
    }}
    body {{ margin: 0; padding: 24px; background: linear-gradient(180deg, #efe8d5, var(--bg)); color: var(--ink); font: 16px/1.5 Georgia, 'Iowan Old Style', serif; }}
    .wrap {{ max-width: 980px; margin: 0 auto; }}
    .hero {{ padding: 24px; border: 1px solid var(--line); background: var(--panel); border-radius: 18px; box-shadow: 0 18px 48px rgba(44, 36, 20, 0.08); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 18px; }}
    .card {{ padding: 14px; border-radius: 14px; background: rgba(255,255,255,0.66); border: 1px solid var(--line); }}
    .label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.7; }}
    .value {{ font-size: 28px; font-weight: 700; }}
    .state-ok {{ color: var(--accent); }}
    .state-error {{ color: var(--warn); }}
    pre {{ white-space: pre-wrap; word-break: break-word; background: rgba(255,255,255,0.6); padding: 16px; border-radius: 14px; border: 1px solid var(--line); }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>DataPulse Watch Daemon</h1>
      <p class="{ 'state-error' if self.status.get('state') == 'error' else 'state-ok' }">state: {self.status.get('state', 'idle')}</p>
      <div class="grid">
        <div class="card"><div class="label">Heartbeat</div><div>{self.status.get('heartbeat_at', '-')}</div></div>
        <div class="card"><div class="label">Cycles</div><div class="value">{metrics.get('cycles_total', 0)}</div></div>
        <div class="card"><div class="label">Success</div><div class="value">{metrics.get('success_total', 0)}</div></div>
        <div class="card"><div class="label">Errors</div><div class="value">{metrics.get('error_total', 0)}</div></div>
        <div class="card"><div class="label">Alerts</div><div class="value">{metrics.get('alerts_total', 0)}</div></div>
      </div>
      <h2>Last Result</h2>
      <pre>{json.dumps(self.status.get('last_result', {}), ensure_ascii=False, indent=2)}</pre>
    </div>
  </div>
</body>
</html>
"""
        self.html_path.write_text(html, encoding="utf-8")

    def mark_started(self) -> dict[str, Any]:
        now = _utcnow()
        self.status["started_at"] = self.status.get("started_at") or now
        self.status["heartbeat_at"] = now
        self.status["updated_at"] = now
        self.status["state"] = "running"
        self._persist()
        return self.status

    def mark_cycle_started(self) -> dict[str, Any]:
        now = _utcnow()
        self.status["heartbeat_at"] = now
        self.status["updated_at"] = now
        self.status["last_cycle_started_at"] = now
        self.status["state"] = "running"
        self._persist()
        return self.status

    def record_cycle(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = _utcnow()
        metrics = self.status.setdefault("metrics", {})
        results = payload.get("results", [])
        success_count = 0
        error_count = 0
        alert_count = 0
        for row in results if isinstance(results, list) else []:
            if str(row.get("status", "")).lower() == "success":
                success_count += 1
            else:
                error_count += 1
            alert_count += int(row.get("alert_count", 0) or 0)

        metrics["cycles_total"] = int(metrics.get("cycles_total", 0) or 0) + 1
        metrics["due_total"] = int(metrics.get("due_total", 0) or 0) + int(payload.get("due_count", 0) or 0)
        metrics["runs_total"] = int(metrics.get("runs_total", 0) or 0) + int(payload.get("run_count", 0) or 0)
        metrics["success_total"] = int(metrics.get("success_total", 0) or 0) + success_count
        metrics["error_total"] = int(metrics.get("error_total", 0) or 0) + error_count
        metrics["alerts_total"] = int(metrics.get("alerts_total", 0) or 0) + alert_count

        self.status["heartbeat_at"] = now
        self.status["updated_at"] = now
        self.status["last_cycle_finished_at"] = now
        self.status["last_result"] = payload
        self.status["last_error"] = ""
        self.status["state"] = "running"
        self._persist()
        return self.status

    def record_error(self, error: str) -> dict[str, Any]:
        now = _utcnow()
        metrics = self.status.setdefault("metrics", {})
        metrics["error_total"] = int(metrics.get("error_total", 0) or 0) + 1
        self.status["heartbeat_at"] = now
        self.status["updated_at"] = now
        self.status["last_cycle_finished_at"] = now
        self.status["last_error"] = str(error or "").strip()
        self.status["state"] = "error"
        self._persist()
        return self.status

    def mark_stopped(self) -> dict[str, Any]:
        now = _utcnow()
        self.status["heartbeat_at"] = now
        self.status["updated_at"] = now
        self.status["state"] = "idle"
        self._persist()
        return self.status

    def snapshot(self) -> dict[str, Any]:
        return self.status
