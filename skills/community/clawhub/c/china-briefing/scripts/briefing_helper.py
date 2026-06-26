#!/usr/bin/env python3
"""
briefing_helper.py — 新闻简报辅助工具

功能：根据用户需求自动判断地理/行业尺度，推荐搜索策略。

用法:
  python3 scripts/briefing_helper.py <关键词>
  
示例:
  python3 scripts/briefing_helper.py 江川路街道
  python3 scripts/briefing_helper.py 国际新闻
  python3 scripts/briefing_helper.py AI
"""
import sys
import json

# 行政区划（扩展）
PROVINCES = {
    "北京", "上海", "天津", "重庆",
    "广东", "江苏", "浙江", "山东", "河南", "四川", "湖北", "湖南",
    "河北", "山西", "辽宁", "吉林", "黑龙江", "安徽", "福建", "江西",
    "陕西", "甘肃", "青海", "台湾", "内蒙古", "广西", "西藏", "宁夏", "新疆",
    "香港", "澳门", "海南", "贵州", "云南"
}

MAJOR_CITIES = {
    "北京", "上海", "广州", "深圳", "重庆", "成都", "杭州", "南京",
    "武汉", "西安", "天津", "苏州", "郑州", "长沙", "东莞", "青岛",
    "宁波", "沈阳", "大连", "厦门", "昆明", "哈尔滨", "济南", "合肥",
    "福州", "南昌", "长春", "石家庄", "贵阳", "南宁", "太原", "兰州",
    "乌鲁木齐", "呼和浩特", "银川", "拉萨", "西宁", "海口", "三亚"
}

INDUSTRY_KEYWORDS = {
    "AI", "人工智能", "大模型", "芯片", "半导体",
    "科技", "互联网", "软件", "算法", "算力",
    "股票", "股市", "财经", "经济", "市场", "汇率", "基金", "债券",
    "房产", "楼市", "房价", "房地产",
    "汽车", "新能源", "电动车", "电池",
    "医疗", "健康", "疫情", "疫苗",
    "教育", "高考", "考研", "留学",
    "游戏", "电竞", "动漫",
    "体育", "足球", "篮球", "奥运会", "世界杯",
    "军事", "国防", "军队",
    "航天", "火箭", "卫星", "太空",
}

GLOBAL_KEYWORDS = [
    "国际", "全球", "world", "international", "海外", "外交",
    "美国", "俄罗斯", "日本", "韩国", "朝鲜", "英国", "法国",
    "德国", "伊朗", "以色列", "欧盟", "北约", "联合国"
]

LOCAL_DISTRICT_SUFFIXES = [
    "区", "街道", "镇", "乡", "县", "市", "新区", "开发区",
    "镇", "村", "社区"
]


def detect_scale(query: str) -> dict:
    """Detect the briefing scale from user query"""
    q = query.strip().lower()

    # Check industry first (can be at any scale)
    industry = None
    for kw in INDUSTRY_KEYWORDS:
        if kw.lower() in q:
            industry = kw
            break

    # Check global
    for kw in GLOBAL_KEYWORDS:
        if kw.lower() in q:
            return {"scale": "global", "industry": industry, "location": "",
                    "search_queries": _global_queries(industry)}

    # Check province
    for p in PROVINCES:
        if p in q:
            return {"scale": "province", "industry": industry, "location": p,
                    "search_queries": _province_queries(p, industry)}

    # Check city
    for c in MAJOR_CITIES:
        if c in q:
            return {"scale": "city", "industry": industry, "location": c,
                    "search_queries": _city_queries(c, industry)}

    # Check district/street (anything ending in suffixes)
    loc = ""
    for suffix in LOCAL_DISTRICT_SUFFIXES:
        if suffix in q:
            # Extract location name (everything before suffix + suffix)
            idx = q.index(suffix)
            loc = q[:idx + 1]
            break

    if loc and len(loc) >= 2:
        return {"scale": "local", "industry": industry, "location": loc,
                "search_queries": _local_queries(loc, industry)}

    # Default: if no scale detected, try industry or general
    if industry:
        return {"scale": "industry", "industry": industry, "location": "",
                "search_queries": _industry_queries(industry)}

    # Try to match anything
    if len(q) >= 2:
        loc = q
        return {"scale": "local", "industry": None, "location": loc,
                "search_queries": _local_queries(loc, None)}

    return {"scale": "general", "industry": None, "location": "",
            "search_queries": ["今日新闻 最新 2026"]}


def _global_queries(industry):
    queries = [
        "world news latest today April 2026",
        "国际新闻 重大事件 2026",
        "international breaking news global",
    ]
    if industry:
        queries.append(f"{industry} global news 2026")
    return queries


def _province_queries(province, industry):
    queries = [
        f"{province} 2026 最新动态",
        f"{province} 经济 民生 政策",
        f"{province} 政府 新闻",
    ]
    if industry:
        queries.append(f"{province} {industry}")
    return queries


def _city_queries(city, industry):
    queries = [
        f"{city} 2026 最新",
        f"{city} 民生 经济 社区",
        f"{city} 政府 实事项目",
        f"{city} 人大 会议",
    ]
    if industry:
        queries.append(f"{city} {industry}")
    return queries


def _local_queries(loc, industry):
    queries = [
        f"{loc} 2026 最新",
        f"{loc} 民生 实事",
        f"{loc} 社区 改造",
        f"{loc} 公众号",
    ]
    if industry:
        queries.append(f"{loc} {industry}")
    return queries


def _industry_queries(industry):
    return [
        f"{industry} 最新进展 2026",
        f"{industry} news latest April 2026",
        f"{industry} 行业 趋势",
    ]


def print_strategy(result):
    """Print recommended search strategy"""
    scale_names = {
        "global": "🌍 全球尺度",
        "province": "🏛️ 省级尺度",
        "city": "🏙️ 城市尺度",
        "local": "📍 区县/街道尺度",
        "industry": "🏭 行业尺度",
        "general": "📋 综合尺度"
    }

    print(f"\n{'='*50}")
    print(f"  尺度识别: {scale_names.get(result['scale'], result['scale'])}")
    if result['location']:
        print(f"  位置: {result['location']}")
    if result['industry']:
        print(f"  行业: {result['industry']}")
    print(f"{'='*50}")
    print(f"\n推荐搜索词:")
    for i, q in enumerate(result['search_queries'], 1):
        print(f"  {i}. {q}")
    print()


def main():
    if len(sys.argv) < 2:
        # Demo mode
        demos = ["国际简报", "上海简报", "江川路街道简报", "AI行业简报"]
        for d in demos:
            print(f"\n--- 输入: {d} ---")
            result = detect_scale(d)
            print_strategy(result)
        return

    query = sys.argv[1]
    result = detect_scale(query)
    print_strategy(result)

    # Output JSON for programmatic use
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
