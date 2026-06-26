# AI News Hub - 安装指南

## 系统要求

- Python 3.8+
- 依赖包（可选）：`feedparser`（更好的RSS解析）

## 安装步骤

### 方式1：使用OpenClaw Skill（推荐）

如果已安装此技能，直接使用即可：

```
用户：今天有什么AI新闻？
助手：📰 今日AI新闻速递（自动聚合）
```

### 方式2：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/lanyasheng/ai-news-aggregator.git
cd ai-news-aggregator/scripts

# 2. 安装依赖（可选，提升性能）
pip3 install feedparser

# 3. 测试运行
python3 rss_aggregator.py --category all --days 1 --limit 5 --json
```

## 使用方法

### 基础命令

```bash
# 查看所有分类的最新新闻
python3 rss_aggregator.py --category all --days 1 --limit 10

# 只看公司博客
python3 rss_aggregator.py --category company --days 1 --limit 5

# 只看论文
python3 rss_aggregator.py --category papers --days 3 --limit 10

# 只看中文媒体
python3 rss_aggregator.py --category cn_media --days 3 --limit 10

# AI Agent 相关
python3 rss_aggregator.py --category ai-agent --days 7 --limit 10
```

### arXiv 论文搜索

```bash
# 最新AI论文（按热度排序）
python3 arxiv_papers.py --limit 5 --top 10

# 搜索特定主题
python3 arxiv_papers.py --query "multi-agent" --limit 5

# 搜索特定领域
python3 arxiv_papers.py --query "NLP" --limit 10
```

### GitHub Trending

```bash
# AI相关热门项目（今日）
python3 github_trending.py --ai-only

# 本周热门
python3 github_trending.py --since weekly
```

## 输出格式

### JSON 格式
```bash
python3 rss_aggregator.py --category all --days 1 --json
```

输出示例：
```json
{
  "timestamp": "2026-04-14T10:00:00+08:00",
  "total": 32,
  "items": [...]
}
```

### 默认文本格式
```bash
python3 rss_aggregator.py --category all --days 1
```

输出示例：
```
📰 AI新闻聚合
━━━━━━━━━━━━━━━━━━━━━━━━
【公司动态】
• OpenAI 发布 GPT-5 预览版 | 2小时前

【论文发布】
• arXiv: 多智能体协作综述（热榜第一）

【GitHub热门】
• langchain/langchain: 🔥 本周最热 +1200 stars
```

## 性能优化

### 缓存机制
- 首次抓取后自动缓存（ETag/Last-Modified）
- 缓存有效期：1小时
- 重复抓取：秒级完成

### 并发优化
- 10线程并发抓取
- 15秒快速超时
- 100源12秒完成

## 故障排除

### 问题1：抓取超时
```bash
# 减少并发线程数
export THREAD_POOL_SIZE=5
python3 rss_aggregator.py --category all
```

### 问题2：某些源无法访问
```bash
# 只抓取可用的源
python3 rss_aggregator.py --category company --fast-fail
```

### 问题3：日期过滤不生效
```bash
# 确保使用 --days 参数
python3 rss_aggregator.py --category all --days 3
```

## 高级用法

### 自定义RSS源

编辑 `scripts/rss_sources.json`：

```json
{
  "name": "你的自定义源",
  "url": "https://example.com/feed.xml",
  "category": "custom"
}
```

### 生成日报脚本

```bash
#!/bin/bash
# 每天早上8点生成AI早报
python3 scripts/rss_aggregator.py --category all --days 1 --limit 20 > /tmp/ai-daily-$(date +%Y%m%d).txt
```

### 定时任务

```cron
# 每天8点生成早报
0 8 * * * python3 /path/to/ai-news-aggregator/scripts/rss_aggregator.py --category all --days 1 > /tmp/ai-news.txt

# 每周一9点生成周报
0 9 * * 1 python3 /path/to/ai-news-aggregator/scripts/rss_aggregator.py --category all --days 7 > /tmp/ai-weekly.txt
```

## 技术支持

- GitHub Issues: https://github.com/lanyasheng/ai-news-aggregator/issues
- 文档: SKILL.md
- 测试：`python3 -m unittest test_rss_aggregator.py -v`
