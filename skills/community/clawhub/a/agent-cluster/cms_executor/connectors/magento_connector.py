"""
Magento Connector — Magento REST API (v2)

支持：
- Products (CRUD，含复杂产品类型)
- Categories (树形结构管理)
- Customers
- Orders / Invoices / Shipments
- Stock Items (库存)
- CMS Pages / Blocks

认证：
- Integration Token（推荐，用于 Agent 场景）
- OAuth 1.0a（传统场景）
"""

from __future__ import annotations

import logging
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


class MagentoConnector(BaseCMSConnector):
    """
    Magento 2 REST API 连接器
    
    API Reference: https://developer.adobe.com/commerce/webapi/rest/
    """

    platform = CMSPlatform.MAGENTO

    def __init__(self, credentials: CMSCredentials):
        super().__init__(credentials)
        self._token: str | None = None
        self._store_id: int = credentials.extra_headers.get("store_id", 0)
        self._website_id: int = credentials.extra_headers.get("website_id", 0)
        self._capabilities = [
            "create_product", "read_product", "update_product", "delete_product",
            "manage_categories",
            "read_customer", "update_customer",
            "read_order", "create_invoice", "create_shipment",
            "update_inventory", "update_pricing",
            "manage_cms_pages", "manage_cms_blocks",
        ]

    def _build_client(self) -> httpx.AsyncClient:
        """构建带 Bearer Token 的客户端"""
        headers = {
            "User-Agent": "M-A3-CMS-Executor/Magento",
            "Content-Type": "application/json",
            **self.credentials.extra_headers,
        }
        if self.credentials.oauth_token:
            headers["Authorization"] = f"Bearer {self.credentials.oauth_token}"
        elif self.credentials.api_key:
            headers["Authorization"] = f"Bearer {self.credentials.api_key}"
        return httpx.AsyncClient(
            base_url=self.credentials.api_base,
            headers=headers,
            timeout=httpx.Timeout(self.credentials.timeout),
            follow_redirects=True,
        )

    async def _get_integration_token(self, client: httpx.AsyncClient) -> str:
        """获取 Admin Integration Token（如果尚未获取）"""
        if self._token:
            return self._token
        # 如果凭证中提供了集成 token，直接使用
        if self.credentials.oauth_token:
            self._token = self.credentials.oauth_token
            return self._token
        # 否则尝试通过 admin/token 获取（仅支持用户名/密码模式）
        # 此处假定 credentials.oauth_token 已经是有效的 admin token
        raise Exception("Magento integration token not configured. Please provide oauth_token.")

    async def _do_health_check(self, client: httpx.AsyncClient) -> bool:
        try:
            await self._get_integration_token(client)
            resp = await client.get("/rest/V1/store/storeConfigs")
            return resp.status_code == 200
        except Exception:
            return False

    def _store_headers(self, extra: dict = None) -> dict:
        h = {}
        if self._store_id:
            h["X-Upload-Key"] = str(self._store_id)  # Magento header
        if extra:
            h.update(extra)
        return h

    async def _do_read(self, client: httpx.AsyncClient, resource_id: str) -> dict:
        """
        读取 Magento 资源
        resource_id 格式: "products/SKU" | "categories/ID" | "orders/ID" | "customers/ID"
        """
        parts = resource_id.split("/", 1)
        domain = parts[0]
        identifier = parts[1] if len(parts) > 1 else parts[0]

        endpoint_map = {
            "products": f"/rest/V1/products/{identifier}",
            "categories": f"/rest/V1/categories/{identifier}",
            "orders": f"/rest/V1/orders/{identifier}",
            "customers": f"/rest/V1/customers/{identifier}",
            "cms_pages": f"/rest/V1/cmsPage/{identifier}",
            "cms_blocks": f"/rest/V1/cmsBlock/{identifier}",
        }
        endpoint = endpoint_map.get(domain, f"/rest/V1/{domain}/{identifier}")
        resp = await client.get(endpoint)
        resp.raise_for_status()
        return resp.json()

    async def _do_list(
        self, client: httpx.AsyncClient, filters: dict, page: int, per_page: int
    ) -> dict:
        search_criteria = {
            "searchCriteria": {
                "currentPage": page,
                "pageSize": min(per_page, 100),
            }
        }
        if filters.get("filter_groups"):
            search_criteria["searchCriteria"]["filter_groups"] = filters["filter_groups"]
        if filters.get("sort_orders"):
            search_criteria["searchCriteria"]["sortOrders"] = filters["sort_orders"]

        domain = filters.get("domain", "products")
        resp = await client.get(
            f"/rest/V1/{domain}",
            params={"searchCriteria": json.dumps(search_criteria["searchCriteria"])} if not filters.get("use_body") else None,
            json=search_criteria if filters.get("use_body") else None,
        )
        resp.raise_for_status()
        return resp.json()

    async def _do_create(self, client: httpx.AsyncClient, data: dict) -> dict:
        domain = data.pop("_domain", "products")
        endpoint_map = {
            "products": "/rest/V1/products",
            "categories": "/rest/V1/categories",
            "customers": "/rest/V1/customers",
        }
        endpoint = endpoint_map.get(domain, f"/rest/V1/{domain}")
        resp = await client.post(endpoint, json=data)
        resp.raise_for_status()
        return resp.json()

    async def _do_update(self, client: httpx.AsyncClient, resource_id: str, data: dict) -> dict:
        parts = resource_id.split("/", 1)
        domain = parts[0]
        identifier = parts[1] if len(parts) > 1 else parts[0]
        endpoint_map = {
            "products": f"/rest/V1/products/{identifier}",
            "categories": f"/rest/V1/categories/{identifier}",
            "customers": f"/rest/V1/customers/{identifier}",
            "orders": f"/rest/V1/orders/{identifier}",
        }
        endpoint = endpoint_map.get(domain, f"/rest/V1/{domain}/{identifier}")
        resp = await client.put(endpoint, json=data)
        resp.raise_for_status()
        return resp.json()

    async def _do_delete(self, client: httpx.AsyncClient, resource_id: str, soft: bool) -> dict:
        if soft:
            # Soft delete via status update
            parts = resource_id.split("/", 1)
            identifier = parts[1] if len(parts) > 1 else parts[0]
            return await self._do_update(client, resource_id, {"extension_attributes": {"is_deleted": True}})
        parts = resource_id.split("/", 1)
        domain = parts[0]
        identifier = parts[1] if len(parts) > 1 else parts[0]
        endpoint_map = {
            "products": f"/rest/V1/products/{identifier}",
            "categories": f"/rest/V1/categories/{identifier}",
            "customers": f"/rest/V1/customers/{identifier}",
        }
        endpoint = endpoint_map.get(domain, f"/rest/V1/{domain}/{identifier}")
        resp = await client.delete(endpoint)
        resp.raise_for_status()
        return resp.json()

    async def _do_upload_media(self, client: httpx.AsyncClient, file_path: str, metadata: dict) -> dict:
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        filename = file_path.split("/")[-1]
        with open(file_path, "rb") as f:
            file_content = base64.b64encode(f.read()).decode()
        payload = {
            "fileName": filename,
            "type": mime_type or "image/jpeg",
            "content": file_content,
            "mediaType": metadata.get("media_type", "image"),
        }
        resp = await client.post("/rest/V1/products/media", json=payload)
        resp.raise_for_status()
        return resp.json()

    def _normalize_read_response(self, raw: dict, resource_id: str) -> CMSResource:
        """将 Magento REST 响应归一化为 CMSResource"""
        domain = resource_id.split("/")[0]
        if domain == "products":
            return self._normalize_product(raw, resource_id)
        elif domain == "categories":
            return self._normalize_category(raw, resource_id)
        elif domain in ("cms_pages", "cmsPage"):
            return self._normalize_cms_page(raw, resource_id)
        else:
            return CMSResource(
                resource_id=resource_id,
                resource_type=CMSResourceType.OTHER,
                platform=self.platform,
                title=str(raw.get("id", resource_id)),
                metadata=raw,
                raw=raw,
            )

    def _normalize_product(self, raw: dict, resource_id: str) -> CMSResource:
        """归一化 Magento 产品"""
        name = raw.get("name", "")
        sku = raw.get("sku", resource_id.split("/")[-1])
        price = raw.get("price", 0.0)
        status = "active" if raw.get("status") == 1 else "disabled"
        custom_attributes = {
            a["attribute_code"]: a["value"] for a in raw.get("custom_attributes", [])
        }
        extension_attrs = raw.get("extension_attributes", {})
        stock = extension_attrs.get("stock_item", {})
        images = extension_attrs.get("product_images", [])

        return CMSResource(
            resource_id=resource_id,
            resource_type=CMSResourceType.PRODUCT,
            platform=self.platform,
            title=name,
            content=raw.get("description", ""),
            slug=sku,
            status=status,
            metadata={
                "sku": sku,
                "price": price,
                "cost": raw.get("cost"),
                "weight": raw.get("weight"),
                "category_ids": raw.get("category_links", []),
                "inventory": stock.get("qty", 0),
                "is_in_stock": stock.get("is_in_stock", True),
                "visibility": raw.get("visibility"),
                "type_id": raw.get("type_id", "simple"),
            },
            seo_title=custom_attributes.get("meta_title", ""),
            seo_description=custom_attributes.get("meta_description", ""),
            tags=[raw.get("type_id", "")],
            categories=[str(c.get("category_id")) for c in raw.get("category_links", [])],
            created_at=raw.get("created_at", ""),
            updated_at=raw.get("updated_at", ""),
            url=raw.get("extension_attributes", {}).get("request_url", ""),
            raw=raw,
        )

    def _normalize_category(self, raw: dict, resource_id: str) -> CMSResource:
        """归一化 Magento 分类"""
        return CMSResource(
            resource_id=resource_id,
            resource_type=CMSResourceType.POST,  # 分类作为内容分类
            platform=self.platform,
            title=raw.get("name", ""),
            slug=str(raw.get("id", "")),
            status="active" if raw.get("is_active", True) else "disabled",
            metadata={
                "parent_id": raw.get("parent_id"),
                "path": raw.get("path", ""),
                "position": raw.get("position"),
                "include_in_menu": raw.get("include_in_menu"),
            },
            created_at=raw.get("created_at", ""),
            updated_at=raw.get("updated_at", ""),
            raw=raw,
        )

    def _normalize_cms_page(self, raw: dict, resource_id: str) -> CMSResource:
        """归一化 Magento CMS Page"""
        return CMSResource(
            resource_id=resource_id,
            resource_type=CMSResourceType.PAGE,
            platform=self.platform,
            title=raw.get("title", ""),
            content=raw.get("content", ""),
            slug=raw.get("identifier", ""),
            status="published" if raw.get("is_active", True) else "draft",
            metadata={
                "layout_handle": raw.get("page_layout"),
                "meta_keywords": raw.get("meta_keywords"),
            },
            seo_title=raw.get("meta_title", ""),
            seo_description=raw.get("meta_description", ""),
            created_at=raw.get("creation_time", ""),
            updated_at=raw.get("update_time", ""),
            raw=raw,
        )

    def to_platform_format(self, data: dict, operation: str) -> dict:
        """将通用数据转换为 Magento REST API 格式"""
        result = {}
        if "title" in data:
            result["name" if "product" in str(data.get("_domain", "")) else "title"] = data["title"]
        if "description" in data:
            result["description"] = data["description"]
        if "short_description" in data:
            result["short_description"] = data["short_description"]
        if "price" in data:
            result["price"] = float(data["price"])
        if "status" in data:
            result["status"] = 1 if data["status"] in ("active", "published", "1") else 0
        if "weight" in data:
            result["weight"] = data["weight"]
        if "quantity" in data:
            result["extension_attributes"] = {
                "stock_item": {
                    "qty": data["quantity"],
                    "is_in_stock": data.get("is_in_stock", data["quantity"] > 0),
                }
            }
        if "visibility" in data:
            vis_map = {"hidden": 1, "catalog": 2, "search": 3, "catalog_search": 4}
            result["visibility"] = vis_map.get(data["visibility"], 4)
        if "seo_title" in data:
            result["custom_attributes"] = result.get("custom_attributes", []) + [
                {"attribute_code": "meta_title", "value": data["seo_title"]}
            ]
        if "seo_description" in data:
            result["custom_attributes"] = result.get("custom_attributes", []) + [
                {"attribute_code": "meta_description", "value": data["seo_description"]}
            ]
        return result

    # ── Magento 专属方法 ──────────────────────────────────────────────────

    async def update_inventory(self, sku: str, quantity: int, is_in_stock: bool = None) -> CMSResult:
        """
        更新 Magento 产品库存
        
        通过 /rest/V1/products/{sku}/stockItems/{itemId}
        """
        from .base_connector import CMSOperation
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=CMSResourceType.INVENTORY,
            platform=self.platform,
            resource_id=f"products/{sku}",
            data={"sku": sku, "quantity": quantity},
            risk_level=RiskLevel.MEDIUM,
        )
        try:
            client = self._client or self._build_client()
            snapshot_id = await self.snapshot(f"products/{sku}")
            stock_payload = {
                "stockItem": {
                    "qty": quantity,
                    "is_in_stock": is_in_stock if is_in_stock is not None else (quantity > 0),
                    "manage_stock": True,
                }
            }
            resp = await client.put(f"/rest/V1/products/{sku}/stockItems/1", json=stock_payload)
            resp.raise_for_status()
            elapsed = (time.perf_counter() - start) * 1000
            res = CMSResult.ok(op, resource_id=sku, data=resp.json())
            res.snapshot_id = snapshot_id
            res.execution_time_ms = elapsed
            return res
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return CMSResult.error(op, str(e))

    async def bulk_update_pricing(self, price_updates: list[dict]) -> list[CMSResult]:
        """
        批量更新价格（Magento Bulk API）
        
        price_updates: [{"sku": "SKU1", "price": 99.99}, ...]
        """
        from .base_connector import CMSOperation
        results = []
        for item in price_updates:
            sku = item["sku"]
            op = CMSOperation(
                operation_type=CMSOperationType.UPDATE,
                resource_type=CMSResourceType.PRODUCT,
                platform=self.platform,
                resource_id=f"products/{sku}",
                data={"price": item["price"]},
                risk_level=RiskLevel.HIGH,
            )
            result = await self.update(f"products/{sku}", {"price": item["price"]})
            results.append(result)
        return results
