"""每日健康自检调度器。

v1.9.0: 对已配 Key 的厂商做最小真实调用（"hi" ~2 token），
记录延迟/成功率/配额余量入 SQLite，异常次日晨报。
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .monitor import compute_concurrency_limit, get_hardware_info


# 最小探测 prompt（~2 token，控制成本）
MINIMAL_PROMPT = "hi"
HEALTH_CHECK_TIMEOUT = 5  # 秒


class HealthScheduler:
    """每日健康自检调度器。"""

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = str(Path.home() / ".cn-model-gateway" / "health.db")
        self.db_path = db_path
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        if db_path == ":memory:":
            self._conn = sqlite3.connect(db_path)
            self._conn.execute("PRAGMA journal_mode=WAL")
        self._init_db()
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def _get_conn(self) -> sqlite3.Connection:
        """Get database connection (shared for :memory: mode)."""
        if self._conn is not None:
            return self._conn
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        conn = self._get_conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS health_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                provider TEXT NOT NULL,
                success INTEGER NOT NULL DEFAULT 0,
                duration_ms INTEGER DEFAULT 0,
                error_type TEXT,
                error_message TEXT,
                quota_remaining TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS health_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()

    def check_once(self, router: Any) -> List[Dict[str, Any]]:
        """执行一次健康检查，返回各厂商结果。"""
        results = []
        for provider, adapter in router._adapters.items():
            if not adapter.is_available():
                continue
            result = self._check_provider(provider, adapter)
            results.append(result)
            self._save_result(result)
        return results

    def _check_provider(self, provider: str, adapter: Any) -> Dict[str, Any]:
        """对单个厂商做最小调用。"""
        start = time.time()
        try:
            from .adapters.base import ChatMessage
            msgs = [ChatMessage(role="user", content=MINIMAL_PROMPT)]
            resp = adapter.chat(msgs, max_tokens=1)
            duration_ms = int((time.time() - start) * 1000)
            return {
                "provider": provider,
                "success": True,
                "duration_ms": duration_ms,
                "error_type": None,
                "error_message": None,
                "quota_remaining": resp.usage.get("total_tokens", ""),
            }
        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            error_type = self._classify_error(str(e))
            return {
                "provider": provider,
                "success": False,
                "duration_ms": duration_ms,
                "error_type": error_type,
                "error_message": str(e)[:200],
                "quota_remaining": None,
            }

    def _classify_error(self, error_msg: str) -> str:
        """分类错误类型。"""
        msg = error_msg.lower()
        if "429" in msg or "rate" in msg:
            return "rate_limit"
        elif "451" in msg or "region" in msg:
            return "region_block"
        elif "balance" in msg or "quota" in msg or "insufficient" in msg:
            return "balance_insufficient"
        elif "content" in msg or "audit" in msg or "block" in msg:
            return "content_audit"
        elif "auth" in msg or "key" in msg or "token" in msg:
            return "auth_failure"
        else:
            return "unknown"

    def _save_result(self, result: Dict[str, Any]) -> None:
        """保存检查结果到 SQLite。"""
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO health_log "
            "(timestamp, provider, success, duration_ms, error_type, error_message, quota_remaining) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                time.time(),
                result["provider"],
                1 if result["success"] else 0,
                result["duration_ms"],
                result.get("error_type"),
                result.get("error_message"),
                result.get("quota_remaining"),
            ),
        )
        conn.commit()

    def get_recent_results(self, hours: int = 24) -> List[Dict[str, Any]]:
        """获取最近 N 小时的健康检查结果。"""
        cutoff = time.time() - hours * 3600
        conn = self._get_conn()
        conn.row_factory = sqlite3.Row
        with conn:
            rows = conn.execute(
                "SELECT * FROM health_log WHERE timestamp >= ? ORDER BY timestamp DESC",
                (cutoff,),
            ).fetchall()
            return [dict(r) for r in rows]

    def generate_morning_report(self) -> str:
        """生成晨报 HTML。"""
        results_24h = self.get_recent_results(24)
        if not results_24h:
            return "<p>暂无健康检查数据</p>"

        # 按厂商聚合
        provider_stats: Dict[str, Dict[str, Any]] = {}
        for r in results_24h:
            p = r["provider"]
            if p not in provider_stats:
                provider_stats[p] = {
                    "total": 0,
                    "success": 0,
                    "errors": [],
                    "avg_duration": 0,
                }
            provider_stats[p]["total"] += 1
            if r["success"]:
                provider_stats[p]["success"] += 1
            else:
                provider_stats[p]["errors"].append(r)

        # 生成 HTML
        lines = [
            "<html><head><meta charset='utf-8'>",
            "<style>",
            "body{font-family:sans-serif;max-width:800px;margin:20px auto;padding:0 20px;}",
            "h1{font-size:18px;border-bottom:2px solid #378ADD;padding-bottom:8px;}",
            "table{width:100%;border-collapse:collapse;margin:16px 0;}",
            "th,td{padding:8px 12px;border:1px solid #ddd;text-align:left;}",
            "th{background:#E6F1FB;}",
            ".ok{color:#639922;}.err{color:#E24B4A;}",
            ".alert{background:#FAEEDA;padding:12px;border-left:4px solid #BA7517;margin:12px 0;}",
            "</style></head><body>",
            f"<h1>🏥 国产模型健康晨报 — {time.strftime('%Y-%m-%d')}</h1>",
        ]

        # 异常告警置顶
        alerts = []
        for p, stats in provider_stats.items():
            if stats["total"] > 0:
                success_rate = stats["success"] / stats["total"]
                if success_rate < 0.5:
                    alerts.append(f"<div class='alert'>⚠️ <b>{p}</b> 成功率仅 {success_rate:.0%}，建议检查 API Key 或联系厂商</div>")

        if alerts:
            lines.append("<h2>🚨 异常告警</h2>")
            lines.extend(alerts)

        # 详细表格
        lines.append("<h2>📊 各厂商状态</h2>")
        lines.append("<table><tr><th>厂商</th><th>检查次数</th><th>成功率</th><th>平均延迟</th><th>最近错误</th></tr>")
        for p, stats in provider_stats.items():
            success_rate = stats["success"] / stats["total"] if stats["total"] > 0 else 0
            avg_dur = sum(r["duration_ms"] for r in results_24h if r["provider"] == p) / max(stats["total"], 1)
            last_error = stats["errors"][0]["error_type"] if stats["success"] < stats["total"] else "-"
            status_class = "ok" if success_rate >= 0.8 else "err"
            lines.append(
                f"<tr><td>{p}</td><td>{stats['total']}</td>"
                f"<td class='{status_class}'>{success_rate:.0%}</td>"
                f"<td>{avg_dur:.0f}ms</td><td>{last_error}</td></tr>"
            )
        lines.append("</table>")

        # 变更雷达
        lines.append("<h2>📡 变更雷达</h2>")
        anomaly = self._detect_anomaly()
        if anomaly:
            for a in anomaly:
                lines.append(f"<div class='alert'>🔍 {a}</div>")
        else:
            lines.append("<p>✅ 未检测到异常变更</p>")

        lines.append(f"<p style='color:#888;font-size:12px;'>生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>")
        lines.append("</body></html>")
        return "\n".join(lines)

    def _detect_anomaly(self) -> List[str]:
        """检测异常变更（滑动窗口 + 3σ）。"""
        results_7d = self.get_recent_results(168)  # 7 days
        if not results_7d:
            return []

        # 按厂商计算 7d 基线错误率
        provider_baseline: Dict[str, float] = {}
        provider_recent: Dict[str, Dict[str, int]] = {}

        for r in results_7d:
            p = r["provider"]
            if p not in provider_recent:
                provider_recent[p] = {"total": 0, "errors": 0}
            provider_recent[p]["total"] += 1
            if not r["success"]:
                provider_recent[p]["errors"] += 1

        for p, stats in provider_recent.items():
            provider_baseline[p] = stats["errors"] / max(stats["total"], 1)

        # 24h 错误率
        results_24h = self.get_recent_results(24)
        recent_stats: Dict[str, Dict[str, int]] = {}
        for r in results_24h:
            p = r["provider"]
            if p not in recent_stats:
                recent_stats[p] = {"total": 0, "errors": 0}
            recent_stats[p]["total"] += 1
            if not r["success"]:
                recent_stats[p]["errors"] += 1

        # 3σ 检测
        alerts = []
        for p, stats in recent_stats.items():
            if stats["total"] < 3:
                continue
            recent_rate = stats["errors"] / stats["total"]
            baseline_rate = provider_baseline.get(p, 0)
            # 简化 3σ: 24h 错误率 > 基线 + 3 * sqrt(baseline * (1-baseline) / n)
            import math
            if baseline_rate > 0:
                sigma = math.sqrt(baseline_rate * (1 - baseline_rate) / stats["total"])
                if recent_rate > baseline_rate + 3 * sigma and recent_rate > 0.3:
                    alerts.append(f"<b>{p}</b> 24h 错误率 {recent_rate:.0%} 显著高于 7d 基线 {baseline_rate:.0%}，疑似接口变更或故障")
            elif recent_rate > 0.5:
                alerts.append(f"<b>{p}</b> 24h 错误率 {recent_rate:.0%}（历史无错误），疑似接口变更")

        return alerts

    def save_report(self, path: Optional[str] = None) -> str:
        """保存晨报到文件。"""
        html = self.generate_morning_report()
        if path is None:
            path = str(Path.home() / ".cn-model-gateway" / f"health_report_{time.strftime('%Y-%m-%d')}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return path

    def start_scheduler(self, router: Any, interval_hours: int = 24) -> None:
        """启动后台调度线程。"""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._scheduler_loop,
            args=(router, interval_hours),
            daemon=True,
        )
        self._thread.start()

    def stop_scheduler(self) -> None:
        """停止后台调度。"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=10)

    def _scheduler_loop(self, router: Any, interval_hours: int) -> None:
        """调度循环。"""
        while self._running:
            try:
                self.check_once(router)
            except Exception:
                pass
            time.sleep(interval_hours * 3600)
