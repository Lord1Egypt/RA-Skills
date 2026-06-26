"""
百度内容审核 API 客户端
提供文本审核和图像审核功能
"""

import os
import json
import base64
import time
import requests
from typing import Optional, Union


# API 地址
TEXT_CENSOR_URL = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
IMG_CENSOR_URL = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"

# Token 缓存文件路径
TOKEN_CACHE_FILE = os.path.expanduser("~/.claude/skills/baidu-content-censor/token_cache.json")


def get_ak_sk() -> tuple:
    """
    获取 AK 和 SK
    从环境变量 BCE_SINAN_AK 和 BCE_SINAN_SK 读取
    """
    ak = os.environ.get("BCE_SINAN_AK")
    sk = os.environ.get("BCE_SINAN_SK")

    if not ak:
        raise ValueError("未设置环境变量 BCE_SINAN_AK，请先设置后再调用审核接口")
    if not sk:
        raise ValueError("未设置环境变量 BCE_SINAN_SK，请先设置后再调用审核接口")

    return ak, sk


def load_token_cache() -> Optional[dict]:
    """从缓存文件加载 token"""
    if os.path.exists(TOKEN_CACHE_FILE):
        try:
            with open(TOKEN_CACHE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def save_token_cache(token_data: dict) -> None:
    """保存 token 到缓存文件"""
    cache_dir = os.path.dirname(TOKEN_CACHE_FILE)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    with open(TOKEN_CACHE_FILE, "w") as f:
        json.dump(token_data, f)


def get_access_token() -> str:
    """
    获取 access_token
    优先从缓存加载，若缓存无效则重新获取
    """
    # 尝试从缓存加载
    cache = load_token_cache()
    if cache:
        expires_at = cache.get("expires_at", 0)
        # 提前 5 分钟判断为过期，避免边界问题
        if time.time() < expires_at - 300:
            return cache.get("access_token")

    # 缓存无效，重新获取
    ak, sk = get_ak_sk()

    url = f"{TOKEN_URL}?grant_type=client_credentials&client_id={ak}&client_secret={sk}"

    response = requests.post(url)
    result = response.json()

    if "access_token" in result:
        # 计算过期时间
        expires_in = result.get("expires_in", 2592000)  # 默认 30 天
        expires_at = time.time() + expires_in

        token_data = {
            "access_token": result["access_token"],
            "expires_in": expires_in,
            "expires_at": expires_at
        }
        save_token_cache(token_data)

        return result["access_token"]
    else:
        raise ValueError(f"获取 access_token 失败: {result}")


def refresh_access_token() -> str:
    """强制刷新 access_token"""
    ak, sk = get_ak_sk()

    url = f"{TOKEN_URL}?grant_type=client_credentials&client_id={ak}&client_secret={sk}"

    response = requests.post(url)
    result = response.json()

    if "access_token" in result:
        expires_in = result.get("expires_in", 2592000)
        expires_at = time.time() + expires_in

        token_data = {
            "access_token": result["access_token"],
            "expires_in": expires_in,
            "expires_at": expires_at
        }
        save_token_cache(token_data)

        return result["access_token"]
    else:
        raise ValueError(f"获取 access_token 失败: {result}")


def text_censor(text: str, appid: Optional[int] = None, skip_cache: bool = False) -> dict:
    """
    文本审核接口

    Args:
        text: 待审核的文本内容
        appid: 可选的应用ID
        skip_cache: 是否跳过缓存，强制刷新 token

    Returns:
        dict: 审核结果的 JSON 响应
    """
    global _last_access_token

    access_token = get_access_token()

    # 检查返回的 error_code 是否为 110/111（access_token 无效或过期）
    _last_access_token = access_token

    url = f"{TEXT_CENSOR_URL}?access_token={access_token}"

    data = {"text": text, "isFromSkill": "true"}
    if appid:
        data["appid"] = appid

    response = requests.post(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    result = response.json()

    # 如果返回 110 或 111，强制刷新 token 并重试
    if result.get("error_code") in [110, 111]:
        if skip_cache:
            raise ValueError(f"Access token 无效: {result}")
        access_token = refresh_access_token()
        _last_access_token = access_token
        url = f"{TEXT_CENSOR_URL}?access_token={access_token}"
        response = requests.post(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        result = response.json()

    return result


def image_censor(
    image: Optional[str] = None,
    img_url: Optional[str] = None,
    appid: Optional[int] = None,
    skip_cache: bool = False
) -> dict:
    """
    图像审核接口

    Args:
        image: 待审核图片的 Base64 编码（与 img_url 二选一）
        img_url: 待审核图片的 URL（与 image 二选一）
        appid: 可选的应用ID
        skip_cache: 是否跳过缓存，强制刷新 token

    Returns:
        dict: 审核结果的 JSON 响应
    """
    global _last_access_token

    access_token = get_access_token()
    _last_access_token = access_token

    url = f"{IMG_CENSOR_URL}?access_token={access_token}"

    if not image and not img_url:
        raise ValueError("必须提供 image 或 img_url 参数之一")

    if image and img_url:
        raise ValueError("image 和 img_url 不能同时提供")

    data = {"isFromSkill": "true"}
    if image:
        # 检查是否为文件路径，如果是则读取并转换为 Base64
        if os.path.isfile(image):
            with open(image, "rb") as f:
                image = base64.b64encode(f.read()).decode("utf-8")
        data["image"] = image
    elif img_url:
        data["imgUrl"] = img_url

    if appid:
        data["appid"] = appid

    response = requests.post(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    result = response.json()

    # 如果返回 110 或 111，强制刷新 token 并重试
    if result.get("error_code") in [110, 111]:
        if skip_cache:
            raise ValueError(f"Access token 无效: {result}")
        access_token = refresh_access_token()
        _last_access_token = access_token
        url = f"{IMG_CENSOR_URL}?access_token={access_token}"
        response = requests.post(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        result = response.json()

    return result


def censor(content: Union[str, dict], content_type: Optional[str] = None, **kwargs) -> dict:
    """
    通用审核接口，自动识别内容类型

    Args:
        content: 待审核的内容（文本字符串或图片路径/URL）
        content_type: 可指定内容类型，"text" 或 "image"
        **kwargs: 其他参数，如 appid

    Returns:
        dict: 审核结果的 JSON 响应
    """
    # 自动识别内容类型
    if content_type is None:
        # 如果是文件路径或 URL，判定为图片
        if content.startswith("http://") or content.startswith("https://"):
            content_type = "image"
        elif os.path.isfile(content):
            content_type = "image"
        else:
            content_type = "text"

    if content_type == "text":
        return text_censor(text=content, **kwargs)
    elif content_type == "image":
        # 尝试作为 URL 或 Base64 处理
        if content.startswith("http://") or content.startswith("https://"):
            return image_censor(img_url=content, **kwargs)
        else:
            return image_censor(image=content, **kwargs)
    else:
        raise ValueError(f"不支持的内容类型: {content_type}")


# 用于跟踪最后一次使用的 token
_last_access_token = None