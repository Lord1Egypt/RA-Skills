# -*- coding: utf-8 -*-
"""
订单询盘能力实现

调用 NewtonOrderBatchInquiry 接口，对指定订单发起询盘。

接口入参：
  - orderIds: 订单 id 列表，最多十个
  - question：询盘问题（单个字符串）
  - imageList: 采购商品图片说明，URL 列表（可不传）
  - ordersStatus: 订单状态 set（可不传）

接口出参：
  - suc：bool，是否成功
  - errorMsg：错误信息
"""

import sys
import time
import uuid
from typing import Dict, Any, List, Optional

from _http import api_post
from _errors import ServiceError, ParamError
from settings import settings

_MAX_ORDER_IDS = 10


def _resolve_image_list(
    local_images: Optional[List[str]] = None,
    image_urls: Optional[List[str]] = None,
) -> List[str]:
    """
    将本地图片和在线图片 URL 统一解析为 URL 列表

    本地图片：上传到纵横平台，获取 CDN URL
    在线链接：直接使用

    Args:
        local_images: 本地图片文件路径列表
        image_urls: 图片在线链接列表

    Returns:
        图片 URL 列表
    """
    result = []

    if local_images:
        from _img_upload import upload_images
        urls = upload_images(local_images)
        result.extend(urls)
        print("本地图片上传完成，获取到 {} 个 URL".format(len(urls)), file=sys.stderr)

    if image_urls:
        result.extend(image_urls)

    return result


def inquiry_send(
    order_ids: List[str],
    question: str,
    local_images: Optional[List[str]] = None,
    image_urls: Optional[List[str]] = None,
    orders_status: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    订单询盘主函数，调用 NewtonOrderBatchInquiry 触发询盘。

    Args:
        order_ids: 订单 id 列表，最多 10 个
        question: 询盘问题（单个字符串，必填）
        local_images: 本地图片路径列表，采购商品图片说明（可不传，自动上传获取URL）
        image_urls: 图片URL列表，采购商品图片说明（可不传，已有在线链接时使用）
        orders_status: 订单状态 set（可不传）

    Returns:
        {"suc": bool, "errorMsg": str, "elapsed_seconds": float}
    """
    if not order_ids:
        raise ParamError("orderIds 不能为空")

    if len(order_ids) > _MAX_ORDER_IDS:
        raise ParamError("orderIds 最多 {} 个，当前 {} 个".format(_MAX_ORDER_IDS, len(order_ids)))

    if not question or not question.strip():
        raise ParamError("question 不能为空")

    # 处理图片参数：本地上传 + 在线链接 → 统一为 URL 列表
    image_list = _resolve_image_list(local_images, image_urls)

    body: Dict[str, Any] = {
        "orderIds": order_ids,
        "question": question,
        "appKey": "newton_api_order_inquiry",
        "imageList": image_list,
        "taskId": str(uuid.uuid4()),
    }

    if orders_status:
        body["ordersStatus"] = orders_status

    start_time = time.time()

    resp = api_post(
        path=settings.TOOL_PATH,
        body=body,
        timeout=settings.TOOL_TIMEOUT,
    )

    elapsed = round(time.time() - start_time, 1)

    # 解析接口返回（实际结构: resp.data.model.suc）
    data = resp.get("data", {})
    if isinstance(data, dict):
        model = data.get("model", {})
        if isinstance(model, dict):
            suc = model.get("suc", False)
            error_msg = model.get("errorMsg", "")
        else:
            suc = data.get("suc", False)
            error_msg = data.get("errorMsg", "")
    else:
        suc = resp.get("suc", False)
        error_msg = resp.get("errorMsg", "")

    if not suc:
        raise ServiceError("询盘触发失败: {}".format(error_msg or resp))

    return {
        "suc": suc,
        "errorMsg": error_msg,
        "elapsed_seconds": elapsed,
    }
