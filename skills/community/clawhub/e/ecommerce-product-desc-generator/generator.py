#!/usr/bin/env python3
"""
电商产品描述批量生成器 - 核心生成引擎
支持平台：亚马逊、淘宝、拼多多、TikTok Shop、Shopify
"""

import random
import csv
import io
import re
from typing import Dict, List, Optional

__version__ = "1.0.0"

# ============================================================
# 词汇池
# ============================================================

TITLE_OPENERS_EN = [
    "Premium", "High-Quality", "Top-Rated", "Best-Selling",
    "Professional", "Durable", "Elegant", "Portable",
    "Multifunctional", "Lightweight", "Heavy-Duty", "Stylish"
]

QUALITY_WORDS_EN = [
    "Stainless Steel", "Eco-Friendly", "Organic", "Handcrafted",
    "Fashionable", "Waterproof", "Rechargeable", "FDA-Approved",
    "BPA-Free", " hypoallergenic", "Scratch-Resistant"
]

FEATURE_WORDS_EN = [
    "Ergonomic", "Compact", "Foldable", "Adjustable", "Easy-to-Use",
    "Travel-Friendly", "Kid-Safe", "Pet-Friendly", "Multi-Use",
    "Space-Saving", "High-Capacity"
]

USE_CASE_WORDS_EN = [
    "Perfect for Home", "Ideal for Office", "Great for Outdoors",
    "Must-Have for", "Essential for", "Designed for",
    " Suitable for Daily Use", "Great Gift for"
]

BENEFIT_WORDS_EN = [
    "saves your time and money",
    "makes your life easier",
    "brings comfort to your daily routine",
    "helps you stay organized",
    "delivers professional results at home",
    "upgrades your lifestyle instantly"
]

TITLE_OPENERS_CN = [
    "【精选】", "【爆款】", "【热卖】", "【新品】",
    "【推荐】", "【限时】", "【特惠】", "【旗舰】"
]

QUALITY_WORDS_CN = [
    "优质", "精品", "高端", "轻奢", "环保",
    "简约", "实用", "耐用", "精致", "时尚"
]

FEATURE_WORDS_CN = [
    "多功能", "便携式", "可折叠", "防水", "充电式",
    "迷你", "大容量", "智能", "无线", "轻便"
]

BENEFIT_WORDS_CN = [
    "提升生活品质", "省时省力", "改善居家体验",
    "让生活更便捷", "送礼自用两相宜", "打造品质生活"
]

TAOBAO_STYLE_WORDS = [
    "厂家直销", "正品保证", "七天无理由", "急速发货",
    "亏本冲量", "限时秒杀", "今日特价", "销量冠军"
]

PINBUYI_STYLE_WORDS = [
    "拼团立省", "百亿补贴", "品牌特卖", "工厂价",
    "限时拼购", "新人专享", "全网最低价", "亏本引流"
]

# ============================================================
# 平台模板
# ============================================================

AMAZON_TITLE_TEMPLATES = [
    "{opener} {product_name} - {feature} {quality} {material} for {use_case}",
    "{product_name} | {feature} {quality} {material} | {use_case} & Everyday Use",
    "{opener} {product_name} {material} - {feature} Design | Perfect for {use_case}",
    "{product_name} ({material}, {feature}) - {quality} & Durable | Best for {use_case}",
    "{opener} {product_name} - Premium {material} {feature} for {use_case} (New {year})",
]

AMAZON_BULLET_TEMPLATES = [
    "**PREMIUM QUALITY**: {quality} {material} ensures durability and long-lasting performance, withstand daily wear and tear.",
    "**EASY TO USE**: {feature} design allows effortless operation — perfect for {use_case}. No complicated setup required.",
    "**MULTI-PURPOSE**: Great for {use_case}, {use_case_2} and many other scenarios. Versatile enough for everyday needs.",
    "**SAFE & RELIABLE**: {quality} materials, {safety} certified. 100% satisfaction guarantee or your money back.",
    "**GREAT VALUE**: {benefit}. Buy with confidence — this is the best {product_name} deal you'll find online.",
]

AMAZON_DESCRIPTION_TEMPLATE = """{product_name} — your go-to solution for {use_case}.

Crafted with {quality} {material}, this {feature} {product_name} is designed to make your life easier and more enjoyable. Whether you're at home, in the office, or on the go, it delivers consistent, reliable performance every time.

**Why choose our {product_name}?**
{benefit}. Built to last with premium materials and thoughtful engineering. Every detail has been optimized for your satisfaction.

**What's Included:**
• 1x {product_name}
• User Manual
• Premium Packaging

**Note:** Images are for illustration purposes. Slight color/size variations may occur due to lighting and manufacturing.

Keywords: {keywords}
"""

TIKTOK_BULLET_TEMPLATES = [
    "✅ {quality} {material} — feels premium, looks amazing 😍",
    "✅ {feature} design — so easy to use, even for beginners!",
    "✅ Perfect for {use_case} — honestly this changed my daily routine 💯",
    "✅ Great gift idea 🎁 — whoever gets this will love it!",
    "✅ Amazing value for the price — don't sleep on this one 🔥",
]

TIKTOK_DESCRIPTION_TEMPLATE = """✨ NAME ✨

Okay real talk — this {product_name} is so good 🤩

I've been using it for {duration} and honestly... {benefit} 🙌

**Why you need this:**
• {feature} design, super easy to use
• {quality} {material} — feels expensive af
• Perfect for {use_case}
• Makes a great gift 🎁

**Shipping:** Fast delivery available 🚚

Drop a ❤️ if you want more picks like this!

#fyp #tiktokmademebuyit #productrecommendation #musthave #lifestyle
"""

SHOPIFY_TITLE_TEMPLATES = [
    "{product_name} | {feature} {quality} {material} — {brand}",
    "{product_name} — {feature} {material} for {use_case} | {brand}",
    "{brand} {product_name} | Premium {quality} {material} — {feature} Design",
]

SHOPIFY_DESCRIPTION_TEMPLATE = """**{product_name}** — thoughtfully designed for those who appreciate quality and functionality.

**Overview**
{benefit}. Made with {quality} {material}, this {product_name} brings together style, performance, and durability in one beautifully crafted package.

**Key Features**
- **{feature} Design**: Engineered for ease of use and maximum effectiveness
- **{quality} {material}**: Built to last, day after day
- **{use_case}**: Your perfect companion for everyday life
- Versatile and practical — fits seamlessly into any lifestyle

**Details**
- Material: {quality} {material}
- Design: {feature}
- Suitable for: {use_case}

**Shipping & Returns**
Free shipping on orders over $50. 30-day hassle-free returns.

**Customer Promise**
Every {product_name} is quality-checked before delivery. Your satisfaction is our priority.

Questions? We're here to help — reach out anytime.
"""

TAOBAO_TITLE_TEMPLATES = [
    "{opener}{product_name}{feature}{quality} {material} {category}",
    "{style_word} {product_name} {feature} {material} {quality} 正品{category}",
    "{product_name} {feature} {material} {quality} {category} 厂家直销",
    "{opener}{material} {product_name} {feature} {quality} {category}",
    "{product_name} {quality} {feature} {material} {category} 全国联保",
]

TAOBAO_BENEFIT_TEMPLATES_CN = [
    "品质保证，正品保障，支持七天无理由退货",
    "环保材质，安全无毒，全家适用",
    "工厂直销价，性价比超高，买到就是赚到",
    "设计精美，做工精细，彰显品质生活",
    "功能强大，操作简单，送礼自用两相宜",
]

TAOBAO_DESCRIPTION_TEMPLATE = """【产品名称】{product_name}

【产品特点】
✨ {feature}设计，简约时尚
✨ {quality}{material}，坚固耐用
✨ 适用于{use_case}
✨ 适合送给：家人、朋友、同事

【产品参数】
- 材质：{quality}{material}
- 功能：{feature}
- 适用场景：{use_case}
{category_line}

【购买保障】
✅ 正品保证
✅ 七天无理由退货
✅ 闪电发货
✅ 售后无忧

【温馨提示】
产品实物与图片可能略有差异，以实际为准。
有任何问题欢迎咨询客服，我们第一时间为您解答！
"""

PINBUYI_TITLE_TEMPLATES = [
    "{style_word}{product_name}{feature}{material} 拼团价{category}",
    "{product_name}{feature}{material}{quality} 限时拼购 全国包邮",
    "{style_word}{material}{product_name}{feature}{quality} 亏本冲量",
    "{product_name}{quality}{feature}{material}{category} 工厂直发",
]

PINBUYI_DESCRIPTION_TEMPLATE = """💰 {product_name} — 拼团价来了！

🔥 限时拼团，超值优惠，现在下单立省！

【产品亮点】
✅ {feature}{material}，{quality}
✅ 适用于{use_case}
✅ 性价比之王，同款低价放心购

【为什么选我们？】
• 工厂源头价格，没有中间商赚差价
• 品质有保障，售后无忧
• 发货速度快，物流可查

【规格说明】
- 材质：{quality}{material}
- 功能：{feature}
- 适用：{use_case}

⚠️ 拼团有效期有限，喜欢就赶紧下单！
收到货有任何问题随时联系客服～
"""


# ============================================================
# 平台关键词占位符
# ============================================================

YEAR = 2026
DURATION_CHOICES = ["a week", "two weeks", "a month", "a few months"]
SAFETY_CERTS = ["CE", "FCC", "RoHS", "UL"]


# ============================================================
# 工具函数
# ============================================================

def safe_keyword(text: str) -> str:
    """清理关键词中的特殊字符"""
    return re.sub(r"[^\w\s\-&,]", "", text)


def pick_random(lst: List[str]) -> str:
    return random.choice(lst)


def fill_template(template: str, vars_dict: Dict) -> str:
    """简单模板填充，支持 {key} 格式"""
    result = template
    for key, val in vars_dict.items():
        result = result.replace(f"{{{key}}}", str(val))
    return result


def build_vars(
    product_name: str,
    category: str,
    keywords: str,
    brand: str = "",
    price: str = "",
) -> Dict:
    """构建填充变量字典"""
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []
    keyword_str = ", ".join(kw_list) if kw_list else product_name

    opener_en = pick_random(TITLE_OPENERS_EN)
    quality_en = pick_random(QUALITY_WORDS_EN)
    feature_en = pick_random(FEATURE_WORDS_EN)
    material_en = pick_random(QUALITY_WORDS_EN)  # reuse pool
    use_case = pick_random(USE_CASE_WORDS_EN).replace("Perfect for ", "").replace("Ideal for ", "")
    use_case_2 = pick_random(USE_CASE_WORDS_EN).replace("Great for ", "").replace("Essential for ", "")
    benefit_en = pick_random(BENEFIT_WORDS_EN)
    safety = pick_random(SAFETY_CERTS)
    duration = pick_random(DURATION_CHOICES)

    opener_cn = pick_random(TITLE_OPENERS_CN)
    quality_cn = pick_random(QUALITY_WORDS_CN)
    feature_cn = pick_random(FEATURE_WORDS_CN)
    material_cn = pick_random(QUALITY_WORDS_CN)
    use_case_cn = pick_random(BENEFIT_WORDS_CN).replace("提升", "").replace("省时", "省时省力")
    style_word = pick_random(TAOBAO_STYLE_WORDS)
    pin_style = pick_random(PINBUYI_STYLE_WORDS)

    brand_str = brand if brand else "PremiumBrand"
    price_str = price if price else ""

    return {
        # English
        "opener": opener_en,
        "quality": quality_en,
        "feature": feature_en,
        "material": material_en,
        "use_case": use_case,
        "use_case_2": use_case_2,
        "benefit": benefit_en,
        "safety": safety,
        "duration": duration,
        "brand": brand_str,
        "year": YEAR,
        "keywords": keyword_str,
        "price": price_str,
        # Chinese
        "product_name": product_name,
        "category": category,
        "opener_cn": opener_cn,
        "quality_cn": quality_cn,
        "feature_cn": feature_cn,
        "material_cn": material_cn,
        "use_case_cn": use_case_cn,
        "style_word": style_word,
        "pin_style": pin_style,
        "benefit_cn": pick_random(TAOBAO_BENEFIT_TEMPLATES_CN),
        "category_line": f"- 类别：{category}" if category else "",
    }


# ============================================================
# 平台生成器
# ============================================================

def generate_amazon(product_name: str, category: str, keywords: str,
                    brand: str = "", price: str = "") -> Dict[str, str]:
    vars_d = build_vars(product_name, category, keywords, brand, price)
    title = fill_template(pick_random(AMAZON_TITLE_TEMPLATES), vars_d)
    # limit title to 200 chars
    if len(title) > 200:
        title = title[:197] + "..."

    bullets = [fill_template(t, vars_d) for t in AMAZON_BULLET_TEMPLATES]
    description = fill_template(AMAZON_DESCRIPTION_TEMPLATE, vars_d)
    return {"title": title, "bullets": bullets, "description": description}


def generate_taobao(product_name: str, category: str, keywords: str,
                    brand: str = "", price: str = "") -> Dict[str, str]:
    vars_d = build_vars(product_name, category, keywords, brand, price)
    title = fill_template(pick_random(TAOBAO_TITLE_TEMPLATES), vars_d)
    if len(title) > 30:
        title = title[:27] + "..."
    description = fill_template(TAOBAO_DESCRIPTION_TEMPLATE, vars_d)
    return {"title": title, "description": description}


def generate_pinduoduo(product_name: str, category: str, keywords: str,
                       brand: str = "", price: str = "") -> Dict[str, str]:
    vars_d = build_vars(product_name, category, keywords, brand, price)
    title = fill_template(pick_random(PINBUYI_TITLE_TEMPLATES), vars_d)
    if len(title) > 30:
        title = title[:27] + "..."
    description = fill_template(PINBUYI_DESCRIPTION_TEMPLATE, vars_d)
    return {"title": title, "description": description}


def generate_tiktok(product_name: str, category: str, keywords: str,
                    brand: str = "", price: str = "") -> Dict[str, str]:
    vars_d = build_vars(product_name, category, keywords, brand, price)
    title = f"✨ {product_name} — {vars_d['feature']} & {vars_d['quality']} | Must-Have! 😍"
    if len(title) > 100:
        title = title[:97] + "..."
    bullets = [fill_template(t, vars_d) for t in TIKTOK_BULLET_TEMPLATES]
    description = fill_template(TIKTOK_DESCRIPTION_TEMPLATE, vars_d)
    return {"title": title, "bullets": bullets, "description": description}


def generate_shopify(product_name: str, category: str, keywords: str,
                     brand: str = "", price: str = "") -> Dict[str, str]:
    vars_d = build_vars(product_name, category, keywords, brand, price)
    title = fill_template(pick_random(SHOPIFY_TITLE_TEMPLATES), vars_d)
    description = fill_template(SHOPIFY_DESCRIPTION_TEMPLATE, vars_d)
    return {"title": title, "description": description}


# ============================================================
# 主生成器类
# ============================================================

class ProductDescGenerator:
    """电商产品描述生成器"""

    PLATFORMS = {
        "amazon": ("亚马逊", generate_amazon),
        "taobao": ("淘宝", generate_taobao),
        "pinduoduo": ("拼多多", generate_pinduoduo),
        "tiktok": ("TikTok Shop", generate_tiktok),
        "shopify": ("Shopify", generate_shopify),
    }

    def __init__(self):
        pass

    def generate_single(
        self,
        product_name: str,
        category: str = "",
        keywords: str = "",
        brand: str = "",
        price: str = "",
        platforms: Optional[List[str]] = None,
    ) -> Dict[str, Dict]:
        if platforms is None:
            platforms = list(self.PLATFORMS.keys())

        results = {}
        for pid in platforms:
            if pid not in self.PLATFORMS:
                continue
            label, func = self.PLATFORMS[pid]
            results[pid] = {
                "label": label,
                **func(product_name, category, keywords, brand, price)
            }
        return results

    def to_markdown(self, results: Dict[str, Dict], product_name: str) -> str:
        lines = [f"# {product_name} — 产品描述生成结果\n"]
        for pid, data in results.items():
            label = data["label"]
            lines.append(f"## 🏪 {label}\n")
            lines.append(f"**标题**: {data['title']}\n")
            if "bullets" in data:
                lines.append("**卖点 (Bullet Points)**:\n")
                for i, b in enumerate(data["bullets"], 1):
                    lines.append(f"{i}. {b}\n")
            lines.append(f"\n**详情描述**:\n\n{data['description']}\n")
            lines.append("\n---\n")
        return "".join(lines)

    def to_txt(self, results: Dict[str, Dict], product_name: str) -> str:
        sections = []
        for pid, data in results.items():
            label = data["label"]
            lines = [f"=== {label} ({product_name}) ===", f"标题: {data['title']}"]
            if "bullets" in data:
                for i, b in enumerate(data["bullets"], 1):
                    lines.append(f"  [{i}] {b}")
            lines.append(f"详情:\n{data['description']}")
            sections.append("\n".join(lines))
        return "\n\n".join(sections)

    def to_csv(self, results: Dict[str, Dict]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["平台", "标题", "卖点", "详情描述"])
        for pid, data in results.items():
            label = data["label"]
            bullets = " | ".join(data.get("bullets", []))
            writer.writerow([label, data["title"], bullets, data["description"]])
        return output.getvalue()

    def generate_batch(
        self,
        products: List[Dict],
        platforms: Optional[List[str]] = None,
        output_format: str = "markdown",
    ) -> str:
        """批量生成，products 为 [{product_name, category, keywords, brand, price}, ...]"""
        all_results = []
        for p in products:
            result = self.generate_single(
                product_name=p.get("product_name", ""),
                category=p.get("category", ""),
                keywords=p.get("keywords", ""),
                brand=p.get("brand", ""),
                price=p.get("price", ""),
                platforms=platforms,
            )
            all_results.append((p.get("product_name", "Product"), result))

        if output_format == "csv":
            rows = [["产品名称", "平台", "标题", "详情描述"]]
            for name, results in all_results:
                for pid, data in results.items():
                    rows.append([name, data["label"], data["title"], data["description"]])
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(rows)
            return output.getvalue()
        else:
            parts = []
            for name, results in all_results:
                if output_format == "markdown":
                    parts.append(self.to_markdown(results, name))
                else:
                    parts.append(self.to_txt(results, name))
            return "\n\n".join(parts)


# ============================================================
# CSV 解析
# ============================================================

def parse_csv_input(csv_text: str) -> List[Dict]:
    """解析 CSV 输入，返回产品字典列表"""
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    products = []
    for row in reader:
        products.append({
            "product_name": row.get("product_name") or row.get("产品名称") or "",
            "category": row.get("category") or row.get("类目") or "",
            "keywords": row.get("keywords") or row.get("关键词") or "",
            "brand": row.get("brand") or row.get("品牌") or "",
            "price": row.get("price") or row.get("价格") or "",
        })
    return [p for p in products if p["product_name"]]
