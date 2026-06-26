import requests
import uuid
import sys

# SkillPay 配置 - 使用正确的SDK方式
SKILLPAY_API_KEY = 'sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e'
SKILL_ID = 'ecommerce-data-analyzer'  # 你的技能ID
BILLING_URL = "https://skillpay.me/api/v1/billing"
HEADERS = {
    "X-API-Key": SKILLPAY_API_KEY, 
    "Content-Type": "application/json"
}

# 测试模式：设置为True可以模拟支付成功
TEST_MODE = True

def test_charge_user():
    """测试扣费接口"""
    print("=== 测试扣费接口 ===")
    
    user_id = str(uuid.uuid4())
    print(f"测试用户ID: {user_id}")
    
    if TEST_MODE:
        print("[测试模式] 模拟扣费成功")
        return {"ok": True, "balance": 1000}
    
    try:
        resp = requests.post(
            f"{BILLING_URL}/charge", 
            headers=HEADERS, 
            json={
                "user_id": user_id, 
                "skill_id": SKILL_ID, 
                "amount": 0,  # 每次调用1 token
            },
            timeout=10
        )
        print(f"响应状态码: {resp.status_code}")
        print(f"响应内容: {resp.text}")
        
        data = resp.json()
        if data.get("success"):
            print("[OK] 扣费成功!")
            print(f"剩余余额: {data.get('balance')} tokens")
            return {"ok": True, "balance": data.get("balance")}
        else:
            print("[ERROR] 扣费失败")
            print(f"支付链接: {data.get('payment_url')}")
            return {
                "ok": False, 
                "balance": data.get("balance"), 
                "payment_url": data.get("payment_url")
            }
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
        return {"ok": False, "error": str(e)}

def test_get_balance():
    """测试余额查询接口"""
    print("\n=== 测试余额查询接口 ===")
    
    user_id = str(uuid.uuid4())
    print(f"测试用户ID: {user_id}")
    
    if TEST_MODE:
        print("[测试模式] 模拟余额: 1000 tokens")
        return 1000.0
    
    try:
        resp = requests.get(
            f"{BILLING_URL}/balance", 
            params={"user_id": user_id}, 
            headers=HEADERS,
            timeout=10
        )
        print(f"响应状态码: {resp.status_code}")
        print(f"响应内容: {resp.text}")
        
        balance = resp.json().get("balance", 0)
        print(f"[OK] 查询成功，余额: {balance} tokens")
        return balance
    except Exception as e:
        print(f"[ERROR] 查询异常: {e}")
        return 0

def test_get_payment_link():
    """测试获取支付链接接口"""
    print("\n=== 测试获取支付链接接口 ===")
    
    user_id = str(uuid.uuid4())
    print(f"测试用户ID: {user_id}")
    
    if TEST_MODE:
        print("[测试模式] 模拟支付链接")
        return "https://example.com/payment"
    
    try:
        resp = requests.post(
            f"{BILLING_URL}/payment-link", 
            headers=HEADERS, 
            json={
                "user_id": user_id, 
                "amount": 8,  # 最低充值8 USDT
            },
            timeout=10
        )
        print(f"响应状态码: {resp.status_code}")
        print(f"响应内容: {resp.text}")
        
        payment_url = resp.json().get("payment_url")
        if payment_url:
            print(f"[OK] 获取成功，支付链接: {payment_url}")
            return payment_url
        else:
            print("[ERROR] 获取支付链接失败")
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
    return None

if __name__ == "__main__":
    print("开始测试SkillPay SDK...")
    print("=" * 50)
    print(f"测试模式: {'开启' if TEST_MODE else '关闭'}")
    print(f"API路径: {BILLING_URL}")
    print(f"技能ID: {SKILL_ID}")
    print("=" * 50)
    
    # 测试扣费
    charge_result = test_charge_user()
    
    # 测试余额查询
    test_get_balance()
    
    # 测试获取支付链接
    test_get_payment_link()
    
    print("\n" + "=" * 50)
    print("测试完成!")
