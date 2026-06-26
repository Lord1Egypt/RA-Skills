"""
Shopify Connector — Shopify GraphQL API

支持：
- Products (CRUD, inventory, pricing)
- Orders (read, fulfillment)
- Blog / Article 管理
- Media 上传 (Assets API)
- Store settings

认证：Shopify Admin API Access Token
"""

from __future__ import annotations

import hashlib
import logging
import time
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


# Shopify GraphQL Mutations & Queries
class ShopifyQueries:
    """常用 Shopify GraphQL 查询"""

    PRODUCT_QUERY = """
    query getProduct($id: ID!) {
        product(id: $id) {
            id title descriptionHtml status vendor productType
            createdAt updatedAt
            variants(first: 5) {
                edges { node {
                    id title price inventoryQuantity
                    selectedOptions { name value }
                }}
            }
            images(first: 5) { edges { node { id url altText }}}
            seo { title description }
            tags
        }
    }
    """

    PRODUCTS_QUERY = """
    query getProducts($first: Int!, $after: String) {
        products(first: $first, after: $after) {
            pageInfo { hasNextPage endCursor }
            edges { node { id title status vendor productType tags updatedAt }}
        }
    }
    """

    PRODUCT_CREATE_MUTATION = """
    mutation productCreate($input: ProductInput!) {
        productCreate(input: $input) {
            product { id title status }
            userErrors { field message }
        }
    }
    """

    PRODUCT_UPDATE_MUTATION = """
    mutation productUpdate($input: ProductInput!) {
        productUpdate(input: $input) {
            product { id title status }
            userErrors { field message }
        }
    }
    """

    PRODUCT_DELETE_MUTATION = """
    mutation productDelete($id: ID!) {
        productDelete(id: $id) {
            deletedProductId
            userErrors { field message }
        }
    }
    """

    INVENTORY_UPDATE_MUTATION = """
    mutation inventoryAdjustQuantity($input: InventoryAdjustQuantityInput!) {
        inventoryAdjustQuantity(input: $input) {
            inventoryLevel { id available }
            userErrors { field message }
        }
    }
    """

    BLOG_QUERY = """
    query getBlog($id: ID!) {
        blog(id: $id) {
            id title handle
            articles(first: 5) { edges { node { id title handle publishedAt }}}
        }
    }
    """

    ARTICLE_CREATE_MUTATION = """
    mutation articleCreate($input: ArticleInput!) {
        articleCreate(input: $input) {
            article { id title handle }
            userErrors { field message }
        }
    }
    """


class ShopifyConnector(BaseCMSConnector):
    """
    Shopify Admin API 连接器（GraphQL）
    
    API Reference: https://shopify.dev/docs/admin-api/graphql
    """

    platform = CMSPlatform.SHOPIFY

    def __init__(self, credentials: CMSCredentials):
        super().__init__(credentials)
        self._idempotency_store: dict[str, str] = {}  # key -> existing_resource_id
        self._capabilities = [
            "create_product", "read_product", "update_product", "delete_product",
            "update_inventory", "update_pricing",
            "read_order", "fulfill_order",
            "create_article", "read_article", "update_article",
            "upload_media",
        ]

    def _build_client(self) -> httpx.AsyncClient:
        """构建带 Shopify Admin API Token 的客户端"""
        headers = {
            "User-Agent": "M-A3-CMS-Executor/Shopify",
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.credentials.oauth_token,
            **self.credentials.extra_headers,
        }
        return httpx.AsyncClient(
            base_url=self.credentials.api_base,
            headers=headers,
            timeout=httpx.Timeout(self.credentials.timeout),
            follow_redirects=True,
        )

    async def _do_health_check(self, client: httpx.AsyncClient) -> bool:
        try:
            body = {"query": "{ shop { name } }"}
            resp = await client.post("/graphql.json", json=body)
            if resp.status_code == 200:
                data = resp.json()
                return "errors" not in data and data.get("data", {}).get("shop")
            return False
        except Exception:
            return False

    async def _graphql(self, client: httpx.AsyncClient, query: str, variables: dict = None) -> dict:
        """执行 GraphQL 请求"""
        body = {"query": query}
        if variables:
            body["variables"] = variables
        resp = await client.post("/graphql.json", json=body)
        resp.raise_for_status()
        result = resp.json()
        if result.get("errors"):
            raise Exception(f"GraphQL Error: {result['errors']}")
        return result.get("data", {})

    async def _do_read(self, client: httpx.AsyncClient, resource_id: str) -> dict:
        # 解析资源类型和 ID（Shopify 使用 gid:// 格式）
        if resource_id.startswith("gid://shopify/"):
            parts = resource_id.replace("gid://shopify/", "").split("/")
            resource_type = parts[0]
            gid_id = parts[1] if len(parts) > 1 else resource_id
        else:
            resource_type = "Product"
            gid_id = resource_id

        query_map = {
            "Product": ShopifyQueries.PRODUCT_QUERY,
            "Article": ShopifyQueries.BLOG_QUERY,
        }
        query = query_map.get(resource_type, ShopifyQueries.PRODUCT_QUERY)
        data = await self._graphql(client, query, {"id": resource_id})
        return data.get(resource_type.lower(), {}) or data

    async def _do_list(
        self, client: httpx.AsyncClient, filters: dict, page: int, per_page: int
    ) -> dict:
        variables = {"first": min(per_page, 50)}
        if page > 1:
            cursor = filters.get(f"cursor_page_{page-1}")
            if cursor:
                variables["after"] = cursor

        data = await self._graphql(client, ShopifyQueries.PRODUCTS_QUERY, variables)
        products = data.get("products", {})
        return {
            "items": [e["node"] for e in products.get("edges", [])],
            "page_info": products.get("pageInfo", {}),
        }

    async def _do_create(self, client: httpx.AsyncClient, data: dict) -> dict:
        mutation = ShopifyQueries.PRODUCT_CREATE_MUTATION
        result = await self._graphql(client, mutation, {"input": data})
        errors = result.get("productCreate", {}).get("userErrors", [])
        if errors:
            raise Exception(f"Shopify validation errors: {errors}")
        return result.get("productCreate", {}).get("product", {})

    async def _do_update(self, client: httpx.AsyncClient, resource_id: str, data: dict) -> dict:
        if not resource_id.startswith("gid://"):
            resource_id = f"gid://shopify/Product/{resource_id}"
        input_data = {"id": resource_id, **{k: v for k, v in data.items() if k != "id"}}
        result = await self._graphql(client, ShopifyQueries.PRODUCT_UPDATE_MUTATION, {"input": input_data})
        errors = result.get("productUpdate", {}).get("userErrors", [])
        if errors:
            raise Exception(f"Shopify validation errors: {errors}")
        return result.get("productUpdate", {}).get("product", {})

    async def _do_delete(self, client: httpx.AsyncClient, resource_id: str, soft: bool) -> dict:
        if not resource_id.startswith("gid://"):
            resource_id = f"gid://shopify/Product/{resource_id}"
        if not soft:
            result = await self._graphql(client, ShopifyQueries.PRODUCT_DELETE_MUTATION, {"id": resource_id})
            errors = result.get("productDelete", {}).get("userErrors", [])
            if errors:
                raise Exception(f"Shopify validation errors: {errors}")
            return result.get("productDelete", {})
        # Soft delete: archive the product
        return await self._do_update(client, resource_id, {"status": "ARCHIVED"})

    async def _do_upload_media(self, client: httpx.AsyncClient, file_path: str, metadata: dict) -> dict:
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        filename = file_path.split("/")[-1]
        # Shopify requires staged uploads first
        staged_query = """
        mutation createStagedUploads($input: [StagedUploadInput!]!) {
            stagedUploadsCreate(input: $input) {
                stagedTargets { url resourceUrl parameters { name value }}
            }
        }
        """
        staged_input = [{
            "resource": "FILE",
            "filename": filename,
            "mimeType": mime_type or "image/jpeg",
            "httpMethod": "POST",
        }]
        staged_result = await self._graphql(client, staged_query, {"input": staged_input})
        targets = staged_result.get("stagedUploadsCreate", {}).get("stagedTargets", [])
        if not targets:
            raise Exception("Failed to create staged upload")
        target = targets[0]
        upload_url = target["url"]
        params = {p["name"]: p["value"] for p in target["parameters"]}
        with open(file_path, "rb") as f:
            file_content = f.read()
        upload_resp = httpx.AsyncClient().request(
            "POST", upload_url, files={"file": (filename, file_content, mime_type)},
            data=params,
        )
        import asyncio
        if asyncio.iscoroutine(upload_resp):
            upload_resp = await upload_resp
        return {"url": target.get("resourceUrl", ""), "filename": filename}

    def _normalize_read_response(self, raw: dict, resource_id: str) -> CMSResource:
        """将 Shopify GraphQL 响应归一化为 CMSResource"""
        product_type = raw.get("__typename", "Product")
        resource_type_map = {
            "Product": CMSResourceType.PRODUCT,
            "Article": CMSResourceType.POST,
            "Order": CMSResourceType.ORDER,
        }
        variants = raw.get("variants", {}).get("edges", [])
        price = variants[0]["node"]["price"] if variants else ""
        inventory = sum(e["node"]["inventoryQuantity"] for e in variants)
        images = [e["node"]["url"] for e in raw.get("images", {}).get("edges", [])]
        seo = raw.get("seo", {}) or {}
        return CMSResource(
            resource_id=resource_id,
            resource_type=resource_type_map.get(product_type, CMSResourceType.OTHER),
            platform=self.platform,
            title=raw.get("title", ""),
            content=raw.get("descriptionHtml", ""),
            slug=raw.get("handle", ""),
            status=raw.get("status", "draft").lower(),
            metadata={
                "vendor": raw.get("vendor", ""),
                "product_type": raw.get("productType", ""),
                "price": price,
                "inventory_quantity": inventory,
                "images": images,
            },
            seo_title=seo.get("title", ""),
            seo_description=seo.get("description", ""),
            tags=raw.get("tags", []),
            created_at=raw.get("createdAt", ""),
            updated_at=raw.get("updatedAt", ""),
            url=raw.get("onlineStoreUrl", ""),
            raw=raw,
        )

    def to_platform_format(self, data: dict, operation: str) -> dict:
        """将通用 CMS 数据转换为 Shopify GraphQL input 格式"""
        result = {}
        if "title" in data:
            result["title"] = data["title"]
        if "descriptionHtml" in data:
            result["descriptionHtml"] = data["descriptionHtml"]
        if "handle" in data:
            result["handle"] = data["handle"]
        if "status" in data:
            result["status"] = data["status"].upper()  # ACTIVE, DRAFT, ARCHIVED
        if "vendor" in data:
            result["vendor"] = data["vendor"]
        if "product_type" in data:
            result["productType"] = data["product_type"]
        if "tags" in data:
            result["tags"] = data["tags"]
        if "seo_title" in data:
            result["seo"] = {"title": data["seo_title"], "description": data.get("seo_description", "")}
        if "variants" in data:
            result["variants"] = data["variants"]
        return result

    # ── Shopify 专属方法 ──────────────────────────────────────────────────

    async def update_inventory(self, variant_id: str, quantity: int, adjustment: bool = True) -> CMSResult:
        """
        更新库存数量
        
        Args:
            variant_id: Shopify variant GID
            quantity: 调整后的数量（adjustment=True 时为 delta）
            adjustment: True=增量调整，False=绝对设置
        """
        from .base_connector import CMSOperation
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=CMSResourceType.INVENTORY,
            platform=self.platform,
            resource_id=variant_id,
            data={"quantity": quantity},
            risk_level=RiskLevel.MEDIUM,
        )
        try:
            client = self._client or self._build_client()
            snapshot_id = await self.snapshot(variant_id)
            # 获取当前库存
            input_data = {
                "inventoryLevel": {
                    "availableQuantity": quantity,
                }
            }
            result = await self._graphql(client, ShopifyQueries.INVENTORY_UPDATE_MUTATION, {"input": {
                "inventoryItemId": variant_id,
                "locationId": data.get("location_id", ""),
                "delta": quantity if adjustment else 0,
            }})
            errors = result.get("inventoryAdjustQuantity", {}).get("userErrors", [])
            if errors:
                raise Exception(f"Shopify inventory errors: {errors}")
            elapsed = (time.perf_counter() - start) * 1000
            res = CMSResult.ok(op, resource_id=variant_id, data=result)
            res.snapshot_id = snapshot_id
            res.execution_time_ms = elapsed
            return res
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            res = CMSResult.error(op, str(e))
            res.execution_time_ms = elapsed
            return res

    async def update_price(self, variant_id: str, price: str, compare_at_price: str = "") -> CMSResult:
        """更新产品变体价格"""
        from .base_connector import CMSOperation
        start = time.perf_counter()
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=CMSResourceType.PRODUCT,
            platform=self.platform,
            resource_id=variant_id,
            risk_level=RiskLevel.MEDIUM,
        )
        try:
            client = self._client or self._build_client()
            snapshot_id = await self.snapshot(variant_id)
            update_input = {"id": variant_id, "price": price}
            if compare_at_price:
                update_input["compareAtPrice"] = compare_at_price
            result = await self._graphql(client, ShopifyQueries.PRODUCT_UPDATE_MUTATION, {"input": update_input})
            elapsed = (time.perf_counter() - start) * 1000
            res = CMSResult.ok(op, resource_id=variant_id, data=result.get("productUpdate", {}).get("product", {}))
            res.snapshot_id = snapshot_id
            res.execution_time_ms = elapsed
            return res
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return CMSResult.error(op, str(e))

    async def _check_idempotency(self, client: httpx.AsyncClient, idempotency_key: str) -> str | None:
        """Shopify 幂等性检查：基于 idempotency_key 查找已存在的资源"""
        return self._idempotency_store.get(idempotency_key)
