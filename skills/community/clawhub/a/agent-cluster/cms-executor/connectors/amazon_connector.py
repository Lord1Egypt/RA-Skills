"""
Amazon CMS Connector - Selling Partner API (SP-API) implementation.
支持 Amazon SP-API (LWA OAuth) 认证。
"""
import base64
import hashlib
import hmac
import json
import logging
import time
import urllib.request
import urllib.error
import urllib.parse
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .base_connector import (
    BaseCMSConnector,
    CMSCredential,
    ContentPayload,
    OperationRecord,
    OperationType,
    OperationStatus,
)

logger = logging.getLogger(__name__)


# ── Amazon SP-API 专用数据模型 ────────────────────────────────────────────────

@dataclass
class AmazonListingPayload:
    """Amazon 商品列表载荷（用于创建/更新 Listing）"""
    sku: str = ""
    asin: str = ""  # 可选，创建后由 Amazon 分配
    product_type: str = ""  # e.g. "SHOES", "ELECTRONIC_ACCESSORY"
    title: str = ""
    description: str = ""
    brand: str = ""
    manufacturer: str = ""
    price_amount: float = 0.0
    price_currency: str = "USD"
    quantity: int = 0
    condition_type: str = "New"  # New | Used | Refurbished | Collectible
    fulfillment_channel: str = "MFN"  # MFN (Seller) | FBA
    operation_type: str = "CREATE"  # CREATE | UPDATE | DELETE
    bullet_points: List[str] = field(default_factory=list)
    search_terms: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)  # 图片 URL 列表
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_content_payload(
        cls, content: ContentPayload, sku: str = "", product_type: str = "GENERIC", **kwargs
    ) -> "AmazonListingPayload":
        """从通用 ContentPayload 构造 AmazonListingPayload"""
        return cls(
            sku=sku or f"SKU-{uuid.uuid4().hex[:8].upper()}",
            product_type=product_type,
            title=content.title,
            description=content.content[:2000],
            fulfillment_channel=kwargs.get("fulfillment_channel", "MFN"),
            condition_type=kwargs.get("condition_type", "New"),
            price_amount=float(kwargs.get("price_amount", 0)),
            price_currency=kwargs.get("price_currency", "USD"),
            quantity=int(kwargs.get("quantity", 0)),
            bullet_points=[],
        )


@dataclass
class PricePayload:
    """价格更新载荷"""
    sku: str = ""
    amount: float = 0.0
    currency: str = "USD"


@dataclass
class InventoryPayload:
    """库存更新载荷"""
    sku: str = ""
    quantity: int = 0
    fulfillment_channel: str = "MFN"


# ── Amazon SP-API 客户端 ─────────────────────────────────────────────────────

class AmazonSPAPIError(Exception):
    def __init__(self, code: int, message: str, errors: Optional[List[Dict]] = None):
        self.code = code
        self.message = message
        self.errors = errors or []
        super().__init__(f"[Amazon SP-API {code}] {message}")


class AmazonLWAError(Exception):
    """LWA (Login with Amazon) OAuth 错误"""
    def __init__(self, error: str, error_description: str = ""):
        self.error = error
        self.error_description = error_description
        super().__init__(f"[LWA {error}] {error_description}")


class AmazonConnector(BaseCMSConnector):
    """
    Amazon Selling Partner API (SP-API) 连接器。

    认证方式：LWA OAuth（需要先在 Seller Central 注册应用获取 Client ID/Secret）

    主要功能：
      - 商品列表管理（Catalog Items API）
      - 库存管理（FBA Inventory / Listings Items API）
      - 价格管理（Pricing API）
      - 商品报告（Reports API）
    """

    LWA_TOKEN_URL = "https://api.amazon.com/auth/o2/token"
    SPAPI_BASE = "https://sellingpartnerapi-na.amazon.com"

    def __init__(
        self,
        credential: CMSCredential,
        storage_path: str = "./amazon_history.json",
        region: str = "na",  # na | eu | fe
        marketplace_id: Optional[str] = None,
    ):
        """
        :param credential:
            - url: Seller Central 站点（如 https://sellercentral.amazon.com）
            - username: LWA Client ID
            - api_key: LWA Access Token（或通过 refresh_token 刷新获取）
            - app_password: LWA Client Secret
        :param storage_path: 操作历史存储路径
        :param region: SP-API 区域（na/eu/fe）
        :param marketplace_id: 目标市场 ID（如 A1AM79NJPZON8 for US）
        """
        super().__init__(credential, storage_path)
        self._region = region
        self._marketplace_id = marketplace_id or "A1AM79NJPZON8"  # 默认美国
        self._client_id = credential.username  # 复用 username 存 Client ID
        self._client_secret = credential.app_password  # 复用 app_password 存 Client Secret
        self._access_token = credential.api_key  # 复用 api_key 存 Access Token
        self._refresh_token = ""  # OAuth Refresh Token（需手动传入或从配置读取）
        self._region_map = {
            "na": ("sellingpartnerapi-na.amazon.com", "us-east-1"),
            "eu": ("sellingpartnerapi-eu.amazon.com", "eu-west-1"),
            "fe": ("sellingpartnerapi-fe.amazon.com", "us-west-2"),
        }
        self._endpoint_base, self._aws_region = self._region_map.get(
            region, self._region_map["na"]
        )
        self._spapi_base = f"https://{self._endpoint_base}/"

    # ── LWA OAuth ──────────────────────────────────────────
    def set_refresh_token(self, refresh_token: str) -> None:
        """设置 OAuth Refresh Token（用于自动刷新 Access Token）"""
        self._refresh_token = refresh_token

    def _ensure_valid_token(self) -> str:
        """确保 Access Token 有效，必要时自动刷新"""
        if self._access_token and not self._is_token_expired():
            return self._access_token
        if not self._refresh_token:
            raise AmazonLWAError(
                "missing_refresh_token",
                "No valid access token and no refresh token available. "
                "Call set_refresh_token() first or provide a valid api_key.",
            )
        self._access_token = self._refresh_access_token()
        return self._access_token

    def _is_token_expired(self) -> bool:
        """简单判断 token 是否过期（实际应解析 JWT exp 字段）"""
        return False  # 简化处理，可按需实现 JWT exp 解析

    def _refresh_access_token(self) -> str:
        """通过 Refresh Token 刷新 Access Token"""
        params = urllib.parse.urlencode(
            {
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            }
        ).encode("utf-8")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        req = urllib.request.Request(
            self.LWA_TOKEN_URL, data=params, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=self.credential.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["access_token"]
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logger.error(f"LWA token refresh failed: {e}")
            raise AmazonLWAError("token_refresh_failed", str(e))

    # ── 认证 ──────────────────────────────────────────────
    def authenticate(self) -> bool:
        """验证 SP-API 可访问性（查询 Seller Info）"""
        try:
            token = self._ensure_valid_token()
            resp = self._spapi_request("GET", "/sellers/v1/marketplaceParticipations", token=token)
            return "payload" in resp and resp["payload"] is not None
        except Exception as e:
            logger.error(f"Amazon SP-API authentication failed: {e}")
            return False

    # ── 内容操作（商品列表）──────────────────────────────────────────
    def create_content(self, payload: ContentPayload) -> Dict[str, Any]:
        """在 Amazon 创建商品列表（Listing）"""
        listing = AmazonListingPayload.from_content_payload(payload)
        listing.operation_type = "CREATE"
        result = self._submit_listing_item(listing)
        record = self._build_record(
            OperationType.CREATE, "listing",
            None,
            self._listing_to_payload(listing),
            result,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {
            "success": True,
            "sku": listing.sku,
            "status": result.get("status", "SUBMITTED"),
            "record_id": record.id,
        }

    def update_content(self, content_id: int, payload: ContentPayload) -> Dict[str, Any]:
        """更新 Amazon 商品列表"""
        sku = str(content_id)
        listing = AmazonListingPayload.from_content_payload(payload, sku=sku)
        listing.operation_type = "UPDATE"
        original = self.get_listing(sku)
        result = self._submit_listing_item(listing)
        record = self._build_record(
            OperationType.UPDATE, "listing",
            content_id,
            original,
            result,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {
            "success": True,
            "sku": sku,
            "status": result.get("status", "SUBMITTED"),
            "record_id": record.id,
        }

    def delete_content(self, content_id: int, force: bool = False) -> Dict[str, Any]:
        """删除 Amazon 商品列表（DELETE 操作）"""
        sku = str(content_id)
        original = self.get_listing(sku)
        actual_sku = original.get("sku", sku)  # 从 listing 中取真实 SKU
        listing = AmazonListingPayload(sku=actual_sku, operation_type="DELETE")
        result = self._submit_listing_item(listing)
        record = self._build_record(
            OperationType.DELETE, "listing",
            content_id,
            original,
            result,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {"success": True, "sku": actual_sku, "status": result.get("status"), "record_id": record.id}

    def get_content(self, content_id: int) -> Dict[str, Any]:
        """获取商品列表详情"""
        return self.get_listing(str(content_id))

    def get_listing(self, sku: str) -> Dict[str, Any]:
        """获取指定 SKU 的 Listing 详情"""
        token = self._ensure_valid_token()
        path = f"/listings/2021-08-01/items/{self._seller_id_placeholder()}/{urllib.parse.quote(sku)}"
        resp = self._spapi_request("GET", path, token=token)
        return resp.get("payload", resp)

    def list_content(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """列出商品列表"""
        params = params or {}
        token = self._ensure_valid_token()
        seller_id = self._seller_id_placeholder()
        path = f"/listings/2021-08-01/items/{seller_id}"
        qs_params = {}
        if params.get("status"):
            qs_params["status"] = params["status"]
        if params.get("sku"):
            qs_params["sku"] = params["sku"]
        qs = "?" + urllib.parse.urlencode(qs_params) if qs_params else ""
        resp = self._spapi_request("GET", f"{path}{qs}", token=token)
        items = resp.get("payload", {}).get("items", [])
        return items if isinstance(items, list) else []

    # ── 库存管理 ───────────────────────────────────────────
    def update_inventory(self, sku: str, quantity: int, fulfillment_channel: str = "MFN") -> Dict[str, Any]:
        """更新库存数量"""
        token = self._ensure_valid_token()
        inv_payload = {
            "sku": sku,
            "inventory": [
                {
                    "fulfillment_channel_code": fulfillment_channel,
                    "quantity": quantity,
                    "is_fulfillable": fulfillment_channel == "FBA",
                }
            ],
        }
        path = f"/inventory/v1/items/{urllib.parse.quote(sku)}"
        resp = self._spapi_request("PUT", path, token=token, data=inv_payload)
        record = self._build_record(
            OperationType.UPDATE, "inventory",
            None,
            {"sku": sku, "quantity": quantity},
            resp,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {"success": True, "sku": sku, "quantity": quantity, "record_id": record.id}

    def get_inventory(self, sku: str) -> Dict[str, Any]:
        """获取库存信息"""
        token = self._ensure_valid_token()
        path = f"/inventory/v1/items/{urllib.parse.quote(sku)}"
        resp = self._spapi_request("GET", path, token=token)
        return resp.get("payload", resp)

    def list_inventory(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """批量查询库存（分页）"""
        params = params or {}
        token = self._ensure_valid_token()
        seller_id = self._seller_id_placeholder()
        qs = "?" + urllib.parse.urlencode(
            {
                "sellerId": seller_id,
                "marketplaceIds": self._marketplace_id,
                "nextToken": params.get("next_token", ""),
            }
        )
        resp = self._spapi_request("GET", f"/inventory/v1/items{qs}", token=token)
        items = resp.get("payload", {}).get("items", [])
        return items if isinstance(items, list) else []

    # ── 价格管理 ───────────────────────────────────────────
    def update_pricing(self, sku: str, amount: float, currency: str = "USD") -> Dict[str, Any]:
        """更新商品价格"""
        token = self._ensure_valid_token()
        pricing_payload = {
            "prices": [
                {
                    "sku": sku,
                    "marketplace_id": self._marketplace_id,
                    "price": {"value": amount, "currency": currency},
                }
            ]
        }
        resp = self._spapi_request("POST", "/pricing/2022-05-01/prices", token=token, data=pricing_payload)
        record = self._build_record(
            OperationType.UPDATE, "pricing",
            None,
            {"sku": sku, "amount": amount, "currency": currency},
            resp,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {"success": True, "sku": sku, "amount": amount, "currency": currency, "record_id": record.id}

    def get_pricing(self, sku: str) -> Dict[str, Any]:
        """获取商品定价"""
        token = self._ensure_valid_token()
        qs = f"?MarketplaceId={self._marketplace_id}&SKUs={urllib.parse.quote(sku)}"
        resp = self._spapi_request("GET", f"/pricing/2022-05-01/prices{qs}", token=token)
        prices = resp.get("payload", [])
        return prices[0] if prices else {}

    # ── 报告 ──────────────────────────────────────────────
    def request_report(
        self,
        report_type: str = "GET_MERCHANT_LISTINGS_DATA",
        marketplace_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """请求生成报告"""
        token = self._ensure_valid_token()
        payload = {
            "reportType": report_type,
            "marketplaceIds": marketplace_ids or [self._marketplace_id],
            "reportOptions": {},
        }
        resp = self._spapi_request("POST", "/reports/2021-06-30/reports", token=token, data=payload)
        report_info = resp.get("payload", {})
        record = self._build_record(
            OperationType.CREATE, "report",
            None,
            {"report_type": report_type},
            report_info,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {
            "success": True,
            "report_id": report_info.get("reportId"),
            "status": report_info.get("status"),
            "record_id": record.id,
        }

    def get_report(self, report_id: str) -> Dict[str, Any]:
        """获取报告状态和内容"""
        token = self._ensure_valid_token()
        resp = self._spapi_request("GET", f"/reports/2021-06-30/reports/{report_id}", token=token)
        return resp.get("payload", resp)

    def get_report_document(self, report_document_id: str) -> Dict[str, Any]:
        """获取报告文档下载链接"""
        token = self._ensure_valid_token()
        resp = self._spapi_request(
            "GET",
            f"/reports/2021-06-30/documents/{report_document_id}",
            token=token,
        )
        return resp.get("payload", resp)

    # ── Feed 提交流式（用于批量 Listing 操作）─────────────────────
    def submit_feed(
        self,
        feed_type: str,
        content: str,
        content_type: str = "text/xml",
    ) -> Dict[str, Any]:
        """通过 Feed API 提交 XML 内容（如 POST_PRODUCT_DATA）"""
        token = self._ensure_valid_token()
        body = content.encode("utf-8")
        headers = {
            "Content-Type": content_type,
            "Accept": "application/json",
        }
        path = f"/feeds/2021-06-30/feeds"
        qs = f"?marketplaceIds={self._marketplace_id}"
        resp = self._spapi_request(
            "POST",
            f"{path}{qs}",
            token=token,
            data=body,
            headers=headers,
        )
        feed_info = resp.get("payload", {})
        record = self._build_record(
            OperationType.CREATE, "feed",
            None,
            {"feed_type": feed_type},
            feed_info,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {
            "success": True,
            "feed_id": feed_info.get("feedId"),
            "status": feed_info.get("processingStatus"),
            "record_id": record.id,
        }

    # ── 内部辅助 ───────────────────────────────────────────
    def _seller_id_placeholder(self) -> str:
        """从 credential.url 提取 seller id 或使用默认值"""
        # 实际应从 Seller Central OAuth 流程获取，此处用 URL 中的占位符
        parsed = urllib.parse.urlparse(self.credential.url)
        parts = parsed.netloc.split(".")
        # 如 sellercentral.amazon.com → 从配置中取
        return self.credential.username.split(":")[-1] if ":" in self.credential.username else self.credential.username

    def _spapi_request(
        self,
        method: str,
        path: str,
        token: Optional[str] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        发送 SP-API 请求（含 AWS SigV4 签名）。
        
        注意：完整实现需生成 AWS4-HMAC-SHA256 签名。
        此处为简化版，假设使用已签名的 Access Token 模式。
        """
        if token is None:
            token = self._ensure_valid_token()
        url = self._spapi_base.rstrip("/") + path
        request_headers = {
            "Authorization": f"Bearer {token}",
            "x-amz-access-token": token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "CMS-Executor/Amazon-SP-API-1.0",
        }
        if headers:
            request_headers.update(headers)
        body = None
        if data is not None:
            if isinstance(data, bytes):
                body = data
            else:
                body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=request_headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=self.credential.timeout) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode() if e.fp else ""
            logger.error(f"Amazon SP-API error {e.code}: {err_body}")
            try:
                err_data = json.loads(err_body)
                errors = err_data.get("errors", [])
            except json.JSONDecodeError:
                errors = [{"code": e.code, "message": err_body}]
            raise AmazonSPAPIError(e.code, err_body, errors)
        except urllib.error.URLError as e:
            logger.error(f"Amazon connection error: {e.reason}")
            raise AmazonSPAPIError(0, str(e.reason))

    def _submit_listing_item(self, listing: AmazonListingPayload) -> Dict[str, Any]:
        """通过 Listings Items API 提交商品列表"""
        token = self._ensure_valid_token()
        seller_id = self._seller_id_placeholder()
        sku_encoded = urllib.parse.quote(listing.sku)
        path = f"/listings/2021-08-01/items/{seller_id}/{sku_encoded}"
        # 构建 SP-API listings items payload
        attributes = {
            "productType": [{"value": listing.product_type}],
            "condition_type": [{"value": listing.condition_type}],
        }
        if listing.title:
            attributes["item_display_name"] = [{"value": listing.title}]
        if listing.description:
            attributes["product_description"] = [{"value": listing.description[:2000]}]
        if listing.brand:
            attributes["brand"] = [{"value": listing.brand}]
        if listing.bullet_points:
            attributes["bullet_point"] = [
                {"value": bp} for bp in listing.bullet_points[:5]
            ]
        if listing.price_amount > 0:
            attributes["price"] = [{
                "value": listing.price_amount,
                "currency": listing.price_currency,
            }]
        if listing.quantity >= 0:
            attributes["quantity"] = [{"value": listing.quantity}]
        payload = {
            "attributes": attributes,
            "operationalStatuses": [("ACTIVE" if listing.operation_type == "CREATE" else "ACTIVE")],
        }
        qs = f"?marketplaceId={self._marketplace_id}"
        method = "PUT" if listing.operation_type != "DELETE" else "DELETE"
        resp = self._spapi_request(method, f"{path}{qs}", token=token, data=payload)
        return resp.get("payload", resp)

    @staticmethod
    def _listing_to_payload(listing: AmazonListingPayload) -> Dict[str, Any]:
        return {
            "sku": listing.sku,
            "title": listing.title,
            "description": listing.description,
            "price_amount": listing.price_amount,
            "currency": listing.price_currency,
            "quantity": listing.quantity,
            "product_type": listing.product_type,
            "condition_type": listing.condition_type,
            "fulfillment_channel": listing.fulfillment_channel,
        }

    # ── 操作记录 ───────────────────────────────────────────
    def _build_record(
        self,
        operation: OperationType,
        entity_type: str,
        entity_id: Optional[int],
        payload: Dict[str, Any],
        response: Dict[str, Any],
        status: OperationStatus,
    ) -> OperationRecord:
        return OperationRecord(
            id=self._generate_id(),
            timestamp=datetime.now(),
            operation=operation,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
            response=response,
            status=status,
        )

    # ── 回滚 ──────────────────────────────────────────────
    def _do_rollback(self, record: OperationRecord) -> bool:
        """
        Amazon 回滚策略：
          - DELETE：重新创建 Listing
          - UPDATE：恢复到 payload 中的原始值
          - CREATE：删除 Listing
        注意：Amazon 是最终一致性系统，回滚后需等待同步
        """
        try:
            if record.operation == OperationType.DELETE:
                if record.payload:
                    listing = AmazonListingPayload(**record.payload)
                    listing.operation_type = "CREATE"
                    self._submit_listing_item(listing)
                    record.status = OperationStatus.ROLLED_BACK
                    return True
            elif record.operation == OperationType.UPDATE:
                if record.entity_id and record.payload:
                    listing = AmazonListingPayload(**record.payload)
                    listing.operation_type = "UPDATE"
                    self._submit_listing_item(listing)
                    record.status = OperationStatus.ROLLED_BACK
                    return True
            elif record.operation == OperationType.CREATE:
                if record.entity_id:
                    sku = str(record.entity_id)
                    listing = AmazonListingPayload(sku=sku, operation_type="DELETE")
                    self._submit_listing_item(listing)
                    record.status = OperationStatus.ROLLED_BACK
                    return True
            record.status = OperationStatus.ROLLED_BACK
            return True
        except Exception as e:
            record.error_message = str(e)
            record.status = OperationStatus.FAILED
            logger.error(f"Amazon rollback failed for {record.id}: {e}")
            return False
