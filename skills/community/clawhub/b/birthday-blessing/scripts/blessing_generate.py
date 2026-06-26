#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生日祝福语生成服务 - 实际祝福语生成脚本
"""

import os
import sys
import json
import random
import re

# 添加脚本所在目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from file_utils import load_order, load_config
from sm4_utils import sm4_decrypt, is_valid_key
import base64


# 祝福语素材库
BLESSING_DATABASE = {
    "妈妈": [
        "亲爱的妈妈，祝您生日快乐！愿您永远年轻美丽，健康快乐，幸福常在！",
        "妈妈，您辛苦了！祝您生日快乐，愿您每一天都充满阳光和欢笑！",
        "祝妈妈福如东海长流水，寿比南山不老松，生日快乐！",
        "妈妈，感谢您一生的付出和无私的爱，祝您生日快乐，永远幸福！",
        "愿妈妈时光静好，岁月温柔，生日快乐，健康如意！"
    ],
    "爸爸": [
        "爸爸，您是我最坚强的依靠，祝您生日快乐，健康长寿！",
        "祝爸爸事业顺利，身体健康，生日快乐，您辛苦了！",
        "爸爸，您是我的英雄，祝您生日快乐，永远年轻！",
        "愿爸爸每一天都开心，每一年都健康，生日快乐！",
        "祝爸爸福寿绵长，生日快乐，永远幸福！"
    ],
    "朋友": [
        "祝你生日快乐！愿你的未来充满光明和希望，梦想成真！",
        "生日快乐！愿我们的友谊天长地久，永远不变！",
        "祝你新的一岁心想事成，万事如意，生日快乐！",
        "愿你的生日充满欢乐，愿你的每一天都精彩！生日快乐！",
        "朋友，生日快乐！愿你永远保持年轻的心态，追求自己的梦想！"
    ],
    "老师": [
        "老师，您辛苦了！祝您生日快乐，桃李满天下！",
        "祝愿老师春晖四方，寿比南山，生日快乐！",
        "老师，感谢您的教诲，祝您生日快乐，健康长寿！",
        "祝老师生活甜蜜，工作顺利，生日快乐！",
        "愿老师永远年轻漂亮，生日快乐，幸福美满！"
    ],
    "情侣": [
        "亲爱的，生日快乐！愿陪你度过每一个春夏秋冬！",
        "我愿陪你从青丝到白发，生日快乐，我的最爱！",
        "祝你生日快乐！愿我们的爱情永远甜蜜幸福！",
        "与你相识是我最大的幸运，生日快乐，我爱你！",
        "愿你的世界里只有幸福和快乐，生日快乐forever love！"
    ]
}

# 默认祝福语
DEFAULT_BLESSINGS = [
    "祝你生日快乐！愿你每一天都充满阳光和欢笑！",
    "生日快乐！愿你的梦想都能实现，生活更加精彩！",
    "祝你生日快乐！愿幸福和好运永远伴随着你！",
    "愿你的生日充满欢乐和惊喜，生日快乐！",
    "祝你新的一岁万事如意，心想事成，生日快乐！"
]


def extract_keyword(question: str) -> str:
    """从问题中提取关键词"""
    question = question.lower()
    
    keywords = {
        "妈妈": ["妈妈", "母亲", "妈"],
        "爸爸": ["爸爸", "父亲", "爸"],
        "朋友": ["朋友", "闺蜜", "兄弟", "同学"],
        "老师": ["老师", "老师", "教师"],
        "情侣": ["女朋友", "男朋友", "老婆", "老公", "爱人", "女友", "男友"]
    }
    
    for key, words in keywords.items():
        for word in words:
            if word in question:
                return key
    
    return ""


def generate_blessing(question: str) -> dict:
    """根据场景生成祝福语"""
    
    # 提取关键词
    keyword = extract_keyword(question)
    
    # 根据关键词选择祝福语
    if keyword and keyword in BLESSING_DATABASE:
        blessing = random.choice(BLESSING_DATABASE[keyword])
    else:
        blessing = random.choice(DEFAULT_BLESSINGS)
    
    result = {
        "祝福语": blessing,
        "对象": keyword if keyword else "通用"
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
        print("ERROR: 缺少参数，Usage: blessing_generate.py <order_no> <indicator>", file=sys.stderr)
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
        
        # 生成祝福语
        blessing = generate_blessing(question)
        
        # 输出结果
        print(f"PAY_STATUS: 成功")
        print(f"祝福语: {blessing['祝福语']}")
        
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
