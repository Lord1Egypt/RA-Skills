from pathlib import Path
from typing import Any


class MermaidRenderer:
    # 非业务目录关键词，出现即排除（不区分大小写）
    NON_BUSINESS_KEYWORDS = (
        ".agent_backup", "backup", "ckpt", "tmp", "temp", ".cache", "cache",
        "logs", "log", "snapshots", "snapshot",
    )

    def __init__(self):
        self._non_business_cache: dict[str, bool] = {}

    def _is_business_module(self, module_path: str) -> bool:
        lower = module_path.lower()
        if any(kw in lower for kw in self.NON_BUSINESS_KEYWORDS):
            return False
        # 过滤隐藏目录、缓存/备份/临时/日志等目录
        parts = module_path.split("/")
        return not any(p.startswith(".") or p.startswith("_") or p.lower() in self.NON_BUSINESS_KEYWORDS for p in parts if p)

    @staticmethod
    def _safe_id(mid: str) -> str:
        """把模块ID转成Mermaid合法节点ID。"""
        safe = "".join(c if c.isalnum() or c == "_" else "_" for c in str(mid)).lstrip("_")
        return safe or "node"

    def _modules_to_dict(self, modules: list[dict] | dict[str, dict]) -> dict[str, dict]:
        """兼容 modules 为数组或对象两种历史格式。"""
        if isinstance(modules, dict):
            return modules
        return {m["module_id"]: m for m in modules}

    def _filter_modules(self, modules: list[dict] | dict[str, dict]) -> dict[str, dict]:
        modules = self._modules_to_dict(modules)
        return {
            mid: m for mid, m in modules.items()
            if self._is_business_module(m.get("module_path", mid))
        }

    @staticmethod
    def _clean_label(text: str) -> str:
        """清洗节点展示文本，移除不可见特殊字符与多余反斜杠。"""
        cleaned = "".join(c for c in str(text) if c.isprintable())
        cleaned = cleaned.replace("\\", "").replace('"', "'")
        return cleaned.strip() or "unknown"

    @staticmethod
    def _node_label(mid: str, module_path: str) -> str:
        """节点展示文本：模块名称 | 源码目录。"""
        name = Path(module_path).name or mid
        return f"{name} | {module_path}"

    # 架构分层命名（按 _module_layer 推断）
    LAYER_NAMES = {0: "数据/基础设施层", 1: "服务/核心层", 2: "前端/接入层", 3: "部署/支撑层"}

    def architecture_diagram(
        self,
        modules: list[dict] | dict[str, dict],
        new_modules: set[str] | None = None,
        modified_modules: set[str] | None = None,
        removed_modules: set[str] | None = None,
    ) -> str:
        new_modules = new_modules or set()
        modified_modules = modified_modules or set()
        removed_modules = removed_modules or set()

        filtered = self._filter_modules(modules)
        active = {
            mid: m for mid, m in filtered.items()
            if m.get("dependencies") or m.get("dependents")
        }
        # 无依赖模块不再静默丢弃，显式列入孤立区（A04-E01：防覆盖缺口被误读为不存在）
        isolated = {mid: m for mid, m in filtered.items() if mid not in active}

        lines = ["graph TD"]
        # 按架构层级分 subgraph 渲染，避免扁平毛线团
        by_layer: dict[int, list[str]] = {}
        for mid in active:
            by_layer.setdefault(self._module_layer(mid), []).append(mid)
        for layer in sorted(by_layer):
            lines.append(f'    subgraph LAYER{layer}["{self.LAYER_NAMES[layer]}"]')
            for mid in sorted(by_layer[layer]):
                safe = self._safe_id(mid)
                label = self._node_label(mid, active[mid].get("module_path", mid))
                lines.append(f'        {safe}["{label}"]')
            lines.append("    end")
        if isolated:
            lines.append('    subgraph ISOLATED["孤立模块（无依赖边，显式列出）"]')
            for mid in sorted(isolated):
                safe = self._safe_id(mid)
                label = self._node_label(mid, isolated[mid].get("module_path", mid))
                lines.append(f'        {safe}["{label}"]')
            lines.append("    end")

        edges = set()
        for mid, m in active.items():
            safe_src = self._safe_id(mid)
            for dep in m.get("dependencies", []):
                if dep in active:
                    safe_dst = self._safe_id(dep)
                    edge = (safe_src, safe_dst)
                    if edge not in edges:
                        edges.add(edge)
                        lines.append(f"    {safe_src} --> {safe_dst}")

        # 变更样式
        for mid in sorted(new_modules & set(active.keys())):
            lines.append(f"    style {self._safe_id(mid)} fill:#9cf")
        for mid in sorted(modified_modules & set(active.keys())):
            lines.append(f"    style {self._safe_id(mid)} fill:#ffd")
        for mid in sorted(removed_modules & set(active.keys())):
            lines.append(f"    style {self._safe_id(mid)} fill:#ccc")

        return "\n".join(lines)

    @staticmethod
    def _is_valid_storage_name(name: str) -> bool:
        """简单校验存储名称，过滤版本号、UI组件、代码关键字等脏数据。"""
        n = str(name).strip()
        if not n or len(n) > 64 or len(n) <= 2:
            return False
        lower = n.lower()
        invalid_names = {
            "immutable", "writable", "on", "any", "default", "throw", "true", "false", "return",
            "function", "const", "let", "var", "null", "undefined", "table", "mysql", "redis",
            "value of", "ng-table", "jquery-sortable", "fixed-data-table", "x-editable",
            "antd-tools run sort-api-table", "#/rabbitmq",
        }
        if lower in invalid_names:
            return False
        if any(p in n for p in ("^", "~", ">=", "<=", ">", "<", "@", "display:")):
            return False
        if any(k in lower for k in ("editable", "sortable", "jquery", "leaflet", "ng-table")):
            return False
        return True

    @staticmethod
    def _classify_storage(name: str) -> str:
        n = name.lower()
        if "redis" in n:
            return "Redis"
        if any(k in n for k in ("rabbit", "kafka", "mq", "queue")):
            return "MQ"
        if "minio" in n or "s3" in n:
            return "MinIO"
        if "lance" in n:
            return "LanceDB"
        if any(k in n for k in ("vector", "vec", "embedding")):
            return "VectorCollection"
        return "Table"

    def data_flow_diagram(
        self,
        shared_apis: list[str],
        shared_storages: list[str],
        modules: list[dict] | dict[str, dict],
        new_modules: set[str] | None = None,
        modified_modules: set[str] | None = None,
        removed_modules: set[str] | None = None,
    ) -> str:
        """数据链路图：graph LR，左侧业务模块，右侧全部存储资产，展示所有读写流向。"""
        filtered = self._filter_modules(modules)
        lines = ["graph LR"]

        # 收集全部有效存储（共享 + 独占）
        storage_ids: dict[str, str] = {}
        storage_kinds: dict[str, str] = {}
        idx = 0
        for m in filtered.values():
            for storage in m.get("storages", []):
                name = storage.get("name", "")
                if not self._is_valid_storage_name(name) or name in storage_ids:
                    continue
                storage_ids[name] = self._safe_id(f"STORAGE_{idx}")
                storage_kinds[name] = self._classify_storage(name)
                idx += 1

        # 右侧存储节点
        for name in sorted(storage_ids.keys()):
            safe = storage_ids[name]
            kind = storage_kinds[name]
            lines.append(f'    {safe}["{kind}：{self._clean_label(name)}"]')

        # 左侧业务模块节点（仅保留与存储存在关联的模块）
        connected_modules = {
            mid for mid, m in filtered.items()
            for storage in m.get("storages", [])
            if storage.get("name") in storage_ids
        }
        for mid in sorted(connected_modules):
            safe = self._safe_id(mid)
            label = self._node_label(mid, filtered[mid].get("module_path", mid))
            lines.append(f'    {safe}["{label}"]')

        # 模块 -> 存储 读写流向
        edges = set()
        for mid in sorted(connected_modules):
            safe_src = self._safe_id(mid)
            for storage in filtered[mid].get("storages", []):
                name = storage.get("name", "")
                if name in storage_ids:
                    safe_dst = storage_ids[name]
                    edge = (safe_src, safe_dst)
                    if edge not in edges:
                        edges.add(edge)
                        lines.append(f"    {safe_src} --> {safe_dst}")

        self._append_styles(lines, filtered, new_modules, modified_modules, removed_modules)
        return "\n".join(lines)

    @staticmethod
    def _module_layer(module_id: str) -> int:
        lower = module_id.lower()
        if any(k in lower for k in ("data", "lance", "storage", "db", "archive", "config", "redis", "mysql", "sqlite", "mongo", "elasticsearch")):
            return 0
        if any(k in lower for k in ("frontend", "ui", "web", "client", "appium-frontend", "react", "vue", "angular")):
            return 2
        if any(k in lower for k in ("deploy", "docker", "docs", "test", "ci", "cd", "scripts")):
            return 3
        return 1

    def _pick_module(self, active: dict[str, dict], layer: int, prefs: list[str]) -> str | None:
        ids = [mid for mid in active if self._module_layer(mid) == layer]
        return next((p for p in prefs if p in ids), ids[0] if ids else None)

    def sequence_diagram(
        self,
        modules: list[dict] | dict[str, dict],
        new_modules: set[str] | None = None,
        modified_modules: set[str] | None = None,
        removed_modules: set[str] | None = None,
    ) -> str:
        """时序图：按层选择典型模块，展示 User→前端→后端→存储→返回的完整业务闭环。"""
        filtered = self._filter_modules(modules)
        active = {mid: m for mid, m in filtered.items() if m.get("dependencies") or m.get("dependents")}
        lines = ["sequenceDiagram", "    actor User"]
        if not active:
            lines.extend(["    participant root", "    User->>root: 发起请求"])
            return "\n".join(lines)

        fe = self._pick_module(active, 2, ["frontend", "appium-frontend"])
        be = self._pick_module(active, 1, ["backend", "scripts"])
        storage = self._pick_module(active, 0, ["data", "config"])
        if storage is None:
            storage = next((mid for mid in active if active[mid].get("storages")), None)
        chain = [m for m in (fe, be, storage) if m]
        seen: set[str] = set()
        chain = [m for m in chain if not (m in seen or seen.add(m))]
        if not chain:
            chain = [next(iter(active))]

        for mid in chain:
            lines.append(f'    participant {self._safe_id(mid)} as "{active[mid].get("module_path", mid)}"')

        store_name = None
        for mid in chain[::-1]:
            for s in active[mid].get("storages", []):
                if self._is_valid_storage_name(s.get("name", "")):
                    store_name = self._clean_label(s["name"])
                    break
            if store_name:
                break
        if store_name is None:
            for m in active.values():
                for s in m.get("storages", []):
                    if self._is_valid_storage_name(s.get("name", "")):
                        store_name = self._clean_label(s["name"])
                        break
                if store_name:
                    break
        store_id = None
        if store_name:
            store_id = self._safe_id(f"storage_{store_name}")
            lines.append(f'    participant {store_id} as "{store_name}"')

        lines.append(f"    User->>+{self._safe_id(chain[0])}: 发起请求")
        prev = chain[0]
        for mid in chain[1:]:
            safe = self._safe_id(mid)
            lines.append(f"    {self._safe_id(prev)}->>+{safe}: 调用")
            prev = mid
        if store_id:
            lines.append(f"    {self._safe_id(prev)}->>+{store_id}: 写入/查询")
            lines.append(f"    {store_id}-->>-{self._safe_id(prev)}: 完成")

        for mid in chain[::-1][1:]:
            safe = self._safe_id(mid)
            lines.append(f"    {self._safe_id(prev)}-->>-{safe}: 返回")
            prev = mid
        lines.append(f"    {self._safe_id(prev)}-->>-User: 响应")
        return "\n".join(lines)

    def _append_styles(
        self,
        lines: list[str],
        filtered: dict[str, dict],
        new_modules: set[str] | None,
        modified_modules: set[str] | None,
        removed_modules: set[str] | None,
    ) -> None:
        new_modules = new_modules or set()
        modified_modules = modified_modules or set()
        removed_modules = removed_modules or set()
        for mid in sorted(new_modules & set(filtered.keys())):
            lines.append(f"    style {self._safe_id(mid)} fill:#9cf")
        for mid in sorted(modified_modules & set(filtered.keys())):
            lines.append(f"    style {self._safe_id(mid)} fill:#ffd")
        for mid in sorted(removed_modules & set(filtered.keys())):
            lines.append(f"    style {self._safe_id(mid)} fill:#ccc")

    def render_all(
        self,
        aggregated: dict,
        new_modules: set[str] | None = None,
        modified_modules: set[str] | None = None,
        removed_modules: set[str] | None = None,
    ) -> dict[str, str]:
        modules = self._modules_to_dict(aggregated.get("modules", {}))
        return {
            "architecture": self.architecture_diagram(modules, new_modules, modified_modules, removed_modules),
            "data_flow": self.data_flow_diagram(
                aggregated.get("shared_apis", []),
                aggregated.get("shared_storages", []),
                modules,
                new_modules,
                modified_modules,
                removed_modules,
            ),
            "sequence": self.sequence_diagram(modules, new_modules, modified_modules, removed_modules),
        }
