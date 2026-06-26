---
name: adaptive-web-analyzer
description: 通过指定接口获取网页内容，自适应抓取解析关键文本，并使用大模型进行智能梳理总结
version: 1.0.0
permissions: ["web.fetch", "web.scrape", "llm.chat", "file.write", "system.exec"]
author: your-name
tags: ["web-scraping", "content-analysis", "ai-summarization", "adaptive-parsing"]
---

## 功能概述

当用户需要获取网页内容并进行智能分析时，本技能将：
1. 通过用户指定的API接口或URL获取原始网页内容
2. 使用自适应解析器提取关键文本（自动处理反爬、动态渲染、布局变化）
3. 将提取的文本发送给大模型进行结构化梳理和总结
4. 返回格式化的分析报告

## 触发场景

用户输入包含以下意图时触发：
- "抓取[某网址]的内容并分析"
- "获取[API接口]的数据并整理"
- "分析网页[URL]的关键信息"
- "爬取[网站]并用AI总结"
- "提取[链接]的文本并梳理"

## 执行流程

### 步骤1: 获取网页内容
- 如果用户提供的是API接口：使用HTTP客户端发送请求（支持自定义Headers、Auth）
- 如果用户提供的是普通URL：使用自适应浏览器抓取（处理JavaScript渲染、反爬机制）
- 支持配置：超时时间、重试次数、User-Agent轮换、代理设置

### 步骤2: 自适应内容解析
使用以下策略提取关键文本：
- **智能选择器**：基于内容相似度算法，自动定位正文区域（抗布局变化）
- **反反爬处理**：自动绕过Cloudflare等基础防护（遵守robots.txt）
- **动态渲染**：对SPA应用使用Playwright等待关键元素加载
- **噪声过滤**：自动去除广告、导航栏、页脚等非内容元素
- **多格式支持**：HTML、JSON API响应、Markdown页面

### 步骤3: 内容结构化
提取的文本按以下维度组织：
- 标题/主题
- 关键段落（按重要性排序）
- 列表/表格数据
- 时间戳/元数据
- 链接引用

### 步骤4: 大模型智能梳理
将结构化文本发送给LLM，执行以下分析：
- **摘要生成**：生成3-5句话的核心摘要
- **要点提取**：列出3-7个关键要点
- **分类标签**：自动标注内容类别（技术/新闻/产品/学术等）
- **情感分析**：判断内容倾向（积极/中性/消极）
- **实体识别**：提取人名、组织、产品、地点等关键实体
- **行动建议**：根据内容类型提供后续建议（如需要）

### 步骤5: 输出格式化
返回包含以下字段的JSON/Markdown报告：
```json
{
  "source_url": "原始链接",
  "fetch_time": "抓取时间",
  "content_stats": {
    "total_chars": "总字符数",
    "extracted_chars": "提取字符数",
    "confidence_score": "抓取置信度"
  },
  "analysis": {
    "summary": "AI生成的摘要",
    "key_points": ["要点1", "要点2", "要点3"],
    "category": "内容分类",
    "sentiment": "情感倾向",
    "entities": {
      "persons": ["人物名"],
      "organizations": ["组织名"],
      "products": ["产品名"]
    },
    "suggested_actions": ["建议操作1", "建议操作2"]
  },
  "raw_content_preview": "原始内容前500字（可选）"
}