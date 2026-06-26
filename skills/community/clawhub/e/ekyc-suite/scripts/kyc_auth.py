"""
KYC Authentication Module for eKYC Suite
KYC鉴权模块
=============================================
# SECURITY MANIFEST:
#   Environment variables accessed: KYC_APPID, KYC_SECRET
#   External endpoints called:
#     https://kyc1.qcloud.com/api/oauth2/access_token
#     https://kyc1.qcloud.com/api/oauth2/api_ticket
#     https://miniprogram-kyc.tencentcloudapi.com/api/oauth2/access_token
#     https://miniprogram-kyc.tencentcloudapi.com/api/oauth2/api_ticket
#   Local files read: none
#   Local files written: none
Handles access_token, SIGN ticket, and SHA1 signature for capabilities 1-7.
处理能力1-7的access_token、SIGN ticket和SHA1签名。

Auth flow / 鉴权流程:
  1. GET access_token (app_id + secret)
  2. GET SIGN ticket  (app_id + access_token)
  3. Sign: sort 5 params → concat → SHA1 → 40-char uppercase hex

CRITICAL / 关键: SHA1 only. SHA256 produces 64 chars and WILL fail.
只用SHA1。SHA256产生64位字符串，鉴权必失败。
"""

import hashlib
import random
import string
import time
import requests
import os


# === Base URLs / 基础域名 ===
# Different APIs use different domains — intentional, not a bug.
# 不同API用不同域名——这是正确的，不是bug。
KYC_BASE_MAIN = "https://kyc1.qcloud.com"
KYC_BASE_MINI = "https://miniprogram-kyc.tencentcloudapi.com"

# Capability → base URL mapping / 能力→域名映射
# Ensures token/ticket are fetched from the correct domain.
# 确保从正确域名获取token/ticket。
_CAPABILITY_BASE = {
    "face_compare": KYC_BASE_MINI,
    "photo_liveness_detect": KYC_BASE_MAIN,
    "video_liveness_detect": KYC_BASE_MAIN,
    "id_card_ocr": KYC_BASE_MAIN,
    "bank_card_ocr": KYC_BASE_MAIN,
    "driver_license_ocr": KYC_BASE_MINI,
    "vehicle_license_ocr": KYC_BASE_MINI,
}


def get_env_credentials(prefix="KYC"):
    """
    Load credentials from environment variables.
    从环境变量读取凭证。
    """
    appid = os.environ.get(f"{prefix}_APPID", "")
    secret = os.environ.get(f"{prefix}_SECRET", "")
    if not appid or not secret:
        raise ValueError(
            f"Missing {prefix} credentials. Set {prefix}_APPID and {prefix}_SECRET in your .env file or environment variables.\n"
            f"缺少{prefix}凭证，请在 .env 文件或环境变量中配置 {prefix}_APPID 和 {prefix}_SECRET。\n"
            f"How to obtain / 获取方式:\n"
            f"  1. Visit https://console.cloud.tencent.com/faceid/access (self-service for Key A)\n"
            f"     前往腾讯云人脸核身控制台自助申请密钥A\n"
            f"  2. Or contact Huiyan tech support (WeChat: blue-201809) for Key A and Key B\n"
            f"     或联系慧眼技术支持（微信号：blue-201809）获取密钥A和密钥B\n"
            f"IMPORTANT: Use TEST credentials (free 100 calls). Do NOT use production credentials — production IDs incur charges.\n"
            f"重要提示：请使用测试ID和测试Secret（免费100次调用），不要使用正式ID——正式ID会产生计费。"
        )
    return appid, secret


def get_access_token(app_id: str, secret: str, base_url: str = KYC_BASE_MAIN) -> str:
    """
    Step 1: Get access_token. Valid for 7200s.
    第1步：获取access_token，有效期7200秒。
    """
    url = f"{base_url}/api/oauth2/access_token"
    params = {
        "app_id": app_id,
        "secret": secret,
        "grant_type": "client_credential",
        "version": "1.0.0"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        safe_msg = str(e)
        for sensitive in [secret, app_id]:
            safe_msg = safe_msg.replace(sensitive, "***")
        raise RuntimeError(f"access_token network error / 网络错误: {safe_msg}") from None
    data = resp.json()
    if str(data.get("code")) != "0":
        raise RuntimeError(
            f"Failed to get access_token / 获取access_token失败: "
            f"code={data.get('code')}, msg={data.get('msg')}"
        )
    return data["access_token"]


def get_sign_ticket(app_id: str, access_token: str, base_url: str = KYC_BASE_MAIN) -> str:
    """
    Step 2: Get SIGN ticket. Valid for 3600s.
    第2步：获取SIGN ticket，有效期3600秒。
    """
    url = f"{base_url}/api/oauth2/api_ticket"
    params = {
        "app_id": app_id,
        "access_token": access_token,
        "type": "SIGN",
        "version": "1.0.0"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        safe_msg = str(e)
        for sensitive in [access_token, app_id]:
            safe_msg = safe_msg.replace(sensitive, "***")
        raise RuntimeError(f"SIGN ticket network error / 网络错误: {safe_msg}") from None
    data = resp.json()
    if str(data.get("code")) != "0":
        raise RuntimeError(
            f"Failed to get SIGN ticket / 获取SIGN ticket失败: "
            f"code={data.get('code')}, msg={data.get('msg')}"
        )
    tickets = data.get("tickets", [])
    if not tickets:
        raise RuntimeError("SIGN ticket array is empty / tickets数组为空")
    return tickets[0]["value"]


def generate_nonce(length: int = 32) -> str:
    """Generate 32-char alphanumeric random string / 生成32位随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_order_no() -> str:
    """Generate unique order number / 生成唯一订单号"""
    return f"ekyc{int(time.time()*1000)}{random.randint(1000,9999)}"


def sign_request(app_id: str, order_no: str, nonce: str, version: str, ticket: str) -> str:
    """
    Step 3: SHA1 signature from 5 parameters / 第3步：5参数SHA1签名

    Algorithm (DO NOT MODIFY / 算法，请勿修改):
      1. Take 5 values: appId, orderNo, nonce, version, ticket
      2. Sort lexicographically / 字典序排列
      3. Concatenate without separator / 无分隔符拼接
      4. SHA1 hash (UTF-8)
      5. UPPERCASE → exactly 40 characters / 大写，恰好40位

    WARNING / 警告: SHA256 → 64 chars → auth WILL fail / SHA256=64位=鉴权必败!
    """
    values = [app_id, order_no, nonce, version, ticket]
    values.sort()
    concat = ''.join(values)
    signature = hashlib.sha1(concat.encode('utf-8')).hexdigest().upper()
    assert len(signature) == 40, (
        f"Signature length error! Expected 40 (SHA1), got {len(signature)}. "
        f"签名长度错误！期望40(SHA1)，实际{len(signature)}。"
        f"You are likely using SHA256. / 你可能误用了SHA256。"
    )
    return signature


def get_full_auth(capability: str = None, base_url: str = None):
    """
    Complete auth flow / 完整鉴权流程:
    credentials → access_token → ticket → signing function

    Args:
        capability: auto-selects base URL / 自动选择域名
        base_url: manual override / 手动覆盖

    Returns: (app_id, sign_fn) where sign_fn(order_no, nonce) → 40-char signature
    """
    app_id, secret = get_env_credentials("KYC")

    if base_url is None and capability:
        base_url = _CAPABILITY_BASE.get(capability, KYC_BASE_MAIN)
    elif base_url is None:
        base_url = KYC_BASE_MAIN

    access_token = get_access_token(app_id, secret, base_url)
    ticket = get_sign_ticket(app_id, access_token, base_url)

    def sign_fn(order_no: str, nonce: str) -> str:
        return sign_request(app_id, order_no, nonce, "1.0.0", ticket)

    return app_id, sign_fn


def parse_response(data: dict, *fields) -> dict:
    """
    Dual-path response parsing (top-level + result nested).
    双路径响应解析（顶层+result嵌套），防止undefined。
    """
    result = {}
    for field in fields:
        value = data.get(field)
        if value is None and isinstance(data.get("result"), dict):
            value = data["result"].get(field)
        result[field] = value
    return result
