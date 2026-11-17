import re
from typing import Any


class GranularityValidator:
    def __init__(self):
        self.violations: list[dict] = []

    def reset(self):
        self.violations = []

    def check_module(self, module: dict) -> bool:
        ok = True
        path = module.get("module_path", "")
        if not path.endswith("/"):
            self.violations.append({
                "type": "module",
                "module_id": module.get("module_id"),
                "reason": "module_path必须以/结尾",
                "value": path,
            })
            ok = False
        return ok

    def check_api(self, module_id: str, api: dict) -> bool:
        ok = True
        allowed = {"route", "purpose", "shared", "kind"}
        extra = set(api.keys()) - allowed
        if extra:
            self.violations.append({
                "type": "api",
                "module_id": module_id,
                "reason": "API包含禁止字段",
                "value": list(extra),
            })
            ok = False
        if not api.get("route"):
            self.violations.append({
                "type": "api",
                "module_id": module_id,
                "reason": "API路由缺失",
                "value": api,
            })
            ok = False
        return ok

    def check_storage(self, module_id: str, storage: dict) -> bool:
        ok = True
        allowed = {"name", "shared"}
        extra = set(storage.keys()) - allowed
        if extra:
            self.violations.append({
                "type": "storage",
                "module_id": module_id,
                "reason": "存储包含禁止字段",
                "value": list(extra),
            })
            ok = False
        if not storage.get("name"):
            self.violations.append({
                "type": "storage",
                "module_id": module_id,
                "reason": "存储名称缺失",
                "value": storage,
            })
            ok = False
        return ok

    def validate(self, module: dict) -> tuple[bool, list[dict]]:
        self.reset()
        ok = self.check_module(module)
        for api in module.get("apis", []):
            ok = self.check_api(module.get("module_id"), api) and ok
        for storage in module.get("storages", []):
            ok = self.check_storage(module.get("module_id"), storage) and ok
        return ok, list(self.violations)
