# -*- coding: utf-8 -*-
"""
纵横图片上传工具

将本地图片 Base64 编码后批量上传到纵横平台，返回图片 URL 列表。
供截图搜品等流程内部调用。

API 参数：imageBytesStrList (List[str])
API 返回：List[str] (URL 列表)
"""

import base64
import os
import sys
from typing import List

from _http import api_post
from _errors import ParamError, ServiceError
from settings import settings


def upload_images(image_paths: List[str]) -> List[str]:
    """
    批量上传本地图片到纵横平台

    Args:
        image_paths: 本地图片文件绝对路径列表

    Returns:
        纵横平台图片 URL 列表（与输入顺序对应）
    """
    if not image_paths:
        raise ParamError("图片路径列表不能为空")

    image_bytes_str_list = []
    for image_path in image_paths:
        image_path = image_path.strip()
        if not image_path:
            continue
        if not os.path.exists(image_path):
            raise ParamError("图片文件不存在: {}".format(image_path))

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        if not image_bytes:
            raise ParamError("图片文件为空: {}".format(image_path))

        image_bytes_str_list.append(base64.b64encode(image_bytes).decode("utf-8"))
        print("图片编码完成: {} ({:.1f} KB)".format(
            os.path.basename(image_path), len(image_bytes) / 1024), file=sys.stderr)

    if not image_bytes_str_list:
        raise ParamError("没有有效的图片文件")

    print("正在上传 {} 张图片...".format(len(image_bytes_str_list)), file=sys.stderr)

    resp = api_post(
        path=settings.IMG_UPLOAD_PATH,
        body={"imageBytesStrList": image_bytes_str_list},
        timeout=settings.IMG_UPLOAD_TIMEOUT,
    )

    # 解析返回的 URL 列表
    url_list = []
    if isinstance(resp, dict):
        data = resp.get("data", [])
        if isinstance(data, list):
            url_list = [item for item in data if isinstance(item, str) and item]
        elif isinstance(data, dict):
            # 兼容 matchResult 为列表的情况
            match_result = data.get("matchResult", [])
            if isinstance(match_result, list):
                url_list = [item for item in match_result if isinstance(item, str) and item]
            elif isinstance(match_result, str) and match_result:
                url_list = [match_result]

    if not url_list:
        raise ServiceError("上传成功但未返回图片 URL: {}".format(resp))

    print("上传完成，获取到 {} 个 URL".format(len(url_list)), file=sys.stderr)
    return url_list
