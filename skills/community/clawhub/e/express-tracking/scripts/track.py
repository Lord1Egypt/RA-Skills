#!/usr/bin/env python3
"""快递查询脚本 - 使用快递100 API"""

import sys
import json
import hashlib
import urllib.request
import urllib.parse
import os

# 配置文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "..", "config.json")

# 快递公司编码映射（根据单号前缀自动识别）
COURIER_PATTERNS = {
    "shunfeng": ["SF"],
    "zhongtong": ["731", "732", "733", "734", "735", "736", "757", "758", "759", "761", "762", "763", "764", "765", "766", "767", "768", "769", "770", "771", "772", "773", "774", "775", "776", "777", "778", "779", "780", "ZT"],
    "yuantong": ["YT"],
    "yunda": ["46", "47", "48", "49", "YD"],
    "shentong": ["268", "368", "468", "568", "668", "768", "868", "968", "ST"],
    "jtexpress": ["JT"],
    "jd": ["JD"],
    "ems": ["EM"],
    "huitongkuaidi": ["550", "551", "552", "553", "554", "555", "556", "557", "558", "559", "560", "561", "562", "563", "564", "565", "566", "567", "568", "569", "570"],
}

COURIER_NAMES = {
    "shunfeng": "顺丰速运",
    "zhongtong": "中通快递",
    "yuantong": "圆通速递",
    "yunda": "韵达快递",
    "shentong": "申通快递",
    "jtexpress": "极兔速递",
    "jd": "京东物流",
    "ems": "邮政EMS",
    "huitongkuaidi": "百世快递",
}


def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def detect_courier(tracking_number):
    """根据单号前缀识别快递公司编码"""
    tn = tracking_number.upper()
    for code, prefixes in COURIER_PATTERNS.items():
        for prefix in prefixes:
            if tn.startswith(prefix.upper()):
                return code
    return None


def track_kuaidi100(key, customer, tracking_number, courier_code=None, phone=None):
    """使用快递100 API查询快递"""
    
    if not courier_code:
        courier_code = detect_courier(tracking_number)
        if not courier_code:
            print("❌ 无法自动识别快递公司，请手动指定")
            return None
    
    url = "https://poll.kuaidi100.com/poll/query.do"
    
    param = {
        "com": courier_code,
        "num": tracking_number,
        "phone": phone or "",
        "from": "",
        "to": "",
        "resultv2": "1",
        "show": "0",
        "order": "desc"
    }
    param_str = json.dumps(param, separators=(',', ':'))
    
    temp_sign = param_str + key + customer
    sign = hashlib.md5(temp_sign.encode()).hexdigest().upper()
    
    data = {
        "customer": customer,
        "param": param_str,
        "sign": sign
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(data).encode("utf-8"),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except Exception as e:
        return {"error": str(e)}


def format_result(result):
    """格式化查询结果"""
    if "error" in result:
        return f"❌ 查询失败: {result['error']}"
    
    if result.get("state") or result.get("status") == "200":
        lines = []
        courier_name = COURIER_NAMES.get(result.get("com", ""), result.get("com", "未知"))
        lines.append(f"📦 {courier_name}")
        lines.append(f"📌 单号: {result.get('nu', '')}")
        
        state_map = {"0": "运输中", "1": "揽件", "2": "疑难", "3": "已签收", "4": "退签", "5": "派件中", "6": "退回", "7": "转投"}
        state = state_map.get(str(result.get("state", "")), "未知")
        lines.append(f"📍 状态: {state}\n")
        
        data = result.get("data", [])
        if data:
            lines.append("📋 物流轨迹:")
            for i, item in enumerate(data[:15]):
                time = item.get("time", item.get("ftime", ""))
                context = item.get("context", "")
                icon = "📍" if i == 0 else "  "
                lines.append(f"{icon} {time} {context}")
            if len(data) > 15:
                lines.append(f"   ... 还有 {len(data) - 15} 条记录")
        
        return "\n".join(lines)
    
    return f"❌ 查询失败: {result.get('message', result.get('returnCode', '未知错误'))}"


def main():
    config = load_config()
    
    # 从配置读取 key/customer/default_phone
    key = config.get("key", "")
    customer = config.get("customer", "")
    default_phone = config.get("default_phone", "")
    
    if not key or not customer:
        print("❌ 请先配置 config.json")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("用法: track.py <快递单号> [快递公司编码] [手机号]")
        print("\n快递公司编码:")
        for code, name in COURIER_NAMES.items():
            print(f"  {code}: {name}")
        sys.exit(1)
    
    tracking_number = sys.argv[1]
    courier_code = sys.argv[2] if len(sys.argv) > 2 else None
    phone = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 顺丰默认使用配置的手机号
    if not phone and default_phone:
        tn_upper = tracking_number.upper()
        if tn_upper.startswith("SF") or courier_code == "shunfeng":
            phone = default_phone
    
    result = track_kuaidi100(key, customer, tracking_number, courier_code, phone)
    if result:
        print(format_result(result))


if __name__ == "__main__":
    main()