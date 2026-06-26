#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝宝取名服务 - 实际取名生成脚本
"""

import os
import sys
import json
import random

# 添加脚本所在目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from file_utils import load_order, load_config
from sm4_utils import sm4_decrypt, is_valid_key
import base64


# 名字素材库
NAME_DATABASE = {
    "男": {
        "单字": ["宇", "轩", "浩", "博", "睿", "哲", "俊", "豪", "明", "晨", "旭", "昊", "文", "武", "承", "继"],
        "双字": ["梓涵", "子墨", "一诺", "浩然", "博文", "宇轩", "明哲", "俊豪", "博远", "睿哲", "天佑", "子涵"]
    },
    "女": {
        "单字": ["雅", "婷", "萱", "欣", "雨", "雪", "梅", "兰", "竹", "菊", "琴", "诗", "画", "玉", "珍", "莉"],
        "双字": ["思雨", "诗涵", "雅婷", "欣怡", "雪晴", "雨晴", "诗琪", "雅楠", "欣悦", "思琪", "语桐", "诗桐"]
    }
}


def detect_gender(question: str) -> str:
    """检测性别"""
    question = question.lower()
    
    if "男" in question or "儿子" in question or "公子" in question:
        return "男"
    elif "女" in question or "女儿" in question or "千金" in question:
        return "女"
    else:
        return random.choice(["男", "女"])


def generate_names(gender: str, count: int = 5) -> list:
    """生成名字列表"""
    if gender == "男":
        names = NAME_DATABASE["男"]["双字"][:count]
    else:
        names = NAME_DATABASE["女"]["双字"][:count]
    
    # 如果不够，随机补充
    while len(names) < count:
        all_names = NAME_DATABASE[gender]["双字"]
        name = random.choice(all_names)
        if name not in names:
            names.append(name)
    
    return names[:count]


def generate_name(question: str) -> dict:
    """根据需求生成名字"""
    
    # 检测性别
    gender = detect_gender(question)
    
    # 生成名字
    names = generate_names(gender, 5)
    
    result = {
        "名字": names,
        "性别": gender,
        "寓意": "吉祥如意，前程似锦"
    }
    
    return result


def verify_payment(order_no: str, credential: str) -> tuple:
    """
    验证支付凭证
    返回 (pay_status, error_info)
    """
    config = load_config()
    sm4_key_b64 = config.get("crypto", {}).get("sm4_key")
    
    if not sm4_key_b64:
        return ("ERROR", "配置文件缺少 crypto.sm4_key")
    
    try:
        sm4_key = base64.b64decode(sm4_key_b64)
    except Exception:
        return ("ERROR", "crypto.sm4_key 必须是有效的 Base64 编码")
    
    if not is_valid_key(sm4_key):
        return ("ERROR", "SM4 密钥必须为 16 字节")
    
    # 解密支付凭据
    try:
        decrypted = sm4_decrypt(credential, sm4_key)
    except Exception as e:
        return ("ERROR", f"支付凭证解密失败: {e}")
    
    # 解析支付状态
    pay_status = "PENDING"
    try:
        root = json.loads(decrypted)
        pay_status = root.get("payStatus", "PENDING")
    except Exception:
        pass
    
    # 检查支付是否成功
    if pay_status.upper() != "SUCCESS":
        return (pay_status, f"支付未成功，状态: {pay_status}")
    
    return ("SUCCESS", "")


def main():
    if len(sys.argv) < 3:
        print("ERROR: 缺少参数，Usage: name_generate.py <order_no> <indicator>", file=sys.stderr)
        print("PAY_STATUS: ERROR")
        print("ERROR_INFO: 缺少参数")
        sys.exit(1)
    
    order_no = sys.argv[1]
    indicator = sys.argv[2]  # 从命令行参数获取indicator
    
    try:
        # 加载订单信息
        order_data = load_order(indicator, order_no)
        
        # 获取问题/场景描述
        question = order_data.get('question', '')
        
        # 获取支付凭证
        credential = order_data.get('payCredential', '')
        if not credential:
            print("PAY_STATUS: ERROR")
            print("ERROR_INFO: 未完成支付，请先完成支付流程")
            sys.exit(1)
        
        # 验证支付
        pay_status, error_info = verify_payment(order_no, credential)
        
        if pay_status == "ERROR":
            print(f"PAY_STATUS: ERROR")
            print(f"ERROR_INFO: {error_info}")
            sys.exit(1)
        
        if pay_status != "SUCCESS":
            print(f"PAY_STATUS: {pay_status}")
            print(f"ERROR_INFO: {error_info}")
            sys.exit(1)
        
        # 生成名字
        name_result = generate_name(question)
        
        # 输出结果
        print(f"PAY_STATUS: 成功")
        print(f"推荐名字: {', '.join(name_result['名字'])}")
        
    except FileNotFoundError as e:
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: 订单文件不存在")
        sys.exit(1)
    except Exception as e:
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
