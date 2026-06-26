"""
API Integration - 真实API接入层

模块：
- api_adapter: 多ERP系统适配器（SAP/用友/金蝶等）
- api_config: 配置化API端点管理
- api_health: 健康检查与故障降级
- mock_data: 开发/演示用模拟数据
"""

from __future__ import annotations

from .api_adapter import (
    BaseERPAdapter,
    ERPAdapterManager,
    ERPType,
    ConnectionStatus,
    APIEndpoint,
    APIResponse,
    HealthCheckResult,
)
from .api_config import (
    APIConfigManager,
    ERPConfig,
    SystemConfig,
)
from .api_health import HealthMonitor, HealthAlert, HealthSnapshot, AlertLevel
from .mock_data import MockDataGenerator

__all__ = [
    "BaseERPAdapter", "ERPAdapterManager", "ERPType", "ConnectionStatus",
    "APIEndpoint", "APIResponse", "HealthCheckResult",
    "APIConfigManager", "ERPConfig", "SystemConfig",
    "HealthMonitor", "HealthAlert", "HealthSnapshot", "AlertLevel",
    "MockDataGenerator",
]
