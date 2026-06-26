# SEO Optimization Guide for ClawHub Skills
# ClawHub Skill SEO优化完全指南

## Overview / 概述

SEO for ClawHub skills follows similar principles to GitHub README SEO and app store optimization (ASO). The goal is to make your skill **discoverable** through search and **clickable** when seen.

## 1. Title Optimization / 标题优化

### English Title Principles

| Principle | ✅ Good | ❌ Bad |
|-----------|--------|-------|
| Front-load value | "Insurance Claims AI Analyzer" | "A Tool for Analyzing Insurance Claims with AI" |
| Include keyword | "Stock Technical Analysis Pro" | "The Ultimate Analysis Tool" |
| Be specific | "China C-ROSS Actuarial Calculator" | "Financial Calculator" |
| Use numbers | "10-Step Bid Writing System" | "Complete Bid Writing Guide" |
| Action-oriented | "Predict Lottery Numbers with AI" | "Lottery Prediction Tool" |

### Title Length: 4-7 words (English) / 4-10 characters (Chinese)

### A/B Testing Titles:

```
Variant A: "DeepSeek Insurance Actuarial Expert"
Variant B: "China Actuarial Tool — C-ROSS & Life Table 2025"
Variant C: "Professional Insurance Actuarial Calculator for China"
→ Pick based on CTR data after 1 week
```

## 2. Description Optimization / 描述优化

### Length: 200-300 characters (English) / 100-200 characters (Chinese)

### Structure: AIDA Framework

```
A (Attention):    Bold hook — "The ONLY skill that..."
I (Interest):    Problem + solution — "Wrote 50 bid docs in 1 hour"
D (Desire):      Results — "Used by 300+ insurance analysts"
A (Action):      CTA — "Install and start now"
```

### Description Checklist:

```markdown
✅ Contains primary keyword in first 50 characters
✅ Second sentence answers "who is this for"
✅ Third sentence gives concrete result/proof
✅ Ends with action-oriented phrase
✅ Avoids jargon that non-experts can't understand
✅ No emojis in English (unless appropriate)
✅ Chinese description: shorter, use Chinese punctuation
```

### Examples:

**Insurance Claims (English):**
> "AI-powered insurance claims processing skill — analyzes medical receipts via OCR, detects fraud with graph neural networks, and auto-generates claim decisions. Built for Chinese insurance companies. Reduces claim processing time by 93%. Install now."

**Insurance Claims (中文):**
> "保险理赔AI专家——多模态票据识别+智能判责+反欺诈图谱，覆盖医疗险/重疾险/车险/财产险全险种，理赔审核效率提升93%。适用：保险公司理赔部、风控合规、个险代理人。"

## 3. Tag Optimization / 标签优化

### Optimal Tag Count: 10-15 tags

### Tag Categories:

```
Must-Have Tags:
  ├── Platform: clawhub, skill, ai-agent, workbuddy
  ├── Domain: insurance, stock-market, lottery, finance
  └── Type: python, automation, analysis, api

Evergreen Tags (high search volume):
  ├── AI/ML: deepseek, llm, gpt, claude, ai-agent, automation
  ├── Business: insurance, finance, accounting, legal
  ├── Tools: python, api, data-analysis, visualization
  └── Markets: china, a-stock, crypto, forex

Trending Tags (check weekly):
  ├── "deepseek", "ai-agent", "webassembly"
  ├── "rpa", "workflow-automation", "low-code"
  └── "china-insurance", "cross", "solvency"

Localization Tags:
  ├── zh (Chinese content) + en (English content)
  ├── china, chinese-market (for China-focused skills)
  └── global, international (for globally-relevant skills)
```

### Tag Combination Formula:

```
[Must-Have × 3] + [Evergreen × 5] + [Trending × 3] + [Localization × 2] = 13 tags
```

## 4. README Optimization / README优化

### The 5-Second Rule:
A visitor decides to star or leave in 5 seconds. Structure accordingly:

```markdown
# [TITLE] — One line value proposition

> **English hook** (1 sentence)
> **中文简介** (1 sentence)

## ✨ Key Features (3-5 bullets, each with concrete result)

## 🚀 Quick Start (3 steps max)

## 📖 Full Documentation

[Rest of content...]
```

### GitHub README Best Practices (apply to ClawHub):

1. **Badges**: Add relevant badges (version, license, downloads)
2. **Visual hierarchy**: H1 = title, H2 = sections, H3 = subsections
3. **Code blocks**: Always provide working code examples
4. **Screenshots/GIFs**: If applicable, add demo visuals
5. **Changelog**: Show you're actively maintaining
6. **Contributing**: Invite collaboration
7. **License**: Add an open license

## 5. Bilingual Strategy / 双语策略

### Why Bilingual Matters:

| Segment | Chinese Users | International Users |
|---------|-------------|--------------------|
| Share of ClawHub | ~70% | ~30% |
| Global appeal | Low without EN | Essential for growth |
| SEO value | Baidu optimized | Google optimized |
| Stars potential | Local community | GitHub-style global |

### Implementation:

```markdown
# SKILL.md Structure (Bilingual)

---
name: English Skill Name        # English name for marketplace
description: English description # English for international search
version: 1.0.0
---

# English Title / English Skill Name

> **English hook** (1 line, SEO-optimized, <50 words)

## English content (main documentation)

---

## 中文部分 (放在英文后面)

> **中文简介**（1行，SEO优化，<100字）

## 中文内容（详细说明）
```

### SEO Keyword Mapping:

| English (for Google/GitHub) | Chinese (for Baidu) |
|-----------------------------|---------------------|
| insurance, actuarial, C-ROSS | 保险、精算、偿二代 |
| technical analysis, trading | 技术分析、炒股、走势 |
| AI agent, automation | AI助手、自动化、智能体 |
| lottery, prediction, numbers | 彩票、预测、选号 |
| claims, underwriting, fraud | 理赔、核保、反欺诈 |

## 6. Changelog Best Practices / 更新日志最佳实践

```markdown
## Changelog Format (Keep it short + meaningful):

### v1.1.0 — 2026-05-04
✨ Added: English README (international users)
✨ Added: SEO keywords from trending analysis
🐛 Fixed: Broken reference link in guide
📝 Updated: Title optimized for "AI Agent" trend

### v1.0.0 — 2026-05-01
🎉 Initial release
```

### Changelog Keywords That Attract Stars:
- "Added English support" — shows international care
- "Fixed [X] issues" — shows active maintenance
- "New tutorial" — shows helpfulness
- "Performance improved" — shows quality

## 7. Search Ranking Factors / 搜索排名因素

Based on GitHub SEO and ClawHub best practices:

| Factor | Weight | How to Optimize |
|--------|--------|----------------|
| **Title keyword match** | ⭐⭐⭐⭐⭐ | Main keyword in title |
| **Description keyword match** | ⭐⭐⭐⭐ | Primary keywords in first 100 chars |
| **Star count** | ⭐⭐⭐⭐ | Encourage starring, cross-post |
| **Download count** | ⭐⭐⭐⭐ | Share widely, SEO |
| **Recent updates** | ⭐⭐⭐ | Update every 1-2 weeks |
| **Tag relevance** | ⭐⭐⭐ | Use exact-match keywords |
| **Readme quality** | ⭐⭐⭐ | English README first |

## 8. Promotion Strategy / 推广策略

### Platform-Specific Tips:

| Platform | What to Post | How to Drive Stars |
|----------|-------------|-------------------|
| **Zhihu** | Tutorial article with skill link | End with "helpful? Star it!" |
| **Weibo** | Short demo + skill name | Engage comments, reply |
| **Bilibili** | Video demo (1-2 min) | Pin comment with install command |
| **WeChat** | Official account article | Add QR code to skill page |
| **GitHub** | Mirror/sibling repo | GitHub stars = credibility |
| **Twitter/X** | English demo thread | #AI #ChatGPT #ClawHub |
| **Reddit** | Useful tool posts | r/China, r/AI, r/quant |

### Growth Hacking Tactics:

```python
def star_growth_tactics():
    """Proven tactics to increase GitHub-style stars."""
    tactics = [
        ("Submit to Product Hunt", "Launch day boost — potential 100+ stars"),
        ("Post in ClawHub Discord/Slack", "Community feedback loop"),
        ("Create comparison article", "vs [Competitor] attracts their users"),
        ("Submit to alternative lists", "clawhub.gpters.dev, skillsbot.cn"),
        ("Create video tutorial", "Bilibili/YouTube — visual proof"),
        ("Guest post on tech blogs", "AI/工具类博客引流"),
        ("Add to awesome-clawhub list", "Community curation = passive discovery"),
        ("Reddit cross-post", "r/China_Investing, r/quant", "organic traffic"),
        ("Engage with user feedback", "Quick responses → 5-star reviews"),
        ("Regular updates", "Changelog = "alive" signal"),
    ]
    return tactics
```
