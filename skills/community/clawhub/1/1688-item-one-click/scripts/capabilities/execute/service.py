#!/usr/bin/env python
"""执行操作服务"""

from _http import api_post
from _const import TOOL_CODE_EXECUTE
from _errors import ParamError, ServiceError

def execute_action(item_id: str, spi_code: str, spi_params: dict) -> dict:
    """
    执行实际的修改操作

    必须在 before_check 通过且用户确认后才能调用。

    Args:
        item_id: 商品ID
        spi_code: 操作码（如 spi_hsf_automatic_title）
        spi_params: 操作参数

    Returns:
        执行结果
    """
    if not item_id:
        raise ParamError("商品ID（item_id）不能为空")
    if not spi_code:
        raise ParamError("操作码（spi_code）不能为空")
    if not spi_params:
        raise ParamError("操作参数（spi_params）不能为空")

    data = api_post(
        f"/api/{TOOL_CODE_EXECUTE}/1.0.0",
        {
            "item_id": item_id,
            "spi_code": spi_code,
            "spi_params": spi_params,
        },
        timeout=30,
    )

    if not isinstance(data, dict):
        raise ServiceError("格式异常，请稍后重试")

    return data
