#!/usr/bin/env python3
"""
商户费率查询脚本
调用 agent/getMerchantFeeInfo 接口
- 请求体 AES 加密
- 响应体 AES 解密
- 支持从本地读取已保存的 agentNo/apikey
"""

import base64
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 认证信息存储路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTH_FILE = os.path.join(SCRIPT_DIR, ".auth.json")


def load_auth():
    """加载已保存的认证信息"""
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_auth(base_url: str, agent_no: str, api_key: str):
    """保存认证信息"""
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump({"baseUrl": base_url, "agentNo": agent_no, "apiKey": api_key}, f)


def aes_encrypt(plaintext: str, key_b64: str) -> str:
    """
    AES-128 加密，ECB模式，PKCS5Padding
    plaintext: 明文字符串
    key_b64: Base64编码的AES密钥
    返回: 加密后的hex字符串
    """
    key_bytes = base64.b64decode(key_b64)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded = pad(plaintext.encode("utf-8"), AES.block_size, style="pkcs7")
    encrypted = cipher.encrypt(padded)
    return encrypted.hex()


def aes_decrypt(ciphertext_hex: str, key_b64: str) -> str:
    """
    AES-128 解密，ECB模式，PKCS5Padding
    ciphertext_hex: hex字符串
    key_b64: Base64编码的AES密钥
    返回: 解密后的明文字符串
    """
    key_bytes = base64.b64decode(key_b64)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size, style="pkcs7")
    return decrypted.decode("utf-8")


def query_merchant_fee(base_url: str, agent_no: str, api_key: str, user_id: str, tusn: str) -> dict:
    """
    查询商户费率

    Args:
        base_url: API Base URL
        agent_no: 代理商号
        api_key: API Key（Base64编码的AES密钥）
        user_id: 商户编号
        tusn: SN编号

    Returns:
        dict: API 响应结果（已解密）
    """
    url = f"{base_url.rstrip('/')}/agent/getMerchantFeeInfo"
    timeout = 30

    # 构造明文请求体
    plaintext = json.dumps(
        {"agentNo": agent_no, "userId": user_id, "tusn": tusn}, separators=(",", ":")
    )

    # AES 加密
    encrypted_data = aes_encrypt(plaintext, api_key)

    # form-data 请求
    form_data = urllib.parse.urlencode(
        {"appKey": agent_no, "data": encrypted_data}
    ).encode("utf-8")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        req = urllib.request.Request(
            url, data=form_data, headers=headers, method="POST"
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            resp_body = response.read().decode("utf-8")

        # 解密响应
        if resp_body.strip():
            decrypted = aes_decrypt(resp_body, api_key)
            return json.loads(decrypted)
        else:
            return {"retCode": "9999", "retMsg": "响应为空"}

    except urllib.error.HTTPError as e:
        return {"retCode": "9999", "retMsg": f"HTTP错误: {e.code} {e.reason}"}
    except urllib.error.URLError as e:
        return {"retCode": "9999", "retMsg": f"网络错误: {e.reason}"}
    except json.JSONDecodeError as e:
        return {"retCode": "9999", "retMsg": f"响应解析失败: {e}"}
    except Exception as e:
        return {"retCode": "9999", "retMsg": f"未知错误: {str(e)}"}


def format_output(result: dict) -> str:
    """
    格式化输出
    """
    ret_code = result.get("retCode", "")
    ret_msg = result.get("retMsg", "")

    # 失败
    if ret_code != "0000":
        return f"❌ 查询失败\n\n**返回码**：{ret_code}\n**原因**：{ret_msg}"

    # 成功
    data = result.get("data", {})
    user_id = result.get("userId", "")

    lines = ["✅ 商户费率信息", ""]
    lines.append(f"**商户编号**：{user_id}")
    lines.append(f"**商户名称**：{data.get('realName', '-')}")
    lines.append(
        f"**所属代理**：{data.get('directAgentName', '-')}（{data.get('directAgentNo', '-')}）"
    )
    lines.append("")
    lines.append("━━ 费率详情 ━━")

    # 费率信息
    rate_fields = [
        ("贷记卡基础费率", "creditRadio", "%"),
        ("借记卡费率", "debitRadio", "%"),
        ("借记卡封顶手续费", "debitTopRate", "元"),
        ("云闪付费率", "flashRadio", "%"),
        ("支付宝龙舟计划费率", "vipRadio", "%"),
        ("扫码费率（微信/支付宝）", "wxPayRadio", "%"),
        ("出款服务费", "singleFee", "元"),
        ("商户管理费1", "manageFeeOne", "%"),
        ("商户管理费2", "manageFeeTwo", "%"),
    ]

    for label, key, unit in rate_fields:
        value = data.get(key)
        if value is not None:
            lines.append(f"**{label}**：{value}{unit}")

    # 绑定终端
    tusn_list = data.get("tusn", "")
    tusn_display = tusn_list if tusn_list else "无"
    lines.append("")
    lines.append(f"**绑定终端**：{tusn_display}")

    return "\n".join(lines)


def main():
    """
    用法：
      首次/换代理：python3 query_fee.py <baseUrl> <agentNo> <apiKey> <userId> <tusn>
      复用认证：    python3 query_fee.py <userId> <tusn>
    """
    if len(sys.argv) == 6:
        base_url, agent_no, api_key, user_id, tusn = sys.argv[1:]
    elif len(sys.argv) == 3:
        user_id, tusn = sys.argv[1:]
        auth = load_auth()
        if not auth:
            print("⚠️ 未找到已保存的认证信息，请提供完整参数：baseUrl agentNo apikey userId tusn", file=sys.stderr)
            sys.exit(1)
        base_url = auth["baseUrl"]
        agent_no = auth["agentNo"]
        api_key = auth["apiKey"]
    else:
        print("用法:", file=sys.stderr)
        print("  首次/换代理：python3 query_fee.py <baseUrl> <agentNo> <apiKey> <userId> <tusn>", file=sys.stderr)
        print("  复用认证：    python3 query_fee.py <userId> <tusn>", file=sys.stderr)
        sys.exit(1)

    result = query_merchant_fee(base_url, agent_no, api_key, user_id, tusn)

    # 保存认证信息（不管成功失败都保存）
    save_auth(base_url, agent_no, api_key)

    print(format_output(result))

    # 非0000退出码
    if result.get("retCode") != "0000":
        sys.exit(1)


if __name__ == "__main__":
    main()
