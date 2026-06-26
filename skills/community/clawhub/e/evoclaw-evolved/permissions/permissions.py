# Permissions — 权限规则引擎
# 参考: claude-code/src/core/permissions/
#
# 设计:
#   ToolName              → 精确匹配 (Bash, Read, Write...)
#   ToolName(pattern)     → Glob 模式匹配 (Bash(python:*), Read(*.pem)...)
#
#   alwaysAllow / alwaysDeny 规则引擎
#   stripDangerousForAutoMode → Auto mode 时自动剥离危险规则
#   restoreDangerous → 退出时恢复

from __future__ import annotations
import fnmatch
import re
import copy
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum
import json

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))
PERMISSIONS_FILE = WORKSPACE / "evoclaw" / "permissions" / "rules.json"
PERMISSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)


# ─── 危险模式库 ──────────────────────────────────────────────────

DANGEROUS_PATTERNS = [
    "Bash(sudo *)",
    "Bash(rm *)",
    "Bash(mv * /dev/null)",
    "Bash(chmod *)",
    "Bash(python* -c *)",
    "Bash(curl * | sh)",
    "Bash(wget * | sh)",
    "Write(/etc/*)",
    "Write(~/.ssh/*)",
    "Write(*.exe)",
    "Read(/etc/shadow)",
    "Read(~/.bash_history)",
]


# ─── 权限模式 ────────────────────────────────────────────────────

class PermissionMode(str, Enum):
    ACCEPT_ALL = "accept_all"        # 全部允许
    DENY_ALL = "deny_all"            # 全部拒绝
    BY_RULES = "by_rules"            # 按规则
    ASK = "ask"                       # 逐个询问


# ─── 规则定义 ───────────────────────────────────────────────────

@dataclass
class PermissionRule:
    """
    单条权限规则.
    格式:
      ToolName              → 精确匹配
      ToolName(pattern)    → Glob 模式 (使用 fnmatch)
    """
    tool: str          # e.g. "Bash" 或 "Bash(python:*)"
    allow: bool = True # True = allow, False = deny
    reason: str = ""   # 原因说明
    source: str = "user"  # 规则来源 (user/org/plugin)

    def matches(self, tool_call: str) -> bool:
        """检查 tool_call 是否匹配此规则"""
        # 提取 tool 名和参数
        if "(" in self.tool:
            # 格式: ToolName(pattern)
            name_part = self.tool.split("(")[0]
            pattern_part = self.tool.split("(")[1].rstrip(")")
            if not fnmatch.fnmatch(tool_call, f"{name_part}({pattern_part})"):
                return False
            if pattern_part == "*":
                return True
            # 检查参数部分
            try:
                actual_pattern = tool_call.split("(", 1)[1].rstrip(")")
                return fnmatch.fnmatch(actual_pattern, pattern_part)
            except IndexError:
                return False
        else:
            # 精确匹配
            return tool_call == self.tool

    def to_dict(self) -> dict:
        return {"tool": self.tool, "allow": self.allow, "reason": self.reason, "source": self.source}

    @classmethod
    def from_dict(cls, d: dict) -> "PermissionRule":
        return cls(**d)


# ─── 权限上下文 ─────────────────────────────────────────────────

@dataclass
class PermissionContext:
    """
    权限上下文. 参考: claude-code ToolPermissionContext.
    不可变传递, 每次修改返回新实例.
    """
    mode: PermissionMode = PermissionMode.BY_RULES
    rules: list[PermissionRule] = field(default_factory=list)
    always_allow: list[PermissionRule] = field(default_factory=list)
    always_deny: list[PermissionRule] = field(default_factory=list)
    always_ask: list[PermissionRule] = field(default_factory=list)
    bypass_available: bool = True
    dangerous_rules_backup: list[PermissionRule] = field(default_factory=list)

    def query(self, tool_call: str) -> str:
        """
        查询 tool_call 的权限结果.
        Returns: "allow" | "deny" | "ask"
        """
        if self.mode == PermissionMode.ACCEPT_ALL:
            return "allow"
        if self.mode == PermissionMode.DENY_ALL:
            return "deny"

        # 规则匹配顺序: always_deny > always_allow > rules
        for rule in self.always_deny:
            if rule.matches(tool_call):
                return "deny"

        for rule in self.always_allow:
            if rule.matches(tool_call):
                return "allow"

        for rule in self.rules:
            if rule.matches(tool_call):
                return "allow" if rule.allow else "deny"

        return "ask"  # 未匹配的默认询问

    def strip_dangerous(self) -> "PermissionContext":
        """
        剥离危险规则 (进入 auto mode 时调用).
        参考: claude-code stripDangerousPermissionsForAutoMode()
        """
        dangerous = []
        remaining_always_allow = []
        for rule in self.always_allow:
            for pattern in DANGEROUS_PATTERNS:
                r = PermissionRule(tool=pattern)
                if r.matches(rule.tool):
                    dangerous.append(rule)
                    break
            else:
                remaining_always_allow.append(rule)

        ctx = PermissionContext(
            mode=self.mode,
            rules=self.rules,
            always_allow=remaining_always_allow,
            always_deny=self.always_deny,
            always_ask=self.always_ask,
            bypass_available=False,
            dangerous_rules_backup=dangerous,
        )
        return ctx

    def restore_dangerous(self) -> "PermissionContext":
        """
        恢复危险规则 (退出 auto mode 时调用).
        """
        return PermissionContext(
            mode=self.mode,
            rules=self.rules,
            always_allow=self.always_allow + self.dangerous_rules_backup,
            always_deny=self.always_deny,
            always_ask=self.always_ask,
            bypass_available=True,
            dangerous_rules_backup=[],
        )

    def with_mode(self, mode: PermissionMode) -> "PermissionContext":
        """返回新实例 (mode 改变)"""
        return PermissionContext(
            mode=mode,
            rules=self.rules,
            always_allow=self.always_allow,
            always_deny=self.always_deny,
            always_ask=self.always_ask,
            bypass_available=self.bypass_available,
            dangerous_rules_backup=self.dangerous_rules_backup,
        )

    def add_always_allow(self, tool: str, reason: str = "", source: str = "user") -> "PermissionContext":
        rule = PermissionRule(tool=tool, allow=True, reason=reason, source=source)
        existing = [r for r in self.always_allow if r.tool == tool]
        if not existing:
            new_allow = self.always_allow + [rule]
        else:
            new_allow = self.always_allow
        return PermissionContext(
            mode=self.mode, rules=self.rules,
            always_allow=new_allow,
            always_deny=self.always_deny,
            always_ask=self.always_ask,
            bypass_available=self.bypass_available,
            dangerous_rules_backup=self.dangerous_rules_backup,
        )

    def add_always_deny(self, tool: str, reason: str = "", source: str = "user") -> "PermissionContext":
        rule = PermissionRule(tool=tool, allow=False, reason=reason, source=source)
        existing = [r for r in self.always_deny if r.tool == tool]
        if not existing:
            new_deny = self.always_deny + [rule]
        else:
            new_deny = self.always_deny
        return PermissionContext(
            mode=self.mode, rules=self.rules,
            always_allow=self.always_allow,
            always_deny=new_deny,
            always_ask=self.always_ask,
            bypass_available=self.bypass_available,
            dangerous_rules_backup=self.dangerous_rules_backup,
        )

    def to_dict(self) -> dict:
        return {
            "mode": self.mode.value,
            "rules": [r.to_dict() for r in self.rules],
            "always_allow": [r.to_dict() for r in self.always_allow],
            "always_deny": [r.to_dict() for r in self.always_deny],
            "always_ask": [r.to_dict() for r in self.always_ask],
            "bypass_available": self.bypass_available,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PermissionContext":
        return cls(
            mode=PermissionMode(d.get("mode", "by_rules")),
            rules=[PermissionRule.from_dict(r) for r in d.get("rules", [])],
            always_allow=[PermissionRule.from_dict(r) for r in d.get("always_allow", [])],
            always_deny=[PermissionRule.from_dict(r) for r in d.get("always_deny", [])],
            always_ask=[PermissionRule.from_dict(r) for r in d.get("always_ask", [])],
            bypass_available=d.get("bypass_available", True),
        )


# ─── 规则存储 ───────────────────────────────────────────────────

class PermissionStore:
    """规则持久化"""

    @staticmethod
    def save(ctx: PermissionContext) -> None:
        PERMISSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PERMISSIONS_FILE.write_text(json.dumps(ctx.to_dict(), indent=2, ensure_ascii=False))

    @staticmethod
    def load() -> PermissionContext:
        if PERMISSIONS_FILE.exists():
            try:
                return PermissionContext.from_dict(json.loads(PERMISSIONS_FILE.read_text()))
            except Exception:
                pass
        return PermissionContext()

    @staticmethod
    def add_rule(ctx: PermissionContext, tool: str, allow: bool,
                 reason: str = "", source: str = "user") -> PermissionContext:
        """添加规则并保存"""
        new_ctx = PermissionContext(
            mode=ctx.mode,
            rules=ctx.rules + [PermissionRule(tool=tool, allow=allow, reason=reason, source=source)],
            always_allow=ctx.always_allow,
            always_deny=ctx.always_deny,
            always_ask=ctx.always_ask,
            bypass_available=ctx.bypass_available,
        )
        PermissionStore.save(new_ctx)
        return new_ctx


# ─── 便捷函数 ──────────────────────────────────────────────────

DEFAULT_CONTEXT = PermissionContext()


def check_permission(tool_call: str, ctx: Optional[PermissionContext] = None) -> str:
    """查询权限, 返回 'allow' | 'deny' | 'ask'"""
    return (ctx or DEFAULT_CONTEXT).query(tool_call)


def parse_tool_call(raw: str) -> tuple[str, str]:
    """解析 'Bash(python:*.py)' → ('Bash', 'python:*.py')"""
    if "(" in raw and raw.endswith(")"):
        parts = raw.split("(", 1)
        return parts[0], parts[1].rstrip(")")
    return raw, "*"


def enter_auto_mode(ctx: PermissionContext) -> PermissionContext:
    """进入 auto mode: 剥离危险权限"""
    return ctx.strip_dangerous()


def exit_auto_mode(ctx: PermissionContext) -> PermissionContext:
    """退出 auto mode: 恢复危险权限"""
    return ctx.restore_dangerous()


if __name__ == "__main__":
    ctx = PermissionContext()

    # 设置 always_allow
    ctx = ctx.add_always_allow("Read", "读取文件")
    ctx = ctx.add_always_allow("Write", "写入文件")
    ctx = ctx.add_always_deny("Bash(sudo *)", "危险命令")

    # 测试
    print(f"Read: {ctx.query('Read')}")          # allow
    print(f"Write: {ctx.query('Write')}")        # allow
    print(f"Bash(sudo rm -rf /): {ctx.query('Bash(sudo rm -rf /)')}")  # deny
    print(f"Bash(python test.py): {ctx.query('Bash(python test.py)')}")  # ask

    # Auto mode 测试
    auto_ctx = ctx.strip_dangerous()
    print(f"\nAuto mode - Read: {auto_ctx.query('Read')}")  # allow
    print(f"Auto mode - Bash(python:*) stripped: {auto_ctx.bypass_available}")  # False

    PermissionStore.save(auto_ctx)
    print("✅ Permissions: rules saved")
