"""
Shopify CMS Connector - GraphQL Admin API implementation.
支持 Shopify Admin API (API Key + Secret / OAuth) 认证。
"""
import base64
import json
import logging
import time
import urllib.request
import urllib.error
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime
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


# ── Shopify 专用数据模型 ──────────────────────────────────────────────────────

@dataclass
class VariantPayload:
    """商品变体"""
    title: str = "Default Title"
    price: str = "0.00"
    sku: str = ""
    inventory_quantity: int = 0
    inventory_policy: str = "deny"  # deny | continue
    weight: float = 0.0
    weight_unit: str = "kg"  # kg | lb | oz | g
    tax_code: str = ""
    option1: str = ""  # 第一个选项名称（如"颜色"）
    option2: str = ""  # 第二个选项名称（如"尺码"）
    option3: str = ""  # 第三个选项名称
    image_id: Optional[str] = None


@dataclass
class ImagePayload:
    """商品图片"""
    src: str = ""
    alt_text: str = ""
    position: int = 1


@dataclass
class SEOPayload:
    """SEO 元数据"""
    title: str = ""
    description: str = ""


@dataclass
class ProductPayload:
    """Shopify 商品发布载荷"""
    title: str = ""
    body_html: str = ""  # 商品描述（支持 HTML）
    vendor: str = ""  # 品牌/供应商
    product_type: str = ""  # 产品类型
    status: str = "draft"  # draft | active | archived | private
    tags: List[str] = field(default_factory=list)
    variants: List[VariantPayload] = field(default_factory=list)
    images: List[ImagePayload] = field(default_factory=list)
    seo: Optional[SEOPayload] = None
    # 映射 ContentPayload 字段（兼容基类接口）
    _content: Optional[ContentPayload] = None

    @classmethod
    def from_content_payload(cls, content: ContentPayload, **kwargs) -> "ProductPayload":
        """从通用 ContentPayload 构造 ProductPayload"""
        return cls(
            title=content.title,
            body_html=content.content,
            status="active" if content.status == "publish" else "draft",
            tags=[],
            variants=[
                VariantPayload(
                    title=content.title,
                    price=kwargs.get("price", "0.00"),
                    sku=kwargs.get("sku", ""),
                    inventory_quantity=kwargs.get("inventory_quantity", 0),
                )
            ],
            seo=SEOPayload(
                title=content.excerpt or content.title,
                description=content.content[:300],
            ),
            _content=content,
        )


# ── Shopify GraphQL 客户端 ───────────────────────────────────────────────────

class ShopifyGraphQLError(Exception):
    def __init__(self, errors: List[Dict[str, Any]]):
        self.errors = errors
        super().__init__(json.dumps(errors, ensure_ascii=False))


class ShopifyConnector(BaseCMSConnector):
    """
    Shopify Admin API 连接器。

    认证方式：
      - 私有应用：API Key + Secret → 生成访问令牌
      - 自定义应用 OAuth：客户端 ID + Secret → 完成 OAuth 流程

    接口：Shopify GraphQL Admin API 2024-01+
    """

    API_VERSION = "2024-01"

    def __init__(
        self,
        credential: CMSCredential,
        storage_path: str = "./shopify_history.json",
        shop_name: Optional[str] = None,
    ):
        """
        :param credential: CMSCredential，包含 url（https://{shop}.myshopify.com）
        :param storage_path: 操作历史存储路径
        :param shop_name: Shopify 商店名称（从 URL 提取，或手动指定）
        """
        super().__init__(credential, storage_path)
        self._shop_name = shop_name or self._extract_shop_name(credential.url)
        self._access_token: Optional[str] = credential.api_key  # 复用 api_key 字段存访问令牌
        self._api_base = (
            f"https://{self._shop_name}.myshopify.com/admin/api/{self.API_VERSION}/graphql.json"
        )

    # ── 认证 ──────────────────────────────────────────────
    def authenticate(self) -> bool:
        """验证 Shopify API 可访问性（查询 shop 信息）"""
        query = """
        query {
          shop {
            id
            name
            myshopifyDomain
          }
        }
        """
        try:
            resp = self._graphql(query)
            return resp.get("data", {}).get("shop") is not None
        except Exception as e:
            logger.error(f"Shopify authentication failed: {e}")
            return False

    @staticmethod
    def _extract_shop_name(url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        host = parsed.netloc or url
        # Shopify 官方域名：xxx.myshopify.com → 取 xxx
        if "myshopify.com" in host:
            return host.split(".")[0]
        # 自定义域名：shop.example.com → 取完整域名
        return host

    # ── 内容操作（商品 CRUD）──────────────────────────────────────────
    def create_content(self, payload: ContentPayload) -> Dict[str, Any]:
        """创建 Shopify 商品（Product）"""
        product = ProductPayload.from_content_payload(payload)
        query = self._build_product_create_mutation(product)
        resp = self._graphql(query)
        errors = resp.get("errors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        mutation_data = resp["data"]["productCreate"]
        user_errors = mutation_data.get("userErrors", [])
        if user_errors:
            raise ShopifyGraphQLError(user_errors)
        data = mutation_data["product"]
        if data is None:
            raise ShopifyGraphQLError([{"message": "productCreate returned null product"}])
        record = self._build_record(
            OperationType.CREATE, "product",
            self._extract_id(data["id"]),
            self._product_to_payload(product),
            data,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {
            "success": True,
            "id": self._extract_id(data["id"]),
            "title": data.get("title"),
            "handle": data.get("handle"),
            "record_id": record.id,
        }

    def update_content(self, content_id: int, payload: ContentPayload) -> Dict[str, Any]:
        """更新 Shopify 商品"""
        original = self.get_product(content_id)
        product = ProductPayload.from_content_payload(payload)
        query = self._build_product_update_mutation(content_id, product)
        resp = self._graphql(query)
        errors = resp.get("errors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        mutation_data = resp["data"]["productUpdate"]
        user_errors = mutation_data.get("userErrors", [])
        if user_errors:
            raise ShopifyGraphQLError(user_errors)
        data = mutation_data["product"]
        record = self._build_record(
            OperationType.UPDATE, "product",
            content_id,
            original,
            data,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {
            "success": True,
            "id": content_id,
            "title": data.get("title"),
            "handle": data.get("handle"),
            "record_id": record.id,
        }

    def delete_content(self, content_id: int, force: bool = False) -> Dict[str, Any]:
        """删除 Shopify 商品（归档 / 永久删除）"""
        original = self.get_product(content_id)
        mutation = "productDelete" if force else "productUpdate"
        gid = self._to_gid("Product", content_id)
        if force:
            query = f"""
            mutation {{
              productDelete(input: {{ id: "{gid}" }}) {{
                deletedProductId
                userErrors {{ field message }}
              }}
            }}
            """
        else:
            query = f"""
            mutation {{
              productUpdate(input: {{ id: "{gid}", archived: true }}) {{
                product {{ id title archived }}
                userErrors {{ field message }}
              }}
            }}
            """
        resp = self._graphql(query)
        errors = resp.get("errors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        record = self._build_record(
            OperationType.DELETE, "product",
            content_id,
            original,
            resp.get("data", {}),
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {
            "success": True,
            "deleted": True,
            "archived": not force,
            "record_id": record.id,
        }

    def get_content(self, content_id: int) -> Dict[str, Any]:
        """获取商品详情"""
        gid = self._to_gid("Product", content_id)
        query = f"""
        query {{
          product(id: "{gid}") {{
            id title handle status vendor productType
            bodyHtml tags createdAt updatedAt
            seo {{ title description }}
            variants(first: 250) {{
              edges {{ node {{
                id title sku price inventoryQuantity
                weight weightUnit inventoryPolicy
                image {{ id src altText }}
              }}}}
            }}
            images(first: 50) {{
              edges {{ node {{ id src altText position }} }}
            }}
          }}
        }}
        """
        resp = self._graphql(query)
        data = resp.get("data", {}).get("product")
        if not data:
            raise ValueError(f"Product {content_id} not found")
        return data

    def list_content(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """列出商品，支持分页/过滤"""
        params = params or {}
        first = params.get("first", 50)
        query_str = params.get("query", "")
        query = f"""
        query {{
          products(first: {first}{f', query: "{query_str}"' if query_str else ''}) {{
            edges {{ node {{
              id title handle status vendor productType
              createdAt updatedAt
            }}}}
            pageInfo {{ hasNextPage endCursor }}
          }}
        }}
        """
        resp = self._graphql(query)
        edges = resp.get("data", {}).get("products", {}).get("edges", [])
        return [e["node"] for e in edges]

    # ── 商品变体操作 ───────────────────────────────────────────
    def create_variant(self, product_id: int, variant: VariantPayload) -> Dict[str, Any]:
        """为商品添加变体"""
        gid = self._to_gid("Product", product_id)
        mutation = f"""
        mutation {{
          productVariantCreate(input: {{
            productId: "{gid}"
            price: "{variant.price}"
            sku: "{variant.sku}"
            title: "{variant.title}"
            inventoryQuantity: {variant.inventory_quantity}
            inventoryPolicy: {variant.inventory_policy.upper()}
            weight: {variant.weight}
            weightUnit: {variant.weight_unit.upper()}
            option1: "{variant.option1}"
            option2: "{variant.option2}"
            option3: "{variant.option3}"
          }}) {{
            productVariant {{ id title sku price }}
            userErrors {{ field message }}
          }}
        }}
        """
        resp = self._graphql(mutation)
        data = resp.get("data", {}).get("productVariantCreate", {})
        errors = data.get("userErrors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        variant_node = data["productVariant"]
        record = self._build_record(
            OperationType.CREATE, "variant",
            self._extract_id(variant_node["id"]),
            vars(variant),
            variant_node,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {"success": True, "id": self._extract_id(variant_node["id"]), "record_id": record.id}

    def update_variant(self, variant_id: int, variant: VariantPayload) -> Dict[str, Any]:
        """更新商品变体"""
        gid = self._to_gid("ProductVariant", variant_id)
        mutation = f"""
        mutation {{
          productVariantUpdate(input: {{
            id: "{gid}"
            price: "{variant.price}"
            sku: "{variant.sku}"
            title: "{variant.title}"
            inventoryQuantity: {variant.inventory_quantity}
            inventoryPolicy: {variant.inventory_policy.upper()}
            weight: {variant.weight}
            weightUnit: {variant.weight_unit.upper()}
            option1: "{variant.option1}"
            option2: "{variant.option2}"
            option3: "{variant.option3}"
          }}) {{
            productVariant {{ id title sku price }}
            userErrors {{ field message }}
          }}
        }}
        """
        resp = self._graphql(mutation)
        data = resp.get("data", {}).get("productVariantUpdate", {})
        errors = data.get("userErrors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        variant_node = data["productVariant"]
        record = self._build_record(
            OperationType.UPDATE, "variant",
            variant_id,
            vars(variant),
            variant_node,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {"success": True, "id": variant_id, "record_id": record.id}

    def delete_variant(self, variant_id: int) -> Dict[str, Any]:
        """删除商品变体"""
        gid = self._to_gid("ProductVariant", variant_id)
        mutation = f"""
        mutation {{
          productVariantDelete(id: "{gid}") {{
            deletedProductVariantId
            userErrors {{ field message }}
          }}
        }}
        """
        resp = self._graphql(mutation)
        data = resp.get("data", {}).get("productVariantDelete", {})
        errors = data.get("userErrors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        record = self._build_record(
            OperationType.DELETE, "variant",
            variant_id,
            {},
            data,
            OperationStatus.EXECUTED,
        )
        self._save_record(record)
        return {"success": True, "deleted": True, "record_id": record.id}

    # ── 商品图片操作 ───────────────────────────────────────────
    def add_product_image(self, product_id: int, image: ImagePayload) -> Dict[str, Any]:
        """为商品添加图片"""
        gid = self._to_gid("Product", product_id)
        mutation = f"""
        mutation {{
          productImageCreate(input: {{
            productId: "{gid}"
            src: "{image.src}"
            altText: "{image.alt_text}"
            position: {image.position}
          }}) {{
            image {{ id src altText }}
            userErrors {{ field message }}
          }}
        }}
        """
        resp = self._graphql(mutation)
        data = resp.get("data", {}).get("productImageCreate", {})
        errors = data.get("userErrors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        node = data["image"]
        return {"success": True, "id": self._extract_id(node["id"]), "src": node["src"]}

    def delete_product_image(self, image_id: str) -> Dict[str, Any]:
        """删除商品图片"""
        gid = self._to_gid("ProductImage", image_id)
        mutation = f"""
        mutation {{
          productImageDelete(id: "{gid}") {{
            deletedImageId
            userErrors {{ field message }}
          }}
        }}
        """
        resp = self._graphql(mutation)
        data = resp.get("data", {}).get("productImageDelete", {})
        errors = data.get("userErrors", [])
        if errors:
            raise ShopifyGraphQLError(errors)
        return {"success": True, "deleted": True}

    # ── 内部辅助 ───────────────────────────────────────────
    def get_product(self, product_id: int) -> Dict[str, Any]:
        return self.get_content(product_id)

    def _graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """发送 GraphQL 请求"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self._access_token,
            "User-Agent": "CMS-Executor/Shopify-1.0",
        }
        req = urllib.request.Request(
            self._api_base, data=body, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=self.credential.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode() if e.fp else ""
            logger.error(f"Shopify GraphQL error {e.code}: {err_body}")
            raise ShopifyGraphQLError([{"code": e.code, "message": err_body}])
        except urllib.error.URLError as e:
            logger.error(f"Shopify connection error: {e.reason}")
            raise ShopifyGraphQLError([{"code": 0, "message": str(e.reason)}])

    @staticmethod
    def _extract_id(gid: str) -> int:
        """从 Shopify GID 提取数字 ID，如 gid://shopify/Product/123 → 123"""
        try:
            return int(gid.split("/")[-1])
        except (ValueError, IndexError):
            return 0

    @staticmethod
    def _to_gid(resource: str, numeric_id: int) -> str:
        """将数字 ID 转换为 Shopify GID 格式"""
        return f"gid://shopify/{resource}/{numeric_id}"

    @staticmethod
    def _build_product_create_mutation(product: ProductPayload) -> str:
        tags_str = ", ".join(f'"{t}"' for t in product.tags)
        variants_input = ""
        if product.variants:
            variants_lines = []
            for v in product.variants:
                variants_lines.append(f"""{{
                  price: "{v.price}"
                  sku: "{v.sku}"
                  title: "{v.title}"
                  inventoryQuantity: {v.inventory_quantity}
                  inventoryPolicy: {v.inventory_policy.upper()}
                  weight: {v.weight}
                  weightUnit: {v.weight_unit.upper()}
                  option1: "{v.option1}"
                  option2: "{v.option2}"
                  option3: "{v.option3}"
                }}""")
            variants_input = f"variantsInput: [{','.join(variants_lines)}]"
        elif not product.title:
            variants_input = 'variantsInput: [{ price: "0.00", title: "Default Title" }]'
        images_input = ""
        if product.images:
            images_lines = []
            for img in product.images:
                images_lines.append(f'{{ src: "{img.src}", altText: "{img.alt_text}" }}')
            images_input = f"imagesInput: [{','.join(images_lines)}]"
        seo_block = ""
        if product.seo:
            seo_block = f'seo: {{ title: "{product.seo.title}", description: "{product.seo.description}" }}'
        return f"""
        mutation {{
          productCreate(input: {{
            title: "{product.title}"
            bodyHtml: """ + '"""' + f"""{product.body_html}""" + '"""' + f"""
            vendor: "{product.vendor}"
            productType: "{product.product_type}"
            status: {product.status.upper()}
            tags: [{tags_str}]
            {variants_input}
            {images_input}
            {seo_block}
          }}) {{
            product {{
              id title handle status vendor productType
              createdAt
              variants(first: 250) {{
                edges {{ node {{ id title sku price }} }}
              }}
            }}
            userErrors {{ field message }}
          }}
        }}
        """

    @staticmethod
    def _build_product_update_mutation(product_id: int, product: ProductPayload) -> str:
        gid = ShopifyConnector._to_gid("Product", product_id)
        tags_str = ", ".join(f'"{t}"' for t in product.tags)
        seo_block = ""
        if product.seo:
            seo_block = f'seo: {{ title: "{product.seo.title}", description: "{product.seo.description}" }}'
        return f"""
        mutation {{
          productUpdate(input: {{
            id: "{gid}"
            title: "{product.title}"
            bodyHtml: """ + '"""' + f"""{product.body_html}""" + '"""' + f"""
            vendor: "{product.vendor}"
            productType: "{product.product_type}"
            status: {product.status.upper()}
            tags: [{tags_str}]
            {seo_block}
          }}) {{
            product {{ id title handle status }}
            userErrors {{ field message }}
          }}
        }}
        """

    @staticmethod
    def _product_to_payload(product: ProductPayload) -> Dict[str, Any]:
        return {
            "title": product.title,
            "body_html": product.body_html,
            "vendor": product.vendor,
            "product_type": product.product_type,
            "status": product.status,
            "tags": product.tags,
            "variants": [vars(v) for v in product.variants],
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
        try:
            if record.entity_id is None:
                return False
            if record.operation == OperationType.DELETE:
                # 如果是归档操作，取消归档（设为 active）
                gid = self._to_gid("Product", record.entity_id)
                query = f"""
                mutation {{
                  productUpdate(input: {{ id: "{gid}", archived: false }}) {{
                    product {{ id title archived }}
                    userErrors {{ field message }}
                  }}
                }}
                """
                self._graphql(query)
                record.status = OperationStatus.ROLLED_BACK
                return True
            elif record.operation == OperationType.UPDATE:
                if record.payload:
                    payload = record.payload
                    gid = self._to_gid("Product", record.entity_id)
                    body_html = payload.get("body_html", "").replace('"', '\\"')
                    title = payload.get("title", "").replace('"', '\\"')
                    query = f"""
                    mutation {{
                      productUpdate(input: {{
                        id: "{gid}",
                        title: "{title}",
                        bodyHtml: """ + '"""' + f"""{body_html}""" + '"""' + f"""
                        vendor: "{payload.get('vendor', '')}"
                        productType: "{payload.get('product_type', '')}"
                        status: {payload.get('status', 'DRAFT').upper()}
                      }}) {{
                        product {{ id }}
                        userErrors {{ field message }}
                      }}
                    }}
                    """
                    self._graphql(query)
                    record.status = OperationStatus.ROLLED_BACK
                    return True
            elif record.operation == OperationType.CREATE:
                if record.entity_id:
                    gid = self._to_gid("Product", record.entity_id)
                    query = f"""
                    mutation {{
                      productDelete(input: {{ id: "{gid}" }}) {{
                        deletedProductId
                        userErrors {{ field message }}
                      }}
                    }}
                    """
                    self._graphql(query)
                    record.status = OperationStatus.ROLLED_BACK
                    return True
            record.status = OperationStatus.ROLLED_BACK
            return True
        except Exception as e:
            record.error_message = str(e)
            record.status = OperationStatus.FAILED
            logger.error(f"Shopify rollback failed for {record.id}: {e}")
            return False
