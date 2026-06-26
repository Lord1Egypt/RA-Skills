#!/usr/bin/env python3
"""
Chaoji API Client - 潮际API客户端
处理签名、请求发送等基础功能
"""
import time
import uuid
import hashlib
import requests
from typing import Dict, Any, Optional


class ChaojiApiClient:
    """潮际API客户端"""

    def __init__(self, app_key: str, access_key_id: str, access_key_secret: str, endpoint: str):
        """
        初始化API客户端

        Args:
            app_key: 应用Key
            access_key_id: Access Key ID
            access_key_secret: Access Key Secret
            endpoint: API端点域名
        """
        self.app_key = app_key
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.endpoint = endpoint
        self.base_url = f"https://{endpoint}/api"
        self.timeout = 8000
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json;charset=utf-8",
            "accessKey": self.access_key_id,
            "appKey": self.app_key,
        })

    def post(self, api_name: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送POST请求

        Args:
            api_name: API名称
            params: 请求参数

        Returns:
            API响应
        """
        headers = {"apiName": api_name}
        request_headers = self._prepare_headers(headers)

        args = self._clean_none({
            "url": self.base_url,
            "headers": request_headers,
            "json": params or {},
            "timeout": self.timeout,
        })

        response = self.session.post(**args)
        self._handle_exception(response)

        try:
            return response.json()
        except ValueError:
            return {"text": response.text}

    def get(self, path: str, api_name: Optional[str] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送GET请求

        Args:
            path: API路径
            api_name: API名称（可选）
            params: 查询参数

        Returns:
            API响应
        """
        url = f"{self.base_url}{path}"
        headers = {}
        if api_name:
            headers["apiName"] = api_name
        request_headers = self._prepare_headers(headers)

        args = self._clean_none({
            "url": url,
            "headers": request_headers,
            "params": params,
            "timeout": self.timeout,
        })

        response = self.session.get(**args)
        self._handle_exception(response)

        try:
            return response.json()
        except ValueError:
            return {"text": response.text}

    def _prepare_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """准备请求头（添加签名）"""
        headers["requestId"] = str(uuid.uuid1())
        timestamp = int(round(time.time() * 1000))
        headers["timestamp"] = str(timestamp)
        headers["sign"] = self._get_sign(timestamp)
        return headers

    def _get_sign(self, timestamp: int) -> str:
        """生成签名"""
        sign_str = f"{self.app_key}{self.access_key_id}{timestamp}{self.access_key_secret}"
        m = hashlib.md5()
        m.update(sign_str.encode("utf-8"))
        return m.hexdigest()

    def _handle_exception(self, response):
        """处理HTTP异常"""
        if response.status_code >= 400:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    def _clean_none(self, d: Dict) -> Dict:
        """清理None值"""
        return {k: v for k, v in d.items() if v is not None}
