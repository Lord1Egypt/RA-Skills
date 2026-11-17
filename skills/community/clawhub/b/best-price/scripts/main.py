"""购物比价助手 - 跨京东/天猫双平台比价，支持关键词搜索。"""

import os
import json
import re
import socket
import urllib.request
from typing import Optional

# ============ SCF代理配置 ============
_PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "tp_8k2mX9vQ4z")
PROXIES = {
    "jd": {
        "url": "https://1439498936-9n7zsjnaif.ap-guangzhou.tencentscf.com",
        "token": _PROXY_TOKEN,
    },
    "taobao": {
        "url": "https://1439498936-lofjio3yzf.ap-guangzhou.tencentscf.com",
        "token": _PROXY_TOKEN,
    },
}
PROXY_TIMEOUT = 15

# ============ 非标品关键词 ============
NON_STANDARD_KEYWORDS = [
    "t恤", "polo衫", "衬衫", "裙子", "裤子", "牛仔裤", "外套", "大衣",
    "毛衣", "卫衣", "风衣", "棉服", "羽绒服", "西服", "西装", "短裤",
    "内衣", "睡衣", "秋裤", "马甲", "开衫", "针织衫", "雪纺", "连衣裙",
    "半身裙", "夹克", "棒球服", "小香风", "国风", "唐装",
    "高跟鞋", "皮鞋", "凉鞋", "拖鞋", "平底鞋", "帆布鞋", "豆豆鞋",
    "老爹鞋", "穆勒鞋",
    "手提包", "单肩包", "斜挎包", "双肩包", "手包", "腰包", "腋下包",
    "耳环", "耳钉", "项链", "手链", "戒指", "发饰", "胸针", "手镯",
    "脚链", "吊坠",
    "挂画", "花瓶", "摆件", "抱枕", "地毯", "窗帘", "墙贴", "烛台",
    "装饰画", "干花",
    "定制", "手工", "刻字",
]

# ============ 品类关键词 ============
CATEGORY_KEYWORDS = [
    "手机", "智能手表", "手表", "平板", "平板电脑", "笔记本", "笔记本电脑",
    "显示器", "打印机", "硬盘", "内存", "显卡", "耳机", "相机", "投影仪",
    "投影", "游戏机", "游戏主机", "路由器", "键盘", "鼠标", "键盘鼠标",
    "扫地机器人", "扫地机", "电视", "冰箱", "洗衣机", "空调", "热水器",
    "吹风机", "剃须刀", "电动牙刷", "牙刷", "净化器", "空气净化器",
    "净水器", "破壁机", "空气炸锅", "炸锅", "电饭煲", "运动鞋", "包",
    "香水", "酒", "名酒", "奶粉", "纸尿裤", "图书", "粮油",
    "switch", "ps5", "xbox",
]

# ============ 型号指示符 ============
MODEL_PATTERN = re.compile(
    r"\d+|\d+[GTgt][Bb]?|\bPro\b|\bMax\b|\bPlus\b|\bUltra\b|\bMini\b"
    r"|\bSE\b|\bLite\b|\bAir\b|\bStudio\b",
    re.IGNORECASE,
)

# ============ 配件关键词 ============
ACCESSORY_KEYWORDS = [
    "充电器", "充电头", "数据线", "保护套", "手机壳", "贴膜", "钢化膜", "手机膜",
    "支架", "转接头", "扩展坞", "适配器", "电源适配", "快充头", "充电线",
    "耳机套", "表带", "保护壳", "保护膜", "键盘膜", "屏幕膜",
    "展示盒", "展示机", "模型", "模型机", "空盒", "包装盒", "仿真",
    "安装服务", "延保", "碎屏险", "维修",
    "遥控器", "滤网", "滤芯", "替换", "配件", "底座", "挂架",
    "纸巾", "抽纸", "卫生纸", "垃圾袋", "洗衣液",
    "后盖", "电池盖", "外壳", "屏幕外观", "边框", "面壳",
    "内屏", "外屏", "总成", "排线",
    "电池", "集尘桶", "尘袋", "滚刷", "吸头", "软管", "接头",
]

# ============ 品牌库 ============
KNOWN_BRANDS = {
    "apple", "iphone", "ipad", "macbook", "samsung", "huawei", "xiaomi", "redmi",
    "oppo", "vivo", "oneplus", "honor",
    "lenovo", "thinkpad", "dell", "hp", "asus", "rog",
    "sony", "nintendo",
    "dyson", "philips", "panasonic",
    "roborock", "ecovacs", "dreame",
    "hisense", "tcl", "gree", "midea", "haier", "siemens",
    "nike", "adidas", "lining", "anta",
    "lv", "louis vuitton", "gucci", "chanel", "prada", "dior", "hermes",
    "rolex", "omega", "casio",
    "maotai", "moutai", "wuliangye",
    "aptamil", "friso", "feihe",
    "pampers", "merries",
    # 中文
    "华为", "苹果", "小米", "三星", "荣耀", "一加",
    "联想", "戴尔", "惠普", "华硕",
    "索尼", "松下", "飞利浦",
    "美的", "格力", "海尔", "海信", "西门子",
    "戴森", "石头", "科沃斯", "追觅",
    "耐克", "阿迪达斯", "李宁", "安踏",
    "劳力士", "欧米茄", "卡西欧",
    "茅台", "五粮液",
    "飞鹤", "帮宝适", "大王",
}

# ============ 中文→英文品牌映射 ============
BRAND_CN_MAP = {
    "huawei": "华为", "apple": "苹果", "xiaomi": "小米", "samsung": "三星",
    "honor": "荣耀", "oneplus": "一加",
    "lenovo": "联想", "dell": "戴尔", "hp": "惠普", "asus": "华硕",
    "sony": "索尼", "panasonic": "松下", "philips": "飞利浦",
    "midea": "美的", "gree": "格力", "haier": "海尔", "hisense": "海信",
    "siemens": "西门子",
    "dyson": "戴森",
    "roborock": "石头", "ecovacs": "科沃斯", "dreame": "追觅",
    "nike": "耐克", "adidas": "阿迪达斯", "lining": "李宁", "anta": "安踏",
    "rolex": "劳力士", "omega": "欧米茄", "casio": "卡西欧",
    "maotai": "茅台", "moutai": "茅台", "wuliangye": "五粮液",
    "feihe": "飞鹤",
    "pampers": "帮宝适", "merries": "大王",
}

# ============ 子品牌→归一化品牌 ============
BRAND_CANONICAL = {
    "iphone": "apple", "ipad": "apple", "macbook": "apple",
    "galaxy": "samsung", "redmi": "xiaomi",
    "rog": "asus", "thinkpad": "lenovo",
    # 中文品牌→英文归一化
    "华为": "huawei", "苹果": "apple", "小米": "xiaomi", "三星": "samsung",
    "荣耀": "honor", "一加": "oneplus",
    "联想": "lenovo", "戴尔": "dell", "惠普": "hp", "华硕": "asus",
    "索尼": "sony", "松下": "panasonic", "飞利浦": "philips",
    "美的": "midea", "格力": "gree", "海尔": "haier", "海信": "hisense",
    "西门子": "siemens", "戴森": "dyson",
    "石头": "roborock", "科沃斯": "ecovacs", "追觅": "dreame",
    "耐克": "nike", "阿迪达斯": "adidas", "李宁": "lining",
    "劳力士": "rolex", "欧米茄": "omega", "卡西欧": "casio",
    "茅台": "maotai", "五粮液": "wuliangye",
    "飞鹤": "feihe", "帮宝适": "pampers", "大王": "merries",
}

# ============ 品牌→默认品类推断 ============
BRAND_CATEGORY_MAP = {
    "apple": "手机", "iphone": "手机", "ipad": "平板", "macbook": "笔记本",
    "samsung": "手机", "huawei": "手机", "xiaomi": "手机", "redmi": "手机",
    "oppo": "手机", "vivo": "手机", "oneplus": "手机", "honor": "手机",
    "lenovo": "笔记本", "thinkpad": "笔记本", "dell": "笔记本", "hp": "笔记本", "asus": "笔记本",
    "sony": "耳机", "nintendo": "游戏机",
    "dyson": "吸尘器", "philips": "剃须刀", "panasonic": "剃须刀",
    "roborock": "扫地机器人", "ecovacs": "扫地机器人", "dreame": "扫地机器人",
    "hisense": "电视", "tcl": "电视", "gree": "空调", "midea": "空调", "haier": "冰箱",
    "siemens": "冰箱",
    "nike": "运动鞋", "adidas": "运动鞋",
    "rolex": "手表", "omega": "手表", "casio": "手表",
    "maotai": "酒", "moutai": "酒", "wuliangye": "酒",
    "aptamil": "奶粉", "friso": "奶粉", "feihe": "奶粉",
    "pampers": "纸尿裤", "merries": "纸尿裤",
    "华为": "手机", "苹果": "手机", "小米": "手机", "三星": "手机",
    "荣耀": "手机", "一加": "手机",
    "戴森": "吸尘器", "石头": "扫地机器人", "科沃斯": "扫地机器人", "追觅": "扫地机器人",
    "美的": "空调", "格力": "空调", "海尔": "冰箱",
    "耐克": "运动鞋", "阿迪达斯": "运动鞋",
    "茅台": "酒", "五粮液": "酒",
    "飞鹤": "奶粉", "帮宝适": "纸尿裤", "大王": "纸尿裤",
}

# ============ 提示语 ============
HINT_LINK = "暂时无法从链接中读取商品信息。请复制商品标题发送给我，我来帮你天猫+京东比价找最低价！"
HINT_PDD_LINK = "拼多多暂不支持比价，目前支持天猫和京东双平台比价。如需查询该商品在天猫/京东的价格，请复制商品标题发送给我！"
HINT_NON_STANDARD = "暂不支持该品类商品的比价。我们支持3C数码、家电、品牌鞋包表、香水、名酒、母婴、图书、品牌粮油等37个标品品类的比价。如需比价，请选择这些品类中的商品，复制商品标题发给我试试！"
HINT_VAGUE = "请打开商品页面，长按商品标题复制发给我，我来帮你天猫+京东比价找最低价！只需3步：打开商品页→长按标题→复制粘贴给我。"

def _safe_str(val, default=""):
    """防御None和'None'字符串"""
    if val is None or val == "None":
        return default
    try:
        s = str(val).strip()
        return s if s else default
    except Exception:
        return default

def _safe_float(val):
    """安全转float，失败返回None"""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        if "-" in val and re.match(r"\d+\.?\d*\s*-\s*\d+\.?\d*", val):
            try:
                return float(val.split("-")[0].strip())
            except (ValueError, IndexError):
                return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None
    return None

# ============ SCF代理调用 ============
def _scf_call(proxy_key: str, req_type: str, params: dict) -> dict:
    """调用SCF代理接口"""
    proxy = PROXIES[proxy_key]
    payload = json.dumps({"type": req_type, "params": params}).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-Proxy-Token": proxy["token"]}
    req = urllib.request.Request(proxy["url"], data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=PROXY_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data if data else {}
    except (socket.timeout, TimeoutError):
        return {"ok": False, "error": "timeout"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def _extract_items(data: dict) -> list:
    """从SCF响应中提取商品列表"""
    if not isinstance(data, dict) or not data.get("ok"):
        return []
    items = data.get("data", [])
    if isinstance(items, list):
        return items
    if isinstance(items, dict):
        for key in ("result", "items", "list"):
            val = items.get(key, [])
            if isinstance(val, list):
                return val
    return []

# ============ 链接检测 ============
def _detect_link_type(query: str) -> str:
    """检测文本是否包含电商链接特征，返回'pdd_link'/'link'/'none'"""
    if re.search(r"(yangkeduo\.com|pinduoduo\.com)", query):
        return "pdd_link"
    if re.search(r"(3\.cn|jd\.com|tb\.cn|taobao\.com|tmall\.com)", query):
        return "link"
    return "none"

def _clean_url_from_text(text: str) -> str:
    """从文本中提取URL（噪音清洗辅助）"""
    m = re.search(r"https?://[^\s<>\"']+", text)
    return m.group(0) if m else text

# ============ 噪音清洗 ============
def _clean_noise(text: str) -> str:
    """去emoji/促销前缀/口令码/URL，不拆分品牌型号"""
    text = re.sub(r"[🧧💰🎁🎉🔥💯✨🌟⭐🛒🏠🎊💸🉐👑💎🏷️📦🚚👍✅🎊🎈🎀🛍️🖤💛🤍💚💙💜🩷🩵🩶❤️🧡💗💖💝💘💕]", "", text)
    text = re.sub(r"【[^】]*】", "", text)
    text = re.sub(
        r"限时[特优折扣降]惠?|限时秒杀|限时抢购|限时特价|限时福利"
        r"|特惠|秒杀|抢购|特价|福利|直降|立减|到手价"
        r"|政府补贴[^，。！\s]*|国补[^，。！\s]*"
        r"|新品首发|新品上市|新品特惠"
        r"|限量版|限量发售|限量供应"
        r"|爆款|热卖|畅销|热销"
        r"|包邮|满减|满赠|买一送一"
        r"|官方正品|正品保障|正品行货"
        r"|晒单[^，。！\s]*|好评返现|好评领红包",
        "", text)
    text = re.sub(r"\b(?:HU|MU|CZ|MF|JD)\d{3,}\b", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"点击链接.*$", "", text)
    text = re.sub(r"[!！~～]{2,}", "", text)
    text = re.sub(r"\s*[!！]\s*", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def _is_non_standard(query: str) -> bool:
    """非标品品类检测"""
    q = query.lower()
    return any(kw in q for kw in NON_STANDARD_KEYWORDS)

# ============ 品牌提取 ============
def _extract_brand(query: str) -> Optional[str]:
    """提取并归一化品牌名"""
    q = query.lower()
    for brand in sorted(KNOWN_BRANDS, key=len, reverse=True):
        if brand in q:
            return BRAND_CANONICAL.get(brand, brand)
    return None

def _has_category_keyword(query: str) -> bool:
    q = query.lower()
    return any(cat in q for cat in CATEGORY_KEYWORDS)

def _has_model_indicator(query: str) -> bool:
    if MODEL_PATTERN.search(query):
        return True
    if re.search(r"[A-Za-z]+\d+", query):
        return True
    if re.search(r"\d+[A-Za-z]+", query):
        return True
    return False

def _is_vague_input(query: str) -> bool:
    """检测模糊输入（品牌+品类无型号）"""
    has_brand = _extract_brand(query) is not None
    has_category = _has_category_keyword(query)
    has_model = _has_model_indicator(query)
    if has_model:
        return False
    if has_brand and has_category:
        return True
    if has_category and not has_brand:
        return True
    if has_brand and not has_category:
        return True
    return False

# ============ 辅助函数 ============
def _parse_sales_tip(sales_tip) -> float:
    """解析销量文本如'1.5万+'"""
    if not sales_tip or not isinstance(sales_tip, str):
        return 0
    s = sales_tip.strip().rstrip("+")
    try:
        if "万" in s:
            return float(s.replace("万", "")) * 10000
        return float(s)
    except (ValueError, TypeError):
        return 0

def _parse_coupon_amount(coupon_info):
    """从优惠券文本提取减免金额"""
    if not coupon_info or not isinstance(coupon_info, str):
        return 0
    m = re.search(r"减(\d+\.?\d*)", coupon_info)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d+\.?\d*)元(?:优惠)?券", coupon_info)
    if m:
        return float(m.group(1))
    return 0

def _compute_final_price(price, final_price_raw, coupon_discount=None, coupon_min_order=None):
    """计算到手价，返回(final_price, saved)"""
    p = _safe_float(price)
    fp_raw = _safe_float(final_price_raw)
    cd = _safe_float(coupon_discount)
    cm = _safe_float(coupon_min_order)
    if fp_raw is not None and p is not None and fp_raw < p and fp_raw > 0:
        saved = round(p - fp_raw, 2)
        return fp_raw, saved
    if cd and cd > 0 and p is not None:
        if cm and p < cm:
            return p, 0
        computed_fp = round(p - cd, 2)
        if computed_fp > 0:
            return computed_fp, cd
    if p is not None:
        fp = fp_raw if fp_raw is not None and fp_raw > 0 and fp_raw <= p else p
        saved = round(p - fp, 2) if fp < p else 0
        return fp, saved
    return fp_raw, 0

def _is_accessory(name: str) -> bool:
    if not name:
        return False
    return any(kw in name for kw in ACCESSORY_KEYWORDS)

def _relevance_score(name: str, keyword: str) -> float:
    """计算名称与关键词的相关性(0-1)"""
    if not name or not keyword:
        return 0.0
    name_lower = name.lower()
    keyword_lower = keyword.lower()
    if keyword_lower in name_lower:
        return 1.0
    tokens = [t for t in re.split(r"\s+", keyword_lower) if len(t) > 1]
    if tokens:
        matched = sum(1 for t in tokens if t in name_lower or re.sub(r"b$", "", t) in name_lower)
        token_score = matched / len(tokens)
        if token_score > 0:
            return token_score
    if len(keyword_lower) >= 2:
        sub_matches = 0
        sub_total = 0
        for i in range(len(keyword_lower) - 1):
            sub = keyword_lower[i:i+2]
            if any(c.isalpha() or "\u4e00" <= c <= "\u9fff" for c in sub):
                sub_total += 1
                if sub in name_lower:
                    sub_matches += 1
        if sub_total > 0:
            return sub_matches / sub_total
    return 0.0

def _model_number_matches(name: str, keyword: str) -> bool:
    """检查商品名是否包含关键词中的型号数字，防止17被当成16"""
    nums = re.findall(r"(?<=[a-zA-Z\u4e00-\u9fff\s])(\d{1,4})(?=[a-zA-Z\s\u4e00-\u9fff]|$)", keyword)
    model_nums = [n for n in nums if n not in ("128", "256", "512", "1024")]
    if not model_nums:
        return True
    for num in model_nums:
        if not re.search(r"(?<!\d)" + num + r"(?!\d)", name.lower()):
            return False
    return True

def _has_sub_brand_conflict(query: str, product_name: str) -> bool:
    """检测查询品牌与商品名的子品牌冲突（如搜'小米14'却返回'红米14C'）"""
    q = query.lower()
    n = product_name.lower()
    # 小米 vs 红米/Redmi
    if ("小米" in q or "xiaomi" in q) and ("红米" in n or "redmi" in n):
        if "红米" not in q and "redmi" not in q:
            return True
    # 华为 vs 荣耀/Honor
    if ("华为" in q or "huawei" in q) and ("荣耀" in n or "honor" in n):
        if "荣耀" not in q and "honor" not in q:
            return True
    return False

def _is_brand_mismatch(query_brand: str, product_name: str) -> bool:
    """检测品牌不一致：query品牌与商品属于另一个已知品牌（非子品牌关系）"""
    if not query_brand:
        return False
    n = product_name.lower()
    qb = query_brand.lower()
    # 归一化query品牌
    qb_norm = BRAND_CANONICAL.get(qb, qb)
    # 检查商品名是否属于另一个已知品牌（排除query品牌自身及其子品牌）
    for brand in KNOWN_BRANDS:
        b_norm = BRAND_CANONICAL.get(brand, brand)
        # 跳过query品牌及归一化后的同一品牌（中英文同一品牌）
        if b_norm == qb_norm or brand == qb_norm:
            continue
        cn = BRAND_CN_MAP.get(brand, "")
        # 商品名包含该品牌名
        if brand in n or (cn and cn in n):
            # 确认这个品牌确实属于另一个品牌集团（非query品牌的中文/英文别名）
            matched_norm = BRAND_CANONICAL.get(brand, brand)
            if matched_norm == qb_norm:
                continue
            return True
    return False

def _flagship_score(shop_title: str, brand: str) -> int:
    """店铺品牌匹配评分(0-3)"""
    if not shop_title or not brand:
        return 0
    shop_lower = shop_title.lower()
    brand_lower = brand.lower()
    matched = False
    if brand_lower in shop_lower:
        matched = True
    else:
        cn_alias = BRAND_CN_MAP.get(brand_lower, "")
        if cn_alias and cn_alias in shop_title:
            matched = True
        elif brand in shop_title:
            matched = True
    if not matched:
        return 0
    if "官方旗舰店" in shop_title:
        return 3
    if "旗舰店" in shop_title:
        return 2
    if "专卖店" in shop_title or "专营店" in shop_title:
        return 1
    return 0

# ============ 关键词简化 ============
def _simplify_keyword(keyword: str) -> str:
    """去规格/内存/型号编码/匹数，用于搜索fallback"""
    k = re.sub(r"\b\d+[GTgt][Bb]?\s*[+＋]\s*\d+[GTgt][Bb]?\b", "", keyword)
    k = re.sub(r"\b(\d{1,2})\s*[+＋]\s*(\d{2,4})\b", "", k)
    k = re.sub(r"\b\d+[GTgt][Bb]?\b", "", k, flags=re.IGNORECASE)
    k = re.sub(r"[A-Z]{2,4}[-]?\d{2,5}[A-Z0-9/\-]*", "", k)
    k = re.sub(r"\d+\.?\d*匹", "", k)
    k = re.sub(r"[（(][^）)]*[）)]", "", k)
    k = re.sub(r"\s+", " ", k).strip()
    return k

_CATEGORY_SUFFIXES = [
    "吹风机", "吸尘器", "剃须刀", "电动牙刷", "空气净化器", "净水器",
    "扫地机器人", "洗衣机", "冰箱", "空调", "电视", "热水器",
    "破壁机", "空气炸锅", "电饭煲", "微波炉", "烤箱", "投影仪",
    "手机", "平板", "笔记本", "显示器", "耳机", "手表", "相机",
    "路由器", "打印机", "智能手表",
]

def _strip_category_suffix(keyword: str) -> str:
    """去掉关键词末尾品类词，如'戴森V15吹风机'→'戴森V15'"""
    for cat in sorted(_CATEGORY_SUFFIXES, key=len, reverse=True):
        if keyword.endswith(cat) and len(keyword) > len(cat):
            return keyword[: -len(cat)].strip()
    return keyword

# ============ 平台搜索 ============
def _search_jd(keyword: str) -> list:
    """京东搜索，三级fallback"""
    items_raw = []
    kw_simplified = _simplify_keyword(keyword)
    kw_stripped = _strip_category_suffix(kw_simplified if kw_simplified else keyword)
    candidates = [keyword]
    if kw_simplified and kw_simplified != keyword:
        candidates.append(kw_simplified)
    if kw_stripped and kw_stripped not in candidates:
        candidates.append(kw_stripped)
    for kw in candidates:
        data = _scf_call("jd", "goods_query", {
            "keyword": kw, "pageIndex": 1, "pageSize": 20, "isSelf": True,
        })
        items_raw = _extract_items(data)
        if items_raw:
            break
    results = []
    for item in items_raw:
        if not isinstance(item, dict):
            continue
        is_self = item.get("isJdSale") == 1
        shop_name = item.get("shopName", "")
        is_brand_shop = False
        if not is_self and shop_name:
            for b in sorted(KNOWN_BRANDS, key=len, reverse=True):
                if b in shop_name.lower():
                    is_brand_shop = True
                    break
                cn = BRAND_CN_MAP.get(b, "")
                if cn and cn in shop_name:
                    is_brand_shop = True
                    break
        if not is_self and not is_brand_shop:
            continue
        # 过滤二手/翻新商品
        if "二手" in shop_name or "翻新" in shop_name or "拍拍" in shop_name:
            continue
        rating = item.get("goodCommentsShare")
        if rating is not None and rating < 90:
            continue
        price = item.get("price")
        discount = item.get("bestCouponDiscount")
        final_price, saved = _compute_final_price(
            price,
            item.get("lowestCouponPrice") or item.get("lowestPrice"),
            coupon_discount=discount,
        )
        coupon_text = "省¥{}".format(int(saved)) if saved > 0 else None
        material_url = item.get("materialUrl", "")
        buy_url = "https://{}".format(material_url) if material_url and not material_url.startswith("http") else "https://item.jd.com/{}.html".format(item.get("itemId", ""))
        results.append({
            "name": item.get("skuName", ""), "brand": item.get("brandName", ""),
            "shop": item.get("shopName", ""), "shop_type": "京东自营" if is_self else "品牌店",
            "price": price, "final_price": final_price,
            "saved": saved if saved > 0 else None,
            "coupon": coupon_text,
            "sales": item.get("inOrderCount30Days"), "rating": rating,
            "image": item.get("imageUrl", ""), "buy_url": buy_url,
            "_is_self": is_self,
        })
    return results

def _search_taobao(keyword: str) -> list:
    """淘宝搜索，三级fallback"""
    items_raw = []
    kw_simplified = _simplify_keyword(keyword)
    kw_stripped = _strip_category_suffix(kw_simplified if kw_simplified else keyword)
    candidates = [keyword]
    if kw_simplified and kw_simplified != keyword:
        candidates.append(kw_simplified)
    if kw_stripped and kw_stripped not in candidates:
        candidates.append(kw_stripped)
    for kw in candidates:
        if not kw:
            continue
        data = _scf_call("taobao", "search", {
            "keyword": kw, "is_tmall": True, "page_no": 1, "page_size": 20,
        })
        items_raw = _extract_items(data)
        if items_raw:
            break
    results = []
    for item in items_raw:
        if not isinstance(item, dict):
            continue
        if item.get("user_type") == "C店":
            continue
        coupon_info = item.get("coupon_info", "")
        coupon_discount = _safe_float(item.get("coupon_amount")) or _parse_coupon_amount(coupon_info)
        coupon_min_order = _safe_float(item.get("coupon_start_fee"))
        final_price, saved = _compute_final_price(
            item.get("price"),
            item.get("final_price"),
            coupon_discount=coupon_discount,
            coupon_min_order=coupon_min_order,
        )
        coupon_text = "省¥{}".format(int(saved)) if saved > 0 else None
        results.append({
            "name": item.get("title", ""), "brand": item.get("brand_name", ""),
            "shop": item.get("shop_title", ""),
            "shop_type": "天猫",
            "price": item.get("price"), "final_price": final_price,
            "saved": saved if saved > 0 else None,
            "coupon": coupon_text,
            "sales": item.get("sales"), "rating": None,
            "image": item.get("pict_url", ""), "buy_url": item.get("click_url", ""),
        })
    return results

# ============ 最优选筛选 ============
def _pick_best_jd(items, brand, keyword=""):
    if not items:
        return None, [], None
    target = [it for it in items if not _is_accessory(it.get("name", "")) and not _has_sub_brand_conflict(keyword, it.get("name", "")) and not _is_brand_mismatch(brand, it.get("name", ""))]
    if not target:
        return None, [], "京东未找到相关商品"
    def _brand_in_shop(item):
        b = (brand or item.get("brand", "")).lower()
        s = item.get("shop", "")
        if not b or not s:
            return 1
        sl = s.lower()
        if b in sl:
            return 0
        cn = BRAND_CN_MAP.get(b, "")
        if cn and cn in s:
            return 0
        if brand in s:
            return 0
        return 1
    def sort_key(item):
        rel = -_relevance_score(item.get("name", ""), keyword)
        self_first = 0 if item.get("_is_self") else 1
        bs = _brand_in_shop(item)
        price = item.get("final_price") or item.get("price") or 999999
        rating = -(item.get("rating") or 0)
        raw_s = item.get("sales")
        sales = -_parse_sales_tip(str(raw_s)) if raw_s else 0
        return (rel, self_first, bs, price, rating, sales)
    sorted_items = sorted(target, key=sort_key)
    # 去重：同一店铺同一价格且名称前30字符相同视为同款变体，只保留第一条
    seen = set()
    deduped = []
    for it in sorted_items:
        shop_key = it.get("shop", "")
        price_key = str(it.get("final_price") or it.get("price", ""))
        name_key = it.get("name", "").lower()[:30]
        key = (shop_key, price_key, name_key)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)
    sorted_items = deduped
    if not sorted_items:
        return None, [], "京东未找到相关商品"
    best = sorted_items[0]
    # 相关性门槛：最优选相关性<0.5或型号数字不匹配，不返回错误结果
    if best:
        best_rel = _relevance_score(best.get("name", ""), keyword)
        model_ok = _model_number_matches(best.get("name", ""), keyword)
        if best_rel < 0.5 or not model_ok:
            return None, [], "京东未找到相关商品"
    alts = sorted_items[1:3]
    note = None
    br = best.get("rating")
    if br is not None and br < 95:
        note = "该商品好评率{}%，低于京东自营优质标准(95%)".format(br)
    return best, alts, note

def _pick_best_taobao(items, brand, keyword=""):
    if not items:
        return None, [], None
    target = [it for it in items if not _is_accessory(it.get("name", "")) and not _has_sub_brand_conflict(keyword, it.get("name", "")) and not _is_brand_mismatch(brand, it.get("name", ""))]
    if not target:
        return None, [], "天猫未找到相关商品"
    def sort_key(item):
        rel = -_relevance_score(item.get("name", ""), keyword)
        b = (brand or item.get("brand", "")).lower()
        fs = -_flagship_score(item.get("shop", ""), b)
        price = item.get("final_price") or item.get("price") or 999999
        raw_s = item.get("sales")
        sales = -_parse_sales_tip(str(raw_s)) if raw_s else 0
        return (rel, price, fs, sales)
    sorted_items = sorted(target, key=sort_key)
    # 去重：同一店铺同一价格且名称前30字符相同视为同款变体，只保留第一条
    seen = set()
    deduped = []
    for it in sorted_items:
        shop_key = it.get("shop", "")
        price_key = str(it.get("final_price") or it.get("price", ""))
        name_key = it.get("name", "").lower()[:30]
        key = (shop_key, price_key, name_key)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)
    sorted_items = deduped
    if not sorted_items:
        return None, [], "天猫未找到相关商品"
    # 相关性门槛：最优选相关性<0.5或型号数字不匹配，不返回错误结果
    if sorted_items:
        best_rel = _relevance_score(sorted_items[0].get("name", ""), keyword)
        model_ok = _model_number_matches(sorted_items[0].get("name", ""), keyword)
        if best_rel < 0.5 or not model_ok:
            return None, [], "天猫未找到相关商品"
    return sorted_items[0], sorted_items[1:3], None

# ============ 核心比价逻辑 ============
def _compare_price(query: str, platform: str = "all") -> str:
    """核心比价：检测链接→清洗→非标品/模糊检测→双平台搜索→筛选"""
    query = query.strip()
    if not query:
        return json.dumps({"query": query, "results": None, "hint": "请输入商品关键词或链接"}, ensure_ascii=False)
    link_type = _detect_link_type(query)
    if link_type == "pdd_link":
        return json.dumps({"query": query, "results": None, "hint": HINT_PDD_LINK}, ensure_ascii=False)
    if link_type == "link":
        return json.dumps({"query": query, "results": None, "hint": HINT_LINK}, ensure_ascii=False)
    search_keyword = _clean_noise(query)
    if _is_non_standard(search_keyword):
        return json.dumps({"query": query, "results": None, "hint": HINT_NON_STANDARD}, ensure_ascii=False)
    if _is_vague_input(search_keyword):
        return json.dumps({"query": query, "results": None, "hint": HINT_VAGUE}, ensure_ascii=False)
    if platform == "pdd":
        return json.dumps({"query": query, "results": None, "hint": HINT_PDD_LINK}, ensure_ascii=False)
    platforms = ["jd", "taobao"] if platform == "all" else [platform]
    query_brand = _extract_brand(search_keyword)
    # 生成品牌+品类的fallback关键词（去掉型号，保留品牌和品类）
    _cat_suffix = None
    for cat in _CATEGORY_SUFFIXES:
        if search_keyword.endswith(cat) and len(search_keyword) > len(cat):
            _cat_suffix = cat
            break
    brand_cat_keyword = None
    cn_brand = BRAND_CN_MAP.get(query_brand.lower(), query_brand) if query_brand else query_brand
    if query_brand and _cat_suffix:
        brand_cat_keyword = "{} {}".format(cn_brand, _cat_suffix)
    elif query_brand and not _cat_suffix:
        # 品牌推断默认品类（如"iPhone 16 Pro Max"无品类后缀→推断"手机"）
        inferred_cat = BRAND_CATEGORY_MAP.get(query_brand.lower(), "")
        if inferred_cat:
            brand_cat_keyword = "{} {}".format(cn_brand, inferred_cat)
    results = {}
    if "jd" in platforms:
        jd_items = _search_jd(search_keyword)
        if not query_brand:
            for it in jd_items:
                if it.get("brand"):
                    query_brand = it["brand"]
                    break
        best, alts, note = _pick_best_jd(jd_items, query_brand, search_keyword)
        # 第一轮无结果时，用品牌+品类再搜一次（放宽型号匹配）
        if best is None and brand_cat_keyword:
            jd_items2 = _search_jd(brand_cat_keyword)
            if jd_items2:
                best2, alts2, note2 = _pick_best_jd(jd_items2, query_brand, brand_cat_keyword)
                if best2:
                    best, alts = best2, alts2
                    note = "未找到精确型号，推荐同品牌热销款"
        results["jd"] = {"best": best, "alternatives": alts, "note": note}
    if "taobao" in platforms:
        tb_items = _search_taobao(search_keyword)
        if not query_brand:
            for it in tb_items:
                if it.get("brand"):
                    query_brand = it["brand"]
                    break
        best, alts, note = _pick_best_taobao(tb_items, query_brand, search_keyword)
        # 第一轮无结果时，用品牌+品类再搜一次（放宽型号匹配）
        if best is None and brand_cat_keyword:
            tb_items2 = _search_taobao(brand_cat_keyword)
            if tb_items2:
                best2, alts2, note2 = _pick_best_taobao(tb_items2, query_brand, brand_cat_keyword)
                if best2:
                    best, alts = best2, alts2
                    note = "未找到精确型号，推荐同品牌热销款"
        results["taobao"] = {"best": best, "alternatives": alts, "note": note}
    return json.dumps({"query": query, "cleaned_keyword": search_keyword, "results": results, "hint": None}, ensure_ascii=False, default=str)

# ============ 格式化输出 ============
def _fmt_price(val) -> str:
    """格式化价格：整数去.0，小数保留2位"""
    if val is None:
        return ""
    try:
        f = float(val)
        if f == int(f):
            return str(int(f))
        return "{:.2f}".format(f)
    except (ValueError, TypeError):
        return str(val)

def _format_item(item: dict, index: int, is_best: bool = True) -> str:
    parts = []
    prefix = "★" if is_best else " ○"
    name = item.get("name", "")
    shop = item.get("shop", "")
    shop_type = item.get("shop_type", "")
    price = item.get("price")
    final_price = item.get("final_price")
    sales = item.get("sales")
    rating = item.get("rating")
    buy_url = item.get("buy_url", "")
    saved = item.get("saved")
    parts.append("  {} {}".format(prefix, name))
    if shop:
        parts.append("    店铺：{}（{}）".format(shop, shop_type))
    if final_price and price and _safe_float(final_price) != _safe_float(price) and _safe_float(final_price) < _safe_float(price):
        parts.append("    到手价：¥{}".format(_fmt_price(final_price)))
        if saved and _safe_float(saved) > 0:
            parts.append("    原价：¥{}（省¥{}）".format(_fmt_price(price), _fmt_price(saved)))
        else:
            parts.append("    原价：¥{}".format(_fmt_price(price)))
    elif price:
        parts.append("    价格：¥{}".format(_fmt_price(price)))
    elif final_price:
        parts.append("    价格：¥{}".format(_fmt_price(final_price)))
    if rating:
        parts.append("    好评率：{}%".format(rating))
    if sales:
        parts.append("    销量：{}".format(sales))
    if buy_url:
        parts.append("    购买：{}".format(buy_url))
    return "\n".join(parts)

def _format_result(result: dict) -> str:
    content_parts = []
    if result.get("hint"):
        return result["hint"]
    results = result.get("results")
    if not results:
        return "未找到比价结果，请尝试更具体的商品关键词。"
    platform_names = {"jd": "京东", "taobao": "天猫"}
    for pk in ["jd", "taobao"]:
        pd = results.get(pk)
        if pd is None:
            continue
        pn = platform_names.get(pk, pk)
        best = pd.get("best")
        alts = pd.get("alternatives", [])
        note = pd.get("note")
        content_parts.append("【{}】".format(pn))
        if note:
            content_parts.append("  ⚠️ {}".format(note))
        if best:
            content_parts.append(_format_item(best, 1, is_best=True))
            for i, alt in enumerate(alts, 2):
                content_parts.append(_format_item(alt, i, is_best=False))
        else:
            content_parts.append("  暂无结果")
        content_parts.append("")
    return "\n".join(content_parts)

# ============ CH入口函数 ============
def compare_price(query: str) -> str:
    """跨平台比价入口：京东/天猫双平台搜索同一商品比较价格"""
    try:
        if not query:
            return "请输入商品关键词或链接"
        result_str = _compare_price(query)
        result = json.loads(result_str)
        text = _format_result(result)
        return text
    except Exception:
        return "查询出错，请稍后重试"


# ============ CLI入口 ============
TOOLS = {
    "compare_price": lambda params: compare_price(params.get("query", "")),
}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(json.dumps({"error": "用法: python3 main.py <tool> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)

    tool = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "参数JSON解析失败: {}".format(e)}, ensure_ascii=False))
        sys.exit(1)

    if tool not in TOOLS:
        print(json.dumps({"error": "未知工具: {}，可用工具: {}".format(tool, ", ".join(TOOLS.keys()))}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = TOOLS[tool](args)
        print(json.dumps({"content": result}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
