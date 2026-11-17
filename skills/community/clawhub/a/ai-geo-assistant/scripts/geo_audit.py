#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
geo_audit.py — GEO（生成式引擎优化）体检与优化流水线脚本

零第三方依赖，仅需 Python 3.8+ 标准库。

子命令：
  crawl    网站抓取（Stage 1）：整站 BFS 抓取，落盘 HTML + 清单
  analyze  全维度 GEO 分析（Stage 2-14）+ 评分（十维扣分制）
  plan     生成 GEO 优化方案（Stage 15）
  optimize 自动优化，产出可粘贴的 JSON-LD / FAQ / meta 片段（Stage 16）
  validate 对比基线报告验证优化效果（Stage 17）

评分口径：十维维度 + 扣分制（满分 100），Grade A/B/C/D/F，AI 可见度，GEO 六维评分。

所有输出 JSON 使用 ensure_ascii=False（保留中文）。
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from collections import Counter, defaultdict
from datetime import datetime
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; YunZhiGEO/1.0)"
DELAY_FLOOR = 2.0  # 相邻请求最小间隔（秒），避免对目标站造成压力

# ============================================================================
# 评分维度配置（十维，满分 100，扣分制）
# ============================================================================
DIMENSION_CONFIG = {
    "crawlability":    {"label": "Crawlability",            "label_cn": "可抓取性", "maxScore": 12},
    "metadata":        {"label": "Metadata",               "label_cn": "元数据/结构化", "maxScore": 12},
    "readability":     {"label": "Machine Readability",     "label_cn": "机器可读性", "maxScore": 12},
    "trust":           {"label": "Trust Signals",          "label_cn": "信任信号", "maxScore": 8},
    "freshness":       {"label": "Freshness",              "label_cn": "内容新鲜度", "maxScore": 8},
    "entity":          {"label": "Entity Clarity",         "label_cn": "实体清晰度", "maxScore": 10},
    "discoverability": {"label": "Internal Discoverability","label_cn": "站内可发现性", "maxScore": 8},
    "answerability":   {"label": "Answerability",          "label_cn": "可回答性", "maxScore": 12},
    "citation":        {"label": "Citation Readiness",      "label_cn": "可引用性", "maxScore": 8},
    "content":         {"label": "Content Quality",         "label_cn": "内容质量", "maxScore": 10},
}

# 规则文案（summary / whyItMatters / fixSuggestion / estimatedGain / example）
ISSUE_COPY = {
    "crawl.missing-canonical": {
        "summary": "The page is missing a canonical URL signal.",
        "whyItMatters": "Canonical tags help search systems and crawlers understand the preferred page URL.",
        "fixSuggestion": "Add a self-referencing canonical tag for indexable pages.",
        "example": '<link rel="canonical" href="https://example.com/current-page" />',
        "estimatedGain": "2-4 points",
    },
    "crawl.missing-lang": {
        "summary": "The document language is not declared on the root HTML element.",
        "whyItMatters": "Language hints help machines parse the page and choose the right localized interpretation.",
        "fixSuggestion": 'Add a language attribute such as <html lang="en">.',
        "example": '<html lang="en">',
        "estimatedGain": "1-2 points",
    },
    "crawl.noindex-directive": {
        "summary": "The page exposes a noindex directive.",
        "whyItMatters": "Noindex can prevent the page from being discovered or reused in search and AI retrieval flows.",
        "fixSuggestion": "Remove noindex from pages that should be discoverable.",
        "example": '<meta name="robots" content="index,follow" />',
        "estimatedGain": "3-5 points",
    },
    "meta.missing-description": {
        "summary": "The page does not include a meta description.",
        "whyItMatters": "Meta descriptions improve page summarization and discovery context.",
        "fixSuggestion": "Add a concise description that states the page topic and outcome.",
        "example": '<meta name="description" content="Learn how to improve AI citation readiness for your landing page." />',
        "estimatedGain": "2-3 points",
    },
    "discoverability.missing-internal-links": {
        "summary": "The page does not expose meaningful internal navigation paths.",
        "whyItMatters": "Internal links help crawlers and AI systems discover related context around the page topic.",
        "fixSuggestion": "Add links to related pages, docs, product details, or supporting resources.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "meta.missing-open-graph": {
        "summary": "The page is missing core Open Graph metadata.",
        "whyItMatters": "Open Graph fields strengthen page summarization and sharing context across systems.",
        "fixSuggestion": "Add at least og:title and og:description that align with the page topic.",
        "example": '<meta property="og:title" content="GEO Inspector Audit Guide" />',
        "estimatedGain": "1-3 points",
    },
    "meta.missing-schema": {
        "summary": "No schema.org structured data was detected.",
        "whyItMatters": "Structured data helps machines identify the page type, entity, and key content signals faster.",
        "fixSuggestion": "Add JSON-LD schema matching the page type, such as Organization, Article, Product, or FAQPage.",
        "example": '{ "@context": "https://schema.org", "@type": "Article", "headline": "..." }',
        "estimatedGain": "3-6 points",
    },
    "meta.missing-article-schema": {
        "summary": "This content page is missing Article-style structured data.",
        "whyItMatters": "Article schema helps machines interpret the page as editorial content with authorship and publication context.",
        "fixSuggestion": "Add Article or BlogPosting JSON-LD with headline, author, publish date, and updated date.",
        "example": '{ "@context": "https://schema.org", "@type": "Article", "headline": "GEO Audit Guide" }',
        "estimatedGain": "2-4 points",
    },
    "meta.missing-product-schema": {
        "summary": "This product or service page lacks Product or Service structured data.",
        "whyItMatters": "Structured product signals help AI systems understand what is being offered and how to describe it.",
        "fixSuggestion": "Add Product, Service, or SoftwareApplication schema depending on the page type.",
        "example": '{ "@context": "https://schema.org", "@type": "SoftwareApplication", "name": "..." }',
        "estimatedGain": "2-4 points",
    },
    "meta.missing-organization-schema": {
        "summary": "The page does not expose a clear brand or site-level schema signal.",
        "whyItMatters": "Organization and WebSite schema help AI systems connect content to a known entity.",
        "fixSuggestion": "Add Organization or WebSite JSON-LD with name, url, and sameAs links where relevant.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "meta.missing-docs-schema": {
        "summary": "The documentation page is missing schema that matches instructional content.",
        "whyItMatters": "HowTo, TechArticle, and FAQPage schema make docs easier for machines to classify and summarize.",
        "fixSuggestion": "Add HowTo, TechArticle, or FAQPage schema depending on the page intent.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "entity.missing-primary-entity": {
        "summary": "The page does not clearly identify the brand, company, or primary entity behind it.",
        "whyItMatters": "AI systems need a stable entity signal to connect the page to a recognizable source.",
        "fixSuggestion": "Expose the brand or organization more clearly using visible copy, Open Graph site name, and Organization or WebSite schema.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "entity.missing-content-owner": {
        "summary": "The page does not clearly identify who owns or publishes the content.",
        "whyItMatters": "Named owners help AI systems understand who stands behind the content.",
        "fixSuggestion": "Add an author, publisher, or organization signal in visible page content or structured data.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "entity.product-entity-ambiguous": {
        "summary": "The product page does not clearly tie the offer back to a known entity.",
        "whyItMatters": "Entity ambiguity makes it harder for AI systems to describe the offer with confidence.",
        "fixSuggestion": "Connect the product to a named brand, company, or publisher using visible labels and structured data.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "discoverability.weak-related-navigation": {
        "summary": "The page includes too few internal pathways to related content.",
        "whyItMatters": "Related-page pathways help AI systems understand where this page sits inside the site context.",
        "fixSuggestion": "Add links to adjacent docs, related articles, product detail pages, or next-step resources.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "readability.missing-h1": {
        "summary": "The page has no H1 heading.",
        "whyItMatters": "A strong H1 helps machines and users identify the page's main topic.",
        "fixSuggestion": "Add a single H1 that clearly states the page topic.",
        "example": "<h1>GEO Audit Checklist for AI Search Visibility</h1>",
        "estimatedGain": "2-3 points",
    },
    "readability.multiple-h1": {
        "summary": "The page uses multiple H1 headings.",
        "whyItMatters": "Too many H1 tags can blur the primary topic signal.",
        "fixSuggestion": "Keep one primary H1 and demote the rest to H2/H3 as needed.",
        "example": None,
        "estimatedGain": "1-2 points",
    },
    "readability.thin-headings": {
        "summary": "The page has weak heading structure.",
        "whyItMatters": "Subheadings make content easier for machines to segment, summarize, and quote.",
        "fixSuggestion": "Break the content into sections with clear H2/H3 headings.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "readability.long-paragraphs": {
        "summary": "Paragraph blocks are too long and dense.",
        "whyItMatters": "Long paragraphs reduce scanability and make it harder for machines to isolate useful answer units.",
        "fixSuggestion": "Split dense paragraphs into shorter units and add subheadings or bullets.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "readability.missing-structured-formatting": {
        "summary": "The page lacks lists, steps, or tables that structure the information.",
        "whyItMatters": "Structured formatting makes content easier to segment, extract, and quote.",
        "fixSuggestion": "Add checklists, bullet lists, steps, comparison tables, or short modules.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "readability.docs-missing-steps": {
        "summary": "The documentation page lacks a clear step-by-step structure.",
        "whyItMatters": "Instructional pages are easier to reuse when the task flow is explicit.",
        "fixSuggestion": "Break the guide into ordered steps or phases with short descriptions.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "readability.product-missing-comparison-structure": {
        "summary": "The product page does not help machines compare or frame the offer.",
        "whyItMatters": "Comparison blocks and feature tables improve how AI systems describe a product's positioning.",
        "fixSuggestion": "Add a feature matrix, comparison section, or clear differentiator list.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "trust.missing-authority-signals": {
        "summary": "The page lacks clear author, organization, or contact signals.",
        "whyItMatters": "Trust signals help AI systems attribute the content to a real source.",
        "fixSuggestion": "Expose author, brand, about, or contact information on the page.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "trust.missing-author": {
        "summary": "The page lacks clear author attribution.",
        "whyItMatters": "Named authors help AI systems assess source identity and editorial ownership.",
        "fixSuggestion": "Add an author name near the title or in schema markup.",
        "example": None,
        "estimatedGain": "2-3 points",
    },
    "freshness.missing-publish-date": {
        "summary": "The page does not expose a publish date.",
        "whyItMatters": "Publication dates help machines understand freshness and citation context.",
        "fixSuggestion": 'Display and mark up a publish date in HTML or schema.',
        "example": '<time datetime="2026-06-21">June 21, 2026</time>',
        "estimatedGain": "1-2 points",
    },
    "freshness.missing-modified-date": {
        "summary": "The page does not expose an updated date.",
        "whyItMatters": "Updated dates strengthen freshness signals for reference-style content.",
        "fixSuggestion": "Add a last updated timestamp where ongoing maintenance matters.",
        "example": None,
        "estimatedGain": "1-2 points",
    },
    "freshness.stale-reference-content": {
        "summary": "The page appears old relative to reference-style content expectations.",
        "whyItMatters": "Stale content is less likely to be trusted or quoted for time-sensitive guidance.",
        "fixSuggestion": "Review the page, refresh outdated claims, and update the visible modified date when content is maintained.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "citation.missing-source-links": {
        "summary": "The page does not reference external sources or supporting materials.",
        "whyItMatters": "Source links improve factual grounding and make the page safer for AI systems to cite.",
        "fixSuggestion": "Link to supporting data, primary documentation, or reputable references.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "citation.missing-citable-structure": {
        "summary": "The page lacks clean blocks that are easy to quote or cite.",
        "whyItMatters": "Definitions, FAQs, short quotes, and tables create reusable answer units for AI systems.",
        "fixSuggestion": "Add definition blocks, FAQs, short takeaway quotes, or summary tables that package key claims clearly.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "trust.homepage-missing-brand-paths": {
        "summary": "The homepage lacks clear About or Contact trust pathways.",
        "whyItMatters": "Brand trust signals help AI systems connect content to a real company or team.",
        "fixSuggestion": "Add visible About, Contact, Team, or Company links in the main nav or footer.",
        "example": None,
        "estimatedGain": "2-3 points",
    },
    "answerability.missing-definition": {
        "summary": "The page lacks clear definition or answer-style statements.",
        "whyItMatters": "AI systems are more likely to quote content that states the answer directly.",
        "fixSuggestion": "Add a short summary or definition paragraph near the top of the page.",
        "example": "Generative Engine Optimization (GEO) is the practice of structuring web content so AI systems can understand, summarize, and cite it accurately.",
        "estimatedGain": "3-5 points",
    },
    "answerability.landing-unclear-value-prop": {
        "summary": "The landing page does not state its offer clearly enough near the top.",
        "whyItMatters": "AI systems need a compact value statement to understand what the page is promising.",
        "fixSuggestion": "Add a direct value proposition that says what the product does, for whom, and why it matters.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "answerability.missing-summary-intro": {
        "summary": "The top of the page does not quickly summarize the main answer.",
        "whyItMatters": "A strong opening summary increases the chance that AI systems extract the correct takeaway.",
        "fixSuggestion": "Add a concise intro paragraph that directly explains the page topic and outcome.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "answerability.missing-structured-blocks": {
        "summary": "The page is missing FAQ, steps, comparison, or list-style answer blocks.",
        "whyItMatters": "Structured answer blocks are easier for AI systems to extract and rephrase accurately.",
        "fixSuggestion": "Add FAQs, step-by-step sections, checklists, or comparison tables.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "answerability.missing-faq": {
        "summary": "The page does not include a FAQ-style question block.",
        "whyItMatters": "FAQ sections create explicit answer candidates for question-based AI retrieval.",
        "fixSuggestion": "Add a short FAQ section covering common user questions about the topic.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "answerability.missing-quotable-snippets": {
        "summary": "The page lacks short statements that can be quoted cleanly.",
        "whyItMatters": "AI systems often favor compact, direct statements when generating answers.",
        "fixSuggestion": "Add concise definitions, key claims, or takeaway statements in standalone sentences.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "answerability.product-missing-buyer-qa": {
        "summary": "The product page does not address buyer-style questions directly.",
        "whyItMatters": "Buyer Q&A cues help AI systems answer commercial and comparison queries more accurately.",
        "fixSuggestion": "Add FAQs, objections, fit criteria, or use-case comparisons for prospective buyers.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "answerability.docs-missing-task-guidance": {
        "summary": "The documentation page does not guide the user through a concrete task.",
        "whyItMatters": "Task-oriented guidance makes docs more reusable in answer engines and coding assistants.",
        "fixSuggestion": "Add steps, prerequisites, expected outcomes, or troubleshooting guidance.",
        "example": None,
        "estimatedGain": "2-4 points",
    },
    "content.thin-content": {
        "summary": "The page content is too thin for strong machine understanding.",
        "whyItMatters": "Thin pages usually offer too little context for robust summaries or citations.",
        "fixSuggestion": "Expand the page with clearer explanation, examples, and supporting detail.",
        "example": None,
        "estimatedGain": "3-5 points",
    },
    "content.light-depth": {
        "summary": "The page has some substance, but still lacks enough supporting depth.",
        "whyItMatters": "Shallow coverage limits how confidently machines can summarize and compare the content.",
        "fixSuggestion": "Add examples, edge cases, comparisons, or implementation details to deepen the page.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "content.missing-supporting-structure": {
        "summary": "The page lacks supporting blocks that make the content more complete.",
        "whyItMatters": "Content depth improves when explanations are backed by steps, tables, bullets, or other structured elements.",
        "fixSuggestion": "Add supporting modules such as checklists, examples, data tables, or how-it-works steps.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "content.article-light-depth": {
        "summary": "The article is presentable, but still lighter than a strong reference-style resource.",
        "whyItMatters": "Deeper editorial coverage gives AI systems more context to summarize and cite reliably.",
        "fixSuggestion": "Add examples, caveats, source-backed claims, and deeper section coverage.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "content.product-light-detail": {
        "summary": "The product page needs more decision-making detail.",
        "whyItMatters": "Machines describe products better when the page includes use cases, features, and differentiation.",
        "fixSuggestion": "Expand with capabilities, ideal users, implementation detail, or comparisons.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "content.docs-light-depth": {
        "summary": "The documentation page needs more practical detail.",
        "whyItMatters": "Thin docs are less useful for task completion and AI-assisted answer generation.",
        "fixSuggestion": "Add examples, edge cases, output expectations, or troubleshooting details.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "content.homepage-thin-messaging": {
        "summary": "The homepage does not provide enough brand or product context.",
        "whyItMatters": "Thin homepage messaging makes it harder for machines to understand the company and offering quickly.",
        "fixSuggestion": "Expand the hero and supporting sections with clearer positioning, proof, and navigation cues.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
    "discoverability.homepage-weak-discovery": {
        "summary": "The homepage exposes too few internal discovery paths.",
        "whyItMatters": "Homepages should help crawlers and AI systems find the site's most important sections quickly.",
        "fixSuggestion": "Add links to primary sections such as product, docs, pricing, blog, or contact pages.",
        "example": None,
        "estimatedGain": "1-3 points",
    },
}

# 文本模式
FAQ_PATTERNS = [r"^q[:：]", r"^faq$", r"frequently asked", r"常见问题", r"问题解答", r"问答"]
DEFINITION_PATTERNS = [r"\bis\b", r"\brefers to\b", r"\bmeans\b", r"是指", r"指的是", r"是什么", r"是一种"]
COMPARISON_PATTERNS = [r"\bvs\b", r"\bcompare\b", r"\bcomparison\b", r"对比", r"比较", r"区别", r"优缺点"]
STEP_PATTERNS = [r"\b(step|steps|how to)\b", r"步骤", r"教程", r"指南", r"如何"]
SUMMARY_PATTERNS = [r"^摘要[:：]", r"^导读[:：]", r"^概述[:：]", r"^本文(?:介绍|总结|讲解|主要)", r"^本篇(?:介绍|总结|讲解|主要)"]
CITATION_PATTERNS = [r"\[(?:\d+|参考)\]", r"参考资料", r"参考链接", r"相关推荐", r"来源[:：]", r"原文链接", r"文档地址"]
QUOTABLE_PATTERNS = [r"^结论[:：]", r"^要点[:：]", r"^一句话总结[:：]", r"^核心观点[:：]", r"^关键点[:：]"]
USE_CASE_PATTERNS = [r"适用场景", r"适用于", r"适合", r"使用场景", r"应用场景", r"什么情况下", r"何时使用"]
PITFALL_PATTERNS = [r"常见错误", r"常见问题", r"避坑", r"踩坑", r"误区", r"容易出错", r"注意不要"]
PRECAUTION_PATTERNS = [r"注意事项", r"注意点", r"注意[:：]", r"温馨提示", r"建议[:：]", r"提醒[:：]"]
IGNORED_PARAGRAPH_PATTERNS = [r"相关推荐", r"热门推荐", r"猜你喜欢", r"评论", r"点赞", r"收藏", r"分享", r"上一篇", r"下一篇"]

ENTITY_DATE_PATTERN = re.compile(
    r"(?:(?:19|20)\d{2}[./-]\d{1,2}[./-]\d{1,2}(?:[ T]\d{1,2}:\d{2}(?::\d{2})?)?|"
    r"(?:19|20)\d{2}年\d{1,2}月\d{1,2}日(?:\s*\d{1,2}:\d{2}(?::\d{2})?)?)"
)
ENTITY_PUBLISH_PATTERN = re.compile(r"(发布|发表于|发布于|posted|published|created)", re.I)
ENTITY_MODIFIED_PATTERN = re.compile(r"(更新|修改|编辑于|最后更新|last updated|updated|modified|edited)", re.I)

CN_COMPANY_RE = re.compile(
    r"([\u4e00-\u9fa5A-Za-z0-9·&（）()\-\.]{2,40}?"
    r"(?:集团|股份(?:有限)?公司|有限公司|有限责任公司|（[\u4e00-\u9fa5A-Za-z0-9]+）?公司|公司))"
)
EN_COMPANY_RE = re.compile(r"([A-Z][A-Za-z0-9&.\-']{1,30}\s(?:Inc\.|Ltd\.|LLC|GmbH|Co\.,?\s?Ltd\.|Corp\.|PLC))")
# 多词英文名（如 "Zhengzhou FoamTech Nano Materials Co.,Ltd."），EN_COMPANY_RE 只吃最后一个词，需单独匹配
EN_COMPANY_MULTI_RE = re.compile(
    r"([A-Z][A-Za-z0-9&.\-']{1,40}(?:\s+[A-Za-z0-9&.\-']{1,40}){0,5}\s?,?\s?"
    r"(?:Co\.,?\s?Ltd\.?|Inc\.?|Ltd\.?|LLC|GmbH|Corp\.?|PLC|Holdings|Group)\.?)"
)
ICP_RE = re.compile(r"([\u4e00-\u9fa5]*(?:ICP|京ICP|沪ICP|粤ICP|苏ICP)[证备]?\s?[\d\-]+号)")
TM_RE = re.compile(r"[®™]")
PRICE_RE = re.compile(r"(?:¥|￥|RMB|RMB\s?)\s?\d[\d,]*\.?\d*|\$\s?\d[\d,]*\.?\d*|\d[\d,]*\s?元|\d[\d,]*\s?USD")
QUESTION_RE = re.compile(r"([^。！!?？;；]{0,60}?(?:什么|怎么|如何|为什么|哪[里个些种]?|多少|几|怎样|何时|哪里)[^。！!?？;；]{0,40}[?？])", re.I)
EN_QUESTION_RE = re.compile(r"([^.?!]{4,80}?\b(?:what|how|why|when|where|which|who|is|are|can|do|does)\b[^.?!]{0,40}[\?])", re.I)

INDUSTRY_LEXICON = {
    "制造业": ["制造", "工厂", "生产线", "设备", "机械", "零部件", "加工", "工业"],
    "软件/IT": ["软件", "SaaS", "系统", "平台", "开发", "API", "云计算", "大数据", "人工智能", "解决方案"],
    "电商/零售": ["电商", "零售", "商城", "店铺", "商品", "下单", "购物车", "直播带货"],
    "教育/培训": ["教育", "培训", "课程", "学校", "学员", "老师", "考研", "留学"],
    "医疗/健康": ["医疗", "健康", "医院", "诊所", "药品", "养生", "康复", "器械"],
    "金融/保险": ["金融", "银行", "保险", "理财", "贷款", "基金", "证券", "投资"],
    "法律/咨询": ["法律", "律师", "咨询", "合规", "诉讼", "合同", "法务"],
    "建筑/地产": ["建筑", "地产", "房地产", "工程", "装修", "施工", "物业"],
    "餐饮/食品": ["餐饮", "食品", "餐厅", "饮品", "食材", "烘焙", "酒水"],
    "旅游/酒店": ["旅游", "酒店", "旅行", "机票", "景区", "民宿", "行程"],
    "能源/环保": ["能源", "环保", "新能源", "光伏", "储能", "碳中和", "污水"],
    "文创/传媒": ["文创", "传媒", "影视", "设计", "品牌策划", "内容", "直播"],
}

SERVICE_KW = ["服务", "咨询", "解决方案", "维护", "运维", "培训", "托管", "定制", "技术支持", "售后服务", "服务热线"]
PRODUCT_KW = ["产品", "型号", "规格", "SKU", "系列", "品类", "货号", "商品详情", "参数"]
GEO_TOPIC_CHECKLIST = [
    ("公司简介/关于我们", ["关于我们", "公司简介", "企业简介", "about us", "关于", "成立于", "使命", "愿景"]),
    ("产品信息", ["产品", "product"]),
    ("服务信息", ["服务", "service", "解决方案"]),
    ("价格/报价", ["价格", "报价", "多少钱", "price", "收费", "套餐"]),
    ("联系方式", ["联系我们", "联系方式", "电话", "邮箱", "地址", "contact"]),
    ("案例/客户", ["案例", "客户", "成功案例", "合作伙伴", "testimonial"]),
    ("资质认证", ["认证", "资质", "ISO", "证书", "ce认证", "专利"]),
    ("常见问题FAQ", ["常见问题", "faq", "疑问", "问答"]),
    ("博客/资讯", ["博客", "资讯", "新闻", "文章", "blog", "news"]),
    ("团队/招聘", ["团队", "招聘", "人才", "careers", "join us"]),
    ("政策/隐私", ["隐私政策", "隐私", "条款", "terms", "policy"]),
]


# ----------------------------------------------------------------------------
# 抓取
# ----------------------------------------------------------------------------

def fetch(url, timeout=15, ua=UA, extra_headers=None):
    headers = {"User-Agent": ua, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        ctype = resp.headers.get("Content-Type", "")
        enc = resp.headers.get_content_charset() or "utf-8"
        if "charset" not in ctype.lower():
            m = re.search(rb"charset=[\"']?([\w-]+)", data[:2048])
            if m:
                enc = m.group(1).decode("ascii", "ignore") or enc
        try:
            text = data.decode(enc, "replace")
        except (LookupError, UnicodeDecodeError):
            text = data.decode("utf-8", "replace")
        return text, resp.geturl(), resp.status


def _robots_cache():
    return {}


def can_fetch(url, delay_info=None):
    try:
        p = urllib.parse.urlparse(url)
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{p.scheme}://{p.netloc}/robots.txt")
        rp.read()
        return rp.can_fetch(UA, url)
    except Exception:
        return True


def _same_domain(a, b):
    return urllib.parse.urlparse(a).netloc == urllib.parse.urlparse(b).netloc


def crawl(start_url, max_pages=30, depth=3, delay=DELAY_FLOOR, out_dir="geo_crawl"):
    os.makedirs(out_dir, exist_ok=True)
    visited = set()
    queue = [(start_url, 0)]
    pages = []
    last_req = 0
    while queue and len(visited) < max_pages:
        url, d = queue.pop(0)
        if url in visited:
            continue
        if d > depth:
            continue
        visited.add(url)
        wait = DELAY_FLOOR - (time.time() - last_req)
        if wait > 0:
            time.sleep(wait)
        last_req = time.time()
        try:
            if not can_fetch(url):
                pages.append({"url": url, "status": "robots_denied"})
                continue
            text, final_url, status = fetch(url)
        except Exception as e:
            pages.append({"url": url, "status": "error", "error": str(e)})
            continue
        fname = re.sub(r"[^A-Za-z0-9._-]", "_", urllib.parse.urlparse(final_url).path or "index") + ".html"
        if fname == ".html":
            fname = "index.html"
        fpath = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(text)
        pages.append({"url": final_url, "status": status, "saved": fpath})
        try:
            for link in extract_links(text, final_url):
                if link.get("is_internal") and link["href"] not in visited:
                    if len(visited) + len(queue) < max_pages:
                        queue.append((link["href"], d + 1))
        except Exception:
            pass
    manifest = {"start_url": start_url, "pages": pages}
    mpath = os.path.join(out_dir, "manifest.json")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return manifest


# ----------------------------------------------------------------------------
# HTML 解析 / 快照构建
# ----------------------------------------------------------------------------

def nw(value):
    """normalizeWhitespace"""
    return re.sub(r"\s+", " ", str(value or "")).strip()


def decode_html_entities(text):
    return (str(text or "")
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", "\"")
            .replace("&#39;", "'"))


def strip_tags(html_text):
    s = re.sub(r"<script[\s\S]*?</script>", " ", str(html_text or ""), flags=re.I | re.S)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return nw(s)


def has_text_value(value):
    return isinstance(value, str) and value.strip() != ""


def safe_json_parse(text):
    try:
        return json.loads(text)
    except Exception:
        return None


def collect_json_types(value, out):
    if not value or not isinstance(value, dict):
        if isinstance(value, list):
            for item in value:
                collect_json_types(item, out)
        return
    t = value.get("@type")
    if isinstance(t, list):
        for x in t:
            if isinstance(x, str):
                out.append(x)
    elif isinstance(t, str):
        out.append(t)
    if "@graph" in value:
        collect_json_types(value["@graph"], out)


def absolute_url(href, base):
    if not href:
        return None
    try:
        return urllib.parse.urljoin(base or "https://example.com/", href)
    except Exception:
        return None


# ============================================================================
# DOM 引擎（标准库 html.parser 自建）+ 信号提取（对齐 geo-html-analyzer.js）
# 替换 geo_audit.py 中基于正则的提取层。
# ============================================================================
from html.parser import HTMLParser


class _Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = dict(attrs) if attrs else {}
        self.children = []
        self.parent = None

    def get(self, name, default=None):
        return self.attrs.get(name, default)


class _DomBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Node("#document", {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = _Node(tag.lower(), attrs)
        self.stack[-1].children.append(node)
        node.parent = self.stack[-1]
        self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = _Node(tag.lower(), attrs)
        self.stack[-1].children.append(node)
        node.parent = self.stack[-1]

    def handle_endtag(self, tag):
        tag = tag.lower()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                # 必须弹出被闭合的节点本身（原为 [:i+1]，导致标签永不闭合、后续节点全部嵌套进去）
                self.stack = self.stack[:i]
                break

    def handle_data(self, data):
        if data:
            self.stack[-1].children.append(data)


def _text_of(node):
    """递归取文本，排除 script/style 子树。"""
    if isinstance(node, str):
        return node
    if node.tag in ("script", "style", "noscript", "template"):
        return ""
    parts = []
    for ch in node.children:
        parts.append(_text_of(ch))
    return "".join(parts)


def _descendants(node):
    out = []
    for ch in node.children:
        if isinstance(ch, _Node):
            out.append(ch)
            out.extend(_descendants(ch))
    return out


def _direct_text(node):
    """仅取节点的直接文本子节点（不含后代），用于识别叶子文本元素。"""
    if isinstance(node, str):
        return node
    return "".join(c for c in node.children if isinstance(c, str))


def _parse_compound(compound):
    """解析 'div.foo#bar[rel="x"][data-y*=z]' -> (tag, classes, id, attrs)。"""
    tag = None
    classes = []
    idv = None
    attrs = []  # (name, op, value); op in {'', '=', '*=', '^='}
    # 注意：标签名必须允许数字（h1~h6），否则标题选择器全部失效
    m = re.match(r"^([a-zA-Z][\w-]*|\*)?(.*)$", compound)
    if m:
        tag = m.group(1)
        rest = m.group(2)
    else:
        rest = compound
    for part in re.finditer(r"([.#])([\w-]+)|\[([^\]]+)\]", rest):
        if part.group(1) == ".":
            classes.append(part.group(2))
        elif part.group(1) == "#":
            idv = part.group(2)
        else:
            inside = part.group(3)
            am = re.match(r"\s*([\w-]+)\s*(\*=|\^=|=)?\s*\"?([^\"]*)\"?\s*$", inside)
            if am:
                attrs.append((am.group(1), am.group(2) or "", am.group(3)))
    return tag, classes, idv, attrs


def _matches_compound(node, compound):
    if isinstance(node, str):
        return False
    tag, classes, idv, attrs = _parse_compound(compound)
    if tag and tag != "*" and node.tag != tag.lower():
        return False
    if classes:
        node_classes = (node.attrs.get("class") or "").split()
        for c in classes:
            if c not in node_classes:
                return False
    if idv is not None and node.attrs.get("id") != idv:
        return False
    for an, op, av in attrs:
        val = node.attrs.get(an)
        if val is None:
            return False
        if op == "=":
            if val != av:
                return False
        elif op == "*=":
            if av not in val:
                return False
        elif op == "^=":
            if not val.startswith(av):
                return False
        # op == "" -> 仅存在即可
    return True


def _parse_selector(group):
    flat = []
    for p in re.split(r"\s+", group.strip()):
        for s in re.split(r"(>)", p):
            s = s.strip()
            if s:
                flat.append(s)
    result = []
    comb = " "
    for t in flat:
        if t == ">":
            comb = ">"
        else:
            result.append((comb, t))
            comb = " "
    return result


def _match_sequence(node, tokens):
    """node 匹配 tokens 序列的最后一个 compound，前缀按组合符匹配祖先。"""
    if isinstance(node, str):
        return False
    comb, comp = tokens[-1]
    if not _matches_compound(node, comp):
        return False
    if len(tokens) == 1:
        return True
    rest = tokens[:-1]
    if comb == ">":
        if node.parent is None:
            return False
        return _match_sequence(node.parent, rest)
    p = node.parent
    while p is not None:
        if _match_sequence(p, rest):
            return True
        p = p.parent
    return False


def query_selector_all(root, selector):
    groups = [g.strip() for g in selector.split(",") if g.strip()]
    out = []
    seen = set()
    all_nodes = _descendants(root)
    for node in all_nodes:
        for g in groups:
            if _match_sequence(node, _parse_selector(g)):
                if id(node) not in seen:
                    seen.add(id(node))
                    out.append(node)
                break
    return out


def query_selector_one(root, selector):
    res = query_selector_all(root, selector)
    return res[0] if res else None


def _doc_body(doc):
    b = query_selector_one(doc, "body")
    if b:
        return b
    h = query_selector_one(doc, "html")
    return h or doc


def _query_meta_content(doc, selector):
    node = query_selector_one(doc, selector)
    if not node:
        return ""
    val = node.attrs.get("content")
    return nw(val) if val else ""


# ---------------------------------------------------------------------------
# 主内容区选择器（对齐 jsnew PRIMARY_CONTENT_SELECTORS / EXCLUDE）
# ---------------------------------------------------------------------------
PRIMARY_CONTENT_SELECTORS = [
    "#content_views", ".markdown_views", ".markdown-body", ".md-content", ".mdx-content",
    ".theme-doc-markdown", ".theme-doc-markdown-container", ".VPDoc", ".vp-doc", ".vitepress-doc",
    ".nextra-content", ".prose", ".ProseMirror", ".article-content", ".article_content",
    ".post-content", ".entry-content", ".rich_media_content", ".detail-content", ".article-main",
    ".post-body", ".article-body", ".entry", ".main-content", ".doc-content", ".content-body",
    ".article-area", ".article-viewer", ".article", ".note-content", ".note-content-container",
    ".docMainContainer", ".doc-content-container", ".docs-content", ".docs-wrapper", ".docs-article",
    ".documentation", ".wiki-content", ".post_detail", ".blog-post", ".blog-detail", ".entry-body",
    ".post-detail", ".RichContent-inner", ".Post-RichTextContainer", ".rich_media_wrp",
    "#img-content", ".rich_media_area_primary", '[itemprop="articleBody"]',
    "main article", "article", "main", '[role="main"]', ".blog-content-box",
]
PRIMARY_CONTENT_EXCLUDE_SELECTORS = [
    "nav", "aside", "footer", ".sidebar", ".recommend-box", ".recommend-right", ".recommend-list",
    ".toolbar", ".comment-box", ".comment-list-box", ".directory-box", ".catalog-box", ".toc-box",
    ".recommend-area", ".sidebar-block", ".author-info-block", ".recommended-area", ".hot-list",
    ".table-of-contents", ".toc", ".toc-container", ".toc-wrapper", ".right-sidebar", ".left-sidebar",
    ".floating-toolbar", ".sticky-toolbar", ".social-share", ".share-box", ".pagination",
    ".breadcrumbs", ".advertisement", ".adsbygoogle",
]
ENTITY_AUTHOR_SELECTORS = [
    '[rel="author"]', '[itemprop="author"]', "[data-author-name]", '[data-testid*="author"]',
    '[class*="author"]', '[class*="writer"]', '[class*="editor"]', '[class*="nickname"]',
    '[class*="blogger"]', '[class*="profile-name"]', '[class*="user-profile"]', '[class*="user-name"]',
    '[class*="username"]', '[class*="user-nick"]', ".author-name", ".user-name", ".nickname",
    ".meta-author", '[name="author"]',
]
ENTITY_DATE_SELECTORS = [
    "time", "[datetime]", '[class*="publish"]', '[class*="posted"]', '[class*="created"]',
    '[class*="update"]', '[class*="modified"]', '[class*="edit"]', '[class*="date"]',
    '[class*="time"]', '[class*="meta"]', '[class*="info"]', '[class*="author"]',
    '[class*="header"]', "[data-publish]", "[data-published]", "[data-modified]",
    "[data-created]",
]


def _unique_strings(values):
    seen = set()
    out = []
    for v in values:
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _collect_entity_json_values(value, field_names, output):
    if not value or not isinstance(value, dict):
        if isinstance(value, list):
            for item in value:
                _collect_entity_json_values(item, field_names, output)
        return
    for key, child in value.items():
        if key in field_names:
            if isinstance(child, str):
                output.append(child)
            elif isinstance(child, dict):
                _collect_entity_json_values(child, ["name"], output)
        if isinstance(child, (dict, list)):
            _collect_entity_json_values(child, field_names, output)


def _collect_entity_org_names(value, output):
    if not value or not isinstance(value, dict):
        if isinstance(value, list):
            for item in value:
                _collect_entity_org_names(item, output)
        return
    type_value = value.get("@type")
    types = (type_value if isinstance(type_value, list) else [type_value]) or []
    types = [str(t).lower() for t in types if t]
    if any(t in ("organization", "website", "brand", "publisher") for t in types) and isinstance(value.get("name"), str):
        output.append(value["name"])
    for field_name in ("publisher", "sourceOrganization", "isPartOf", "copyrightHolder"):
        child = value.get(field_name)
        if isinstance(child, str):
            output.append(child)
        elif isinstance(child, dict):
            _collect_entity_json_values(child, ["name"], output)
    for child in value.values():
        if isinstance(child, (dict, list)):
            _collect_entity_org_names(child, output)


def _build_doc(html_text):
    b = _DomBuilder()
    try:
        b.feed(str(html_text or ""))
    except Exception:
        pass
    return b.root


# ----------------------------------------------------------------------------
# HTML 清洗：剔除 script/style/noscript/template 原始文本（对齐 JS innerText
# 行为，避免把脚本/样式内容误判为正文）。保留 application/ld+json，因为
# 结构化数据提取依赖它。
# ----------------------------------------------------------------------------
_SCRIPT_RE = re.compile(r"<script\b[^>]*>[\s\S]*?</script\s*>", re.I)
_STYLE_RE = re.compile(r"<style\b[^>]*>[\s\S]*?</style\s*>", re.I)
_NOSCRIPT_RE = re.compile(r"<noscript\b[^>]*>[\s\S]*?</noscript\s*>", re.I)
_TEMPLATE_RE = re.compile(r"<template\b[^>]*>[\s\S]*?</template\s*>", re.I)
_LD_JSON_OPEN_RE = re.compile(r'<script\b[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>', re.I)


def _clean_html(html):
    if not html:
        return ""
    def _keep_or_drop(m):
        return m.group(0) if _LD_JSON_OPEN_RE.match(m.group(0)) else " "
    cleaned = _SCRIPT_RE.sub(_keep_or_drop, html)
    cleaned = _STYLE_RE.sub(" ", cleaned)
    cleaned = _NOSCRIPT_RE.sub(" ", cleaned)
    cleaned = _TEMPLATE_RE.sub(" ", cleaned)
    return cleaned


def _extract_entity_script_value_raw(html, pattern):
    for m in _SCRIPT_RE.finditer(html or ""):
        block = m.group(0)
        if _LD_JSON_OPEN_RE.match(block):
            continue
        sm = re.search(pattern, block, re.I)
        if sm and sm.group(1):
            return nw(sm.group(1))
    return ""


def _text_of_including_script(node):
    """取节点内全部文本（不排除 script/style 自身内容）。

    _text_of 会为 script/style 返回空串，若用它读 <script type="application/ld+json">
    永远得到空值，导致 JSON-LD 全部漏检。读 schema 必须用本函数。
    """
    if isinstance(node, str):
        return node
    parts = []
    for ch in node.children:
        parts.append(_text_of_including_script(ch))
    return "".join(parts)


def extract_schema_blocks_dom(doc):
    blocks = []
    for node in query_selector_all(doc, 'script[type="application/ld+json"]'):
        raw = nw(_text_of_including_script(node))
        if not raw:
            continue
        parsed = safe_json_parse(raw)
        types = []
        collect_json_types(parsed, types)
        blocks.append({"raw": raw, "parsedTypes": types})
    return blocks


def extract_page_meta_dom(doc, page_url):
    canonical_node = query_selector_one(doc, 'link[rel="canonical"], link[rel="alternate"][hreflang="x-default"]')
    canonical_href = canonical_node.attrs.get("href", "") if canonical_node else ""
    title_node = query_selector_one(doc, "title")
    title = nw(_text_of(title_node)) if title_node else ""
    html_node = query_selector_one(doc, "html")
    lang = nw(html_node.attrs.get("lang", "")) if html_node else ""

    def og(prop):
        node = query_selector_one(doc, 'meta[property="og:%s"]' % prop)
        if not node:
            return ""
        v = node.attrs.get("content")
        return nw(v) if v else ""

    og = {
        "title": og("title"),
        "description": og("description"),
        "image": absolute_url(og("image"), page_url) or None,
        "type": og("type"),
        "siteName": og("site_name"),
    }
    og = {k: v for k, v in og.items() if v}
    return {
        "title": title or _query_meta_content(doc, 'meta[name="title"]') or "",
        "metaDescription": _query_meta_content(doc, 'meta[name="description"]') or _query_meta_content(doc, 'meta[property="description"]'),
        "canonical": absolute_url(canonical_href, page_url) or canonical_href or "",
        "lang": lang,
        "metaRobots": _query_meta_content(doc, 'meta[name="robots"]') or _query_meta_content(doc, 'meta[name="googlebot"]'),
        "openGraph": og,
    }


def extract_headings_dom(doc):
    headings = []
    for node in query_selector_all(doc, "h1, h2, h3, h4, h5, h6"):
        try:
            level = int(node.tag[1])
        except Exception:
            level = 1
        text = nw(_text_of(node))
        if text:
            headings.append({"level": level, "text": text})
    return headings


def extract_links_dom(doc, base_url):
    base = absolute_url(base_url or "https://example.com/", base_url or "https://example.com/") or "https://example.com/"
    try:
        base_host = urllib.parse.urlparse(base).hostname or ""
    except Exception:
        base_host = ""
    links = []
    for node in query_selector_all(doc, "a[href]"):
        href = nw(node.attrs.get("href", ""))
        if not href or href.startswith(("javascript:", "#")):
            continue
        is_ext = href.startswith(("mailto:", "tel:"))
        rel = node.attrs.get("rel", "") or ""
        is_nofollow = "nofollow" in rel.lower()
        if is_ext:
            links.append({"href": href, "text": nw(_text_of(node)), "isInternal": False,
                          "isExternal": False, "isNofollow": is_nofollow})
            continue
        resolved = absolute_url(href, base)
        if not resolved:
            continue
        try:
            host = urllib.parse.urlparse(resolved).hostname or ""
        except Exception:
            host = ""
        links.append({
            "href": resolved,
            "text": nw(_text_of(node)),
            "isInternal": host == base_host,
            "isExternal": host not in ("", base_host),
            "isNofollow": is_nofollow,
        })
    return links


def _unique_nodes(nodes):
    seen = set()
    out = []
    for n in nodes:
        if id(n) not in seen:
            seen.add(id(n))
            out.append(n)
    return out


def get_primary_content_roots(doc):
    candidates = []
    for selector in PRIMARY_CONTENT_SELECTORS:
        for node in query_selector_all(doc, selector):
            if len(_text_of(node)) >= 120:
                candidates.append(node)
    candidates = _unique_nodes(candidates)
    scored = []
    for node in candidates:
        text = _text_of(node)
        text_length = len(text)
        paragraph_count = len(query_selector_all(node, "p"))
        heading_count = len(query_selector_all(node, "h1, h2, h3, h4"))
        list_count = len(query_selector_all(node, "ul, ol"))
        table_count = len(query_selector_all(node, "table"))
        code_count = len(query_selector_all(node, "pre, code"))
        image_count = len(query_selector_all(node, "img"))
        link_count = len(query_selector_all(node, "a[href]"))
        noisy_count = sum(len(query_selector_all(node, sel)) for sel in PRIMARY_CONTENT_EXCLUDE_SELECTORS)
        id_text = (node.attrs.get("id") or "").lower()
        class_text = (node.attrs.get("class") or "").lower()
        bonus = 0
        if node.tag == "article":
            bonus += 800
        if "content" in id_text:
            bonus += 500
        if "article" in id_text:
            bonus += 450
        if "markdown" in class_text:
            bonus += 450
        if "article" in class_text:
            bonus += 400
        if "post-content" in class_text:
            bonus += 400
        if "entry-content" in class_text:
            bonus += 400
        if "rich_media_content" in class_text:
            bonus += 400
        if "markdown-body" in class_text:
            bonus += 420
        if "theme-doc-markdown" in class_text:
            bonus += 420
        if "vp-doc" in class_text:
            bonus += 420
        if "prose" in class_text:
            bonus += 300
        if "doc-content" in class_text:
            bonus += 320
        if "documentation" in class_text:
            bonus += 320
        if "main-content" in class_text:
            bonus += 250
        score = (min(text_length, 4200) + 180 * paragraph_count + 90 * heading_count
                 + 60 * list_count + 80 * table_count + 70 * code_count + 20 * image_count
                 - 12 * link_count - 260 * noisy_count
                 + (40 * paragraph_count if paragraph_count >= 4 else 0) + bonus)
        if score > 0:
            scored.append((score, node))
    scored.sort(key=lambda x: -x[0])
    return [n for _, n in scored]


def _query_scoped_nodes(roots, selector, limit):
    out = []
    seen = set()
    for root in roots:
        for node in query_selector_all(root, selector):
            if len(out) >= limit:
                break
            if id(node) in seen:
                continue
            seen.add(id(node))
            out.append(node)
        if len(out) >= limit:
            break
    return out


def scoped_query(doc, selector, limit):
    roots = get_primary_content_roots(doc)
    active = roots if roots else [_doc_body(doc)]
    return _query_scoped_nodes(active, selector, limit)


def create_block(block_type, text):
    normalized = nw(text)
    if not normalized:
        return None
    if block_type == "paragraph" and any(re.search(p, normalized, re.I) for p in IGNORED_PARAGRAPH_PATTERNS):
        return None
    return {"type": block_type, "text": normalized}


def extract_content_blocks_dom(doc):
    blocks = []

    def add_para(nodes):
        for node in nodes:
            if len(nw(_text_of(node))) >= 24:
                b = create_block("paragraph", _text_of(node))
                if b:
                    blocks.append(b)

    for node in scoped_query(doc, ".summary, .abstract, .lead, .article-summary, .post-summary, .doc-summary, .excerpt, .introduction, .intro, .overview, .highlight, .callout", 12):
        b = create_block("paragraph", _text_of(node))
        if b and len(b["text"]) >= 30:
            blocks.append(b)
    for node in scoped_query(doc, "p, li, div", 36):
        if len(nw(_text_of(node))) >= 24 and SUMMARY_PATTERNS and any(re.search(p, nw(_text_of(node)), re.I) for p in SUMMARY_PATTERNS):
            b = create_block("paragraph", _text_of(node))
            if b:
                blocks.append(b)
    for node in scoped_query(doc, "p, article section > div, main section > div", 48):
        if len(nw(_text_of(node))) >= 20:
            b = create_block("paragraph", _text_of(node))
            if b:
                blocks.append(b)
    for node in scoped_query(doc, "ul, ol", 20):
        if len(nw(_text_of(node))) >= 20:
            b = create_block("list", _text_of(node))
            if b:
                blocks.append(b)
    for node in scoped_query(doc, "table", 10):
        if len(nw(_text_of(node))) >= 30:
            b = create_block("table", _text_of(node))
            if b:
                blocks.append(b)
    for node in scoped_query(doc, "blockquote, q, [data-quote], .quote, .blockquote, .pullquote", 16):
        if len(nw(_text_of(node))) >= 20:
            b = create_block("quote", _text_of(node))
            if b:
                blocks.append(b)
    for node in scoped_query(doc, "dt", 10):
        b = create_block("definition", "%s: %s" % (_text_of(node), _text_of(node.next_element if hasattr(node, "next_element") else None)))
        if b:
            blocks.append(b)
    for node in scoped_query(doc, "p", 20):
        if len(nw(_text_of(node))) >= 20 and any(re.search(p, nw(_text_of(node)), re.I) for p in DEFINITION_PATTERNS):
            b = create_block("definition", _text_of(node))
            if b:
                blocks.append(b)
    faq_nodes = scoped_query(doc, '[itemtype*="FAQPage"], [data-faq], [class*="faq"], [class*="question"], details', 14)
    if faq_nodes:
        for node in faq_nodes:
            b = create_block("faq", _text_of(node))
            if b:
                blocks.append(b)
    else:
        for node in scoped_query(doc, "h2, h3, h4", 20):
            if any(re.search(p, nw(_text_of(node)), re.I) for p in FAQ_PATTERNS):
                b = create_block("faq", _text_of(node.parent if hasattr(node, "parent") else node))
                if b:
                    blocks.append(b)
    for node in scoped_query(doc, "ol, [class*='steps'], [class*='step'], [data-step]", 16):
        txt = nw(_text_of(node.parent if hasattr(node, "parent") else node))
        if STEP_PATTERNS and (any(re.search(p, txt, re.I) for p in STEP_PATTERNS) or re.search(r"^\s*(?:step\s*\d+|第[\d一二三四五六七八九十]+步|[1-9]\.)", txt, re.I)):
            b = create_block("steps", _text_of(node))
            if b:
                blocks.append(b)
    for node in scoped_query(doc, "img[alt]", 12):
        alt = node.attrs.get("alt", "") or ""
        b = create_block("image", alt)
        if b:
            blocks.append(b)
    # 通用正文兜底：捕获主内容区/body 下含实质中文的叶子文本元素
    # （兼容 div/span 型 CMS 站点，这类站点正文常不在 <p> 也不在 article/main/section 内）
    sweep_roots = get_primary_content_roots(doc) or [_doc_body(doc)]
    for root in sweep_roots:
        for node in query_selector_all(root, "p, div, span, li"):
            d = _direct_text(node)
            nd = nw(d)
            if len(nd) >= 10 and len(re.findall(r"[\u4e00-\u9fff]", nd)) >= 4:
                b = create_block("paragraph", d)
                if b:
                    blocks.append(b)
    # 去重
    seen = set()
    deduped = []
    for b in blocks:
        key = (b["type"], b["text"])
        if key not in seen:
            seen.add(key)
            deduped.append(b)
    # fallback
    deduped.extend(_fallback_paragraph_block(doc, deduped))
    return deduped


def _fallback_paragraph_block(doc, blocks):
    paragraphs = [b for b in blocks if b["type"] == "paragraph"]
    total = sum(len(b["text"]) for b in paragraphs)
    if len(paragraphs) >= 2 or total >= 280:
        return []
    selectors = PRIMARY_CONTENT_SELECTORS + ["body"]
    for selector in selectors:
        node = query_selector_one(doc, selector)
        if not node:
            continue
        text = _text_of(node)
        if len(text) < 140:
            continue
        if any(b["text"] == text for b in paragraphs):
            continue
        clipped = text if len(text) <= 2400 else (text[:2400].rstrip() + "...")
        b = create_block("paragraph", clipped)
        if b:
            return [b]
    return []


def normalize_entity_date(value):
    m = re.search(ENTITY_DATE_PATTERN, str(value or ""))
    if not m:
        return ""
    return (m.group(0).replace("年", "-").replace("月", "-").replace("日", "")
            .replace("/", "-").replace("T", " ").strip())


def extract_entity_signals_dom(schema_blocks, doc, raw_html=""):
    meta_author = _query_meta_content(doc, 'meta[name="author"]')
    og_site_name = _query_meta_content(doc, 'meta[property="og:site_name"]')
    author_names = []
    org_names = []
    if meta_author:
        author_names.append(meta_author)
    if og_site_name:
        org_names.append(og_site_name)
    # 补充：从 <title> / 页脚版权区 / 正文短文本识别公司名实体
    # （很多站没有 og:site_name，也没有 JSON-LD，公司全称只出现在 <title> 或页脚备案信息里）
    if not org_names:
        _company_candidates = []
        _title_node = query_selector_one(doc, "title")
        if _title_node:
            _company_candidates.append(nw(_text_of(_title_node)))
        # 属性匹配：很多站没有 <footer> 标签，版权信息在 class/id 含 copyright/footer/icp 的容器里
        for _node in _descendants(doc):
            _mark = ("%s %s" % (_node.attrs.get("class", ""), _node.attrs.get("id", ""))).lower()
            if re.search(r"(copyright|copy-right|footer|site-info|icp|beian)", _mark):
                _t = nw(_text_of(_node))
                if 0 < len(_t) <= 600:
                    _company_candidates.append(_t)
        # 兜底：整页文本（公司名常只出现在页尾版权行，节点扫描可能够不到）
        _company_candidates.append(nw(_text_of(_doc_body(doc)))[:20000])
        for _cand in _company_candidates:
            for _m in CN_COMPANY_RE.finditer(_cand):
                _name = _m.group(1).strip(" -_|｜·.。")
                # 若命中片段含分隔符（如"品牌词-公司全称"），取含"公司/集团"的纯公司名段
                for _p in [x for x in re.split(r"[-_|｜/]", _name) if x]:
                    if CN_COMPANY_RE.fullmatch(_p):
                        _name = _p
                        break
                # 过滤过短/噪声（如"idc公司"）：要求至少 4 个汉字
                if len(re.findall(r"[\u4e00-\u9fa5]", _name)) >= 4 and 5 <= len(_name) <= 40:
                    org_names.append(_name)
            # 优先用多词匹配（能拿到完整公司名），再用单词匹配兜底
            _en_hits = [m.group(1).strip() for m in EN_COMPANY_MULTI_RE.finditer(_cand)]
            if not _en_hits:
                _en_hits = [m.group(1).strip() for m in EN_COMPANY_RE.finditer(_cand)]
            for _n in _en_hits:
                # 去掉 "© Copyright 2026 ..." 这类前缀噪声
                _n = re.sub(r"^(?:\s*(?:©|\(c\)|copyright|all\s+rights\s+reserved|powered\s+by|20\d\d|19\d\d))+",
                            "", _n, flags=re.I).strip(" .,-")
                if 4 <= len(_n) <= 60:
                    org_names.append(_n)
            if org_names:
                break
    for selector in ENTITY_AUTHOR_SELECTORS:
        for node in query_selector_all(doc, selector):
            v = nw(_text_of(node))
            if 2 <= len(v) <= 80:
                author_names.append(v)
    for node in query_selector_all(doc, "span, div, p, a, strong")[:80]:
        m = re.search(r"(?:作者|编辑|发布者|Author|By)[:：]\s*([^\n|｜/]{2,60})", nw(_text_of(node)), re.I)
        if m:
            author_names.append(m.group(1))
    script_author = _extract_entity_script_value_raw(raw_html, r"""(?:var|let|const)\s+(?:nickName|nickname|authorName|author|username|userName|blogger|editorName)\s*=\s*["']([^"'\\\n]{2,80})["']""")
    if script_author:
        author_names.append(script_author)
    schema_types = []
    schema_values = []
    for block in schema_blocks:
        for t in block["parsedTypes"]:
            schema_types.append(t)
        parsed = safe_json_parse(block["raw"])
        if parsed:
            schema_values.append(parsed)
        if re.search(r'"name"\s*:\s*"([^"]+)"', block["raw"]) and re.search(r"Organization|WebSite|Brand", block["raw"], re.I):
            m = re.search(r'"name"\s*:\s*"([^"]+)"', block["raw"])
            if m:
                org_names.append(m.group(1))
        if re.search(r'"author"\s*:', block["raw"], re.I) and re.search(r'"name"\s*:\s*"([^"]+)"', block["raw"], re.I):
            m = re.search(r'"author"[\s\S]*?"name"\s*:\s*"([^"]+)"', block["raw"], re.I)
            if m:
                author_names.append(m.group(1))
    for value in schema_values:
        _collect_entity_json_values(value, ["author", "creator"], author_names)
        _collect_entity_org_names(value, org_names)
    schema_publish = []
    schema_modified = []
    for value in schema_values:
        _collect_entity_json_values(value, ["datePublished", "pubDate", "dateCreated", "uploadDate"], schema_publish)
        _collect_entity_json_values(value, ["dateModified", "upDate", "modifiedTime"], schema_modified)
    links = query_selector_all(doc, "a[href]")
    published_meta = (_query_meta_content(doc, 'meta[property="article:published_time"]')
                      or _query_meta_content(doc, 'meta[name="publish_date"]')
                      or _query_meta_content(doc, 'meta[itemprop="datePublished"]')
                      or _query_meta_content(doc, 'meta[name="pubdate"]'))
    modified_meta = (_query_meta_content(doc, 'meta[property="article:modified_time"]')
                     or _query_meta_content(doc, 'meta[itemprop="dateModified"]')
                     or _query_meta_content(doc, 'meta[name="lastmod"]')
                     or _query_meta_content(doc, 'meta[name="last-modified"]'))
    publish_date = (normalize_entity_date(published_meta)
                    or _extract_entity_date(doc, "published")
                    or normalize_entity_date(_extract_entity_script_value_raw(raw_html, r"""(?:var|let|const)\s+(?:postTime|publishTime|publishedAt|publishDate|articlePublishedTime|pubDate)\s*=\s*["']([^"'\\\n]{8,40})["']"""))
                    or next((normalize_entity_date(x) for x in schema_publish if normalize_entity_date(x)), "")
                    or "")
    modified_date = (normalize_entity_date(modified_meta)
                     or _extract_entity_date(doc, "modified")
                     or normalize_entity_date(_extract_entity_script_value_raw(raw_html, r"""(?:var|let|const)\s+(?:updateTime|updatedAt|modifiedTime|lastModified|articleModifiedTime|upDate)\s*=\s*["']([^"'\\\n]{8,40})["']"""))
                     or next((normalize_entity_date(x) for x in schema_modified if normalize_entity_date(x)), "")
                     or "")
    return {
        "authorNames": _unique_strings(author_names),
        "organizationNames": _unique_strings(org_names),
        "publishDate": publish_date,
        "modifiedDate": modified_date,
        "contactLinks": _unique_strings([node.attrs.get("href", "") for node in links
                                         if re.search(r"(contact|support|help|customer service|联系方式|联系我们|客服|支持|mailto:|tel:|whatsapp)", "%s %s" % (node.attrs.get("href", ""), _text_of(node)), re.I)]),
        "aboutLinks": _unique_strings([node.attrs.get("href", "") for node in links
                                      if re.search(r"(about|company|team|our story|关于我们|团队|公司)", "%s %s" % (node.attrs.get("href", ""), _text_of(node)), re.I)]),
        "schemaTypes": _unique_strings(schema_types),
    }


def _extract_entity_date(doc, mode):
    if mode == "published":
        direct = 'time[datetime], [data-publish], [data-published], [data-created]'
    else:
        direct = '[data-modified], [data-updated], [class*="update"] time[datetime], [class*="modified"] time[datetime]'
    for node in query_selector_all(doc, direct):
        value = (node.attrs.get("datetime") or node.attrs.get("data-publish") or node.attrs.get("data-published")
                 or node.attrs.get("data-created") or node.attrs.get("data-modified") or node.attrs.get("data-updated")
                 or _text_of(node))
        norm = normalize_entity_date(value)
        if norm:
            return norm
    pattern = ENTITY_PUBLISH_PATTERN if mode == "published" else ENTITY_MODIFIED_PATTERN
    for node in query_selector_all(doc, ", ".join(ENTITY_DATE_SELECTORS))[:60]:
        text = nw(_text_of(node))
        parent_text = nw(_text_of(node.parent)) if node.parent else ""
        if not (pattern.search(text) or pattern.search(parent_text)):
            continue
        norm = normalize_entity_date(text) or normalize_entity_date(parent_text)
        if norm:
            return norm
    return ""


def _extract_entity_script_value(doc, pattern):
    for node in query_selector_all(doc, "script"):
        m = re.search(pattern, _text_of(node), re.I)
        if m and m.group(1):
            return nw(m.group(1))
    return ""

def extract_schema_blocks(html_text):
    return extract_schema_blocks_dom(_build_doc(html_text))

def extract_page_meta(html_text):
    return extract_page_meta_dom(_build_doc(_clean_html(html_text)), "")

def extract_headings(html_text):
    return extract_headings_dom(_build_doc(_clean_html(html_text)))

def extract_links(html_text, base_url):
    return extract_links_dom(_build_doc(_clean_html(html_text)), base_url)

def extract_content_blocks(html_text):
    return extract_content_blocks_dom(_build_doc(_clean_html(html_text)))

def extract_entity_signals(schema_blocks, html_text, links):
    return extract_entity_signals_dom(schema_blocks, _build_doc(_clean_html(html_text)), html_text)

def detect_pattern(text, patterns):
    return any(re.search(p, text, re.I) for p in patterns)

def extract_text_summary(content_blocks):
    paragraphs = [b for b in content_blocks if b["type"] == "paragraph"]
    paragraph_lengths = [len(b["text"]) for b in paragraphs]
    total = sum(paragraph_lengths)
    visible_text = " ".join(b["text"] for b in paragraphs)
    excerpt = visible_text[:280]
    joined = " ".join(b["text"] for b in content_blocks)
    first_paras = paragraphs[:3]
    has_summary_lead = any(detect_pattern(b["text"], SUMMARY_PATTERNS) for b in first_paras) or len(excerpt) >= 140
    return {
        "visibleTextLength": total,
        "paragraphCount": len(paragraphs),
        "averageParagraphLength": round(total / len(paragraphs)) if paragraphs else 0,
        "hasFaqPattern": any(b["type"] == "faq" for b in content_blocks),
        "hasDefinitionPattern": any(b["type"] == "definition" for b in content_blocks) or detect_pattern(joined, DEFINITION_PATTERNS),
        "hasStepsPattern": any(b["type"] == "steps" for b in content_blocks),
        "hasComparisonPattern": detect_pattern(joined, COMPARISON_PATTERNS),
        "hasSummaryLead": has_summary_lead,
        "hasCitationPattern": any(detect_pattern(b["text"], CITATION_PATTERNS) for b in content_blocks) or detect_pattern(joined, CITATION_PATTERNS),
        "hasQuotableSnippet": any(b["type"] == "quote" for b in content_blocks)
            or any((28 <= len(b["text"]) <= 120 and re.search(r"[:：。]", b["text"])) for b in paragraphs),
        "hasUseCasePattern": detect_pattern(joined, USE_CASE_PATTERNS),
        "hasPitfallPattern": detect_pattern(joined, PITFALL_PATTERNS),
        "hasPrecautionPattern": detect_pattern(joined, PRECAUTION_PATTERNS),
        "excerpt": excerpt,
    }

def _collect_json_values(value, field_names, out=None):
    if out is None:
        out = []
    if not value or not isinstance(value, dict):
        if isinstance(value, list):
            for it in value:
                _collect_json_values(it, field_names, out)
        return out
    for k, child in value.items():
        if k in field_names:
            if isinstance(child, str):
                out.append(child)
            elif isinstance(child, dict):
                _collect_json_values(child, ["name"], out)
        if isinstance(child, (dict, list)):
            _collect_json_values(child, field_names, out)
    return out


def _collect_org_names(value, out):
    if not value or not isinstance(value, dict):
        if isinstance(value, list):
            for it in value:
                _collect_org_names(it, out)
        return
    t = value.get("@type")
    types = [t] if isinstance(t, str) else (t if isinstance(t, list) else [])
    if any(str(x).lower() in ("organization", "website", "brand", "publisher") for x in types) and isinstance(value.get("name"), str):
        out.append(value["name"])
    for f in ("publisher", "sourceOrganization", "isPartOf", "copyrightHolder"):
        child = value.get(f)
        if isinstance(child, str):
            out.append(child)
        elif isinstance(child, dict):
            _collect_json_values(child, ["name"], out)
    for child in value.values():
        if isinstance(child, (dict, list)):
            _collect_org_names(child, out)


def _unique(values):
    return list(dict.fromkeys([nw(v) for v in values if v]).__iter__()) if False else list(dict.fromkeys([str(v).strip() for v in values if v]))


def has_schema_type(parsed_types, expected):
    return any(str(t).lower() == str(e).lower() for t in (parsed_types or []) for e in (expected or []))


def count_keyword_hits(text, keywords):
    return sum(1 for k in keywords if k in text)


def pathname_lower(url):
    try:
        return urllib.parse.urlparse(url or "").path.lower()
    except Exception:
        return "/"


def is_product_detail_path(pathname):
    return bool(re.search(r"/products/[^/]+|/productdetail(?:/|$)|/product/[^/]+|/detail/[^/]+", pathname))


def infer_page_role(url, title, headings, schema_blocks):
    pathname = pathname_lower(url)
    headings_text = " ".join(h["text"].lower() for h in headings)
    t = str(title or "").lower()
    merged = f"{t} {headings_text} {pathname}".lower()
    schema_types = [tp for b in schema_blocks for tp in b["parsedTypes"]]
    is_home = pathname in ("/", "", "/home", "/index")
    has_brand = has_schema_type(schema_types, ["WebSite", "Organization", "Brand"])
    has_product = has_schema_type(schema_types, ["Product", "Service", "SoftwareApplication"])
    has_article = has_schema_type(schema_types, ["Article", "BlogPosting", "NewsArticle"])
    has_docs = has_schema_type(schema_types, ["TechArticle", "HowTo", "FAQPage"])
    og_type = ""
    if is_home and (has_brand or og_type.count("website") or count_keyword_hits(merged, ["home", "about us", "contact us", "latest news", "company"]) >= 2) and not has_article:
        return "about" if "about" in merged else "homepage"
    if re.search(r"/pages/about|/about\b|about us|about our company|our company", merged):
        return "about"
    if re.search(r"/pages/contact|/contact\b|contact us|email us|phone|whatsapp", merged):
        return "contact"
    if re.search(r"/products/?$|/products\b|/productlist(?:/|$)|/product\b", pathname) and not is_product_detail_path(pathname):
        return "product-list"
    if is_product_detail_path(pathname) or (has_product and not is_home):
        return "product-detail"
    if re.search(r"/news/?$|all news|latest news|news list", merged):
        return "news-list"
    if has_article:
        return "article"
    if has_docs:
        return "docs"
    if re.search(r"landing|campaign|webinar|demo|signup|free trial|book a demo|get started", merged):
        return "landing"
    return "unknown"


def infer_page_type(url, title, headings, schema_blocks):
    pathname = pathname_lower(url)
    try:
        host = urllib.parse.urlparse(url or "").hostname.lower()
    except Exception:
        host = ""
    headings_text = " ".join(h["text"].lower() for h in headings)
    t = str(title or "").lower()
    merged = f"{t} {headings_text} {pathname}".lower()
    role = infer_page_role(url, title, headings, schema_blocks)
    schema_types = [tp for b in schema_blocks for tp in b["parsedTypes"]]
    has_brand = has_schema_type(schema_types, ["WebSite", "Organization", "Brand"])
    has_product = has_schema_type(schema_types, ["Product", "Service", "SoftwareApplication"])
    has_article = has_schema_type(schema_types, ["Article", "BlogPosting", "NewsArticle"])
    has_docs = has_schema_type(schema_types, ["TechArticle", "HowTo", "FAQPage"])
    og_type = ""
    homepage_hits = count_keyword_hits(merged, ["home", "about us", "contact us", "all news", "company", "latest news", "about our company", "why choose us"])
    product_hits = count_keyword_hits(merged, ["pricing", "features", "plans", "product", "service", "solution", "platform", "套餐", "价格", "功能", "产品介绍", "解决方案", "服务介绍"])
    is_home = pathname in ("/", "", "/home", "/index")

    if role == "homepage":
        return "homepage"
    if role in ("product-list", "product-detail"):
        return "product"
    if role in ("about", "contact"):
        return "homepage"
    if role in ("news-list", "article"):
        return "article"
    if role == "docs":
        return "docs"
    if role == "landing":
        return "landing"
    if "article" in og_type:
        return "article"
    if "product" in og_type:
        return "product"
    if has_article:
        return "article"
    if has_docs or "/docs" in pathname or "/doc/" in pathname or "/documentation" in pathname or "/kb" in pathname \
            or "/knowledge" in pathname or "/manual" in pathname or "/tutorial" in pathname or "/learn" in pathname \
            or "/api" in pathname or "/guide" in pathname or "/help" in pathname \
            or detect_pattern(merged, [r"(docs|documentation|guide|help center|knowledge base|api reference|developer|开发文档|帮助中心|使用指南|教程|快速开始|接入指南)"]):
        return "docs"
    if "/blog" in pathname or "/news" in pathname or "/article" in pathname or "/p/" in pathname or "/post" in pathname \
            or "/posts" in pathname or "/details" in pathname or "/archives" in pathname or "/s/" in pathname \
            or host.startswith("blog.") or detect_pattern(merged, [r"(blog|article|editorial|news|release note|博客|文章|资讯|专栏|公众号|新闻|动态|观点|案例分享)"]):
        return "article"
    if is_home and (has_brand or "website" in og_type or homepage_hits >= 2) and not has_article:
        return "homepage"
    if "/product" in pathname or "/products" in pathname or "/productdetail" in pathname or "/productlist" in pathname \
            or "/solution" in pathname or "/solutions" in pathname or "/service" in pathname or "/services" in pathname \
            or "/platform" in pathname or "/pricing" in pathname or "/features" in pathname \
            or (product_hits >= 2 and not has_article) or has_product:
        return "product"
    if (has_brand and is_home) or is_home:
        return "homepage"
    if detect_pattern(merged, [r"landing|campaign|webinar|demo|signup|free trial|book a demo|get started|立即体验|立即试用|预约演示|申请试用|活动页"]):
        return "landing"
    return "unknown"


def create_snapshot_from_html(html_text, url=""):
    page_url = url if has_text_value(url) else "https://example.com/geo-sample-page"
    meta = extract_page_meta(html_text)
    headings = extract_headings(html_text)
    schema = extract_schema_blocks(html_text)
    links = extract_links(html_text, page_url)
    content_blocks = extract_content_blocks(html_text)
    text_summary = extract_text_summary(content_blocks)
    entity_signals = extract_entity_signals(schema, html_text, links)
    page_type = infer_page_type(page_url, meta["title"], headings, schema)
    page_role = infer_page_role(page_url, meta["title"], headings, schema)
    return {
        "url": page_url,
        "title": meta["title"],
        "metaDescription": meta["metaDescription"],
        "canonical": meta["canonical"],
        "lang": meta["lang"],
        "h1List": [h["text"] for h in headings if h["level"] == 1],
        "headings": headings,
        "metaRobots": meta["metaRobots"],
        "openGraph": meta["openGraph"],
        "schema": schema,
        "links": links,
        "contentBlocks": content_blocks,
        "textSummary": text_summary,
        "entitySignals": entity_signals,
        "pageTypeHint": page_type,
        "pageRoleHint": page_role,
    }


# ----------------------------------------------------------------------------
# 规则引擎（十维扣分制）
# ----------------------------------------------------------------------------

def failure(rule_key, dimension, priority, score_impact, title, evidence=None):
    res = {"ruleKey": rule_key, "dimension": dimension, "passed": False,
           "priority": priority, "scoreImpact": score_impact, "title": title}
    if evidence:
        res["evidence"] = evidence
    return res


def get_reference_age_in_days(snapshot):
    es = snapshot.get("entitySignals", {})
    for dv in (es.get("modifiedDate"), es.get("publishDate")):
        if dv:
            try:
                ts = datetime.strptime(re.sub(r"[T ]\d{1,2}:\d{2}(?::\d{2})?$", "", dv), "%Y-%m-%d")
                return (datetime.now() - ts).days
            except Exception:
                try:
                    ts = datetime.strptime(dv[:10], "%Y-%m-%d")
                    return (datetime.now() - ts).days
                except Exception:
                    continue
    return None


def run_rules(snapshot):
    results = []
    page_type = str(snapshot.get("pageTypeHint", "unknown"))
    page_role = str(snapshot.get("pageRoleHint", "unknown"))
    schema_types = [tp for b in snapshot.get("schema", []) for tp in b["parsedTypes"]]
    links = snapshot.get("links", [])
    content_blocks = snapshot.get("contentBlocks", [])
    text_summary = snapshot.get("textSummary", {})
    entity_signals = snapshot.get("entitySignals", {})

    internal_links = [l for l in links if l.get("isInternal")]
    has_internal_links = len(internal_links) > 0
    has_external_links = any(l.get("isExternal") for l in links)
    og = snapshot.get("openGraph", {})
    has_og_title = has_text_value(og.get("title"))
    has_og_desc = has_text_value(og.get("description"))

    has_faq_blocks = any(b["type"] == "faq" for b in content_blocks)
    has_def_blocks = any(b["type"] == "definition" for b in content_blocks)
    has_list_blocks = any(b["type"] == "list" for b in content_blocks)
    has_step_blocks = any(b["type"] == "steps" for b in content_blocks)
    has_table_blocks = any(b["type"] == "table" for b in content_blocks)
    has_quote_blocks = any(b["type"] == "quote" for b in content_blocks)
    avg_para_len = int(text_summary.get("averageParagraphLength", 0))

    has_about_links = len(entity_signals.get("aboutLinks", [])) > 0
    has_contact_links = len(entity_signals.get("contactLinks", [])) > 0
    ref_age = get_reference_age_in_days(snapshot)
    has_brand_schema = has_schema_type(schema_types, ["Organization", "WebSite", "Brand"])
    has_product_schema = has_schema_type(schema_types, ["Product", "Service", "SoftwareApplication"])
    org_names = entity_signals.get("organizationNames", [])
    author_names = entity_signals.get("authorNames", [])
    has_primary_entity = len(org_names) > 0 or has_text_value(og.get("siteName")) or has_brand_schema
    has_content_owner = len(author_names) > 0 or len(org_names) > 0 or has_text_value(og.get("siteName"))

    is_about = page_role == "about"
    is_contact = page_role == "contact"
    is_homepage_like = page_type == "homepage" or is_about or is_contact
    is_product_list = page_role == "product-list"
    is_product_detail = page_role == "product-detail"

    if not has_text_value(snapshot.get("canonical")):
        results.append(failure("crawl.missing-canonical", "crawlability", "P1", 2, "Missing canonical tag"))
    if not has_text_value(snapshot.get("lang")):
        results.append(failure("crawl.missing-lang", "crawlability", "P2", 1, "Missing document language"))
    meta_robots = str(snapshot.get("metaRobots", "")).lower()
    if meta_robots and "noindex" in meta_robots:
        results.append(failure("crawl.noindex-directive", "crawlability", "P1", 4, "Page has a noindex directive"))

    if not has_internal_links:
        results.append(failure("discoverability.missing-internal-links", "discoverability", "P2", 2, "Missing internal link pathways"))
    if is_homepage_like and len(internal_links) < 3:
        results.append(failure("discoverability.homepage-weak-discovery", "discoverability", "P2", 2, "Homepage has weak internal discovery"))
    if page_type in ("article", "docs", "product", "landing") and has_internal_links and len(internal_links) < 2:
        results.append(failure("discoverability.weak-related-navigation", "discoverability", "P2", 2, "Page has weak related-page pathways"))

    if not has_text_value(snapshot.get("metaDescription")):
        results.append(failure("meta.missing-description", "metadata", "P1", 3, "Missing meta description"))
    if not has_og_title or not has_og_desc:
        results.append(failure("meta.missing-open-graph", "metadata", "P2", 2, "Missing Open Graph metadata"))
    if len(snapshot.get("schema", [])) == 0:
        results.append(failure("meta.missing-schema", "metadata", "P1", 5, "Missing structured data"))
    if page_type == "article" and not has_schema_type(schema_types, ["Article", "BlogPosting", "NewsArticle"]):
        results.append(failure("meta.missing-article-schema", "metadata", "P1", 3, "Article page missing Article schema"))
    if page_type == "product" and not has_schema_type(schema_types, ["Product", "Service", "SoftwareApplication"]):
        results.append(failure("meta.missing-product-schema", "metadata", "P1", 3, "Product page missing Product or Service schema"))
    if (is_homepage_like or page_type == "product") and not has_schema_type(schema_types, ["Organization", "WebSite"]):
        results.append(failure("meta.missing-organization-schema", "metadata", "P2", 2, "Missing brand or site schema"))
    if page_type == "docs" and not has_schema_type(schema_types, ["HowTo", "TechArticle", "FAQPage"]):
        results.append(failure("meta.missing-docs-schema", "metadata", "P2", 2, "Documentation page missing docs-friendly schema"))

    if (is_homepage_like or page_type in ("landing", "product")) and not has_primary_entity:
        results.append(failure("entity.missing-primary-entity", "entity", "P1", 4, "Missing clear primary entity signal"))
    if page_type in ("article", "docs") and not has_content_owner:
        results.append(failure("entity.missing-content-owner", "entity", "P1", 3, "Missing clear content owner signal"))
    if page_type == "product" and not has_product_schema and len(org_names) == 0 and not has_text_value(og.get("siteName")):
        results.append(failure("entity.product-entity-ambiguous", "entity", "P2", 2, "Product page entity is ambiguous"))

    h1_list = snapshot.get("h1List", [])
    headings = snapshot.get("headings", [])
    if len(h1_list) == 0:
        results.append(failure("readability.missing-h1", "readability", "P1", 3, "Missing H1 heading"))
    if len(h1_list) > 1:
        results.append(failure("readability.multiple-h1", "readability", "P2", 2, "Multiple H1 headings"))
    if len(headings) < 3:
        results.append(failure("readability.thin-headings", "readability", "P2", 3, "Weak heading structure"))
    if avg_para_len > 600:
        results.append(failure("readability.long-paragraphs", "readability", "P2", 2, "Paragraphs are too long"))
    if not has_list_blocks and not has_step_blocks and not has_table_blocks:
        results.append(failure("readability.missing-structured-formatting", "readability", "P1", 3, "Missing structured formatting blocks"))
    if page_type == "docs" and not has_step_blocks:
        results.append(failure("readability.docs-missing-steps", "readability", "P1", 3, "Documentation page missing step-by-step structure"))
    if is_product_detail and not has_table_blocks and not text_summary.get("hasComparisonPattern"):
        results.append(failure("readability.product-missing-comparison-structure", "readability", "P2", 2, "Product page missing comparison structure"))

    has_authority = len(author_names) > 0 or len(org_names) > 0 or len(entity_signals.get("contactLinks", [])) > 0 or len(entity_signals.get("aboutLinks", [])) > 0
    if not has_authority:
        results.append(failure("trust.missing-authority-signals", "trust", "P1", 4, "Missing authority signals"))
    if is_homepage_like and not has_about_links and not has_contact_links:
        results.append(failure("trust.homepage-missing-brand-paths", "trust", "P1", 3, "Homepage missing About or Contact trust paths"))
    if page_type in ("article", "docs") and len(author_names) == 0:
        results.append(failure("trust.missing-author", "trust", "P1", 3, "Missing author attribution"))

    if page_type in ("article", "docs") and not has_text_value(entity_signals.get("publishDate")):
        results.append(failure("freshness.missing-publish-date", "freshness", "P2", 2, "Missing publish date"))
    if page_type in ("article", "docs") and not has_text_value(entity_signals.get("modifiedDate")):
        results.append(failure("freshness.missing-modified-date", "freshness", "P2", 1, "Missing updated date"))
    if page_type in ("article", "docs") and ref_age is not None and ref_age > 365:
        results.append(failure("freshness.stale-reference-content", "freshness", "P1", 3, "Reference content looks stale", {"ageInDays": ref_age}))

    if not has_external_links and page_type in ("article", "docs"):
        results.append(failure("citation.missing-source-links", "citation", "P1", 3, "Missing external citations or references"))
    if page_type in ("article", "product", "docs") and not has_quote_blocks and not has_def_blocks and not has_faq_blocks and not has_table_blocks and not text_summary.get("hasCitationPattern"):
        results.append(failure("citation.missing-citable-structure", "citation", "P2", 2, "Missing citation-friendly content blocks"))

    if not text_summary.get("hasDefinitionPattern"):
        results.append(failure("answerability.missing-definition", "answerability", "P1", 4, "Missing answer-style definition"))
    if page_type == "landing" and not text_summary.get("hasDefinitionPattern") and not has_def_blocks:
        results.append(failure("answerability.landing-unclear-value-prop", "answerability", "P1", 3, "Landing page lacks a clear value proposition"))
    if not has_def_blocks and not text_summary.get("hasSummaryLead"):
        results.append(failure("answerability.missing-summary-intro", "answerability", "P1", 3, "Missing strong summary intro"))
    if not text_summary.get("hasFaqPattern") and not text_summary.get("hasStepsPattern") and not text_summary.get("hasComparisonPattern") and not text_summary.get("hasUseCasePattern") and not text_summary.get("hasPitfallPattern"):
        results.append(failure("answerability.missing-structured-blocks", "answerability", "P1", 3, "Missing structured answer blocks"))
    if page_type in ("article", "docs",) or is_product_detail:
        if not has_faq_blocks:
            results.append(failure("answerability.missing-faq", "answerability", "P2", 2, "Missing FAQ block"))
    if not has_quote_blocks and not has_def_blocks and not text_summary.get("hasQuotableSnippet"):
        results.append(failure("answerability.missing-quotable-snippets", "answerability", "P1", 3, "Missing quotable answer snippets"))
    if is_product_detail and not text_summary.get("hasComparisonPattern") and not has_faq_blocks and not text_summary.get("hasUseCasePattern"):
        results.append(failure("answerability.product-missing-buyer-qa", "answerability", "P1", 3, "Product page missing buyer Q&A cues"))
    if page_type == "docs" and not has_step_blocks and not has_faq_blocks and not text_summary.get("hasPitfallPattern") and not text_summary.get("hasPrecautionPattern"):
        results.append(failure("answerability.docs-missing-task-guidance", "answerability", "P1", 3, "Documentation page missing task-oriented guidance"))

    visible_len = int(text_summary.get("visibleTextLength", 0))
    if visible_len < 800:
        results.append(failure("content.thin-content", "content", "P1", 4, "Thin page content"))
    elif 800 <= visible_len < 1400:
        results.append(failure("content.light-depth", "content", "P2", 2, "Content depth is still light"))
    if not has_table_blocks and not has_list_blocks and not has_step_blocks and page_type != "homepage":
        results.append(failure("content.missing-supporting-structure", "content", "P2", 2, "Missing supporting content structure"))
    if page_type == "article" and visible_len < 1200:
        results.append(failure("content.article-light-depth", "content", "P2", 2, "Article content depth is light"))
    if is_product_detail and visible_len < 1000:
        results.append(failure("content.product-light-detail", "content", "P2", 2, "Product page lacks enough detail"))
    if page_type == "docs" and visible_len < 1000:
        results.append(failure("content.docs-light-depth", "content", "P2", 2, "Documentation page needs more depth"))
    if is_product_list and visible_len < 500:
        results.append(failure("content.product-light-detail", "content", "P2", 1, "Product listing page lacks enough category context"))
    if is_homepage_like and visible_len < 500:
        results.append(failure("content.homepage-thin-messaging", "content", "P2", 2, "Homepage messaging is too thin"))

    return results


# ----------------------------------------------------------------------------
# 评分 / 汇总
# ----------------------------------------------------------------------------

def build_issue(result):
    copy = ISSUE_COPY.get(result["ruleKey"], {
        "summary": "A GEO issue was detected on this page.",
        "whyItMatters": "This issue reduces machine understanding or citation readiness.",
        "fixSuggestion": "Review the affected section and strengthen its machine-readable signals.",
        "example": None,
        "estimatedGain": None,
    })
    issue = {
        "id": f"{result['ruleKey']}:{result['dimension']}",
        "ruleKey": result["ruleKey"],
        "title": result["title"],
        "dimension": result["dimension"],
        "priority": result["priority"],
        "scoreImpact": result["scoreImpact"],
        "summary": copy["summary"],
        "whyItMatters": copy["whyItMatters"],
        "fixSuggestion": copy["fixSuggestion"],
        "example": copy["example"],
        "estimatedGain": copy["estimatedGain"],
    }
    if "evidence" in result:
        issue["evidence"] = result["evidence"]
    return issue


PRIORITY_WEIGHT = {"P0": 3, "P1": 2, "P2": 1}


def sort_issues(issues):
    return sorted(issues, key=lambda i: (PRIORITY_WEIGHT.get(i["priority"], 0), i["scoreImpact"]), reverse=True)


def compute_grade(score):
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def score_status(score, max_score):
    ratio = (score / max_score) if max_score else 0
    if ratio >= 0.8:
        return "good"
    if ratio >= 0.55:
        return "warning"
    return "critical"


def infer_dimension_status(score, max_score):
    ratio = (score / max_score) if max_score else 0
    if ratio >= 0.7:
        return "good"
    if ratio >= 0.4:
        return "warning"
    return "critical"


def format_ai_visibility_level(score):
    if score >= 85:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


def format_ai_visibility_summary(score):
    if score >= 85:
        return "AI 可见度较强，页面更容易被发现、理解和引用。"
    if score >= 60:
        return "AI 可见度中等，建议继续补足引用性与回答能力。"
    return "AI 可见度偏弱，建议优先补结构、引用性和答案式内容。"


def analyze_html(html_text, url="", options=None):
    options = options or {}
    snapshot = create_snapshot_from_html(html_text, url)
    raw_issues = run_rules(snapshot)
    issues = [build_issue(r) for r in sort_issues(raw_issues)]

    dims = {}
    for key, cfg in DIMENSION_CONFIG.items():
        dim_issues = [i for i in issues if i["dimension"] == key]
        penalty = sum(int(i["scoreImpact"]) for i in dim_issues)
        capped = min(cfg["maxScore"], penalty)
        score = max(0, cfg["maxScore"] - capped)
        dims[key] = {
            "key": key,
            "label": cfg["label"],
            "label_cn": cfg["label_cn"],
            "score": score,
            "maxScore": cfg["maxScore"],
            "percentScore": round(score / cfg["maxScore"] * 100),
            "issueCount": len(dim_issues),
            "status": score_status(score, cfg["maxScore"]),
        }

    total_score = sum(d["score"] for d in dims.values())
    grade = compute_grade(total_score)

    # AI 可见度：discoverability + citation + answerability 的百分制均值
    def pct(k):
        return dims[k]["percentScore"]
    visibility_score = round((pct("discoverability") + pct("citation") + pct("answerability")) / 3)

    # GEO 六维评分
    def block_avg(keys):
        return round(sum(pct(k) for k in keys) / len(keys))
    geo_score_block = {
        "title": "GEO 六维评分",
        "dimensions": [
            {"key": "content", "label": "内容结构", "score": block_avg(["content", "readability"])},
            {"key": "metadata", "label": "结构化数据", "score": pct("metadata")},
            {"key": "ai_visibility", "label": "AI 可见度", "score": block_avg(["discoverability", "citation"])},
            {"key": "freshness", "label": "内容新鲜度", "score": pct("freshness")},
            {"key": "brand_consistency", "label": "品牌一致性", "score": block_avg(["entity", "trust"])},
            {"key": "answerability", "label": "问答覆盖度", "score": pct("answerability")},
        ],
    }

    # 最强/最弱维度
    def ratio(d):
        return d["score"] / d["maxScore"]
    strongest = max(dims.values(), key=lambda d: (ratio(d), -d["issueCount"], d["score"]))
    weakest = min(dims.values(), key=lambda d: (ratio(d), d["issueCount"], -d["score"]))
    top_priorities = [i["title"] for i in issues[:3]]
    one_liner = ("该页面 GEO 基础信号较强，可进入更深层的 AI 分析。" if not issues
                 else f"该页面存在 {len(issues)} 个 GEO 问题，最大缺口在 {weakest['label_cn']}。")

    ai_visibility = {
        "score": visibility_score,
        "level": format_ai_visibility_level(visibility_score),
        "summary": format_ai_visibility_summary(visibility_score),
        "signals": [
            {"key": "discoverability", "label": "可发现性", "score": pct("discoverability")},
            {"key": "citation", "label": "可引用性", "score": pct("citation")},
            {"key": "answerability", "label": "可回答性", "score": pct("answerability")},
        ],
    }

    report = {
        "url": snapshot["url"],
        "title": snapshot["title"],
        "pageType": snapshot["pageTypeHint"],
        "pageRole": snapshot["pageRoleHint"],
        "totalScore": total_score,
        "grade": grade,
        "maxScore": 100,
        "dimensions": list(dims.values()),
        "dimension_scores": {k: d["score"] for k, d in dims.items()},
        "aiVisibility": ai_visibility,
        "geoScoreBlock": geo_score_block,
        "issues": issues,
        "topIssues": issues[:3],
        "summary": {
            "oneLiner": one_liner,
            "strongestArea": strongest["key"],
            "weakestArea": weakest["key"],
            "topPriorities": top_priorities,
        },
        "_snapshot": snapshot,  # 仅供内部 plan/optimize 复用
    }
    return report


# ----------------------------------------------------------------------------
# 兼容层：从 snapshot 推导旧版 analysis（供 optimize/plan 复用既有逻辑）
# ----------------------------------------------------------------------------

def snapshot_to_analysis(snapshot):
    all_text = strip_tags(_reconstruct_simple(snapshot))
    org_names = snapshot["entitySignals"]["organizationNames"]
    author_names = snapshot["entitySignals"]["authorNames"]
    schema_types = [tp for b in snapshot["schema"] for tp in b["parsedTypes"]]
    headings = snapshot["headings"]
    intent_questions = []
    # 从标题与可见文本抽取问句
    sample = " ".join(h["text"] for h in headings)
    for m in QUESTION_RE.findall(sample) + EN_QUESTION_RE.findall(sample):
        intent_questions.append(m.strip())

    industry_scores = {}
    for ind, kws in INDUSTRY_LEXICON.items():
        s = sum(all_text.count(k) for k in kws)
        if s > 0:
            industry_scores[ind] = s
    industry_ranked = sorted(industry_scores.items(), key=lambda x: -x[1])

    # 知识覆盖
    covered, missing = [], []
    low = all_text.lower()
    for label, kws in GEO_TOPIC_CHECKLIST:
        if any(k.lower() in low for k in kws):
            covered.append(label)
        else:
            missing.append(label)

    has_faq_schema = has_schema_type(schema_types, ["FAQPage"])
    has_product_schema = has_schema_type(schema_types, ["Product", "Service", "SoftwareApplication"])
    has_brand_schema = has_schema_type(schema_types, ["Organization", "WebSite", "Brand"])

    return {
        "enterprise": {
            "detected_names": org_names[:10],
            "name_count": len(org_names),
            "icp": ICP_RE.findall(all_text)[:5],
            "has_about_page": bool(re.search(r"(关于我们|公司简介|企业简介|about us)", all_text, re.I)),
            "clarity": "clear" if (len(org_names) >= 1 and re.search(r"(关于我们|公司简介|企业简介|about us)", all_text, re.I)) else ("partial" if org_names else "missing"),
        },
        "brand": {
            "brand_names": (snapshot["entitySignals"]["organizationNames"][:5] or [snapshot["openGraph"].get("siteName", "")]),
            "title_brand": [snapshot["title"]],
            "logos": [],
            "trademark_symbols": len(TM_RE.findall(all_text)),
            "has_explicit_brand": bool(snapshot["openGraph"].get("siteName") or org_names),
            "clarity": "clear" if (snapshot["openGraph"].get("siteName") or org_names) else "missing",
        },
        "products": {
            "detected": [snapshot.get("title", "")] if has_product_schema else [],
            "count": 1 if has_product_schema else 0,
            "has_price_signal": bool(PRICE_RE.search(all_text)),
            "has_product_schema": has_product_schema,
        },
        "services": {
            "keyword_hits": [k for k in SERVICE_KW if k in all_text],
            "has_service_schema": has_schema_type(schema_types, ["Service"]),
            "service_headings": [h["text"] for h in headings if any(k in h["text"] for k in SERVICE_KW)][:15],
            "detected": bool(any(k in all_text for k in SERVICE_KW)) or has_schema_type(schema_types, ["Service"]),
        },
        "industry": {
            "ranked": industry_ranked[:5],
            "top": industry_ranked[0][0] if industry_ranked else None,
            "second": industry_ranked[1][0] if len(industry_ranked) > 1 else None,
        },
        "target_market": {
            "langs": [snapshot["lang"]] if snapshot["lang"] else [],
            "primary": None,
        },
        "intent": {
            "questions": intent_questions[:30],
            "question_count": len(intent_questions),
            "intent_distribution": {},
            "candidate_queries": [h["text"] for h in headings if h["level"] <= 2 and 4 < len(h["text"]) < 40][:20],
        },
        "knowledge_coverage": {
            "covered": covered,
            "missing": missing,
            "coverage_ratio": round(len(covered) / len(GEO_TOPIC_CHECKLIST), 2),
        },
        "credibility": {
            "score": 70 if (author_names or org_names) else 40,
            "signals": {
                "has_author": bool(author_names),
                "has_dates": bool(snapshot["entitySignals"]["publishDate"] or snapshot["entitySignals"]["modifiedDate"]),
                "has_references_section": bool(re.search(r"(参考文献|资料来源|引用|reference|来源：|数据来源)", all_text, re.I)),
                "has_contact": bool(snapshot["entitySignals"]["contactLinks"]),
                "has_privacy": bool(re.search(r"(隐私政策|隐私条款|privacy|terms)", all_text, re.I)),
            },
        },
        "structured_data": {
            "types_found": sorted(set(schema_types)),
            "recommended": ["Organization", "WebSite", "FAQPage", "Product", "Service", "BreadcrumbList", "Article"],
            "present": [t for t in ["Organization", "WebSite", "FAQPage", "Product", "Service", "BreadcrumbList", "Article"] if has_schema_type(schema_types, [t])],
            "missing": [t for t in ["Organization", "WebSite", "FAQPage", "Product", "Service", "BreadcrumbList", "Article"] if not has_schema_type(schema_types, [t])],
            "coverage_ratio": round(len([t for t in ["Organization", "WebSite", "FAQPage", "Product", "Service", "BreadcrumbList", "Article"] if has_schema_type(schema_types, [t])]) / 7, 2),
            "microdata_or_rdfa": bool(re.search(r'itemscope|itemtype=|vocab="http://schema.org|property="[a-z]+:[a-z]+"', all_text, re.I)),
        },
        "faq": {
            "has_faq_schema": has_faq_schema,
            "schema_pairs": 0,
            "onpage_question_count": len(intent_questions),
            "sample_pairs": [],
        },
        "citations": {
            "external_link_count": len([l for l in snapshot["links"] if l.get("isExternal")]),
            "authoritative_count": len([l for l in snapshot["links"] if l.get("isExternal") and re.search(r"\.(edu|gov)(\.[a-z]{2})?/|wikipedia\.org|doi\.org", l["href"], re.I)]),
            "has_reference_section": bool(re.search(r"(参考文献|资料来源|引用|reference|来源：|数据来源)", all_text, re.I)),
        },
        "_brand_schema": has_brand_schema,
    }


def _reconstruct_simple(snapshot):
    """用快照内的文本近似还原可见文本（供兼容层关键词统计）。"""
    parts = [snapshot.get("title", "")]
    for b in snapshot.get("contentBlocks", []):
        if b.get("type") in ("paragraph", "list", "table", "quote", "definition"):
            parts.append(b.get("text", ""))
    return " ".join(parts)


# ----------------------------------------------------------------------------
# 生成优化方案（Stage 15）：基于 issues（P1→high, P2→medium）
# ----------------------------------------------------------------------------

def build_plan_from_report(report):
    sug = []
    for issue in report["issues"]:
        impact = "high" if issue["priority"] == "P1" else "medium"
        sug.append({
            "dimension": issue["dimension"],
            "impact": impact,
            "ruleKey": issue["ruleKey"],
            "issue": issue["title"],
            "recommendation": issue["fixSuggestion"],
            "fix": issue.get("example") or "",
            "estimatedGain": issue.get("estimatedGain") or "",
        })
    return sug


# ----------------------------------------------------------------------------
# 自动优化（Stage 16）：产出可粘贴片段（复用旧版 optimize 逻辑）
# ----------------------------------------------------------------------------

def build_optimizations(analysis, url=""):
    a = analysis
    org_name = (a["enterprise"]["detected_names"] or a["brand"]["brand_names"] or ["YOUR_COMPANY"])[0] or "YOUR_COMPANY"
    site_name = (a["brand"]["brand_names"] or [org_name])[0] or org_name
    logo = ""
    page_url = url

    blocks = {}
    blocks["Organization"] = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": org_name,
        "url": page_url,
        "logo": logo,
    }
    if a["enterprise"]["icp"]:
        blocks["Organization"]["identifier"] = "ICP " + a["enterprise"]["icp"][0]
    blocks["WebSite"] = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_name,
        "url": page_url,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{page_url}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }
    if page_url:
        parts = [p for p in urllib.parse.urlparse(page_url).path.split("/") if p]
        if parts:
            crumbs = [{"@type": "ListItem", "position": i + 1,
                       "name": urllib.parse.unquote(p),
                       "item": page_url.rsplit("/", 1)[0] + "/" + "/".join(parts[:i + 1]) + "/"}
                      for i, p in enumerate(parts)]
        else:
            crumbs = [{"@type": "ListItem", "position": 1, "name": site_name, "item": page_url}]
        blocks["BreadcrumbList"] = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}

    qs = a["intent"]["questions"][:10]
    if qs:
        blocks["FAQPage"] = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": "【请在此填写该问题的权威答案】"}}
                for q in qs
            ],
        }
    if a["products"]["count"] and a["products"]["detected"]:
        blocks["Product"] = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": a["products"]["detected"][0],
            "description": "【产品描述】",
            "brand": {"@type": "Brand", "name": site_name},
        }

    all_ld = list(blocks.values())
    html_snippet = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(b, ensure_ascii=False, indent=2)}\n</script>'
        for b in all_ld
    )
    meta_suggestions = [
        f'<title>{site_name} | {a["industry"]["top"] or "专业服务"}</title>',
        f'<meta name="description" content="【一句话说明 {org_name} 的核心业务与差异化】">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{site_name}">',
    ]
    return {
        "organization_name": org_name,
        "json_ld_blocks": blocks,
        "html_snippet": html_snippet,
        "meta_suggestions": meta_suggestions,
        "note": "自动生成的 JSON-LD 为骨架，含【】占位处需人工补全真实数据；禁止编造价格/评分/作者等事实。",
    }


# ----------------------------------------------------------------------------
# 验证（Stage 17）
# ----------------------------------------------------------------------------

def validate(baseline_report, current_report):
    b = baseline_report.get("geo_score", {})
    c = current_report.get("geo_score", {})
    bd = b.get("dimension_scores", {})
    cd = c.get("dimension_scores", {})
    delta = {
        "geo_score": round(c.get("geo_score", 0) - b.get("geo_score", 0), 1),
        "dimensions": {k: round(cd.get(k, 0) - bd.get(k, 0), 1) for k in bd},
    }
    baseline_sug = len(baseline_report.get("suggestions", []))
    current_sug = len(current_report.get("suggestions", []))
    return {
        "baseline_geo_score": b.get("geo_score"),
        "current_geo_score": c.get("geo_score"),
        "delta": delta,
        "baseline_suggestions": baseline_sug,
        "current_suggestions": current_sug,
        "resolved": max(0, baseline_sug - current_sug),
        "verdict": "improved" if delta["geo_score"] > 0 else ("unchanged" if delta["geo_score"] == 0 else "regressed"),
    }


# ----------------------------------------------------------------------------
# 加载源（URL / 文件 / crawl 目录）
# ----------------------------------------------------------------------------

def load_html_from_url(url, max_pages=1, depth=1, delay=DELAY_FLOOR):
    manifest = crawl(url, max_pages=max_pages, depth=depth, delay=delay, out_dir="_geo_tmp")
    for p in manifest["pages"]:
        if p.get("saved") and os.path.exists(p["saved"]):
            with open(p["saved"], "r", encoding="utf-8") as f:
                return f.read(), p["url"]
    return "", url


def load_html_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read(), file_path


def load_html_from_crawldir(crawl_dir):
    mpath = os.path.join(crawl_dir, "manifest.json")
    if not os.path.exists(mpath):
        raise SystemExit(f"未找到清单：{mpath}")
    with open(mpath, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    pages = manifest.get("pages", [])
    for p in pages:
        if p.get("saved") and os.path.exists(p["saved"]):
            with open(p["saved"], "r", encoding="utf-8") as f:
                return f.read(), p["url"]
    return "", manifest.get("start_url", "")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def cmd_crawl(args):
    manifest = crawl(args.url, max_pages=args.max_pages, depth=args.depth, delay=max(DELAY_FLOOR, args.delay))
    out = args.out or os.path.join("geo_crawl", "manifest.json")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[crawl] 抓取 {len([p for p in manifest['pages'] if p.get('saved')])} 页 -> {out}")


def cmd_analyze(args):
    if args.url:
        html_text, src = load_html_from_url(args.url, max_pages=args.max_pages, depth=args.depth, delay=args.delay)
    elif args.file:
        html_text, src = load_html_from_file(args.file)
    elif args.crawldir:
        html_text, src = load_html_from_crawldir(args.crawldir)
    else:
        raise SystemExit("analyze 需要 --url / --file / --crawldir 之一")
    if not html_text:
        raise SystemExit("未能获取页面 HTML，请检查 URL 或文件。")
    report = analyze_html(html_text, src)
    analysis = snapshot_to_analysis(report["_snapshot"])
    geo = {
        "geo_score": report["totalScore"],
        "grade": report["grade"],
        "max_score": report["maxScore"],
        "dimensions": report["dimensions"],
        "dimension_scores": report["dimension_scores"],
        "weights": {k: v["maxScore"] for k, v in DIMENSION_CONFIG.items()},
        "ai_visibility": report["aiVisibility"],
        "geo_score_block": report["geoScoreBlock"],
    }
    suggestions = build_plan_from_report(report)
    site_block = {
        "url": report["url"],
        "title": report["title"],
        "page_type": report["pageType"],
        "page_role": report["pageRole"],
        "page_count": 1,
        "total_chars": report["_snapshot"]["textSummary"]["visibleTextLength"],
    }
    out = args.out or "geo_report.json"
    final = {
        "site": site_block,
        "analysis": analysis,
        "geo_score": geo,
        "suggestions": suggestions,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    print(f"[analyze] GEO Score={report['totalScore']}/100  Grade={report['grade']}  AI可见度={report['aiVisibility']['level']}({report['aiVisibility']['score']})")
    dims_str = ", ".join(f"{d['key']}={d['score']}" for d in report["dimensions"])
    print(f"[analyze] 十维：{dims_str}")
    print(f"[analyze] 优化建议 {len(suggestions)} 条 -> {out}")


def cmd_plan(args):
    with open(args.report, "r", encoding="utf-8") as f:
        report = json.load(f)
    sug = report.get("suggestions")
    if not sug:
        # 无 suggestions 但有 raw geo，尝试从 issues 重建：需要原始 html，这里提示用户重跑 analyze
        raise SystemExit("report 缺少 suggestions，请用 analyze 重新生成（含 --file/--url 源）")
    print(f"[plan] 共 {len(sug)} 条 GEO 优化建议：")
    for s in sug:
        print(f"  [{s['impact'].upper()}] {s['dimension']}: {s['issue']}")
        print(f"      建议：{s['recommendation']}")


def cmd_optimize(args):
    with open(args.report, "r", encoding="utf-8") as f:
        report = json.load(f)
    if "analysis" not in report:
        raise SystemExit("report 缺少 analysis，请用 analyze 重新生成")
    url = report.get("site", {}).get("url", "") if isinstance(report.get("site"), dict) else ""
    res = build_optimizations(report["analysis"], url)
    out = args.out or "geo_optimizations.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print(f"[optimize] 已生成 JSON-LD / meta 片段 -> {out}")
    print(f"[optimize] 组织名：{res['organization_name']}；含 {len(res['json_ld_blocks'])} 个 schema 块")


def cmd_validate(args):
    with open(args.baseline, "r", encoding="utf-8") as f:
        base = json.load(f)
    with open(args.current, "r", encoding="utf-8") as f:
        cur = json.load(f)
    v = validate(base, cur)
    print(f"[validate] 基线 {v['baseline_geo_score']} -> 当前 {v['current_geo_score']}（Δ{v['delta']['geo_score']}）")
    print(f"[validate] 建议数 {v['baseline_suggestions']} -> {v['current_suggestions']}，已解决 {v['resolved']}")
    print(f"[validate] 结论：{v['verdict']}")


def main():
    ap = argparse.ArgumentParser(description="GEO 体检与优化流水线")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("crawl", help="网站抓取")
    p.add_argument("--url", required=True)
    p.add_argument("--max-pages", type=int, default=30)
    p.add_argument("--depth", type=int, default=3)
    p.add_argument("--delay", type=float, default=DELAY_FLOOR)
    p.add_argument("--out", default="geo_crawl/manifest.json")
    p.set_defaults(func=cmd_crawl)

    p = sub.add_parser("analyze", help="GEO 全维度分析 + 十维评分")
    p.add_argument("--url")
    p.add_argument("--file")
    p.add_argument("--crawldir")
    p.add_argument("--max-pages", type=int, default=1)
    p.add_argument("--depth", type=int, default=1)
    p.add_argument("--delay", type=float, default=DELAY_FLOOR)
    p.add_argument("--out", default="geo_report.json")
    p.set_defaults(func=cmd_analyze)

    p = sub.add_parser("plan", help="生成 GEO 优化方案")
    p.add_argument("--report", required=True)
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("optimize", help="自动优化产出片段")
    p.add_argument("--report", required=True)
    p.add_argument("--out", default="geo_optimizations.json")
    p.set_defaults(func=cmd_optimize)

    p = sub.add_parser("validate", help="验证优化效果")
    p.add_argument("--baseline", required=True)
    p.add_argument("--current", required=True)
    p.set_defaults(func=cmd_validate)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
