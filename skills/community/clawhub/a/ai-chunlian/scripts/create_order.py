import sys
import json
import base64
import os
import random
from datetime import datetime

from file_utils import save_order, load_config, get_db_connection, compute_indicator
from sm4_utils import sm4_encrypt, is_valid_key

# 硬编码的 slug，用于计算 indicator
SLUG = "ai-chunlian-v2"


def create_order(question: str, style: str = "彩虹屁") -> tuple:
    """
    创建订单，返回 (order_no, amount, encrypted_data, pay_to)
    """
    config = load_config()
    
    # 从配置获取
    sm4_key_b64 = config.get("crypto", {}).get("sm4_key")
    if not sm4_key_b64 or sm4_key_b64 == "YOUR_SM4_KEY_BASE64":
        raise RuntimeError("配置文件缺少 crypto.sm4_key，请先配置你的 SM4 密钥")
    
    try:
        sm4_key = base64.b64decode(sm4_key_b64)
    except Exception:
        raise RuntimeError("crypto.sm4_key 必须是有效的 Base64 编码")
    
    if not is_valid_key(sm4_key):
        raise RuntimeError("SM4 密钥必须为 16 字节")
    
    pay_to = config.get("payment", {}).get("pay_to")
    if not pay_to or pay_to == "YOUR_PAY_TO_VALUE":
        raise RuntimeError("配置文件缺少 payment.pay_to，请先配置你的收款账号")
    
    amount = config.get("service", {}).get("amount", 1)
    
    # 1) 生成订单号：时间戳 + 6位随机数
    order_no = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100000, 999999))
    
    # 2) 构建明文数据
    plain_dict = {
        "orderNo": order_no,
        "amount": amount,
        "payTo": pay_to
    }
    plain_text = json.dumps(plain_dict, ensure_ascii=False)
    
    # 3) SM4 加密（与 Java Hutool SM4.encryptBase64 兼容）
    encrypted_data = sm4_encrypt(plain_text, sm4_key)
    
    # 4) 订单落库
    conn = get_db_connection()
    now = datetime.now().isoformat()
    conn.execute('''
        INSERT INTO orders (order_no, question, style, amount, pay_to, order_status, fulfill_status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'INIT', 'UNFULFILLED', ?, ?)
    ''', (order_no, question, style, amount, pay_to, now, now))
    conn.commit()
    conn.close()
    
    return order_no, amount, encrypted_data, pay_to


def save_order_info(order_no: str, amount: str, question: str,
                    encrypted_data: str, pay_to: str, indicator: str, style: str) -> str:
    """
    Save order info to the fixed directory.
    Includes all fixed values needed by pre-verify-skill and dynamic values.
    Returns the full path of the saved JSON file.
    """
    order_data = {
        "skill-id": "si-clawpraise",
        "order_no": order_no,
        "amount": amount,
        "question": question,
        "style": style,
        "encrypted_data": encrypted_data,
        "pay_to": pay_to,
        "description": "花式夸夸服务费用",
        "slug": SLUG,
        "resource_url": "local",
    }
    return save_order(indicator, order_no, order_data)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create praise order")
    parser.add_argument("question", help="Target to praise")
    parser.add_argument("style", nargs="?", default="彩虹屁", help="Praise style")
    args = parser.parse_args()

    indicator = compute_indicator(SLUG)

    try:
        order_no, amount, encrypted_data, pay_to = create_order(args.question, args.style)
    except RuntimeError as e:
        print(f"订单创建失败: {e}")
        sys.exit(1)

    save_order_info(order_no, amount, args.question,
                    encrypted_data, pay_to, indicator, args.style)

    print(f"ORDER_NO={order_no}")
    print(f"AMOUNT={amount}")
    print(f"QUESTION={args.question}")
    print(f"INDICATOR={indicator}")
