"""
事务管理器原子性测试
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from middlewares.transaction_manager import (
    TransactionManager,
    TransactionPrepareError,
)


class TestTransactionManager:
    """TransactionManager 事务测试"""

    def test_stage_create_and_commit(self, tmp_path):
        """基本创建+提交"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("test.txt", "hello")
        tx.commit()

        assert (tmp_path / "test.txt").exists()
        assert (tmp_path / "test.txt").read_text() == "hello"

    def test_stage_create_and_rollback(self, tmp_path):
        """基本创建+回滚"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("test.txt", "hello")
        tx.rollback()

        assert not (tmp_path / "test.txt").exists()

    def test_stage_modify_existing_file(self, tmp_path):
        """修改已有文件"""
        original = tmp_path / "existing.txt"
        original.write_text("original")

        tx = TransactionManager(tmp_path)
        tx.stage_modify("existing.txt", "modified")
        tx.commit()

        assert original.read_text() == "modified"

    def test_stage_modify_rollback_restores(self, tmp_path):
        """修改回滚恢复原内容"""
        original = tmp_path / "existing.txt"
        original.write_text("original")

        tx = TransactionManager(tmp_path)
        tx.stage_modify("existing.txt", "modified")
        tx.rollback()

        assert original.read_text() == "original"

    def test_stage_delete_and_commit(self, tmp_path):
        """删除已有文件"""
        f = tmp_path / "to_delete.txt"
        f.write_text("delete me")

        tx = TransactionManager(tmp_path)
        tx.stage_delete("to_delete.txt")
        tx.commit()

        assert not f.exists()

    def test_stage_delete_rollback_restores(self, tmp_path):
        """删除回滚恢复文件"""
        f = tmp_path / "to_delete.txt"
        f.write_text("delete me")

        tx = TransactionManager(tmp_path)
        tx.stage_delete("to_delete.txt")
        tx.rollback()

        assert f.exists()
        assert f.read_text() == "delete me"

    def test_commit_twice_is_noop(self, tmp_path):
        """重复 commit 无副作用"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("test.txt", "hello")
        tx.commit()
        tx.commit()  # 不应抛异常

    def test_rollback_after_commit_is_noop(self, tmp_path):
        """commit 后 rollback 不应恢复文件"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("test.txt", "hello")
        tx.commit()

        # commit 后 rollback 不应该删除文件
        tx.rollback()
        assert (tmp_path / "test.txt").exists()

    def test_prepare_empty_operations(self, tmp_path):
        """空操作 prepare 应该返回 True"""
        tx = TransactionManager(tmp_path)
        assert tx.prepare()

    def test_prepare_with_valid_staging(self, tmp_path):
        """有有效 staging 文件时 prepare 返回 True"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("test.txt", "hello")
        assert tx.prepare()

    def test_multiple_files_atomic(self, tmp_path):
        """多文件事务：全部成功或全部回滚"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("a.txt", "a")
        tx.stage_create("b.txt", "b")
        tx.stage_create("c.txt", "c")
        tx.commit()

        assert (tmp_path / "a.txt").exists()
        assert (tmp_path / "b.txt").exists()
        assert (tmp_path / "c.txt").exists()

    def test_file_hash_tracking(self, tmp_path):
        """文件哈希追踪"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("test.txt", "hello world")
        h = tx.get_file_hash("test.txt")
        assert h is not None
        assert len(h) == 64  # SHA256

    def test_file_hash_missing(self, tmp_path):
        """不存在的文件返回 None"""
        tx = TransactionManager(tmp_path)
        assert tx.get_file_hash("nonexistent.txt") is None

    def test_staged_files_property(self, tmp_path):
        """staged_files 属性"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("a.txt", "a")
        tx.stage_delete("b.txt")  # delete 不应出现在 staged_files 中
        tx.stage_create("c.txt", "c")

        staged = tx.staged_files
        assert "a.txt" in staged
        assert "c.txt" in staged
        assert "b.txt" not in staged

    def test_idempotent_hash(self, tmp_path):
        """相同内容生成相同哈希"""
        tx1 = TransactionManager(tmp_path / "dir1")
        tx1.stage_create("test.txt", "hello")

        tx2 = TransactionManager(tmp_path / "dir2")
        tx2.stage_create("test.txt", "hello")

        assert tx1.get_file_hash("test.txt") == tx2.get_file_hash("test.txt")

    def test_stage_create_nested_directory(self, tmp_path):
        """嵌套目录创建"""
        tx = TransactionManager(tmp_path)
        tx.stage_create("deep/nested/dir/file.txt", "content")
        tx.commit()

        assert (tmp_path / "deep" / "nested" / "dir" / "file.txt").exists()
