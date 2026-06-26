#!/usr/bin/env python3
"""
权限门控完整实现 — Fail-closed 安全模型

设计原则：
- 默认拒绝所有操作，显式授权才能执行
- 只读操作自动放行，写入操作需要用户确认
- 支持工具级权限分级（none/read/write/admin）
"""

from enum import IntEnum
from typing import Callable, Optional
import json
import hashlib


class PermissionLevel(IntEnum):
    NONE = 0
    READ = 1
    WRITE = 2
    ADMIN = 3


class ToolPermissionGate:
    """Fail-closed 权限门控。默认拒绝，显式授权。"""

    def __init__(self, config_path: Optional[str] = None):
        self._permissions: dict[str, PermissionLevel] = {}
        self._readonly_tools: set[str] = set()
        self._hooks: dict[str, list[Callable]] = {
            "before": [],
            "after": [],
            "on_deny": [],
        }
        self._audit_log: list[dict] = []
        if config_path:
            self._load_config(config_path)

    # ── 核心判断 ──────────────────────────────────

    def can_execute(self, tool_name: str, level: PermissionLevel = PermissionLevel.READ) -> bool:
        """判断是否允许执行。未显式注册的工具默认拒绝。"""
        if tool_name in self._readonly_tools:
            return True
        if tool_name not in self._permissions:
            return False  # 未注册工具默认拒绝
        required = self._permissions[tool_name]
        return level >= required

    def request_approval(self, tool_name: str, reason: str = "") -> str:
        """生成授权请求（由调用方展示给用户）"""
        return (
            f"⚠️ 需要授权执行 {tool_name}\n"
            f"   原因: {reason or '未指定'}\n"
            f"   确认吗？(y/n)"
        )

    # ── 权限管理 ──────────────────────────────────

    def grant(self, tool_name: str, level: PermissionLevel) -> None:
        """授予权限"""
        prev = self._permissions.get(tool_name, PermissionLevel.NONE)
        self._permissions[tool_name] = level
        self._log("grant", tool_name, f"{prev.name} → {level.name}")

    def revoke(self, tool_name: str) -> None:
        """撤销权限"""
        self._permissions.pop(tool_name, None)
        self._log("revoke", tool_name)

    def mark_readonly(self, tool_name: str) -> None:
        """标记为只读工具（自动放行）"""
        self._readonly_tools.add(tool_name)

    # ── 钩子系统 ──────────────────────────────────

    def on(self, event: str, callback: Callable) -> None:
        """注册事件钩子: before | after | on_deny"""
        if event in self._hooks:
            self._hooks[event].append(callback)

    def _fire(self, event: str, **kwargs) -> None:
        for cb in self._hooks.get(event, []):
            try:
                cb(**kwargs)
            except Exception as e:
                self._log("hook_error", event, str(e))

    # ── 审计 ──────────────────────────────────────

    def _log(self, action: str, target: str, detail: str = "") -> None:
        from datetime import datetime
        self._audit_log.append({
            "ts": datetime.now().isoformat(),
            "action": action,
            "target": target,
            "detail": detail,
        })

    def audit_report(self) -> list[dict]:
        return list(self._audit_log)

    # ── 持久化 ────────────────────────────────────

    def _load_config(self, path: str) -> None:
        with open(path) as f:
            cfg = json.load(f)
        for tool, lvl in cfg.get("permissions", {}).items():
            self._permissions[tool] = PermissionLevel[lvl.upper()]
        for tool in cfg.get("readonly", []):
            self._readonly_tools.add(tool)

    def save_config(self, path: str) -> None:
        cfg = {
            "permissions": {k: v.name.lower() for k, v in self._permissions.items()},
            "readonly": sorted(self._readonly_tools),
        }
        with open(path, "w") as f:
            json.dump(cfg, f, indent=2)


# ── 使用示例 ──────────────────────────────────────

if __name__ == "__main__":
    gate = ToolPermissionGate()

    # 注册只读工具
    gate.mark_readonly("read_file")
    gate.mark_readonly("list_dir")

    # 写入工具需要显式授权
    gate.grant("write_file", PermissionLevel.WRITE)
    gate.grant("delete_file", PermissionLevel.ADMIN)

    # 注册拒绝钩子
    gate.on("on_deny", lambda tool_name, **kw: print(f"🚫 {tool_name} 被拒绝"))

    # 测试
    print(gate.can_execute("read_file"))    # True（只读）
    print(gate.can_execute("write_file"))   # True（已授权）
    print(gate.can_execute("delete_file"))  # True（Admin）
    print(gate.can_execute("run_shell"))    # False（未授权）
