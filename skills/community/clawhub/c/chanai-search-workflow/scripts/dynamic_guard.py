#!/usr/bin/env python3
import json
import sys

DYNAMIC_KEYWORDS = [
    "航班", "机票", "票价", "余票", "舱位", "酒店", "房价", "库存", "现货", "价格", "股价", "币价", "新闻", "突发", "报名", "开售", "门票", "演唱会", "演出", "availability", "price", "stock", "flight", "hotel", "ticket", "fare", "booking"
]

DYNAMIC_SUBTYPES = {
    "flight": ["航班", "机票", "直飞", "中转", "舱位", "余票", "flight", "fare", "airline"],
    "hotel": ["酒店", "房价", "房态", "入住", "hotel", "room", "check-in"],
    "product-price": ["价格", "库存", "现货", "优惠", "京东", "淘宝", "天猫", "price", "stock", "sale"],
    "ticketing": ["门票", "演出", "演唱会", "报名", "开售", "ticket", "booking"],
    "finance-news": ["股价", "币价", "基金", "新闻", "突发", "stock", "coin", "news", "breaking"],
}


def detect_subtype(query: str):
    q = query.lower()
    scores = []
    for subtype, kws in DYNAMIC_SUBTYPES.items():
        hit = sum(1 for k in kws if k.lower() in q)
        if hit:
            scores.append((hit, subtype))
    scores.sort(reverse=True)
    return scores[0][1] if scores else None


def main():
    if len(sys.argv) < 2:
        print("Usage: dynamic_guard.py <query>", file=sys.stderr)
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    q = query.lower()
    matched = [k for k in DYNAMIC_KEYWORDS if k.lower() in q]
    is_dynamic = len(matched) > 0
    subtype = detect_subtype(query) if is_dynamic else None
    result = {
        "query": query,
        "isDynamic": is_dynamic,
        "dynamicSubtype": subtype,
        "matchedKeywords": matched,
        "guidance": guidance(is_dynamic),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def guidance(is_dynamic: bool):
    if not is_dynamic:
        return ["No dynamic-info guard triggered."]
    return [
        "Treat public-web search as preliminary discovery only.",
        "Prefer real-time or official pages for final decision advice.",
        "Do not present search snippets or aggregator blurbs as final truth.",
        "Explicitly separate preliminary findings from real-time page findings.",
    ]


if __name__ == "__main__":
    main()
