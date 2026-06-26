---
name: daily-fintech-brief
description: "Review daily AI advancements and domestic banking fintech progress from tier-1 curated sources with full text inspection. Trigger words: 生成今日金融科技简报, 每日AI内参, 银行科技复盘, 金融科技简报."
metadata:
  openclaw:
    emoji: "🏦"
    capabilities:
      - id: fetch_and_summarize
        description: "自动化执行：抓取数据源 → 本地存储(仅保留7天) → 调用LLM总结 → 输出标准格式日报 → 永久保存总结文档"
      - id: save_report
        description: "将LLM总结的高质量Markdown报告持久化写入到本地文件系统（永久保留）"
    permissions:
      network: true
      filesystem: true
---

# 每日 AI 与金融科技内参深度生成指令

当触发此技能时，请严格按照以下自动化管道执行，禁止凭空幻觉。

## 🤖 核心执行管道

### Step 1: 获取数据
调用 `fetch_and_summarize` 工具。按照以下优先级获取数据：
1. **优先检查今日报告是否已存在**（`output/reports/{date}.md`）
   - 若存在 → 返回 status: "already_exists" + 报告内容，直接展示给用户
2. **若今日报告不存在，检查昨日是否有原始数据**
   - 若昨日有数据 → 返回 status: "success_from_cache" + 昨日数据（因为今天还没抓取，用昨日数据分析）
3. **若昨日也无数据，执行实时爬取**
   - 深入第一梯队网站的二级详情页，将今日所有包含硬核技术落地内文的全文捞回
   - 将原始数据按天存储到 `~/.openclaw/workspace/skills/daily-fintech-brief/data/raw/{date}.json`（保留7天）
4. 将获取到的原始数据以 JSON 格式返回给你

### Step 2: LLM 总结（由你执行）
仔细阅读爬虫传回的全部 Article 内容，按照以下要求进行深度提炼：

#### 过滤原则
- **宁缺毋滥**：如果详情页中没有抓取到任何实质性的技术细节或数据，该条新闻宁可不入选
- **严禁捏造**：所有总结必须基于爬虫传回的详情页正文，禁止脑补任何没有发生的科技项目

#### 信息提取要点
重点提取以下信息：
- **具体的应用场景**（哪家银行/机构？什么业务场景？）
- **使用的模型/技术栈名称**（大模型？什么框架？）
- **实际达到的业务量化成效**（提升了百分之多少？延迟降低了多少毫秒？）
- **底层的技术架构演进细节**（分布式？云原生？微服务？）

### Step 3: 输出标准格式日报
根据下方【标准输出格式】生成今日简报，并调用 `save_report` 工具将其保存。

### Step 4: 本地归档
报告会自动保存到 `~/.openclaw/workspace/skills/daily-fintech-brief/output/reports/{date}.md`（永久保留，不删除）

---

## 📊 标准输出格式

### 🏦 每日 AI 与金融科技高级内参

**生成日期**: YYYY-MM-DD  
**数据来源**: {date}

---

### 今日风向概述

[用 2-3 句话高度概括过去 24 小时国内外金融科技详情页中暴露出的最核心技术演进或战略动向]

---

### 一、全球 AI 技术前沿速递

来源: The Batch / Ben's Bites

| # | 核心突破 | 技术要点 | 来源 |
|---|---------|-------|-----|
| 1 | [厂商/项目名称] | [技术参数、实现逻辑、行业影响] | [原文链接] |
| 2 | ... | ... | ... |

---

### 二、国内银行业金融科技风向标

来源: 中国金融电脑 / 中国电子银行网 / 移动支付网

| # | 银行/机构 | 应用场景 | 技术实现 | 业务成效 | 来源 |
|---|---------|-------|--------|-------|-------|-----|
| 1 | 【XX银行】| [场景名] | [技术细节] | [量化指标] | [原文链接] |
| 2 | ... | ... | ... | ... | ... |

---

### 三、国际银行科技动态参考

来源: Banking Dive

| # | 机构 | 动向 | 技术细节 | 来源 |
|---|-----|-----|--------|-----|
| 1 | [机构名] | [描述] | [技术细节] | [原文链接] |
| 2 | ... | ... | ... | ... |

---

### 📕 本期涉及数据来源汇总

| 来源 | 文章数 |
|-----|-------|
| The Batch | X |
| Ben's Bites | X |
| 中国金融电脑 | X |
| ... | X |
| **合计** | X |

---

## 📕 数据来源
| 标题 | 地址 (URL) | 类型 (Type) | 基础根域名 (Base URL) |
| --- | --- | --- | --- |
| The Batch | [https://www.deeplearning.ai/the-batch/rss/](https://www.deeplearning.ai/the-batch/rss/) | rss | - |
| Ben's Bites | [https://www.bensbites.co/rss](https://www.bensbites.co/rss) | rss | - |
| Banking Dive | [https://www.bankingdive.com/feeds/news/](https://www.bankingdive.com/feeds/news/) | rss | - |
| 中国金融电脑-科技资讯 | [https://www.fcc.com.cn/art/kjzx/](https://www.fcc.com.cn/art/kjzx/) | html_list | [https://www.fcc.com.cn](https://www.fcc.com.cn) |
| 中国电子银行网-数字银行 | [https://www.cebnet.com.cn/szyh/](https://www.cebnet.com.cn/szyh/) | html_list | [https://www.cebnet.com.cn](https://www.cebnet.com.cn) |
| 中国电子银行网-金融AI | [https://www.cebnet.com.cn/financialai/](https://www.cebnet.com.cn/financialai/) | html_list | [https://www.cebnet.com.cn](https://www.cebnet.com.cn) |
| 移动支付网-首页 | [https://www.mpaypass.com.cn/](https://www.mpaypass.com.cn/) | html_list | [https://www.mpaypass.com.cn](https://www.mpaypass.com.cn) |
| 移动支付网-金科专栏 | [https://www.mpaypass.com.cn/authordefault.asp?id=80115](https://www.mpaypass.com.cn/authordefault.asp?id=80115) | html_list | [https://www.mpaypass.com.cn](https://www.mpaypass.com.cn) |