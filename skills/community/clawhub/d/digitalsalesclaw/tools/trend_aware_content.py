#!/usr/bin/env python3
"""
DigitalSalesClaw - trend_aware_content.py
趋势感知内容工具

功能:
- 热点监控（关键词热度趋势）
- 季节性内容推荐
- 竞品内容动态追踪
- 自动生成趋势相关选题

输入: {"action": "trending|seasonal|competitor_content|auto_generate", "keyword": "...", "platform": "..."}
输出: {"trends, topics, content_briefs, suggestions}
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from db import get_conn, close_conn

try:
    import jieba
    import jieba.analyse
    JIEBA = True
except ImportError:
    JIEBA = False

SKILL_DIR = Path(__file__).parent.parent


SEASONAL_CALENDAR = {
    "01": {"name": "一月", "events": ["元旦", "腊八节"], "topics": ["新年健康计划", "冬季养生", "腊八粥食谱"], "diseases": ["流感", "心脑血管"]},
    "02": {"name": "二月", "events": ["春节", "元宵节", "情人节"], "topics": ["节日饮食健康", "春节养生", "年后减脂"], "diseases": ["消化不良", "节后综合征"]},
    "03": {"name": "三月", "events": ["妇女节", "植树节", "世界睡眠日"], "topics": ["女性健康", "春季过敏", "睡眠改善"], "diseases": ["过敏性鼻炎", "春困"]},
    "04": {"name": "四月", "events": ["清明节", "世界卫生日"], "topics": ["清明养生", "春季护肝", "爱国卫生月"], "diseases": ["肝病", "过敏"]},
    "05": {"name": "五月", "events": ["劳动节", "青年节", "护士节", "母亲节"], "topics": ["劳动健康", "护士节致敬", "母亲节礼物-健康", "夏季准备"], "diseases": ["职业病", "颈椎病"]},
    "06": {"name": "六月", "events": ["儿童节", "端午节", "父亲节", "世界献血日"], "topics": ["儿童健康", "端午节养生", "夏季养生", "献血知识"], "diseases": ["手足口病", "中暑"]},
    "07": {"name": "七月", "events": ["建党节", "暑假开始"], "topics": ["暑期安全", "夏季防晒", "儿童暑期健康"], "diseases": ["热射病", "暑期儿童意外"]},
    "08": {"name": "八月", "events": ["建军节", "七夕节"], "topics": ["夏季养生", "七夕健康礼物", "末伏养生"], "diseases": ["湿气重", "空调病"]},
    "09": {"name": "九月", "events": ["教师节", "中秋节", "世界急救日"], "topics": ["教师职业病", "中秋健康饮食", "急救知识"], "diseases": ["咽喉炎", "颈椎病", "月饼健康食用"]},
    "10": {"name": "十月", "events": ["国庆节", "重阳节", "世界精神卫生日"], "topics": ["国庆健康出行", "重阳敬老", "心理健康"], "diseases": ["假期综合征", "高血压"]},
    "11": {"name": "十一月", "events": ["双十一", "感恩节"], "topics": ["冬季养生开始", "双十一健康好物", "心脑血管预防"], "diseases": ["心脑血管", "流感"]},
    "12": {"name": "十二月", "events": ["双十二", "冬至", "圣诞节", "世界艾滋病日"], "topics": ["冬至进补", "年末健康总结", "圣诞健康", "艾滋病预防"], "diseases": ["流感", "心脑血管", "冬季抑郁"]},
}


def get_trending(platform=None, category=None, limit=20):
    """获取当前热点话题"""
    conn = get_conn()
    
    try:
        sql = """
            SELECT cm.campaign_id, cm.impressions, cm.clicks,
                   cm.engagement_rate, cm.date, cc.name as campaign_name
            FROM content_metrics cm
            LEFT JOIN content_campaigns cc ON cc.id = cm.campaign_id
            WHERE cm.date >= date('now', '-14 days') AND cm.impressions > 0
        """
        params = []
        if platform:
            sql += " AND cc.platform = ?"
            params.append(platform)
        sql += " ORDER BY cm.impressions DESC LIMIT 50"

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM content_metrics LIMIT 0").description]
        metrics = [dict(zip(cols, r)) for r in rows]

        keyword_freq = defaultdict(lambda: {"count": 0, "total_imp": 0, "avg_eng": 0})
        for m in metrics:
            campaign_name = m.get("campaign_name", "") or ""
            tokens = list(jieba.cut(campaign_name)) if JIEBA else campaign_name.split()
            for token in tokens:
                if len(token) >= 2:
                    keyword_freq[token]["count"] += 1
                    keyword_freq[token]["total_imp"] += m.get("impressions") or 0
                    keyword_freq[token]["avg_eng"] += m.get("engagement_rate") or 0

        trending = []
        for kw, data in keyword_freq.items():
            if data["count"] >= 2:
                trending.append({
                    "keyword": kw,
                    "content_count": data["count"],
                    "total_impressions": data["total_imp"],
                    "avg_engagement": round(data["avg_eng"] / data["count"], 2),
                    "heat_score": round(data["count"] * 0.3 + data["total_imp"] / 10000 * 0.7, 2),
                })

        trending.sort(key=lambda x: -x["heat_score"])

        now = datetime.now()
        month_key = now.strftime("%m")
        seasonal = SEASONAL_CALENDAR.get(month_key, {})

        return {
            "platform": platform or "all",
            "period": "14d",
            "trending_keywords": trending[:limit],
            "seasonal_topics": seasonal.get("topics", []),
            "seasonal_events": seasonal.get("events", []),
            "current_month": seasonal.get("name", ""),
            "suggestions": [
                f"当前热点：「{'」「'.join([t['keyword'] for t in trending[:3]])}",
                f"本月季节性话题：{'、'.join(seasonal.get('topics', [])[:3])}",
                "建议结合热点及时生成相关内容"
            ]
        }
    finally:
        close_conn(conn)


def get_seasonal_content(month=None):
    """获取当月/指定月的季节性内容推荐"""
    now = datetime.now()
    target_month = month or now.strftime("%m")
    seasonal = SEASONAL_CALENDAR.get(target_month, {})

    if not seasonal:
        return {"error": f"Invalid month: {month}"}

    content_briefs = []
    for topic in seasonal.get("topics", []):
        for disease in seasonal.get("diseases", [])[:2]:
            content_briefs.append({
                "title": f"{seasonal['name']}必看：关于{topic}你必须知道的事",
                "topic": topic,
                "related_disease": disease,
                "platform": "douyin",
                "style": "科普",
                "urgency": "high" if seasonal.get("events") else "medium",
                "content_angle": f"结合{seasonal.get('events', [])[0] if seasonal.get('events') else ''}，从{topic}切入，实用性强",
            })

    return {
        "month": target_month,
        "month_name": seasonal.get("name", ""),
        "events": seasonal.get("events", []),
        "topics": seasonal.get("topics", []),
        "diseases": seasonal.get("diseases", []),
        "content_briefs": content_briefs,
        "suggestions": [
            f"{seasonal['name']}热点：「{'」「'.join(seasonal.get('topics', [])[:3])}",
            f"相关疾病：{'、'.join(seasonal.get('diseases', [])[:3])}",
            "建议提前 1-2 周准备内容，抓住节日流量"
        ]
    }


def track_competitor_content(competitor_name=None, platform=None, limit=20):
    """追踪竞品最近的内容动态"""
    conn = get_conn()
    
    try:
        sql = """
            SELECT ca.competitor_name, ca.competitor_price, ca.competitor_rating,
                   ca.analysis_date, dp.name as product_name, dp.platform
            FROM competitor_analysis ca
            LEFT JOIN drug_products dp ON dp.product_id = ca.product_id
            WHERE 1=1
        """
        params = []
        if competitor_name:
            sql += " AND ca.competitor_name LIKE ?"
            params.append(f"%{competitor_name}%")
        if platform:
            sql += " AND dp.platform = ?"
            params.append(platform)
        sql += " ORDER BY ca.analysis_date DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM competitor_analysis LIMIT 0").description]
        analysis = [dict(zip(cols, r)) for r in rows]

        competitor_summary = defaultdict(lambda: {"records": 0, "latest_price": None, "rating_trend": []})
        for a in analysis:
            name = a.get("competitor_name", "unknown")
            competitor_summary[name]["records"] += 1
            competitor_summary[name]["latest_price"] = a.get("competitor_price")
            competitor_summary[name]["rating_trend"].append(a.get("competitor_rating"))

        summary = []
        for name, data in competitor_summary.items():
            ratings = data["rating_trend"]
            rating_change = None
            if len(ratings) >= 2:
                rating_change = round(ratings[0] - ratings[-1], 2)

            summary.append({
                "competitor_name": name,
                "record_count": data["records"],
                "latest_price": data["latest_price"],
                "latest_rating": ratings[0] if ratings else None,
                "rating_change": rating_change,
                "trend": "up" if rating_change and rating_change > 0 else "down" if rating_change and rating_change < 0 else "stable",
            })

        summary.sort(key=lambda x: -x["record_count"])

        return {
            "competitor_name": competitor_name or "all",
            "platform": platform or "all",
            "total_records": len(analysis),
            "competitor_summary": summary,
            "suggestions": [
                f"追踪了 {len(summary)} 个竞品动态",
                "关注评分上升的竞品，学习其内容策略",
                "注意价格变动的竞品，评估竞争压力"
            ]
        }
    finally:
        close_conn(conn)


def auto_generate_trend_content(keyword=None, platform="douyin", conn=None):
    """基于热点关键词自动生成内容脚本建议"""
    if not keyword:
        trending = get_trending(platform=platform, limit=5)
        top_kw = trending.get("trending_keywords", [])
        keyword = top_kw[0]["keyword"] if top_kw else "健康科普"

    seasonal = SEASONAL_CALENDAR.get(datetime.now().strftime("%m"), {})
    seasonal_topics = seasonal.get("topics", [])

    angles = [
        {"type": "科普", "template": "关于{keyword}，你不知道的3个真相"},
        {"type": "误区", "template": "关于{keyword}的常见误区，80%的人都错了"},
        {"type": "实用", "template": "{keyword}怎么办？教你正确应对方法"},
        {"type": "故事", "template": "一个关于{keyword}的真实故事，看完沉默了"},
        {"type": "数据", "template": "最新研究：{keyword}的惊人数据曝光"},
    ]

    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        related_topics = []
        if JIEBA:
            tokens = list(jieba.cut(keyword))
            for tok in tokens:
                if len(tok) >= 2:
                    rows = conn.execute("""
                        SELECT topic, status, priority FROM content_topics
                        WHERE topic LIKE ? AND status IN ('pending', 'approved')
                        LIMIT 5
                    """, (f"%{tok}%",)).fetchall()
                    for r in rows:
                        related_topics.append({"topic": r[0], "status": r[1], "priority": r[2]})

        content_briefs = []
        for angle in angles:
            title = angle["template"].format(keyword=keyword)

            if platform == "douyin":
                hook = f"你知道{keyword}的真相是什么吗？"
                script_outline = f"""开场钩子（3秒）: {hook}
痛点引入（10秒）: {keyword}是很多人都面临的问题
核心内容（30秒）:
  1. 关于{keyword}的正确认知
  2. 常见的{keyword}误区
  3. 如何正确处理{keyword}
行动号召（5秒）: 点赞关注，每天分享健康知识"""
            elif platform == "xiaohongshu":
                title = f"关于{keyword}，这件事没人告诉你"
                script_outline = f"""封面：{keyword}干货｜建议收藏
开头：{keyword}这件事，越早知道越好
正文结构：
  - 什么是{keyword}
  - {keyword}的3个常见误区
  - 正确应对{keyword}的方法
结尾：你们关于{keyword}有什么经历？评论区见！"""
            else:
                script_outline = f"{keyword}相关深度分析内容"

            content_briefs.append({
                "title": title,
                "platform": platform,
                "angle_type": angle["type"],
                "keyword": keyword,
                "script_outline": script_outline.strip(),
                "estimated_length": "30-60秒" if platform == "douyin" else "300-800字",
                "urgency": "high",
                "related_seasonal": seasonal_topics[:2],
            })

        return {
            "keyword": keyword,
            "platform": platform,
            "content_briefs": content_briefs,
            "related_pending_topics": related_topics[:5],
            "suggestions": [
                f"基于热点「{keyword}」生成了 {len(content_briefs)} 个内容方案",
                f"本月季节性关联：{'、'.join(seasonal_topics[:2])}",
                "建议优先测试「科普」角度，看数据后再调整"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "trending")

    if action == "trending":
        result = get_trending(
            platform=args.get("platform"),
            category=args.get("category"),
            limit=args.get("limit", 20),
        )
    elif action == "seasonal":
        result = get_seasonal_content(month=args.get("month"))
    elif action == "competitor_content":
        result = track_competitor_content(
            competitor_name=args.get("competitor_name"),
            platform=args.get("platform"),
            limit=args.get("limit", 20),
        )
    elif action == "auto_generate":
        result = auto_generate_trend_content(
            keyword=args.get("keyword"),
            platform=args.get("platform", "douyin"),
        )
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
