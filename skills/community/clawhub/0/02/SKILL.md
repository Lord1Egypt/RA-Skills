---
name: "web-search"
version: "1.0.0"
description: "安全的网络搜索工具，支持多个搜索引擎"
author: "AI Skills Team"
tags: ["搜索", "联网", "DuckDuckGo", "Wikipedia"]
requires: []
---

# AI联网搜索技能

安全的网络搜索工具，支持多个搜索引擎，无需API密钥。

## 技能描述

提供免费的网络搜索功能，支持DuckDuckGo和Wikipedia等搜索引擎，内置结果缓存机制（24小时），保护用户隐私。

## 使用场景

- 用户问："Python最新版本是什么？" → 搜索并返回结果
- 用户说："搜索人工智能的最新进展" → 获取相关资讯
- 用户问："什么是量子计算？" → 搜索Wikipedia百科
- 用户说："查找Python教程" → 返回搜索结果

## 工具和依赖

### 工具列表

- `scripts/web_search.py`：核心搜索模块

### API密钥

无（使用免费搜索引擎）

### 外部依赖

- Python 3.7+
- duckduckgo-search
- beautifulsoup4
- requests

## 配置说明

### 环境变量

```bash
# 可选：付费搜索引擎API
export SERPER_API_KEY="your-key"  # Serper API
export BRAVE_API_KEY="your-key"   # Brave Search API
```

### 数据存储位置

缓存：`~/.ai_search_cache.db`（24小时有效期）

## 使用示例

### 基本用法

```python
from web_search import WebSearchTool

# 创建搜索工具
search = WebSearchTool()

# 综合搜索
results = search.search("Python编程", engines=['duckduckgo', 'wikipedia'])

# 快速搜索（格式化输出）
print(search.quick_search("人工智能"))
```

### 场景1：综合搜索

用户："搜索Python编程教程"

AI：
```python
results = search.search("Python编程", engines=['duckduckgo'])
# 返回前10个结果，包含标题、链接、摘要
```

### 场景2：百科查询

用户："什么是量子计算？"

AI：
```python
results = search.search("量子计算", engines=['wikipedia'])
# 返回Wikipedia摘要
```

### 场景3：使用缓存

用户："再次搜索Python"（短时间内重复搜索）

AI：
```python
# 从缓存返回结果，提高速度
results = search.search("Python")
# 结果来源：缓存
```

## 故障排除

### 问题1：DuckDuckGo搜索失败

**现象**：搜索无结果或报错

**解决**：
1. 检查网络连接
2. DuckDuckGo有请求频率限制，稍后重试
3. 尝试切换到Wikipedia引擎

### 问题2：缓存过期

**现象**：搜索结果较旧

**解决**：
```python
# 清除缓存
rm ~/.ai_search_cache.db
```

### 问题3：搜索结果不相关

**现象**：返回结果与问题不符

**解决**：
1. 使用更精确的关键词
2. 尝试不同的搜索引擎
3. 使用付费API获得更好结果（可选）

## 注意事项

1. **请求频率**：DuckDuckGo免费API有频率限制
2. **结果时效**：搜索结果仅供参考，请自行验证
3. **缓存机制**：24小时内的重复搜索会返回缓存结果
4. **隐私保护**：搜索缓存存储在本地，不上传云端
