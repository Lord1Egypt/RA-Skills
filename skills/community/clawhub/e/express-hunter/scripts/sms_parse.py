"""
快递短信解析脚本
用法: python sms_parse.py "<短信全文>"
自动提取快递单号和快递公司，加入追踪列表
"""
import sys, json, os, re
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

DATA_DIR = "G:/PC先生/express_data"
PACKAGES_FILE = os.path.join(DATA_DIR, "packages.json")

# 快递公司关键词匹配
COURIER_KEYWORDS = [
    ("顺丰", "shunfeng", "顺丰速运"),
    ("圆通", "yuantong", "圆通速递"),
    ("中通", "zhongtong", "中通快递"),
    ("申通", "shentong", "申通快递"),
    ("韵达", "yunda", "韵达快递"),
    ("百世", "huitongkuaidi", "百世汇通"),
    ("EMS", "ems", "EMS"),
    ("邮政", "youzhengguonei", "邮政包裹"),
    ("京东", "jd", "京东物流"),
    ("极兔", "jtexpress", "极兔速递"),
    ("德邦", "debangwuliu", "德邦物流"),
    ("天天", "tiantian", "天天快递"),
    ("宅急送", "zhaijisong", "宅急送"),
    ("优速", "youshuwuliu", "优速快递"),
    ("安能", "annengwuliu", "安能物流"),
    ("丹鸟", "danniao", "丹鸟物流"),
    ("菜鸟", "cainiao", "菜鸟裹裹"),
    ("丰网", "fengwang", "丰网速运"),
]

# 常见快递单号格式（正则）
TRACKING_PATTERNS = [
    # 顺丰: SF + 12位数字
    (r'SF\d{12,14}', 'shunfeng', '顺丰速运'),
    # 中通: 7开头/75开头 + 数字 或 ZT开头
    (r'(?:ZT|zt)\d{10,15}', 'zhongtong', '中通快递'),
    # 圆通: YT开头 + 数字
    (r'(?:YT|yt)\d{10,15}', 'yuantong', '圆通速递'),
    # 韵达: 4开头或YD开头
    (r'(?:YD|yd)\d{10,15}', 'yunda', '韵达快递'),
    # 申通: 7开头或STO开头
    (r'(?:STO|sto)\d{10,15}', 'shentong', '申通快递'),
    # EMS: 13位数字，通常以1开头
    (r'\b[1-9]\d{12}\b', 'ems', 'EMS'),
    # 京东: JD开头 + 数字
    (r'(?:JD|jd|JDV|jdv)[A-Za-z0-9]{10,18}', 'jd', '京东物流'),
    # 极兔: JT开头
    (r'(?:JT|jt)\d{10,15}', 'jtexpress', '极兔速递'),
    # 德邦: DP开头 或 DPK开头
    (r'(?:DP|dp|DPK|dpk)\d{8,15}', 'debangwuliu', '德邦物流'),
    # 通用: 连续10-20位数字+字母组合（谨慎匹配，避免手机号）
    (r'(?<!\d)[A-Za-z0-9]{10,20}(?!\d)', None, None),
]

def load_packages():
    if os.path.exists(PACKAGES_FILE):
        with open(PACKAGES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"packages": []}

def save_packages(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PACKAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_valid_tracking(tn):
    """验证是否为合理的快递单号"""
    # 纯数字至少10位
    if tn.isdigit() and len(tn) >= 10:
        # 过滤掉手机号（11位1开头纯数字）
        if len(tn) == 11 and tn.startswith("1"):
            return False
        return True
    # 字母+数字
    if re.match(r'^[A-Za-z]{2,4}\d{8,15}$', tn):
        return True
    # JD特殊格式
    if re.match(r'^JD[A-Za-z0-9]{10,18}$', tn):
        return True
    return False

def parse_sms(text):
    """解析短信内容，提取快递信息"""
    result = {"found": [], "raw": text}
    used_numbers = set()
    
    # 先尝试识别快递公司
    detected_courier = None
    for keyword, code, name in COURIER_KEYWORDS:
        if keyword in text:
            detected_courier = (code, name)
            break
    
    # 再提取单号
    for pattern, courier_code, courier_name in TRACKING_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            tn = match.strip().upper() if isinstance(match, str) else match
            if tn in used_numbers:
                continue
            if not is_valid_tracking(tn):
                continue
            
            used_numbers.add(tn)
            
            # 优先使用模式匹配的快递公司，其次短信关键词检测的
            if courier_code and courier_name:
                result["found"].append({
                    "tracking_number": tn,
                    "courier_code": courier_code,
                    "courier_name": courier_name,
                })
            elif detected_courier:
                result["found"].append({
                    "tracking_number": tn,
                    "courier_code": detected_courier[0],
                    "courier_name": detected_courier[1],
                })
            else:
                result["found"].append({
                    "tracking_number": tn,
                    "courier_code": "auto",
                    "courier_name": "自动识别",
                })
    
    return result

def add_to_tracking(tracking_number, courier_code="auto", courier_name="自动识别", label=""):
    """添加到追踪列表"""
    data = load_packages()
    
    # 检查是否已存在
    for pkg in data["packages"]:
        if pkg["tracking_number"] == tracking_number:
            return {"added": False, "reason": "已在追踪列表中", "tracking_number": tracking_number}
    
    now = datetime.now().isoformat()
    data["packages"].append({
        "tracking_number": tracking_number,
        "courier_code": courier_code,
        "courier_name": courier_name,
        "label": label,
        "added_at": now,
        "last_status": "待查询",
        "last_update": now,
        "traces": [],
        "delivered": False
    })
    
    save_packages(data)
    return {"added": True, "tracking_number": tracking_number, "courier": courier_name}

def main():
    if len(sys.argv) < 2:
        print("用法: python sms_parse.py \"<短信全文>\"")
        print("示例: python sms_parse.py \"【顺丰】您的快递SF123456789012已发出\"")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    
    # 解析
    result = parse_sms(text)
    
    if not result["found"]:
        print("❌ 未识别到快递信息，请检查短信内容")
        print(f"   短信内容: {text[:50]}...")
        sys.exit(1)
    
    added_list = []
    for item in result["found"]:
        r = add_to_tracking(
            item["tracking_number"],
            item["courier_code"],
            item["courier_name"]
        )
        added_list.append(r)
    
    if not added_list:
        print("❌ 所有单号已在追踪列表中")
        sys.exit(1)
    
    # 输出结果
    for item in added_list:
        if item["added"]:
            print(f"✅ 已添加: {item['courier']} {item['tracking_number']}")
        else:
            print(f"⏭️ 跳过: {item['tracking_number']} ({item['reason']})")
    
    print(f"\n共识别 {len(result['found'])} 个快递，新增 {sum(1 for a in added_list if a['added'])} 个")

if __name__ == "__main__":
    main()
