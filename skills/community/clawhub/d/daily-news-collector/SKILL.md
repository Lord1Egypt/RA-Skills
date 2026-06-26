---
name: daily-news-collector
description: 每天从多个媒体渠道（RSS源、网站、API）自动收集最新资讯，智能分析并生成结构化日报。适用于需要定期监控行业动态、新闻资讯、竞品信息等场景。
dependency:
  python:
    - requests==2.31.0
    - feedparser==6.0.10
    - beautifulsoup4==4.12.2
    - lxml==4.9.3
---

# 每日资讯收集助手

## 任务目标
- 本 Skill 用于：每天自动从多个媒体渠道收集最新资讯并生成结构化日报
- 能力包含：
  - 支持RSS订阅源、网页抓取等多种数据源
  - 自动解析和格式化原始数据
  - 智能筛选重要资讯并分类整理
  - 生成可读性强的Markdown格式日报
- 触发条件：用户需要"收集资讯"、"生成日报"、"监控媒体动态"等场景

## 前置准备
- 依赖说明：
  ```
  requests==2.31.0
  feedparser==6.0.10
  beautifulsoup4==4.12.2
  lxml==4.9.3
  ```
- 配置媒体源：根据 [references/sources.md](references/sources.md) 创建 `sources.json` 配置文件

## 操作步骤

### 标准流程

1. **收集原始数据**
   - 从RSS源收集：调用 `scripts/collect_feeds.py` 读取配置并获取文章列表
     ```bash
     python /workspace/projects/daily-news-collector/scripts/collect_feeds.py --config ./sources.json --output ./raw_data.json
     ```
   - 从网页抓取：调用 `scripts/collect_webpages.py` 获取网页内容
     ```bash
     python /workspace/projects/daily-news-collector/scripts/collect_webpages.py --url <URL> --output ./webpage_data.json
     ```
   - 合并数据到统一的JSON文件供后续分析

2. **分析筛选资讯**
   - 智能体读取收集到的原始数据
   - 根据用户需求筛选重要资讯（如：科技类、商业类、特定关键词）
   - 按主题自动分类（科技、商业、社会、政策等）
   - 为每条资讯生成简明摘要（1-2句话）

3. **生成日报**
   - 参照 [assets/template.md](assets/template.md) 的格式
   - 按分类组织内容，包含标题、链接、摘要、来源
   - 添加日期、统计数据（总条数、分类分布）
   - 输出为Markdown格式的日报文件

### 可选分支
- 当只需要RSS数据：仅执行 `collect_feeds.py`
- 当需要增量更新：检查历史数据，只收集新发布的内容
- 当需要定制分类：在分析阶段根据用户指定的分类规则

## 资源索引
- 核心脚本：
  - [scripts/collect_feeds.py](scripts/collect_feeds.py) (解析RSS订阅源，获取文章列表)
  - [scripts/collect_webpages.py](scripts/collect_webpages.py) (抓取网页内容，提取正文)
- 配置参考：
  - [references/sources.md](references/sources.md) (媒体源配置指南和示例)
  - [references/format.md](references/format.md) (日报格式规范)
- 输出模板：
  - [assets/template.md](assets/template.md) (日报结构模板)

## 注意事项
- 脚本负责数据获取和格式化，智能体负责内容分析和总结
- 定期更新媒体源配置以保持数据新鲜度
- 遵守目标网站的robots.txt规则，合理设置抓取频率
- 生成的日报保存在当前工作目录（`.`），便于用户访问

## 使用示例

### 示例1：收集科技媒体资讯
```bash
# 1. 配置RSS源（如36氪、TechCrunch等）
# 2. 收集数据
python /workspace/projects/daily-news-collector/scripts/collect_feeds.py --config ./tech_sources.json --output ./tech_news.json

# 3. 智能体分析并生成科技日报（由智能体完成）
# - 筛选科技类资讯
# - 生成分类摘要
# - 输出：daily-tech-report-2024-01-15.md
```

### 示例2：监控竞品动态
```bash
# 1. 配置竞品官网和新闻源
# 2. 收集网页内容
python /workspace/projects/daily-news-collector/scripts/collect_webpages.py --url https://competitor.com/news --output ./competitor_news.json

# 3. 智能体分析竞品动态（由智能体完成）
# - 提取关键信息（产品发布、融资、合作等）
# - 生成竞品监控报告
```

### 示例3：综合日报
```bash
# 1. 从多个源收集数据（RSS + 网页）
python /workspace/projects/daily-news-collector/scripts/collect_feeds.py --config ./all_sources.json --output ./all_news.json

# 2. 智能体生成综合日报（由智能体完成）
# - 按主题分类
# - 生成每日摘要
# - 输出：daily-report-2024-01-15.md
```
