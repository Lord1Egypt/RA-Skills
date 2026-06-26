---
name: ai-deepnews
description: AI Product Manager daily intelligence digest. Fetches news from 16+ curated RSS sources across tech media, AI labs, research papers, developer communities, and podcasts. Auto-translates to Chinese with deduplication and date filtering. Zero API keys required.
---

# AIPM News Digest / AI 产品经理情报日报

面向 AI 从业者和产品经理的每日情报采集工具。从 16+ 精选 RSS 源自动抓取最新 AI 资讯，翻译成中文摘要，按来源分类输出 Markdown 格式日报。

## 信息源覆盖

### 科技媒体
| 来源 | 说明 |
|------|------|
| TechCrunch AI | 硅谷顶级科技媒体 AI 频道 |
| The Verge AI | 消费科技视角的 AI 报道 |
| Ars Technica | 深度技术分析 |
| MIT Technology Review | MIT 技术评论，前沿趋势 |

### AI 实验室官方博客
| 来源 | 说明 |
|------|------|
| OpenAI Blog | GPT/ChatGPT/Sora 等产品动态 |
| Google AI Blog | Gemini/DeepMind 研究进展 |
| DeepMind Blog | AlphaFold 等基础研究 |
| Anthropic Blog | Claude 系列模型与安全研究 |
| Hugging Face Blog | 开源模型与社区生态 |

### 学术论文
| 来源 | 说明 |
|------|------|
| arXiv cs.AI | 人工智能核心论文 |
| arXiv cs.CL | 自然语言处理/LLM 论文 |

### 开发者社区
| 来源 | 说明 |
|------|------|
| r/MachineLearning | Reddit 机器学习板块热帖 |
| r/LocalLLaMA | 本地大模型部署社区 |
| Hacker News | YC 创业社区 AI 热议（50+ 赞） |

### 播客与深度内容
| 来源 | 说明 |
|------|------|
| Latent Space | AI 工程师播客，嘉宾质量极高 |
| The Cognitive Revolution | AI 认知革命，行业领袖访谈 |

## Setup

```bash
cd skills/aipm-news-digest && python3 -m venv venv && ./venv/bin/pip install feedparser googletrans==4.0.0-rc1
```

无需任何 API Key，开箱即用。

## Usage

```bash
cd skills/aipm-news-digest && ./venv/bin/python fetch_ai_news_improved.py
```

输出示例：
```
🤖 AI 资讯日报 - 2026-03-11 08:00 UTC
📰 共 25 条新资讯

---
### 📌 OpenAI Blog
**GPT-5 发布：多模态推理能力大幅提升**
> OpenAI 今日发布 GPT-5，在数学推理和代码生成方面...
🔗 原文链接

### 📌 arXiv cs.CL
**基于强化学习的大语言模型对齐新方法**
> 本文提出一种新的 RLHF 替代方案...
🔗 原文链接
```

## Features

- **16+ 精选源** — 覆盖媒体、实验室、论文、社区、播客五大维度
- **自动去重** — 基于内容哈希，不会重复推送
- **时间过滤** — 只推送 3 天内的文章，过期自动跳过
- **缓存自清理** — 7 天自动清理已读记录
- **免费翻译** — Google Translate API，无需额外配置
- **可配置** — `MAX_ARTICLES_PER_FEED`（每源上限）、`MAX_TOTAL_ARTICLES`（总条数）、`MAX_DAYS_OLD`（时效天数）均可调整

## 重点追踪对象

### 硅谷大厂
- **OpenAI** — GPT/ChatGPT/Sora/o系列，Sam Altman 动态
- **Google DeepMind** — Gemini/AlphaFold，Demis Hassabis、Jeff Dean
- **Anthropic** — Claude 系列，Dario Amodei、Amanda Askell
- **Meta AI** — LLaMA 开源生态，Yann LeCun
- **Apple** — Apple Intelligence/端侧模型，Craig Federighi
- **Microsoft** — Copilot/Azure AI，Satya Nadella、Kevin Scott
- **NVIDIA** — GPU/CUDA/推理加速，Jensen Huang

### AI 核心人物
- **Andrej Karpathy** — 前 Tesla/OpenAI，AI 教育与创业
- **Jim Fan（范麟熙）** — NVIDIA 高级研究科学家，具身智能
- **François Chollet** — Keras 创始人，AGI 评估（ARC）
- **Ilya Sutskever** — SSI 联合创始人，前 OpenAI 首席科学家
- **Fei-Fei Li（李飞飞）** — 斯坦福 HAI，World Labs 创始人

### 独立 KOL / 分析师
- **宝玉（@dotey）** — AI 资讯翻译与深度解读
- **Simon Willison** — LLM 工具链与应用实践
- **Swyx（shawn@wang）** — Latent Space 主理人，AI 工程趋势

## 适用场景

- AI 产品经理每日情报采集
- 技术团队 AI 动态周报素材
- 个人 AI 学习与信息追踪
- 配合 cron 定时任务自动推送到 Telegram/WhatsApp/Slack
