---
name: "ai-news-hub"
slug: ai-news-hub
version: "2.3.1"
homepage: https://github.com/lanyasheng/ai-news-aggregator
description: "AI新闻阅读助手。100+ RSS源并发抓取、兴趣评分、跨天去重、统一预取。智能聚合AI/技术新闻、arXiv论文、GitHub热门项目、AI公司动态。支持日报/周报生成、关键词筛选、分类订阅。"
changelog: "v2.3.1: 修复脚本路径引用问题（统一使用相对路径 scripts/），提升文档准确性"
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# AI News Hub — AI/技术新闻高性能聚合引擎

并发抓取 100+ RSS 源，12秒完成，支持 ETag/Last-Modified 缓存、日期过滤。

## Setup

确保 Python 3.8+ 可用，无需额外依赖（纯标准库）。

## When to Use

用户需要查看 AI/技术新闻、技术趋势、最新论文、GitHub 热门项目、AI 公司动态时使用。

**触发关键词：**
- "AI 新闻"、"技术新闻"、"今天有什么新闻"、"科技早报"
- "最新论文"、"arXiv"、"AI 研究"、"论文摘要"
- "GitHub 热门"、"趋势项目"、"热门仓库"
- "OpenAI 动态"、"Anthropic 更新"、"Claude更新"
- "多智能体"、"LLM"、"大模型"、"Agent"
- "机器学习"、"深度学习"、"NLP"、"计算机视觉"
- "行业动态"、"投资融资"、"产品发布"

**用户意图识别：**
- 快速了解：今天有什么AI新闻？
- 深度追踪：OpenAI最近有什么更新？
- 研究方向：多智能体的最新论文有哪些？
- 项目发现：GitHub上有什么好的AI项目？
- 特定关键词：搜索"多智能体"相关的新闻

---

## 用户交互场景

### 场景1：快速获取今日AI新闻
```
用户：今天有什么AI新闻？
助手：📰 今日AI新闻速递

━━━━━━━━━━━━━━━━━━━━━━━━━━
【公司动态】
• OpenAI 发布 GPT-5 预览版 | 2小时前
• Anthropic Claude 4 性能提升 40% | 5小时前
• Google DeepMind 发布新论文 | 8小时前

【论文发布】
• arXiv: 多智能体协作综述（热榜第一）
• HuggingFace: 新开源模型 Llama-4

【GitHub热门】
• langchain/langchain: 🔥 本周最热 +1200 stars
• microsoft/autogen: 多智能体框架 +800 stars

【投资融资】
• Mistral AI 完成6亿美元融资 | 估值60亿

━━━━━━━━━━━━━━━━━━━━━━━━━━
数据来源：100+ RSS源 | 聚合时间：2026-04-14
```

### 场景2：特定公司动态追踪
```
用户：OpenAI 最近有什么动态？
助手：🏢 OpenAI 近期动态追踪

━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 最近7天更新（共12条）

【产品发布】
✅ GPT-5 预览版发布（2026-04-12）
✅ Sora 升级：支持高清视频生成（2026-04-10）

【技术博客】
✅ 推理能力优化新突破（2026-04-09）
✅ 多模态能力增强（2026-04-08）

【商业动态】
✅ 与微软深化合作（2026-04-07）
✅ 企业版新增功能（2026-04-06）

━━━━━━━━━━━━━━━━━━━━━━━━━━
数据来源：OpenAI Blog +媒体报道
```

### 场景3：arXiv论文搜索
```
用户：有什么最新的多智能体论文？
助手：🔬 arXiv 最新论文：多智能体专题

━━━━━━━━━━━━━━━━━━━━━━━━━━
【Top 5 热门论文】

1️⃣ Multi-Agent Collaboration: A Survey
   • 作者：Zhang et al.
   • 发布：2026-04-13
   • 引用：127 | ⭐ 热度：95
   • 摘要：系统综述多智能体协作的最新进展...

2️⃣ Efficient Multi-Agent Systems
   • 作者：Li et al.
   • 发布：2026-04-12
   • 引用：89 | ⭐ 热度：92
   • 摘要：提出高效的多智能体通信协议...

3️⃣ Autonomous Agent Teams
   • 作者：Wang et al.
   • 发布：2026-04-11
   • 引用：76 | ⭐ 热度：88
   • 摘要：实现完全自主的智能体团队...

━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 查看论文摘要，回复编号获取详情
```

### 场景4：GitHub热门项目发现
```
用户：GitHub上有什么热门的AI项目？
助手：🔥 GitHub AI项目热门榜

━━━━━━━━━━━━━━━━━━━━━━━━━━
【本周Top 10】

1. 🔥 langchain/langchain
   • Stars: +1,234 ⭐
   • 描述：LLM应用开发框架
   • 语言：Python
   • 更新：5小时前

2. ⚡ microsoft/autogen
   • Stars: +876 ⭐
   • 描述：多智能体对话框架
   • 语言：Python
   • 更新：3小时前

3. 🚀 vllm-project/vllm
   • Stars: +654 ⭐
   • 描述：LLM推理加速引擎
   • 语言：Python
   • 更新：6小时前

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 趋势分析：多智能体框架本周最受关注
```

### 场景5：关键词筛选
```
用户：搜索"多智能体"相关的新闻
助手：🔍 关键词搜索：多智能体

━━━━━━━━━━━━━━━━━━━━━━━━━━
【找到 8 条相关新闻】

📰 新闻资讯
• 多智能体协作技术突破 | MIT Tech Review
• 企业级多智能体应用案例 | The Verge
• 多智能体工具链兴起 | InfoQ

🔬 论文研究
• Multi-Agent Survey | arXiv热榜
• 协作机制优化论文 | arXiv新增

💻 项目动态
• autogen 新版本发布 | GitHub Trending
• swarm 多智能体库更新 | GitHub Trending

━━━━━━━━━━━━━━━━━━━━━━━━━━
时间范围：最近7天 | 相关度评分：>70
```

### 场景6：生成日报/周报
```
用户：生成今天的AI早报
助手：📱 AI科技早报

━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 2026年4月14日 星期一

【头条】
• OpenAI GPT-5预览版震撼发布
• Anthropic融资60亿美元估值创新高

【技术前沿】
• 多智能体协作研究综述
• LLaMA 4开源，性能媲美GPT-4
• 3D生成模型迎来重大突破

【商业动态】
• AI基础设施投资热潮持续
• 企业AI应用落地加速

【GitHub精选】
• langchain 本周最热 +1234 stars
• autogen 多智能体框架受关注

━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 数据统计：100+源 | 去重后32条
⏱️ 聚合耗时：12.5秒
```

---

## Architecture

```
ai-news-hub/
├── scripts/
│   ├── rss_aggregator.py      # 核心 RSS 抓取器
│   ├── rss_sources.json       # 100+ RSS 源配置
│   ├── arxiv_papers.py        # arXiv 论文搜索
│   ├── github_trending.py     # GitHub 热门项目
│   └── summarize_url.py       # 文章摘要
└── SKILL.md                   # 本文件
```

## Data Sources

| 分类 | 源数 | 内容 |
|------|------|------|
| company | 16 | OpenAI, Anthropic, Google, Meta, NVIDIA, Apple, Mistral 等官方博客 |
| papers | 6 | arXiv AI/ML/NLP/CV, HuggingFace Daily Papers, BAIR |
| media | 16 | MIT Tech Review, TechCrunch, Wired, The Verge, VentureBeat 等 |
| newsletter | 15 | Simon Willison, Lilian Weng, Andrew Ng, Karpathy 等专家 |
| community | 12 | HN, GitHub Trending, Product Hunt, V2EX 等 |
| cn_media | 5 | 机器之心, 量子位, 36氪, 少数派, InfoQ |
| ai-agent | 5 | LangChain, LlamaIndex, Mem0, Ollama, vLLM 博客 |
| twitter | 10 | Sam Altman, Karpathy, LeCun, Hassabis 等 AI 领袖 |

## Core Commands

### RSS 聚合
```bash
# 抓取所有源（最近3天新闻）
python3 scripts/rss_aggregator.py --category all --days 3 --limit 10

# 只看公司博客
python3 scripts/rss_aggregator.py --category company --days 1 --limit 5

# 只看中文媒体
python3 scripts/rss_aggregator.py --category cn_media --days 3 --limit 10

# AI Agent 相关
python3 scripts/rss_aggregator.py --category ai-agent --days 7 --limit 10

# 输出 JSON 格式
python3 scripts/rss_aggregator.py --category all --days 1 --json
```

### arXiv 论文
```bash
# 最新 AI 论文（按热度排序）
python3 scripts/arxiv_papers.py --limit 5 --top 10

# 搜索特定主题
python3 scripts/arxiv_papers.py --query "multi-agent" --top 5
```

### GitHub Trending
```bash
# AI 相关热门项目（今日）
python3 scripts/github_trending.py --ai-only

# 本周热门
python3 scripts/github_trending.py --since weekly
```

## Core Rules

### 1. 优先使用 --days 参数
默认抓取最近 N 天的新闻，避免获取过期内容：
- 日报：`--days 1`
- 周报：`--days 7`
- 月报：`--days 30`

### 2. 分类选择策略
| 用户需求 | 推荐分类 |
|----------|----------|
| 公司动态 | `--category company` |
| 技术论文 | `--category papers` |
| 中文资讯 | `--category cn_media` |
| 社区趋势 | `--category community` |
| AI Agent | `--category ai-agent` |

### 3. 缓存机制
- 首次抓取后自动缓存（ETag/Last-Modified）
- 缓存有效期 1 小时
- 重复抓取秒级完成

## Configuration

编辑 `scripts/rss_sources.json` 添加/删除 RSS 源：
```json
{
  "name": "OpenAI Blog",
  "url": "https://openai.com/blog/rss.xml",
  "category": "company"
}
```
## 更新日志

### v2.3.0 (2026-04-14) - 用户体验优化
- ✅ 新增完整的用户交互场景（6个典型场景）
- ✅ 优化输出格式：结构化展示、图标标注、分隔线美化
- ✅ 新增关键词筛选功能（精准查找相关内容）
- ✅ 新增分类订阅系统（支持按类别订阅）
- ✅ 新增日报/周报生成功能（格式化报告输出）
- ✅ 增强兴趣评分算法（智能计算相关性）
- ✅ 性能优化：100源聚合时间缩短至10.2秒
- ✅ 完善跨天去重机制
- ✅ 增加趋势分析功能（热门榜、增长趋势）

### v2.2.0
- ✅ 统一预取缓存机制
- ✅ 兴趣评分算法（基于关键词匹配）
- ✅ 跨天去重
- ✅ 仓库结构重构

### v2.1.0
- ✅ 10线程并发抓取
- ✅ ETag/Last-Modified缓存
- ✅ 15秒快速超时
- ✅ 1小时TTL缓存持久化

### v2.0.0
- ✅ 初始版本
- ✅ 支持70+ RSS源
- ✅ arXiv论文搜索
- ✅ GitHub Trending
