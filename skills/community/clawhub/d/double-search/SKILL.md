---
name: double-search
description: 双搜索功能 (Tavily + Kimi) - 支持并行搜索和结果合并
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["python3"]
      env:
        - TAVILY_API_KEY
        - KIMI_API_KEY
    primaryEnv: "TAVILY_API_KEY"
    install:
      - id: pip
        kind: pip
        packages: ["aiohttp", "python-dotenv"]
        label: "安装Python依赖 (pip)"
---

# Double Search Skill

双重搜索功能，同时使用Tavily和Kimi搜索引擎，提供更全面、准确的搜索结果。

## 功能特性

- ✅ **双引擎并行搜索**：同时使用Tavily和Kimi
- ✅ **智能结果合并**：自动合并、去重和排序
- ✅ **异步高效**：基于asyncio的高性能实现
- ✅ **错误容错**：单个搜索失败不影响整体
- ✅ **灵活配置**：支持环境变量和配置文件

## 快速开始

### 1. 安装Python依赖

```bash
pip install aiohttp python-dotenv
```

### 2. 设置环境变量

在`.env`文件中添加：

```bash
TAVILY_API_KEY=tvly-xxxxxxxxxxxx
KIMI_API_KEY=your_kimi_api_key_here
```

或者设置系统环境变量：

```bash
export TAVILY_API_KEY="tvly-xxxxxxxxxxxx"
export KIMI_API_KEY="your_kimi_api_key_here"
```

### 3. 基本使用

```python
from double_search import DoubleSearcher

async def search_example():
    searcher = DoubleSearcher()

    # 执行搜索
    results = await searcher.search("人工智能发展趋势")

    # 打印结果
    print(f"搜索结果: {results}")

    # 查看各个搜索引擎的结果
    print(f"Tavily结果: {results.get('tavily', [])}")
    print(f"Kimi结果: {results.get('kimi', [])}")

    return results
```

## API文档

### DoubleSearcher类

#### 初始化

```python
searcher = DoubleSearcher()
```

#### search方法

```python
async def search(
    query: str,
    merge_results: bool = True,
    limit_per_source: int = 5
) -> Dict[str, Any]
```

**参数：**
- `query` (str): 搜索查询字符串
- `merge_results` (bool): 是否合并结果（默认True）
- `limit_per_source` (int): 每个搜索源返回的结果数量（默认5）

**返回：**
```json
{
  "query": "搜索内容",
  "merged_results": [
    {
      "title": "结果标题",
      "url": "https://example.com",
      "snippet": "结果摘要",
      "source": "tavily"
    }
  ],
  "source_breakdown": {
    "tavily": [...],
    "kimi": [...]
  }
}
```

## 高级用法

### 1. 不合并结果

```python
results = await searcher.search(
    query="技术趋势",
    merge_results=False
)

# 结果按搜索源分开
print(results['tavily'])
print(results['kimi'])
```

### 2. 限制每个源的结果数量

```python
results = await searcher.search(
    query="市场分析",
    limit_per_source=3
)
```

### 3. 自定义结果处理

```python
results = await searcher.search("投资策略")

# 只获取Tavily的结果
tavily_results = results.get('tavily', [])

# 只获取Kimi的结果
kimi_results = results.get('kimi', [])

# 获取合并的结果
all_results = results.get('merged_results', [])
```

## 配置管理

### 环境变量配置

```bash
# 必需
TAVILY_API_KEY=tvly-xxxxxxxxxxxx

# 可选（不设置则只使用Tavily）
KIMI_API_KEY=your_kimi_api_key_here
```

### 配置文件支持

支持`.env`文件：

```bash
# .env文件示例
TAVILY_API_KEY=tvly-xxxxxxxxxxxx
KIMI_API_KEY=your_kimi_api_key_here
```

## 错误处理

```python
async def safe_search(query: str):
    searcher = DoubleSearcher()

    try:
        results = await searcher.search(query)

        if not results['merged_results']:
            return {"error": "搜索无结果", "query": query}

        return results

    except Exception as e:
        return {"error": f"搜索失败: {str(e)}", "query": query}
```

## 性能优化

### 并行搜索效率

- Tavily和Kimi同时搜索，总时间接近较慢的搜索引擎
- 适合需要全面结果的场景

### 结果缓存

```python
from functools import lru_cache

class CachedSearcher(DoubleSearcher):
    @lru_cache(maxsize=100)
    async def search(self, query: str, ...):
        return await super().search(query, ...)
```

## 使用场景

### 1. 内容创作

```python
async def research_topic(topic):
    searcher = DoubleSearcher()
    results = await searcher.search(topic)

    # 分析多个来源
    insights = analyze_results(results)
    return insights
```

### 2. 财经分析

```python
async def financial_analysis(ticker):
    searcher = DoubleSearcher()
    query = f"{ticker} 财经分析"
    results = await searcher.search(query)

    # 过滤财经相关结果
    financial_news = filter_financial_content(results)
    return financial_news
```

### 3. 代码搜索

```python
async def code_search(problem):
    searcher = DoubleSearcher()
    results = await searcher.search(problem)

    # 优先获取技术相关结果
    technical_results = filter_tech_content(results)
    return technical_results
```

## 故障排除

### 问题1：搜索无结果

```bash
# 检查API keys
echo $TAVILY_API_KEY
echo $KIMI_API_KEY

# 验证API keys有效性
```

### 问题2：Python模块未找到

```bash
# 确保在正确的工作目录
cd ~/.openclaw/skills/double-search

# 检查Python路径
which python3
```

### 问题3：依赖缺失

```bash
# 安装依赖
pip install aiohttp python-dotenv
```

## 版本信息

- **版本**: 1.0.0
- **Python版本**: 3.8+
- **更新日期**: 2026-03-27
- **兼容性**: OpenClaw skill系统
