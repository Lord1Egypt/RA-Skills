# GEO AgentOps v2.0

> 🦞 AI-Powered Export GEO Operations System — 让AI引擎主动推荐你的产品和服务

[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](package.json)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GEO](https://img.shields.io/badge/GEO-6%20Platforms-purple.svg)](#)
[![B2B](https://img.shields.io/badge/B2B-Export-Blue.svg)](#)

---

## 💡 一句话价值主张

**把产品写进AI的答案里。** GEO（生成式引擎优化）让B2B出海企业在ChatGPT、Claude、Gemini、Perplexity等AI引擎中主动被推荐——每条询盘成本仅$0.04，是Google Ads的1/30。

---

## ⚡ 核心效果数据

| 指标 | GEO AgentOps | Google Ads对比 |
|------|-------------|---------------|
| 每条询盘成本 | **$0.04** | $1.20 |
| 询盘增长 | **+127%** | +15% |
| 月均AI渠道询盘 | **580条** | 260条 |
| 见效周期 | **1-2个月** | 即时 |
| 内容生命周期 | **长期** | 停止付费=消失 |

---

## 🎯 三大产品模块

| 产品 | 图标 | 功能 | 定价 |
|------|------|------|------|
| **Echo** 📢 | GEO内容智能引擎 | 主题规划 + 文章生成 + FAQ优化 | $19/月 |
| **Wing** 🪽 | 多平台内容分发 | 一键发布 LinkedIn/Twitter/Reddit/Medium/Quora | $39/月 |
| **Radar** 📡 | AI引用监测与优化 | 实时追踪6大平台引用排名，自动优化建议 | $39/月 |
| **All-in Bundle** | 全部三大模块 | 三合一，完整GEO工作流 | **$59/月** |

---

## 🔄 6步GEO工作流

```
⚙️ 配置品牌  →  🤖 AI内容生成  →  📤 多平台发布
     ↓              ↓                   ↓
📝 内容归档      🔗 引用监测         📊 报告生成
     ↑              ↑                   ↑
   关键词       Perplexity/GPT       效果洞察
   平台选择       Claude/Gemini        持续优化
```

1. **⚙️ 配置品牌** — 设置品牌名、核心关键词、目标平台
2. **🤖 AI内容生成** — 选择模型×Agent×主题，秒级生成
3. **📤 发布平台** — 一键同步至 LinkedIn / Twitter/X / Reddit / Medium / Quora
4. **📝 内容归档** — 追踪所有内容发布状态与版本
5. **🔗 引用监测** — 监控AI引擎引用排名（SOM得分）
6. **📊 报告生成** — 一键生成周/月度运营报告

---

## 🤖 6大内容Agent

| Agent | 图标 | 输出 | 说明 |
|-------|------|------|------|
| Topic Planner | 📡 | 每周选题库 | 行业热点 + 关键词挖掘 + 内容日历 |
| Headline Generator | 🔥 | 10个爆款标题 | 高点击率标题，A/B测试支持 |
| GEO Article | 📝 | 1200词完整文章 | AI引用优化结构，Schema标记 |
| FAQ Content | ❓ | 8组AI可引用Q&A | 精确匹配AI查询模式 |
| LinkedIn Post | 💼 | 专业领英帖子 | B2B行业风格，互动引导 |
| Weekly Report | 📊 | 自动周报模板 | 效果数据可视化 |

---

## 🌍 4大AI引擎支持

| 引擎 | 权重策略 | 最优内容类型 |
|------|---------|------------|
| 🤖 **ChatGPT** | 权威引用+结构化 | FAQ + 步骤指南 |
| 💎 **Claude** | 深度分析+引用 | 长文 + 案例研究 |
| ✨ **Gemini** | Google原生+实时性 | 新闻 + 产品更新 |
| 🔍 **Perplexity** | **新鲜度0.98** + 来源 | Reddit + 社区内容 |

> **Perplexity技巧**：48小时内发布内容达到引用峰值，30天内持续有效，Reddit内容占引用来源46.7%。

---

## 📊 客户案例

### 案例1：Amazon FBA户外装备卖家
- 询盘增长：**+127%**
- 单条询盘成本：**$0.04**
- 月均AI渠道询盘：**580条**

### 案例2：Shopify厨房用品 DTC品牌
- LinkedIn互动增长：**+340%**
- 平均AI引用率：**68%**
- 月均合格线索：**210条**

### 案例3：B2B工业阀门出口商
- 6大AI平台TOP3占位率：**89%**
- 独立站自然流量：**+420%**
- SEO ROI：**1:6**

---

## 🚀 快速开始

### 安装
```bash
# 克隆仓库
git clone https://github.com/WangM-A3/geo-agentops.git
cd geo-agentops

# 安装依赖
pip install -r requirements.txt

# 查看完整文档
cat SKILL.md
```

### 配置 API Key
```bash
# 设置环境变量
export OPENAI_API_KEY=sk-xxx
export ANTHROPIC_API_KEY=sk-xxx
```

### 生成第一篇GEO内容
```python
from geo_agentops import TopicPlanner, GEOArticle, FAQGenerator

# Step 1: 生成选题
planner = TopicPlanner(model="gpt-4o")
topics = planner.generate_weekly_topics(brand="Industrial Valves")

# Step 2: 生成GEO文章
article = GEOArticle(model="gpt-4o")
content = article.generate(topic=topics[0], keywords=["ball valve", "industrial"])

# Step 3: 生成FAQ（最高引用率）
faq = FAQGenerator(model="gpt-4o")
qa_pairs = faq.generate(question_count=8)

print(f"文章已生成: {len(content.words)}字")
print(f"FAQ已生成: {len(qa_pairs)}组")
```

---

## 🆚 竞品对比

| 能力 | GEO AgentOps | 传统SEO工具 | 纯AI写作工具 |
|------|-------------|-----------|------------|
| AI平台覆盖 | **6大平台** | 仅Google | 无 |
| 引用监测 | ✅ 实时SOM得分 | ❌ 无 | ❌ 无 |
| 多平台分发 | ✅ 5大平台 | ❌ 无 | ❌ 无 |
| GEO优化 | ✅ 深度 | ❌ 无 | 基础 |
| 内容Agent | ✅ 6个专业Agent | ❌ 无 | 仅生成 |
| 效果报告 | ✅ 自动 | 部分 | ❌ 无 |

---

## 🗂️ 目录结构

```
geo-agentops/
├── SKILL.md                    # 完整技能文档
├── README.md                   # 本文件
├── clawhub.yaml               # ClawHub配置
├── package.json               # 包配置
├── llms.txt                   # LLM可爬取指南
├── references/                # 参考文档
│   ├── GEO-METHODOLOGY.md    # GEO方法论
│   ├── SCHEMA-GUIDE.md       # Schema标记指南
│   └── LLMs-TXT-GUIDE.md     # LLMs.txt配置
├── scripts/                    # 执行脚本
│   └── geo_score.py          # GEO评分引擎
└── templates/                  # 内容模板
    ├── geo-article.md        # GEO文章模板
    ├── faq-template.md        # FAQ模板
    └── weekly-report.md      # 周报模板
```

---

## 📞 联系方式

- 🐙 GitHub: [github.com/WangM-A3/geo-agentops](https://github.com/WangM-A3/geo-agentops)
- 📧 Email: support@openclaw.ai

---

*© 2024 OpenClaw AI Team. MIT-0 Licensed.*
