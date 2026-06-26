"""
API Adapter Pattern - 多ERP系统适配器

支持多种ERP系统的统一接入：
- SAP S/4HANA
- 用友U8/NC/YonBIP
- 金蝶K3 Cloud/EAS
- Oracle ERP Cloud
- 通用REST API

每个ERP系统只需实现对应的Adapter类，即插即用。
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# 枚举定义
# =============================================================================

class ERPType(Enum):
    """支持的ERP类型"""
    SAP = "sap"
    YONYOU = "yonyou"         # 用友
    KINGDEE = "kingdee"       # 金蝶
    ORACLE = "oracle"
    CUSTOM = "custom"         # 自定义REST
    MOCK = "mock"             # 模拟数据（开发模式）


class ConnectionStatus(Enum):
    """连接状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"     # 降级运行
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class APIEndpoint:
    """API端点配置"""
    name: str
    base_url: str
    auth_type: str = "bearer"   # bearer / basic / apikey / oauth2
    headers: dict = field(default_factory=dict)
    timeout: float = 30.0
    retry_count: int = 3
    retry_delay: float = 1.0    # 秒
    circuit_breaker_threshold: int = 5  # 断路器阈值
    circuit_breaker_timeout: float = 60.0  # 断路器恢复时间（秒）


@dataclass
class APIResponse:
    """统一API响应格式"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    status_code: int = 200
    source: str = "unknown"      # 数据来源（ERP类型）
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    latency_ms: float = 0.0


@dataclass
class HealthCheckResult:
    """健康检查结果"""
    erp_type: str
    status: ConnectionStatus
    latency_ms: float
    message: str
    last_success: Optional[str] = None
    failure_count: int = 0


# =============================================================================
# 基类适配器
# =============================================================================

class BaseERPAdapter(ABC):
    """
    ERP适配器基类

    所有ERP适配器必须实现以下接口：
    - connect()         → 建立连接
    - health_check()   → 健康检查
    - query_inventory() → 查询库存
    - query_orders()   → 查询订单
    - create_order()   → 创建订单
    - query_suppliers() → 查询供应商
    """

    def __init__(
        self,
        endpoint: APIEndpoint,
        mode: str = "production",  # production / demo
    ):
        self.endpoint = endpoint
        self.mode = mode
        self._connected = False
        self._failure_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._circuit_open = False
        self._http_client: Optional[httpx.AsyncClient] = None

    @property
    def erp_type(self) -> str:
        return self.__class__.__name__.replace("ERPAdapter", "").lower()

    async def _get_client(self) -> httpx.AsyncClient:
        """获取或创建HTTP客户端"""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(
                base_url=self.endpoint.base_url,
                timeout=self.endpoint.timeout,
                headers=self.endpoint.headers,
            )
        return self._http_client

    def _check_circuit_breaker(self) -> bool:
        """断路器检查"""
        if not self._circuit_open:
            return False

        if self._last_failure_time:
            elapsed = (datetime.now() - self._last_failure_time).total_seconds()
            if elapsed >= self.endpoint.circuit_breaker_timeout:
                logger.info(f"[{self.erp_type}] 断路器恢复，尝试重置")
                self._circuit_open = False
                self._failure_count = 0
                return False
        return True

    def _record_success(self):
        """记录成功调用"""
        self._failure_count = 0
        self._circuit_open = False

    def _record_failure(self):
        """记录失败调用"""
        self._failure_count += 1
        self._last_failure_time = datetime.now()
        if self._failure_count >= self.endpoint.circuit_breaker_threshold:
            self._circuit_open = True
            logger.warning(
                f"[{self.erp_type}] 断路器打开（连续{self._failure_count}次失败），"
                f"将在{self.endpoint.circuit_breaker_timeout}秒后尝试恢复"
            )

    @abstractmethod
    async def connect(self) -> bool:
        """建立连接"""
        ...

    @abstractmethod
    async def health_check(self) -> HealthCheckResult:
        """健康检查"""
        ...

    @abstractmethod
    async def query_inventory(
        self,
        sku: Optional[str] = None,
        warehouse: Optional[str] = None,
        **kwargs
    ) -> APIResponse:
        """查询库存"""
        ...

    @abstractmethod
    async def query_orders(
        self,
        order_id: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs
    ) -> APIResponse:
        """查询订单"""
        ...

    @abstractmethod
    async def create_order(self, order_data: dict) -> APIResponse:
        """创建订单"""
        ...

    @abstractmethod
    async def query_suppliers(
        self,
        supplier_id: Optional[str] = None,
        **kwargs
    ) -> APIResponse:
        """查询供应商"""
        ...

    async def close(self):
        """关闭连接"""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()


# =============================================================================
# SAP S/4HANA 适配器
# =============================================================================

class SAPERPAdapter(BaseERPAdapter):
    """
    SAP S/4HANA 适配器

    SAP RFC/BAPI接口封装，使用OData或REST API
    关键配置项：SAP_HOST, SAP_CLIENT, SAP_SYSNR, SAP_USER, SAP_PASSWORD
    """

    async def connect(self) -> bool:
        try:
            client = await self._get_client()
            resp = await client.get("/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner")
            self._connected = resp.status_code in (200, 401)
            return self._connected
        except Exception as e:
            logger.error(f"[SAP] 连接失败: {e}")
            return False

    async def health_check(self) -> HealthCheckResult:
        import time
        start = time.time()
        try:
            client = await self._get_client()
            resp = await client.get("/sap/opu/odata/sap/API_BUSINESS_PARTNER/$metadata")
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self._record_success()
                return HealthCheckResult(
                    erp_type="sap",
                    status=ConnectionStatus.HEALTHY,
                    latency_ms=latency,
                    message="SAP S/4HANA 连接正常",
                    last_success=datetime.now().isoformat(),
                )
            return HealthCheckResult(
                erp_type="sap",
                status=ConnectionStatus.DEGRADED,
                latency_ms=latency,
                message=f"SAP 返回状态码 {resp.status_code}",
            )
        except Exception as e:
            self._record_failure()
            return HealthCheckResult(
                erp_type="sap",
                status=ConnectionStatus.UNAVAILABLE,
                latency_ms=(time.time() - start) * 1000,
                message=f"连接失败: {e}",
                failure_count=self._failure_count,
            )

    async def query_inventory(self, sku=None, warehouse=None, **kwargs) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="SAP 断路器已打开（服务不可用）", source="sap")
        import time
        start = time.time()
        try:
            client = await self._get_client()
            odata_filter = f"$filter=Material eq '{sku}'" if sku else ""
            resp = await client.get(f"/sap/opu/odata/sap/API_MATERIAL_STOCK_SRV/A_MaterialStock?{odata_filter}")
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self._record_success()
                return APIResponse(
                    success=True,
                    data=resp.json(),
                    source="sap",
                    latency_ms=latency,
                )
            self._record_failure()
            return APIResponse(success=False, error=f"SAP API返回{resp.status_code}", status_code=resp.status_code, source="sap")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="sap", latency_ms=(time.time() - start) * 1000)

    async def query_orders(self, order_id=None, status=None, **kwargs) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="SAP 断路器已打开", source="sap")
        try:
            client = await self._get_client()
            resp = await client.get("/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder")
            if resp.status_code == 200:
                self._record_success()
                return APIResponse(success=True, data=resp.json(), source="sap")
            self._record_failure()
            return APIResponse(success=False, error=f"SAP API返回{resp.status_code}", source="sap")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="sap")

    async def create_order(self, order_data: dict) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="SAP 断路器已打开", source="sap")
        try:
            client = await self._get_client()
            resp = await client.post("/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder", json=order_data)
            if resp.status_code in (200, 201):
                self._record_success()
                return APIResponse(success=True, data=resp.json(), source="sap", status_code=201)
            self._record_failure()
            return APIResponse(success=False, error=f"SAP API返回{resp.status_code}", source="sap")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="sap")

    async def query_suppliers(self, supplier_id=None, **kwargs) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="SAP 断路器已打开", source="sap")
        try:
            client = await self._get_client()
            url = f"/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner('{supplier_id}')" if supplier_id else "/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner"
            resp = await client.get(url)
            if resp.status_code == 200:
                self._record_success()
                return APIResponse(success=True, data=resp.json(), source="sap")
            self._record_failure()
            return APIResponse(success=False, error=f"SAP API返回{resp.status_code}", source="sap")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="sap")


# =============================================================================
# 用友适配器
# =============================================================================

class YonyouERPAdapter(BaseERPAdapter):
    """
    用友适配器（支持U8/NC/YonBIP）

    用友 REST API 接口封装
    关键配置项：YONYOU_HOST, YONYOU_ACCOUNT, YONYOU_PASSWORD, YONYOU_APPKEY
    """

    async def connect(self) -> bool:
        try:
            client = await self._get_client()
            resp = await client.post("/uapim/apiportal/login", json={
                "account": self.endpoint.headers.get("X-Yonyou-Account", ""),
                "password": self.endpoint.headers.get("X-Yonyou-Password", ""),
                "appkey": self.endpoint.headers.get("X-Yonyou-Appkey", ""),
            })
            self._connected = resp.status_code == 200
            return self._connected
        except Exception as e:
            logger.error(f"[用友] 连接失败: {e}")
            return False

    async def health_check(self) -> HealthCheckResult:
        import time
        start = time.time()
        try:
            client = await self._get_client()
            resp = await client.get("/uapim/apiportal/ping")
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self._record_success()
                return HealthCheckResult(erp_type="yonyou", status=ConnectionStatus.HEALTHY, latency_ms=latency, message="用友连接正常", last_success=datetime.now().isoformat())
            return HealthCheckResult(erp_type="yonyou", status=ConnectionStatus.DEGRADED, latency_ms=latency, message=f"返回{resp.status_code}")
        except Exception as e:
            self._record_failure()
            return HealthCheckResult(erp_type="yonyou", status=ConnectionStatus.UNAVAILABLE, latency_ms=(time.time() - start) * 1000, message=str(e), failure_count=self._failure_count)

    async def query_inventory(self, sku=None, warehouse=None, **kwargs) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="用友断路器已打开", source="yonyou")
        import time
        start = time.time()
        try:
            client = await self._get_client()
            params = {"invcode": sku} if sku else {}
            resp = await client.get("/uapim/apiportal/inventory/list", params=params)
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                self._record_success()
                return APIResponse(success=True, data=resp.json().get("data", []), source="yonyou", latency_ms=latency)
            self._record_failure()
            return APIResponse(success=False, error=f"用友API返回{resp.status_code}", source="yonyou")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="yonyou", latency_ms=(time.time() - start) * 1000)

    async def query_orders(self, order_id=None, status=None, **kwargs) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="用友断路器已打开", source="yonyou")
        try:
            client = await self._get_client()
            resp = await client.get("/uapim/apiportal/order/list", params={"id": order_id} if order_id else {})
            if resp.status_code == 200:
                self._record_success()
                return APIResponse(success=True, data=resp.json().get("data", []), source="yonyou")
            self._record_failure()
            return APIResponse(success=False, error=f"用友API返回{resp.status_code}", source="yonyou")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="yonyou")

    async def create_order(self, order_data: dict) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="用友断路器已打开", source="yonyou")
        try:
            client = await self._get_client()
            resp = await client.post("/uapim/apiportal/order/create", json=order_data)
            if resp.status_code in (200, 201):
                self._record_success()
                return APIResponse(success=True, data=resp.json(), source="yonyou", status_code=201)
            self._record_failure()
            return APIResponse(success=False, error=f"用友API返回{resp.status_code}", source="yonyou")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="yonyou")

    async def query_suppliers(self, supplier_id=None, **kwargs) -> APIResponse:
        if self._check_circuit_breaker():
            return APIResponse(success=False, error="用友断路器已打开", source="yonyou")
        try:
            client = await self._get_client()
            resp = await client.get("/uapim/apiportal/vendor/list", params={"vendorcode": supplier_id} if supplier_id else {})
            if resp.status_code == 200:
                self._record_success()
                return APIResponse(success=True, data=resp.json().get("data", []), source="yonyou")
            self._record_failure()
            return APIResponse(success=False, error=f"用友API返回{resp.status_code}", source="yonyou")
        except Exception as e:
            self._record_failure()
            return APIResponse(success=False, error=str(e), source="yonyou")


# =============================================================================
# 统一适配器管理器
# =============================================================================

class ERPAdapterManager:
    """
    ERP适配器管理器

    统一管理多个ERP适配器，支持：
    - 自动适配器选择
    - 故障降级（主ERP故障时切换到备用）
    - 健康检查轮询
    """

    def __init__(self):
        self._adapters: dict[str, BaseERPAdapter] = {}
        self._primary_erp: Optional[str] = None

    def register(self, name: str, adapter: BaseERPAdapter, is_primary: bool = False):
        """注册ERP适配器"""
        self._adapters[name] = adapter
        if is_primary or self._primary_erp is None:
            self._primary_erp = name
        logger.info(f"已注册ERP适配器: {name} {'(主)' if name == self._primary_erp else ''}")

    def get_adapter(self, name: Optional[str] = None) -> Optional[BaseERPAdapter]:
        """获取适配器，优先使用指定的，否则用主适配器"""
        if name and name in self._adapters:
            return self._adapters[name]
        if self._primary_erp:
            return self._adapters.get(self._primary_erp)
        return None

    def get_fallback_adapter(self) -> Optional[BaseERPAdapter]:
        """获取备用适配器（故障降级时使用）"""
        for name, adapter in self._adapters.items():
            if name != self._primary_erp:
                result = adapter._check_circuit_breaker()
                if not result:
                    return adapter
        return None

    async def query_inventory(self, sku=None, warehouse=None, erp_name: Optional[str] = None) -> APIResponse:
        """查询库存，支持故障降级"""
        adapter = self.get_adapter(erp_name)
        if adapter is None:
            return APIResponse(success=False, error="未配置ERP适配器", source="none")
        response = await adapter.query_inventory(sku=sku, warehouse=warehouse)
        if not response.success and response.error and "断路器" in response.error:
            # 故障降级：尝试备用适配器
            fallback = self.get_fallback_adapter()
            if fallback:
                logger.warning(f"主ERP [{self._primary_erp}] 不可用，切换到备用ERP")
                return await fallback.query_inventory(sku=sku, warehouse=warehouse)
        return response

    async def query_orders(self, order_id=None, status=None, erp_name: Optional[str] = None) -> APIResponse:
        """查询订单"""
        adapter = self.get_adapter(erp_name)
        if adapter is None:
            return APIResponse(success=False, error="未配置ERP适配器", source="none")
        return await adapter.query_orders(order_id=order_id, status=status)

    async def create_order(self, order_data: dict, erp_name: Optional[str] = None) -> APIResponse:
        """创建订单"""
        adapter = self.get_adapter(erp_name)
        if adapter is None:
            return APIResponse(success=False, error="未配置ERP适配器", source="none")
        return await adapter.create_order(order_data)

    async def query_suppliers(self, supplier_id=None, erp_name: Optional[str] = None) -> APIResponse:
        """查询供应商"""
        adapter = self.get_adapter(erp_name)
        if adapter is None:
            return APIResponse(success=False, error="未配置ERP适配器", source="none")
        return await adapter.query_suppliers(supplier_id=supplier_id)

    async def health_check_all(self) -> list[HealthCheckResult]:
        """对所有ERP进行健康检查"""
        results = []
        for name, adapter in self._adapters.items():
            result = await adapter.health_check()
            results.append(result)
        return results

    async def close_all(self):
        """关闭所有连接"""
        for adapter in self._adapters.values():
            await adapter.close()
