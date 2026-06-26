#!/usr/bin/env python3
"""
工具按需加载完整实现

设计原则：
- 首次请求只返回轻量索引（名称 + 用途描述）
- 被选中后才加载完整参数 schema 和执行逻辑
- 避免一次性加载所有工具的 token 开销
"""

from typing import Any, Callable, Optional
from dataclasses import dataclass, field


@dataclass
class ToolIndexEntry:
    """轻量索引条目 — 仅名称和用途"""
    name: str
    purpose: str
    category: str = "general"


@dataclass
class ToolFullSpec:
    """完整工具规格 — 选中后才加载"""
    name: str
    description: str
    parameters: dict[str, Any]          # JSON Schema
    handler: Callable[..., Any]
    requires_approval: bool = False
    examples: list[str] = field(default_factory=list)


class ToolRegistry:
    """轻量索引 → 选中 → 加载完整参数"""

    def __init__(self):
        self._index: dict[str, ToolIndexEntry] = {}
        self._loaders: dict[str, Callable[[], ToolFullSpec]] = {}
        self._cache: dict[str, ToolFullSpec] = {}

    # ── 注册 ──────────────────────────────────────

    def register(self, entry: ToolIndexEntry, loader: Callable[[], ToolFullSpec]) -> None:
        """注册工具：轻量索引 + 完整加载器"""
        self._index[entry.name] = entry
        self._loaders[entry.name] = loader

    # ── 轻量列表 ──────────────────────────────────

    def list_tools(self, category: Optional[str] = None) -> list[dict]:
        """返回轻量工具列表，不加载完整参数"""
        result = []
        for name, entry in self._index.items():
            if category and entry.category != category:
                continue
            result.append({
                "name": name,
                "purpose": entry.purpose,
                "category": entry.category,
            })
        return result

    # ── 按需加载 ──────────────────────────────────

    def get_full(self, name: str) -> Optional[ToolFullSpec]:
        """按需加载完整工具规格"""
        if name in self._cache:
            return self._cache[name]

        loader = self._loaders.get(name)
        if not loader:
            return None

        spec = loader()
        self._cache[name] = spec
        return spec

    # ── 批量加载 ──────────────────────────────────

    def preload(self, names: list[str]) -> dict[str, ToolFullSpec]:
        """批量预加载指定工具"""
        return {name: self.get_full(name) for name in names if self.get_full(name)}

    # ── 搜索 ──────────────────────────────────────

    def search(self, query: str) -> list[dict]:
        """在轻量索引中搜索匹配的工具"""
        q = query.lower()
        return [
            {"name": name, "purpose": entry.purpose}
            for name, entry in self._index.items()
            if q in name.lower() or q in entry.purpose.lower()
        ]

    # ── 工具执行 ──────────────────────────────────

    def execute(self, name: str, **kwargs) -> Any:
        """加载并执行工具。需要审批的工具会抛出异常。"""
        spec = self.get_full(name)
        if not spec:
            raise ValueError(f"未知工具: {name}")
        if spec.requires_approval:
            raise PermissionError(f"工具 {name} 需要审批才能执行")
        return spec.handler(**kwargs)

    # ── 统计 ──────────────────────────────────────

    @property
    def stats(self) -> dict:
        return {
            "indexed": len(self._index),
            "loaded": len(self._cache),
            "eager_ratio": f"{len(self._cache)}/{len(self._index)}",
        }


# ── 使用示例 ──────────────────────────────────────

if __name__ == "__main__":
    registry = ToolRegistry()

    # 注册：先给轻量索引，再给完整加载器
    registry.register(
        ToolIndexEntry("weather", "查询天气", category="info"),
        lambda: ToolFullSpec(
            name="weather",
            description="查询指定城市的天气",
            parameters={"city": {"type": "string"}},
            handler=lambda city: f"{city}: 晴 22°C",
            examples=["weather --city Beijing"],
        ),
    )

    # 轻量列表（不加载完整参数）
    print("Available tools:", registry.list_tools())
    print("Stats:", registry.stats)  # indexed=1, loaded=0

    # 选中后才加载
    spec = registry.get_full("weather")
    print(f"Loaded: {spec.name}, params: {spec.parameters}")
    print("Stats:", registry.stats)  # indexed=1, loaded=1
