#!/usr/bin/env python3
"""
DigitalSalesClaw - content_predict.py
内容效果预测
基于历史数据 + 内容特征 + 平台算法规律预测互动率/CTR/完播率

输入: {"action": "predict|score", "topic": "...", "platform": "douyin", "title": "...", "content": "..."}
输出: {"predicted_engagement, ctr, completion_rate, score, factors, suggestions}
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# 历史数据统计
def get_platform_baselines(conn, platform: str) -> dict:
    """获取平台基准指标"""
    rows = conn.execute("""
        SELECT
            AVG(engagement_rate) as avg_engagement,
            AVG(ctr) as avg_ctr,
            AVG(CASE WHEN engagement_rate > 0 THEN engagement_rate ELSE NULL END) as avg_engagement_nonzero,
            COUNT(*) as sample_count
        FROM content_metrics cm
        JOIN content_campaigns cc ON cc.id = cm.campaign_id
        WHERE cc.platform = ?
          AND cm.date >= date('now', '-90 days')
    """, (platform,)).fetchone()

    return {
        "avg_engagement": rows[0] or 0.02,
        "avg_ctr": rows[1] or 0.03,
        "avg_engagement_nonzero": rows[2] or 0.05,
        "sample_count": rows[3] or 10,
    }


def analyze_title_quality(title: str) -> dict:
    """分析标题质量"""
    score = 50  # 基础分
    factors = []
    issues = []

    # 加分项
    if any(kw in title for kw in ["揭秘", "真相", "竟然", "原来", "难怪"]):
        score += 10
        factors.append("悬念词（揭秘/真相等）加分")
    if any(kw in title for kw in ["!", "？", "！", "？"]):
        score += 8
        factors.append("使用标点符号增强语气")
    if re.search(r'\d+', title):
        score += 10
        factors.append("含数字增强可信度")
    if len(title) <= 20:
        score += 8
        factors.append("标题长度适中（≤20字）")
    elif len(title) > 35:
        score -= 5
        issues.append("标题过长可能影响点击率")
    if any(kw in title for kw in ["必须", "收藏", "转发", "关注"]):
        score += 5
        factors.append("行动引导词加分")
    if any(kw in title for kw in ["这种", "这个", "那个", "竟然"]):
        score += 5
        factors.append("指代词引发好奇心")

    # 扣分项
    if any(kw in title for kw in ["最佳", "第一", "顶级", "绝对"]):
        score -= 15
        issues.append("含绝对化用语，可能违规且降低可信度")
    if any(kw in title for kw in ["根治", "治愈", "保证"]):
        score -= 20
        issues.append("含医疗效果承诺，违反广告法")
    if title.startswith(("所以", "因为", "由于")):
        score -= 5
        issues.append("开头平淡，缺乏悬念")

    return {
        "score": max(0, min(100, score)),
        "factors": factors,
        "issues": issues,
        "length": len(title),
    }


def analyze_content_quality(content: str, topic: str) -> dict:
    """分析内容质量"""
    score = 50
    factors = []
    issues = []

    # 长度分析
    char_count = len(content)
    if 300 <= char_count <= 600:
        score += 10
        factors.append("字数适中（300-600字）")
    elif char_count < 200:
        score -= 5
        issues.append("内容过短，信息量不足")
    elif char_count > 2000:
        score -= 5
        issues.append("内容过长，可能影响完播率")

    # 结构分析
    paragraphs = content.split('\n')
    has_structure = len(paragraphs) >= 3
    if has_structure:
        score += 8
        factors.append("结构清晰，分段合理")

    # 关键词覆盖
    topic_kw = topic[:4] if topic else ""
    if topic_kw and topic_kw in content:
        score += 5
        factors.append("内容紧扣主题")

    # 互动引导
    if any(kw in content for kw in ["评论区", "评论", "你们觉得", "觉得呢"]):
        score += 8
        factors.append("有互动引导，提升评论率")
    if any(kw in content for kw in ["点赞", "关注", "收藏"]):
        score += 5
        factors.append("有行动引导")

    # 合规风险词检测
    banned = ["根治", "治愈", "最佳", "第一", "顶级", "无效退款"]
    found_banned = [kw for kw in banned if kw in content]
    if found_banned:
        score -= 15 * len(found_banned)
        issues.append(f"含合规风险词：{', '.join(found_banned)}")

    return {
        "score": max(0, min(100, score)),
        "factors": factors,
        "issues": issues,
        "char_count": char_count,
        "paragraph_count": len(paragraphs),
    }


def predict_performance(topic: str, title: str, content: str, platform: str) -> dict:
    """预测内容效果"""
    conn = get_conn()
    
    try:
        baselines = get_platform_baselines(conn, platform)

        title_analysis = analyze_title_quality(title) if title else {"score": 50, "factors": [], "issues": []}
        content_analysis = analyze_content_quality(content, topic) if content else {"score": 50, "factors": [], "issues": []}

        # 综合评分
        title_weight = 0.4
        content_weight = 0.4
        baseline_weight = 0.2

        quality_score = (
            title_analysis["score"] * title_weight +
            content_analysis["score"] * content_weight +
            baselines["avg_engagement_nonzero"] * 100 * baseline_weight
        )

        # 预测指标
        base_engagement = baselines["avg_engagement_nonzero"]
        engagement_multiplier = quality_score / 50  # 质量分影响系数

        predicted_engagement = min(0.5, base_engagement * engagement_multiplier)
        predicted_ctr = min(0.15, baselines["avg_ctr"] * (title_analysis["score"] / 50))
        predicted_completion = min(0.95, 0.5 + (quality_score / 100) * 0.4)

        # 效果评级
        if predicted_engagement >= 0.08:
            rating = "excellent"
            rating_text = "优秀"
        elif predicted_engagement >= 0.04:
            rating = "good"
            rating_text = "良好"
        elif predicted_engagement >= 0.02:
            rating = "average"
            rating_text = "一般"
        else:
            rating = "poor"
            rating_text = "待优化"

        # 建议
        suggestions = []
        if title_analysis["score"] < 60:
            suggestions.append(f"标题优化建议：{' '.join(title_analysis['issues']) if title_analysis['issues'] else '增加悬念词、数字或疑问句'}")
        if content_analysis["score"] < 60:
            suggestions.append(f"内容优化建议：{' '.join(content_analysis['issues']) if content_analysis['issues'] else '丰富内容结构，增加互动引导'}")
        if not suggestions:
            suggestions.append("整体质量良好，可按计划发布")

        return {
            "topic": topic,
            "title": title,
            "platform": platform,
            "predicted_engagement_rate": round(predicted_engagement, 4),
            "predicted_ctr": round(predicted_ctr, 4),
            "predicted_completion_rate": round(predicted_completion, 4),
            "quality_score": round(quality_score, 1),
            "rating": rating,
            "rating_text": rating_text,
            "baselines": baselines,
            "title_analysis": title_analysis,
            "content_analysis": content_analysis,
            "suggestions": suggestions,
        }
    finally:
        close_conn(conn)


def quick_score(topic: str, title: str, platform: str = "douyin") -> dict:
    """快速评分（不分析正文）"""
    title_analysis = analyze_title_quality(title) if title else {"score": 50}

    # 平台基准
    platform_baselines = {
        "douyin": {"expected_ctr": 0.03, "expected_engagement": 0.05},
        "xiaohongshu": {"expected_ctr": 0.05, "expected_engagement": 0.06},
        "wechat": {"expected_ctr": 0.02, "expected_engagement": 0.03},
    }
    base = platform_baselines.get(platform, platform_baselines["douyin"])

    score = title_analysis["score"]
    ctr_score = min(0.15, base["expected_ctr"] * (score / 50))

    return {
        "topic": topic,
        "title": title,
        "platform": platform,
        "title_score": title_analysis["score"],
        "predicted_ctr": round(ctr_score, 4),
        "factors": title_analysis.get("factors", []),
        "issues": title_analysis.get("issues", []),
        "quick_verdict": "良好" if score >= 60 else "需优化" if score >= 40 else "较差",
    }


def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"topic": sys.argv[1]}
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
    action = args.get("action", "predict")
    topic = args.get("topic", "")
    title = args.get("title", "")
    content = args.get("content", "")
    platform = args.get("platform", "douyin")

    if action == "score":
        result = quick_score(topic, title, platform)
    else:
        result = predict_performance(topic, title, content, platform)

    print(json.dumps(result, ensure_ascii=False, indent=2))
