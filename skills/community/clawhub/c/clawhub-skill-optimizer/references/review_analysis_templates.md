# Review Analysis Templates & Sentiment Analysis
# 用户评论分析模板与情感分析

## 1. Review Collection / 评论收集

### Manual Review Collection:

```python
# ── Simulated review data structure ───────────────────────
REVIEWS = [
    {
        "platform": "clawhub",
        "user": "user_xxx",
        "rating": 5,
        "text": "非常好用！帮助我在一周内完成了3个投标文件，强烈推荐！",
        "date": "2026-05-01",
        "helpful_count": 12
    },
    {
        "platform": "clawhub",
        "user": "user_yyy",
        "rating": 4,
        "text": "功能很全，但希望能有更多模板。还有英文版本吗？",
        "date": "2026-05-02",
        "helpful_count": 8
    },
    {
        "platform": "clawhub",
        "user": "user_zzz",
        "rating": 2,
        "text": "太复杂了，看不懂怎么用。文档写得像教科书，希望能加点示例。",
        "date": "2026-05-03",
        "helpful_count": 5
    },
    {
        "platform": "weibo",
        "user": "微博用户",
        "rating": 5,
        "text": "终于有人做了保险投标的专业工具！比通用AI好用太多！",
        "date": "2026-05-01",
        "helpful_count": 23
    },
    {
        "platform": "zhihu",
        "user": "保险精算师",
        "rating": 4,
        "text": "偿二代内容很专业，但希望加上2025年第四套生命表的内容。",
        "date": "2026-05-02",
        "helpful_count": 15
    },
]
```

## 2. Sentiment Analysis Engine / 情感分析引擎

```python
import re
from collections import Counter, defaultdict

# ── Sentiment Lexicons ─────────────────────────────────────
POSITIVE_EN = {
    "great", "amazing", "excellent", "love", "perfect", "awesome",
    "fantastic", "helpful", "useful", "best", "brilliant", "wonderful",
    "outstanding", "superb", "recommended", "impressive", "powerful"
}

NEGATIVE_EN = {
    "confusing", "broken", "bug", "issue", "problem", "wrong",
    "difficult", "hard", "complicated", "frustrated", "disappointed",
    "useless", "waste", "annoying", "poor", "bad", "fail", "error"
}

POSITIVE_CN = {
    "好", "棒", "赞", "优秀", "完美", "实用", "有用", "强大",
    "推荐", "感谢", "喜欢", "专业", "详细", "全面", "高效"
}

NEGATIVE_CN = {
    "差", "难", "复杂", "问题", "错误", "不懂", "没用", "失望",
    "模糊", "缺", "少", "希望", "建议", "改进", "希望有",
    "太", "不够", "没有", "无法", "无法理解"
}

# ── Core Sentiment Analyzer ────────────────────────────────
def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of a single review text."""
    text_lower = text.lower()

    pos_count = sum(1 for w in POSITIVE_EN if w in text_lower)
    neg_count = sum(1 for w in NEGATIVE_EN if w in text_lower)

    for w in POSITIVE_CN:
        if w in text: pos_count += 1
    for w in NEGATIVE_CN:
        if w in text: neg_count += 1

    # Score: positive - negative
    score = pos_count - neg_count

    if score >= 2:
        sentiment = "POSITIVE"
    elif score <= -2:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return {
        "text": text,
        "sentiment": sentiment,
        "pos_count": pos_count,
        "neg_count": neg_count,
        "score": score
    }


# ── Full Review Analysis ───────────────────────────────────
def analyze_all_reviews(reviews: list[dict]) -> dict:
    """Comprehensive review analysis."""

    sentiments = [analyze_sentiment(r["text"]) for r in reviews]

    results = {
        "total_reviews": len(reviews),
        "avg_rating": round(sum(r["rating"] for r in reviews) / len(reviews), 2),
        "sentiment_distribution": Counter(s["sentiment"] for s in sentiments),
        "positive_reviews": [],
        "negative_reviews": [],
        "feature_requests": [],
        "pain_points": [],
        "top_keywords": Counter(),
    }

    feature_patterns = [
        r"希望(.+)", r"建议(.+)", r"能不能(.+)",
        r"wish (.+)could", r"would be nice", r"should have",
        r"add (.+)feature", r"include (.+)", r"support (.+)"
    ]

    pain_point_patterns = [
        r"不懂", r"不会用", r"复杂", r"搞不清楚",
        r"confusing", r"complicated", r"hard to",
        r"don't understand", r"can't figure out"
    ]

    for review, sentiment in zip(reviews, sentiments):
        text = review["text"]
        rating = review["rating"]

        if sentiment["sentiment"] == "POSITIVE" or rating >= 4:
            results["positive_reviews"].append({
                "user": review["user"],
                "text": text,
                "rating": rating,
                "platform": review["platform"]
            })

        if sentiment["sentiment"] == "NEGATIVE" or rating <= 2:
            results["negative_reviews"].append({
                "user": review["user"],
                "text": text,
                "rating": rating,
                "platform": review["platform"],
                "urgency": "CRITICAL" if rating <= 1 else "HIGH"
            })

        # Feature requests
        for pattern in feature_patterns:
            match = re.search(pattern, text)
            if match:
                results["feature_requests"].append({
                    "request": match.group(0),
                    "user": review["user"],
                    "platform": review["platform"],
                    "priority": "HIGH" if rating >= 4 else "MEDIUM"
                })

        # Pain points
        for pattern in pain_point_patterns:
            if re.search(pattern, text):
                results["pain_points"].append({
                    "pain_point": text,
                    "user": review["user"],
                    "platform": review["platform"],
                    "urgency": "CRITICAL" if rating <= 2 else "MEDIUM"
                })

        # Keywords
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        results["top_keywords"].update(words)

    return results


# ── Generate Report ────────────────────────────────────────
def generate_review_report(reviews: list[dict], skill_name: str) -> str:
    """Generate a structured review analysis report."""

    analysis = analyze_all_reviews(reviews)

    report = f"""
# 📝 Review Analysis Report
**Skill**: {skill_name}
**Total Reviews**: {analysis['total_reviews']}
**Average Rating**: ⭐ {analysis['avg_rating']} / 5.0
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 Overview

| Metric | Value |
|--------|-------|
| Total Reviews | {analysis['total_reviews']} |
| Average Rating | {analysis['avg_rating']} |
| Positive Reviews | {Counter(analysis['sentiment_distribution'])['POSITIVE']} |
| Neutral Reviews | {Counter(analysis['sentiment_distribution'])['NEUTRAL']} |
| Negative Reviews | {Counter(analysis['sentiment_distribution'])['NEGATIVE']} |
| Feature Requests | {len(analysis['feature_requests'])} |
| Pain Points | {len(analysis['pain_points'])} |

---

## ⭐ Top Praised Features (from 4-5 star reviews)

"""
    for i, rev in enumerate(analysis["positive_reviews"][:5], 1):
        report += f"{i}. **[{rev['platform']}]** \"{rev['text']}\" — {rev['user']}\n"

    report += "\n## 💡 Feature Requests (Prioritized)\n\n"
    for i, req in enumerate(analysis["feature_requests"], 1):
        report += f"{i}. **{req['request']}** [Priority: {req['priority']}] — {req['platform']}\n"

    report += "\n## ⚠️ Pain Points (Fix Priority)\n\n"
    for i, pp in enumerate(analysis["pain_points"], 1):
        report += f"{i}. **[{pp['urgency']}]** \"{pp['pain_point']}\" — {pp['platform']}\n"

    report += "\n## 🔑 Top Keywords in Reviews\n\n"
    report += "| Keyword | Frequency |\n|---------|-----------|\n"
    for kw, count in analysis["top_keywords"].most_common(15):
        report += f"| {kw} | {count} |\n"

    report += "\n## 🎯 Recommended Actions\n\n"
    report += "| Priority | Action | Reason |\n|---------|--------|--------|\n"
    for req in sorted(analysis["feature_requests"], key=lambda x: x["priority"] == "HIGH", reverse=True)[:3]:
        report += f"| HIGH | Address: {req['request'][:40]} | Multiple users requesting |\n"
    for pp in sorted(analysis["pain_points"], key=lambda x: x["urgency"])[:2]:
        report += f"| CRITICAL | Fix pain point: {pp['pain_point'][:40]} | Hurting user experience |\n"

    return report
```

## 3. Review Response Templates / 评论回复模板

```markdown
## For Positive Reviews (5 stars):
> "非常感谢您的认可！🙏 我们很高兴这个技能对您有帮助。您的支持是我们持续优化的动力！"

## For Feature Requests (4-5 stars):
> "感谢您的建议！{具体建议}已经在我们的开发计划中，预计在下一个版本中加入。感谢您帮助我们改进！"

## For Pain Points (1-2 stars):
> "抱歉给您带来不好的体验！{具体问题}是我们需要改进的地方。建议您：{具体解决方案}。也可以联系我们的客服获取帮助，我们会持续优化。"

## For Confusing UX (2-3 stars):
> "感谢您的反馈！我们的文档确实可以更易懂。我们已添加了{具体改进}，希望对您有帮助。如果您有任何问题，随时联系我们！"
```

## 4. Competitive Intelligence / 竞品情报分析

```python
# ── Competitor Review Analysis ─────────────────────────────
def analyze_competitor_reviews(competitor_skills: list[dict]) -> dict:
    """
    Analyze reviews of competing skills to find gaps and opportunities.
    competitor_skills: list of dicts with {name, reviews: []}
    """
    findings = {
        "gaps": [],        # What users want but competitors lack
        "complaints": [],  # Common complaints across competitors
        "praises": [],     # What competitors do well
        "opportunities": []  # High-value, low-competition features
    }

    for skill in competitor_skills:
        analysis = analyze_all_reviews(skill["reviews"])

        # Extract unique praises (what this competitor does well)
        for rev in analysis["positive_reviews"][:3]:
            findings["praises"].append({
                "skill": skill["name"],
                "text": rev["text"]
            })

        # Extract gaps (feature requests = gaps)
        for req in analysis["feature_requests"]:
            findings["gaps"].append({
                "skill": skill["name"],
                "request": req["request"]
            })

    # Find opportunities (gaps mentioned by multiple competitors' users)
    gap_counter = Counter(g["request"] for g in findings["gaps"])
    findings["opportunities"] = [
        {"feature": feature, "count": count,
         "opportunity": "Many users want this — few provide it"}
        for feature, count in gap_counter.most_common(10)
        if count >= 2  # Mentioned by 2+ competitors' users
    ]

    return findings
```

## 5. Review-Based Skill Improvement Workflow / 基于评论的技能改进流程

```markdown
## Weekly Review Improvement Cycle

### Monday: Collect & Analyze
- Pull all reviews from: ClawHub + social media mentions
- Run sentiment analysis
- Generate Review Analysis Report

### Tuesday: Prioritize Issues
- Tag issues by type: Bug / UX / Missing Feature / Documentation
- Score by frequency × severity
- Create backlog of top 5 issues to fix

### Wednesday: Implement Fixes
- Fix critical bugs (if any)
- Simplify confusing sections in documentation
- Add missing examples/tutorials

### Thursday: Test & Prepare Update
- Test all changes locally
- Update CHANGELOG.md
- Prepare version bump

### Friday: Publish Update
- Publish v1.x.x update
- Reply to reviews thanking + noting improvements
- Share update on social media
```
