#!/usr/bin/env python3
"""
腾讯云 API 签名 v3 通用调用脚本 (Python 版)
基于腾讯云 API 签名 v3 文档实现: https://cloud.tencent.com/document/product/213/30654

纯 Python 标准库实现，支持 Windows / Linux / macOS 跨平台运行。
不依赖 curl、openssl、jq 等外部工具。

用法 (命令行):
    python3 tcloud_api.py <service> <host> <action> <version> [payload] [region]

示例:
    python3 tcloud_api.py advisor advisor.tencentcloudapi.com DescribeArchList 2020-07-21 '{"PageNumber":1,"PageSize":10}'

作为模块导入:
    from tcloud_api import call_api
    result = call_api("advisor", "advisor.tencentcloudapi.com",
                      "DescribeArchList", "2020-07-21",
                      {"PageNumber": 1, "PageSize": 10})

环境变量（必须提前设置）:
    TENCENTCLOUD_SECRET_ID  - 腾讯云 SecretId
    TENCENTCLOUD_SECRET_KEY - 腾讯云 SecretKey
    TENCENTCLOUD_TOKEN      - 临时密钥 Token（可选，使用临时密钥时设置）

输出格式（统一 JSON）:
    成功: {"success": true, "action": "<Action>", "data": {...}, "requestId": "xxx"}
    失败: {"success": false, "action": "<Action>", "error": {"code": "xxx", "message": "xxx"}, "requestId": "xxx"}
"""

import hashlib
import hmac
import json
import os
import ssl
import sys
import time
from datetime import datetime, timezone
from typing import Union
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from i18n import T


def _get_ssl_context():
    """获取 SSL 上下文，兼容各平台 CA 证书差异"""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        # certifi 不可用时降级到系统默认 CA（Windows/Linux 系统 CA 通常可用）
        return ssl.create_default_context()


def _sign_tc3(key: bytes, msg: str) -> bytes:
    """TC3 HMAC-SHA256 签名辅助函数"""
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _output_json(obj: dict) -> str:
    """统一 JSON 输出"""
    return json.dumps(obj, ensure_ascii=False)


def _make_error(action: str, code: str, message: str, request_id: str = "") -> dict:
    """构造统一错误结果"""
    return {
        "success": False,
        "action": action,
        "error": {"code": code, "message": message},
        "requestId": request_id,
    }


def _make_success(action: str, data: dict, request_id: str) -> dict:
    """构造统一成功结果"""
    return {
        "success": True,
        "action": action,
        "data": data,
        "requestId": request_id,
    }


def call_api(service: str, host: str, action: str, version: str,
             payload: Union[dict, str] = None, region: str = "ap-singapore",
             secret_id: str = None, secret_key: str = None,
             token: str = None) -> dict:
    """
    调用腾讯云 API（TC3-HMAC-SHA256 签名）

    Args:
        service: 服务名（如 advisor, sts, cam）
        host: 接口域名（如 advisor.tencentcloudapi.com）
        action: 接口名称（如 DescribeArchList）
        version: 接口版本（如 2020-07-21）
        payload: 请求体，dict 或 JSON 字符串
        region: 地域，国际站固定 ap-singapore（实测国际站账号各接口均由新加坡服务）
        secret_id: SecretId，不传则通过 credential_manager 或环境变量获取
        secret_key: SecretKey，不传则通过 credential_manager 或环境变量获取
        token: 临时密钥 Token，不传则通过 credential_manager 或环境变量获取

    Returns:
        dict: 统一格式的结果字典
    """
    # 密钥：优先使用显式传入，其次通过 credential_manager 统一获取（国际站仅 AK/SK 环境变量）
    if not secret_id or not secret_key:
        try:
            from credential_manager import get_credential, CredentialNotFoundError
            cred = get_credential()
            secret_id = secret_id or cred["secretId"]
            secret_key = secret_key or cred["secretKey"]
            token = token or cred.get("token", "")
        except ImportError:
            # credential_manager 不可用，回退到环境变量
            secret_id = secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
            token = token or os.environ.get("TENCENTCLOUD_TOKEN", "")
        except CredentialNotFoundError:
            return _make_error(
                action, "NeedAuth",
                T("未找到凭证，请配置 AK/SK 环境变量。")
            )
        except Exception as e:
            return _make_error(
                action, "NeedAuth", str(e)
            )

    if not secret_id or not secret_key:
        return _make_error(
            action, "MissingCredentials",
            T("未配置凭证。请配置 AK/SK 环境变量。\n"
              "密钥获取: https://console.tencentcloud.com/cam/capi")
        )

    # ---- 服务白名单限制 ----
    # AK/SK: 允许 advisor + cam + sts（凭证校验需要）
    _AKSK_ALLOWED_SERVICES = {"advisor", "cam", "sts"}

    allowed = _AKSK_ALLOWED_SERVICES
    deny_hint = T("CloudQ 不支持调用 {service} 服务。", service=service)

    if service not in allowed:
        return _make_error(
            action, "ServiceNotAllowed",
            T("当前凭证不允许调用 {service} 服务（允许: {allowed}）。{hint}",
              service=service, allowed=", ".join(sorted(allowed)), hint=deny_hint)
        )

    # 请求体
    if payload is None:
        payload_str = "{}"
    elif isinstance(payload, dict):
        payload_str = json.dumps(payload, separators=(",", ":"))
    else:
        payload_str = str(payload)

    # 签名参数
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    # 步骤 1：拼接规范请求串
    hashed_payload = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    canonical_request = (
        f"POST\n"
        f"/\n"
        f"\n"
        f"content-type:application/json; charset=utf-8\n"
        f"host:{host}\n"
        f"x-tc-action:{action.lower()}\n"
        f"\n"
        f"content-type;host;x-tc-action\n"
        f"{hashed_payload}"
    )

    # 步骤 2：拼接待签名字符串
    credential_scope = f"{date}/{service}/tc3_request"
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode("utf-8")
    ).hexdigest()
    string_to_sign = (
        f"{algorithm}\n"
        f"{timestamp}\n"
        f"{credential_scope}\n"
        f"{hashed_canonical_request}"
    )

    # 步骤 3：计算签名
    secret_date = _sign_tc3(f"TC3{secret_key}".encode("utf-8"), date)
    secret_service = _sign_tc3(secret_date, service)
    secret_signing = _sign_tc3(secret_service, "tc3_request")
    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    # 步骤 4：拼接 Authorization
    authorization = (
        f"{algorithm} "
        f"Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders=content-type;host;x-tc-action, "
        f"Signature={signature}"
    )

    # 步骤 5：发送请求
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version,
        "X-TC-Region": region,
    }
    if token:
        headers["X-TC-Token"] = token

    req = Request(
        f"https://{host}",
        data=payload_str.encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        ctx = _get_ssl_context()
        with urlopen(req, context=ctx, timeout=30) as resp:
            response_body = resp.read().decode("utf-8")
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8")
            # 尝试解析 API 错误响应
            data = json.loads(body)
            response = data.get("Response", {})
            error = response.get("Error", {})
            if error:
                return _make_error(
                    action,
                    error.get("Code", "HTTPError"),
                    error.get("Message", f"HTTP {e.code}"),
                    response.get("RequestId", ""),
                )
        except Exception:
            pass
        return _make_error(
            action, "HTTPError",
            T("HTTP 请求失败 (状态码 {code}): {reason}", code=e.code, reason=e.reason)
        )
    except URLError as e:
        return _make_error(
            action, "NetworkError",
            T("网络连接失败，请检查网络和域名 {host} 是否可达: {reason}",
              host=host, reason=e.reason)
        )
    except Exception as e:
        return _make_error(
            action, "NetworkError",
            T("请求异常: {error}", error=e)
        )

    # 步骤 6：解析响应
    try:
        data = json.loads(response_body)
    except json.JSONDecodeError:
        return _make_error(action, "ParseError", T("响应不是有效的 JSON"))

    response = data.get("Response", {})
    request_id = response.get("RequestId", "")

    if "Error" in response:
        err = response["Error"]
        return _make_error(
            action,
            err.get("Code", "Unknown"),
            err.get("Message", T("未知错误")),
            request_id,
        )

    # 成功：移除 RequestId 后将剩余字段作为 data
    result_data = {k: v for k, v in response.items() if k != "RequestId"}
    return _make_success(action, result_data, request_id)


def main():
    """命令行入口"""
    args = sys.argv[1:]

    if len(args) < 4:
        print(_output_json(_make_error(
            "", "MissingParameter",
            T("缺少必要参数。用法: python3 tcloud_api.py <service> <host> <action> <version> [payload] [region]")
        )))
        sys.exit(1)

    service = args[0]
    host = args[1]
    action = args[2]
    version = args[3]
    payload_str = args[4] if len(args) > 4 else "{}"
    region = args[5] if len(args) > 5 else "ap-singapore"

    # 解析 payload
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        payload = payload_str

    result = call_api(service, host, action, version, payload, region)
    print(_output_json(result))

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
