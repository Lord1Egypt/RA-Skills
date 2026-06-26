# -*- coding: utf-8 -*-
"""
纵横图片上传工具

将本地图片 Base64 编码后批量上传到纵横平台，返回图片 URL 列表。
供截图搜品等流程内部调用。

API 参数：imageBytesStrList (List[str])
API 返回：List[str] (URL 列表)
"""

import base64
import mimetypes
import os
import sys
import tempfile
from typing import List
from urllib.parse import urlparse

import requests

from _http import api_post
from _errors import ParamError, ServiceError, TimeoutError
from settings import settings


DOWNLOAD_TIMEOUT_SECONDS = 60
DOWNLOAD_CHUNK_SIZE = 64 * 1024


def is_http_url(value: str) -> bool:
    """Return whether a value is an HTTP(S) URL."""
    parsed = urlparse((value or "").strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def _image_suffix_from_response(url: str, resp) -> str:
    """Infer a reasonable temporary file suffix for a downloaded image."""
    path_suffix = os.path.splitext(urlparse(url).path)[1]
    if path_suffix and len(path_suffix) <= 16:
        return path_suffix

    content_type = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    guessed = mimetypes.guess_extension(content_type) if content_type else ""
    return guessed or ".img"


def _download_image_url(url: str, output_dir: str, index: int) -> str:
    """Download one remote image URL to a temporary local file."""
    clean_url = (url or "").strip()
    if not is_http_url(clean_url):
        raise ParamError("图片 URL 不合法: {}".format(clean_url))

    print("正在下载图片 URL: {}".format(clean_url), file=sys.stderr)
    resp = None
    try:
        resp = requests.get(clean_url, stream=True, timeout=DOWNLOAD_TIMEOUT_SECONDS)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        raise TimeoutError("下载图片超时: {}".format(clean_url))
    except requests.exceptions.RequestException as e:
        if resp is not None:
            resp.close()
        raise ServiceError("下载图片失败: {} ({})".format(clean_url, e))

    try:
        suffix = _image_suffix_from_response(clean_url, resp)
        local_path = os.path.join(output_dir, "remote_image_{}{}".format(index, suffix))
        total_bytes = 0
        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                if not chunk:
                    continue
                f.write(chunk)
                total_bytes += len(chunk)
    finally:
        resp.close()

    if total_bytes <= 0:
        raise ParamError("下载图片为空: {}".format(clean_url))

    print("图片下载完成: {} ({:.1f} KB)".format(
        os.path.basename(local_path), total_bytes / 1024), file=sys.stderr)
    return local_path


def upload_image_urls(image_urls: List[str]) -> List[str]:
    """
    下载远程图片 URL 到本地临时文件，再上传到纵横平台。

    Args:
        image_urls: HTTP(S) 图片 URL 列表

    Returns:
        纵横平台图片 URL 列表（与输入顺序对应）
    """
    clean_urls = [url.strip() for url in image_urls or [] if url and url.strip()]
    if not clean_urls:
        raise ParamError("图片 URL 列表不能为空")

    with tempfile.TemporaryDirectory(prefix="1688_procurement_img_") as tmp_dir:
        local_paths = [
            _download_image_url(url, tmp_dir, index)
            for index, url in enumerate(clean_urls, start=1)
        ]
        return upload_images(local_paths)


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
