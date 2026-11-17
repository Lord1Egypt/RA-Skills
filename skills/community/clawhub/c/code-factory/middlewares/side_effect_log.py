"""
副作用追踪器 —— 记录所有文件/系统操作，支持审计与幂等性检测。

职责：
1. 审计：谁在什么时候执行了什么操作
2. 回滚辅助：知道需要撤销哪些操作
3. 幂等性检测：同一输入重复执行是否产生相同副作用序列
"""

import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class SideEffectType(str, Enum):
    FILE_CREATE = "file_create"
    FILE_MODIFY = "file_modify"
    FILE_DELETE = "file_delete"
    CMD_EXEC = "cmd_exec"
    API_CALL = "api_call"


@dataclass
class SideEffectRecord:
    """单条副作用记录"""
    operation: SideEffectType
    target: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    before_hash: Optional[str] = None
    after_hash: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class SideEffectTracker:
    """
    副作用追踪器。

    用法:
        tracker = SideEffectTracker()
        tracker.record(SideEffectType.FILE_CREATE, "src/main.py",
                        after_state=content)
        # ... 更多操作 ...
        tracker.verify_idempotent(previous_run)  # 检查幂等性
    """

    def __init__(self):
        self.log: List[SideEffectRecord] = []

    def record(
        self,
        operation: SideEffectType,
        target: str,
        before_state: str = "",
        after_state: str = "",
        **metadata,
    ) -> SideEffectRecord:
        """记录一次副作用操作"""
        rec = SideEffectRecord(
            operation=operation,
            target=target,
            before_hash=self._hash(before_state) if before_state else None,
            after_hash=self._hash(after_state) if after_state else None,
            metadata=metadata,
        )
        self.log.append(rec)
        return rec

    def is_idempotent(self, previous_log: List[SideEffectRecord]) -> bool:
        """
        对比两次执行的副作用日志，判断是否幂等。
        比较操作序列：操作类型 + 目标 + 内容哈希
        """
        if len(self.log) != len(previous_log):
            return False
        for current, previous in zip(self.log, previous_log):
            if current.operation != previous.operation:
                return False
            if current.target != previous.target:
                return False
            if current.after_hash != previous.after_hash:
                return False
        return True

    def get_operations_by_type(self, op_type: SideEffectType) -> List[SideEffectRecord]:
        """按操作类型过滤"""
        return [r for r in self.log if r.operation == op_type]

    def get_modified_files(self) -> List[str]:
        """获取所有被修改的文件列表"""
        return [r.target for r in self.log if r.operation in (
            SideEffectType.FILE_CREATE,
            SideEffectType.FILE_MODIFY,
            SideEffectType.FILE_DELETE,
        )]

    def get_created_files(self) -> List[str]:
        """获取所有被创建的文件列表（用于 Saga 补偿）"""
        return [r.target for r in self.log if r.operation == SideEffectType.FILE_CREATE]

    def get_compensation_plan(self) -> List[Dict]:
        """
        生成补偿计划：逆序列出需要回滚的操作。

        返回格式：
        [
            {"action": "delete", "target": "src/main.py"},
            {"action": "delete", "target": "tests/test_main.py"},
            ...
        ]
        逆序排列，保证依赖关系正确（先创建的文件后删除）。
        """
        plan = []
        for r in reversed(self.log):
            if r.operation == SideEffectType.FILE_CREATE:
                plan.append({"action": "delete", "target": r.target})
            elif r.operation == SideEffectType.FILE_MODIFY:
                if r.before_hash:
                    plan.append({
                        "action": "restore",
                        "target": r.target,
                        "hash": r.before_hash,
                    })
            elif r.operation == SideEffectType.FILE_DELETE:
                if r.before_hash:
                    plan.append({
                        "action": "recreate",
                        "target": r.target,
                        "hash": r.before_hash,
                    })
        return plan

    def clear(self) -> None:
        """清空日志"""
        self.log.clear()

    @staticmethod
    def _hash(content: str) -> str:
        """SHA256 哈希（前 16 字符，用于幂等性比对）"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> List[Dict]:
        """序列化为字典列表"""
        return [
            {
                "timestamp": r.timestamp,
                "operation": r.operation.value,
                "target": r.target,
                "before_hash": r.before_hash,
                "after_hash": r.after_hash,
                "metadata": r.metadata,
            }
            for r in self.log
        ]
