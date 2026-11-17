# -*- coding: utf-8 -*-
"""
订单询盘能力实现

调用 alibaba.1688.newton.order.batch.inquiry 接口，对指定订单发起询盘。

接口入参：
  - orderIds: 订单 id 列表
  - question：询盘问题（单个字符串）
  - imageList: 采购商品图片说明，URL 列表（可不传）
  - ordersStatus: 订单状态 set（可不传）

接口出参：
  - suc：bool，是否成功
  - errorMsg：错误信息
"""

import logging
import os
import sys
import time
import uuid
from typing import Dict, Any, List, Optional

from _http import api_post
from _errors import ServiceError, ParamError
from settings import settings

logger = logging.getLogger(__name__)

# Newton cloud 运行时会话上下文 → ext 字段的环境变量映射。
# 这些标识只存在于 runtime 元数据 / HTTP 头，不会进入 agent 的可见上下文，
# 因此无法靠主 agent 手填 --ext，只能由技能进程从运行时注入的环境变量读取。
# 注意：NEWTON_SESSION_ID / NEWTON_REPLY_ID 为与运行时约定的变量名，运行时是否真的注入
# 这些变量尚未在真实会话中核实（SLS 日志不含 env、无法证实/证伪）；若未注入则读到空、
# 该字段不下发（静默降级、无副作用）。需运行时侧确认或配合注入后方能真正生效。
_EXT_ENV_MAP = {
    # sessionId：会话级、稳定
    "sessionId": "NEWTON_SESSION_ID",
    # chat_id：会话消息级，用于回流商家回复时定位对话
    "chat_id": "NEWTON_REPLY_ID",
}


def _collect_runtime_ext() -> Dict[str, Any]:
    """
    从运行时注入的环境变量收集会话上下文，组装为 ext map。

    仅收集非空值；对应环境变量缺失时跳过该字段（不写空串）。
    """
    ctx: Dict[str, Any] = {}
    for ext_key, env_name in _EXT_ENV_MAP.items():
        val = os.environ.get(env_name, "").strip()
        if val:
            ctx[ext_key] = val
    return ctx

# 图片扩展名白名单：仅这些后缀的 URL 才会作为图片进入 imageList；
# 其它后缀（如 .xls/.pdf/.doc）视为普通文件链接，放入独立的 fileList 参数透传给商家。
_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp")


def _is_image_url(url: str) -> bool:
    """判断 URL 是否为图片格式（按扩展名，忽略 query/fragment）"""
    if not url:
        return False
    path = url.split("?", 1)[0].split("#", 1)[0]
    return path.lower().endswith(_IMAGE_EXTENSIONS)


def _classify_urls(urls: Optional[List[str]]) -> (List[str], List[str]):
    """将 URL 列表按扩展名拆分为 (图片URL, 非图片URL)"""
    image_urls: List[str] = []
    file_urls: List[str] = []
    if not urls:
        return image_urls, file_urls
    for url in urls:
        u = (url or "").strip()
        if not u:
            continue
        if _is_image_url(u):
            image_urls.append(u)
        else:
            file_urls.append(u)
    return image_urls, file_urls


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
    order_single_round: Optional[bool] = None,
    ext: Optional[Dict[str, Any]] = None,
    inquiry_timeout: Optional[int] = None,
    orders_detail: Optional[List[Dict[str, Any]]] = None,
    is_price_negotiation: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    订单询盘主函数，调用 alibaba.1688.newton.order.batch.inquiry 触发询盘。

    Args:
        order_ids: 订单 id 列表
        question: 询盘问题（单个字符串，必填）
        local_images: 本地图片路径列表，采购商品图片说明（可不传，自动上传获取URL）
        image_urls: 图片URL列表，采购商品图片说明（可不传，已有在线链接时使用）
        orders_status: 订单状态 set（可不传）
        order_single_round: 是否单轮对话（三态，原生 bool 或 None）。
            用户明确表达不需要自动回复/不需要多轮对话/不需要 AI 对话/只需要单轮对话时传 True；
            明确表达需要自动回复/需要多轮对话/需要 AI 对话时传 False；
            未提及时传 None（默认，不下发 orderSingleRound 字段）
        ext: 扩展字段 map（可不传），透传给接口的 ext 字段。
            会话上下文会自动从运行时环境变量读取并注入 ext
            （sessionId ← NEWTON_SESSION_ID，chat_id ← NEWTON_REPLY_ID，缺失则不下发）；
            此处显式传入的 ext 优先级更高，会覆盖自动读取的同名字段。
        inquiry_timeout: 询盘超时时间，单位分钟（int，可不传）。
            用户明确表达"设置询盘超时时间为 X 分钟/小时"等意图时，由上层换算为
            正整数分钟传入，会注入 ext["timeout"] 透传给下游接口；未提及则不下发。
            注意：这是业务层的询盘超时（分钟），与 HTTP 请求超时（settings.TOOL_TIMEOUT）无关。
        orders_detail: 按订单维度的附件列表（可不传）。当用户提供按订单维度指定的
            图片或文件时使用。每个元素为 {"order_id": str, "image_urls": list, "file_urls": list}。
            传入时按订单维度循环调用 gateway，返回 wwTaskId 列表。
        is_price_negotiation: 是否改价/议价意图（bool，可不传）。由 workflow 意图解析层
            识别用户意图后传入（改价/议价/目标总价等 → True；催发货/问物流等 → False），
            会注入 ext["isPriceNegotiation"] 透传给下游接口；未提及则不下发。

    Returns:
        不传 orders_detail 时：{"suc": bool, "errorMsg": str, "wwTaskId": str, "elapsed_seconds": float}
        传 orders_detail 时：{"results": list, "elapsed_seconds": float, "success_count": int, "fail_count": int}
    """
    if not order_ids:
        raise ParamError("orderIds 不能为空")

    if not question or not question.strip():
        raise ParamError("question 不能为空")

    # 询盘超时（分钟）：提供时必须为正整数（bool 是 int 子类，需显式排除）
    if inquiry_timeout is not None:
        if isinstance(inquiry_timeout, bool) or not isinstance(inquiry_timeout, int):
            raise ParamError("inquiry_timeout 必须是整数（单位分钟），当前类型 {}".format(type(inquiry_timeout).__name__))
        if inquiry_timeout <= 0:
            raise ParamError("inquiry_timeout 必须为正整数（单位分钟），当前值 {}".format(inquiry_timeout))

    # orders_detail：按订单维度指定附件，每个订单单独调用一次 gateway
    if orders_detail is not None:
        if not isinstance(orders_detail, list) or len(orders_detail) == 0:
            raise ParamError("orders_detail 必须是非空列表")
        for item in orders_detail:
            if not isinstance(item, dict) or "order_id" not in item:
                raise ParamError("orders_detail 每个元素必须包含 order_id 字段")
            if item["order_id"] not in order_ids:
                raise ParamError(
                    "orders_detail 中的 order_id '{}' 不在 order_ids 列表中".format(item["order_id"]))
        return _inquiry_send_by_orders_detail(
            question=question,
            orders_detail=orders_detail,
            orders_status=orders_status,
            order_single_round=order_single_round,
            ext=ext,
            inquiry_timeout=inquiry_timeout,
            is_price_negotiation=is_price_negotiation,
        )

    # 拆分 image_urls：图片扩展名 → imageList；非图片链接 → fileList
    real_image_urls, file_link_urls = _classify_urls(image_urls)

    # 处理图片参数：本地上传 + 图片在线链接 → 统一为 URL 列表
    image_list = _resolve_image_list(local_images, real_image_urls)

    if file_link_urls:
        print("检测到 {} 个非图片链接，放入 fileList 参数".format(len(file_link_urls)), file=sys.stderr)

    # 生成询盘任务 ID，透出到最终输出 JSON 作为本次询盘任务的标识
    ww_task_id = str(uuid.uuid4())

    body: Dict[str, Any] = {
        "orderIds": order_ids,
        "questions": [question],
        "appKey": "newton_api_order_inquiry",
        "imageList": image_list,
        "taskId": ww_task_id,
    }

    # 单轮对话开关为三态：仅当用户明确表达意图（True/False）时才下发；None 表示未提及，不下发
    if order_single_round is not None:
        body["orderSingleRound"] = order_single_round

    # 扩展字段 ext（map）：以运行时环境注入的会话上下文（sessionId / chat_id）为基底，
    # 显式传入的 ext 优先级更高（覆盖同名字段）。合并后非空才下发。
    merged_ext: Dict[str, Any] = _collect_runtime_ext()
    if ext:
        merged_ext.update(ext)
    # 询盘超时（分钟）：专用参数，优先级最高，注入 ext["timeout"]（int）
    if inquiry_timeout is not None:
        merged_ext["timeout"] = inquiry_timeout
    # 改价/议价意图标识：注入 ext["isPriceNegotiation"]（bool）
    if is_price_negotiation is not None:
        merged_ext["isPriceNegotiation"] = is_price_negotiation
    if merged_ext:
        body["ext"] = merged_ext

    # 非图片链接（如 .xls/.pdf/.doc）作为独立参数 fileList 传给接口（str 列表，支持多个）
    if file_link_urls:
        body["fileList"] = file_link_urls

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
        "wwTaskId": ww_task_id,
        "elapsed_seconds": elapsed,
    }


def _inquiry_send_by_orders_detail(
    question: str,
    orders_detail: List[Dict[str, Any]],
    orders_status: Optional[List[str]] = None,
    order_single_round: Optional[bool] = None,
    ext: Optional[Dict[str, Any]] = None,
    inquiry_timeout: Optional[int] = None,
    is_price_negotiation: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    按订单维度循环调用 inquiry_send，每个订单单独发一次 gateway 请求。

    每个订单的附件（image_urls / file_urls）独立，互不影响。

    Returns:
        {"results": list, "elapsed_seconds": float, "success_count": int, "fail_count": int}
    """
    # 入参（非空、元素含 order_id、order_id ∈ order_ids）已由调用方 inquiry_send 校验，此处不重复

    start_time = time.time()
    results = []
    success_count = 0
    fail_count = 0

    for detail in orders_detail:
        oid = detail["order_id"]
        detail_image_urls = detail.get("image_urls") or None
        detail_file_urls = detail.get("file_urls") or None

        try:
            # 每个订单单独调用 inquiry_send（不传 orders_detail 避免递归）。
            # image_urls + file_urls 合并后传入，_classify_urls 会按扩展名
            # 自动分流：图片 → imageList，非图片 → fileList。
            all_urls = []
            if detail_image_urls:
                all_urls.extend(detail_image_urls)
            if detail_file_urls:
                all_urls.extend(detail_file_urls)
            result = inquiry_send(
                order_ids=[oid],
                question=question,
                image_urls=all_urls if all_urls else None,
                orders_status=orders_status,
                order_single_round=order_single_round,
                ext=ext,
                inquiry_timeout=inquiry_timeout,
                is_price_negotiation=is_price_negotiation,
            )
            results.append({
                "order_id": oid,
                "wwTaskId": result.get("wwTaskId", ""),
                "suc": True,
                "errorMsg": "",
                "elapsed_seconds": result.get("elapsed_seconds", 0),
            })
            success_count += 1
        except Exception as e:
            results.append({
                "order_id": oid,
                "wwTaskId": "",
                "suc": False,
                "errorMsg": str(e),
                "elapsed_seconds": 0,
            })
            fail_count += 1

    elapsed = round(time.time() - start_time, 1)

    if success_count == 0 and fail_count > 0:
        raise ServiceError("所有订单询盘均失败，共 {} 个订单".format(fail_count))

    return {
        "results": results,
        "elapsed_seconds": elapsed,
        "success_count": success_count,
        "fail_count": fail_count,
    }
