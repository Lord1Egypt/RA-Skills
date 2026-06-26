---
name: duckduckgo-search
description: Search the web using DuckDuckGo. No API key required. Supports instant answers and HTML scraping modes. Privacy-focused search alternative.
homepage: https://duckduckgo.com
metadata:
  openclaw:
    emoji: "🦆"
    requires:
      bins: ["python3"]
---

# DuckDuckGo Search Skill

使用 DuckDuckGo 进行隐私保护的网页搜索，**无需 API Key**。

## 特点

- ✅ **无需 API Key** - 直接使用
- ✅ **隐私保护** - 不追踪用户
- ✅ **两种模式** - Instant API / HTML Scraping
- ✅ **免费无限制** - 无配额限制

---

## 使用方法

### 基本搜索

```bash
python3 scripts/duckduckgo_search.py "搜索关键词"
```

### 指定结果数量

```bash
python3 scripts/duckduckgo_search.py "Python 教程" -n 10
```

### 选择搜索模式

```bash
# Instant 模式（快速，适合事实性问题）
python3 scripts/duckduckgo_search.py "Python 是什么" --mode instant

# HTML 模式（完整搜索结果）
python3 scripts/duckduckgo_search.py "Python 教程" --mode html
```

### 带关键信息总结

```bash
python3 scripts/duckduckgo_search.py "伊朗局势" --summarize
```

### JSON 输出

```bash
python3 scripts/duckduckgo_search.py "API" --json
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索关键词（必需） | - |
| `-n, --top-k` | 返回结果数量 | 5 |
| `--mode` | 搜索模式：`instant` / `html` | `html` |
| `--fetch-content` | 抓取网页内容（仅 html） | false |
| `--summarize` | 生成关键信息总结 | false |
| `--json` | 输出原始 JSON | false |

---

## 搜索模式对比

| 模式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **Instant** | 快速、稳定 | 结果有限 | 事实性问题、定义查询 |
| **HTML** | 完整搜索结果 | 可能被反爬 | 一般搜索、需要多个结果 |

### Instant 模式示例

```bash
python3 scripts/duckduckgo_search.py "Python 编程语言"
```

**输出**：
```
🔍 DuckDuckGo 搜索结果 (3 条)
============================================================

1. Python (programming language) - Wikipedia
   🔗 https://en.wikipedia.org/wiki/Python_(programming_language)
   📝 Python is a high-level, general-purpose programming language...
   📊 来源：instant

2. Python.org
   🔗 https://www.python.org/
   📝 The official home of the Python Programming Language...
   📊 来源：instant
```

### HTML 模式示例

```bash
python3 scripts/duckduckgo_search.py "Python 入门教程" --mode html -n 10
```

---

## 输出格式

### 标准输出（默认）

```
🔍 DuckDuckGo 搜索结果 (5 条)
============================================================

1. 标题
   🔗 https://example.com
   📝 内容摘要...
   📊 来源：instant/html
```

### JSON 输出

```json
[
  {
    "title": "标题",
    "url": "https://example.com",
    "snippet": "摘要",
    "source": "instant",
    "type": "abstract"
  }
]
```

---

## 在 OpenClaw 中使用

### 自动搜索（根据 SOUL.md）

```
搜一下 Python 教程
```

### 手动调用

```bash
exec("python3 skills/duckduckgo-search/scripts/duckduckgo_search.py '关键词' -n 5")
```

---

## 限制与注意事项

### ⚠️ 速率限制

- DuckDuckGo 没有官方 API，使用 HTML 端点可能被限制
- 建议请求间隔 2-5 秒
- 大量请求可能触发 403 错误

### ⚠️ 结果质量

- **Instant 模式**：只返回"即时答案"和相关主题，不是完整搜索
- **HTML 模式**：返回完整结果，但解析可能不稳定

### ⚠️ 反爬虫

- DuckDuckGo 可能检测并阻止自动化请求
- 如遇 403 错误，稍后重试
- 生产环境建议使用官方 API（如 Tavily、Brave）

---

## 与 Tavily 搜索对比

| 特性 | DuckDuckGo | Tavily |
|------|------------|--------|
| **API Key** | 不需要 | 需要 |
| **成本** | 免费 | 免费额度 + 付费 |
| **结果质量** | 一般 | 优秀（AI 总结） |
| **稳定性** | 一般 | 高 |
| **适用场景** | 轻量搜索 | 生产环境 |

**建议**：
- 日常轻量搜索 → DuckDuckGo
- 生产环境/高质量需求 → Tavily

---

## 故障排除

### 问题 1：无搜索结果

**原因**：Instant API 没有相关答案  
**解决**：切换到 HTML 模式
```bash
python3 scripts/duckduckgo_search.py "关键词" --mode html
```

### 问题 2：403 Forbidden

**原因**：被 DuckDuckGo 限制  
**解决**：
1. 等待几分钟后重试
2. 降低请求频率
3. 使用代理 IP

### 问题 3：URL 无法访问

**原因**：DuckDuckGo 重定向链接未正确解析  
**解决**：检查 `extract_real_url()` 函数

---

## 示例查询

```bash
# 事实性问题（Instant 模式）
python3 scripts/duckduckgo_search.py "Python 是谁创造的"

# 教程搜索（HTML 模式）
python3 scripts/duckduckgo_search.py "Python 入门教程" --mode html -n 10

# 技术文档
python3 scripts/duckduckgo_search.py "Python requests 库用法" --mode html

# 获取 JSON 用于程序处理
python3 scripts/duckduckgo_search.py "API" --json
```

---

## 相关技能

- **tavily-search** - AI 增强搜索（推荐用于生产）
- **web_search** - OpenClaw 内置搜索（需 Brave API）
- **web_fetch** - 网页内容提取

---

*基于 DuckDuckGo 公开端点，仅供学习使用。生产环境建议使用官方 API。*
