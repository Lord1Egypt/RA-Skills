"""
Tests for Rollback Manager

Covers:
- SnapshotStore save/load
- Fingerprint computation
- Snapshot listing and filtering
- Rollback success and failure
- Version comparison
- Auto cleanup
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cms_executor.connectors.base_connector import CMSPlatform, CMSResourceType, CMSOperationType
from cms_executor.engine.rollback import (
    RollbackManager, SnapshotStore, Snapshot,
    RollbackResult, RollbackStatus,
)


# =============================================================================
# Tests: SnapshotStore
# =============================================================================

class TestSnapshotStore:
    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.store = SnapshotStore(base_dir=self.tmpdir, retention_days=30)

    def teardown_method(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @pytest.mark.asyncio
    async def test_save_and_load(self):
        snapshot = Snapshot(
            snapshot_id="test_wp_posts_1",
            resource_id="posts/1",
            platform=CMSPlatform.WORDPRESS,
            resource_type="post",
            operation_type="update",
            fingerprint="abc123",
            file_path=Path(self.tmpdir),
            created_at=datetime.now(timezone.utc).isoformat(),
            agent_id="agent_01",
            execution_id="exec_01",
            metadata={"resource_data": {"title": "Hello", "content": "World"}},
        )
        path = await self.store.save(snapshot)
        assert path.exists()
        loaded = await self.store.load("test_wp_posts_1")
        assert loaded is not None
        assert loaded.resource_id == "posts/1"
        assert loaded.fingerprint == "abc123"

    @pytest.mark.asyncio
    async def test_load_data(self):
        snapshot = Snapshot(
            snapshot_id="test_wp_posts_2",
            resource_id="posts/2",
            platform=CMSPlatform.WORDPRESS,
            resource_type="post",
            operation_type="update",
            fingerprint="xyz789",
            file_path=Path(self.tmpdir),
            created_at=datetime.now(timezone.utc).isoformat(),
            metadata={"resource_data": {"title": "Updated Title", "content": "Updated content"}},
        )
        await self.store.save(snapshot)
        data = await self.store.load_data("test_wp_posts_2")
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"

    def test_fingerprint_consistency(self):
        data = {"title": "Same", "content": "Same"}
        fp1 = self.store.compute_fingerprint(data)
        fp2 = self.store.compute_fingerprint(data)
        assert fp1 == fp2
        # Different data = different fingerprint
        fp3 = self.store.compute_fingerprint({"title": "Different"})
        assert fp1 != fp3

    def test_list_filter_by_platform(self):
        # Add snapshots for different platforms
        self.store._index["snap_wp"] = Snapshot(
            snapshot_id="snap_wp", resource_id="r1",
            platform=CMSPlatform.WORDPRESS, resource_type="post",
            operation_type="update", fingerprint="f1",
            file_path=Path(self.tmpdir), created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.store._index["snap_sh"] = Snapshot(
            snapshot_id="snap_sh", resource_id="r2",
            platform=CMSPlatform.SHOPIFY, resource_type="product",
            operation_type="update", fingerprint="f2",
            file_path=Path(self.tmpdir), created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.store._index["snap_am"] = Snapshot(
            snapshot_id="snap_am", resource_id="r3",
            platform=CMSPlatform.AMAZON, resource_type="product",
            operation_type="update", fingerprint="f3",
            file_path=Path(self.tmpdir), created_at=datetime.now(timezone.utc).isoformat(),
        )
        wp_list = self.store.list(platform=CMSPlatform.WORDPRESS)
        assert len(wp_list) == 1
        assert wp_list[0].snapshot_id == "snap_wp"

    def test_list_filter_by_resource_id(self):
        self.store._index["snap1"] = Snapshot(
            snapshot_id="snap1", resource_id="posts/100",
            platform=CMSPlatform.WORDPRESS, resource_type="post",
            operation_type="update", fingerprint="f1",
            file_path=Path(self.tmpdir), created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.store._index["snap2"] = Snapshot(
            snapshot_id="snap2", resource_id="posts/200",
            platform=CMSPlatform.WORDPRESS, resource_type="post",
            operation_type="update", fingerprint="f2",
            file_path=Path(self.tmpdir), created_at=datetime.now(timezone.utc).isoformat(),
        )
        results = self.store.list(resource_id="posts/100")
        assert len(results) == 1
        assert results[0].resource_id == "posts/100"


# =============================================================================
# Tests: RollbackManager
# =============================================================================

class TestRollbackManager:
    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.store = SnapshotStore(base_dir=self.tmpdir)
        self.manager = RollbackManager(self.store)

    def teardown_method(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @pytest.mark.asyncio
    async def test_create_snapshot(self):
        snapshot_id = await self.manager.create_snapshot(
            resource_id="posts/123",
            platform=CMSPlatform.WORDPRESS,
            resource_data={"title": "Original Title", "content": "Original Content"},
            agent_id="agent_01",
            execution_id="exec_01",
            operation_type="update",
        )
        assert snapshot_id.startswith("wordpress_posts/123_")
        loaded = await self.store.load(snapshot_id)
        assert loaded is not None
        assert loaded.agent_id == "agent_01"

    @pytest.mark.asyncio
    async def test_rollback_not_found(self):
        result = await self.manager.rollback("non_existent_snapshot_id")
        assert result.status == RollbackStatus.NOT_FOUND
        assert result.duration_ms < 1000  # Should be fast

    @pytest.mark.asyncio
    async def test_rollback_no_connector(self):
        # Create a snapshot first
        snapshot_id = await self.manager.create_snapshot(
            resource_id="posts/123",
            platform=CMSPlatform.WORDPRESS,
            resource_data={"title": "Old Title"},
            operation_type="update",
        )
        # Rollback without connector should fail gracefully
        result = await self.manager.rollback(snapshot_id, connector=None)
        assert result.status == RollbackStatus.FAILED

    @pytest.mark.asyncio
    async def test_compare_versions(self):
        # Create two snapshots with different data
        id1 = await self.manager.create_snapshot(
            resource_id="posts/1",
            platform=CMSPlatform.WORDPRESS,
            resource_data={"title": "Version A", "content": "Content A", "status": "draft"},
            operation_type="update",
        )
        id2 = await self.manager.create_snapshot(
            resource_id="posts/1",
            platform=CMSPlatform.WORDPRESS,
            resource_data={"title": "Version B", "content": "Content B", "status": "published"},
            operation_type="update",
        )
        diff = await self.manager.compare_versions(id1, id2)
        assert "diff" in diff
        assert "added" in diff["diff"]
        assert "removed" in diff["diff"]
        assert "modified" in diff["diff"]
        assert "title" in diff["diff"]["modified"]

    def test_get_history(self):
        result1 = RollbackResult(
            rollback_id="rb1", snapshot_id="snap1",
            status=RollbackStatus.SUCCESS, message="OK",
            duration_ms=100,
        )
        result2 = RollbackResult(
            rollback_id="rb2", snapshot_id="snap2",
            status=RollbackStatus.FAILED, message="Not found",
            duration_ms=50,
        )
        self.manager._rollback_history.append(result1)
        self.manager._rollback_history.append(result2)
        history = self.manager.get_history()
        assert len(history) == 2
        assert history[0].rollback_id == "rb1"


# =============================================================================
# Tests: RollbackResult
# =============================================================================

class TestRollbackResult:
    def test_to_dict(self):
        result = RollbackResult(
            rollback_id="rb_test_123",
            snapshot_id="snap_123",
            status=RollbackStatus.SUCCESS,
            message="Rollback successful",
            duration_ms=450.5,
            resource_id="posts/123",
            platform=CMSPlatform.WORDPRESS,
            verification_passed=True,
        )
        d = result.to_dict()
        assert d["rollback_id"] == "rb_test_123"
        assert d["status"] == "success"
        assert d["duration_ms"] == 450.5
        assert d["verification_passed"] is True
