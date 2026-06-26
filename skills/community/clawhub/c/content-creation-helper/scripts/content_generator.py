#!/usr/bin/env python3
"""
Content Creation Helper for Finance/Trading Platforms

Generates platform-optimized content for:
- Xiaohongshu (小红书) — casual, emoji-heavy
- Zhihu (知乎) — professional, in-depth
- WeChat Official Account (公众号) — semi-formal, structured

Provides:
- generate_xiaohongshu_post() — RED-style notes
- generate_zhihu_answer() — Zhihu answers
- generate_wechat_article() — 公众号 articles
- optimize_title() — SEO title optimization
- generate_hashtags() — Platform-appropriate hashtags
- adapt_across_platforms() — Multi-platform adaptation
"""

def generate_xiaohongshu_post(title, highlights, data_points, insights,
                              risk_note="不构成投资建议,保护好自己的本金最重要！",
                              tags=None):
    """Generate a Xiaohongshu-style post.
    
    Args:
        title: Catchy title (used in cover)
        highlights: String of key insight (1-2 sentences)
        data_points: List of (label, value) tuples for the 行情速览 section
        insights: List of insight strings
        risk_note: Risk disclaimer
        tags: List of hashtags (default: finance/trading tags)
    """
    if tags is None:
        tags = ["#期货", "#交易", "#投资", "#理财", "#复盘"]
    
    emojis = ["🔥", "📌", "📊", "💡", "⚠️"]
    
    post = f"""{emojis[0]} {title}

{emojis[1]} 今日重点
{highlights}

{emojis[2]} 行情速览
"""
    for label, value in data_points:
        post += f"· {label}: {value}\n"
    
    post += f"\n{emojis[3]} 我的思考\n"
    for insight in insights:
        post += f"{insight}\n"
    
    post += f"\n{emojis[4]} 风险提示\n{risk_note}\n\n"
    post += " ".join(tags)
    
    return post


def generate_zhihu_answer(question, key_point, data_points, analysis_points,
                          conclusion, risk_note=None):
    """Generate a Zhihu-style answer.
    
    Args:
        question: The question being answered
        key_point: Core thesis (1 sentence)
        data_points: List of data bullet points
        analysis_points: List of analysis sections
        conclusion: Conclusion text
        risk_note: Risk disclaimer
    """
    if risk_note is None:
        risk_note = "以上内容仅为个人分析,不构成投资建议。期货交易风险较高,请合理控制仓位,设置止损。"
    
    answer = f"""**{question}**

**回答：**

## 一、核心观点
{key_point}

## 二、数据支撑
"""
    for dp in data_points:
        answer += f"- {dp}\n"
    
    answer += "\n## 三、逻辑分析\n"
    for i, ap in enumerate(analysis_points, 1):
        answer += f"{i}. {ap}\n"
    
    answer += f"\n## 四、结论\n{conclusion}\n"
    answer += f"\n---\n⚠️ **风险提示：** {risk_note}"
    
    return answer


def generate_wechat_article(title, summary, sections, disclaimer=None):
    """Generate a WeChat Official Account article.
    
    Args:
        title: Article title
        summary: Brief intro
        sections: List of (heading, content) tuples
        disclaimer: Risk disclaimer
    """
    if disclaimer is None:
        disclaimer = "以上分析仅供参考,不构成投资建议。期货交易风险较大,请根据自身情况谨慎决策。"
    
    article = f"""📌 **{title}**

{summary}

---
"""
    for heading, content in sections:
        article += f"\n## {heading}\n\n{content}\n"
    
    article += f"\n---\n📝 **免责声明：** {disclaimer}\n\n"
    article += "*如果觉得内容有帮助,欢迎点赞/在看/转发👇*"
    
    return article


def optimize_title(text, platform="xiaohongshu"):
    """Optimize a title for the given platform.
    
    Args:
        text: Original title text
        platform: One of 'xiaohongshu', 'zhihu', 'wechat'
    """
    if platform == "xiaohongshu":
        # Add emoji prefix, keep it punchy
        if not any(text.startswith(e) for e in ["🔥", "📈", "💰", "⚠️", "💡"]):
            text = f"🔥 {text}"
        if len(text) > 30:
            text = text[:27] + "..."
    elif platform == "zhihu":
        # Ensure it starts with question form
        if not any(text.startswith(q) for q in ["如何", "怎样", "什么", "为什么", "哪些"]):
            text = f"如何看待{text}？"
    elif platform == "wechat":
        # Add brackets prefix for style
        if not text.startswith("【"):
            text = f"【盘后总结】{text}"
    
    return text


def generate_hashtags(text, platform="xiaohongshu"):
    """Generate relevant hashtags based on content text."""
    common_tags = ["期货", "交易"]
    product_tags = {
        "纯碱": ["纯碱"],
        "甲醇": ["甲醇"],
        "铁矿石": ["铁矿石"],
        "螺纹": ["螺纹钢"],
        "焦炭": ["焦炭"],
        "原油": ["原油"],
        "黄金": ["黄金"],
        "白银": ["白银"],
        "沪深300": ["沪深300"],
        "中证500": ["中证500"],
        "集运": ["集运欧线"],
    }
    
    tags = set(common_tags)
    for keyword, related in product_tags.items():
        if keyword in text:
            tags.update(related)
    
    if platform == "xiaohongshu":
        tags.update(["投资", "理财", "搞钱", "复盘"])
        return [f"#{t}" for t in tags]
    else:
        return list(tags)


def adapt_across_platforms(content, platforms=None):
    """Adapt the same content across multiple platforms."""
    if platforms is None:
        platforms = ["xiaohongshu", "zhihu", "wechat"]
    
    results = {}
    for p in platforms:
        if p == "xiaohongshu":
            results[p] = f"[Adapt to RED style]: {content[:100]}..."
        elif p == "zhihu":
            results[p] = f"[Adapt to Zhihu style]: {content[:100]}..."
        elif p == "wechat":
            results[p] = f"[Adapt to WeChat style]: {content[:100]}..."
    
    return results


if __name__ == "__main__":
    # Demo: generate a sample post
    post = generate_xiaohongshu_post(
        title="纯碱今天又跌了,我为什么反而加仓了？",
        highlights="纯碱今天跌了3%,但我觉得可能是个机会。（不是推荐！！理性看！）",
        data_points=[("纯碱主力合约", "1550,跌幅3.2%"),
                     ("库存", "连续3周累积创新高"),
                     ("技术面", "已经超卖了 ❗️")],
        insights=["利空出尽 + 技术超卖 + 成本支撑",
                  "这三个信号同时出现的时候,往往就是情绪的极致反转点",
                  "当然,右侧确认之前,绝不重仓"],
    )
    print("=== Xiaohongshu Demo ===\n")
    print(post)
