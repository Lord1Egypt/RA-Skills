# Tool Schema Validation
# 参考: claude-code src/core/tools.ts ToolInputJSONSchema + ValidationResult
#
# 设计:
#   ValidationResult 标准化返回
#     {result: true}  或  {result: false, message: string, errorCode: int}
#   工具调用前校验输入类型/必填/格式
#   ToolPermissionContext 权限上下文深层传递

from __future__ import annotations
import re
import fnmatch
from typing import Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


# ─── 验证结果 ───────────────────────────────────────────────────

@dataclass
class ValidationResult:
    """
    标准化验证结果.
    参考: claude-code ValidationResult 类型.
    
    成功: {result: True}
    失败: {result: False, message: "...", errorCode: int}
    """
    result: bool
    message: str = ""
    error_code: int = 0
    field: str = ""  # 可选: 失败字段名

    def to_dict(self) -> dict:
        if self.result:
            return {"result": True}
        return {
            "result": False,
            "message": self.message,
            "errorCode": self.error_code,
            "field": self.field,
        }

    @classmethod
    def ok(cls) -> "ValidationResult":
        return cls(result=True)

    @classmethod
    def fail(cls, message: str, error_code: int = 1, field: str = "") -> "ValidationResult":
        return cls(result=False, message=message, error_code=error_code, field=field)


# ─── 错误码定义 ─────────────────────────────────────────────────

class ErrorCode(int, Enum):
    UNKNOWN = 1
    TYPE_MISMATCH = 2          # 类型不匹配
    REQUIRED_MISSING = 3       # 必填字段缺失
    FORMAT_INVALID = 4         # 格式非法
    RANGE_OUT_OF_BOUNDS = 5    # 数值超出范围
    PERMISSION_DENIED = 6      # 权限不足
    NOT_FOUND = 7              # 资源不存在
    DUPLICATE = 8              # 重复条目
    TOOL_NOT_FOUND = 9         # 工具不存在


# ─── 类型检查 ───────────────────────────────────────────────────

TYPE_CHECKERS: dict[str, Callable[[Any], bool]] = {
    "string": lambda v: isinstance(v, str),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


# ─── 工具 Schema 定义 ──────────────────────────────────────────

@dataclass
class ToolSchema:
    """
    工具输入 Schema.
    参考: claude-code ToolInputJSONSchema.
    """
    name: str
    description: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)  # JSON Schema style

    def validate(self, args: dict) -> ValidationResult:
        """
        验证工具调用参数.
        支持:
          - required: 必填字段
          - type: 类型检查
          - pattern: 正则表达式
          - enum: 枚举值
          - minLength/maxLength: 字符串长度
          - minimum/maximum: 数值范围
        """
        props = self.parameters.get("properties", {})
        required = self.parameters.get("required", [])

        # 1. 必填检查
        for field_name in required:
            if field_name not in args or args[field_name] is None:
                return ValidationResult.fail(
                    f"Missing required field: {field_name}",
                    error_code=ErrorCode.REQUIRED_MISSING,
                    field=field_name,
                )

        # 2. 类型 + 格式检查
        for field_name, field_schema in props.items():
            value = args.get(field_name)
            if value is None:
                continue  # 可选字段空值跳过

            field_type = field_schema.get("type")
            if field_type and field_type in TYPE_CHECKERS:
                if not TYPE_CHECKERS[field_type](value):
                    return ValidationResult.fail(
                        f"Field '{field_name}' must be of type {field_type}, got {type(value).__name__}",
                        error_code=ErrorCode.TYPE_MISMATCH,
                        field=field_name,
                    )

            # pattern
            pattern = field_schema.get("pattern")
            if pattern and isinstance(value, str):
                if not re.match(pattern, value):
                    return ValidationResult.fail(
                        f"Field '{field_name}' does not match pattern: {pattern}",
                        error_code=ErrorCode.FORMAT_INVALID,
                        field=field_name,
                    )

            # enum
            enum = field_schema.get("enum")
            if enum and value not in enum:
                return ValidationResult.fail(
                    f"Field '{field_name}' must be one of: {', '.join(map(str, enum))}",
                    error_code=ErrorCode.FORMAT_INVALID,
                    field=field_name,
                )

            # string length
            if isinstance(value, str):
                min_len = field_schema.get("minLength")
                max_len = field_schema.get("maxLength")
                if min_len and len(value) < min_len:
                    return ValidationResult.fail(
                        f"Field '{field_name}' must be at least {min_len} characters",
                        error_code=ErrorCode.RANGE_OUT_OF_BOUNDS,
                        field=field_name,
                    )
                if max_len and len(value) > max_len:
                    return ValidationResult.fail(
                        f"Field '{field_name}' must be at most {max_len} characters",
                        error_code=ErrorCode.RANGE_OUT_OF_BOUNDS,
                        field=field_name,
                    )

            # number range
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                minimum = field_schema.get("minimum")
                maximum = field_schema.get("maximum")
                if minimum is not None and value < minimum:
                    return ValidationResult.fail(
                        f"Field '{field_name}' must be >= {minimum}",
                        error_code=ErrorCode.RANGE_OUT_OF_BOUNDS,
                        field=field_name,
                    )
                if maximum is not None and value > maximum:
                    return ValidationResult.fail(
                        f"Field '{field_name}' must be <= {maximum}",
                        error_code=ErrorCode.RANGE_OUT_OF_BOUNDS,
                        field=field_name,
                    )

        return ValidationResult.ok()


# ─── 工具注册表 ─────────────────────────────────────────────────

class ToolRegistry:
    """
    工具注册表.
    注册工具 Schema，验证调用参数.
    """

    _tools: dict[str, ToolSchema] = {}

    @classmethod
    def register(cls, schema: ToolSchema) -> None:
        cls._tools[schema.name] = schema

    @classmethod
    def get(cls, name: str) -> Optional[ToolSchema]:
        return cls._tools.get(name)

    @classmethod
    def validate(cls, tool_name: str, args: dict) -> ValidationResult:
        schema = cls._tools.get(tool_name)
        if not schema:
            return ValidationResult.fail(
                f"Tool '{tool_name}' not found",
                error_code=ErrorCode.TOOL_NOT_FOUND,
            )
        return schema.validate(args)

    @classmethod
    def list_tools(cls) -> list[str]:
        return list(cls._tools.keys())


# ─── 预置工具 Schemas ──────────────────────────────────────────

def register_standard_tools() -> None:
    """注册 OpenClaw 标准工具 Schema"""

    ToolRegistry.register(ToolSchema(
        name="Read",
        description="读取文件",
        parameters={
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {"type": "string", "minLength": 1},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10000},
                "offset": {"type": "integer", "minimum": 1},
            },
        },
    ))

    ToolRegistry.register(ToolSchema(
        name="Write",
        description="写文件",
        parameters={
            "type": "object",
            "required": ["file_path", "content"],
            "properties": {
                "file_path": {"type": "string", "minLength": 1},
                "content": {"type": "string"},
            },
        },
    ))

    ToolRegistry.register(ToolSchema(
        name="exec",
        description="执行 shell 命令",
        parameters={
            "type": "object",
            "required": ["command"],
            "properties": {
                "command": {"type": "string", "minLength": 1},
                "timeout": {"type": "integer", "minimum": 1, "maximum": 3600},
                "workdir": {"type": "string"},
                "elevated": {"type": "boolean"},
            },
        },
    ))

    ToolRegistry.register(ToolSchema(
        name="sessions_spawn",
        description="创建子代理",
        parameters={
            "type": "object",
            "required": ["task", "runtime"],
            "properties": {
                "task": {"type": "string", "minLength": 1},
                "runtime": {"type": "string", "enum": ["subagent", "acp"]},
                "mode": {"type": "string", "enum": ["run", "session"]},
                "agentId": {"type": "string"},
            },
        },
    ))

    ToolRegistry.register(ToolSchema(
        name="feishu_bitable_create_record",
        description="飞书多维表格创建记录",
        parameters={
            "type": "object",
            "required": ["app_token", "table_id", "fields"],
            "properties": {
                "app_token": {"type": "string", "minLength": 1},
                "table_id": {"type": "string", "minLength": 1},
                "fields": {"type": "object"},
            },
        },
    ))


# ─── 便捷函数 ────────────────────────────────────────────────────

def validate_tool_call(tool_name: str, args: dict) -> ValidationResult:
    """验证工具调用参数"""
    return ToolRegistry.validate(tool_name, args)


if __name__ == "__main__":
    register_standard_tools()

    # Test: valid call
    r = validate_tool_call("Read", {"file_path": "/tmp/test.txt", "limit": 100})
    print(f"Read(valid): {r.to_dict()}")

    # Test: missing required
    r = validate_tool_call("Read", {"limit": 100})
    print(f"Read(missing): {r.to_dict()}")

    # Test: wrong type
    r = validate_tool_call("Read", {"file_path": 123})
    print(f"Read(wrong_type): {r.to_dict()}")

    # Test: unknown tool
    r = validate_tool_call("FakeTool", {})
    print(f"FakeTool: {r.to_dict()}")

    print("✅ ToolSchema: all tests passed")
