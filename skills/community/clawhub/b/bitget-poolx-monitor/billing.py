#!/usr/bin/env python3
"""
SkillPay.me 收费接口
"""
import requests

BILLING_API_URL = "https://skillpay.me"
BILLING_API_KEY = "sk_0c57911690182c45404f945f2908a9e2e32ed448055895ac02227856eaf226ad"
SKILL_ID = "6a3b1843-5266-40c6-8f0c-408512bb6f43"

def check_balance(user_id):
    """查询用户余额"""
    url = f"{BILLING_API_URL}/api/v1/billing/balance"
    headers = {"X-API-Key": BILLING_API_KEY}
    
    try:
        resp = requests.get(f"{url}?user_id={user_id}", headers=headers, timeout=10)
        data = resp.json()
        return data.get("balance", 0)
    except Exception as e:
        print(f"查询余额错误: {e}")
        return 0

def charge_user(user_id, amount=0.001):
    """
    扣费（每次调用）
    amount: USDT 数量，默认 0.001
    """
    url = f"{BILLING_API_URL}/api/v1/billing/charge"
    headers = {
        "X-API-Key": BILLING_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "user_id": user_id,
        "skill_id": SKILL_ID,
        "amount": amount
    }
    
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        result = resp.json()
        
        if result.get("success"):
            return {"ok": True, "balance": result.get("balance", 0)}
        else:
            return {
                "ok": False, 
                "balance": result.get("balance", 0),
                "payment_url": result.get("payment_url", "")
            }
    except Exception as e:
        print(f"扣费错误: {e}")
        return {"ok": False, "error": str(e)}

def get_payment_link(user_id, amount=10):
    """生成充值链接"""
    url = f"{BILLING_API_URL}/api/v1/billing/payment-link"
    headers = {
        "X-API-Key": BILLING_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"user_id": user_id, "amount": amount}
    
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=10)
        result = resp.json()
        return result.get("payment_url", "")
    except Exception as e:
        print(f"生成充值链接错误: {e}")
        return ""

# 使用示例
if __name__ == "__main__":
    user = "test_user"
    
    # 1. 查询余额
    balance = check_balance(user)
    print(f"用户余额: {balance} USDT")
    
    # 2. 扣费
    result = charge_user(user, 0.001)
    if result.get("ok"):
        print("✅ 扣费成功，执行功能")
    else:
        print(f"❌ 扣费失败: {result}")
        if result.get("payment_url"):
            print(f"充值链接: {result['payment_url']}")
