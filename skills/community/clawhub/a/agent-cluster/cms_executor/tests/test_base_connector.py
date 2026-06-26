"""
Tests for Base CMS Connector

Covers:
- CMSCredentials creation and validation
- CMSResource fingerprinting
- CMSOperation idempotency
- CMSResult success/error factories
- is_dangerous_operation detection
- Snapshot and rollback path generation
"""

import pytest
import json
from datetime import datetime, timezone

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cms_executor.connectors.base_connector import (
    BaseCMSConnector,
    CMSCredentials,
    CMSResource,
    CMSOperation,
    CMSPlatform,
    CMSResult,
    CMSResourceType,
    CMSOperationType,
    CMSConnectionStatus,
    RiskLevel,
    is_dangerous_operation,
)


class DummyConnector(BaseCMSConnector):
    """测试用连接器（实现所有抽象方法）"""

    platform = CMSPlatform.CUSTOM

    def __init__(self):
        super().__init__(CMSCredentials(
            platform=CMSPlatform.CUSTOM,
            api_base="https://test.example.com",
            api_key="test_key",
        ))

    async def _do_health_check(self, client):
        return True

    async def _do_read(self, client, resource_id):
        return {"id": resource_id, "title": "Test Resource", "content": "Hello"}

    async def _do_list(self, client, filters, page, per_page):
        return {"items": [{"id": "1"}, {"id": "2"}], "total": 2}

    async def _do_create(self, client, data):
        return {"id": "new_123", **data}

    async def _do_update(self, client, resource_id, data):
        return {"id": resource_id, **data}

    async def _do_delete(self, client, resource_id, soft):
        return {"id": resource_id, "deleted": True, "soft": soft}

    async def _do_upload_media(self, client, file_path, metadata):
        return {"id": "media_123", "url": f"https://cdn.example.com/{file_path}"}

    def _normalize_read_response(self, raw, resource_id):
        return CMSResource(
            resource_id=resource_id,
            resource_type=CMSResourceType.POST,
            platform=self.platform,
            title=raw.get("title", ""),
            content=raw.get("content", ""),
            raw=raw,
        )

    def to_platform_format(self, data, operation):
        return data


# =============================================================================
# Tests: CMSCredentials
# =============================================================================

class TestCMSCredentials:
    def test_from_dict(self):
        creds = CMSCredentials.from_dict({
            "platform": "wordpress",
            "api_base": "https://example.com/wp-json",
            "api_key": "user:app_pass",
        })
        assert creds.platform == CMSPlatform.WORDPRESS
        assert creds.api_base == "https://example.com/wp-json"
        assert "user:app_pass" in creds.api_key

    def test_masked(self):
        creds = CMSCredentials(
            platform=CMSPlatform.SHOPIFY,
            api_base="https://example.myshopify.com",
            api_key="test_token_example",
            oauth_token="shcate_test",
        )
        masked = creds.masked()
        assert masked["platform"] == "shopify"
        assert "shpa***" in masked["api_key"]
        assert "shca***" in masked["oauth_token"]
        assert "***" not in masked["api_base"]


# =============================================================================
# Tests: CMSResource
# =============================================================================

class TestCMSResource:
    def test_fingerprint(self):
        r1 = CMSResource(
            resource_id="123",
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.WORDPRESS,
            title="Hello World",
            content="This is content",
            status="draft",
        )
        r2 = CMSResource(
            resource_id="123",
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.WORDPRESS,
            title="Hello World",
            content="This is content",
            status="draft",
        )
        r3 = CMSResource(
            resource_id="123",
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.WORDPRESS,
            title="Hello World",
            content="Different content",
            status="draft",
        )
        assert r1.fingerprint() == r2.fingerprint()
        assert r1.fingerprint() != r3.fingerprint()

    def test_to_dict(self):
        r = CMSResource(
            resource_id="test_123",
            resource_type=CMSResourceType.PRODUCT,
            platform=CMSPlatform.SHOPIFY,
            title="Test Product",
            content="<p>Description</p>",
            status="active",
            tags=["tag1", "tag2"],
        )
        d = r.to_dict()
        assert d["resource_id"] == "test_123"
        assert d["resource_type"] == "product"
        assert d["platform"] == "shopify"
        assert d["title"] == "Test Product"
        assert d["tags"] == ["tag1", "tag2"]


# =============================================================================
# Tests: CMSOperation
# =============================================================================

class TestCMSOperation:
    def test_auto_idempotency_key(self):
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.WORDPRESS,
            resource_id="posts/123",
            data={"title": "New Title", "slug": "hello"},
        )
        assert op.idempotency_key == "update:post:posts/123:hello"
        assert op.operation_id  # auto-generated

    def test_explicit_idempotency_key(self):
        op = CMSOperation(
            operation_type=CMSOperationType.CREATE,
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.WORDPRESS,
            data={"title": "New Post"},
            idempotency_key="create:post:my-unique-key",
        )
        assert op.idempotency_key == "create:post:my-unique-key"

    def test_to_dict(self):
        op = CMSOperation(
            operation_type=CMSOperationType.CREATE,
            resource_type=CMSResourceType.PRODUCT,
            platform=CMSPlatform.MAGENTO,
            agent_id="agent_01",
            risk_level=RiskLevel.MEDIUM,
        )
        d = op.to_dict()
        assert d["operation_type"] == "create"
        assert d["platform"] == "magento"
        assert d["agent_id"] == "agent_01"
        assert d["risk_level"] == "medium"


# =============================================================================
# Tests: CMSResult
# =============================================================================

class TestCMSResult:
    def test_ok_factory(self):
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.WORDPRESS,
            resource_id="posts/1",
        )
        result = CMSResult.ok(op, resource_id="posts/1", data={"title": "Updated"})
        assert result.success is True
        assert result.resource_id == "posts/1"
        assert result.rollback_available is True  # UPDATE is rollbackable

    def test_error_factory(self):
        op = CMSOperation(
            operation_type=CMSOperationType.DELETE,
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.WORDPRESS,
            resource_id="posts/1",
        )
        result = CMSResult.error(op, "Not found", error_code="NOT_FOUND")
        assert result.success is False
        assert result.error_code == "NOT_FOUND"
        assert "Not found" in result.message


# =============================================================================
# Tests: Danger Detection
# =============================================================================

class TestDangerDetection:
    def test_dangerous_drop_table(self):
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            platform=CMSPlatform.CUSTOM,
            resource_id="db/table",
            data={"sql": "DROP TABLE users"},
        )
        dangerous, reason = is_dangerous_operation(op)
        assert dangerous is True
        assert "DROP TABLE" in reason

    def test_dangerous_price_zero(self):
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            platform=CMSPlatform.SHOPIFY,
            resource_id="gid://shopify/ProductVariant/1",
            data={"price": 0.00},
        )
        dangerous, _ = is_dangerous_operation(op)
        assert dangerous is True

    def test_safe_operation(self):
        op = CMSOperation(
            operation_type=CMSOperationType.UPDATE,
            platform=CMSPlatform.WORDPRESS,
            resource_id="posts/123",
            data={"title": "New Title", "status": "publish"},
        )
        dangerous, _ = is_dangerous_operation(op)
        assert dangerous is False


# =============================================================================
# Tests: BaseConnector abstract interface
# =============================================================================

class TestBaseConnectorInterface:
    @pytest.mark.asyncio
    async def test_connect_and_disconnect(self):
        connector = DummyConnector()
        assert connector.status == CMSConnectionStatus.DISCONNECTED
        ok = await connector.connect()
        assert ok is True
        assert connector.status == CMSConnectionStatus.CONNECTED
        await connector.disconnect()
        assert connector.status == CMSConnectionStatus.DISCONNECTED

    @pytest.mark.asyncio
    async def test_read(self):
        connector = DummyConnector()
        await connector.connect()
        result = await connector.read("posts/123")
        assert result.success is True
        assert result.resource_id == "posts/123"
        await connector.disconnect()

    @pytest.mark.asyncio
    async def test_list(self):
        connector = DummyConnector()
        await connector.connect()
        result = await connector.list(filters={"status": "publish"}, page=1, per_page=10)
        assert result.success is True
        assert len(result.data.get("items", [])) == 2
        await connector.disconnect()

    @pytest.mark.asyncio
    async def test_create_with_idempotency(self):
        connector = DummyConnector()
        await connector.connect()
        op = CMSOperation(
            operation_type=CMSOperationType.CREATE,
            resource_type=CMSResourceType.POST,
            platform=CMSPlatform.CUSTOM,
            data={"title": "New Post"},
            idempotency_key="test_idempotency_key",
        )
        # First create
        result1 = await connector.create(op.data, op.resource_type)
        assert result1.success is True
        await connector.disconnect()

    @pytest.mark.asyncio
    async def test_snapshot_and_rollback_path(self):
        connector = DummyConnector()
        await connector.connect()
        snapshot_id = await connector.snapshot("posts/123")
        assert snapshot_id.startswith("custom_posts/123_")
        # Snapshot file created - check in snapshots/{platform}/{date}/
        import os, tempfile
        # Find the snapshot - it should be in snapshots/custom/...
        found = False
        for root, dirs, files in os.walk("snapshots"):
            for fname in files:
                if fname.endswith(".json") and "custom_posts" in fname:
                    found = True
                    break
        assert found, "Snapshot file should be created in snapshots/ directory"
        await connector.disconnect()

    @pytest.mark.asyncio
    async def test_delete_soft_default(self):
        connector = DummyConnector()
        await connector.connect()
        result = await connector.delete("posts/123")
        assert result.success is True
        assert result.snapshot_id  # snapshot created
        assert result.rollback_available is True
        await connector.disconnect()
