#!/usr/bin/env python3
"""
Chaoji OSS - 潮际OSS上传模块
处理文件上传到阿里云OSS
"""
import os
import time
import requests
from typing import Dict, Any, Optional

try:
    from chaoji_client import ChaojiApiClient
except ImportError:
    from .chaoji_client import ChaojiApiClient


APP_KEY = "marketing-server"
ENDPOINT = "open.metac-inc.com"


class ChaojiOssUploader:
    """潮际OSS文件上传器"""

    def __init__(self, access_key_id: str, access_key_secret: str):
        """
        初始化OSS上传器

        Args:
            access_key_id: CHAOJI Access Key
            access_key_secret: CHAOJI Secret Key
        """
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.client = ChaojiApiClient(APP_KEY, access_key_id, access_key_secret, ENDPOINT)
        self._oss_info = None

    def _get_oss_secret_info(self, file_type: str = "1") -> Dict[str, Any]:
        """
        获取OSS签名信息

        Args:
            file_type: 文件类型，1=图片

        Returns:
            OSS签名信息
        """
        headers = {"apiName": "marketing_oss_get_oss_secret_info_fileType"}
        params = {"fileType": file_type}
        return self.client.get("", api_name="marketing_oss_get_oss_secret_info_fileType", params=params)

    def upload_file(self, file_path: str, custom_filename: Optional[str] = None, file_type: str = "1") -> Dict[str, Any]:
        """
        上传文件到OSS

        Args:
            file_path: 本地文件路径
            custom_filename: 自定义文件名（可选）
            file_type: 文件类型，1=图片

        Returns:
            上传结果，包含url、key、filename
        """
        # 获取OSS签名
        response = self._get_oss_secret_info(file_type)
        if response.get("code") != 2000:
            return {
                "success": False,
                "error": f"获取OSS签名失败: {response.get('message')}"
            }

        oss_info = response.get("data", {})

        # 检查签名是否过期
        current_time = int(time.time() * 1000)
        expire = oss_info.get("expire", 0)
        if current_time > expire:
            return {
                "success": False,
                "error": "签名已过期"
            }

        # 准备文件名
        filename = custom_filename or os.path.basename(file_path)
        oss_key = oss_info.get("dir", "") + filename

        # 构造表单数据
        form_data = {
            "key": oss_key,
            "OSSAccessKeyId": oss_info.get("accessid"),
            "policy": oss_info.get("policy"),
            "Signature": oss_info.get("signature"),
            "success_action_status": "200",
        }

        # 上传文件
        try:
            with open(file_path, "rb") as f:
                files = {"file": (filename, f)}
                host = oss_info.get("host", "").strip()
                response = requests.post(host, data=form_data, files=files, timeout=300)

            if response.status_code == 200:
                file_url = f"{host}/{oss_key}"
                return {
                    "success": True,
                    "url": file_url,
                    "key": oss_key,
                    "filename": filename
                }
            else:
                return {
                    "success": False,
                    "error": f"上传失败，HTTP {response.status_code}",
                    "response": response.text
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"上传异常: {str(e)}"
            }

    def upload_image(self, file_path: str, custom_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        上传图片到OSS（file_type=1）

        Args:
            file_path: 本地文件路径
            custom_filename: 自定义文件名（可选）

        Returns:
            上传结果
        """
        return self.upload_file(file_path, custom_filename, file_type="1")


def upload_image_to_oss(file_path: str,
                        access_key_id: Optional[str] = None,
                        access_key_secret: Optional[str] = None,
                        custom_filename: Optional[str] = None) -> Dict[str, Any]:
    """
    便捷函数：上传图片到OSS

    Args:
        file_path: 本地文件路径
        access_key_id: CHAOJI AK，默认从环境变量CHAOJI_AK获取
        access_key_secret: CHAOJI SK，默认从环境变量CHAOJI_SK获取
        custom_filename: 自定义文件名

    Returns:
        上传结果字典
    """
    ak = access_key_id or os.environ.get("CHAOJI_AK")
    sk = access_key_secret or os.environ.get("CHAOJI_SK")

    if not ak or not sk:
        return {
            "success": False,
            "error": "未配置CHAOJI_AK或CHAOJI_SK环境变量"
        }

    uploader = ChaojiOssUploader(ak, sk)
    return uploader.upload_image(file_path, custom_filename)


def extract_oss_path(url: str) -> str:
    """
    从URL中提取OSS Path

    Args:
        url: 完整URL

    Returns:
        OSS Path（如 marketing/image/xxx/xxx.jpg）
    """
    if ".com/" in url:
        return url.split(".com/", 1)[1]
    elif ".aliyuncs.com/" in url:
        return url.split(".aliyuncs.com/", 1)[1]
    return url
