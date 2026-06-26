"""响应格式化工具模块

提供统一的响应格式
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, List, Dict


@dataclass
class Response:
    """标准响应格式"""
    code: int = 0
    message: str = "success"
    data: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @staticmethod
    def success(data: Any = None, message: str = "success") -> "Response":
        """成功响应"""
        return Response(code=0, message=message, data=data)

    @staticmethod
    def error(message: str, code: int = 1) -> "Response":
        """错误响应"""
        return Response(code=code, message=message, data=None)


@dataclass
class ListResponse:
    """列表响应格式"""
    items: List[Any] = field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@dataclass
class ErrorResponse:
    """错误响应格式"""
    code: int
    message: str
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"code": self.code, "message": self.message}
        if self.details:
            result["details"] = self.details
        return result

    def to_json(self, indent: Optional[int] = None) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


def format_tool_response(
    success: bool = True,
    data: Any = None,
    error_message: Optional[str] = None,
    error_code: int = 1,
    **extra_fields
) -> Dict[str, Any]:
    """格式化工具响应

    统一的响应格式：
    - success: 是否成功
    - data: 响应数据（成功时）
    - error_message: 错误信息（失败时）
    - error_code: 错误码（失败时）
    - 其他额外字段

    Args:
        success: 是否成功
        data: 响应数据
        error_message: 错误信息
        error_code: 错误码
        **extra_fields: 额外字段

    Returns:
        格式化的响应字典
    """
    if success:
        result = {
            "success": True,
            "code": 0,
            "message": "success",
            "data": data
        }
    else:
        result = {
            "success": False,
            "code": error_code,
            "message": error_message or "Unknown error",
            "data": None
        }

    # 添加额外字段
    result.update(extra_fields)

    return result


def format_success(data: Any = None, message: str = "success", **kwargs) -> Dict[str, Any]:
    """格式化成功响应为字典"""
    result = {
        "success": True,
        "code": 0,
        "message": message,
        "data": data
    }
    result.update(kwargs)
    return result


def format_error(message: str, code: int = 1, **kwargs) -> Dict[str, Any]:
    """格式化错误响应为字典"""
    result = {
        "success": False,
        "code": code,
        "message": message,
        "data": None
    }
    result.update(kwargs)
    return result


def format_list(items: List[Any], total: int = 0, **kwargs) -> Dict[str, Any]:
    """格式化列表响应为字典"""
    result = {
        "success": True,
        "code": 0,
        "message": "success",
        "data": {
            "items": items,
            "total": total,
        }
    }
    result["data"].update(kwargs)
    return result
