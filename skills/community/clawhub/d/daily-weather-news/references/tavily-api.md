# Tavily Search API 文档

## 概述
Tavily Search API 是一个AI优化的网络搜索工具，专为AI agents设计，提供精准、结构化的搜索结果。

## 基本用法
```bash
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "搜索查询" --topic news --days 1
```

### 命令参数
- `--topic`: 搜索主题 (news, general, images等)
- `--days`: 搜索时间范围 (天数)
- `--maxResults`: 最大结果数量
- `--language`: 语言设置 (可选)

## 中文新闻搜索策略

### 推荐搜索模式
```bash
# 中文新闻网站搜索
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "site:news.cn 今日国际新闻 OR site:xinhuanet.com 国际新闻 OR site:people.com.cn 国际新闻" --topic news --days 1

# 综合中文新闻搜索
node ~/.openclaw/workspace/skills/tavily-search/scripts/search.mjs "今日国际重要新闻 中文" --topic news --days 1
```

### 推荐的中文新闻源
- **新华网**: site:xinhuanet.com
- **人民网**: site:people.com.cn  
- **央视网**: site:cctv.com
- **中国新闻网**: site:news.cn

### 搜索结果格式
返回结构化的JSON格式，包含：
- Answer: 搜索结果摘要
- Sources: 详细来源列表
- 每个来源包含URL、标题、相关度等信息

## API密钥配置
```bash
export TAVILY_API_KEY="your-api-key-here"
```

## 错误处理
- API密钥错误：检查TAVILY_API_KEY环境变量
- 网络连接问题：检查网络连接
- 搜索结果为空：尝试调整搜索关键词

## 性能优化
- 使用site:限定搜索范围提高相关性
- 合理设置时间范围避免过时信息
- 使用OR操作符扩大搜索覆盖面