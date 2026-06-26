"""
API Health Monitor - API健康检查与故障降级

功能：
- 多ERP系统健康检查轮询
- 断路器模式实现
- 故障自动降级
- 告警通知回调
- 健康历史记录
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Optional
import json

from api_adapter import ConnectionStatus, HealthCheckResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 数据模型
# =============================================================================

class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class HealthAlert:
    """健康告警"""
    timestamp: str
    erp_name: str
    level: AlertLevel
    message: str
    previous_status: str
    current_status: str


@dataclass
class HealthSnapshot:
    """健康状态快照"""
    timestamp: str
    system_mode: str
    overall_status: str
    primary_erp: str
    adapters: dict[str, dict]
    alerts: list[HealthAlert]


# =============================================================================
# 健康监控器
# =============================================================================

class HealthMonitor:
    """
    API健康监控器

    功能：
    - 定时健康检查（后台轮询）
    - 状态变化告警
    - 故障历史记录
    - 降级状态管理
    """

    def __init__(
        self,
        check_interval: float = 60.0,       # 检查间隔（秒）
        alert_callback: Optional[Callable[[HealthAlert], None]] = None,
        history_size: int = 100,
    ):
        self.check_interval = check_interval
        self.alert_callback = alert_callback
        self.history_size = history_size

        self._health_history: list[HealthSnapshot] = []
        self._alerts: list[HealthAlert] = []
        self._last_status: dict[str, str] = {}   # erp_name -> last status
        self._monitoring = False
        self._monitor_task: Optional[asyncio.Task] = None
        self._adapters: dict[str, Any] = {}       # name -> adapter

    def register_adapter(self, name: str, adapter: Any):
        """注册要监控的适配器"""
        self._adapters[name] = adapter
        self._last_status[name] = "unknown"
        logger.info(f"健康监控器已注册适配器: {name}")

    async def check_once(self) -> HealthSnapshot:
        """执行一次全面健康检查"""
        results = {}
        overall_healthy = True
        primary_status = ConnectionStatus.UNKNOWN

        for name, adapter in self._adapters.items():
            try:
                if hasattr(adapter, "health_check"):
                    result: HealthCheckResult = await adapter.health_check()
                    results[name] = {
                        "status": result.status.value,
                        "latency_ms": round(result.latency_ms, 2),
                        "message": result.message,
                        "last_success": result.last_success,
                        "failure_count": result.failure_count,
                    }

                    # 状态变化检测
                    current_status = result.status.value
                    last_status = self._last_status.get(name)
                    if last_status and last_status != current_status:
                        alert = HealthAlert(
                            timestamp=datetime.now().isoformat(),
                            erp_name=name,
                            level=AlertLevel.ERROR if result.status != ConnectionStatus.HEALTHY else AlertLevel.INFO,
                            message=f"状态从 {last_status} 变为 {current_status}",
                            previous_status=last_status,
                            current_status=current_status,
                        )
                        self._alerts.append(alert)
                        logger.warning(f"[健康监控] {name}: {alert.message}")
                        if self.alert_callback:
                            self.alert_callback(alert)

                    self._last_status[name] = current_status

                    if name == "sap_primary" or (name == list(self._adapters.keys())[0] and "primary" in name):
                        primary_status = result.status

                    if result.status != ConnectionStatus.HEALTHY:
                        overall_healthy = False
                else:
                    # Mock适配器
                    results[name] = adapter.health_check()
                    self._last_status[name] = "healthy"

            except Exception as e:
                logger.error(f"[健康监控] {name} 检查失败: {e}")
                results[name] = {
                    "status": "error",
                    "message": str(e),
                    "latency_ms": 0,
                }
                overall_healthy = False

        snapshot = HealthSnapshot(
            timestamp=datetime.now().isoformat(),
            system_mode="production" if overall_healthy else "degraded",
            overall_status="healthy" if overall_healthy else "degraded",
            primary_erp=list(self._adapters.keys())[0] if self._adapters else "none",
            adapters=results,
            alerts=self._alerts[-10:],  # 最近10条告警
        )

        self._health_history.append(snapshot)
        if len(self._health_history) > self.history_size:
            self._health_history = self._health_history[-self.history_size:]

        return snapshot

    async def start_monitoring(self):
        """启动后台监控（定时轮询）"""
        if self._monitoring:
            logger.warning("健康监控已在运行中")
            return
        self._monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info(f"健康监控已启动（间隔 {self.check_interval}s）")

    async def stop_monitoring(self):
        """停止后台监控"""
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("健康监控已停止")

    async def _monitor_loop(self):
        """监控主循环"""
        while self._monitoring:
            try:
                await self.check_once()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[监控循环] 异常: {e}")
                await asyncio.sleep(self.check_interval)

    def get_status(self) -> dict:
        """获取当前健康状态摘要"""
        if not self._health_history:
            return {"status": "unknown", "message": "尚未执行健康检查"}
        latest = self._health_history[-1]
        return {
            "overall_status": latest.overall_status,
            "primary_erp": latest.primary_erp,
            "adapters": {
                name: info["status"]
                for name, info in latest.adapters.items()
            },
            "recent_alerts": len(self._alerts),
            "last_check": latest.timestamp,
        }

    def get_history(self, limit: int = 20) -> list[HealthSnapshot]:
        """获取健康检查历史"""
        return self._health_history[-limit:]

    def export_report(self, path: str):
        """导出健康报告"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "current_status": self.get_status(),
            "alerts": [
                {
                    "timestamp": a.timestamp,
                    "erp_name": a.erp_name,
                    "level": a.level.value,
                    "message": a.message,
                }
                for a in self._alerts[-50:]
            ],
            "history": [
                {
                    "timestamp": s.timestamp,
                    "overall_status": s.overall_status,
                    "adapters": {n: i["status"] for n, i in s.adapters.items()},
                }
                for s in self._health_history[-50:]
            ],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        logger.info(f"健康报告已导出到 {path}")
