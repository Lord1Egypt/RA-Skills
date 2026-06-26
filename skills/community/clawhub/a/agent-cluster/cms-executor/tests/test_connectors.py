"""
Shopify & Amazon Connector 单元测试（Mock 模式，无需真实 API）。
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from connectors.base_connector import (
    CMSCredential, ContentPayload, OperationRecord,
    OperationType, OperationStatus,
)
from connectors.shopify_connector import (
    ShopifyConnector, ShopifyGraphQLError,
    ProductPayload, VariantPayload, ImagePayload, SEOPayload,
)
from connectors.amazon_connector import (
    AmazonConnector, AmazonSPAPIError, AmazonLWAError,
    AmazonListingPayload, PricePayload, InventoryPayload,
)


# ── Shopify Connector Tests ──────────────────────────────────────────────────

class TestShopifyConnector(unittest.TestCase):
    """Shopify 连接器单元测试（Mock GraphQL）"""

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_file.close()
        self.cred = CMSCredential(
            url="https://test-shop.myshopify.com",
            api_key="test_token_example",
        )
        self.shopify = ShopifyConnector(self.cred, storage_path=self.tmp_file.name)

    def tearDown(self):
        self.shopify.close()
        os.unlink(self.tmp_file.name)

    # ── 认证 ──────────────────────────────────────────────
    def test_authenticate_success(self):
        """认证成功时返回 True"""
        mock_resp = {
            "data": {
                "shop": {"id": "gid://shopify/Shop/1", "name": "Test Shop"}
            }
        }
        with patch.object(self.shopify, "_graphql", return_value=mock_resp):
            result = self.shopify.authenticate()
            self.assertTrue(result)

    def test_authenticate_failure(self):
        """认证失败时返回 False"""
        with patch.object(self.shopify, "_graphql", side_effect=ShopifyGraphQLError([{"message": "Bad token"}])):
            result = self.shopify.authenticate()
            self.assertFalse(result)

    # ── 商品创建 ─────────────────────────────────────────
    def test_create_content_success(self):
        """create_content 成功返回 id 和 record_id"""
        mock_graphql_resp = {
            "data": {
                "productCreate": {
                    "product": {
                        "id": "gid://shopify/Product/9876543",
                        "title": "Test Product",
                        "handle": "test-product",
                        "status": "ACTIVE",
                        "variants": {
                            "edges": [{"node": {"id": "gid://shopify/ProductVariant/1", "title": "Default Title", "price": "0.00"}}]
                        }
                    },
                    "userErrors": [],
                }
            }
        }
        with patch.object(self.shopify, "_graphql", return_value=mock_graphql_resp):
            payload = ContentPayload(
                title="Test Product",
                content="<p>Product description</p>",
                status="publish",
            )
            result = self.shopify.create_content(payload)
            self.assertTrue(result["success"])
            self.assertEqual(result["id"], 9876543)
            self.assertIn("record_id", result)

    def test_create_content_with_errors(self):
        """API 返回 userErrors 时抛出 ShopifyGraphQLError"""
        mock_resp = {
            "data": {
                "productCreate": {
                    "product": None,
                    "userErrors": [{"field": "title", "message": "required"}],
                }
            }
        }
        with patch.object(self.shopify, "_graphql", return_value=mock_resp):
            payload = ContentPayload(title="", content="Body")
            with self.assertRaises(ShopifyGraphQLError) as ctx:
                self.shopify.create_content(payload)
            self.assertEqual(ctx.exception.errors[0]["field"], "title")

    # ── 商品更新 ─────────────────────────────────────────
    def test_update_content_success(self):
        """update_content 成功保存原始快照用于回滚"""
        product_resp = {
            "data": {
                "product": {
                    "id": "gid://shopify/Product/123",
                    "title": "Old Title",
                    "handle": "old-product",
                    "status": "DRAFT",
                }
            }
        }
        update_resp = {
            "data": {
                "productUpdate": {
                    "product": {
                        "id": "gid://shopify/Product/123",
                        "title": "New Title",
                        "handle": "old-product",
                        "status": "ACTIVE",
                    },
                    "userErrors": [],
                }
            }
        }
        def gql_side_effect(query):
            if "query {" in query:
                return product_resp
            return update_resp

        with patch.object(self.shopify, "_graphql", side_effect=gql_side_effect):
            payload = ContentPayload(title="New Title", content="Updated", status="publish")
            result = self.shopify.update_content(123, payload)
            self.assertTrue(result["success"])
            self.assertEqual(result["id"], 123)

    # ── 商品删除 ─────────────────────────────────────────
    def test_delete_content_archive(self):
        """force=False 时执行归档（而非永久删除）"""
        product_resp = {
            "data": {
                "product": {
                    "id": "gid://shopify/Product/456",
                    "title": "Archived Product",
                }
            }
        }
        delete_resp = {
            "data": {
                "productUpdate": {
                    "product": {"id": "gid://shopify/Product/456", "title": "Archived Product", "archived": True},
                    "userErrors": [],
                }
            }
        }
        def gql_side_effect(query):
            if "query {" in query:
                return product_resp
            return delete_resp

        with patch.object(self.shopify, "_graphql", side_effect=gql_side_effect):
            result = self.shopify.delete_content(456, force=False)
            self.assertTrue(result["success"])
            self.assertTrue(result["archived"])

    def test_delete_content_permanent(self):
        """force=True 时永久删除商品"""
        product_resp = {
            "data": {
                "product": {
                    "id": "gid://shopify/Product/789",
                    "title": "Deleted Product",
                }
            }
        }
        delete_resp = {
            "data": {
                "productDelete": {
                    "deletedProductId": "gid://shopify/Product/789",
                    "userErrors": [],
                }
            }
        }
        def gql_side_effect(query):
            if "query {" in query:
                return product_resp
            return delete_resp

        with patch.object(self.shopify, "_graphql", side_effect=gql_side_effect):
            result = self.shopify.delete_content(789, force=True)
            self.assertTrue(result["success"])
            self.assertFalse(result["archived"])

    # ── 变体操作 ─────────────────────────────────────────
    def test_create_variant_success(self):
        """create_variant 成功返回变体 ID"""
        mock_resp = {
            "data": {
                "productVariantCreate": {
                    "productVariant": {
                        "id": "gid://shopify/ProductVariant/555",
                        "title": "Large / Blue",
                        "sku": "SKU-LB-01",
                        "price": "29.99",
                    },
                    "userErrors": [],
                }
            }
        }
        with patch.object(self.shopify, "_graphql", return_value=mock_resp):
            variant = VariantPayload(
                title="Large / Blue",
                sku="SKU-LB-01",
                price="29.99",
                inventory_quantity=100,
                option1="Large",
                option2="Blue",
            )
            result = self.shopify.create_variant(123, variant)
            self.assertTrue(result["success"])
            self.assertEqual(result["id"], 555)

    def test_delete_variant_success(self):
        """delete_variant 成功"""
        mock_resp = {
            "data": {
                "productVariantDelete": {
                    "deletedProductVariantId": "gid://shopify/ProductVariant/555",
                    "userErrors": [],
                }
            }
        }
        with patch.object(self.shopify, "_graphql", return_value=mock_resp):
            result = self.shopify.delete_variant(555)
            self.assertTrue(result["success"])
            self.assertTrue(result["deleted"])

    # ── 图片操作 ─────────────────────────────────────────
    def test_add_product_image_success(self):
        """add_product_image 成功返回图片 ID"""
        mock_resp = {
            "data": {
                "productImageCreate": {
                    "image": {
                        "id": "gid://shopify/ProductImage/111",
                        "src": "https://cdn.shopify.com/test.jpg",
                        "altText": "Product image",
                    },
                    "userErrors": [],
                }
            }
        }
        with patch.object(self.shopify, "_graphql", return_value=mock_resp):
            img = ImagePayload(src="https://cdn.shopify.com/test.jpg", alt_text="Product image")
            result = self.shopify.add_product_image(123, img)
            self.assertTrue(result["success"])
            self.assertEqual(result["id"], 111)

    # ── 列表查询 ─────────────────────────────────────────
    def test_list_content_returns_edges(self):
        """list_content 正确解析 GraphQL edges"""
        mock_resp = {
            "data": {
                "products": {
                    "edges": [
                        {"node": {"id": "gid://shopify/Product/1", "title": "Product 1"}},
                        {"node": {"id": "gid://shopify/Product/2", "title": "Product 2"}},
                    ],
                    "pageInfo": {"hasNextPage": False},
                }
            }
        }
        with patch.object(self.shopify, "_graphql", return_value=mock_resp):
            results = self.shopify.list_content({"first": 10})
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]["title"], "Product 1")

    # ── 回滚 ─────────────────────────────────────────────
    def test_rollback_create(self):
        """回滚创建操作 = 删除商品"""
        rollback_query = []
        def gql_side_effect(query):
            rollback_query.append(query)
            return {
                "data": {
                    "productDelete": {
                        "deletedProductId": "gid://shopify/Product/100",
                        "userErrors": [],
                    }
                }
            }

        with patch.object(self.shopify, "_graphql", side_effect=gql_side_effect):
            record = OperationRecord(
                id="test-rollback-1",
                timestamp=__import__("datetime").datetime.now(),
                operation=OperationType.CREATE,
                entity_type="product",
                entity_id=100,
                payload={"title": "Rollback Product"},
                response={},
                status=OperationStatus.EXECUTED,
            )
            result = self.shopify._do_rollback(record)
            self.assertTrue(result)
            self.assertEqual(record.status, OperationStatus.ROLLED_BACK)
            self.assertIn("productDelete", rollback_query[0])

    # ── 数据模型转换 ─────────────────────────────────────
    def test_product_payload_from_content(self):
        """ProductPayload.from_content_payload 正确转换"""
        content = ContentPayload(
            title="Shopify Product",
            content="<p>Great product</p>",
            status="publish",
            excerpt="SEO title here",
        )
        product = ProductPayload.from_content_payload(
            content,
            price="19.99",
            sku="SKU-001",
            inventory_quantity=50,
        )
        self.assertEqual(product.title, "Shopify Product")
        self.assertEqual(product.status, "active")
        self.assertEqual(product.variants[0].price, "19.99")
        self.assertEqual(product.variants[0].sku, "SKU-001")
        self.assertEqual(product.variants[0].inventory_quantity, 50)
        self.assertIsNotNone(product.seo)


# ── Amazon Connector Tests ──────────────────────────────────────────────────

class TestAmazonConnector(unittest.TestCase):
    """Amazon SP-API 连接器单元测试（Mock HTTP）"""

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_file.close()
        self.cred = CMSCredential(
            url="https://sellercentral.amazon.com",
            username="amzn1.application-xxx.client_id",
            api_key="Atza|xxx-access-token",
            app_password="test_secret_example",
        )
        self.amazon = AmazonConnector(
            self.cred,
            storage_path=self.tmp_file.name,
            region="na",
            marketplace_id="A1AM79NJPZON8",
        )

    def tearDown(self):
        self.amazon.close()
        os.unlink(self.tmp_file.name)

    # ── 认证 ─────────────────────────────────────────────
    def test_authenticate_success(self):
        """认证成功时返回 True"""
        mock_resp = {"payload": [{"sellerId": "A2XYZ", "marketplaceId": "ATVPDKIKX0DER"}]}
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            result = self.amazon.authenticate()
            self.assertTrue(result)

    def test_authenticate_failure(self):
        """认证失败时返回 False"""
        with patch.object(self.amazon, "_spapi_request", side_effect=AmazonSPAPIError(401, "Unauthorized")):
            result = self.amazon.authenticate()
            self.assertFalse(result)

    def test_ensure_valid_token_with_refresh(self):
        """无 token 时使用 refresh_token 刷新"""
        self.amazon._access_token = None
        self.amazon._refresh_token = "refresh_token_abc"
        with patch.object(self.amazon, "_refresh_access_token", return_value="new_access_token"):
            token = self.amazon._ensure_valid_token()
            self.assertEqual(token, "new_access_token")

    def test_ensure_valid_token_no_refresh_raises(self):
        """无 token 且无 refresh_token 时抛出 AmazonLWAError"""
        self.amazon._access_token = None
        self.amazon._refresh_token = ""
        with self.assertRaises(AmazonLWAError) as ctx:
            self.amazon._ensure_valid_token()
        self.assertEqual(ctx.exception.error, "missing_refresh_token")

    # ── 商品创建 ─────────────────────────────────────────
    def test_create_content_success(self):
        """create_content 成功返回 SKU 和 record_id"""
        mock_resp = {
            "payload": {
                "sku": "SKU-ABC123",
                "status": "SUBMITTED",
                "summaries": [],
            }
        }
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            payload = ContentPayload(title="Amazon Product", content="Description here")
            result = self.amazon.create_content(payload)
            self.assertTrue(result["success"])
            self.assertIn("SKU-", result["sku"])
            self.assertEqual(result["status"], "SUBMITTED")
            self.assertIn("record_id", result)

    def test_create_content_generates_sku(self):
        """未提供 SKU 时自动生成"""
        mock_resp = {"payload": {"status": "SUBMITTED", "summaries": []}}
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            payload = ContentPayload(title="No SKU Product", content="Desc")
            result = self.amazon.create_content(payload)
            self.assertTrue(result["success"])
            self.assertRegex(result["sku"], r"^SKU-[A-F0-9]+$")

    # ── 商品更新 ─────────────────────────────────────────
    def test_update_content_success(self):
        """update_content 成功触发 PUT 请求"""
        get_resp = {
            "payload": {
                "sku": "SKU-UPD-001",
                "attributes": {"productType": [{"value": "SHOES"}]},
            }
        }
        update_resp = {
            "payload": {
                "sku": "SKU-UPD-001",
                "status": "SUBMITTED",
            }
        }
        def spapi_side_effect(*args, **kwargs):
            if args[1].startswith("/listings"):
                return update_resp
            return get_resp

        with patch.object(self.amazon, "_spapi_request", side_effect=spapi_side_effect):
            payload = ContentPayload(title="Updated Title", content="Updated desc")
            result = self.amazon.update_content(123, payload)
            self.assertTrue(result["success"])
            self.assertEqual(result["status"], "SUBMITTED")

    # ── 商品删除 ─────────────────────────────────────────
    def test_delete_content_success(self):
        """delete_content 执行 DELETE 操作"""
        get_resp = {
            "payload": {
                "sku": "SKU-DEL-001",
                "attributes": {},
            }
        }
        delete_resp = {
            "payload": {
                "sku": "SKU-DEL-001",
                "status": "SUBMITTED",
            }
        }
        def spapi_side_effect(*args, **kwargs):
            if args[0] == "GET":
                return get_resp
            return delete_resp

        with patch.object(self.amazon, "_spapi_request", side_effect=spapi_side_effect):
            result = self.amazon.delete_content(123)
            self.assertTrue(result["success"])
            self.assertEqual(result["sku"], "SKU-DEL-001")

    # ── 库存管理 ─────────────────────────────────────────
    def test_update_inventory_success(self):
        """update_inventory 成功"""
        mock_resp = {"payload": {"sku": "SKU-INV-001", "items": []}}
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            result = self.amazon.update_inventory("SKU-INV-001", quantity=200)
            self.assertTrue(result["success"])
            self.assertEqual(result["quantity"], 200)
            self.assertIn("record_id", result)

    def test_get_inventory_returns_payload(self):
        """get_inventory 返回库存数据"""
        mock_resp = {
            "payload": {
                "sku": "SKU-GET-001",
                "inventory": [{"fulfillmentChannelCode": "MFN", "quantity": 50}],
            }
        }
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            result = self.amazon.get_inventory("SKU-GET-001")
            self.assertEqual(result["sku"], "SKU-GET-001")

    # ── 价格管理 ─────────────────────────────────────────
    def test_update_pricing_success(self):
        """update_pricing 成功"""
        mock_resp = {"payload": [{"sku": "SKU-PRC-001", "status": "SUBMITTED"}]}
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            result = self.amazon.update_pricing("SKU-PRC-001", amount=49.99, currency="USD")
            self.assertTrue(result["success"])
            self.assertEqual(result["amount"], 49.99)
            self.assertEqual(result["currency"], "USD")

    def test_get_pricing_returns_price(self):
        """get_pricing 返回价格数据"""
        mock_resp = {
            "payload": [
                {
                    "sku": "SKU-PRC-GET",
                    "price": {"value": 29.99, "currency": "USD"},
                }
            ]
        }
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            result = self.amazon.get_pricing("SKU-PRC-GET")
            self.assertEqual(result["price"]["value"], 29.99)

    # ── 报告 ─────────────────────────────────────────────
    def test_request_report_success(self):
        """request_report 返回 report_id"""
        mock_resp = {
            "payload": {
                "reportId": "REP-12345678",
                "status": "IN_PROGRESS",
                "reportType": "GET_MERCHANT_LISTINGS_DATA",
            }
        }
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            result = self.amazon.request_report()
            self.assertTrue(result["success"])
            self.assertEqual(result["report_id"], "REP-12345678")
            self.assertEqual(result["status"], "IN_PROGRESS")

    def test_get_report_document(self):
        """get_report_document 返回文档下载链接"""
        mock_resp = {
            "payload": {
                "reportDocumentId": "DOC-98765",
                "url": "https://amazonaws.com/s3/signed-url",
                "encryptionDetails": {},
                "contentType": "text/xml",
            }
        }
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            result = self.amazon.get_report_document("DOC-98765")
            self.assertIn("url", result)
            self.assertEqual(result["reportDocumentId"], "DOC-98765")

    # ── Feed ─────────────────────────────────────────────
    def test_submit_feed_success(self):
        """submit_feed 成功返回 feed_id"""
        mock_resp = {
            "payload": {
                "feedId": "FEED-55555",
                "status": "IN_PROGRESS",
                "feedType": "POST_PRODUCT_DATA",
            }
        }
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            xml_content = '<?xml version="1.0"?><AmazonEnvelope></AmazonEnvelope>'
            result = self.amazon.submit_feed(
                feed_type="POST_PRODUCT_DATA",
                content=xml_content,
                content_type="text/xml",
            )
            self.assertTrue(result["success"])
            self.assertEqual(result["feed_id"], "FEED-55555")

    # ── 回滚 ─────────────────────────────────────────────
    def test_rollback_update(self):
        """回滚更新操作 = 恢复到 payload 中的原始值"""
        rollback_calls = []
        def spapi_side_effect(method, path, **kwargs):
            rollback_calls.append((method, path))
            return {"payload": {"status": "SUBMITTED"}}

        with patch.object(self.amazon, "_spapi_request", side_effect=spapi_side_effect):
            record = OperationRecord(
                id="test-rollback-2",
                timestamp=__import__("datetime").datetime.now(),
                operation=OperationType.UPDATE,
                entity_type="listing",
                entity_id=123,
                payload={"sku": "SKU-RB-001", "title": "Old Title", "price_amount": 9.99},
                response={},
                status=OperationStatus.EXECUTED,
            )
            result = self.amazon._do_rollback(record)
            self.assertTrue(result)
            self.assertEqual(record.status, OperationStatus.ROLLED_BACK)

    def test_rollback_create(self):
        """回滚创建操作 = 删除 Listing"""
        rollback_calls = []
        def spapi_side_effect(method, path, **kwargs):
            rollback_calls.append((method, path))
            return {"payload": {"status": "SUBMITTED"}}

        with patch.object(self.amazon, "_spapi_request", side_effect=spapi_side_effect):
            record = OperationRecord(
                id="test-rollback-3",
                timestamp=__import__("datetime").datetime.now(),
                operation=OperationType.CREATE,
                entity_type="listing",
                entity_id=123,
                payload={"sku": "SKU-RB-002"},
                response={},
                status=OperationStatus.EXECUTED,
            )
            result = self.amazon._do_rollback(record)
            self.assertTrue(result)
            # DELETE 操作
            self.assertEqual(rollback_calls[0][0], "DELETE")

    # ── 数据模型转换 ─────────────────────────────────────
    def test_amazon_listing_payload_from_content(self):
        """AmazonListingPayload.from_content_payload 正确转换"""
        content = ContentPayload(title="Amazon Item", content="Description")
        listing = AmazonListingPayload.from_content_payload(
            content,
            sku="SKU-MANUAL",
            product_type="ELECTRONIC_ACCESSORY",
            price_amount=39.99,
            currency="USD",
            quantity=20,
            fulfillment_channel="MFN",
        )
        self.assertEqual(listing.sku, "SKU-MANUAL")
        self.assertEqual(listing.title, "Amazon Item")
        self.assertEqual(listing.price_amount, 39.99)
        self.assertEqual(listing.quantity, 20)
        self.assertEqual(listing.fulfillment_channel, "MFN")

    # ── 异常处理 ─────────────────────────────────────────
    def test_spapi_error_raises(self):
        """HTTP 错误抛出 AmazonSPAPIError"""
        import urllib.error
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = urllib.error.HTTPError(
                "", 400, "Bad Request", {},
                __import__("io").BytesIO(b'{"errors": [{"code": "InvalidInput","message":"bad"}]}')
            )
            with self.assertRaises(AmazonSPAPIError) as ctx:
                self.amazon._spapi_request("GET", "/test", token="tok")
            self.assertEqual(ctx.exception.code, 400)

    # ── 历史持久化 ───────────────────────────────────────
    def test_history_persists_across_instances(self):
        """操作记录正确持久化，重新加载后可见"""
        mock_resp = {"payload": {"status": "SUBMITTED", "summaries": []}}
        with patch.object(self.amazon, "_spapi_request", return_value=mock_resp):
            payload = ContentPayload(title="Persist Amazon", content="Desc")
            self.amazon.create_content(payload)

        # 重新实例化，加载历史
        amazon2 = AmazonConnector(self.cred, storage_path=self.tmp_file.name)
        history = amazon2.get_history()
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[-1]["operation"], "create")
        self.assertEqual(history[-1]["entity_type"], "listing")
        amazon2.close()


# ── 跨连接器测试 ────────────────────────────────────────────────────────────

class TestConnectorIntegration(unittest.TestCase):
    """跨连接器集成测试（验证接口一致性）"""

    def test_shopify_and_amazon_record_structure(self):
        """Shopify 和 Amazon 生成的操作记录结构一致"""
        now = __import__("datetime").datetime.now()

        wp_record = OperationRecord(
            id="rec-001", timestamp=now,
            operation=OperationType.CREATE, entity_type="product",
            entity_id=1, payload={}, response={},
            status=OperationStatus.EXECUTED,
        )
        self.assertEqual(wp_record.operation, OperationType.CREATE)
        self.assertIsInstance(wp_record.to_dict(), dict)

    def test_shopify_connector_extracts_gid(self):
        """ShopifyConnector._extract_id 正确解析 GID"""
        self.assertEqual(ShopifyConnector._extract_id("gid://shopify/Product/9876543"), 9876543)
        self.assertEqual(ShopifyConnector._extract_id("gid://shopify/ProductVariant/555"), 555)
        self.assertEqual(ShopifyConnector._extract_id("invalid"), 0)

    def test_shopify_connector_builds_gid(self):
        """ShopifyConnector._to_gid 正确构造 GID"""
        self.assertEqual(
            ShopifyConnector._to_gid("Product", 123),
            "gid://shopify/Product/123"
        )
        self.assertEqual(
            ShopifyConnector._to_gid("ProductVariant", 456),
            "gid://shopify/ProductVariant/456"
        )

    def test_product_payload_variants_defaults(self):
        """VariantPayload 有合理的默认值"""
        v = VariantPayload()
        self.assertEqual(v.price, "0.00")
        self.assertEqual(v.inventory_policy, "deny")
        self.assertEqual(v.weight_unit, "kg")
        self.assertEqual(v.inventory_quantity, 0)

    def test_amazon_listing_defaults(self):
        """AmazonListingPayload 有合理的默认值"""
        listing = AmazonListingPayload()
        self.assertEqual(listing.price_currency, "USD")
        self.assertEqual(listing.condition_type, "New")
        self.assertEqual(listing.fulfillment_channel, "MFN")
        self.assertEqual(listing.operation_type, "CREATE")

    def test_vendor_extraction_from_url(self):
        """ShopifyConnector._extract_shop_name 从 URL 提取商店名"""
        self.assertEqual(
            ShopifyConnector._extract_shop_name("https://my-store.myshopify.com"),
            "my-store"
        )
        self.assertEqual(
            ShopifyConnector._extract_shop_name("https://shop.example.com"),
            "shop.example.com"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
