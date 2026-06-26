"""
Media Labeling Authentication Module for eKYC Suite
图像标签鉴权模块
======================================================
# SECURITY MANIFEST:
#   Environment variables accessed: LABEL_APPID, LABEL_SECRET
#   External endpoints called: https://kyc2.qcloud.com/idap-ac/oauth2/v2/api_ticket
#   Local files read: none
#   Local files written: none
Handles ticket and SHA1 signature for Media Labeling API (capability 8).
处理能力8的ticket和SHA1签名。

Key differences from KYC auth / 与KYC鉴权的区别:
  1. No access_token step — ticket obtained directly / 无access_token步骤，直接获取ticket
  2. Signature uses 6 parameters (adds unixTimeStamp) / 签名用6参数（多一个unixTimeStamp）
  3. Base URL: kyc2.qcloud.com
  4. Ticket endpoint: /idap-ac/oauth2/v2/api_ticket

Still SHA1 (40-char uppercase). DO NOT use SHA256.
仍然使用SHA1（40位大写），请勿使用SHA256。
"""

import hashlib
import random
import string
import time
import requests
import os


LABEL_BASE = "https://kyc2.qcloud.com"


def get_label_credentials():
    """
    Load media labeling credentials from environment.
    从环境变量读取图像标签凭证。
    """
    appid = os.environ.get("LABEL_APPID", "")
    secret = os.environ.get("LABEL_SECRET", "")
    if not appid or not secret:
        raise ValueError(
            "Missing media labeling credentials. Set LABEL_APPID and LABEL_SECRET in your .env file or environment variables.\n"
            "缺少图像标签凭证，请在 .env 文件或环境变量中配置 LABEL_APPID 和 LABEL_SECRET。\n"
            "Note: Media labeling uses a SEPARATE credential set from KYC. / 注意：图像标签使用独立密钥，与KYC不同。\n"
            "Contact Huiyan tech support (WeChat: blue-201809) for credentials.\n"
            "联系慧眼技术支持（微信号：blue-201809）获取密钥。\n"
            "IMPORTANT: Use TEST credentials (free 100 calls). Do NOT use production credentials — production IDs incur charges.\n"
            "重要提示：请使用测试ID和测试Secret（免费100次调用），不要使用正式ID——正式ID会产生计费。"
        )
    return appid, secret


def get_label_ticket(app_id: str, secret: str) -> str:
    """
    Get SIGN ticket directly (no access_token needed).
    直接获取ticket（无需access_token）。
    Endpoint: https://kyc2.qcloud.com/idap-ac/oauth2/v2/api_ticket
    """
    url = f"{LABEL_BASE}/idap-ac/oauth2/v2/api_ticket"
    params = {"appId": app_id, "secret": secret}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        safe_msg = str(e)
        for sensitive in [secret, app_id]:
            safe_msg = safe_msg.replace(sensitive, "***")
        raise RuntimeError(f"Label ticket network error / 网络错误: {safe_msg}") from None
    data = resp.json()
    if str(data.get("code")) not in ("0",) and data.get("code") != 0:
        raise RuntimeError(
            f"Failed to get label ticket / 获取标签ticket失败: "
            f"code={data.get('code')}, msg={data.get('msg')}"
        )
    return data["ticket"]


def generate_nonce(length: int = 32) -> str:
    """Generate 32-char alphanumeric random string / 生成32位随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_order_no() -> str:
    """Generate unique order number / 生成唯一订单号"""
    return f"label{int(time.time()*1000)}{random.randint(1000,9999)}"


def sign_label_request(app_id: str, order_no: str, nonce: str, version: str,
                       ticket: str, unix_timestamp: str) -> str:
    """
    SHA1 signature from 6 parameters / 6参数SHA1签名

    Same algorithm as KYC but with 6 values (adds unixTimeStamp).
    与KYC相同算法，但用6个值（多一个unixTimeStamp）。

    WARNING / 警告: SHA1 only! Not SHA256! / 只用SHA1！
    """
    values = [app_id, order_no, nonce, version, ticket, unix_timestamp]
    values.sort()
    concat = ''.join(values)
    signature = hashlib.sha1(concat.encode('utf-8')).hexdigest().upper()
    assert len(signature) == 40, (
        f"Signature length error! Expected 40 (SHA1), got {len(signature)}. "
        f"签名长度错误！期望40，实际{len(signature)}。"
    )
    return signature


def get_label_auth():
    """
    Complete auth flow for media labeling.
    图像标签完整鉴权流程。
    Returns: (app_id, sign_fn) where sign_fn(order_no, nonce, unix_timestamp) → signature
    """
    app_id, secret = get_label_credentials()
    ticket = get_label_ticket(app_id, secret)

    def sign_fn(order_no: str, nonce: str, unix_timestamp: str) -> str:
        return sign_label_request(app_id, order_no, nonce, "1.0.0", ticket, unix_timestamp)

    return app_id, sign_fn
