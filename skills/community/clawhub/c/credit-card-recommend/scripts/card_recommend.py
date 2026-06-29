#!/usr/bin/env python3
"""
信用卡推荐脚本

从官方接口获取信用卡数据，根据用户需求筛选并推荐合适的信用卡。
单遍遍历：边筛选边构建记录，跳过不匹配的产品，减少内存开销。

用法:
    python card_recommend.py [--keyword 关键词] [--level 卡等级] [--benefit 权益类型] [--json]

示例:
    python card_recommend.py --keyword "免年费"
    python card_recommend.py --level W3 --top 3
    python card_recommend.py --benefit "航延" --json
"""

import json
import os
import sys
import urllib.request
import urllib.error
from typing import List, Dict, Optional


API_URL = "https://cs.citiccardcdn.citicbank.com/citiccard/cardshopcloud/eshop/appimg/cardshop/card/remain_first.json"

LEVEL_MAP = {
    "W3": "i白金卡",
    "W2": "白金卡",
    "B3": "精英/精逸白金卡",
    "K4": "精逸级白金卡",
    "E4": "尊贵级白金卡",
    "C5": "尊尚白金卡",
    "F7": "高端白金卡",
    "00": "尊贵/高端白金卡",
    "TU": "特殊白金等级",
    "GOLD": "金卡",
}

# 免年费等级代码
FREE_ANNUAL_FEE_LEVELS = {"W3", "W2", "GOLD"}

# sid 配置：QClaw 使用专属 sid，其他平台使用通用 sid
QCLAW_SID = "R00002"
DEFAULT_SID = "R00003"

# 平台环境变量检测（依次检查）
PLATFORM_ENV_KEYS = [
    "CLIENT_INFO_IDE_TYPE",    # 主检测变量（WorkBuddy / QClaw / OpenClaw）
    "CLIENT_INFO_PLATFORM",    # 备用检测变量
    "CLIENT_INFO_PLUGIN_NAME", # 备用检测变量
]

# 平台标识值 → URL 参数中的短标识
PLATFORM_SHORT_NAMES = {
    "WORKBUDDY": "wb",
    "QCLAW": "qc",
    "OPENCLAW": "oc",
    "WORKBUDDY-DESKTOP": "wb",
}


# ── 平台检测 & sid ──────────────────────────────────────────

def detect_platform_tag() -> str:
    """
    检测当前运行平台，返回平台短标识

    依次检查 CLIENT_INFO_IDE_TYPE / CLIENT_INFO_PLATFORM / CLIENT_INFO_PLUGIN_NAME，
    匹配到已知平台则返回对应短标识（wb/qc/oc），未匹配则返回空字符串。
    """
    for env_key in PLATFORM_ENV_KEYS:
        value = os.environ.get(env_key, "").upper().strip()
        if not value:
            continue
        for platform_name, short_tag in PLATFORM_SHORT_NAMES.items():
            if platform_name in value:
                return short_tag
    return ""


def get_sid() -> str:
    """
    根据当前平台返回 sid 值

    - QClaw → R00002（专属 sid）
    - 其他平台（WorkBuddy / OpenClaw / 命令行）→ R00003（通用 sid）
    """
    if detect_platform_tag() == "qc":
        return QCLAW_SID
    return DEFAULT_SID


def append_sid(url: str) -> str:
    """
    向 URL 拼接 sid 和 platform 参数

    - URL 已含 ? 和其他参数 → 用 & 拼接
    - URL 不含 ? → 用 ? 拼接
    - URL 为空 → 原样返回
    - URL 已含 sid 参数 → 不重复拼接
    - sid 由平台自动决定：QClaw → R00002，其他 → R00003
    - platform 作为独立参数拼接，如 ?sid=R00003&platform=wb
    - 未检测到平台时只拼 sid，不加 platform
    """
    if not url:
        return url
    if "sid=" in url:
        return url

    sid = get_sid()
    platform_tag = detect_platform_tag()
    separator = "&" if "?" in url else "?"
    result = f"{url}{separator}sid={sid}"

    if platform_tag:
        result = f"{result}&platform={platform_tag}"

    return result


# ── 数据获取 ────────────────────────────────────────────────

def fetch_card_data() -> dict:
    """从接口获取信用卡数据"""
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ── 引导模式：返回可选筛选维度 ─────────────────────────────

# 用场景引导选项（固定，不依赖接口数据）
GUIDE_OPTIONS = {
    "usage_scenarios": [
        {"key": "travel", "label": "航旅出行", "description": "经常出差、坐飞机，看重航延险、里程累积、机场贵宾厅", "params": "--benefit \"航延\""},
        {"key": "shopping", "label": "购物返现", "description": "日常消费为主，希望笔笔返现、多倍积分", "params": "--keyword \"返现\""},
        {"key": "dining", "label": "餐饮娱乐", "description": "经常点外卖、看电影、美食消费", "params": "--keyword \"美团\""},
        {"key": "fuel", "label": "加油充电", "description": "有车一族，加油、充电优惠", "params": "--keyword \"加油\""},
        {"key": "internet", "label": "互联网会员", "description": "希望送视频/音乐会员权益", "params": "--keyword \"会员\""},
        {"key": "health", "label": "医疗健康", "description": "看重就医绿通、健康体检等权益", "params": "--keyword \"医疗\""},
        {"key": "study", "label": "留学教育", "description": "留学缴费、外币消费需求", "params": "--keyword \"留学\""},
        {"key": "free_fee", "label": "免年费优先", "description": "不想交年费，刷卡或绑卡即可免", "params": "--free-annual-fee"},
    ],
    "levels": [
        {"code": "GOLD", "name": "金卡", "description": "入门级，免年费"},
        {"code": "W3", "name": "i白金卡", "description": "刷卡免年费，性价比最高"},
        {"code": "W2", "name": "白金卡", "description": "刷卡免年费，权益更丰富"},
        {"code": "B3", "name": "精英/精逸白金卡", "description": "进阶级，年费480-2000元"},
        {"code": "E4", "name": "尊贵级白金卡", "description": "高端权益，年费2000元"},
        {"code": "F7", "name": "高端白金卡", "description": "顶级权益，年费6800元+"},
    ],
}


def get_guide() -> dict:
    """返回引导选项数据（供 LLM 展示给用户选择）"""
    return GUIDE_OPTIONS


# ── 单条记录构建 ────────────────────────────────────────────

def get_primary_card(variants: List[dict]) -> dict:
    """获取产品的默认卡面变体（if=="1"优先，否则取第一个）"""
    for v in variants:
        if v.get("if") == "1":
            return v
    return variants[0] if variants else {}


def has_free_annual_fee(card: dict) -> bool:
    """判断卡片是否免年费"""
    level = card.get("f", "")
    if level in FREE_ANNUAL_FEE_LEVELS:
        return True
    for cr in card.get("cr", []):
        title = cr.get("t", "")
        brief = cr.get("d", "")
        if "免年费" in title or "免年费" in brief:
            return True
    return False


def build_card_record(product: dict, card: dict, cdn_path: str) -> dict:
    """构建标准化卡片记录"""
    apply_url = append_sid(product.get("pu") or product.get("au", ""))
    image_url = cdn_path + card.get("ci", "") if card.get("ci") else ""
    level_code = card.get("f", "")
    level_name = LEVEL_MAP.get(level_code, level_code)

    benefits = []
    for cr in card.get("cr", []):
        benefits.append({
            "title": cr.get("t", ""),
            "brief": cr.get("d", ""),
            "detail": cr.get("dt", ""),
        })

    return {
        "name": card.get("cn", product.get("pn", "")),
        "product_name": product.get("pn", ""),
        "level_code": level_code,
        "level_name": level_name,
        "image_url": image_url,
        "apply_url": apply_url,
        "benefits": benefits,
        "tags": product.get("fl", ""),
        "new_customer_gift": card.get("ncg", ""),
        "gi": product.get("gi", ""),
        "product_code": card.get("p", ""),
        "is_free_annual_fee": has_free_annual_fee(card),
        "is_default_face": card.get("if") == "1",
        "variant_label": card.get("l", ""),
    }


# ── 单遍筛选 + 构建 + 排序（核心优化） ──────────────────────

def recommend(data: dict, keyword: str = "", level: str = "",
              benefit: str = "", free_annual_fee: bool = False,
              top_n: int = 5) -> List[dict]:
    """
    单遍遍历：边筛选边构建，跳过不匹配产品，最后排序取 top_n。

    优化点：
    - 不再先构建全部记录再筛选，而是先判断是否匹配，匹配才构建
    - 减少 60+ → 只构建命中产品的完整记录
    """
    cdn_path = data.get("cdnPath", "")
    seen_products = set()   # 用产品名(pn)去重，同一产品只保留一条
    matched = []

    # 预处理关键词（只做一次小写转换）
    keyword_lower = keyword.lower() if keyword else ""
    benefit_lower = benefit.lower() if benefit else ""

    for product in data.get("datas", []):
        # 去重：同一产品（pn 相同）只保留第一条
        pn = product.get("pn", "")
        if pn and pn in seen_products:
            continue

        # 取默认卡面
        variants = product.get("ch", [])
        if not variants:
            continue
        card = get_primary_card(variants)
        if not card:
            continue

        # ── 先用原始数据做轻量筛选，不构建记录 ──

        # 等级筛选
        if level and card.get("f", "") != level:
            continue

        # 免年费筛选
        if free_annual_fee and not has_free_annual_fee(card):
            continue

        # 关键词匹配（名称 + 标签 + 变体标签）
        if keyword_lower:
            name = card.get("cn", product.get("pn", "")).lower()
            tags = product.get("fl", "").lower()
            variant_label = card.get("l", "").lower()
            if not (keyword_lower in name or keyword_lower in tags or keyword_lower in variant_label):
                continue

        # 权益关键词匹配（只在 cr 数组中搜索，不构建 benefits 列表）
        if benefit_lower:
            benefit_match = any(
                benefit_lower in cr.get("t", "").lower() or benefit_lower in cr.get("d", "").lower()
                for cr in card.get("cr", [])
            )
            if not benefit_match:
                continue

        # ── 通过筛选，才构建完整记录 ──
        record = build_card_record(product, card, cdn_path)
        matched.append(record)
        if pn:
            seen_products.add(pn)

    # 排序：新户礼遇优先 > 免年费优先 > 权益数量多优先 > 默认卡面优先
    matched.sort(key=lambda c: (
        1 if c["new_customer_gift"] else 0,
        1 if c["is_free_annual_fee"] else 0,
        len(c["benefits"]),
        1 if c["is_default_face"] else 0,
    ), reverse=True)

    return matched[:top_n]


# ── 输出格式化 ──────────────────────────────────────────────

def format_card(card: dict) -> str:
    """格式化单张卡片信息为可读文本"""
    lines = [f"### {card['name']}"]
    lines.append(f"- **卡等级**: {card['level_name']}")
    if card["image_url"]:
        lines.append(f"- **卡面图片**: {card['image_url']}")
    if card["new_customer_gift"]:
        lines.append(f"- **新户礼遇**: {card['new_customer_gift']}")
    if card["benefits"]:
        lines.append("- **核心权益**:")
        for i, b in enumerate(card["benefits"], 1):
            lines.append(f"  {i}. {b['title']}: {b['brief']}")
    if card["apply_url"]:
        lines.append(f"- **申请链接**: {card['apply_url']}")
    return "\n".join(lines)


# ── CLI 入口 ────────────────────────────────────────────────

def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="信用卡推荐")
    parser.add_argument("--keyword", default="", help="关键词匹配（名称、标签）")
    parser.add_argument("--level", default="", help="卡等级代码（如 W3, W2, GOLD, B3, E4 等）")
    parser.add_argument("--benefit", default="", help="权益关键词（如 航延、返现、免年费）")
    parser.add_argument("--free-annual-fee", action="store_true", help="仅免年费卡片")
    parser.add_argument("--top", type=int, default=5, help="返回前 N 张卡片（默认 5）")
    parser.add_argument("--json", action="store_true", dest="json_output", help="以 JSON 格式输出结果")
    parser.add_argument("--guide", action="store_true", dest="guide_mode", help="输出引导选项，供用户选择后再推荐")

    args = parser.parse_args()

    # 引导模式：返回可选维度，不请求接口
    if args.guide_mode:
        print(json.dumps(GUIDE_OPTIONS, ensure_ascii=False, indent=2))
        return

    data = fetch_card_data()

    cards = recommend(data, keyword=args.keyword, level=args.level,
                      benefit=args.benefit, free_annual_fee=args.free_annual_fee,
                      top_n=args.top)

    if not cards:
        if args.json_output:
            print(json.dumps({"count": 0, "cards": []}, ensure_ascii=False))
        else:
            print("未找到匹配的信用卡，请调整筛选条件。")
        sys.exit(0)

    if args.json_output:
        print(json.dumps({"count": len(cards), "cards": cards}, ensure_ascii=False, indent=2))
    else:
        for i, card in enumerate(cards, 1):
            print(f"\n--- 推荐 #{i} ---")
            print(format_card(card))


if __name__ == "__main__":
    main()
