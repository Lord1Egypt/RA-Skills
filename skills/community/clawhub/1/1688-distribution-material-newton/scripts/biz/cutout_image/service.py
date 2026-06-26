#!/usr/bin/env python3
"""抠图（生成白底图）— service"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post, parse_data_field
from _errors import ServiceError
from biz.const import API_CUTOUT_IMAGE, DEFAULT_USER_ID


def cutout_image(image_url: str, prompt: str) -> dict:
    """
    抠图（生成白底图）

    Args:
        image_url: 单张图片 URL
        prompt:    用户提文（原封不动传入）

    Returns:
        {
            "white_img": "白底图 URL（原始尺寸）",
            "white_img_cropped": "白底裁剪图 URL（紧凑裁剪）",
            "mask_img": "蒙版图 URL",
        }
    """
    body = {
        "__userId__": DEFAULT_USER_ID,
        "image_url": image_url,
        "prompt": prompt,
    }

    result = api_post(API_CUTOUT_IMAGE, body)

    # result 格式: {"data": "{\"mask_img\":\"...\",\"white_img\":\"...\",\"white_img_cropped\":\"...\"}", "__success__": true}
    if isinstance(result, dict):
        data = result.get("data", {})
        if isinstance(data, dict):
            return {
                "white_img": data.get("white_img", ""),
                "white_img_cropped": data.get("white_img_cropped", ""),
                "mask_img": data.get("mask_img", ""),
            }
        # data 已经是解析后的顶层 result
        if "white_img" in result:
            return {
                "white_img": result.get("white_img", ""),
                "white_img_cropped": result.get("white_img_cropped", ""),
                "mask_img": result.get("mask_img", ""),
            }

    raise ServiceError(f"抠图返回格式异常：{result}")
