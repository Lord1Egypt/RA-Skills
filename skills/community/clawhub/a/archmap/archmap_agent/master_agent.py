from typing import Any


class MasterAgent:
    def __init__(self, mark_shared: bool = True):
        self.mark_shared = mark_shared

    @staticmethod
    def _module_layer(module_id: str) -> int:
        """按模块名推断架构层级：0=存储/基础设施，1=后端/核心，2=前端/展示，3=部署/文档/测试。"""
        lower = module_id.lower()
        if any(k in lower for k in ("data", "lance", "storage", "db", "archive", "checkpoint", "cache", "pdf", "review", "memory", "vector")):
            return 0
        if any(k in lower for k in ("frontend", "ui", "web", "client", "appium-frontend", "app.frontend")):
            return 2
        if any(k in lower for k in ("deploy", "docker", "docs", "test", "spec", "output", "log")):
            return 3
        return 1

    def _build_reverse_deps(self, modules: list[dict]) -> dict[str, list[str]]:
        reverse: dict[str, list[str]] = {m["module_id"]: [] for m in modules}
        for m in modules:
            for dep in m.get("dependencies", []):
                if dep in reverse:
                    reverse[dep].append(m["module_id"])
        return reverse

    @staticmethod
    def _is_valid_storage_name(name: str) -> bool:
        """过滤前端UI组件、版本号、通用中间件名等无效存储名称。"""
        n = str(name).strip()
        if not n or len(n) > 64 or len(n) <= 2:
            return False
        lower = n.lower()
        invalid = {
            "immutable", "writable", "on", "any", "default", "throw", "true", "false", "return",
            "function", "const", "let", "var", "null", "undefined", "table", "mysql", "redis",
            "value of", "ng-table", "jquery-sortable", "fixed-data-table", "x-editable",
            "antd-tools run sort-api-table", "#/rabbitmq",
        }
        if lower in invalid:
            return False
        if any(p in n for p in ("^", "~", ">=", "<=", ">", "<", "@", "display:")):
            return False
        if any(k in lower for k in ("editable", "sortable", "jquery", "leaflet", "ng-table")):
            return False
        return True

    @staticmethod
    def _is_valid_api_route(route: str) -> bool:
        """过滤乱码、超长、非法字符的API路由。"""
        r = str(route).strip()
        if not r or "/" not in r or len(r) > 120:
            return False
        if any(c in r for c in "|'\"\\ "):
            return False
        return True

    def _detect_dependencies(self, modules: list[dict]) -> list[dict]:
        route_to_modules: dict[str, list[str]] = {}
        storage_to_modules: dict[str, list[str]] = {}
        route_owners: dict[str, list[str]] = {}
        for m in modules:
            for api in m.get("apis", []):
                route = api.get("route", "")
                if not self._is_valid_api_route(route):
                    continue
                route_to_modules.setdefault(route, []).append(m["module_id"])
                if api.get("kind") == "defined":
                    route_owners.setdefault(route, []).append(m["module_id"])
            for storage in m.get("storages", []):
                name = storage.get("name", "")
                if not self._is_valid_storage_name(name):
                    continue
                storage_to_modules.setdefault(name, []).append(m["module_id"])

        shared_routes = {r for r, mods in route_to_modules.items() if len(mods) > 1}
        shared_storages = {s for s, mods in storage_to_modules.items() if len(mods) > 1}

        # 模块可导入名归一化：Python 包名不允许 '-'，目录 appium-frontend 对应导入名 appium_frontend
        importable: dict[str, str] = {}
        for m in modules:
            mid = m["module_id"]
            importable.setdefault(mid, mid)
            importable.setdefault(mid.replace("-", "_"), mid)

        for m in modules:
            mid = m["module_id"]
            deps: dict[str, str] = {}  # target -> kind，import 边优先不可覆盖
            # 1) import 边（真实代码级依赖，循环依赖检测唯一依据）
            for pkg in m.get("imports", []):
                target = importable.get(str(pkg))
                if target and target != mid:
                    deps[target] = "import"
            # 2) api 消费边：仅「引用他方定义的路由」成边，提供方自身不成边
            for api in m.get("apis", []):
                route = api.get("route", "")
                api["shared"] = route in shared_routes
                if api.get("kind") != "referenced" or route not in route_owners:
                    continue
                for other in route_owners[route]:
                    if other != mid and other not in deps:
                        deps[other] = "api"
            # 3) 存储共享边（保留原层级方向逻辑）
            for storage in m.get("storages", []):
                name = storage.get("name", "")
                if name not in shared_storages:
                    storage["shared"] = False
                    continue
                storage["shared"] = True
                layer_self = self._module_layer(mid)
                for other in storage_to_modules[name]:
                    if other == mid or other in deps:
                        continue
                    layer_other = self._module_layer(other)
                    # 仅允许从高层依赖低层；同层保留双向
                    if layer_self >= layer_other:
                        deps[other] = "storage"
            m["dependency_edges"] = [{"target": t, "kind": k} for t, k in sorted(deps.items())]
            m["dependencies"] = sorted(deps)
            m["import_dependencies"] = sorted(t for t, k in deps.items() if k == "import")

        reverse = self._build_reverse_deps(modules)
        for m in modules:
            m["dependents"] = sorted(reverse.get(m["module_id"], []))
        return modules

    def aggregate(self, modules: list[dict], baseline: dict | None = None) -> dict:
        modules = self._detect_dependencies(modules)
        shared_apis = sorted({api["route"] for m in modules for api in m.get("apis", []) if api.get("shared")})
        shared_storages = sorted({s["name"] for m in modules for s in m.get("storages", []) if s.get("shared")})

        result = {
            "modules": modules,
            "shared_apis": shared_apis,
            "shared_storages": shared_storages,
            "module_order": [m["module_id"] for m in modules],
        }
        if baseline:
            result["previous_baseline_version"] = baseline.get("generated_at")
        return result

    def merge_incremental(self, baseline: dict, new_modules: list[dict], changed_ids: set[str]) -> dict:
        raw_modules = baseline.get("modules", [])
        if isinstance(raw_modules, dict):
            existing = dict(raw_modules)
        else:
            existing = {m["module_id"]: m for m in raw_modules}
        for m in new_modules:
            existing[m["module_id"]] = m
        # 清理废弃依赖引用
        all_ids = set(existing.keys())
        for m in existing.values():
            m["dependencies"] = [d for d in m.get("dependencies", []) if d in all_ids]
            m["dependents"] = [d for d in m.get("dependents", []) if d in all_ids]
        modules = list(existing.values())
        return self.aggregate(modules, baseline)
