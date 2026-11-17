from __future__ import annotations
__version__ = "8.1.0-aipc"  # V8.1-AIPC: 每次工作自动输出本地/云端对比 + 全互动控件完整性门控


# --- UTF-8 stdout/stderr (Windows 涓枃杈撳嚭闃蹭贡鐮? -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

import json
import os
import uuid
from pathlib import Path
from datetime import datetime, timezone


SKILL_DIR = Path(__file__).resolve().parent.parent
STATE_FILE_NAME = ".cost_state.json"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _current_month_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


log = get_logger("cost_monitor")


class CostMonitor:
    """绔簯鎴愭湰鐩戞帶涓庣啍鏂伐鍏凤紙V7 搂11锛夈?

    缁存姢褰撴湀绱鎴愭湰銆侀绠楀憡璀槇鍊间笌鑷姩鐔旀柇鐘舵侊紝
    骞舵寜 搂11.5 鏍煎紡杈撳嚭鎴愭湰瀹¤鏃織銆?
    """

    def __init__(
        self,
        monthly_budget_usd: float = 10.0,
        storage_dir: Path | None = None,
    ) -> None:
        log = get_logger("cost_monitor")
        self._log = log
        self.monthly_budget_usd: float = float(monthly_budget_usd)
        self.storage_dir: Path = Path(storage_dir) if storage_dir is not None else SKILL_DIR
        self.state_path: Path = self.storage_dir / STATE_FILE_NAME
        self._audit_log_path: Path | None = None
        self._load_state()

    def _load_state(self) -> None:
        if self.state_path.exists():
            try:
                with self.state_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            except (OSError, json.JSONDecodeError):
                data = {}
        else:
            data = {}

        loaded_budget = data.get("monthly_budget_usd", self.monthly_budget_usd)
        try:
            self.monthly_budget_usd = float(loaded_budget)
        except (TypeError, ValueError):
            self.monthly_budget_usd = float(self.monthly_budget_usd)

        self.current_month: str = data.get("current_month") or _current_month_tag()
        self.cumulative_cost_usd: float = float(data.get("cumulative_cost_usd", 0.0))
        history = data.get("history", [])
        if isinstance(history, list):
            self.history: list = history
        else:
            self.history = []

        self._reset_monthly_if_needed()

    def _reset_monthly_if_needed(self) -> None:
        current = _current_month_tag()
        if self.current_month != current:
            self.current_month = current
            self.cumulative_cost_usd = 0.0
            self.history = []
            self._persist()

    def _persist(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "current_month": self.current_month,
            "cumulative_cost_usd": self.cumulative_cost_usd,
            "monthly_budget_usd": self.monthly_budget_usd,
            "history": self.history,
        }
        tmp_path = self.state_path.with_suffix(self.state_path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, self.state_path)

    def get_alert_level(self) -> str:
        if self.monthly_budget_usd <= 0:
            return "critical_100"
        ratio = (self.cumulative_cost_usd / self.monthly_budget_usd) * 100.0
        if ratio >= 100.0:
            return "critical_100"
        if ratio >= 80.0:
            return "warning_80"
        if ratio >= 50.0:
            return "warning_50"
        return "none"

    def check_circuit_breaker(self) -> bool:
        return self.cumulative_cost_usd >= self.monthly_budget_usd

    def get_audit_log_path(self) -> Path:
        if self._audit_log_path is None:
            self._audit_log_path = self.storage_dir / f"cost_audit_{uuid.uuid4()}.json"
        return self._audit_log_path

    def record_cost(self, cost_usd: float, request_id: str) -> dict:
        self._reset_monthly_if_needed()

        cost_value = float(cost_usd)
        self.cumulative_cost_usd += cost_value

        alert_level = self.get_alert_level()
        circuit_breaker_triggered = self.check_circuit_breaker()

        if self.monthly_budget_usd > 0:
            budget_remaining_pct = round(
                max(0.0, (1.0 - self.cumulative_cost_usd / self.monthly_budget_usd) * 100.0),
                2,
            )
        else:
            budget_remaining_pct = 0.0

        audit_entry = {
            "cost_audit_id": f"cost-audit-{uuid.uuid4()}",
            "timestamp": _utc_now_iso(),
            "request_id": request_id,
            "cost_usd": round(cost_value, 6),
            "cumulative_cost_usd": round(self.cumulative_cost_usd, 6),
            "monthly_budget_usd": round(self.monthly_budget_usd, 2),
            "budget_remaining_pct": budget_remaining_pct,
            "alert_level": alert_level,
            "circuit_breaker_triggered": circuit_breaker_triggered,
        }

        self.history.append(audit_entry)
        self._persist()

        audit_log_path = self.get_audit_log_path()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        with audit_log_path.open("w", encoding="utf-8") as f:
            json.dump(audit_entry, f, ensure_ascii=False, indent=2)

        return audit_entry

    def record_degradation(
        self,
        level: int,
        source: str = "edge_cloud",
        reason: str = "",
        request_id: str = "",
    ) -> dict:
        """V7-AIPC 鍗囩骇锛氫笂鎶?degradation_level 鍙樺寲锛圴7.3.2 鏀硅繘5 鍗囩骇鐗堬級锛屽悓鏃惰褰曞埌 work_summary銆?

        鍐欏叆 degradation_log.jsonl 鐩戞帶鏂囦欢锛堟瘡琛屼竴涓簨浠讹級锛?
          - level: 1~5锛?=姝d父, 5=瀹屽叏鏈湴锛?
          - source: edge_cloud / analyze / lesson_plan_guard
          - reason: 瑙彂鍘熷洜锛堝 "consecutive_timeouts=3" / "npu_unavailable"锛?
          - request_id: 鍏宠仈璇锋眰

        渚?Prometheus / 鐩戞帶闈澘閲囬泦銆?
        """
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        log_path = self.storage_dir / "degradation_log.jsonl"
        event = {
            "timestamp": _utc_now_iso(),
            "level": int(level),
            "source": source,
            "reason": reason,
            "request_id": request_id,
            "cumulative_cost_usd": round(self.cumulative_cost_usd, 6),
        }
        try:
            with log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except OSError as e:
            log.warn(f"[cost] degradation 日志写入失败:{e}")
        # 50/80/100% 闃堝?+ degradation 鍗囩骇鏃惰褰曞埌 history
        if level >= 4:
            audit_entry = {
                "cost_audit_id": f"degrade-{uuid.uuid4()}",
                "timestamp": _utc_now_iso(),
                "request_id": request_id,
                "event": "degradation_level_change",
                "level": int(level),
                "source": source,
                "reason": reason,
            }
            self.history.append(audit_entry)
            self._persist()
        log.info(f"[cost] degradation={level} source={source} reason={reason}")
        return event

    def get_degradation_history(self, limit: int = 100) -> list[dict]:
        """读取 degradation_log.jsonl 最近 limit 条事件."""
        log_path = self.storage_dir / "degradation_log.jsonl"
        if not log_path.exists():
            return []
        events: list[dict] = []
        try:
            with log_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except OSError:
            return []
        return events[-limit:]


_default_monitor: CostMonitor | None = None


def get_default_monitor() -> CostMonitor:
    global _default_monitor
    if _default_monitor is None:
        _default_monitor = CostMonitor()
    return _default_monitor

