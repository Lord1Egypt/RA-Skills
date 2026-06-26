#!/usr/bin/env python3
"""图片优化（AI 生图）— service"""

import os
import sys
import time
import json

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post, parse_data_field
from _errors import ServiceError
from biz.const import (
    API_IMAGE_OPTIMIZE,
    API_IMAGE_STATUS,
    DEFAULT_USER_ID,
    POLL_INTERVAL_SECONDS,
    POLL_MAX_SECONDS,
)


def submit_image_optimize(image_urls: str, prompt: str, size: str = "", offer_id: str = "") -> str:
    """
    提交图片优化任务

    Args:
        image_urls: 图片 URL 列表，英文逗号分隔
        prompt:     用户提文（原封不动传入）
        size:       输出比例（可选），如 1:1 / 2:3 / 9:16
        offer_id:   商品 ID（可选）

    Returns:
        instance_id: 异步任务实例 ID
    """
    body = {
        "__userId__": DEFAULT_USER_ID,
        "image_urls": image_urls,
        "prompt": prompt,
    }
    if size:
        body["size"] = size
    if offer_id:
        body["offer_id"] = str(offer_id)

    result = api_post(API_IMAGE_OPTIMIZE, body)
    # result 格式: {"data": {"output": "instance_id"}, "__success__": true}
    if isinstance(result, dict):
        data = result.get("data", {})
        if isinstance(data, dict):
            instance_id = data.get("output", "")
        elif isinstance(data, str):
            # 如果 data 是字符串，尝试解析
            try:
                inner = json.loads(data)
                instance_id = inner.get("output", "") if isinstance(inner, dict) else ""
            except (json.JSONDecodeError, TypeError):
                instance_id = ""
        else:
            instance_id = ""
    else:
        raise ServiceError(f"提交图片优化返回格式异常：{result}")

    if not instance_id:
        raise ServiceError("提交图片优化未返回任务 ID")

    return instance_id


def poll_image_status(instance_id: str) -> dict:
    """
    查询图片优化结果（单次查询）

    Args:
        instance_id: 异步任务实例 ID

    Returns:
        API 返回的完整结果 dict
    """
    body = {
        "__userId__": DEFAULT_USER_ID,
        "instance_id": instance_id,
    }

    result = api_post(API_IMAGE_STATUS, body)
    # api_post 返回格式: {"data": {...status...}, "__success__": true}
    # 或嵌套: {"data": {"data": {...status...}}}
    # 通过 "status" 字段定位真正的状态数据
    if not isinstance(result, dict):
        return {}

    # 优先在 result["data"] 里找
    data = result.get("data", {})
    if isinstance(data, dict):
        # 如果 data 里直接有 status 字段，说明 data 就是状态数据
        if "status" in data:
            return data
        # 否则检查 data["data"]（双层嵌套）
        inner = data.get("data", {})
        if isinstance(inner, dict) and "status" in inner:
            return inner

    # 兜底：result 本身有 status
    if "status" in result:
        return result

    return {}


def submit_and_wait(image_urls: str, prompt: str, size: str = "", offer_id: str = "") -> dict:
    """
    提交图片优化并轮询等待结果

    每 10 秒查询一次，最长等待 3 分钟。

    Returns:
        {
            "instance_id": "xxx",
            "gen_image_url": "xxx",
            "reasoning_context": "xxx",
            "status": "finished",
            "time_cost": "xx.xx",
            "raw_output": {...}
        }
    """
    instance_id = submit_image_optimize(image_urls, prompt, size, offer_id)

    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed >= POLL_MAX_SECONDS:
            raise ServiceError(
                f"图片优化轮询超时（已等待 {int(elapsed)} 秒），任务 ID：{instance_id}。"
                f"可稍后使用任务 ID 查询结果。"
            )

        time.sleep(POLL_INTERVAL_SECONDS)

        status_data = poll_image_status(instance_id)
        status = status_data.get("status", "")

        if status == "finished":
            raw_output = status_data.get("rawOutput", {})
            return {
                "instance_id": instance_id,
                "gen_image_url": raw_output.get("gen_image_url", ""),
                "reasoning_context": raw_output.get("reasoning_context", ""),
                "status": "finished",
                "time_cost": status_data.get("timeCost", ""),
                "raw_output": raw_output,
            }

        if status in ("failed", "error"):
            raw_output = status_data.get("rawOutput", {})
            reason = raw_output.get("reasoning_context", "") or status_data.get("message", "未知错误")
            raise ServiceError(f"图片优化失败：{reason}")

        # 其他状态（processing/pending 等）继续轮询
