---
name: daily-ai-brief-skill
description: 一个简洁高效的AI新闻简报生成技能。每日自动从多个可靠数据源采集AI领域最新动态，生成干净的Markdown格式简报，帮助您快速掌握AI行业前沿信息。
author: ideamac
version: 1.0.0
tags: [ai, news, aggregator]
---

# AI Daily Brief Skill

一个AI新闻聚合技能，每日自动从数十个高质量数据源采集AI领域最新动态，生成结构化的新闻简报。

## 功能特性

- **多源采集**: 支持RSS、X/Twitter、网页爬虫、API等多种数据源
- **智能过滤**: 基于关键词和时效性自动过滤内容
- **智能排序**: 按发布时间降序排列新闻
- **多格式输出**: 支持Markdown、JSON等多种报告格式
- **并发执行**: 使用异步并发技术快速抓取多个数据源
- **可配置性强**: 通过YAML配置文件轻松添加/删除数据源

## 数据源覆盖

- **国内媒体**: 36氪、量子位、新智元等
- **国际媒体**: MIT Technology Review、TechCrunch、Ars Technica等
- **学术研究**: OpenAI Blog、Hugging Face Blog、arXiv CS.AI/CS.LG等
- **社区平台**: X/Twitter关键账号
- **行业动态**: Hacker News、行业博客等

## 安装使用

### 1. 安装依赖
```bash
pip install -r requirements.txt
```
依赖安装若出现失败、速度慢、超时情况，尝试使用国内镜像重试


### 2. 配置数据源

编辑 `src/data_sources.yaml` 配置文件，根据需要启用/禁用数据源，调整抓取参数。

### 3. 运行技能

```bash
python src/main.py
```

### 4. 查看报告

报告将自动生成在 `reports/` 目录下：
- `ai_news_report_YYYYMMDD_HHMMSS.md` - 最全最优的Markdown报告（包含所有新闻条目，按类别结构化组织）
- `ai_news_report_YYYYMMDD_HHMMSS.json` - JSON格式数据（机器可读）

## 配置说明

### 数据源配置

技能使用YAML格式配置文件 (`src/data_sources.yaml`)，包含以下主要部分：

1. **rss_sources**: RSS订阅源配置
2**x_sources**: X/Twitter账号配置
3**web_scrapers**: 网页爬虫配置
4**api_sources**: API接口配置
5**fetch_config**: 抓取全局配置

### 过滤配置

每个数据源支持以下过滤选项：

```yaml
filters:
  include_keywords: ["AI", "人工智能", "大模型"]  # 包含关键词
  exclude_keywords: ["广告", "推广"]              # 排除关键词
```

### 抓取配置

```yaml
fetch_config:
  max_items_per_source: 15      # 每个源最大抓取数量
  timeout_seconds: 30           # 请求超时时间
  max_retries: 2                # 重试次数
  max_age_hours: 72             # 最大新闻年龄（小时）
  exclude_keywords:             # 全局排除关键词
    - "sponsored"
    - "advertisement"
```


## 扩展开发

### 添加新的抓取器

1. 在 `src/modules/` 目录下创建新的抓取器类，继承 `BaseFetcher`
2. 实现 `async def fetch(self) -> List[NewsItem]` 方法
3. 在 `fetcher_factory.py` 中注册新的抓取器类型

### 添加新的数据源

1. 在 `src/data_sources.yaml` 中添加新的数据源配置
2. 根据数据源类型选择相应的抓取器类型
3. 调整过滤参数和抓取数量

## 报告格式

技能生成的报告包含以下关键字段：

| 字段 | 说明 | 是否必须 |
|------|------|----------|
| **标题 (title)** | 新闻标题 | 是 |
| **来源 (source)** | 新闻来源（如36氪等） | 是 |
| **发布时间 (publish_date)** | 新闻发布时间 | 是 |
| **链接 (ref)** | 新闻原文链接，用户可点击查询原文 | **必须展示** |
| **摘要 (summary)** | 新闻摘要 | 是 |

### Ref字段（原文链接）说明

**Ref字段是必须展示的**，用户可以点击查询原文。具体要求如下：

1. **必须性**：每个新闻条目都必须包含ref字段（原文链接）
2. **可点击性**：在Markdown报告中，ref字段必须以`[阅读原文](URL)`格式展示，确保用户可以直接点击访问原文
3. **可追溯性**：ref链接必须指向新闻的原始出处，确保信息的可追溯性
4. **数据一致性**：在JSON报告中，ref对应`url`字段

**示例**：
```
**链接**: [阅读原文](https://example.com/news/123)
```

## 翻译功能

技能生成的报告主要为英文和中文新闻。如需将英文新闻翻译为中英双语，可以使用以下提示词让大模型自行翻译：

```markdown
请将以下英文新闻翻译成中文，并保持中英双语对照格式：

[英文新闻标题]
[英文新闻摘要]

翻译要求：
1. 保持专业术语准确性
2. 译文自然流畅
3. 中英文对照显示
4. 保留原文链接和出处信息

也可以使用更简洁的提示词：

"将以下英文AI新闻翻译为中文，并提供中英双语对照："
```

### 使用示例

假设报告中有以下英文新闻条目：

```
## 1. OpenAI releases new multimodal model
**来源**: OpenAI Blog (rss)
**发布时间**: 2024-05-13 10:30
**链接**: [阅读原文](https://openai.com/blog/new-multimodal-model)
**摘要**: OpenAI has announced a new multimodal model that can process text, images, and audio simultaneously...
```

使用提示词后，大模型将生成：

```
## 1. OpenAI发布新的多模态模型
**来源**: OpenAI Blog (rss)
**发布时间**: 2024-05-13 10:30
**链接**: [阅读原文](https://openai.com/blog/new-multimodal-model)

**英文摘要**: OpenAI has announced a new multimodal model that can process text, images, and audio simultaneously...
**中文翻译**: OpenAI宣布了一个新的多模态模型，可以同时处理文本、图像和音频...

**中英双语摘要**:
- **英文**: OpenAI has announced a new multimodal model that can process text, images, and audio simultaneously.
- **中文**: OpenAI宣布了一个新的多模态模型，可以同时处理文本、图像和音频。
```


## 问题反馈

如遇问题或建议，请提交Issue或联系维护者。