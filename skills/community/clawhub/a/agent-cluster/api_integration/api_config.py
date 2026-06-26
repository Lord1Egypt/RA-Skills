"""
API Configuration - 配置化的API端点管理

支持环境变量、YAML、Python字典三种配置方式
支持多ERP系统并行配置
支持开发/生产/演示多种运行模式
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import yaml

from api_adapter import APIEndpoint, ERPType, BaseERPAdapter, SAPERPAdapter, YonyouERPAdapter
from mock_data import MockDataGenerator

# =============================================================================
# 演示数据标识常量
# =============================================================================

DEMO_PREFIX = "[⚠️ 演示数据，仅供参考]"
DEMO_DATA_SOURCE = "模拟数据（开发/演示模式）"
DEMO_DISCLAIMER = "⚠️ 本数据为模拟生成，不可用于真实业务决策"


# =============================================================================
# 配置数据模型
# =============================================================================

@dataclass
class ERPConfig:
    """单个ERP系统配置"""
    name: str
    erp_type: str                      # sap / yonyou / kingdee / oracle / mock
    enabled: bool = True
    is_primary: bool = False           # 是否为主ERP（故障时优先降级到备）
    base_url: str = ""
    auth_type: str = "bearer"          # bearer / basic / apikey
    api_key: str = ""
    username: str = ""
    password: str = ""
    client_id: str = ""
    client_secret: str = ""
    timeout: float = 30.0
    retry_count: int = 3
    retry_delay: float = 1.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: float = 60.0
    custom_headers: dict = field(default_factory=dict)


@dataclass
class SystemConfig:
    """系统级配置"""
    mode: str = "demo"                  # production / demo / development
    log_level: str = "INFO"
    enable_trace: bool = True
    enable_audit: bool = True
    demo_variance: float = 0.1         # 模拟数据随机波动幅度


@dataclass
class APIConfigManager:
    """API配置管理器"""
    system: SystemConfig = field(default_factory=SystemConfig)
    erp_systems: list[ERPConfig] = field(default_factory=list)

    @classmethod
    def from_env(cls) -> "APIConfigManager":
        """从环境变量加载配置"""
        system = SystemConfig(
            mode=os.getenv("SYSTEM_MODE", "demo"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            enable_trace=os.getenv("ENABLE_TRACE", "true").lower() == "true",
            enable_audit=os.getenv("ENABLE_AUDIT", "true").lower() == "true",
            demo_variance=float(os.getenv("DEMO_VARIANCE", "0.1")),
        )

        erp_configs = []

        # SAP配置
        if os.getenv("SAP_BASE_URL"):
            erp_configs.append(ERPConfig(
                name="sap_primary",
                erp_type="sap",
                enabled=True,
                is_primary=True,
                base_url=os.getenv("SAP_BASE_URL", ""),
                auth_type="bearer",
                api_key=os.getenv("SAP_API_KEY", ""),
                username=os.getenv("SAP_USER", ""),
                password=os.getenv("SAP_PASSWORD", ""),
                timeout=float(os.getenv("SAP_TIMEOUT", "30.0")),
            ))

        # 用友配置
        if os.getenv("YONYOU_BASE_URL"):
            erp_configs.append(ERPConfig(
                name="yonyou_backup",
                erp_type="yonyou",
                enabled=True,
                is_primary=False,
                base_url=os.getenv("YONYOU_BASE_URL", ""),
                auth_type="apikey",
                api_key=os.getenv("YONYOU_APPKEY", ""),
                username=os.getenv("YONYOU_ACCOUNT", ""),
                password=os.getenv("YONYOU_PASSWORD", ""),
                timeout=float(os.getenv("YONYOU_TIMEOUT", "30.0")),
            ))

        # 如果没有配置任何ERP，默认使用模拟模式
        if not erp_configs:
            erp_configs.append(ERPConfig(
                name="mock_default",
                erp_type="mock",
                enabled=True,
                is_primary=True,
            ))

        return cls(system=system, erp_systems=erp_configs)

    @classmethod
    def from_yaml(cls, path: str) -> "APIConfigManager":
        """从YAML文件加载配置"""
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        system_data = raw.get("system", {})
        system = SystemConfig(
            mode=system_data.get("mode", "demo"),
            log_level=system_data.get("log_level", "INFO"),
            enable_trace=system_data.get("enable_trace", True),
            enable_audit=system_data.get("enable_audit", True),
            demo_variance=system_data.get("demo_variance", 0.1),
        )

        erp_configs = []
        for erp_data in raw.get("erp_systems", []):
            cfg = ERPConfig(
                name=erp_data["name"],
                erp_type=erp_data["erp_type"],
                enabled=erp_data.get("enabled", True),
                is_primary=erp_data.get("is_primary", False),
                base_url=erp_data.get("base_url", ""),
                auth_type=erp_data.get("auth_type", "bearer"),
                api_key=erp_data.get("api_key", ""),
                username=erp_data.get("username", ""),
                password=erp_data.get("password", ""),
                timeout=float(erp_data.get("timeout", 30.0)),
                retry_count=int(erp_data.get("retry_count", 3)),
                retry_delay=float(erp_data.get("retry_delay", 1.0)),
                circuit_breaker_threshold=int(erp_data.get("circuit_breaker_threshold", 5)),
                circuit_breaker_timeout=float(erp_data.get("circuit_breaker_timeout", 60.0)),
                custom_headers=erp_data.get("custom_headers", {}),
            )
            erp_configs.append(cfg)

        return cls(system=system, erp_systems=erp_configs)

    def to_yaml(self, path: str):
        """导出配置到YAML文件"""
        data = {
            "system": {
                "mode": self.system.mode,
                "log_level": self.system.log_level,
                "enable_trace": self.system.enable_trace,
                "enable_audit": self.system.enable_audit,
                "demo_variance": self.system.demo_variance,
            },
            "erp_systems": [
                {
                    "name": e.name,
                    "erp_type": e.erp_type,
                    "enabled": e.enabled,
                    "is_primary": e.is_primary,
                    "base_url": e.base_url,
                    "auth_type": e.auth_type,
                    "api_key": e.api_key,
                    "username": e.username,
                    "timeout": e.timeout,
                    "retry_count": e.retry_count,
                    "retry_delay": e.retry_delay,
                    "circuit_breaker_threshold": e.circuit_breaker_threshold,
                    "circuit_breaker_timeout": e.circuit_breaker_timeout,
                    "custom_headers": e.custom_headers,
                }
                for e in self.erp_systems
            ],
        }
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def build_endpoint(self, erp_cfg: ERPConfig) -> APIEndpoint:
        """根据ERPConfig构建APIEndpoint"""
        headers = {}
        if erp_cfg.auth_type == "bearer" and erp_cfg.api_key:
            headers["Authorization"] = f"Bearer {erp_cfg.api_key}"
        elif erp_cfg.auth_type == "apikey" and erp_cfg.api_key:
            headers["X-API-Key"] = erp_cfg.api_key
        elif erp_cfg.auth_type == "basic":
            import base64
            credentials = base64.b64encode(
                f"{erp_cfg.username}:{erp_cfg.password}".encode()
            ).decode()
            headers["Authorization"] = f"Basic {credentials}"
        headers.update(erp_cfg.custom_headers)

        return APIEndpoint(
            name=erp_cfg.name,
            base_url=erp_cfg.base_url,
            auth_type=erp_cfg.auth_type,
            headers=headers,
            timeout=erp_cfg.timeout,
            retry_count=erp_cfg.retry_count,
            retry_delay=erp_cfg.retry_delay,
            circuit_breaker_threshold=erp_cfg.circuit_breaker_threshold,
            circuit_breaker_timeout=erp_cfg.circuit_breaker_timeout,
        )

    def build_adapter(self, erp_cfg: ERPConfig) -> BaseERPAdapter | MockDataGenerator:
        """根据配置构建适配器实例"""
        if erp_cfg.erp_type == "mock":
            return MockDataGenerator(
                variance=self.system.demo_variance,
                demo_prefix=DEMO_PREFIX,
                demo_disclaimer=DEMO_DISCLAIMER,
            )

        endpoint = self.build_endpoint(erp_cfg)

        if erp_cfg.erp_type == "sap":
            return SAPERPAdapter(endpoint, mode=self.system.mode)
        elif erp_cfg.erp_type == "yonyou":
            return YonyouERPAdapter(endpoint, mode=self.system.mode)
        else:
            # 通用适配器（可扩展）
            raise ValueError(f"不支持的ERP类型: {erp_cfg.erp_type}")
