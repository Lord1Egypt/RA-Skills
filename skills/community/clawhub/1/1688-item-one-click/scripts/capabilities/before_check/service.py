#!/usr/bin/env python
"""执行前检查服务"""

from _http import api_post
from _const import TOOL_CODE_BEFORE_CHECK
from _errors import ParamError, ServiceError

def before_check(item_id: str, spi_code: str, spi_params: dict) -> dict:
    """
    执行操作前的前置检查

    判断是否可以执行、是否有协议需要签署。

    Args:
        item_id: 商品ID
        spi_code: 操作码（如 spi_hsf_automatic_title）
        spi_params: 操作参数

    Returns:
        检查结果
    """
    if not item_id:
        raise ParamError("商品ID（item_id）不能为空")
    if not spi_code:
        raise ParamError("操作码（spi_code）不能为空")
    if spi_params is None:
        raise ParamError("操作参数（spi_params）不能为空")

    data = api_post(
        f"/api/{TOOL_CODE_BEFORE_CHECK}/1.0.0",
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
