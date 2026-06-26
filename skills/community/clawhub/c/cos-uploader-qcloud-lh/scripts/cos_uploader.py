#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COS 上传核心模块
- 使用腾讯云 COS Python SDK
- 通过内网/外网域名上传（根据配置自动选择）
- 设置存储类型（根据配置自动选择）
"""

import os
import random
import string
import logging
from datetime import datetime
from qcloud_cos import CosConfig, CosS3Client

from config import load_cos_config

logger = logging.getLogger(__name__)


def _init_cos_client():
    """
    初始化 COS 客户端（从加密配置中读取所有参数）

    Returns:
        tuple: (CosS3Client, config_data)
    """
    config_data = load_cos_config()
    use_internal = config_data.get("use_internal", True)

    cos_config = CosConfig(
        Region=config_data["region"],
        SecretId=config_data["secret_id"],
        SecretKey=config_data["secret_key"],
        Scheme='https',
        EnableInternalDomain=use_internal,  # SDK 自动处理内网/外网域名
    )
    return CosS3Client(cos_config), config_data


def _generate_cos_key(original_filename):
    """
    生成 COS 存储路径
    规则：按年月创建文件夹，按月日+随机数修改文件名

    示例：2026/03/0326_a3f8b2.jpg

    Args:
        original_filename: 原始文件名（如 IMG2762---36d2d101-xxx.jpg）

    Returns:
        str: COS 对象键（如 2026/03/0326_a3f8b2.jpg）
    """
    now = datetime.now()

    # 获取文件扩展名
    _, ext = os.path.splitext(original_filename)
    if not ext:
        ext = ".jpg"  # 默认扩展名

    # 年月文件夹
    year_month = now.strftime("%Y/%m")

    # 月日 + 6位随机字符串作为文件名
    month_day = now.strftime("%m%d")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    filename = f"{month_day}_{random_str}{ext}"

    # 最终路径
    cos_key = f"{year_month}/{filename}"
    return cos_key


def upload_file_to_cos(local_file_path):
    """
    将本地文件上传到 COS（根据加密配置自动选择内网/外网、存储类型）

    Args:
        local_file_path: 本地文件绝对路径

    Returns:
        dict: 上传结果，包含以下字段：
            - success (bool): 是否成功
            - cos_key (str): COS 对象键
            - etag (str): 文件 ETag
            - file_size (int): 文件大小（字节）
            - error (str): 错误信息（仅失败时）
    """
    if not os.path.exists(local_file_path):
        return {
            "success": False,
            "error": f"文件不存在: {local_file_path}"
        }

    original_filename = os.path.basename(local_file_path)
    cos_key = _generate_cos_key(original_filename)

    try:
        client, config_data = _init_cos_client()
        bucket = config_data["bucket"]
        storage_class = config_data.get("storage_class", "STANDARD_IA")

        # 获取文件大小，决定上传方式
        file_size = os.path.getsize(local_file_path)

        if file_size <= 20 * 1024 * 1024:  # 20MB 以下使用简单上传
            with open(local_file_path, 'rb') as fp:
                response = client.put_object(
                    Bucket=bucket,
                    Body=fp,
                    Key=cos_key,
                    StorageClass=storage_class,
                    ContentType=_get_content_type(original_filename),
                )
        else:
            # 大文件使用分块上传
            response = client.upload_file(
                Bucket=bucket,
                LocalFilePath=local_file_path,
                Key=cos_key,
                StorageClass=storage_class,
                PartSize=10,       # 分块大小 10MB
                MAXThread=5,       # 最大并发线程数
                ContentType=_get_content_type(original_filename),
            )

        etag = response.get('ETag', '').strip('"')

        return {
            "success": True,
            "cos_key": cos_key,
            "etag": etag,
            "file_size": file_size,
            "storage_class": storage_class,
        }

    except Exception as e:
        # 脱敏处理：不将完整异常信息暴露给用户，仅记录到日志
        logger.error(f"COS 上传异常: {e}")
        # 返回给用户的错误信息不包含敏感细节
        error_msg = "上传过程中发生错误，请检查网络连接和 COS 配置"
        if "NoSuchBucket" in str(e):
            error_msg = "COS 桶不存在，请检查配置"
        elif "AccessDenied" in str(e):
            error_msg = "COS 访问被拒绝，请检查密钥权限"
        elif "ConnectTimeout" in str(e) or "ConnectionError" in str(e):
            error_msg = "无法连接 COS 服务，请检查内网连通性"
        return {
            "success": False,
            "cos_key": cos_key,
            "error": error_msg,
        }


def _get_content_type(filename):
    """
    根据文件扩展名获取 Content-Type

    Args:
        filename: 文件名

    Returns:
        str: MIME 类型
    """
    ext = os.path.splitext(filename)[1].lower()
    content_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".heif": "image/heif",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
    }
    return content_type_map.get(ext, "application/octet-stream")
