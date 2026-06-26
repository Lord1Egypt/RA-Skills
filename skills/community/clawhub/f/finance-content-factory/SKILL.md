---
name: Financial Content Factory
slug: finance-content-factory
description: AI-powered financial content factory — covers content planning, article writing, social media posts, video scripts, and multi-format content generation for financial marketing. Built for financial marketing teams. Keywords: content marketing, article writing, social media, video scripts, financial marketing, 内容工厂, 内容营销, 文章写作, 社媒内容, 视频脚本, 内容创作, 金融文案, 小红书文案, 抖音脚本, 公众号文章.
version: "3.0.1"
---

# Financial Content Factory / 金融内容工厂

> **English:** AI-powered content factory — covers articles, social media, video scripts.
>
> **中文:** 内容工厂——覆盖文章、社媒、直播脚本。

---


### 金融监管最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| 金融监管 | 2026年Q1：金融内容合规要求提升 | 内容模板库需增加合规标签和风险提示模块 |
| 金融监管 | 营销内容需满足消费者保护和合规留存要求 | 内容模板库需增加合规标签和风险提示模块 |
| 金融监管 | 产品分级告知和风险提示需纳入内容模板 | 内容模板库需增加合规标签和风险提示模块 |

> **数据截止**: 2026-05-25 | 来源：证监会、NFRA、中证协、安永Q1分析
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **内容产出慢** | 营销内容需求大，团队小 | AI批量生成 |
| **质量不稳定** | 兼职写作水平参差 | 质量标准化 |
| **合规风险** | 金融内容监管严 | 合规检查 |
| **形式单一** | 只有图文 | 多格式覆盖 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** content marketing, article writing, social media, video scripts, financial marketing

**中文触发词（优先）：** 内容创作 / 内容工厂 / 文章写作 / 社媒内容 / 视频脚本 / 营销文案 / 金融科普 / 内容规划

---

## Core Capabilities / 核心能力

### 1. Content Templates / 内容模板

```python
CONTENT_TEMPLATES = {
    "产品种草文": {
        "结构": "痛点引入 → 产品介绍 → 核心卖点 → 案例/数据 → CTA",
        "合规要点": ["风险提示", "收益说明", "产品条款链接"]
    },
    "科普文章": {
        "结构": "热门话题 → 概念解释 → 深度分析 → 实用建议",
        "长度": "1500-2000字"
    },
    "社媒短文": {
        "微博": "观点 + 数据/案例 + 互动引导（150字）",
        "小红书": "标题 + 干货 + 种草（500字+图）",
        "抖音": "3秒开场 + 干货 + 互动（60秒内）"
    }
}
```

### 2. Content Calendar / 内容日历

```python
CONTENT_CALENDAR = {
    "banking": {
        "周频率": 5,
        "内容类型分布": {
            "产品推广": "20%",
            "知识科普": "40%",
            "活动宣传": "20%",
            "品牌故事": "20%"
        }
    },
    "insurance": {
        "周频率": 7,
        "内容类型分布": {
            "保障科普": "30%",
            "产品介绍": "20%",
            "案例分享": "20%",
            "热点借势": "15%",
            "团队/品牌": "15%"
        }
    }
}
```

---

## Disclaimer

This skill provides content creation tools for educational purposes.
