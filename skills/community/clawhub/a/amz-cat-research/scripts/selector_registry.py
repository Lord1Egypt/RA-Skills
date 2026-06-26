#!/usr/bin/env python3
"""
selectors.py — Amazon 产品页 DOM 选择器注册表

每个字段：主选择器 + 备用链 + 提取表达式 + 类型
agent 调用 gen_*.py 读取此表生成 JS evaluate 代码
healer.py 读取此表做验证和修复

格式：
  "field_id": {
      "primary":   CSS 主选择器,
      "fallbacks": [备用1, 备用2, ...],
      "extract":   JS 提取表达式（el 代表 querySelector 命中的元素）,
      "type":      text|number|bool|raw,
      "source":    amazon_page|seller_spirit|sif,
  }
"""

from typing import Optional

FIELDS = {
    # ── Amazon 页面原生字段 ──
    "asin": {
        "primary": None,  # 从 URL 提取
        "fallbacks": [],
        "extract": "location.pathname.match(/\\/dp\\/([A-Z0-9]{10})/)?.[1]",
        "type": "text",
        "source": "amazon_page",
    },
    "title": {
        "primary": "#productTitle",
        "fallbacks": ["h1.a-size-large", "[data-feature-name='title'] h1"],
        "extract": "el?.innerText?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "price": {
        "primary": ".a-price .a-offscreen",
        "fallbacks": ["#priceblock_ourprice", "#priceblock_dealprice", "#priceblock_saleprice", ".a-price-whole"],
        "extract": "el?.innerText?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "rating": {
        "primary": "#acrPopover",
        "fallbacks": [".a-icon-star", "[data-feature-name='averageCustomerReviews'] .a-icon-alt"],
        "extract": "el?.getAttribute('title') || el?.innerText?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "review_count": {
        "primary": "#acrCustomerReviewText",
        "fallbacks": ["#reviewsMedley .a-size-base"],
        "extract": "el?.innerText?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "brand": {
        "primary": "#bylineInfo",
        "fallbacks": ["[data-feature-name='brandName']", "[id*='brand']", "a#bylineInfo"],
        "extract": "el?.innerText?.replace(/\\s*Visit the .*/,'')?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "seller": {
        "primary": "#sellerProfileTriggerId",
        "fallbacks": ["[id*='soldBy']", "#tabular-buybox-trt-seller .tabular-buybox-text"],
        "extract": "el?.innerText?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "list_price": {
        "primary": ".a-text-price",
        "fallbacks": ["[aria-label*='List Price']", ".a-price.a-text-price"],
        "extract": "el?.innerText?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "deal_badge": {
        "primary": "#dealBadge_feature_div",
        "fallbacks": [".dealBadge", ".couponBadge", "[class*='deal']", "[class*='coupon']"],
        "extract": "el?.innerText?.trim()",
        "type": "text",
        "source": "amazon_page",
    },
    "bullets": {
        "primary": "#feature-bullets",
        "fallbacks": [".a-unordered-list.a-vertical"],
        "extract": "Array.from(el?.querySelectorAll('li span.a-list-item')||[]).map(e=>e.innerText.trim()).filter(Boolean)",
        "type": "raw",
        "source": "amazon_page",
    },
    "detail_bullets": {
        "primary": "#detailBulletsWrapper_feature_div",
        "fallbacks": ["#detailBullets_feature_div", "#productDetails", "#productDetails_db_sections"],
        "extract": "el?.innerText?.trim()?.substring(0, 1000)",
        "type": "raw",
        "source": "amazon_page",
    },
    "variant_container": {
        "primary": "#twister",
        "fallbacks": ["#twister-plus-desktop-twister-container", "[id*='variation']"],
        "extract": "!!el",
        "type": "bool",
        "source": "amazon_page",
    },
    "variant_names": {
        "primary": "#variation_color_name li img",
        "fallbacks": ["#twister li img", "[id*='variation'] li img", "#twister .swatch"],
        "extract": "__QA__",
        "type": "raw",
        "source": "amazon_page",
        "note": "特殊字段：用 querySelectorAll，gen_product.py 单独处理",
    },

    # ── Amazon 页面补充字段（产品主图/A+内容/视频/Review分布） ──
    "image_main": {
        "primary": "#imgTagWrapperId img",
        "fallbacks": [".a-carousel .a-carousel-card img", "#main-image"],
        "extract": "el?.getAttribute('src')",
        "type": "text",
        "source": "amazon_page",
    },
    "aplus_exists": {
        "primary": "#aplus",
        "fallbacks": [".aplus-v2", "[id*='aplus']"],
        "extract": "!!el",
        "type": "bool",
        "source": "amazon_page",
    },
    "video_exists": {
        "primary": "video",
        "fallbacks": ["[data-video-url]", "[class*='video']"],
        "extract": "!!el",
        "type": "bool",
        "source": "amazon_page",
    },
    "review_histogram": {
        "primary": "#histogramTable",
        "fallbacks": ["#reviews-medley .a-histogram", "[data-hook='histogram-table']"],
        "extract": "el?.innerText?.trim()?.substring(0, 500)",
        "type": "raw",
        "source": "amazon_page",
    },

    # ── 卖家精灵插件字段 ──
    "spirit_container": {
        "primary": "#seller-sprite-extension-quick-view-listing",
        "fallbacks": ["[id*='seller-sprite']", "[class*='seller-spirit']"],
        "extract": "!!el",
        "type": "bool",
        "source": "seller_spirit",
    },
    "spirit_raw": {
        "primary": "#seller-sprite-extension-quick-view-listing",
        "fallbacks": ["[id*='seller-sprite']", "[class*='seller-spirit']"],
        "extract": "el?.innerText?.substring(0, 2000)",
        "type": "raw",
        "source": "seller_spirit",
        "note": "插件全量文本，后续用正则提取子字段",
    },

    # ── SIF 插件字段 ──
    "sif_container": {
        "primary": "[data-sif-container]",
        "fallbacks": [".sif-extension-container", "[class*='sif-']"],
        "extract": "!!el",
        "type": "bool",
        "source": "sif",
    },
    "sif_raw": {
        "primary": "[data-sif-container]",
        "fallbacks": [".sif-extension-container", "[class*='sif-']"],
        "extract": "el?.innerText?.substring(0, 1500)",
        "type": "raw",
        "source": "sif",
        "note": "SIF 插件全量文本，后续用正则提取",
    },
}

# 卖家精灵正则提取子字段
SPIRIT_PATTERNS = {
    "spirit_brand": r"品牌[：:]\s*(.+)",
    "spirit_seller": r"卖家[：:]\s*(.+)",
    "spirit_fba_fee": r"FBA费用[：:]\s*\$?([\d.]+)",
    "spirit_margin": r"毛利率[：:]\s*([\d.]+)%?",
    "spirit_listing_date": r"上架时间[：:]\s*(\d{4}-\d{2}-\d{2})",
    "spirit_sales_30d_parent": r"近30天销量\(父体\)[：:]\s*([\d,]+)",
    "spirit_sales_30d_child": r"近30天销量\(子体\)[：:]\s*([\d,+]+)",
    "spirit_revenue": r"销售额[：:]\s*\$?([\d,]+)",
    "spirit_variant_count": r"变体数[：:]\s*(\d+)",
    "spirit_weight": r"商品重量[：:]\s*(.+)",
    "spirit_dimensions": r"商品尺寸[：:]\s*(.+)",
    "spirit_total_keywords": r"全部流量词[：:]\s*([\d,]+)",
    "spirit_natural_keywords": r"自然搜索词[：:]\s*([\d,]+)",
    "spirit_ad_keyword": r"广告流量词[：:]\s*([\d,]+)",
    "spirit_rating": r"评分\(评分数\)[：:]\s*([\d.]+)\(([\d,]+)\)",
    "spirit_price": r"价格[：:]\s*\$?([\d.]+)",
}

# SIF 正则提取子字段
SIF_PATTERNS = {
    "sif_total_kw": r"流量词[：:]\s*([\d,]+)",
    "sif_natural_kw": r"自然搜索词[：:]\s*([\d,]+)",
    "sif_ad_kw": r"广告流量词[：:]\s*([\d,]+)",
    "sif_sales_7d": r"近7天销量[：:]\s*([\d,]+)",
    "sif_bsr": r"BSR[：:]\s*#?([\d,]+)",
}


def get_field(field_id: str) -> Optional[dict]:
    return FIELDS.get(field_id)


def get_fields_by_source(source: str) -> dict:
    return {k: v for k, v in FIELDS.items() if v.get("source") == source}


def list_fields() -> list:
    return list(FIELDS.keys())
