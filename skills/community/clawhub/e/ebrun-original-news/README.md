# ebrun-original-news

一个用于获取亿邦动力原创电商新闻的 Claude Code Skill，支持按频道读取最新内容，并返回适合代理或自动化流程消费的结构化结果。

### 项目简介

`ebrun-original-news` 面向需要快速获取电商资讯的使用场景，能够根据自然语言中的频道意图，读取亿邦动力对应栏目下的最新文章，并整理为清晰、稳定的输出。

它适合以下任务：

- 查询推荐频道或指定频道的最新文章
- 按电商赛道快速浏览近期动态
- 在上层 Agent、自动化脚本或信息聚合流程中复用

### 主要能力

- 支持主频道与子频道匹配，例如推荐、未来零售、跨境电商、产业互联网、品牌、AI
- 默认返回最新 10 篇文章
- 输出核心字段，包括标题、作者、摘要、发布时间与原文链接
- 内置 Python 与 Shell 两套抓取脚本，便于不同运行环境接入
- 提供版本检查脚本，便于判断 skill 是否有可用更新
- 当频道无法匹配时，自动回退到推荐频道，保证结果可用性

### 目录结构

```text
ebrun-original-news/
├── SKILL.md
├── README.md
├── examples.md
├── references/
│   ├── api-reference.md
│   ├── channel-list.json
│   └── version.json
└── scripts/
    ├── fetch_news.py
    ├── fetch_news.sh
    ├── update.py
    └── update.sh
```

### 触发示例

以下表达适合触发该 skill：

- `查亿邦最新文章`
- `查跨境最新文章`
- `查亚马逊新闻`
- `产业有什么新动态`
- `看看 AI 新闻`
- `看品牌全球化报道`

### 使用方式

#### 1. 通过自然语言调用

在支持 Claude Code Skill 的环境中，可直接使用自然语言描述要查询的频道或主题，skill 会根据 `references/channel-list.json` 自动完成频道识别与调用。

#### 2. 通过脚本直接调用

优先使用内置脚本，而不是在外部重复编写抓取逻辑。

```bash
# 查询 AI 频道最新 10 篇
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10

# 查询推荐频道最新 10 篇
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_recommend" --json --limit 10

# Python 不可用时使用 Shell 版本
bash scripts/fetch_news.sh "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10
```

#### 3. 检查更新

```bash
# 常规检查
python3 scripts/update.py --json

# 强制忽略检查间隔
python3 scripts/update.py --json --force
```

### 输出说明

默认返回适合进一步处理的结构化新闻数据。典型内容包括：

- `title`
- `author`
- `summary`
- `publish_time`
- `url`

在面向终端用户展示时，可进一步格式化为 Markdown 列表或资讯简报。

### 适用边界

推荐用于：

- 电商新闻检索
- 特定频道的最新内容浏览
- 自动化资讯收集与汇总

不建议用于：

- 非电商领域新闻查询
- 历史归档检索
- 超出当前频道映射范围的定制查询

### 原创性与隐私说明

- 本 README 基于本仓库内的 `SKILL.md`、示例和脚本能力重新整理编写，不直接复制内部说明文本。
- 文档仅描述公开可用的功能、目录与使用方式，不暴露任何个人隐私信息、账号信息、Cookie 或凭证内容。
- 示例命令与示例查询仅用于说明调用方式，不包含用户数据或业务敏感内容。
- 如将本 skill 接入生产流程，建议继续遵循最小化日志、最小化输入保留和凭证隔离原则。

## English

### Overview

`ebrun-original-news` is a Claude Code skill for fetching the latest original e-commerce news from Ebrun. It maps user intent to predefined channels, retrieves recent articles, and returns clean structured data for downstream use.

Typical use cases include:

- reading the latest news from a main or sub-channel
- tracking updates across e-commerce sectors
- integrating Ebrun news retrieval into an agent or automation workflow

### Key Features

- Main-channel and sub-channel matching
- Up to 10 latest articles by default
- Structured outputs with title, author, summary, publish time, and source URL
- Both Python and shell fetch scripts for flexible integration
- Built-in update checker for version awareness
- Automatic fallback to the recommended channel when no channel matches

### Project Layout

```text
ebrun-original-news/
├── SKILL.md
├── README.md
├── examples.md
├── references/
│   ├── api-reference.md
│   ├── channel-list.json
│   └── version.json
└── scripts/
    ├── fetch_news.py
    ├── fetch_news.sh
    ├── update.py
    └── update.sh
```

### Example Triggers

This skill is designed for requests such as:

- `Check the latest Ebrun articles`
- `Show me the latest cross-border news`
- `Get Amazon-related news`
- `What is new in industrial internet`
- `Show me AI news`
- `Give me brand globalization updates`

### Usage

#### 1. Natural language invocation

In a Claude Code environment that supports skills, users can ask for a channel or topic in plain language. The skill reads channel mappings from `references/channel-list.json` and resolves the target automatically.

#### 2. Direct script usage

Prefer the built-in scripts instead of reimplementing fetch logic externally.

```bash
# Fetch the latest 10 AI articles
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10

# Fetch the latest 10 recommended articles
python3 scripts/fetch_news.py "_index/ClaudeCode/SkillJson/information_recommend" --json --limit 10

# Shell fallback when Python is unavailable
bash scripts/fetch_news.sh "_index/ClaudeCode/SkillJson/information_channel_88" --json --limit 10
```

#### 3. Version check

```bash
python3 scripts/update.py --json
python3 scripts/update.py --json --force
```

### Output

The skill is designed to return structured news items that are easy to format into markdown, dashboards, or briefings. Typical fields include:

- `title`
- `author`
- `summary`
- `publish_time`
- `url`

### Scope

Recommended for:

- e-commerce news retrieval
- channel-based latest article discovery
- automation and agent-based news aggregation

Not intended for:

- non-e-commerce news topics
- historical archive browsing
- arbitrary queries outside the configured channel mapping

### Originality and Privacy Notes

- This README is newly written from the repository materials and is not a direct copy of the internal skill instructions.
- It documents only functional behavior, file structure, and usage patterns, without exposing personal data, credentials, cookies, or other sensitive information.
- Example prompts and commands are generic and contain no user-specific or operationally sensitive content.
- For production use, it is still best to keep logs minimal, isolate credentials, and avoid retaining unnecessary request data.
