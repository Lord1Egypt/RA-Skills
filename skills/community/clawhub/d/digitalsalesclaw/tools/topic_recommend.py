#!/usr/bin/env python3
"""
DigitalSalesClaw - topic_recommend.py
AI选题推荐引擎
基于热点趋势 + 历史内容表现 + 竞品动态 + 季节性规律 + LLM推理

输入: {"action": "recommend|trending|seasonal", "product": "...", "platform": "...", "limit": 10}
输出: {"topics: [{title, description, type, platforms, keywords, confidence, rationale, urgency}, ...]}
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent

# 季节性选题映射
SEASONAL_TOPICS = {
    "spring": ["春季过敏", "花粉过敏", "春困", "换季感冒", "春季养生"],
    "summer": ["中暑防护", "夏季腹泻", "晒伤", "空调病", "溺水急救"],
    "autumn": ["秋季润燥", "咳嗽", "秋燥", "流感疫苗", "秋季腹泻"],
    "winter": ["流感", "感冒", "心脑血管", "冻伤", "温泉健康"],
    "new_year": ["春节健康", "年夜饭", "喝酒", "熬夜", "节后综合症"],
    "summer_holiday": ["暑假安全", "儿童安全", "海边防晒", "野外急救"],
    "national_day": ["国庆出行", "旅途健康", "急救常识", "常见意外"],
}

# 疾病周期规律（按月份）
DISEASE_SEASONAL = {
    1: ["流感", "心脑血管", "冻伤", "一氧化碳中毒"],
    2: ["流感", "节后综合症", "消化不良"],
    3: ["过敏", "花粉过敏", "哮喘", "结核病"],
    4: ["过敏", "哮喘", "皮肤病", "抑郁症"],
    5: ["过敏", "哮喘", "蚊虫叮咬"],
    6: ["中暑", "空调病", "手足口病", "肠道病毒"],
    7: ["中暑", "热射病", "溺水", "急性肠胃炎"],
    8: ["中暑", "晒伤", "登革热", "乙脑"],
    9: ["流感疫苗", "腹泻", "开学季健康"],
    10: ["流感疫苗", "咳嗽", "秋燥"],
    11: ["流感", "心脑血管", "慢病管理"],
    12: ["流感", "心脑血管", "冻伤", "年终体检"],
}


def get_season() -> str:
    month = datetime.now().month
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        return "winter"


def get_trending_topics() -> list[dict]:
    """从数据库获取高表现选题作为参考"""
    conn = get_conn()
    try:
        topics = conn.execute("""
            SELECT ct.topic, ct.platform, ct.status, ct.priority,
                   cs.title as script_title, cs.content
            FROM content_topics ct
            LEFT JOIN content_scripts cs ON cs.topic_id = ct.id
            WHERE ct.status = 'published'
            ORDER BY ct.created_at DESC
            LIMIT 50
        """).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM content_topics LIMIT 0").description]
        topic_list = [dict(zip(cols, t)) for t in topics]

        keyword_freq = defaultdict(int)
        for t in topic_list:
            content = (t.get("topic", "") + " " + (t.get("script_title") or "") + " " + (t.get("content") or "")).lower()
            for kw in ["糖尿病", "高血压", "感冒", "儿童", "老年人", "心脏", "肝脏", "血糖", "血压", "用药", "健康"]:
                if kw in content:
                    keyword_freq[kw] += 1

        return {
            "topics": topic_list,
            "top_keywords": sorted(keyword_freq.items(), key=lambda x: -x[1])[:10]
        }
    finally:
        close_conn(conn)


def get_seasonal_topics(season: str = None) -> list[str]:
    if season is None:
        season = get_season()
    holidays = []

    # 检测节日
    month = datetime.now().month
    day = datetime.now().day

    if month == 1 and day <= 7:
        holidays.append("new_year")
    elif month == 5 and day >= 1:
        holidays.append("summer_holiday")
    elif month == 10 and day >= 1 and day <= 7:
        holidays.append("national_day")

    topics = []
    for h in holidays:
        topics.extend(SEASONAL_TOPICS.get(h, []))
    topics.extend(SEASONAL_TOPICS.get(season, []))

    # 添加当前月份相关
    topics.extend(DISEASE_SEASONAL.get(month, []))
    return list(set(topics))


def get_competitor_topics() -> list[dict]:
    """获取竞品相关选题"""
    conn = get_conn()
    try:
        products = conn.execute("""
            SELECT name, category, platform FROM drug_products
            ORDER BY reviews_count DESC LIMIT 10
        """).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM drug_products LIMIT 0").description]
        product_list = [dict(zip(cols, p)) for p in products]

        return product_list
    finally:
        close_conn(conn)


def get_high_performance_patterns() -> dict:
    """分析高表现内容的共同特征"""
    conn = get_conn()
    try:
        metrics = conn.execute("""
            SELECT cm.*, cc.name as campaign_name, cc.platform
            FROM content_metrics cm
            JOIN content_campaigns cc ON cc.id = cm.campaign_id
            WHERE cm.engagement_rate > 0.02 OR cm.ctr > 0.03
            ORDER BY cm.engagement_rate DESC
            LIMIT 30
        """).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM content_metrics LIMIT 0").description]
        metric_list = [dict(zip(cols, m)) for m in metrics]

        platform_stats = defaultdict(lambda: {"count": 0, "avg_engagement": 0, "total_engagement": 0})
        for m in metric_list:
            plat = m.get("platform", "unknown")
            eng = m.get("engagement_rate") or 0
            platform_stats[plat]["count"] += 1
            platform_stats[plat]["total_engagement"] += eng

        for plat in platform_stats:
            if platform_stats[plat]["count"] > 0:
                platform_stats[plat]["avg_engagement"] = platform_stats[plat]["total_engagement"] / platform_stats[plat]["count"]

        return {
            "high_performance_count": len(metric_list),
            "platform_stats": dict(platform_stats),
            "avg_ctr": sum(m.get("ctr") or 0 for m in metric_list) / max(len(metric_list), 1),
        }
    finally:
        close_conn(conn)



def generate_recommendations(product: str = None, platform: str = None, limit: int = 10) -> dict:
    """生成选题推荐"""
    trending = get_trending_topics()
    season = get_season()
    seasonal = get_seasonal_topics(season)
    competitor = get_competitor_topics()
    patterns = get_high_performance_patterns()

    # 纯规则生成（LLM推理由OpenClaw agent负责）

    # Fallback: 基于规则生成
    fallback_topics = []
    for kw in seasonal[:limit]:
        urgency = "high" if kw in ["流感", "感冒", "过敏"] else "normal"
        fallback_topics.append({
            "title": f"关于{kw}，你必须知道的事",
            "description": f"全面介绍{kw}的预防、识别和日常管理方法",
            "content_type": "科普",
            "target_audience": "普通大众",
            "platforms": ["douyin", "xiaohongshu"],
            "keywords": [kw, "健康", "科普"],
            "confidence": 0.6,
            "rationale": f"基于当前季节({season})推荐",
            "urgency": urgency,
            "estimated_engagement": "中"
        })

    return {
        "method": "rule_based",
        "season": season,
        "topics": fallback_topics,
        "trending_keywords": trending.get("top_keywords", [])[:5],
        "seasonal_topics": seasonal[:5],
    }


def get_trending_keywords() -> dict:
    """获取当前热点关键词"""
    conn = get_conn()
    try:
        topics = conn.execute("""
            SELECT topic, platform, status, priority
            FROM content_topics
            ORDER BY created_at DESC LIMIT 100
        """).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM content_topics LIMIT 0").description]
        topic_list = [dict(zip(cols, t)) for t in topics]

        kw_count = defaultdict(int)
        for t in topic_list:
            topic = t.get("topic", "")
            for kw in re.findall(r'[\u4e00-\u9fa5]{2,}', topic):
                if len(kw) >= 2 and kw not in ["关于", "必须", "知道", "如何"]:
                    kw_count[kw] += 1

        top_kws = sorted(kw_count.items(), key=lambda x: -x[1])[:20]
        return {
            "keywords": [{"keyword": k, "count": c} for k, c in top_kws],
            "data_source": "content_topics",
            "total_topics": len(topic_list)
        }
    finally:
        close_conn(conn)


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": "recommend"}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"action": "recommend"}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "recommend")
    product = args.get("product")
    platform = args.get("platform")
    limit = args.get("limit", 10)

    if action == "recommend":
        result = generate_recommendations(product, platform, limit)
    elif action == "trending":
        result = get_trending_keywords()
    elif action == "seasonal":
        season = get_season()
        result = {
            "season": season,
            "topics": get_seasonal_topics(season),
            "disease_calendar": DISEASE_SEASONAL.get(datetime.now().month, [])
        }
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
