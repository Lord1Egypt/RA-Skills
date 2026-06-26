#!/usr/bin/env python3
"""
火山引擎账户查询脚本（余额 + 账单）
用法: 
  python3 query_volc_billing.py              # 查询余额
  python3 query_volc_billing.py --history    # 查询历史账单
  python3 query_volc_billing.py --all        # 查询全部
说明: 凭证从 Base64 编码的 .volc_ak_sk.env 文件读取
⚠️ 警告: 这是敏感凭证，请勿泄露
"""

import os
import sys
import base64
import requests
import hmac
import hashlib
import time
from urllib.parse import quote
import json

# 凭证文件路径
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".volc_ak_sk.env")

def load_credentials():
    """从 Base64 编码文件读取火山引擎凭证"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"凭证文件不存在: {CREDENTIALS_FILE}")
    
    akid = None
    secret_key = None
    
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            # 跳过注释行和空行
            if not line or line.startswith("#"):
                continue
            if line.startswith("VOLC_ACCESS_KEY_ID="):
                akid = line.split("=", 1)[1].strip()
            elif line.startswith("VOLC_SECRET_KEY="):
                # SecretKey 直接使用（不需解码）
                secret_key = line.split("=", 1)[1].strip()
    
    if not akid or not secret_key:
        raise ValueError("未找到火山引擎凭证")
    
    return akid, secret_key

def volcengine_sign(secret_key, date_stamp, region, service, string_to_sign):
    """火山引擎 V4 签名"""
    k_date = hmac.new(secret_key.encode('utf-8'), date_stamp.encode('utf-8'), hashlib.sha256).digest()
    k_region = hmac.new(k_date, region.encode('utf-8'), hashlib.sha256).digest()
    k_service = hmac.new(k_region, service.encode('utf-8'), hashlib.sha256).digest()
    k_signing = hmac.new(k_service, "request".encode('utf-8'), hashlib.sha256).digest()
    signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def api_request(action, params=None):
    """火山引擎 API 请求"""
    akid, secret_key = load_credentials()
    
    t = time.gmtime()
    amz_date = time.strftime("%Y%m%dT%H%M%SZ", t)
    date_stamp = time.strftime("%Y%m%d", t)
    
    if params is None:
        params = {}
    params["Action"] = action
    params["Version"] = "2022-01-01"
    
    method = "GET"
    uri = "/"
    canonical_querystring = "&".join([f"{k}={quote(v, safe='')}" for k,v in sorted(params.items())])
    signed_headers = "host;x-date"
    canonical_headers = f"host:open.volcengineapi.com\nx-date:{amz_date}\n"
    hashed_payload = hashlib.sha256(b"").hexdigest()
    
    canonical_request = f"{method}\n{uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{hashed_payload}"
    
    algorithm = "HMAC-SHA256"
    credential_scope = f"{date_stamp}/cn-beijing/billing/request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashed_canonical_request}"
    
    signature = volcengine_sign(secret_key, date_stamp, "cn-beijing", "billing", string_to_sign)
    authorization = f"{algorithm} Credential={akid}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    
    url = f"https://open.volcengineapi.com/?{canonical_querystring}"
    headers = {
        "Host": "open.volcengineapi.com",
        "X-Date": amz_date,
        "Authorization": authorization
    }
    
    resp = requests.get(url, headers=headers)
    return resp.json()

def query_balance():
    """查询账户余额"""
    result = api_request("QueryBalanceAcct")
    return result.get("Result", {})

def query_bill(month):
    """查询指定月份账单"""
    result = api_request("ListBillOverviewByCategory", {"BillPeriod": month})
    bill_list = result.get("Result", {}).get("List", [])
    
    total = 0
    if bill_list:
        for category in bill_list:
            items = category.get("List", [])
            for item in items:
                total = float(item.get('PayableAmount', '0'))
    return month, total

def query_history(months=6):
    """查询历史账单"""
    # 生成近N个月的列表
    from datetime import datetime, timedelta
    result = []
    current = datetime.now()
    
    for i in range(months):
        # 每月1日
        month_date = current.replace(day=1) - timedelta(days=i*30)
        month_str = month_date.strftime("%Y-%m")
        result.append(month_str)
    
    return result

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="火山引擎账户查询")
    parser.add_argument("--history", action="store_true", help="查询历史账单")
    parser.add_argument("--all", action="store_true", help="查询余额+历史账单")
    parser.add_argument("--months", type=int, default=6, help="查询月份数(默认6)")
    args = parser.parse_args()
    
    try:
        # 查询余额
        if args.all or (not args.history):
            balance = query_balance()
            print("=" * 60)
            print("🔥 火山引擎账户余额")
            print("=" * 60)
            print(f"账户ID: {balance.get('AccountID', 'N/A')}")
            print(f"可用余额: {balance.get('AvailableBalance', 'N/A')} 元")
            print(f"现金余额: {balance.get('CashBalance', 'N/A')} 元")
            print(f"欠费金额: {balance.get('ArrearsBalance', 'N/A')} 元")
            print("=" * 60)
        
        # 查询历史账单
        if args.history or args.all:
            months = query_history(args.months)
            print("\n" + "=" * 60)
            print(f"🔥 火山引擎历史账单 (近{args.months}个月)")
            print("=" * 60)
            print(f"{'月份':<10} {'消费金额':<15}")
            print("-" * 60)
            
            total = 0
            for month in months:
                try:
                    m, amount = query_bill(month)
                    print(f"{m:<10} {amount:.2f} 元")
                    total += amount
                except:
                    print(f"{month:<10} 查询失败")
            
            print("-" * 60)
            print(f"{'合计':<10} {total:.2f} 元")
            print("=" * 60)
            
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    main()
