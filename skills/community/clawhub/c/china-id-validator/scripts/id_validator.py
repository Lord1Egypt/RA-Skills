#!/usr/bin/env python3
"""Chinese ID Card (身份证) Validator & Info Extractor"""
import sys
import json
import re
from datetime import datetime

PROVINCE_CODES = {
    "11":"北京","12":"天津","13":"河北","14":"山西","15":"内蒙古",
    "21":"辽宁","22":"吉林","23":"黑龙江","31":"上海","32":"江苏",
    "33":"浙江","34":"安徽","35":"福建","36":"江西","37":"山东",
    "41":"河南","42":"湖北","43":"湖南","44":"广东","45":"广西",
    "46":"海南","50":"重庆","51":"四川","52":"贵州","53":"云南",
    "54":"西藏","61":"陕西","62":"甘肃","63":"青海","64":"宁夏",
    "65":"新疆","71":"台湾","81":"香港","82":"澳门","91":"国外"
}

WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
CHECK_CHARS = "10X98765432"

def validate(id_number):
    """Validate a Chinese ID card number (15 or 18 digits)"""
    id_number = id_number.strip().upper()
    
    if re.match(r'^\d{15}$', id_number):
        return validate_15(id_number)
    elif re.match(r'^\d{17}[\dX]$', id_number):
        return validate_18(id_number)
    else:
        return {"valid": False, "error": "格式错误：应为15位纯数字或18位数字+X"}

def validate_15(id_number):
    province = id_number[:2]
    if province not in PROVINCE_CODES:
        return {"valid": False, "error": f"无效省份代码: {province}"}
    try:
        datetime.strptime("19" + id_number[6:12], "%Y%m%d")
    except ValueError:
        return {"valid": False, "error": "无效出生日期"}
    return {
        "valid": True,
        "type": "15位",
        "province": PROVINCE_CODES[province],
        "province_code": province,
        "birthday": "19" + id_number[6:12],
        "gender": "女" if int(id_number[14]) % 2 == 0 else "男",
        "converted_18": convert_15_to_18(id_number)
    }

def validate_18(id_number):
    province = id_number[:2]
    if province not in PROVINCE_CODES:
        return {"valid": False, "error": f"无效省份代码: {province}"}
    try:
        birth = datetime.strptime(id_number[6:14], "%Y%m%d")
    except ValueError:
        return {"valid": False, "error": "无效出生日期"}
    
    # Check checksum
    total = sum(int(id_number[i]) * WEIGHTS[i] for i in range(17))
    check = CHECK_CHARS[total % 11]
    if check != id_number[17]:
        return {"valid": False, "error": f"校验码错误：末位应为{check}，实际为{id_number[17]}"}
    
    age = (datetime.now() - birth).days // 365
    return {
        "valid": True,
        "type": "18位",
        "province": PROVINCE_CODES[province],
        "province_code": province,
        "birthday": id_number[6:14],
        "age": age,
        "gender": "女" if int(id_number[16]) % 2 == 0 else "男",
        "checksum": id_number[17]
    }

def convert_15_to_18(id15):
    """Convert 15-digit ID to 18-digit"""
    id17 = "19" + id15[:6] + id15[6:]
    total = sum(int(id17[i]) * WEIGHTS[i] for i in range(17))
    return id17 + CHECK_CHARS[total % 11]

def generate(province_code, year, month, day, gender):
    """Generate a random valid ID number (for testing only)"""
    import random
    if province_code not in PROVINCE_CODES:
        return {"error": f"无效省份代码: {province_code}"}
    
    date_str = f"{year}{month.zfill(2)}{day.zfill(2)}"
    try:
        datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        return {"error": "无效日期"}
    
    city_county = f"{random.randint(1,99):02d}{random.randint(1,99):02d}"
    region = province_code + city_county[:4]  # 6-digit region code
    seq = random.randint(10, 99)
    gender_digit = random.choice([d for d in range(10) if d % 2 == (0 if gender == "女" else 1)])
    id17 = region + date_str + f"{seq}{gender_digit}"
    total = sum(int(id17[i]) * WEIGHTS[i] for i in range(17))
    return {"id_number": id17 + CHECK_CHARS[total % 11], "note": "仅供测试使用"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: id_validator.py <身份证号|validate|generate>", "examples": [
            "id_validator.py 110101199003077534",
            "id_validator.py validate 110101199003077534",
            "id_validator.py generate 11 1990 3 7 男"
        ]}, ensure_ascii=False, indent=2))
        return
    
    action = sys.argv[1]
    
    if action == "generate" and len(sys.argv) >= 7:
        result = generate(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif action in ("validate", "校验"):
        if len(sys.argv) < 3:
            result = {"error": "请提供身份证号"}
        else:
            result = validate(sys.argv[2])
    else:
        result = validate(action)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
