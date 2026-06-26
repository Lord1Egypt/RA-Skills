"""
Tests for Platform Connectors

Covers:
- WordPressConnector: REST API format conversion, SEO metadata
- ShopifyConnector: GraphQL format, inventory/pricing updates
- AmazonConnector: SP-API format
- MagentoConnector: REST format, inventory updates
"""

import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cms_executor.connectors.base_connector import (
    CMSCredentials, CMSResourceType, CMSOperationType,
    CMSOperation, CMSResource, RiskLevel,
)
from cms_executor.connectors.wordpress_connector import WordPressConnector
from cms_executor.connectors.shopify_connector import ShopifyConnector
from cms_executor.connectors.amazon_connector import AmazonConnector
from cms_executor.connectors.magento_connector import MagentoConnector
from cms_executor.connectors import CMSPlatform


# =============================================================================
# Tests: WordPress Connector
# =============================================================================

class TestWordPressConnector:
    def test_init(self):
        creds = CMSCredentials(
            platform=CMSPlatform.WORDPRESS,
            api_base="https://example.com/wp-json",
            api_key="user:app_password",
        )
        conn = WordPressConnector(creds)
        assert conn.platform == CMSPlatform.WORDPRESS
        assert "create_post" in conn.capabilities
        assert "update_seo" in conn.capabilities

    def test_to_platform_format(self):
        creds = CMSCredentials(platform=CMSPlatform.WORDPRESS, api_base="https://example.com/wp-json", api_key="test")
        conn = WordPressConnector(creds)
        data = {
            "title": "SEO Title",
            "content": "<p>Hello world</p>",
            "slug": "hello-world",
            "status": "publish",
            "seo_title": "Optimized SEO Title",
            "seo_description": "Meta description",
        }
        wp_data = conn.to_platform_format(data, "create")
        assert wp_data["title"] == "SEO Title"
        assert wp_data["slug"] == "hello-world"
        assert wp_data["status"] == "publish"
        assert "_yoast_wpseo_title" in wp_data
        assert "_yoast_wpseo_metadesc" in wp_data

    def test_normalize_read_response(self):
        creds = CMSCredentials(platform=CMSPlatform.WORDPRESS, api_base="https://example.com/wp-json", api_key="test")
        conn = WordPressConnector(creds)
        raw = {
            "id": 123,
            "type": "post",
            "title": {"rendered": "Hello World"},
            "content": {"rendered": "<p>Content here</p>"},
            "slug": "hello-world",
            "status": "publish",
            "date": "2024-01-01T00:00:00",
            "modified": "2024-01-02T00:00:00",
            "link": "https://example.com/hello-world",
            "categories": [1, 2],
            "tags": [10, 11],
            "author": 1,
            "_yoast_wpseo_title": "SEO Title",
            "_yoast_wpseo_metadesc": "Meta description",
        }
        resource = conn._normalize_read_response(raw, "posts/123")
        assert resource.resource_id == "posts/123"
        assert resource.title == "Hello World"
        assert resource.content == "<p>Content here</p>"
        assert resource.slug == "hello-world"
        assert resource.seo_title == "SEO Title"
        assert resource.seo_description == "Meta description"
        assert resource.categories == ["1", "2"]
        assert resource.tags == ["10", "11"]
        assert resource.resource_type == CMSResourceType.POST

    @pytest.mark.asyncio
    async def test_health_check_success(self):
        creds = CMSCredentials(platform=CMSPlatform.WORDPRESS, api_base="https://example.com/wp-json", api_key="test")
        conn = WordPressConnector(creds)
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.get = AsyncMock(return_value=mock_response)
        ok = await conn._do_health_check(mock_client)
        assert ok is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        creds = CMSCredentials(platform=CMSPlatform.WORDPRESS, api_base="https://example.com/wp-json", api_key="test")
        conn = WordPressConnector(creds)
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=Exception("Network error"))
        ok = await conn._do_health_check(mock_client)
        assert ok is False

    @pytest.mark.asyncio
    async def test_read_post(self):
        creds = CMSCredentials(platform=CMSPlatform.WORDPRESS, api_base="https://example.com/wp-json", api_key="test")
        conn = WordPressConnector(creds)
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 123, "title": {"rendered": "Test"}}
        mock_client.get = AsyncMock(return_value=mock_response)
        result = await conn._do_read(mock_client, "posts/123")
        assert result["id"] == 123

    @pytest.mark.asyncio
    async def test_delete_soft(self):
        creds = CMSCredentials(platform=CMSPlatform.WORDPRESS, api_base="https://example.com/wp-json", api_key="test")
        conn = WordPressConnector(creds)
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 123, "deleted": True}
        mock_client.delete = AsyncMock(return_value=mock_response)
        result = await conn._do_delete(mock_client, "posts/123", soft=True)
        assert result["deleted"] is True


# =============================================================================
# Tests: Shopify Connector
# =============================================================================

class TestShopifyConnector:
    def test_init(self):
        creds = CMSCredentials(
            platform=CMSPlatform.SHOPIFY,
            api_base="https://example.myshopify.com/admin/api/2024-01",
            oauth_token="<TEST_TOKEN>",
        )
        conn = ShopifyConnector(creds)
        assert conn.platform == CMSPlatform.SHOPIFY
        assert "update_inventory" in conn.capabilities

    def test_to_platform_format(self):
        creds = CMSCredentials(platform=CMSPlatform.SHOPIFY, api_base="https://example.myshopify.com", oauth_token="test")
        conn = ShopifyConnector(creds)
        data = {
            "title": "New Product",
            "descriptionHtml": "<p>Description</p>",
            "handle": "new-product",
            "status": "active",
            "vendor": "Acme",
            "product_type": "Electronics",
            "tags": ["tag1", "tag2"],
            "seo_title": "SEO Title",
            "seo_description": "SEO Description",
        }
        shopify_data = conn.to_platform_format(data, "create")
        assert shopify_data["title"] == "New Product"
        assert shopify_data["handle"] == "new-product"
        assert shopify_data["status"] == "ACTIVE"
        assert shopify_data["vendor"] == "Acme"
        assert shopify_data["seo"]["title"] == "SEO Title"

    def test_normalize_product_response(self):
        creds = CMSCredentials(platform=CMSPlatform.SHOPIFY, api_base="https://example.myshopify.com", oauth_token="test")
        conn = ShopifyConnector(creds)
        raw = {
            "id": "gid://shopify/Product/123",
            "title": "Test Product",
            "descriptionHtml": "<p>Great product</p>",
            "handle": "test-product",
            "status": "ACTIVE",
            "vendor": "Acme Corp",
            "productType": "Electronics",
            "tags": ["sale", "featured"],
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-02T00:00:00Z",
            "variants": {
                "edges": [
                    {"node": {"id": "v1", "price": "29.99", "inventoryQuantity": 100}}
                ]
            },
            "images": {"edges": [{"node": {"url": "https://cdn.example.com/img.jpg"}}]},
            "seo": {"title": "SEO", "description": "SEO desc"},
        }
        resource = conn._normalize_read_response(raw, "gid://shopify/Product/123")
        assert resource.title == "Test Product"
        assert resource.status == "active"
        assert resource.tags == ["sale", "featured"]
        assert resource.metadata["price"] == "29.99"
        assert resource.metadata["inventory_quantity"] == 100
        assert resource.seo_title == "SEO"

    def test_resource_id_gid_parsing(self):
        creds = CMSCredentials(platform=CMSPlatform.SHOPIFY, api_base="https://example.myshopify.com", oauth_token="test")
        conn = ShopifyConnector(creds)
        raw = {"title": "Test"}
        resource = conn._normalize_read_response(raw, "gid://shopify/Product/123")
        assert resource.resource_type == CMSResourceType.PRODUCT


# =============================================================================
# Tests: Amazon Connector
# =============================================================================

class TestAmazonConnector:
    def test_init(self):
        creds = CMSCredentials(
            platform=CMSPlatform.AMAZON,
            api_base="https://sellingpartnerapi-na.amazon.com",
            api_key="amzn_client_id",
            oauth_token="atzr|...",
            aws_secret_key="secret",
            aws_region="us-east-1",
        )
        conn = AmazonConnector(creds)
        assert conn.platform == CMSPlatform.AMAZON
        assert "update_pricing" in conn.capabilities
        assert "update_inventory" in conn.capabilities

    def test_to_platform_format(self):
        creds = CMSCredentials(platform=CMSPlatform.AMAZON, api_base="https://sellingpartnerapi-na.amazon.com", api_key="test")
        conn = AmazonConnector(creds)
        data = {
            "title": "Product Title",
            "price": 29.99,
            "quantity": 100,
            "currency": "USD",
            "seo_title": "SEO Keyword Title",
            "seo_description": "SEO keyword description",
        }
        amazon_data = conn.to_platform_format(data, "update")
        assert "item_name" in amazon_data
        assert amazon_data["item_name"][0]["value"] == "Product Title"
        assert amazon_data["list_price"][0]["value"] == 29.99
        assert amazon_data["fulfillment_availability"][0]["value"] == "100"

    def test_normalize_catalog_response(self):
        creds = CMSCredentials(platform=CMSPlatform.AMAZON, api_base="https://sellingpartnerapi-na.amazon.com", api_key="test")
        conn = AmazonConnector(creds)
        raw = {
            "asin": "B0ABC12345",
            "summaries": [
                {"brand": "Acme", "product_type": "Electronics", "item_name": "Great Product", "status": "ACTIVE"}
            ],
            "attributes": {
                "item_name": [{"value": "Great Product", "language": "en_US"}]
            },
        }
        resource = conn._normalize_read_response(raw, "catalog/B0ABC12345")
        assert resource.resource_id == "catalog/B0ABC12345"
        assert resource.metadata["asin"] == "B0ABC12345"
        assert resource.metadata["brand"] == "Acme"


# =============================================================================
# Tests: Magento Connector
# =============================================================================

class TestMagentoConnector:
    def test_init(self):
        creds = CMSCredentials(
            platform=CMSPlatform.MAGENTO,
            api_base="https://example.com/rest/V1",
            oauth_token="abc123token",
            extra_headers={"store_id": 1, "website_id": 1},
        )
        conn = MagentoConnector(creds)
        assert conn.platform == CMSPlatform.MAGENTO
        assert conn._store_id == 1
        assert "update_inventory" in conn.capabilities

    def test_to_platform_format(self):
        creds = CMSCredentials(platform=CMSPlatform.MAGENTO, api_base="https://example.com/rest/V1", oauth_token="test")
        conn = MagentoConnector(creds)
        data = {
            "_domain": "products",
            "title": "Product Name",
            "description": "Product description",
            "price": 49.99,
            "quantity": 50,
            "status": "active",
            "seo_title": "SEO Title",
            "seo_description": "SEO Description",
        }
        magento_data = conn.to_platform_format(data, "update")
        assert magento_data["name"] == "Product Name"
        assert magento_data["price"] == 49.99
        assert magento_data["status"] == 1
        assert "extension_attributes" in magento_data
        assert magento_data["extension_attributes"]["stock_item"]["qty"] == 50
        assert any(a["attribute_code"] == "meta_title" for a in magento_data.get("custom_attributes", []))

    def test_normalize_product(self):
        creds = CMSCredentials(platform=CMSPlatform.MAGENTO, api_base="https://example.com/rest/V1", oauth_token="test")
        conn = MagentoConnector(creds)
        raw = {
            "id": 100,
            "name": "Test Product",
            "sku": "TEST-SKU-001",
            "price": 99.99,
            "status": 1,
            "visibility": 4,
            "type_id": "simple",
            "created_at": "2024-01-01 00:00:00",
            "updated_at": "2024-01-02 00:00:00",
            "custom_attributes": [
                {"attribute_code": "meta_title", "value": "SEO Title"},
                {"attribute_code": "meta_description", "value": "SEO Desc"},
            ],
            "extension_attributes": {
                "stock_item": {"qty": 200, "is_in_stock": True},
            },
        }
        resource = conn._normalize_read_response(raw, "products/TEST-SKU-001")
        assert resource.resource_id == "products/TEST-SKU-001"
        assert resource.title == "Test Product"
        assert resource.metadata["sku"] == "TEST-SKU-001"
        assert resource.metadata["inventory"] == 200
        assert resource.metadata["is_in_stock"] is True
        assert resource.seo_title == "SEO Title"

    def test_normalize_category(self):
        creds = CMSCredentials(platform=CMSPlatform.MAGENTO, api_base="https://example.com/rest/V1", oauth_token="test")
        conn = MagentoConnector(creds)
        raw = {
            "id": 5,
            "name": "Electronics",
            "parent_id": 2,
            "path": "1/2/5",
            "position": 1,
            "is_active": True,
        }
        resource = conn._normalize_read_response(raw, "categories/5")
        assert resource.title == "Electronics"
        assert resource.metadata["parent_id"] == 2
        assert resource.metadata["path"] == "1/2/5"
        assert resource.status == "active"
