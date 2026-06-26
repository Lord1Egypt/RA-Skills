"""
Base CMS Connector — 抽象连接器基类

定义所有平台连接器的统一接口，确保：
1. 一致的 API 签名和返回格式
2. 幂等性保护（通过 idempotency_key）
3. 错误归一化
4. 快照/回滚支持
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Generic, TypeVar

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar("T")


# =============================================================================
# 枚举定义
# =============================================================================

class CMSPlatform(Enum):
    """支持的 CMS 平台"""
    WORDPRESS = "wordpress"
    SHOPIFY = "shopify"
    AMAZON = "amazon"
    MAGENTO = "magento"
    CUSTOM = "custom"


class CMSOperationType(Enum):
    """CMS 操作类型"""
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LIST = "list"
    UPLOAD = "upload"
    SNAPSHOT = "snapshot"


class CMSResourceType(Enum):
    """CMS 资源类型"""
    POST = "post"
    PAGE = "page"
    PRODUCT = "product"
    MEDIA = "media"
    ORDER = "order"
    INVENTORY = "inventory"
    CUSTOMER = "customer"
    SETTING = "setting"
    SEO_METADATA = "seo_metadata"
    OTHER = "other"


class CMSConnectionStatus(Enum):
    """连接状态"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


class RiskLevel(Enum):
    """操作风险等级"""
    LOW = "low"          # 读取、预览
    MEDIUM = "medium"    # 创建、局部更新
    HIGH = "high"        # 批量更新、删除
    CRITICAL = "critical"  # 整站操作、DROP


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class CMSCredentials:
    """
    CMS 凭据（加密存储，实际使用时从密钥管理器获取）
    
    支持多种认证方式：
    - api_key: 普通 API Key
    - oauth_token: OAuth 访问令牌
    - aws_ credentials: AWS 访问密钥（Amazon 专用）
    """
    platform: CMSPlatform
    api_base: str
    api_key: str = ""
    oauth_token: str = ""
    aws_access_key: str = ""
    aws_secret_key: str = ""
    aws_region: str = "us-east-1"
    extra_headers: dict = field(default_factory=dict)
    timeout: float = 30.0

    @classmethod
    def from_dict(cls, data: dict) -> "CMSCredentials":
        """从字典创建凭据对象"""
        return cls(
            platform=CMSPlatform(data.get("platform", "custom")),
            api_base=data.get("api_base", ""),
            api_key=data.get("api_key", ""),
            oauth_token=data.get("oauth_token", ""),
            aws_access_key=data.get("aws_access_key", ""),
            aws_secret_key=data.get("aws_secret_key", ""),
            aws_region=data.get("aws_region", "us-east-1"),
            extra_headers=data.get("extra_headers", {}),
            timeout=data.get("timeout", 30.0),
        )

    def masked(self) -> dict:
        """返回脱敏版本（用于日志）"""
        return {
            "platform": self.platform.value,
            "api_base": self.api_base,
            "api_key": self.api_key[:4] + "***" if self.api_key else "",
            "oauth_token": self.oauth_token[:4] + "***" if self.oauth_token else "",
            "has_aws": bool(self.aws_access_key),
        }


@dataclass
class CMSResource:
    """
    CMS 资源统一表示
    
    所有平台的内容/产品/订单等资源都映射为这个结构。
    """
    resource_id: str
    resource_type: CMSResourceType
    platform: CMSPlatform
    title: str = ""
    content: str = ""
    slug: str = ""
    status: str = "draft"
    metadata: dict = field(default_factory=dict)
    seo_title: str = ""
    seo_description: str = ""
    tags: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    url: str = ""
    raw: dict = field(default_factory=dict)  # 平台原生数据

    def fingerprint(self) -> str:
        """计算资源指纹，用于变更检测"""
        content = json.dumps({
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "metadata": self.metadata,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "resource_id": self.resource_id,
            "resource_type": self.resource_type.value,
            "platform": self.platform.value,
            "title": self.title,
            "content": self.content,
            "slug": self.slug,
            "status": self.status,
            "metadata": self.metadata,
            "seo_title": self.seo_title,
            "seo_description": self.seo_description,
            "tags": self.tags,
            "categories": self.categories,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "url": self.url,
        }


@dataclass
class CMSOperation:
    """
    CMS 操作请求
    
    描述一个完整的 CMS 写操作，包含幂等性保护。
    """
    operation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operation_type: CMSOperationType = CMSOperationType.READ
    resource_type: CMSResourceType = CMSResourceType.POST
    platform: CMSPlatform = CMSPlatform.WORDPRESS
    resource_id: str = ""
    idempotency_key: str = ""  # 用于幂等性保护
    data: dict = field(default_factory=dict)  # 操作数据
    agent_id: str = ""
    execution_id: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.idempotency_key:
            self.idempotency_key = f"{self.operation_type.value}:{self.resource_type.value}:{self.resource_id}:{self.data.get('slug', '')}"

    def to_dict(self) -> dict:
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type.value,
            "resource_type": self.resource_type.value,
            "platform": self.platform.value,
            "resource_id": self.resource_id,
            "success": self.success,
            "message": self.message,
            "error_code": self.error_code,
            "data": self.data,
            "snapshot_id": self.snapshot_id,
            "rollback_available": self.rollback_available,
            "execution_time_ms": self.execution_time_ms,
        }


@dataclass
class CMSResult:
    """
    CMS 操作结果（统一返回格式）
    
    无论成功/失败，所有 CMS 操作都返回这个结构。
    """
    success: bool
    operation_id: str
    platform: CMSPlatform
    operation_type: CMSOperationType
    resource_id: str = ""
    message: str = ""
    error_code: str = ""
    data: dict = field(default_factory=dict)
    snapshot_id: str = ""  # 关联的快照ID
    rollback_available: bool = False
    execution_time_ms: float = 0.0
    raw_response: Any = None

    @classmethod
    def ok(cls, op: CMSOperation, resource_id: str = "", data: dict = None, message: str = "OK") -> "CMSResult":
        return cls(
            success=True,
            operation_id=op.operation_id,
            platform=op.platform,
            operation_type=op.operation_type,
            resource_id=resource_id,
            message=message,
            data=data or {},
            rollback_available=op.operation_type in (CMSOperationType.UPDATE, CMSOperationType.DELETE),
        )

    @classmethod
    def error(cls, op: CMSOperation, message: str, error_code: str = "UNKNOWN") -> "CMSResult":
        return cls(
            success=False,
            operation_id=op.operation_id,
            platform=op.platform,
            operation_type=op.operation_type,
            message=message,
            error_code=error_code,
        )

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "operation_id": self.operation_id,
            "platform": self.platform.value,
            "operation_type": self.operation_type.value,
            "resource_id": self.resource_id,
            "message": self.message,
            "error_code": self.error_code,
            "snapshot_id": self.snapshot_id,
            "rollback_available": self.rollback_available,
            "execution_time_ms": self.execution_time_ms,
        }


# =============================================================================
# 危险操作检测
# =============================================================================

DANGEROUS_PATTERNS = [
    "DROP TABLE", "DROP DATABASE", "DELETE FROM", "TRUNCATE",
    "rm -rf", "rm /", "--", "EVAL_CALL", "EXEC_CALL",
    "0.00",  # price set to zero
    "price\":0", "price\": 0",  # price injection
]


def is_dangerous_operation(op: CMSOperation) -> tuple[bool, str]:
    """
    检测危险操作模式
    
    Returns:
        (is_dangerous, reason)
    """
    data_str = json.dumps(op.data, ensure_ascii=False).lower()
    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in data_str:
            return True, f"危险模式匹配: {pattern}"
    return False, ""


# =============================================================================
# 连接器基类
# =============================================================================

class BaseCMSConnector(ABC):
    """
    CMS 连接器抽象基类
    
    所有平台连接器必须实现以下方法：
    - _build_client(): 构建 HTTP 客户端
    - _normalize_read_response(): 将平台原生响应转为 CMSResource
    - to_platform_format(): 将通用数据转为平台原生格式
    
    基类提供：
    - 连接管理（connect/disconnect/health_check）
    - 通用错误处理
    - 幂等性保护
    - 快照支持（基类框架，子类可覆盖）
    """

    platform: CMSPlatform = CMSPlatform.CUSTOM
    _client: httpx.AsyncClient | None = None
    _connected_at: str = ""

    def __init__(self, credentials: CMSCredentials):
        self.credentials = credentials
        self._status = CMSConnectionStatus.DISCONNECTED
        self._capabilities: list[str] = []
        logger.info(f"[{self.platform.value}] Connector initialized with base URL: {credentials.api_base}")

    # ── 连接管理 ───────────────────────────────────────────────────────────

    async def connect(self) -> bool:
        """建立连接，初始化 HTTP 客户端"""
        if self._status == CMSConnectionStatus.CONNECTED:
            return True
        try:
            self._status = CMSConnectionStatus.CONNECTING
            self._client = self._build_client()
            ok = await self.health_check()
            if ok:
                self._status = CMSConnectionStatus.CONNECTED
                self._connected_at = datetime.now(timezone.utc).isoformat()
                logger.info(f"[{self.platform.value}] Connected successfully at {self._connected_at}")
                return True
            else:
                self._status = CMSConnectionStatus.ERROR
                return False
        except Exception as e:
            self._status = CMSConnectionStatus.ERROR
            logger.error(f"[{self.platform.value}] Connection failed: {e}")
            return False

    async def disconnect(self) -> None:
        """断开连接"""
        if self._client:
            await self._client.aclose()
            self._client = None
        self._status = CMSConnectionStatus.DISCONNECTED
        logger.info(f"[{self.platform.value}] Disconnected")

    async def health_check(self) -> bool:
        """健康检查，子类必须实现"""
        try:
            client = self._client or self._build_client()
            return await self._do_health_check(client)
        except Exception:
            return False

    @abstractmethod
    async def _do_health_check(self, client: httpx.AsyncClient) -> bool:
        """子类实现具体的健康检查逻辑"""
        ...

    def _build_client(self) -> httpx.AsyncClient:
        """构建 HTTP 客户端"""
        headers = {
            "User-Agent": f"M-A3-CMS-Executor/{self.platform.value}",
            **self.credentials.extra_headers,
        }
        return httpx.AsyncClient(
            base_url=self.credentials.api_base,
            headers=headers,
            timeout=httpx.Timeout(self.credentials.timeout),
            follow_redirects=True,
        )

    # ── 资源操作 ───────────────────────────────────────────────────────────

    async def read(self, resource_id: str) -> CMSResult:
        """
        读取单个资源
        
        Args:
            resource_id: 资源唯一标识符
            
        Returns:
            CMSResult: 包含 CMSResource.data
        """
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.READ,
            resource_type=CMSResourceType.OTHER,
            platform=self.platform,
            resource_id=resource_id,
            risk_level=RiskLevel.LOW,
        )
        try:
            client = self._client or self._build_client()
            response_data = await self._do_read(client, resource_id)
            resource = self._normalize_read_response(response_data, resource_id)
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.ok(op, resource_id=resource_id, data=resource.to_dict())
            result.execution_time_ms = elapsed
            result.raw_response = response_data
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.error(op, str(e))
            result.execution_time_ms = elapsed
            return result

    async def list(self, filters: dict = None, page: int = 1, per_page: int = 20) -> CMSResult:
        """列出资源列表"""
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.LIST,
            resource_type=CMSResourceType.OTHER,
            platform=self.platform,
            risk_level=RiskLevel.LOW,
        )
        try:
            client = self._client or self._build_client()
            response_data = await self._do_list(client, filters or {}, page, per_page)
            items = self._normalize_list_response(response_data)
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.ok(op, data={"items": items, "page": page, "per_page": per_page})
            result.execution_time_ms = elapsed
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.error(op, str(e))
            result.execution_time_ms = elapsed
            return result

    async def create(self, data: dict, resource_type: CMSResourceType = CMSResourceType.OTHER) -> CMSResult:
        """
        创建资源（幂等性保护）
        
        如果提供了 idempotency_key，重复调用不会创建重复资源。
        """
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.CREATE,
            resource_type=resource_type,
            platform=self.platform,
            idempotency_key=data.get("idempotency_key", ""),
            data=data,
            risk_level=RiskLevel.MEDIUM,
        )
        # 危险操作检测
        dangerous, reason = is_dangerous_operation(op)
        if dangerous:
            return CMSResult.error(op, f"危险操作被拦截: {reason}", error_code="DANGEROUS_OP")

        try:
            client = self._client or self._build_client()
            # 幂等性检查（子类可覆盖实现）
            existing = await self._check_idempotency(client, op.idempotency_key)
            if existing:
                result = CMSResult.ok(op, resource_id=existing, message="Idempotent: resource already exists")
                result.execution_time_ms = (time.perf_counter() - start) * 1000
                return result

            response_data = await self._do_create(client, self.to_platform_format(data, "create"))
            resource_id = self._extract_resource_id(response_data, "create")
            resource = self._normalize_read_response(response_data, resource_id)
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.ok(op, resource_id=resource_id, data=resource.to_dict())
            result.execution_time_ms = elapsed
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.error(op, str(e))
            result.execution_time_ms = elapsed
            return result

    async def update(self, resource_id: str, data: dict, resource_type: CMSResourceType = CMSResourceType.OTHER) -> CMSResult:
        """
        更新资源（先快照再更新）
        
        Returns CMSResult with snapshot_id for rollback.
        """
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=resource_type,
            platform=self.platform,
            resource_id=resource_id,
            data=data,
            risk_level=RiskLevel.MEDIUM,
        )
        dangerous, reason = is_dangerous_operation(op)
        if dangerous:
            return CMSResult.error(op, f"危险操作被拦截: {reason}", error_code="DANGEROUS_OP")

        try:
            client = self._client or self._build_client()
            # 1. 创建快照
            snapshot_id = await self.snapshot(resource_id)
            # 2. 执行更新
            response_data = await self._do_update(client, resource_id, self.to_platform_format(data, "update"))
            resource = self._normalize_read_response(response_data, resource_id)
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.ok(op, resource_id=resource_id, data=resource.to_dict())
            result.snapshot_id = snapshot_id
            result.rollback_available = True
            result.execution_time_ms = elapsed
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.error(op, str(e))
            result.execution_time_ms = elapsed
            return result

    async def delete(self, resource_id: str, soft: bool = True) -> CMSResult:
        """
        删除资源（软删除优先，snapshot_id 用于恢复）
        
        soft=True 时执行软删除（标记状态），soft=False 执行硬删除。
        """
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.DELETE,
            resource_type=CMSResourceType.OTHER,
            platform=self.platform,
            resource_id=resource_id,
            risk_level=RiskLevel.HIGH if soft else RiskLevel.CRITICAL,
        )
        try:
            client = self._client or self._build_client()
            snapshot_id = await self.snapshot(resource_id)
            response_data = await self._do_delete(client, resource_id, soft)
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.ok(op, resource_id=resource_id, message=f"{'Soft' if soft else 'Hard'} delete successful")
            result.snapshot_id = snapshot_id
            result.rollback_available = True
            result.execution_time_ms = elapsed
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.error(op, str(e))
            result.execution_time_ms = elapsed
            return result

    async def upload_media(self, file_path: str, metadata: dict = None) -> CMSResult:
        """上传媒体文件"""
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.UPLOAD,
            resource_type=CMSResourceType.MEDIA,
            platform=self.platform,
            data={"file_path": file_path, "metadata": metadata or {}},
            risk_level=RiskLevel.MEDIUM,
        )
        try:
            client = self._client or self._build_client()
            response_data = await self._do_upload_media(client, file_path, metadata or {})
            media_id = self._extract_resource_id(response_data, "upload")
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.ok(op, resource_id=media_id, data=response_data)
            result.execution_time_ms = elapsed
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            result = CMSResult.error(op, str(e))
            result.execution_time_ms = elapsed
            return result

    # ── 快照与回滚 ────────────────────────────────────────────────────────

    async def snapshot(self, resource_id: str) -> str:
        """
        创建资源快照（JSON 存储）
        
        子类应覆盖 _get_snapshot_path() 自定义存储路径。
        返回 snapshot_id。
        """
        import os
        from pathlib import Path

        snapshot_id = f"{self.platform.value}_{resource_id}_{int(time.time())}"
        try:
            read_result = await self.read(resource_id)
            if read_result.success:
                snapshot_dir = Path(f"snapshots/{self.platform.value}/{snapshot_id[:8]}")
                snapshot_dir.mkdir(parents=True, exist_ok=True)
                snapshot_file = snapshot_dir / f"{snapshot_id}.json"
                snapshot_data = {
                    "snapshot_id": snapshot_id,
                    "resource_id": resource_id,
                    "platform": self.platform.value,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "resource_data": read_result.data,
                    "raw_response": read_result.raw_response,
                }
                snapshot_file.write_text(json.dumps(snapshot_data, indent=2, ensure_ascii=False))
                logger.info(f"[{self.platform.value}] Snapshot created: {snapshot_id}")
                return snapshot_id
        except Exception as e:
            logger.warning(f"[{self.platform.value}] Snapshot failed for {resource_id}: {e}")
        return snapshot_id

    async def rollback(self, snapshot_id: str) -> CMSResult:
        """
        从快照恢复
        
        从快照文件中读取原始数据，执行恢复操作。
        """
        from pathlib import Path
        parts = snapshot_id.split("_")
        snapshot_dir = Path(f"snapshots/{self.platform.value}/{snapshot_id[:8]}")
        snapshot_file = snapshot_dir / f"{snapshot_id}.json"
        if not snapshot_file.exists():
            return CMSResult.error(
                CMSOperation(platform=self.platform, operation_type=CMSOperationType.SNAPSHOT),
                f"Snapshot not found: {snapshot_id}",
                error_code="SNAPSHOT_NOT_FOUND",
            )
        snapshot_data = json.loads(snapshot_file.read_text())
        resource_id = snapshot_data["resource_id"]
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            platform=self.platform,
            resource_id=resource_id,
            data=snapshot_data["resource_data"],
            risk_level=RiskLevel.MEDIUM,
        )
        return await self.update(resource_id, snapshot_data["resource_data"])

    # ── 抽象方法（子类必须实现） ──────────────────────────────────────────

    @abstractmethod
    async def _do_read(self, client: httpx.AsyncClient, resource_id: str) -> dict:
        """执行平台原生的读取操作"""
        ...

    @abstractmethod
    async def _do_list(self, client: httpx.AsyncClient, filters: dict, page: int, per_page: int) -> dict:
        """执行平台原生的列表操作"""
        ...

    @abstractmethod
    async def _do_create(self, client: httpx.AsyncClient, data: dict) -> dict:
        """执行平台原生的创建操作"""
        ...

    @abstractmethod
    async def _do_update(self, client: httpx.AsyncClient, resource_id: str, data: dict) -> dict:
        """执行平台原生的更新操作"""
        ...

    @abstractmethod
    async def _do_delete(self, client: httpx.AsyncClient, resource_id: str, soft: bool) -> dict:
        """执行平台原生的删除操作"""
        ...

    @abstractmethod
    async def _do_upload_media(self, client: httpx.AsyncClient, file_path: str, metadata: dict) -> dict:
        """执行平台原生的媒体上传操作"""
        ...

    @abstractmethod
    def _normalize_read_response(self, raw: dict, resource_id: str) -> CMSResource:
        """将平台原生响应归一化为 CMSResource"""
        ...

    @abstractmethod
    def to_platform_format(self, data: dict, operation: str) -> dict:
        """将通用数据转换为平台原生格式"""
        ...

    # ── 工具方法 ──────────────────────────────────────────────────────────

    def _extract_resource_id(self, response: dict, operation: str) -> str:
        """从响应中提取资源 ID"""
        for key in ["id", "ID", "entity_id", "post_id", "product_id", "resource_id"]:
            if key in response:
                return str(response[key])
        return f"{operation}_{int(time.time())}"

    def _normalize_list_response(self, response: dict) -> list[dict]:
        """将平台原生列表响应归一化"""
        if isinstance(response, list):
            return response
        for key in ["items", "data", "results", "records", "posts", "products"]:
            if key in response and isinstance(response[key], list):
                return response[key]
        return []

    async def _check_idempotency(self, client: httpx.AsyncClient, idempotency_key: str) -> str | None:
        """
        幂等性检查（子类可覆盖实现缓存检查）
        
        默认实现返回 None（不禁用重复创建）。
        子类如 Shopify 连接器应覆盖此方法实现真正的幂等检查。
        """
        return None

    @property
    def status(self) -> CMSConnectionStatus:
        return self._status

    @property
    def capabilities(self) -> list[str]:
        return self._capabilities
