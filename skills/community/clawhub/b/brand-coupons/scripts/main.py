"""吃喝特惠券 - 品牌优惠搜索，搜索连锁品牌全国通用优惠券"""

import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

# ============ SCF代理配置 ============
CPS_PROXY_URL = "https://1439498936-cltb2hszg7.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = "tp_8k2mX9vQ4z"
PROXY_TIMEOUT = 30
HEADERS = {"Content-Type": "application/json", "X-Proxy-Token": PROXY_TOKEN}

# ============ 全国通用阈值 ============
NATIONAL_CITY_THRESHOLD = 50

# ============ 分页配置 ============
PAGE_SIZE = 30

# ============ 品牌别名→全称 ============
BRAND_ALIASES = {
    "瑞幸": "瑞幸咖啡", "luckin": "瑞幸咖啡",
    "星巴克": "星巴克", "starbucks": "星巴克",
    "库迪": "库迪咖啡", "cotti": "库迪咖啡",
    "蜜雪": "蜜雪冰城", "mioxue": "蜜雪冰城",
    "霸王茶姬": "霸王茶姬", "chagee": "霸王茶姬",
    "海底捞": "海底捞", "haidilao": "海底捞",
    "肯德基": "肯德基", "kfc": "肯德基",
    "麦当劳": "麦当劳", "mcdonalds": "麦当劳",
    "塔斯汀": "塔斯汀", "tastien": "塔斯汀",
    "汉堡王": "汉堡王", "burgerking": "汉堡王",
    "绝味": "绝味鸭脖", "juewei": "绝味鸭脖",
    "周黑鸭": "周黑鸭", "zhouheiya": "周黑鸭",
    "名创": "名创优品", "miniso": "名创优品",
    "百果园": "百果园", "pagoda": "百果园",
    "途虎": "途虎养车", "tuhu": "途虎养车",
    "特来电": "特来电", "telaidian": "特来电",
    "屈臣氏": "屈臣氏", "watsons": "屈臣氏",
    "好想来": "好想来", "haoxianglai": "好想来",
    "来伊份": "来伊份", "laiyifen": "来伊份",
    "好利来": "好利来", "holiland": "好利来",
    "老乡鸡": "老乡鸡", "laoxiangji": "老乡鸡",
    "张亮": "张亮麻辣烫", "zhangliang": "张亮麻辣烫",
    "书亦": "书亦烧仙草", "shuyi": "书亦烧仙草",
    "沪上阿姨": "沪上阿姨", "hushang": "沪上阿姨",
    "茶百道": "茶百道", "chabaidao": "茶百道",
    "紫燕": "紫燕百味鸡", "ziyan": "紫燕百味鸡",
    "煌上煌": "煌上煌", "huangshanghuang": "煌上煌",
    "tims": "Tims咖啡", "天好": "Tims咖啡",
    "挪瓦": "挪瓦咖啡", "nowwa": "挪瓦咖啡",
    "赵一鸣": "赵一鸣零食", "zhaoyiming": "赵一鸣零食",
}

# ============ 品类→品牌映射 ============
CATEGORY_BRANDS = {
    "咖啡": ["瑞幸咖啡", "库迪咖啡", "星巴克"],
    "奶茶": ["霸王茶姬", "蜜雪冰城", "沪上阿姨", "茶百道", "书亦烧仙草"],
    "茶饮": ["霸王茶姬", "蜜雪冰城", "茶百道", "沪上阿姨"],
    "火锅": ["海底捞"],
    "炸鸡": ["肯德基", "塔斯汀"],
    "汉堡": ["麦当劳", "肯德基", "汉堡王"],
    "快餐": ["肯德基", "麦当劳", "塔斯汀"],
    "麻辣烫": ["张亮麻辣烫"],
    "卤味": ["绝味鸭脖", "周黑鸭", "煌上煌", "紫燕百味鸡"],
    "零食": ["好想来", "赵一鸣零食", "来伊份"],
    "养车": ["途虎养车"],
    "充电": ["特来电"],
    "水果": ["百果园"],
    "美妆": ["屈臣氏"],
    "零售": ["名创优品", "屈臣氏"],
    "烘焙": ["好利来"],
}


# ============ 辅助函数 ============
def _safe_str(val, default=""):
    if val is None or val == "None":
        return default
    try:
        s = str(val).strip()
        return s if s else default
    except Exception:
        return default


def _safe_int(val, default=0):
    if val is None or val == "None":
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _safe_float(val, default=0.0):
    if val is None or val == "None":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _parse_sale_volume(val) -> int:
    """解析销量字符串为数字"""
    if not val:
        return 0
    s = str(val).strip()
    m = re.search(r"([\d.]+)\s*(w|万)", s, re.IGNORECASE)
    if m:
        return int(float(m.group(1)) * 10000)
    m = re.search(r"([\d.]+)\s*(k|千)", s, re.IGNORECASE)
    if m:
        return int(float(m.group(1)) * 1000)
    m = re.search(r"([\d.]+)", s)
    if m:
        return int(float(m.group(1)))
    return 0


# ============ SCF代理调用 ============
def _call_cps(route: str, params: dict) -> dict:
    """调用美团CPS SCF代理"""
    payload = {"type": route, "params": params}
    try:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            CPS_PROXY_URL, data=body, headers=HEADERS, method="POST"
        )
        with urllib.request.urlopen(req, timeout=PROXY_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data if data else {}
    except Exception as e:
        return {"code": -1, "error": f"代理请求失败: {e}"}


# ============ 搜索优惠券 ============
def _search_coupons(keyword: str, biz_line: int, page_size: int = 20) -> list:
    """搜索美团CPS优惠券"""
    params = {
        "searchText": keyword,
        "platform": 2,
        "bizLine": biz_line,
        "pageSize": page_size,
        "pageIndex": 1,
    }
    result = _call_cps("query_coupon", params)
    if result.get("code") != 0 and "error" in result:
        return []
    data = result.get("data", {})
    if isinstance(data, dict):
        products = data.get("products", [])
    elif isinstance(data, list):
        products = data
    else:
        products = []
    return products if isinstance(products, list) else []


# ============ 并发搜索 ============
def _search_all_brands(brands: list) -> list:
    """并发搜索多个品牌的到餐+到综"""
    tasks = []
    for brand in brands:
        tasks.append((brand, 1))
        tasks.append((brand, 2))

    all_products = []
    with ThreadPoolExecutor(max_workers=min(len(tasks), 10)) as executor:
        futures = {
            executor.submit(_search_coupons, brand, biz_line, 20): (brand, biz_line)
            for brand, biz_line in tasks
        }
        for future in as_completed(futures, timeout=25):
            try:
                products = future.result()
                if products:
                    all_products.extend(products)
            except Exception:
                pass
    return all_products


# ============ 批量推广链接 ============
def _batch_referral_links(products: list) -> dict:
    """并发获取推广链接"""
    results = {}

    def _fetch_one(product):
        pvs = product.get("productViewSign", "")
        if not pvs:
            return pvs, ""
        biz_line = _safe_int(product.get("bizLine", 1))
        link = _get_referral_link(pvs, biz_line)
        return pvs, link

    with ThreadPoolExecutor(max_workers=min(len(products), 15)) as executor:
        futures = {executor.submit(_fetch_one, p): p for p in products}
        for future in as_completed(futures, timeout=30):
            try:
                pvs, link = future.result()
                if pvs and link:
                    results[pvs] = link
            except Exception:
                pass
    return results


def _get_referral_link(product_view_sign: str, biz_line: int) -> str:
    """获取推广者链接"""
    params = {
        "productViewSign": product_view_sign,
        "platform": 2,
        "bizLine": biz_line,
        "linkTypes": "1",
    }
    result = _call_cps("get_referral_link", params)
    if result.get("code") != 0:
        return ""
    link_map = result.get("referralLinkMap", {})
    if isinstance(link_map, dict):
        link = link_map.get("1", "")
        if link:
            return str(link)
        link = link_map.get("2", "")
        if link:
            return str(link)
    return ""


# ============ 去重 ============
def _dedup(products: list) -> list:
    seen = set()
    result = []
    for p in products:
        pvs = p.get("productViewSign", "")
        if pvs and pvs in seen:
            continue
        if pvs:
            seen.add(pvs)
        result.append(p)
    return result


# ============ 关键词扩展 ============
def _expand_keyword(keyword: str) -> str:
    for short, full in BRAND_ALIASES.items():
        if short.lower() == keyword.lower():
            return full
    return keyword


def _resolve_to_brands(keyword: str) -> list:
    for cat, brands in CATEGORY_BRANDS.items():
        if cat in keyword:
            return brands
    expanded = _expand_keyword(keyword)
    return [expanded]


# ============ 格式化工具 ============
def _format_price(price) -> str:
    p = _safe_float(price, -1)
    if p < 0:
        return ""
    if p == int(p):
        return f"¥{int(p)}"
    return f"¥{p:.1f}"


def _format_coupon(product: dict, referral_link: str) -> str:
    """格式化单个优惠券"""
    name = product.get("name", "")
    brand = product.get("brandName", "")
    sell_price = _format_price(product.get("sellPrice"))
    original_price = _format_price(product.get("originalPrice"))
    img = product.get("headUrl", "")
    sale_volume = product.get("saleVolume", "")

    sp = _safe_float(product.get("sellPrice"), 0)
    op = _safe_float(product.get("originalPrice"), 0)
    saved = op - sp if op > sp > 0 else 0

    if saved > 0:
        price_line = f"{sell_price}（省{_format_price(saved)}） ← {original_price}"
    else:
        price_line = sell_price

    labels = []
    beat_label = product.get("beatMTLabel", "")
    if beat_label:
        labels.append(f"🔥{beat_label}")
    price_label = product.get("pricePowerLabel", "")
    if price_label:
        labels.append(f"📉{price_label}")
    label_str = " | ".join(labels) if labels else ""

    lines = []
    if brand and brand not in name:
        lines.append(f"🏷 {brand}")
    lines.append(f"**{name}**")
    lines.append(f"💰 {price_line}")
    if label_str:
        lines.append(label_str)
    if sale_volume:
        lines.append(f"📦 {sale_volume}")
    if img:
        lines.append(f"![{name}]({img})")
    if referral_link:
        lines.append(f"🛒 [立即购买]({referral_link})")

    return "\n".join(lines)


# ============ 主格式化 ============
def _format_results(keyword: str, products: list, page: int = 1) -> str:
    if not products:
        return (
            f"未找到「{keyword}」的全国通用品牌优惠，换个关键词试试？\n\n"
            "💡 热门品牌：瑞幸 | 库迪 | 霸王茶姬 | 蜜雪冰城 | 海底捞 | "
            "肯德基 | 名创优品 | 途虎养车 | 百果园 | 屈臣氏"
        )

    products = [
        p for p in products
        if p.get("saleStatus") is not False
        and _safe_int(p.get("availablePoiCityNum", 0)) >= NATIONAL_CITY_THRESHOLD
    ]

    if not products:
        return (
            f"未找到「{keyword}」的全国通用品牌优惠，换个关键词试试？\n\n"
            "💡 热门品牌：瑞幸 | 库迪 | 霸王茶姬 | 蜜雪冰城 | 海底捞 | "
            "肯德基 | 名创优品 | 途虎养车 | 百果园 | 屈臣氏"
        )

    products.sort(
        key=lambda p: _parse_sale_volume(p.get("saleVolume", "")),
        reverse=True,
    )

    total = len(products)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, total_pages))
    start = (page - 1) * PAGE_SIZE
    display = products[start:start + PAGE_SIZE]

    link_map = _batch_referral_links(display)

    formatted = []
    for i, p in enumerate(display, 1):
        pvs = p.get("productViewSign", "")
        link = link_map.get(pvs, "")
        item = _format_coupon(p, link)
        formatted.append(f"{i}. {item}")

    header = f"🔍 「{keyword}」全国通用优惠（共{total}个）"
    if total_pages > 1:
        header += f"\n📄 第{page}/{total_pages}页（本页{len(display)}个）"
    header += "\n"

    body = "\n\n".join(formatted)

    footer_parts = []
    if total_pages > 1:
        if page < total_pages:
            footer_parts.append(f"👉 翻页：page={page+1}")
        if page > 1:
            footer_parts.append(f"👉 上一页：page={page-1}")
    footer_parts.append("💡 全国通用券到店出示即可核销，出差旅行也能用")
    footer_parts.append(
        "🔥 热门品牌：瑞幸 | 库迪 | 霸王茶姬 | 蜜雪冰城 | 星巴克 | "
        "海底捞 | 肯德基 | 麦当劳 | 塔斯汀 | 名创优品 | 途虎养车 | 百果园 | 屈臣氏"
    )

    footer = "\n\n---\n" + "\n".join(footer_parts)
    return header + body + footer


# ============ CH入口函数 ============
def main(query: str) -> str:
    """搜索品牌优惠 - 搜索连锁品牌全国通用优惠券"""
    try:
        if not query:
            return "请输入品牌名称或品类关键词\n\n💡 品牌搜索：瑞幸 | 海底捞 | 蜜雪冰城 | 途虎养车\n💡 品类搜索：咖啡 | 奶茶 | 火锅 | 养车 | 零食"

        # 尝试解析JSON参数
        try:
            params = json.loads(query)
            keyword = params.get("keyword", "")
            page = int(params.get("page", 1))
        except (json.JSONDecodeError, ValueError):
            keyword = query.strip()
            page = 1

        if page < 1:
            page = 1

        if not keyword:
            return "请输入品牌名称或品类关键词"

        brands = _resolve_to_brands(keyword)
        all_products = _search_all_brands(brands)

        # 原始关键词也搜一下
        if keyword not in brands and len(brands) == 1 and brands[0] != keyword:
            orig_dining = _search_coupons(keyword, biz_line=1, page_size=10)
            orig_lifestyle = _search_coupons(keyword, biz_line=2, page_size=10)
            all_products.extend(orig_dining)
            all_products.extend(orig_lifestyle)

        all_products = _dedup(all_products)
        text = _format_results(keyword, all_products, page=page)
        return text

    except Exception:
        return "❌ 查询出错，请稍后重试"


if __name__ == "__main__":
    tool = sys.argv[1] if len(sys.argv) > 1 else "search_brand_coupons"
    params_str = sys.argv[2] if len(sys.argv) > 2 else "{}"
    print(main(params_str))
