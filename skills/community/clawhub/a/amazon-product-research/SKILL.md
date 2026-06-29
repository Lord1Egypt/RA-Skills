---
name: amazon-product-research
description: "Amazon 产品全链路深度研究助手。输入一句话（产品名/ASIN/描述），自动完成产品搜索→多产品评论采集→AI情感打标→关键词扩展→VOC痛点聚类→竞品分析→新品机会分析→输出完整交互式HTML可视化报告。覆盖8大分析阶段，一站式Amazon产品调研。"
author: "WorkBuddy"
version: "1.0.1"
triggers:
  - "amazon-product-research"
  - "亚马逊产品研究"
  - "亚马逊产品分析"
  - "Amazon产品调研"
  - "选品分析"
  - "竞品分析"
  - "产品研究"
  - "market research"
agent_created: true
---

# 亚马逊产品研究员 (Amazon Product Research)

一句话描述，8步输出完整调研报告——竞品、关键词、痛点、机会，一个工具搞定。

## 能做什么

输入一句话（产品名/ASIN/描述词），自动完成：

1. 🔍 **产品搜索**：自然语言搜索Amazon产品，返回Top N竞品
2. 📝 **多产品评论采集**：批量抓取每个产品的用户评论
3. 🤖 **AI情感打标**：逐条评论提取情感/痛点/卖点/场景/画像
4. 🔑 **关键词扩展**：基于真实评论，生成高频搜索词、长尾词、关联词
5. 🎯 **VOC痛点聚类**：聚类用户痛点，按严重度和频率排序
6. 📊 **竞品分析**：多产品横向对比，优劣矩阵+市场定位
7. 💡 **新品机会分析**：识别市场空白，推荐新品切入方向
8. 📄 **交互式HTML报告**：一键生成完整可视化报告

## 与其他技能对比

| 功能 | amazon-review-analyzer | **amazon-product-research** |
|------|----------------------|---------------------------|
| 输入方式 | 必须指定ASIN | **一句话自然语言** |
| 分析范围 | 单个产品 | **多产品横向对比** |
| 关键词扩展 | ❌ | ✅ |
| VOC聚类 | ❌ | ✅ |
| 竞品分析 | 基础 | **深度横向对比** |
| 新品机会 | ❌ | ✅ |
| 报告类型 | 单产品洞察 | **全链路调研报告** |

## 快速开始

### 1. 安装依赖

```bash
pip install -r ~/.workbuddy/skills/amazon-product-research/requirements.txt
```

### 2. 体验示例报告（无需API Key）

```bash
python ~/.workbuddy/skills/amazon-product-research/scripts/research.py \
  --query "bluetooth headphones under $50" \
  --use-mock
```

### 3. 完整分析（需LLM API Key）

```bash
# DeepSeek（国内推荐）
python ~/.workbuddy/skills/amazon-product-research/scripts/research.py \
  --query "portable bluetooth speaker waterproof" \
  --api-key YOUR_DEEPSEEK_KEY \
  --api-base https://api.deepseek.com/v1 \
  --model deepseek-chat

# OpenAI
python ~/.workbuddy/skills/amazon-product-research/scripts/research.py \
  --query "yoga mat non slip" \
  --api-key YOUR_OPENAI_KEY
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--query` | ✅ | - | 搜索关键词/产品名/ASIN/描述 |
| `--market` | ❌ | US | 市场区域：US/UK/DE/JP等 |
| `--max-products` | ❌ | 5 | 最多分析的竞品数量 |
| `--max-reviews` | ❌ | 100 | 每个产品最大评论数 |
| `--api-key` | ❌ | - | LLM API Key（无Key则仅生成数据报告） |
| `--api-base` | ❌ | https://api.openai.com/v1 | API Base URL |
| `--model` | ❌ | gpt-4o-mini | 模型名称 |
| `--output` | ❌ | ./product_research_{timestamp}.html | 输出路径 |
| `--rapidapi-key` | ❌ | - | RapidAPI Key（可选） |
| `--use-mock` | ❌ | False | 使用模拟数据演示 |

## 输出报告内容

生成的HTML报告包含以下8大板块：

1. **研究概览**：搜索词、分析产品数、评论总数、评分分布总览
2. **产品一览**：所有产品卡片（图片/价格/评分/链接）
3. **评分与评论概览**：评分分布、情感分布、评论量对比
4. **关键词扩展**：高频词云、长尾关键词、关联搜索词
5. **VOC痛点聚类**：痛点分类树、严重度排序、典型评论引用
6. **竞品对比矩阵**：多维度雷达图对比、优劣势一览表
7. **新品机会分析**：市场空白识别、切入方向建议、风险提示
8. **原始数据导出**：所有打标数据可下载（CSV格式）

## 技术架构

```
用户输入 "portable bluetooth speaker waterproof"
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 1: 产品搜索 (product_search.py)            │
│  自然语言 → Amazon搜索 → Top N产品              │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 2: 多产品评论采集 (fetch_reviews.py)       │
│  对每个ASIN并行抓取评论                          │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 3: AI情感打标 (ai_tagging.py)              │
│  逐条评论 → 情感/痛点/卖点/场景/画像             │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 4: 关键词扩展 (keyword_expansion.py)       │
│  聚合评论 + LLM → 高频词/长尾词/关联词          │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 5: VOC聚类 (voc_clustering.py)             │
│  所有痛点 → LLM聚类 → 类别/严重度/频次          │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 6: 竞品分析 (competitor_analysis.py)       │
│  多产品横向对比 + LLM → 优劣矩阵/定位分析        │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 7: 新品机会 (opportunity_analysis.py)      │
│  VOC + 竞品差距 → LLM → 市场空白/新品方向        │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Stage 8: 报告生成 (generate_report.py)           │
│  全部数据 → 交互式HTML + Chart.js图表            │
└─────────────────────────────────────────────────┘
```

## API Key 配置

### LLM API（核心分析引擎）
支持任何兼容OpenAI API格式的模型：

**OpenAI**
```
--api-key sk-xxx --api-base https://api.openai.com/v1 --model gpt-4o-mini
```

**DeepSeek（国内推荐）**
```
--api-key sk-xxx --api-base https://api.deepseek.com/v1 --model deepseek-chat
```

**DashScope（阿里云）**
```
--api-key sk-xxx --api-base https://dashscope.aliyuncs.com/compatible-mode/v1 --model qwen-plus
```

### RapidAPI Key（可选）
用于获取真实Amazon数据。内置演示数据，无需Key即可体验流程。

1. 访问 https://rapidapi.com/hub/amazon
2. 订阅 "Amazon Products and Reviews" API
3. 通过 `--rapidapi-key` 参数传入

## 注意事项

- ⏱️ **时间成本**：5产品×100评论 ≈ 10-20分钟（取决于LLM API速度）
- 💰 **API成本**：gpt-4o-mini处理500条评论+4次综合分析 ≈ $0.25-0.50
- 🚫 **数据源**：真实数据依赖RapidAPI，无Key时使用模拟数据演示
- 📊 **报告大小**：HTML报告约500KB-2MB（含Chart.js图表）

## 示例

**分析"portable bluetooth speaker waterproof"市场**
```bash
python ~/.workbuddy/skills/amazon-product-research/scripts/research.py \
  --query "portable bluetooth speaker waterproof" \
  --market US \
  --max-products 5 \
  --max-reviews 100 \
  --api-key YOUR_KEY \
  --api-base https://api.deepseek.com/v1 \
  --model deepseek-chat
```

**快速调研"yoga mat"品类（使用模拟数据）**
```bash
python ~/.workbuddy/skills/amazon-product-research/scripts/research.py \
  --query "yoga mat non slip" \
  --use-mock
```

## 常见问题

**Q: 和amazon-review-analyzer有什么区别？**
A: amazon-review-analyzer专注**单个ASIN的评论分析**（痛点/卖点/Listing优化），amazon-product-research做**全链路产品调研**（搜索→竞品→关键词→VOC→机会），适合选品调研和品类分析。

**Q: 没有RapidAPI Key能用吗？**
A: 可以！使用 `--use-mock` 参数，系统会生成逼真的模拟数据，让你体验完整流程。只有获取真实Amazon数据时才需要RapidAPI Key。

**Q: 分析一个品类大概需要多久？**
A: 使用模拟数据约30秒（含报告生成），使用真实API+LLM分析5产品×100评论约10-20分钟，取决于LLM API的并发能力。

**Q: 报告能用手机看吗？**
A: 可以，HTML报告是响应式设计，手机和平板都能正常查看。推荐桌面端查看以获得最佳体验。

## 更新日志

- **v1.0.0** (2026-06-20): 初始版本
  - 8阶段全链路分析
  - 自然语言搜索
  - 多产品横向对比
  - VOC聚类 + 新品机会分析
  - 交互式HTML报告
