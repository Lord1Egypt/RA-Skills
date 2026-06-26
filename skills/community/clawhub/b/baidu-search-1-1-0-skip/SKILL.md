---
name: baidu-search
description: Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# Baidu Search

Search the web via Baidu AI Search API.

## 调用方式

### 方式一：通过文件路径传参（推荐）

将 JSON 写入临时文件，脚本会自动读取并处理 UTF-8 BOM：

```powershell
# PowerShell 中使用
$json = @{
    query = "搜索关键词"
    search_recency_filter = "day"
} | ConvertTo-Json -Compress
[System.IO.File]::WriteAllText("$env:TEMP\baidu_req.json", $json, [System.Text.Encoding]::UTF8)
python.exe "skills\baidu-search-1-1-0\scripts\search.py" "$env:TEMP\baidu_req.json"
```

### 方式二：直接传递 JSON 字符串

```bash
python skills/baidu-search/scripts/search.py '{"query":"关键词","search_recency_filter":"day"}'
```

⚠️ 注意：在 Windows PowerShell 下，直接传参可能因转义问题失败，建议使用方式一。

### 方式三：通过 stdin 管道传递

```bash
echo '{"query":"关键词"}' | python skills/baidu-search/scripts/search.py
```

## 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | 是 | - | 搜索关键词 |
| edition | string | 否 | standard | `standard`（完整版）或 `lite`（精简版） |
| resource_type_filter | array | 否 | web:20 | 资源类型过滤：`web`（最多50）、`video`（最多10）、`image`（最多30）、`aladdin`（最多5） |
| search_filter | object | 否 | - | 高级过滤器（见下文） |
| block_websites | array | 否 | - | 屏蔽的网站，如 `["tieba.baidu.com"]` |
| search_recency_filter | string | 否 | year | 时间过滤：`week`、`month`、`semiyear`、`year` |
| safe_search | boolean | 否 | false | 启用严格内容过滤 |

## SearchFilter 高级过滤器

| 参数 | 类型 | 说明 |
|------|------|------|
| match.site | array | 限制在特定网站，如 `["baike.baidu.com"]` |
| range.pageTime | object | 页面时间范围（见下文） |

### 日期范围格式

- 固定日期：`YYYY-MM-DD`
- 相对时间：`now-1w/d`、`now-1M/d`、`now-1y/d`

| 操作符 | 含义 |
|--------|------|
| gte | 大于等于（起始） |
| lte | 小于等于（结束） |

## 使用示例

```bash
# 基础搜索
python skills/baidu-search/scripts/search.py '{"query":"人工智能"}'

# 按时间过滤
python skills/baidu-search/scripts/search.py '{"query":"最新新闻","search_recency_filter":"week"}'

# 按时间和网站过滤
python skills/baidu-search/scripts/search.py '{
  "query":"最新新闻",
  "search_recency_filter":"week",
  "search_filter":{"match":{"site":["news.baidu.com"]}}
}'

# 资源类型过滤
python skills/baidu-search/scripts/search.py '{
  "query":"旅游景点",
  "resource_type_filter":[{"type":"web","top_k":20},{"type":"video","top_k":5}]
}'
```

## 已知问题与解决方案

### 1. PowerShell JSON 转义问题

**问题**：PowerShell 直接传递 JSON 字符串给 Python 时，单引号/双引号可能被错误解析。

**解决**：使用临时文件方式传递参数。

### 2. UTF-8 BOM 导致 JSON 解析失败

**问题**：部分工具写入文件时会添加 BOM（`\ufeff`），导致 `json.loads()` 解析失败。

**解决**：脚本已内置 BOM 自动处理，调用方无需额外处理。

### 3. 中文输出乱码

**问题**：Windows 终端默认使用 GBK 编码，中文字符输出时可能显示为乱码。

**解决**：脚本已设置 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`，输出时自动转换。

## 当前状态

✅ 功能正常，支持文件路径/stdin/直接参数三种调用方式，自动处理 UTF-8 BOM 和输出编码。
