---
name: douyin-scraper
description: >
  抖音视频内容搜索和爬取工具，支持自然语言查询如"搜索一下海鲜视频"、"找5个最热猫咪搞笑视频"。
  当用户需要搜索抖音视频内容、查找短视频、爬取抖音数据时使用此技能。
  支持中文自然语言解析，可以直接理解用户的搜索意图并提取关键词和过滤条件。
version: 1.0.0
---

# Douyin Scraper - 抖音搜索爬虫

支持自然语言搜索抖音视频内容的工具技能。

## 功能特点

- ✅ **自然语言理解**: 直接理解中文搜索意图，如"搜索一下海鲜视频"
- ✅ **智能解析**: 自动提取关键词、数量、排序方式
- ✅ **多种输出**: 支持文本格式化和 JSON 输出
- ✅ **可扩展**: 可以对接浏览器自动化或抖音开放平台 API

## 触发场景

当用户说以下内容时使用此技能：
- "搜索一下XX视频"
- "找一下XX内容" 
- "帮我搜抖音上的XX"
- "抖音上有什么XX相关的"
- "爬取抖音XX视频"
- 任何包含抖音搜索/查找意图的自然语言查询

## 使用方法

### 1. 解析用户查询

首先使用内置的自然语言解析器理解用户意图：

```python
from scripts.search_douyin import parse_natural_language
parsed = parse_natural_language("搜索一下海鲜视频")
# 返回: {"keyword": "海鲜", "sort": "general", "count": 10, ...}
```

### 2. 执行搜索

```python
from scripts.search_douyin import search_douyin, format_results
results = search_douyin(keyword="海鲜", count=5)
print(format_results(results))
```

### 3. 命令行直接使用

```bash
# 自然语言搜索
python scripts/search_douyin.py "搜索一下海鲜视频"

# 找5个最热猫咪视频
python scripts/search_douyin.py "找5个最热猫咪搞笑视频"

# JSON输出
python scripts/search_douyin.py "海鲜视频" --json
```

## 支持的查询示例

| 用户输入 | 解析结果 |
|---------|---------|
| 搜索一下海鲜视频 | keyword=海鲜, count=10, sort=general |
| 找5个最新猫咪视频 | keyword=猫咪, count=5, sort=latest |
| 帮我搜最热美食探店视频 | keyword=美食探店, sort=most_liked |
| 查找健身教程 | keyword=健身教程 |

## 扩展实现方式

当前版本包含模拟搜索结果。如需实现真实爬取，可以：

### 方案 A: 浏览器自动化 (推荐)

结合 `agent-browser` skill 实现真实浏览器搜索：
```python
# 1. 使用 agent-browser 打开抖音搜索页
# 2. 输入关键词并等待结果
# 3. 提取视频标题、作者、点赞数等信息
```

### 方案 B: 抖音开放平台 API

对接抖音开放平台的搜索接口，需要申请 API Key。

### 方案 C: 第三方数据接口

使用第三方抖音数据服务提供商。

## 输出字段说明

每个视频返回：
- `title`: 视频标题
- `author`: 作者昵称
- `likes`: 点赞数
- `comments`: 评论数
- `shares`: 分享数
- `duration`: 视频时长
- `url`: 视频链接

## 执行流程

1. **识别触发词**: 用户查询包含"抖音"、"搜索"、"找"、"视频"等关键词
2. **解析意图**: 使用 `parse_natural_language()` 解析自然语言
3. **执行搜索**: 调用 `search_douyin()` 获取结果
4. **格式化输出**: 使用 `format_results()` 输出美观结果
5. **提示扩展**: 提醒用户可以配置真实的爬取方案

## 注意事项

- 遵守抖音平台的 robots.txt 和使用条款
- 合理控制请求频率，避免对服务器造成压力
- 仅供学习和研究使用，请勿用于商业用途
- 大规模爬取建议使用官方开放平台接口
