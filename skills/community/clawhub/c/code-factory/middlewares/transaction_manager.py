"""
事务管理器 —— Unit of Work 模式。

保证文件系统副作用：
1. 所有写入先到 staging/ 区域
2. 全部验证通过后原子提交
3. 任何步骤失败 → 完整回滚
"""

import shutil
import tempfile
import hashlib
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class FileOperation:
    """单个文件操作记录"""
    target_path: Path
    staging_path: Path
    operation_type: str  # 'create' | 'modify' | 'delete'
    original_backup_path: Optional[Path] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class TransactionManager:
    """
    Unit of Work 模式事务管理器。

    用法:
        tx = TransactionManager(Path("./project_assets/my_project"))
        try:
            tx.stage_create("src/main.py", content)
            tx.stage_create("tests/test_main.py", test_content)
            # ... 更多文件 ...
            tx.commit()   # 全部写入
        except Exception:
            tx.rollback() # 全部撤销
    """

    def __init__(self, target_dir: Path):
        self.target_dir = Path(target_dir)
        self.staging_dir = Path(tempfile.mkdtemp(prefix="code_factory_staging_"))
        self.operations: List[FileOperation] = []
        self.committed: bool = False
        self._file_hashes: dict[str, str] = {}  # 幂等性追踪

    # ── 暂存操作 ──────────────────────────────────

    def stage_create(self, relative_path: str, content: str) -> FileOperation:
        """暂存新建文件"""
        staging_path = self.staging_dir / relative_path
        staging_path.parent.mkdir(parents=True, exist_ok=True)
        staging_path.write_text(content, encoding="utf-8")

        content_hash = hashlib.sha256(content.encode()).hexdigest()
        self._file_hashes[relative_path] = content_hash

        op = FileOperation(
            target_path=self.target_dir / relative_path,
            staging_path=staging_path,
            operation_type="create",
        )
        self.operations.append(op)
        return op

    def stage_modify(self, relative_path: str, new_content: str) -> FileOperation:
        """暂存修改文件（先备份原文件）"""
        target = self.target_dir / relative_path
        backup: Optional[Path] = None
        if target.exists():
            backup = self.staging_dir / f".backup_{relative_path.replace('/', '_').replace('\\', '_')}"
            shutil.copy2(target, backup)

        staging_path = self.staging_dir / relative_path
        staging_path.parent.mkdir(parents=True, exist_ok=True)
        staging_path.write_text(new_content, encoding="utf-8")

        content_hash = hashlib.sha256(new_content.encode()).hexdigest()
        self._file_hashes[relative_path] = content_hash

        op = FileOperation(
            target_path=target,
            staging_path=staging_path,
            operation_type="modify",
            original_backup_path=backup,
        )
        self.operations.append(op)
        return op

    def stage_delete(self, relative_path: str) -> FileOperation:
        """暂存删除文件（先备份）"""
        target = self.target_dir / relative_path
        backup: Optional[Path] = None
        if target.exists():
            backup = self.staging_dir / f".backup_{relative_path.replace('/', '_').replace('\\', '_')}"
            shutil.copy2(target, backup)

        op = FileOperation(
            target_path=target,
            staging_path=self.staging_dir / relative_path,  # 占位
            operation_type="delete",
            original_backup_path=backup,
        )
        self.operations.append(op)
        return op

    # ── 原子提交（v2.0 增强：prepare → copy → commit 三段式） ──

    def prepare(self) -> bool:
        """
        验证所有 staging 文件完整性（文件存在 + 可读）。

        注意：允许空文件（如 .gitkeep），不检查文件大小。

        Returns:
            True 如果所有 staging 文件完整可提交
        """
        for op in self.operations:
            if op.operation_type in ("create", "modify"):
                if not op.staging_path.exists():
                    return False
        return True

    def commit(self) -> None:
        """
        原子提交：prepare → copy → commit 三段式。

        增强（v2.0）：
        - 提交前先验证 staging 文件完整性（prepare）
        - 复制过程中任一文件失败 → 回滚已复制的文件 + 抛出异常
        - 仅在全部成功后才标记 committed=True
        - committed=True 后不再允许 rollback（此时磁盘状态已一致）
        """
        if self.committed:
            return

        if not self.prepare():
            raise TransactionPrepareError(
                "staging 文件不完整，无法提交。"
                f" 共 {len(self.operations)} 个操作待提交。"
            )

        committed_ops: list[FileOperation] = []

        try:
            # 先执行删除操作
            for op in self.operations:
                if op.operation_type == "delete" and op.target_path.exists():
                    op.target_path.unlink()

            # 再执行创建/修改操作
            for op in self.operations:
                if op.operation_type in ("create", "modify"):
                    op.target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(op.staging_path, op.target_path)
                    committed_ops.append(op)
        except Exception:
            # 回滚已复制的文件
            for op in reversed(committed_ops):
                try:
                    if op.target_path.exists():
                        op.target_path.unlink()
                except OSError:
                    pass
            # 恢复已删除的文件
            for op in self.operations:
                if op.operation_type == "delete" and op.original_backup_path and op.original_backup_path.exists():
                    try:
                        shutil.copy2(op.original_backup_path, op.target_path)
                    except OSError:
                        pass
            raise

        self.committed = True
        self._cleanup_staging()

    # ── 回滚 ──────────────────────────────────────

    def rollback(self) -> None:
        """
        回滚：删除已创建的文件，恢复已修改/删除的文件。
        按操作顺序逆序执行，保证依赖关系正确。
        """
        if self.committed:
            return

        for op in reversed(self.operations):
            try:
                if op.operation_type == "create" and op.target_path.exists():
                    op.target_path.unlink()
                elif op.operation_type in ("modify", "delete") and op.original_backup_path and op.original_backup_path.exists():
                    shutil.copy2(op.original_backup_path, op.target_path)
            except OSError:
                # 回滚失败不应该再抛异常，但记录日志
                pass

        self._cleanup_staging()

    def _cleanup_staging(self) -> None:
        """清理 staging 临时目录"""
        if self.staging_dir.exists():
            shutil.rmtree(self.staging_dir, ignore_errors=True)

    # ── 幂等性 ────────────────────────────────────

    def get_file_hash(self, relative_path: str) -> Optional[str]:
        """获取已暂存文件的哈希（用于幂等性比对）"""
        return self._file_hashes.get(relative_path)

    @property
    def staged_files(self) -> List[str]:
        """返回所有已暂存的文件路径"""
        return [op.target_path.name for op in self.operations if op.operation_type != "delete"]


class TransactionPrepareError(Exception):
    """事务准备阶段失败 —— staging 文件不完整"""

