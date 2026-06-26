import requests
import uuid
import sys

# SkillPay 配置 - 使用正确的API路径
SKILLPAY_API_KEY = 'sk_d11f398e77b6e892eb7a7d421fe912dde27322cf1792366b776b72bd459d3c2e'
# 使用用户提供的正确API路径
SKILLPAY_CREATE_ORDER_URL = 'https://skillpay.me/api/v1/billing/orders/create'
SKILLPAY_VERIFY_ORDER_URL = 'https://skillpay.me/api/v1/billing/orders/verify'

# 测试模式：设置为True可以模拟支付成功
TEST_MODE = False

def test_create_payment_order():
    """测试创建支付订单"""
    print("=== 测试创建支付订单 ===")
    
    if TEST_MODE:
        print("[测试模式] 模拟创建订单成功")
        mock_data = {
            'payment_url': 'https://example.com/payment/12345',
            'order_id': str(uuid.uuid4()),
            'status': 'pending'
        }
        print(f"模拟支付URL: {mock_data['payment_url']}")
        print(f"模拟订单ID: {mock_data['order_id']}")
        return mock_data, mock_data['order_id']
    
    order_id = str(uuid.uuid4())
    payload = {
        'api_key': SKILLPAY_API_KEY,
        'order_id': order_id,
        'amount': 0.001,
        'currency': 'USDT',
        'description': 'E-commerce Data Analyzer Test'
    }
    
    print(f"请求URL: {SKILLPAY_CREATE_ORDER_URL}")
    print(f"请求参数: api_key=***, order_id={order_id}, amount=0.001, currency=USDT")
    
    try:
        response = requests.post(SKILLPAY_CREATE_ORDER_URL, json=payload, timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("[OK] 创建订单成功!")
            print(f"支付URL: {data.get('payment_url')}")
            print(f"订单ID: {order_id}")
            return data, order_id
        else:
            print("[ERROR] 创建订单失败")
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
        print("提示: 请检查API域名是否正确，或使用TEST_MODE=True进行测试")
    
    return None, None

def test_verify_order(order_id):
    """测试验证支付订单"""
    print("\n=== 测试验证支付订单 ===")
    
    if TEST_MODE:
        print("[测试模式] 模拟验证订单成功")
        mock_data = {
            'status': 'success',
            'order_id': order_id,
            'amount': 0.001,
            'currency': 'USDT'
        }
        print(f"模拟订单状态: {mock_data['status']}")
        return mock_data
    
    payload = {
        'api_key': SKILLPAY_API_KEY,
        'order_id': order_id
    }
    
    print(f"请求URL: {SKILLPAY_VERIFY_ORDER_URL}")
    print(f"请求参数: api_key=***, order_id={order_id}")
    
    try:
        response = requests.post(SKILLPAY_VERIFY_ORDER_URL, json=payload, timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("[OK] 验证成功!")
            print(f"订单状态: {data.get('status')}")
            return data
        else:
            print("[ERROR] 验证失败")
    except Exception as e:
        print(f"[ERROR] 请求异常: {e}")
    
    return None

if __name__ == "__main__":
    print("开始测试SkillPay支付接口...")
    print("-" * 50)
    print(f"测试模式: {'开启' if TEST_MODE else '关闭'}")
    print(f"使用API路径: {SKILLPAY_CREATE_ORDER_URL}")
    
    if TEST_MODE:
        print("提示: 在实际使用前，请确认正确的SkillPay API域名")
        print("      并设置 TEST_MODE = False")
    print("-" * 50)
    
    # 测试创建订单
    order_data, order_id = test_create_payment_order()
    
    if order_id:
        # 测试验证订单
        test_verify_order(order_id)
    
    print("\n" + "-" * 50)
    print("测试完成!")
