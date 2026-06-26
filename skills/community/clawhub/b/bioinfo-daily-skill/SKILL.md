---
name: bioinfo-daily
description: 每日生物信息学与肿瘤学研究进展日报生成器。使用 PubMed API 自动搜索前一天的 CNS 及 Nature Index 期刊文献，筛选生物信息学、肿瘤免疫、单细胞测序、空间转录组等领域的高影响力研究，生成包含中文亮点介绍的日报。使用场景：(1) 设置定时任务每天自动获取研究进展并发送到飞书 (2) 手动查询特定日期的最新文献 (3) 为团队生成高质量研究日报。
---

# Bioinfo Daily - 生物信息学日报

## 概述

本技能使用 PubMed E-utilities API 自动搜索并汇总前一天的生物信息学和肿瘤学研究进展，聚焦 CNS（Cell/Nature/Science）及子刊、Nature Index 等高影响力期刊，每天推荐 10 篇左右重要文献，并生成中文亮点介绍。

## 功能特点

- 🔍 **自动搜索**: 使用 PubMed API 搜索前一天新增文献（限定 cancer 相关）
- 📊 **高影响力筛选**: 仅筛选 CNS 及 Nature Index 期刊
- 🎯 **精准分类**: 生物信息学、肿瘤免疫、单细胞测序、空间转录组、临床进展
- 💡 **中文亮点**: 每篇文献 30 字左右中文亮点介绍
- 📝 **智能摘要**: 日报抬头自动生成精选文章 summary
- 🔥 **智能优选**: 文章多时会自动优选创新性强、方向有区分的文章（最多10篇）
- 📰 **日报格式**: 结构化日报，便于阅读和分享

## 使用方法

### 1. 手动生成日报

```bash
python3 ~/.openclaw/workspace/skills/bioinfo-daily/scripts/pubmed_search.py
```

### 2. 查看定时任务

```bash
openclaw cron list
```

### 3. 测试搜索（特定主题）

```bash
# 编辑脚本中的 SEARCH_TOPICS 添加自定义主题
```

## 数据源

**PubMed API**: https://eutils.ncbi.nlm.nih.gov/entrez/eutils

**搜索范围**:
- 🧬 生物信息学算法与工具
- 🦠 肿瘤免疫学最新研究
- 🔬 单细胞测序技术
- 🧪 空间转录组技术
- 💊 癌症免疫治疗临床进展

**期刊筛选**:
- Nature, Science, Cell 主刊及子刊
- Nature Index 期刊
- 其他高影响力期刊（Lancet、JAMA、PNAS 等）

## 输出格式

日报包含：
1. 📅 日期和文献总数
2. 📚 每篇文献：标题、期刊、作者、亮点、链接
3. 📊 数据来源说明

## 配置

**API 配置**（使用环境变量）:
- `NCBI_EMAIL`: 你的邮箱地址
- `NCBI_API_KEY`: 你的 PubMed API Key

**获取 API Key**: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

**配置方式**（任选其一）:

方式 1 - OpenClaw 配置文件 `~/.openclaw/openclaw.json`:
```json
{
  "env": {
    "NCBI_EMAIL": "your@email.com",
    "NCBI_API_KEY": "your_api_key"
  }
}
```

方式 2 - 环境变量:
```bash
export NCBI_EMAIL="your@email.com"
export NCBI_API_KEY="your_api_key"
```

**定时任务**:
- 执行时间：每天早上 8:00（北京时间）
- 搜索范围：前一天新增文献

## 脚本

- `scripts/pubmed_search.py` - PubMed API 搜索和日报生成

## ⚠️ 安全注意事项

### 1. API Key 配置
- 必须配置 `NCBI_API_KEY` 才能使用 PubMed API
- 脚本会在缺少 API Key 时显示警告
- 获取 API Key: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

### 2. .env 文件安全
- 如果使用 `.env` 文件，只放置 NCBI 相关凭证
- 不要在同一文件放其他不相关的 secrets
- `.env` 文件已加入 `.gitignore`，不会提交到 Git

### 3. 网络活动说明
- `pubmed_search.py`: 直接调用 PubMed API（ncbi.nlm.nih.gov）
- `search_bioinfo.py`: 调用 OpenClaw 的 `web_search` 工具（会发送到配置的搜索提供商）
- 如需限制网络访问，可在隔离环境中运行

### 4. 飞书上传（如需自动发布）
- `generate_daily.sh` 引用飞书文档创建步骤
- 需要配置飞书 API 凭证才能自动上传
- 如未配置凭证，脚本会生成文件供手动上传

## 依赖

- Python 3.6+
- requests 库

## 使用示例

```bash
# 生成今日日报
cd ~/.openclaw/workspace/skills/bioinfo-daily
python3 scripts/pubmed_search.py

# 输出保存至 /tmp/bioinfo_daily_YYYYMMDD.txt
```
