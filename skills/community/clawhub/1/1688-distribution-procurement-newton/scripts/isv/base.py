#!/usr/bin/env python3
"""
ISV Provider 基类与全局注册表。

每个 ISV 服务商实现一个 Provider 子类并注册到全局注册表中。
业务层通过 appKey 查找 Provider，调用其 CLI 执行采购相关能力。

参考 1688-distribution-distribute-offer-newton 的 ISV 架构设计。
"""

import base64
import hashlib
import hmac
import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests

# ---------------------------------------------------------------------------
# 全局注册表
# ---------------------------------------------------------------------------

_PROVIDER_REGISTRY: Dict[str, "ISVProvider"] = {}
_APPKEY_TO_PROVIDER: Dict[str, "ISVProvider"] = {}


def register_provider(provider: "ISVProvider"):
    """注册一个 ISV Provider 实例到全局注册表。"""
    _PROVIDER_REGISTRY[provider.name] = provider
    for key in provider.app_keys:
        _APPKEY_TO_PROVIDER[key] = provider


def get_provider_by_appkey(app_key: str) -> Optional["ISVProvider"]:
    """根据 appKey 查找已注册的 ISV Provider。"""
    return _APPKEY_TO_PROVIDER.get(app_key)


def get_provider_by_name(name: str) -> Optional["ISVProvider"]:
    """根据 provider 名称查找已注册的 ISV Provider。"""
    return _PROVIDER_REGISTRY.get(name)


def get_all_providers() -> Dict[str, "ISVProvider"]:
    """返回所有已注册的 ISV Provider（name -> provider）。"""
    return dict(_PROVIDER_REGISTRY)


def find_provider_for_tools(tool_list: list) -> Optional[Dict[str, Any]]:
    """
    从 toolList 中查找匹配的 ISV Provider。

    遍历所有工具的 appKey，返回第一个有对应 Provider 的匹配结果。

    :param tool_list: shop_and_tool_info 返回的 toolList
    :return: {"provider": ISVProvider, "app_key": str, "app_name": str} 或 None
    """
    for tool in tool_list:
        app_key = tool.get("appKey", "")
        if not app_key:
            continue
        provider = get_provider_by_appkey(app_key)
        if provider is not None:
            return {
                "provider": provider,
                "app_key": app_key,
                "app_name": tool.get("appName", ""),
            }
    return None


# ---------------------------------------------------------------------------
# ISV API 客户端基类
# ---------------------------------------------------------------------------

class ISVApiClient:
    """ISV 中台 API 客户端，封装签名和 HTTP 请求。"""

    def __init__(
        self,
        token: str,
        platform: str = "taobao",
        base_url: str = "",
        client_id: str = "",
        client_secret: str = "",
    ):
        self.token = token
        self.platform = platform
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()

    def _build_auth_headers(self, method: str, request_url: str) -> Dict[str, str]:
        """构建 Inner-Auth 签名请求头。"""
        if not self.token:
            raise ValueError("jwt_token 不能为空")

        timestamp = str(int(time.time() * 1000))
        nonce = base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8").rstrip("=")
        path = urlparse(request_url).path
        body_hash = ""
        sign_base = f"{method}\n{path}\n{timestamp}\n{nonce}\n{body_hash}"
        signature = base64.b64encode(
            hmac.new(
                self.client_secret.encode("utf-8"),
                sign_base.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        ).decode("utf-8")

        return {
            "Content-Type": "application/json",
            "X-Client-Id": self.client_id,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Sign": signature,
            "httpAuthorization": f"Bearer {self.token}",
        }

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """发送 GET 请求到 ISV 中台。"""
        url = f"{self.base_url}{path}"
        headers = self._build_auth_headers("GET", url)
        response = self.session.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def post(
        self,
        path: str,
        payload: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """发送 POST 请求到 ISV 中台。"""
        url = f"{self.base_url}{path}"
        headers = self._build_auth_headers("POST", url)
        response = self.session.post(
            url, params=params, json=payload, headers=headers, timeout=30
        )
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# ISV Provider 基类
# ---------------------------------------------------------------------------

class ISVProvider:
    """
    ISV 采购服务商基类。

    每个 ISV 继承此类，实现各能力方法，并在模块加载时调用 register_provider() 注册。
    ISV 的独立 cli.py 和业务脚本放在 providers/<name>/ 子目录下。
    不支持的能力保持默认实现（返回 not_supported）。
    """

    name: str = ""
    app_keys: List[str] = []
    display_name: str = ""
    api_base: str = ""
    platform_credentials: Dict[str, Dict[str, str]] = {}

    @property
    def provider_dir(self) -> str:
        """当前 Provider 的目录路径（providers/<name>/）。"""
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "providers", self.name)

    @property
    def cli_path(self) -> str:
        """当前 Provider 的 cli.py 路径。"""
        return os.path.join(self.provider_dir, "cli.py")

    def get_credential(self, platform: str) -> Dict[str, str]:
        """获取指定平台的认证凭证（client_id, client_secret）。"""
        platform_lower = (platform or "").strip().lower()
        credential = self.platform_credentials.get(platform_lower)
        if not credential:
            raise ValueError(
                f"ISV [{self.display_name}] 不支持平台: {platform}，"
                f"仅支持: {', '.join(self.platform_credentials.keys())}"
            )
        return credential

    def create_client(self, token: str, platform: str = "taobao") -> ISVApiClient:
        """创建该 ISV 的 API 客户端。"""
        credential = self.get_credential(platform)
        return ISVApiClient(
            token=token,
            platform=platform,
            base_url=self.api_base,
            client_id=credential["client_id"],
            client_secret=credential["client_secret"],
        )

    def run_cli(self, command: str, token: str, extra_args: List[str] = None) -> Dict[str, Any]:
        """
        调用该 ISV 的 cli.py 命令。

        :param command: 子命令（如 list-shops, confirm-link 等）
        :param token: ISV Token
        :param extra_args: 额外参数列表
        :return: 解析后的 JSON 响应
        :raises RuntimeError: 调用失败时抛出异常
        """
        if not os.path.isfile(self.cli_path):
            raise RuntimeError(f"ISV [{self.display_name}] 的 cli.py 不存在: {self.cli_path}")

        cmd = [sys.executable, self.cli_path, command, "--token", token]
        if extra_args:
            cmd.extend(extra_args)

        try:
            result = subprocess.run(
                cmd,
                cwd=self.provider_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"ISV [{self.display_name}] 命令 {command} 调用超时")
        except Exception as exc:
            raise RuntimeError(f"ISV [{self.display_name}] 命令 {command} 调用异常: {exc}")

        if result.returncode != 0:
            stderr = result.stderr.strip() if result.stderr else ""
            raise RuntimeError(f"ISV [{self.display_name}] 命令 {command} 执行失败: {stderr}")

        stdout = result.stdout.strip()
        if not stdout:
            return {}

        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {"raw_output": stdout}

    @staticmethod
    def _not_supported(capability_name: str) -> Dict[str, Any]:
        return {
            "success": False,
            "message": f"当前 ISV 不支持 [{capability_name}] 能力",
        }

    # ---- 采购能力（淘宝） ----

    def list_shops(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """查询绑定店铺列表。"""
        return self._not_supported("查询店铺")

    def list_distributors(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """查询分销账号列表。"""
        return self._not_supported("查询分销账号")

    def list_products(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """查询店铺在售商品。"""
        return self._not_supported("查询商品")

    def enable_link_type(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """开启分销宝贝开关。"""
        return self._not_supported("开启分销开关")

    def enable_auto_order(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """保存自动下单配置。"""
        return self._not_supported("自动下单")

    def list_after_sale_accounts(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """查询售后采购账号列表。"""
        return self._not_supported("售后账号查询")

    def enable_auto_after_sale(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """保存售后规则。"""
        return self._not_supported("售后规则")

    def link_preview(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """SKU 匹配预览。"""
        return self._not_supported("SKU 预览")

    def confirm_link(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """确认并保存 SKU 映射。"""
        return self._not_supported("确认关联")

    def link_source(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """分销关系关联。"""
        return self._not_supported("分销关联")

    def query_settings(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """查询采购设置。"""
        return self._not_supported("采购设置")

    # ---- 采购能力（抖音） ----

    def douyin_list_shops(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：查询绑定店铺列表。"""
        return self._not_supported("抖音-查询店铺")

    def douyin_list_distributors(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：查询分销账号列表。"""
        return self._not_supported("抖音-查询分销账号")

    def douyin_list_products(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：查询店铺在售商品。"""
        return self._not_supported("抖音-查询商品")

    def douyin_enable_link_type(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：开启分销商品开关。"""
        return self._not_supported("抖音-开启分销开关")

    def douyin_enable_auto_order(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：保存自动下单配置。"""
        return self._not_supported("抖音-自动下单")

    def douyin_list_after_sale_accounts(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：查询售后采购账号列表。"""
        return self._not_supported("抖音-售后账号查询")

    def douyin_enable_auto_after_sale(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：保存售后规则。"""
        return self._not_supported("抖音-售后规则")

    def douyin_link_preview(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：SKU 匹配预览。"""
        return self._not_supported("抖音-SKU 预览")

    def douyin_confirm_link(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：确认并保存 SKU 映射。"""
        return self._not_supported("抖音-确认关联")

    def douyin_link_source(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：分销关系关联。"""
        return self._not_supported("抖音-分销关联")

    def douyin_query_settings(self, client: ISVApiClient, **kwargs) -> Dict[str, Any]:
        """抖音：查询采购设置。"""
        return self._not_supported("抖音-采购设置")
