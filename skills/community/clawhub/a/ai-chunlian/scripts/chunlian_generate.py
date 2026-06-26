#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
春联生成服务 - 实际春联生成脚本
"""

import os
import sys
import json
import random
import base64
from datetime import datetime

# 添加脚本所在目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from file_utils import load_order, load_config
from sm4_utils import sm4_decrypt, is_valid_key


# 春联素材库
CHUNLIAN_DATABASE = {
    "春节大门": {
        "横批": ["迎春接福", "万象更新", "春满人间", "喜气盈门", "国泰民安"],
        "上联": ["春风得意财源广", "春回大地万物苏", "春满乾坤福满门", "春到人间百花艳", "春意盎然庆丰年"],
        "下联": ["和气生财万象新", "福照家门万事兴", "天增岁月人增寿", "福满人间喜事多", "家和业旺步步高"]
    },
    "乔迁新居": {
        "横批": ["乔迁之喜", "福地呈祥", "安居乐业", "喜迁新居", "金玉满堂"],
        "上联": ["乔迁喜天地人和", "新居落成万事兴", "迁入新居添福寿", "华厦落成千秋盛", "新宅第里沐春风"],
        "下联": ["福照家兴事业隆", "福星高照满堂春", "福到福来福永随", "门庭和顺万般好", "喜气洋洋庆有余"]
    },
    "开业大吉": {
        "横批": ["开业大吉", "财源广进", "生意兴隆", "大展宏图", "鹏程万里"],
        "上联": ["开业大吉四方客", "生意兴隆通四海", "财源茂盛达三江", "开业呈祥财运到", "商战得意马蹄急"],
        "下联": ["财星高照旺百财", "财路亨通步步高", "金银满钵事业成", "宾客盈门富贵来", "日进斗金创辉煌"]
    },
    "婚礼祝福": {
        "横批": ["百年好合", "永结同心", "花好月圆", "佳偶天成", "白头偕老"],
        "上联": ["百年修得同船渡", "两情相悦结连理", "百年好合鸳鸯配", "花开并蒂结同心", "执子之手与子老"],
        "下联": ["千年修得共枕眠", "万载良缘系红绳", "龙凤呈祥庆良缘", "喜结连理永不分离", "相濡以沫度终身"]
    }
}

# 默认春联
DEFAULT_CHUNLIAN = {
    "横批": ["万事如意", "心想事成", "吉星高照"],
    "上联": ["春到江南花似锦", "春回大地万象新", "春风送暖百花开"],
    "下联": ["福临塞北月如银", "福满乾坤喜盈门", "福星高照耀前程"]
}


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


def generate_chunlian(scene: str) -> dict:
    """根据场景生成春联"""
    
    # 尝试匹配场景
    matched_data = None
    for key in CHUNLIAN_DATABASE:
        if key in scene or scene in key:
            matched_data = CHUNLIAN_DATABASE[key]
            break
    
    # 如果没有匹配，使用默认春联
    if matched_data is None:
        matched_data = DEFAULT_CHUNLIAN
    
    # 随机选择
    result = {
        "横批": random.choice(matched_data["横批"]),
        "上联": random.choice(matched_data["上联"]),
        "下联": random.choice(matched_data["下联"]),
        "场景": scene
    }
    
    return result


def main():
    if len(sys.argv) < 3:
        print("ERROR: 缺少参数，Usage: chunlian_generate.py <order_no> <indicator>", file=sys.stderr)
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
        
        # 生成春联
        chunlian = generate_chunlian(question)
        
        # 输出结果
        print(f"PAY_STATUS: 成功")
        print(f"横批: {chunlian['横批']}")
        print(f"上联: {chunlian['上联']}")
        print(f"下联: {chunlian['下联']}")
        
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
