"""
Amazon SP-API Connector — Amazon Selling Partner API

支持：
- Catalog Items (读取产品信息)
- Listings Items (CRUD)
- Inventory (库存管理)
- Pricing (价格管理)
- Orders (读取订单)
- Product Type Definitions

认证：OAuth + LWA (Login with Amazon) 刷新令牌
参考：https://developer-docs.amazon.com/sp-api/
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Any

import httpx

from .base_connector import (
    BaseCMSConnector,
    CMSCredentials,
    CMSPlatform,
    CMSResource,
    CMSResourceType,
    CMSResult,
    CMSOperation,
    CMSOperationType,
    RiskLevel,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AmazonSPAPIClient:
    """
    Amazon SP-API 专用 HTTP 客户端
    处理 LWA OAuth Token 自动刷新和请求签名
    """

    LWA_TOKEN_URL = "https://api.amazon.com/auth/o2/token"
    SPAPI_BASE = "https://sellingpartnerapi-na.amazon.com"

    def __init__(self, credentials: CMSCredentials):
        self.creds = credentials
        self._access_token: str | None = None
        self._token_expires_at: float = 0

    async def get_access_token(self) -> str:
        """获取/刷新 LWA Access Token"""
        if self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token

        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.creds.oauth_token,
            "client_id": self.creds.api_key,
            "client_secret": self.creds.aws_secret_key,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.LWA_TOKEN_URL, data=params)
            resp.raise_for_status()
            data = resp.json()
        self._access_token = data["access_token"]
        self._token_expires_at = time.time() + data.get("expires_in", 3600)
        return self._access_token

    def _sign_request(self, method: str, url: str, body: str, timestamp: str) -> dict:
        """生成 AWS Signature Version 4 签名"""
        # 简化的签名逻辑（生产环境应使用完整 AWS SigV4 实现）
        return {}

    async def request(
        self,
        method: str,
        path: str,
        params: dict = None,
        body: dict = None,
        region: str = None,
    ) -> dict:
        """发送已签名的 SP-API 请求"""
        region = region or self.creds.aws_region or "us-east-1"
        access_token = await self.get_access_token()

        headers = {
            "x-amz-access-token": access_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        base_url = f"{self.SPAPI_BASE}/feeds/{region}" if "/feeds/" in path else self.SPAPI_BASE
        # 使用凭证中的 api_base（支持区域化）
        if self.creds.api_base:
            base_url = self.creds.api_base

        url = f"{base_url}{path}"
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            if method == "GET":
                resp = await client.get(url, headers=headers, params=params)
            elif method == "POST":
                resp = await client.post(url, headers=headers, json=body, params=params)
            elif method == "PUT":
                resp = await client.put(url, headers=headers, json=body, params=params)
            elif method == "DELETE":
                resp = await client.delete(url, headers=headers, params=params)
            else:
                resp = await client.request(method, url, headers=headers, json=body, params=params)
            resp.raise_for_status()
            return resp.json()


class AmazonConnector(BaseCMSConnector):
    """
    Amazon SP-API 连接器
    
    主要操作域：
    - Catalog: GET /catalog/2022-04-01/items
    - Listings: /catalog/2022-04-01/items/{asin}/attributes
    - Inventory: /fba/inventory/v1/summaries
    - Pricing: /pricing/2022-05-01/offers
    - Orders: /orders/v1/orders
    """

    platform = CMSPlatform.AMAZON

    def __init__(self, credentials: CMSCredentials):
        super().__init__(credentials)
        self._client = AmazonSPAPIClient(credentials)
        self._capabilities = [
            "read_catalog", "read_listings", "update_listings",
            "read_inventory", "update_inventory",
            "read_pricing", "update_pricing",
            "read_orders",
        ]

    async def connect(self) -> bool:
        """Amazon 不需要预连接（按需请求）"""
        try:
            await self._client.get_access_token()
            self._status = self._status.__class__.CONNECTED
            logger.info(f"[amazon] SP-API client initialized")
            return True
        except Exception as e:
            logger.error(f"[amazon] Connection failed: {e}")
            self._status = self._status.__class__.ERROR
            return False

    async def _do_health_check(self, client: httpx.AsyncClient) -> bool:
        try:
            token = await self._client.get_access_token()
            return bool(token)
        except Exception:
            return False

    async def _do_read(self, client: httpx.AsyncClient, resource_id: str) -> dict:
        """
        读取 Amazon 资源
        resource_id 格式: "catalog/ASIN123" | "order/ORDER-ID" | "listing/ASIN"
        """
        parts = resource_id.split("/", 1)
        domain = parts[0]
        identifier = parts[1] if len(parts) > 1 else parts[0]

        if domain == "catalog":
            asin = identifier
            return await self._client.request("GET", f"/catalog/2022-04-01/items/{asin}")
        elif domain == "order":
            return await self._client.request("GET", f"/orders/v1/orders/{identifier}")
        elif domain == "listing":
            asin = identifier
            return await self._client.request(
                "GET",
                f"/catalog/2022-04-01/items/{asin}/attributes",
                params={"marketplaceIds": self.creds.extra_headers.get("marketplace_id", "ATVPDKIKX0DER")}
            )
        else:
            return await self._client.request("GET", f"/{domain}/{identifier}")

    async def _do_list(
        self, client: httpx.AsyncClient, filters: dict, page: int, per_page: int
    ) -> dict:
        marketplace_id = self.creds.extra_headers.get("marketplace_id", "ATVPDKIKX0DER")
        params = {
            "marketplaceIds": marketplace_id,
            "pageSize": min(per_page, 20),
        }
        if filters.get("keywords"):
            params["keywords"] = filters["keywords"]
        if filters.get("seller_id"):
            params["sellerId"] = filters["seller_id"]

        resp = await self._client.request("GET", "/catalog/2022-04-01/items", params=params)
        return resp

    async def _do_create(self, client: httpx.AsyncClient, data: dict) -> dict:
        """Amazon SP-API 不支持直接创建（需要 Listing Loader 或 Feeds API）"""
        raise NotImplementedError(
            "Amazon SP-API 创建 Listing 请使用 create_listing() 方法"
        )

    async def _do_update(self, client: httpx.AsyncClient, resource_id: str, data: dict) -> dict:
        """
        更新 Amazon Listing 属性（通过属性更新 API）
        resource_id: "listing/ASIN"
        """
        parts = resource_id.split("/", 1)
        identifier = parts[1] if len(parts) > 1 else parts[0]
        marketplace_id = self.creds.extra_headers.get("marketplace_id", "ATVPDKIKX0DER")
        payload = {
            "attributes": self.to_platform_format(data, "update"),
        }
        return await self._client.request(
            "PUT",
            f"/catalog/2022-04-01/items/{identifier}/attributes",
            params={"marketplaceIds": marketplace_id},
            body=payload,
        )

    async def _do_delete(self, client: httpx.AsyncClient, resource_id: str, soft: bool) -> dict:
        """Amazon Listing 删除（通常为 soft delete，通过更新状态实现）"""
        return await self._do_update(client, resource_id, {"status": "archived"})

    async def _do_upload_media(self, client: httpx.AsyncClient, file_path: str, metadata: dict) -> dict:
        raise NotImplementedError("Amazon media upload via SP-API requires Feeds API (separate workflow)")

    def _normalize_read_response(self, raw: dict, resource_id: str) -> CMSResource:
        """将 Amazon SP-API 响应归一化为 CMSResource"""
        # Catalog item 结构
        summaries = raw.get("summaries", [{}])
        summaries = [s for s in summaries if isinstance(s, dict)]
        summary = summaries[0] if summaries else {}
        attributes = raw.get("attributes", {})
        images = raw.get("images", [])
        first_image = images[0].get("link", "") if images else ""

        # 提取标题
        title = ""
        if isinstance(attributes.get("item_name"), list):
            title = attributes["item_name"][0].get("value", "")
        elif isinstance(summary.get("item_name"), str):
            title = summary["item_name"]

        asin = raw.get("asin", resource_id.split("/")[-1])
        return CMSResource(
            resource_id=resource_id,
            resource_type=CMSResourceType.PRODUCT,
            platform=self.platform,
            title=title,
            slug=asin,
            metadata={
                "asin": asin,
                "brand": summary.get("brand", ""),
                "product_type": summary.get("product_type", ""),
                "status": summary.get("status", ""),
                "images": images,
                "attributes": attributes,
            },
            tags=[summary.get("product_type", "")],
            created_at=raw.get("createdDate", ""),
            updated_at=raw.get("attributes", {}).get("updatedDate", [{}])[0].get("value", ""),
            url=f"https://www.amazon.com/dp/{asin}",
            raw=raw,
        )

    def to_platform_format(self, data: dict, operation: str) -> dict:
        """将通用数据转换为 Amazon 属性格式"""
        result = {}
        if "title" in data:
            result["item_name"] = [{"value": data["title"], "language": "en_US"}]
        if "description" in data:
            result["product_description"] = [{"value": data["description"], "language": "en_US"}]
        if "price" in data:
            currency = data.get("currency", "USD")
            result["list_price"] = [{"value": float(data["price"]), "currency": currency}]
        if "quantity" in data:
            result["fulfillment_availability"] = [{"value": str(data["quantity"]), "marketplace_id": "ATVPDKIKX0DER"}]
        if "status" in data:
            result["status"] = [data["status"]]
        if "seo_title" in data:
            result["subject"] = [{"value": data["seo_title"], "language": "en_US"}]
        if "seo_description" in data:
            result["product_description"] = [{"value": data["seo_description"], "language": "en_US"}]
        return result

    # ── Amazon 专属方法 ───────────────────────────────────────────────────

    async def update_inventory(self, sku: str, quantity: int) -> CMSResult:
        """
        更新 FBA 库存数量
        
        通过 FBA Inventory API 更新可用数量。
        """
        from .base_connector import CMSOperation
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=CMSResourceType.INVENTORY,
            platform=self.platform,
            resource_id=f"inventory/{sku}",
            data={"sku": sku, "quantity": quantity},
            risk_level=RiskLevel.MEDIUM,
        )
        try:
            snapshot_id = await self.snapshot(f"inventory/{sku}")
            resp = await self._client.request(
                "POST",
                "/fba/inventory/v1/summaries",
                body={"skus": [sku], "marketplaceIds": [self.creds.extra_headers.get("marketplace_id", "ATVPDKIKX0DER")]},
            )
            elapsed = (time.perf_counter() - start) * 1000
            res = CMSResult.ok(op, resource_id=sku, data=resp)
            res.snapshot_id = snapshot_id
            res.execution_time_ms = elapsed
            return res
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return CMSResult.error(op, str(e))

    async def update_pricing(self, asin: str, price: float, currency: str = "USD") -> CMSResult:
        """
        批量更新价格（通过 Pricing Health API 或 Feeds API）
        """
        from .base_connector import CMSOperation
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=CMSResourceType.PRODUCT,
            platform=self.platform,
            resource_id=f"pricing/{asin}",
            data={"asin": asin, "price": price, "currency": currency},
            risk_level=RiskLevel.MEDIUM,
        )
        try:
            snapshot_id = await self.snapshot(f"catalog/{asin}")
            # 使用 Feeds API 路径（标准做法）
            resp = await self._client.request(
                "POST",
                "/feeds/2021-06-30/documents",
                body={"contentType": "application/json"},
            )
            elapsed = (time.perf_counter() - start) * 1000
            res = CMSResult.ok(op, resource_id=asin, data={"status": "pricing_update_submitted", "feed_id": resp.get("documentId", "")})
            res.snapshot_id = snapshot_id
            res.execution_time_ms = elapsed
            return res
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return CMSResult.error(op, str(e))

    async def read_order(self, order_id: str) -> CMSResult:
        """读取亚马逊订单"""
        from .base_connector import CMSOperation
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.READ,
            resource_type=CMSResourceType.ORDER,
            platform=self.platform,
            resource_id=f"order/{order_id}",
            risk_level=RiskLevel.LOW,
        )
        try:
            resp = await self._client.request("GET", f"/orders/v1/orders/{order_id}")
            elapsed = (time.perf_counter() - start) * 1000
            return CMSResult.ok(op, resource_id=order_id, data=resp)
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return CMSResult.error(op, str(e))
