#!/usr/bin/env python3
"""
读写分离调度器完整实现

设计原则：
- 只读操作并发执行（read_file, list_dir, search 等）
- 写入操作严格排队（write_file, delete, move 等）
- 同一资源的读写操作正确处理依赖关系
"""

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
import time


class OpType(Enum):
    READ = "read"
    WRITE = "write"


@dataclass
class Operation:
    """单个操作"""
    id: str
    name: str
    type: OpType
    resource: str           # 操作的资源路径（用于依赖判断）
    handler: Callable[..., Any]
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)  # 依赖的其他操作 id

    @property
    def is_readonly(self) -> bool:
        return self.type == OpType.READ


@dataclass
class OpResult:
    op_id: str
    success: bool
    result: Any = None
    error: str = ""
    duration_ms: float = 0


class ReadWriteScheduler:
    """只读并发，写入排队，带依赖管理"""

    def __init__(self, max_read_concurrency: int = 10):
        self._max_read_concurrency = max_read_concurrency
        self._read_semaphore = asyncio.Semaphore(max_read_concurrency)
        self._write_lock = asyncio.Lock()
        self._results: dict[str, OpResult] = {}

    # ── 入口 ──────────────────────────────────────

    async def execute(self, ops: list[Operation]) -> list[OpResult]:
        """执行一批操作，自动分组并发/串行"""
        self._results.clear()

        # 拓扑排序（处理依赖）
        ordered = self._topological_sort(ops)

        # 分组：连续的只读操作可并发
        groups = self._group_ops(ordered)

        for group in groups:
            if all(op.is_readonly for op in group):
                await self._execute_read_group(group)
            else:
                await self._execute_write_group(group)

        return [self._results[op.id] for op in ops if op.id in self._results]

    # ── 执行 ──────────────────────────────────────

    async def _execute_read_group(self, ops: list[Operation]) -> None:
        """只读组：并发执行"""
        async def run(op: Operation):
            async with self._read_semaphore:
                await self._execute_one(op)

        await asyncio.gather(*(run(op) for op in ops))

    async def _execute_write_group(self, ops: list[Operation]) -> None:
        """写入组：串行排队"""
        async with self._write_lock:
            for op in ops:
                await self._execute_one(op)

    async def _execute_one(self, op: Operation) -> None:
        """执行单个操作，计时并记录结果"""
        start = time.monotonic()
        try:
            if asyncio.iscoroutinefunction(op.handler):
                result = await op.handler(*op.args, **op.kwargs)
            else:
                result = op.handler(*op.args, **op.kwargs)
            self._results[op.id] = OpResult(
                op_id=op.id,
                success=True,
                result=result,
                duration_ms=(time.monotonic() - start) * 1000,
            )
        except Exception as e:
            self._results[op.id] = OpResult(
                op_id=op.id,
                success=False,
                error=str(e),
                duration_ms=(time.monotonic() - start) * 1000,
            )

    # ── 分组逻辑 ──────────────────────────────────

    def _group_ops(self, ops: list[Operation]) -> list[list[Operation]]:
        """将操作分组：连续只读一组，遇到写入单独一组"""
        groups = []
        current_group = []

        for op in ops:
            if op.is_readonly:
                current_group.append(op)
            else:
                if current_group:
                    groups.append(current_group)
                    current_group = []
                groups.append([op])

        if current_group:
            groups.append(current_group)

        return groups

    # ── 拓扑排序 ──────────────────────────────────

    def _topological_sort(self, ops: list[Operation]) -> list[Operation]:
        """按依赖关系排序"""
        op_map = {op.id: op for op in ops}
        visited: set[str] = set()
        temp: set[str] = set()
        order: list[Operation] = []

        def visit(op_id: str):
            if op_id in temp:
                raise ValueError(f"循环依赖: {op_id}")
            if op_id in visited:
                return
            temp.add(op_id)
            op = op_map.get(op_id)
            if op:
                for dep_id in op.depends_on:
                    if dep_id in op_map:
                        visit(dep_id)
            temp.discard(op_id)
            visited.add(op_id)
            if op:
                order.append(op)

        for op in ops:
            if op.id not in visited:
                visit(op.id)

        return order

    # ── 统计 ──────────────────────────────────────

    @property
    def summary(self) -> dict:
        results = list(self._results.values())
        success = sum(1 for r in results if r.success)
        total_time = sum(r.duration_ms for r in results)
        return {
            "total": len(results),
            "success": success,
            "failed": len(results) - success,
            "total_duration_ms": total_time,
            "avg_duration_ms": total_time / len(results) if results else 0,
        }


# ── 使用示例 ──────────────────────────────────────

async def demo():
    scheduler = ReadWriteScheduler(max_read_concurrency=5)

    ops = [
        Operation("r1", "read_file", OpType.READ, "/src/main.py",
                  handler=lambda: "file content"),
        Operation("r2", "list_dir", OpType.READ, "/src/",
                  handler=lambda: ["main.py", "utils.py"]),
        Operation("w1", "write_file", OpType.WRITE, "/src/output.txt",
                  handler=lambda: True, depends_on=["r1"]),
        Operation("r3", "search", OpType.READ, "/src/",
                  handler=lambda: ["match1"]),
    ]

    results = await scheduler.execute(ops)
    for r in results:
        status = "✅" if r.success else "❌"
        print(f"  {status} {r.op_id}: {r.duration_ms:.1f}ms")
    print(scheduler.summary)


if __name__ == "__main__":
    asyncio.run(demo())
