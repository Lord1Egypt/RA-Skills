---
name: ClawHub Skill Growth Engine
description: AI-powered ClawHub skill growth optimizer v2.0 — analyzes reviews, tracks 2026 trending topics (AI Agent, MCP, video SEO), rewrites titles/descriptions for maximum downloads and stars. Supports video thumbnail prompts, cross-platform social syndication, and growth metrics tracking. Triggers: clawhub optimization, skill growth, SEO, stars, downloads, review analysis, trending keywords, skill improvement, GitHub stars strategy, video SEO, social media integration, thumbnail generation.
slug: clawhub-skill-optimizer
version: 2.1.0
allowed-tools: []
capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - code-examples-reference
---

# ClawHub Skill Growth Engine / ClawHub技能热度增长引擎

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**
>
> **⚠️ 数据安全警告**
> - 本技能仅提供ClawHub技能优化策略的参考框架，**不执行任何代码或脚本**
> - 文中的Python代码为**教学参考示例**，展示逻辑概念，不会自动执行
> - 文中的API调用（如Google Trends、微博热搜、GitHub Trending）为**外部服务引用**，用户如实际调用需自行评估数据隐私风险：查询关键词、IP地址、时间戳等信息将被发送至第三方平台
> - 不收集、不存储用户的任何平台数据、技能代码或个人信息
> - 热度分析和SEO建议基于公开信息，实际效果因平台算法变化而异
> - 不保证任何优化策略能带来具体的下载量或Star数增长
> - **用户确认要求**：所有涉及修改技能元数据或发布社交媒体内容的建议，均需用户自行手动操作并确认



> **English:** AI-powered growth engine for ClawHub skills — analyze user reviews, track global trending topics, and rewrite your skill metadata (title, description, tags) to maximize downloads and GitHub-style stars.
>
> **中文:** ClawHub技能热度增长引擎——分析用户评论、追踪全网热点、优化技能标题与描述，一站式提升下载量与Star数。

## Trigger Keywords / 触发关键词

**⚠️ 精确触发规则**：仅当用户明确提到ClawHub技能增长/优化需求时激活。日常对话中提及"SEO"、"下载量"、"stars"、"热度"等通用词汇时**不会自动触发**，必须与**ClawHub技能优化**直接关联。

**用户确认规则**：匹配以下关键词时，需先向用户确认后再进入优化模式：
- "您需要ClawHub技能优化建议吗？"
- 仅在用户明确确认后，才提供具体分析和建议

激活关键词（需用户确认后生效）：

- ClawHub 优化 / clawhub 技能增长 / 技能热度提升
- 技能下载量提升 / 技能曝光优化 / 技能SEO
- 评论分析 / 用户反馈分析 / review 分析
- 热点追踪 / 热搜分析 / 趋势挖掘
- 标题优化 / description 优化 / 关键词优化
- skill 改进 / 技能改进 / 提升关注度

## Section 0: Latest ClawHub Platform Updates (2026-05-11)

| 更新日期 | 平台/趋势 | 对技能优化的影响 | 推荐动作 |
|---------|-----------|----------------|---------|
| 2026-05 | AI Agent成为ClawHub下载量最大品类 | 标题含"AI Agent"可提升30%+曝光 | 含AI Agent关键词的技能优先更新 |
| 2026-05 | MCP (Model Context Protocol) 生态爆发 | MCP相关技能搜索量周增300% | 技能description加入MCP关键词 |
| 2026-05 | OpenClaw v2026.3.22发布，700+技能可装 | 技能生态繁荣，竞争加剧 | 差异化描述+社媒推广成刚需 |
| 2026-04 | 视频内容(小红书/抖音/B站)成技能推广主战场 | 带视频演示的技能点赞量高5倍 | 技能增加AI视频脚本+缩略图提示词 |
| 2026-04 | 中国市场(DeepSeek/通义/Kimi)热度高涨 | 中文技能SEO权重提升 | 中文description前30字含核心关键词 |
| 2026-03 | Long Context RAG (100K-2M token) 成热点 | 长文档分析类技能需求爆发 | 精算/财报/法律类技能description强化RAG |
| 2026-03 | 银行保险监管合规类技能需求稳定增长 | 合规类技能长尾流量稳定 | 合规类技能持续更新法规版本 |

---

## Core Capabilities / 核心能力

### 1. User Review & Feedback Analysis Engine
/ 用户评论与反馈分析引擎

Analyze user reviews, feedback, and usage data to extract actionable improvement suggestions.

**Analysis Dimensions:**

| Dimension | What It Detects | Action |
|-----------|----------------|--------|
| **Feature Requests** | Users asking for capabilities the skill lacks | Add missing modules to SKILL.md |
| **Pain Points** | Frustration or confusion signals in reviews | Simplify instructions, add examples |
| **Competitor Mentions** | Users comparing to other tools | Add differentiation points |
| **Localization Gaps** | Non-Chinese users struggling (language barriers) | Add English README + bilingual docs |
| **Pricing/Access Issues** | Access friction, download barriers | Optimize onboarding flow |
| **Emotional Signals** | Excitement/disappointment in wording | Prioritize highly-praised features |
| **Video/Social Requests** | "能不能出个视频教程" / "想要小红书推广" | Add video script + thumbnail prompts |
| **MCP/Integration Gaps** | "能否对接XX工具" / "支持MCP吗" | Add MCP integration section |
| **Long Context Needs** | "处理长文档时卡住" / "支持XX万字吗" | Add context window optimization |

**Review Analysis Code:**

```python
import re
from collections import Counter

def analyze_reviews(reviews: list[str]) -> dict:
    """
    Analyze user reviews and extract actionable insights.
    reviews: list of review texts
    Returns: dict with categorized insights
    """
    positive_keywords = [
        "great", "amazing", "love", "perfect", "useful", "helpful",
        "强大", "好用", "实用", "完美", "赞", "棒", "优秀"
    ]
    negative_keywords = [
        "confusing", "broken", "bug", "missing", "wrong",
        "复杂", "难用", "没用", "问题", "错误", "缺东西"
    ]
    feature_request_patterns = [
        r"wish.*could", r"would be nice", r"should have",
        r"建议", r"希望有", r"能否加入", r"期待"
    ]

    results = {
        "positive_signals": [],
        "negative_signals": [],
        "feature_requests": [],
        "keywords": Counter()
    }

    for review in reviews:
        text_lower = review.lower()
        # Detect sentiment signals
        for kw in positive_keywords:
            if kw in text_lower:
                results["positive_signals"].append(review)
                break
        for kw in negative_keywords:
            if kw in text_lower:
                results["negative_signals"].append(review)
                break
        # Detect feature requests
        for pattern in feature_request_patterns:
            if re.search(pattern, text_lower):
                results["feature_requests"].append(review)
                break
        # Word frequency (simple tokenizer)
        words = re.findall(r'\b\w{3,}\b', text_lower)
        results["keywords"].update(w for w in words if len(w) > 3)

    return results
```

**Output Format:**

```markdown
## Review Analysis Report

### 🔥 Top 5 Praised Features
1. [Feature] — mentioned X times
2. ...

### 💡 Top 5 Feature Requests
1. [Request] — mentioned X times → Priority: HIGH/MEDIUM/LOW
2. ...

### ⚠️ Top 5 Pain Points
1. [Pain point] — urgency: CRITICAL/HIGH/MEDIUM
2. ...

### 📊 Keyword Frequency (Top 20)
| Keyword | Count | Sentiment |
|---------|-------|-----------|
| XXX     | 123   | Positive  |
| ...     | ...   | ...       |

### 🎯 Recommended Actions
1. **[HIGH]** Add [missing feature] to address [request]
2. **[MEDIUM]** Simplify [confusing part] based on [pain point]
3. **[LOW]** Add [example/tutorial] to reduce confusion
```

---

### 2. Trending Topic Tracker
/ 全网热点追踪引擎

Monitor trending topics across 40+ platforms to identify hot keywords that can boost skill visibility.

**Supported Data Sources:**

| Source | API/Endpoint | Data | Use Case |
|--------|-------------|------|----------|
| Weibo Hot Search | `uapis.cn` | Real-time热搜 | China trending |
| Zhihu Hot | `uapis.cn` | 知乎热榜 | Tech discussions |
| Bilibili Trending | `uapis.cn` | B站热搜 | Youth/tech audience |
| GitHub Trending | `github.com/trending` | GitHub热门 | Developer tools |
| WeChat Index | Tencent API | 微信指数 | China ecosystem |
| Baidu Index | `index.baidu.com` | 百度指数 | Search trends |
| Google Trends | `trends.google.com` | Global trends | International |
| Product Hunt | `producthunt.com` | PH热榜 | Global startup tools |

**Trending Data Fetching Code:**

```python
import requests
import json

def fetch_weibo_trending(limit: int = 20) -> list[dict]:
    """Fetch real-time Weibo hot search topics."""
    url = "https://uapis.cn/api/hotboard"
    params = {"type": "weibo", "limit": limit}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        return [
            {"rank": i+1, "title": item.get("title", ""),
             "hot": item.get("hot", ""), "url": item.get("url", "")}
            for i, item in enumerate(data.get("data", [])[:limit])
        ]
    except Exception as e:
        return [{"error": str(e)}]

def fetch_github_trending(lang: str = "python", limit: int = 10) -> list[dict]:
    """Fetch GitHub trending repositories."""
    url = f"https://api.github.com/search/repositories"
    params = {
        "q": f"language:{lang}+created:>2025-01-01",
        "sort": "stars", "order": "desc", "per_page": limit
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        return [
            {"name": item["name"], "stars": item["stargazers_count"],
             "description": item["description"], "url": item["html_url"]}
            for item in data.get("items", [])[:limit]
        ]
    except Exception as e:
        return [{"error": str(e)}]

def google_trends_suggestions(keyword: str) -> list[str]:
    """Get related queries from Google Trends."""
    # Using pytrends library
    from pytrends.request import TrendReq
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='')
    related = pytrends.related_queries()
    suggestions = []
    for kw_list in related.values():
        for item in kw_list.get('top', []) if kw_list else []:
            suggestions.append(item['query'])
    return suggestions[:10]
```

**Trending Keyword Mapping for Skills:**

```python
TRENDING_MAPPING = {
    # 2026 AI/LLM trends → skill keyword suggestions
    "DeepSeek": ["DeepSeek", "LLM", "AI agent", "Chinese AI", "open-source LLM"],
    "AI Agent": ["AI Agent", "workflow automation", "autonomous AI", "MCP"],
    "Claude": ["Claude", "Anthropic", "context window", "reasoning", "long context"],
    "MCP": ["MCP", "Model Context Protocol", "tool integration", "AI agent tools"],
    "Stock Market": ["A-share", "quantitative trading", "technical analysis", "缠论", "量化"],
    "Insurance": ["insurance tech", "insurtech", "risk management", "C-ROSS", "NFRA"],
    "Content Creation": ["AI video", "short video", "social media AI", "video SEO", "thumbnail"],
    "Productivity": ["workflow automation", "efficiency", "productivity tools", "RAG", "long context"],
    "Compliance": ["bank compliance", "NFRA", "Basel III", "AML", "PIPL", "regulatory"],
    "Actuarial": ["actuarial pricing", "C-ROSS II", "IFRS 17", "HKFRS 17", "life table 2025"],
}

def map_trending_to_skill(trending_topics: list[str], skill_tags: list[str]) -> list[dict]:
    """Map trending topics to skill tags for SEO boost."""
    suggestions = []
    for topic in trending_topics:
        for trend, keywords in TRENDING_MAPPING.items():
            if trend.lower() in topic.lower():
                for kw in keywords:
                    if kw not in skill_tags:
                        suggestions.append({
                            "trend": topic,
                            "suggested_tag": kw,
                            "priority": "HIGH" if len(suggestions) < 5 else "MEDIUM"
                        })
    return suggestions[:10]
```

---

### 3. SEO Title & Description Optimizer
/ SEO标题与描述优化器

Rewrite skill titles and descriptions using proven SEO frameworks to maximize search visibility and click-through rate.

**Title Optimization Framework:**

| Principle | English Example | Chinese Example |
|-----------|----------------|----------------|
| **Front-load value** | "AI Insurance Claims Analyzer" | "保险理赔AI专家" |
| **Include keyword** | "Stock Technical Analysis" | "A股技术分析" |
| **Show outcome** | "Increase Downloads 10x" | "提升下载量" |
| **Use numbers** | "5-Step Process" | "7大核心能力" |
| **Be specific** | "China Insurance C-ROSS Actuarial" | "偿二代精算定价" |
| **Evoke emotion** | "Stop Losing Money" | "告别选号盲目" |

**Description Structure (AIDA Framework):**

```
A - Attention:    [Bold hook: "The ONLY ClawHub skill that..."]
I - Interest:     [Specific problem + your unique solution]
D - Desire:       [Concrete results: "Used by 500+ analysts"]
A - Action:       [Clear CTA: "Install now and..."]
```

**Title Rewrite Examples:**

| Original (Chinese) | Optimized (English) | Optimized (Chinese) | Stars Impact |
|--------------------|--------------------|--------------------|--------------|
| 招投标文书助手 | Enterprise Bid Document AI | 企业招投标文书AI助手 | ⭐⭐⭐ |
| 保险反欺诈 | Insurance Anti-Fraud Pro | 保险反欺诈分析专家 | ⭐⭐⭐⭐ |
| 缠论技术分析 | Chanlun Technical Analysis Engine | 缠论技术分析引擎 | ⭐⭐⭐⭐ |
| 彩票预测 | Lottery Data Analysis & Number Generator | 彩票数据分析选号助手 | ⭐⭐ |

**Tag Optimization:**

```python
def optimize_tags(current_tags: list[str], trending_keywords: list[str],
                  competitors: list[str]) -> dict:
    """
    Optimize skill tags for maximum discoverability.
    """
    must_have = ["clawhub", "skill", "ai-agent"]  # Always include
    high_value = ["python", "api", "automation", "analysis", "tool"]
    trending = [kw for kw in trending_keywords if kw not in current_tags][:5]
    competitor_tags = [t for t in competitors if t not in current_tags][:3]

    optimized = must_have + high_value + trending + competitor_tags
    optimized = list(dict.fromkeys(optimized))[:20]  # Dedupe, max 20

    return {
        "current_tags": current_tags,
        "recommended_tags": optimized,
        "new_tags_added": [t for t in optimized if t not in current_tags],
        "tags_removed": [t for t in current_tags if t not in optimized],
        "seo_score_improvement": f"+{len([t for t in optimized if t not in current_tags]) * 5}%",
    }
```

---

### 4. Video Thumbnail & AI Preview Generation
/ AI视频缩略图生成与预览优化

Generate compelling skill preview visuals and AI video scripts for social media promotion.

**Thumbnail Prompt Framework:**

| Platform | Thumbnail Style | Prompt Template |
|----------|---------------|----------------|
| 小红书 | 高对比度大字+真人/产品图 | "Bold Chinese text 'XX', close-up screenshot of [UI], gradient background #hex, 3:4 ratio" |
| 抖音 | 强冲击+情绪化画面 | "Explosion effect, bold text 'XX', dramatic lighting, 9:16 vertical, trending color palette" |
| B站 | 知识感+人物出镜 | "Clean desk setup, person pointing at screen, code editor visible, warm lighting, 16:9" |
| 微信 | 简约商务风 | "Minimal flat design, skill icon centered, subtle gradient, 2:1 ratio, Chinese + English title" |

**AI Thumbnail Generation Code:**

```python
from openai import OpenAI
import json

def generate_thumbnail_prompt(skill_name: str, target_platform: str,
                               highlight: str, style: str = "modern") -> str:
    """Generate optimized thumbnail prompt for skill promotion."""
    platform_configs = {
        "小红书": {"ratio": "3:4", "color": "vibrant coral + white", "text_pos": "top-center"},
        "抖音": {"ratio": "9:16", "color": "neon purple + cyan", "text_pos": "center"},
        "B站": {"ratio": "16:9", "color": "dark blue + gold", "text_pos": "bottom-left"},
        "微信": {"ratio": "2:1", "color": "minimal white + blue", "text_pos": "center-bottom"}
    }
    cfg = platform_configs.get(target_platform, platform_configs["小红书"])

    return (
        f"Professional skill preview thumbnail for '{skill_name}', "
        f"highlight: {highlight}. Style: {style}. "
        f"Aspect ratio {cfg['ratio']}, color scheme {cfg['color']}. "
        f"Large bold text '{skill_name}' at {cfg['text_pos']}. "
        f"Clean, modern, high contrast, suitable for {target_platform}."
    )

def generate_video_script(skill_name: str, skill_slug: clawhub-skill-optimizer
                          duration_sec: int = 60) -> dict:
    """
    Generate 1-minute video script with 4 acts (15s each).
    Returns dict with act breakdown and AI image prompts.
    """
    return {
        "title": f"【技能推荐】{skill_name} — 3分钟上手指南",
        "duration": f"{duration_sec}秒",
        "hook": f"XX秒就能搞定的{skill_name}技能，效率提升10倍！",
        "acts": [
            {"act": 1, "seconds": "0-15s",
             "scene": "Hook — 痛点场景",
             "narration": f"还在为XX问题头疼？{skill_name}帮你一键解决！",
             "visual_prompt": f"Stressed person at desk, messy data, red alerts, warm lighting, cinematic"},
            {"act": 2, "seconds": "15-30s",
             "scene": "Demo — 技能展示",
             "narration": "看，这是它的核心功能，我只需要输入XX，就能得到XX。",
             "visual_prompt": f"Screen recording UI of {skill_name}, clean interface, smooth animation, cursor clicking"},
            {"act": 3, "seconds": "30-45s",
             "scene": "Result — 效果对比",
             "narration": "对比一下：原来要XX分钟，现在只要XX秒，效率提升太明显了！",
             "visual_prompt": f"Split screen: left messy slow process, right clean fast result, dramatic contrast lighting"},
            {"act": 4, "seconds": "45-60s",
             "scene": "CTA — 行动号召",
             "narration": f"安装命令：npx clawhub install @yourname/{skill_slug}，马上试试！",
             "visual_prompt": f"Large text overlay '{skill_name}', install command shown, QR code, clean blue gradient"}
        ]
    }
```

**Video Script Template (Markdown):**

```markdown
## 🎬 {Skill Name} 视频推广脚本 ({duration}秒)

### Act 1: 钩子 (0-{d1}s)
- **画面**: [visual_prompt]
- **配音**: {hook_narration}
- **字幕**: [大字突出痛点关键词]

### Act 2: 演示 ({d1}-{d2}s)
- **画面**: [screen recording showing skill in action]
- **配音**: [step-by-step usage walkthrough]
- **字幕**: [关键操作步骤]

### Act 3: 效果 ({d2}-{d3}s)
- **画面**: Before/After comparison, data visualization
- **配音**: [quantified improvement]
- **字幕**: [数字: 效率提升XX倍/节省XX时间]

### Act 4: 行动号召 ({d3}-{duration}s)
- **画面**: Install command + QR code
- **配音**: [enthusiastic CTA]
- **字幕**: npx clawhub install @yourname/{slug}
```

---

### 4b. Cross-Platform Social Syndication Strategy
/ 跨平台社交媒体推广策略

Design multi-platform promotion campaigns for maximum reach.

**Platform-Specific SEO Matrix:**

| Platform | Title Style | Description Length | Keyword Density | CTA Format |
|----------|-------------|-------------------|-----------------|------------|
| 小红书 | 中文感叹句，含数字 | 300-500字 | 高 | 评论区置顶安装命令 |
| 抖音 | 悬念式/对比式 | 视频字幕为主 | 中 | 评论区引导 |
| B站 | 知识干货型 | 800-2000字 | 低 | 简介区链接 |
| 知乎 | 深度分析型 | 1000-3000字 | 低 | 专栏文章链接 |
| 微信公众号 | 商务正式型 | 500-1000字 | 中 | 文末二维码 |

**Social Proof Framework:**

```python
SOCIAL_PROOF_TYPES = {
    "download_count": {"format": "🔥 X万次安装", "impact": "HIGH"},
    "star_count": {"format": "⭐ X千Star", "impact": "HIGH"},
    "user_testimonial": {"format": "用户说：'...'", "impact": "VERY_HIGH"},
    "media_mention": {"format": "被XX媒体报道", "impact": "MEDIUM"},
    "award_badge": {"format": "🏆 ClawHub热门技能", "impact": "MEDIUM"},
    "update_freshness": {"format": "✅ 今日更新", "impact": "HIGH"},
}

def build_social_proof_badge(skill_data: dict) -> str:
    """Build multi-element social proof string."""
    badges = []
    if skill_data.get("downloads", 0) > 1000:
        badges.append(f"🔥 {skill_data['downloads']//1000}万+安装")
    if skill_data.get("stars", 0) > 100:
        badges.append(f"⭐ {skill_data['stars']//1000}千Star")
    if skill_data.get("last_updated_days", 99) < 7:
        badges.append("✅ 近期更新")
    if skill_data.get("is_top_rated"):
        badges.append("🏆 热门推荐")
    return " | ".join(badges) if badges else ""
```

**A/B Testing Framework for Titles:**

```python
def generate_title_variants(original: str, skill_domain: str) -> list[dict]:
    """Generate 3-5 title variants for A/B testing."""
    templates = {
        "insurance": [
            f"【保险人必装】{original} — 效率提升10倍",
            f"保险{original}专家版：XX分钟搞定XX",
            f"不想加班？{original}让保险工作自动化",
        ],
        "bank": [
            f"银行人专属{original}，合规效率双提升",
            f"【合规必备】{original} — 银保监合规利器",
        ],
        "trading": [
            f"{original}：XX个指标一键分析，炒股不迷茫",
            f"看盘神器！{original}让技术分析零门槛",
        ],
        "default": [
            f"【AI工具】{original} — 3分钟上手教程",
            f"{original}：提升效率XX倍的秘密武器",
        ]
    }
    variants = templates.get(skill_domain, templates["default"])
    return [{"variant": v, "approach": t} for v, t in zip(variants, [
        "数字+感叹词", "领域专属词", "痛点引导"
    ][:len(variants)])]
```

---

### 5. GitHub-Style Stars Growth Strategy
/ GitHub式Star增长策略

Apply proven open-source project growth tactics to ClawHub skills.

**Strategy Framework:**

| Strategy | Implementation | Expected Impact |
|----------|---------------|----------------|
| **README Quality** | First 5 lines = summary. Clear "What/Why/How". Screenshots. | ⭐⭐⭐⭐ |
| **Keyword SEO** | Title + first 2 lines contain main keywords. README H1-H3 structure. | ⭐⭐⭐⭐⭐ |
| **Demo/Preview** | Short video or GIF showing the skill in action | ⭐⭐⭐⭐ |
| **Cross-posting** | Share on Zhihu, Weibo, Bilibili with skill link | ⭐⭐⭐ |
| **Community Building** | Create WeChat group / QQ group for skill users | ⭐⭐⭐ |
| **Regular Updates** | Version updates with changelog. "Updated 2 days ago" signal. | ⭐⭐⭐⭐ |
| **Comparison Content** | "vs [competitor]" articles to attract their users | ⭐⭐⭐ |
| **Trending Integration** | Tie skill to current hot topics (AI agents, DeepSeek, etc.) | ⭐⭐⭐⭐⭐ |
| **Multi-language** | English README = global audience 10x | ⭐⭐⭐⭐⭐ |

**README Bilingual Template:**

```markdown
# [English Title] / [中文标题]

<!-- English (for international users - put FIRST) -->
> **English Description**: One powerful sentence describing the skill's core value.
> Built for [target user]. Solves [specific problem].

## ✨ Features / Features / 核心功能

- ✅ Feature 1 with specific metric or result
- ✅ Feature 2 — [why it matters]
- ✅ Feature 3

## 🚀 Quick Start

```bash
# Install
npx clawhub install @yourname/your-skill

# Use
/your-skill [command]
```

## 📖 Documentation

Full docs at [link] or continue reading below.

---

<!-- 中文部分（放在英文后面，供国内用户阅读） -->
> **中文介绍**：一句话描述技能核心价值。针对[目标用户]，解决[具体问题]。

## 🎯 核心功能

- ✅ 功能1 — [具体效果/数据]
- ✅ 功能2 — [为什么有用]
- ✅ 功能3

## ⚡ 快速上手

1. 安装：`npx clawhub install @yourname/your-skill`
2. 使用：`/your-skill [命令]`
3. 查看文档见下方

## 📚 详细文档

[详细内容...]
```

---

### 5. GitHub-Style Stars Growth Strategy

> **⚠️ 操作提示**：以下策略为**人工操作建议**，需用户自行判断并手动执行。本技能**不会自动修改**任何技能元数据、不会自动在社交媒体发帖、不会自动调用任何外部API。每项操作前请自行评估合规性和平台规则。

/ GitHub式Star增长策略（更新：2026视频+社媒推广）

Apply proven open-source project growth tactics to ClawHub skills.

**Strategy Framework (2026 Updated):**

| Strategy | 2026 Implementation | Expected Impact |
|----------|-------------------|----------------|
| **README Quality** | First 5 lines = summary. Clear "What/Why/How". Screenshots. | ⭐⭐⭐⭐ |
| **Keyword SEO** | Title + first 2 lines contain main keywords. README H1-H3 structure. | ⭐⭐⭐⭐⭐ |
| **Demo Video** | Short video or GIF showing the skill in action (小红书/抖音/B站) | ⭐⭐⭐⭐⭐ |
| **Video Thumbnail** | AI-generated preview thumbnail with bold text + high contrast | ⭐⭐⭐⭐ |
| **Cross-posting** | Share on 知乎/微博/小红书/B站 with skill link | ⭐⭐⭐ |
| **Community Building** | Create WeChat group / QQ group for skill users | ⭐⭐⭐ |
| **Regular Updates** | Version updates with changelog. "Updated 2 days ago" signal. | ⭐⭐⭐⭐ |
| **Comparison Content** | "vs [competitor]" articles to attract their users | ⭐⭐⭐ |
| **Trending Integration** | Tie skill to current hot topics (AI agents, DeepSeek, MCP, etc.) | ⭐⭐⭐⭐⭐ |
| **Multi-language** | English README = global audience 10x | ⭐⭐⭐⭐⭐ |
| **Social Proof Badge** | Downloads + stars count displayed in title | ⭐⭐⭐⭐ |

---

### 6. Full Skill Optimization Report
/ 全流程技能优化报告

Generate a complete optimization report combining all analysis:

```markdown
# 🎯 ClawHub Skill Optimization Report
**Skill**: [skill-name]
**Generated**: [timestamp]
**Analyzer**: ClawHub Skill Growth Engine v2.0.0

---

## 📊 Current Status

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Downloads | XXX | 1,000+ | +XXX |
| Stars | XX | 100+ | +XX |
| Description Length | XXX chars | 200-300 | OK |
| Tags Count | X | 10-15 | Add X |
| Has English README | No | Yes | MISSING |
| Last Updated | YYYY-MM-DD | < 30 days | STALE |

---

## 🔥 Trending Keywords to Integrate

| # | Trending Topic | Relevant Tag | Priority | Integration |
|---|---------------|-------------|---------|-------------|
| 1 | [topic] | [tag] | HIGH | Add to description |
| 2 | [topic] | [tag] | MEDIUM | Add to tags |
| ... | ... | ... | ... | ... |

---

## 📝 Title & Description Rewrite

### Current
**Title**: [old title]
**Description**: [old description]

### Optimized
**Title (EN)**: [optimized English title]
**Title (CN)**: [optimized Chinese title]
**Description (EN)**:
> [SEO-optimized English description - AIDA framework]

**Description (CN)**:
> [优化后的中文描述]

### Tags Optimization
**Current**: [tag1, tag2, ...]
**Add**: [new tags]
**Remove**: [obsolete tags]

---

## 💬 Review Analysis Findings

### Top Requests from Users
1. [Request 1] → Add to SKILL.md priority section
2. [Request 2] → Add FAQ section
3. [Request 3] → Create tutorial

### Pain Points to Fix
1. [Pain point 1] → Rewrite confusing section
2. [Pain point 2] → Add troubleshooting guide

---

## 📋 Action Plan (Priority Order)

| # | Action | Type | Impact | Effort |
|---|--------|------|--------|--------|
| 1 | Add English README | Content | ⭐⭐⭐⭐⭐ | Low |
| 2 | Rewrite title with trending keyword | SEO | ⭐⭐⭐⭐⭐ | Low |
| 3 | Add missing feature from reviews | Feature | ⭐⭐⭐⭐ | Medium |
| 4 | Cross-post on [platform] | Promotion | ⭐⭐⭐⭐ | High |
| ... | ... | ... | ... | ... |

---

## ✅ Checklist for Publishing (v2.0)

- [ ] Title contains main keyword + 2026 trending keyword (AI Agent/MCP/etc.)
- [ ] Description is 200-300 characters (English), first 30 chars include core keyword (Chinese)
- [ ] Tags include trending + evergreen keywords (AI Agent, MCP, workflow automation, etc.)
- [ ] English README added (English FIRST, Chinese SECOND)
- [ ] Video thumbnail prompt generated for each target platform
- [ ] 60-second video script completed (if promoting on social media)
- [ ] Cross-platform social post plan drafted (小红书/抖音/B站/知乎)
- [ ] Social proof badges added (download count, stars, recent update)
- [ ] Changelog updated with v2.0 changes
- [ ] Version bumped to X.X.X
- [ ] All reference files checked for broken links
- [ ] Bilingual trigger keywords in SKILL.md
```

---

## Workflow / 工作流程

```
User Input: Current skill details / user reviews / trending goal
    ↓
[Step 1] Analyze Reviews → Extract pain points + requests
[Step 2] Fetch Trending Data → Map to skill keywords (AI Agent/MCP/video SEO)
[Step 3] SEO Rewrite → Title + description + tags + 2026 trending keywords
[Step 4] Generate Video Assets → Thumbnail prompt + 60s video script
[Step 5] Cross-Platform Plan → Platform-specific SEO + social syndication
[Step 6] GitHub Stars Strategy → README + promotion plan + social proof
[Step 7] Generate Full Report → Actionable checklist
    ↓
User confirms changes
    ↓
Apply: Update SKILL.md + README.md + tags + thumbnail prompts + changelog
```

---

## Reference Files

| File | Content |
|------|---------|
| `references/seo_optimization_guide.md` | Full SEO framework + keyword research methods + 2026 trending |
| `references/trending_topic_tracker.md` | Trending APIs + code + keyword mapping (updated with MCP/video SEO) |
| `references/review_analysis_templates.md` | Review analysis templates + sentiment scoring |
| `references/video_seo_guide.md` | Video thumbnail prompts + platform-specific SEO + 60s script templates |
