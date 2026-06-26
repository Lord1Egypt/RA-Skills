# AI News Skills

[![version](https://img.shields.io/badge/version-1.3.0-blue)](CHANGELOG.md) [![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

一套面向 OpenClaw / Claude Code 的 AI 新闻自动化工作流。

> Three OpenClaw-compatible skills that automate the full AI news pipeline: collect from public web sources into Feishu bitable, generate daily signal briefs with morning guides, and synthesize weekly trend reports with deep dives.

## 它能做什么

```
公开网页 ──→ 自动采集 ──→ 飞书原始新闻表 ──→ AI 筛选 ──→ 日报 & 晨间导读
         fetcher                            reporter       │
                                                           ▼
                                              周报 & 深度解读 & 观察链更新
                                                    weekly_reporter
```

- **`ai_news_fetcher`** — 从多个公开源自动抓取 AI 新闻，写入飞书多维表格
- **`ai_news_reporter`** — 从飞书表读取新闻，AI 筛选高价值事件，生成日报和晨间导读
- **`ai_weekly_reporter`** — 基于本周日报合成趋势线，深度解读，更新产业链观察图谱

支持中文源（如 36氪、财联社）、英文源（如 Forrester）、官方博客（如 OpenAI、Anthropic）、GitHub Trending 等，可按需自行增减。详见 `references/sources.md`。

## 效果示例

### 采集输出（ai_news_fetcher）

fetcher 采集后输出结构化 JSON，每条新闻包含标题、链接、时间、来源：

```json
{
  "fetched_at": "2026-03-21T04:01:47Z",
  "articles": [
    {
      "title": "我们如何监控内部编程智能体的对齐失范",
      "url": "https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/",
      "date": "2026年3月19日",
      "summary": null,
      "source": "OpenAI新闻",
      "parsed_date": "2026-03-18T16:00:00Z"
    },
    {
      "title": "GPT-5.4 mini 与 nano 正式发布",
      "url": "https://openai.com/zh-Hans-CN/index/introducing-gpt-5-4-mini-and-nano/",
      "date": "2026年3月17日",
      "summary": null,
      "source": "OpenAI新闻",
      "parsed_date": "2026-03-16T16:00:00Z"
    }
  ],
  "total": 9,
  "source_group": "public-web"
}
```

写入飞书多维表格后，每条记录自动生成标题哈希、报道窗口键等字段，用于去重和后续日报生成。

### 日报输出（ai_news_reporter）

reporter 从原始新闻表筛选高价值事件，生成 signal 风格的日报：

```markdown
# AI日报｜2026-03-21

统计范围：2026-03-20 09:00 ~ 2026-03-21 09:00
原始记录：47
去重后：38
进入正文：5

## 今日新增信号

### Signal 1：OpenAI 发布 GPT-5.4 mini 与 nano
事件描述：OpenAI 推出两款轻量级模型，主打低成本高效推理……

问题还原：中小开发者需要低成本的生产级模型，但现有方案要么太贵要么能力不足

所属主题：算力
所属链路：模型供给 → 轻量化
所属节点：推理成本优化

旧方案：GPT-4o-mini 作为低成本选项，但上下文窗口和多模态能力有限
新变化：mini 和 nano 分别覆盖中低两档，nano 价格降至 $0.1/1M tokens
为什么重要：直接改变"能力 vs 成本"的选择曲线，agent 场景的调用成本可能降一个量级

待验证问题：
1. nano 在复杂 agent 工作流中的可靠性如何？
2. 竞品（Gemini Flash、Claude Haiku）是否会跟进降价？

关键原文链接：
- GPT-5.4 mini 与 nano 正式发布 | OpenAI新闻 | https://openai.com/...
```

以及发送到群聊的**晨间导读**：

```markdown
早上好。3月21日，周五。
先不急着被消息淹没，今天最值得先看的几件事在这里。

**今天最值得先看的 3 个信号**

**1. OpenAI 发布 GPT-5.4 mini 与 nano**
发生了什么：两款轻量模型上线，nano 价格降至 $0.1/1M tokens
为什么今天先看它：直接影响你的 agent 调用成本预算

---

**2. ……**

---

**今天还值得继续留意的一件事**
Anthropic 和 Google 是否会在本周跟进降价？上周 Claude 4 刚发布……

**完整版日报**
https://飞书文档链接
```

> 以上为示意，实际内容由 AI 根据当日新闻生成。日报模板详见 `ai_news_reporter/references/output-template.md`。

## Quick Start

### 方式一：从 ClawHub 安装（推荐）

已上架 [ClawHub](https://clawhub.ai)，一个命令装全套：

```
clawhub install ai-news-skills
```

### 方式二：从 GitHub 安装

复制下面这句话发给你的 AI agent（Claude Code / OpenClaw / Cursor 等）：

```
帮我安装 AI News Skills：https://raw.githubusercontent.com/yy4fun/ai-news-skills/main/docs/install.md
```

agent 会自动完成所有安装和配置（包括依赖 [Agent Reach](https://github.com/Panniantong/Agent-Reach)），装完让你填飞书表信息就行。

### 方式三：分步安装

如果你想分开装，也是发给 agent：

```
帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

```
帮我安装 AI News Skills：https://raw.githubusercontent.com/yy4fun/ai-news-skills/main/docs/install.md
```

## 安装后需要配置的内容

### 1. 飞书多维表格

安装脚本会自动复制配置模板，你需要填入自己的飞书信息：

```json
{
  "app_name": "你的应用名",
  "app_token": "你的 app_token",
  "table_name": "你的表名",
  "table_id": "你的 table_id",
  "url": "https://你的飞书域名/base/你的app_token"
}
```

配置文件位置：
- `~/.openclaw/workspace/skills/ai_news_fetcher/bitable_target.json`
- `~/.openclaw/workspace/skills/ai_news_reporter/bitable_target.json`

### 2. 新闻源（可选）

默认已配置多个中英文源，开箱即用。如需增减源，只需编辑 `sources.json` 这一个文件。

### 3. 关注清单表（可选）

如果你想用产业链观察和关注清单功能，还需要：
- 在飞书创建一张关注清单多维表格
- 填入 `ai_news_reporter/watch_target.json`（参考 `watch_target.example.json`）

### 4. 定时任务（可选）

在 OpenClaw 中配置 cron 定时任务，实现全自动采集 → 日报 → 周报。

把下面的指令发给你的 AI agent，它会帮你创建定时任务：

#### 新闻采集（建议每天 3-4 次）

```
帮我创建一个 cron 定时任务：
- 名称：AI新闻采集-08:30
- 时间：每天 08:30
- 内容：使用 ai_news_fetcher skill 采集公开网页新闻并写入原始新闻表
- 目标表：填你的 app_token 和 table_id
- 备注字段写 cron:08:30
- 完成后回执发给我
```

#### 日报生成（建议每天早上 1 次，在采集之后）

```
帮我创建一个 cron 定时任务：
- 名称：AI日报生成-09:00
- 时间：每天 09:00
- 内容：使用 ai_news_reporter skill，基于飞书原始新闻表生成当天 AI 日报并发送早报导读
- 报道窗口键格式：YYYY-MM-DD-0900
- 日报发到知识库，早报导读发到群聊
- 日报同时保存一份到 workspace/daily_reports/YYYY-MM-DD.md
- 填你的 app_token、table_id、知识库 URL、群聊 chat_id
- 完成后回执发给我
```

#### 周报生成（建议每周日 1 次）

```
帮我创建一个 cron 定时任务：
- 名称：AI周报生成-周日09:20
- 时间：每周日 09:20
- 内容：使用 ai_weekly_reporter skill 生成本周 AI 周报
- 读取本周一至周日的日报，优先本地 MD，没有的从飞书读
- 每条趋势线对照 watch_chains.md 写判断变化
- 选一个最重要话题做深度解读（必须读原文）
- 周报发到知识库和群聊，同时保存到 workspace/weekly_reports/
- 生成后更新 watch_chains.md
- 填你的知识库 URL、群聊 chat_id
- 完成后回执发给我，包含过程日志
```

> **提示**：建议采集和日报之间留 30 分钟间隔，确保新闻入表后再生成日报。多轮采集可以分布在 05:00、08:30、12:00、18:00 等时段。

## 架构

```
┌─────────────────────────────────────────────────────────┐
│  cron 定时触发 / 飞书对话手动触发                          │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────── ai_news_fetcher ─────────────────────────┐
│                                                         │
│  curl r.jina.ai/URL          ← jina reader 转 markdown  │
│       │                                                 │
│       ▼                                                 │
│  normalize_agent_reach.py    ← 提取标题/链接/时间/摘要    │
│       │                                                 │
│       ▼                                                 │
│  build_source_items.py       ← 生成飞书入表 JSON         │
│       │                                                 │
│       ▼                                                 │
│  两层去重 → 写入飞书多维表格                               │
└─────────────────────────────────────────────────────────┘
                     ▼
┌─────────────── ai_news_reporter ────────────────────────┐
│                                                         │
│  读取关注清单 + 产业链图谱 (watch_chains.md)               │
│       │                                                 │
│       ▼                                                 │
│  按报道窗口键读取原始新闻 → 两层高价值筛选                  │
│       │                                                 │
│       ▼                                                 │
│  阅读全文 → 生成日报 & 晨间导读 → 更新关注清单              │
└─────────────────────────────────────────────────────────┘
                     ▼ (每周日)
┌─────────────── ai_weekly_reporter ──────────────────────┐
│                                                         │
│  读取本周日报 + 产业链图谱                                 │
│       │                                                 │
│       ▼                                                 │
│  跨天信号关联 → 合成趋势线                                 │
│       │                                                 │
│       ▼                                                 │
│  深度解读（阅读原文 + 自我追问）→ 生成周报                  │
│       │                                                 │
│       ▼                                                 │
│  更新 watch_chains.md → 审视关注清单                      │
│       │                                                 │
│       ▼                                                 │
│  框架自我迭代（反馈日志 → 模式识别 → 更新分析框架）         │
└─────────────────────────────────────────────────────────┘
```

## 前置依赖

| 依赖 | 用途 | 必须？ |
|---|---|---|
| [Agent Reach](https://github.com/Panniantong/Agent-Reach) | 给 AI agent 提供网页读取能力（读取 & 搜索 Twitter、Reddit、YouTube、GitHub 等） | ✅ fetcher 核心依赖 |
| Python 3.10+ | 运行 normalize / build 脚本 | ✅ |
| 飞书多维表格 | 存储原始新闻 & 日报输出 | ✅ |
| OpenClaw / Claude Code | 运行 skill、cron 调度 | ✅ |

> Agent Reach 底层使用 [jina reader](https://r.jina.ai) 将网页转为干净的 markdown（`curl r.jina.ai/URL`），这是 fetcher 采集管道的基础。Quick Start 中的安装命令会自动处理。

## 目录结构

```
skills/
├── ai_news_fetcher/
│   ├── SKILL.md                          # skill 说明（给 AI agent 读的）
│   ├── _meta.json                        # skill 元数据
│   ├── sources.json                      # 新闻源唯一配置（加减源只改这里）
│   ├── normalize_agent_reach.py          # jina markdown → 结构化记录
│   ├── build_source_items.py             # 结构化记录 → 飞书入表 JSON
│   ├── bitable_target.example.json       # 飞书配置示例
│   ├── references/
│   │   ├── sources.md                    # 新闻源清单 & 特殊规则
│   │   ├── execution.md                  # 执行流程详细说明
│   │   ├── data-model.md                 # 数据模型定义
│   │   └── gotchas.md                    # 踩坑记录
│   └── tests/
│       └── test_parse_date.py            # 时间解析测试
│
├── ai_news_reporter/
│   ├── SKILL.md
│   ├── _meta.json
│   ├── build_daily_report.py             # 日报生成
│   ├── build_event_candidates.py         # 事件筛选
│   ├── build_signals.py                  # 信号提取
│   ├── bitable_target.example.json
│   ├── watch_target.example.json         # 关注清单表配置示例
│   └── references/
│       ├── reporting.md                  # 日报执行流程
│       ├── output-template.md            # 日报 & 早报模板
│       ├── watch_chains.md               # 产业链关注图谱
│       └── gotchas.md                    # 踩坑记录
│
└── ai_weekly_reporter/
    ├── SKILL.md
    └── references/
        ├── reporting.md                  # 周报执行流程
        ├── output-template.md            # 周报模板
        └── analysis_framework.md         # 深入分析框架（可通过反馈进化）
```

## 核心设计原则

- **原始时间保真**：`原始时间` 原样保留，`发布时间` 只在可信确认时才写入
- **采集与报告分离**：fetcher 只管抓和入表，reporter 只管读和生成，weekly_reporter 只管趋势合成
- **观察链驱动**：`watch_chains.md` 记录产业链判断基线，日报筛选和周报合成都参照它
- **反馈闭环**：日报产出待验证问题 → 关注清单 → 后续日报回答 → 周报审视清理
- **友好抓取**：遇到 403、验证码、登录墙就跳过，不硬刚
- **无日期源兜底**：GitHub Trending、Google Cloud 博客等无发布时间的源，使用 `--fallback-to-now` 用抓取时间代替

## 添加新源

1. 在 `sources.json` 中添加源配置
2. 如有特殊规则，在 `references/sources.md` 中记录
3. 用管道命令手动测试：
   ```bash
   curl -s "https://r.jina.ai/新源URL" \
     | python3 normalize_agent_reach.py --source "新源名"
   ```
4. 如果新源没有发布时间，在源配置中加 `"fallback_to_now": True`，命令加 `--fallback-to-now`
5. 确认输出正常后，cron 会自动采集

## 不包含的内容

公开版已做脱敏，不包含：

- 飞书真实 `app_token` / `table_id`
- 真实 `open_id` / `chat_id`
- cron 任务配置
- 运行日志和历史回执

## Changelog

当前版本：**v1.3.0** — 详见 [CHANGELOG.md](CHANGELOG.md)

## License

[MIT License](LICENSE) — 可以自由使用、修改和分发，保留版权声明即可。
