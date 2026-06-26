#!/usr/bin/env python3
"""
阿里云账户余额查询脚本
用法: python3 query_aliyun_balance.py
说明: 凭证从 Base64 编码的 .aliyun_ak_sk.env 文件读取
⚠️ 警告: 这是敏感凭证，请勿泄露或提交到 GitHub
"""

import os
import json
import base64

# 凭证文件路径
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".aliyun_ak_sk.env")

def load_credentials():
    """从 Base64 编码文件读取凭证"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"凭证文件不存在: {CREDENTIALS_FILE}")
    
    credentials = {}
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("ALIYUN_ACCESS_KEY_ID_B64="):
                b64_id = line.split("=", 1)[1].strip()
                credentials["access_key_id"] = base64.b64decode(b64_id).decode('utf-8')
            elif line.startswith("ALIYUN_ACCESS_KEY_SECRET_B64="):
                b64_secret = line.split("=", 1)[1].strip()
                credentials["access_key_secret"] = base64.b64decode(b64_secret).decode('utf-8')
    
    if not credentials.get("access_key_id") or not credentials.get("access_key_secret"):
        raise ValueError("凭证文件格式错误或为空")
    
    return credentials

def query_balance():
    """查询阿里云账户余额"""
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkbssopenapi.request.v20171214 import QueryAccountBalanceRequest
    
    credentials = load_credentials()
    
    # 创建客户端
    client = AcsClient(
        credentials["access_key_id"], 
        credentials["access_key_secret"], 
        "cn-hangzhou"
    )
    
    # 查询账户余额
    req = QueryAccountBalanceRequest.QueryAccountBalanceRequest()
    req.set_accept_format('json')
    
    resp = client.do_action_with_exception(req)
    result = json.loads(resp.decode('utf-8'))
    
    if not result.get("Success"):
        raise Exception(f"API调用失败: {result.get('Message')}")
    
    return result["Data"]

def main():
    """主函数"""
    import json
    try:
        result = query_balance()
        
        print("=" * 50)
        print("☁️ 阿里云账户余额查询")
        print("=" * 50)
        print(f"货币: {result.get('Currency', 'CNY')}")
        print(f"可用余额: {result.get('AvailableAmount', 'N/A')} 元")
        print(f"可用现金余额: {result.get('AvailableCashAmount', 'N/A')} 元")
        print(f"信用额度: {result.get('CreditAmount', 'N/A')} 元")
        print(f"网商银行信用额度: {result.get('MybankCreditAmount', 'N/A')} 元")
        print("=" * 50)
        
        return result
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        print("请确保已配置阿里云凭证文件")
        return None
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return None

if __name__ == "__main__":
    main()
