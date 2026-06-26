---
name: cn-stock-announcements
description: "A tool to query Chinese listed company announcements from SZSE (Shenzhen Stock Exchange) and SSE (Shanghai Stock Exchange). Supports single/batch stock queries, keyword searches, and exact time-range filtering."
---

# Chinese Stock Announcements (SZSE & SSE)

这个技能用于查询中国A股上市公司（上交所、深交所）的官方信息披露与公告。它可以作为独立脚本供人类或大模型使用，也可以作为 OpenClaw 插件直接集成在 Python 代码中。

## 使用场景

- 用户需要查询某只特定股票（如平安银行 000001、浦发银行 600000）的最新公告时。
- 用户想批量追踪多只股票的动向时。
- 用户想通过**关键词**（如"年报"、"重组"、"分红"）来搜索两市所有相关的公告时。
- 用户需要限定特定的时间范围（精确到时分秒）来过滤公告时。

## 工作流程

当用户请求查询股票公告时，大模型应该直接调用本项目提供的 `stock_plugin.py` 脚本来获取数据，并格式化输出给用户。

### 方式一：命令行/脚本直接调用 (CLI)
你可以直接执行 Python 代码来调用该模块：

```bash
# 例子：查询包含关键词且在指定时间内的公告
python3 -c "
import json
from stock_plugin import StockAnnouncementPlugin
plugin = StockAnnouncementPlugin()
res = plugin.query_announcements(
    keyword='年报',
    start_date='2024-03-15 00:00:01',
    end_date='2024-03-16 00:00:01',
    limit=5
)
print(json.dumps(res, indent=2, ensure_ascii=False))
"
```

### 方式二：在 OpenClaw 工作流中调用 (Python 代码编写)
如果用户要求你编写一段使用该功能的 OpenClaw 代码，你可以按照以下方式组织代码：

```python
from openclaw2 import OpenClaw
from stock_plugin import StockAnnouncementPlugin

# 初始化 OpenClaw 客户端
client = OpenClaw.remote(api_key="your_api_key")

# 安装股票公告查询插件
client.use(StockAnnouncementPlugin())

# 让大模型 Agent 调用插件获取数据
results = client.pipeline([
    "请帮我查询 000001 和 600000 从 2024-03-15 00:00:01 到 2024-03-16 00:00:01 发布关于「年报」的公告"
])

print(results[-1])
```

## 参数说明

`StockAnnouncementPlugin.query_announcements` 支持以下参数：

| 参数 | 类型 | 说明 | 示例 |
|---|---|---|---|
| `stock_codes` | `List[str]` | 股票代码列表（可选） | `["000001", "600000"]` |
| `keyword` | `str` | 搜索关键词（可选） | `"年报"` |
| `start_date` | `str` | 起始时间（精确到秒或天） | `"2024-03-15 00:00:01"` 或 `"2024-03-15"` |
| `end_date` | `str` | 结束时间（精确到秒或天） | `"2024-03-16 00:00:01"` 或 `"2024-03-16"` |
| `limit` | `int` | 单个交易所返回的最大结果数 | `10` (默认) |

### ⚠️ 时间过滤规则注意：
1. **深交所 (SZSE)**：原生 API 请求体支持传入日期(`YYYY-MM-DD`)获取粗略范围，随后通过脚本在本地自动进行**精确到时分秒**的二次过滤筛选。
2. **上交所 (SSE)**：原生 API 仅支持日期级别(`YYYY-MM-DD`)的检索和返回，所以插件会自动截取传入时间的日期部分进行检索。上交所数据由于没有时分秒属性，不支持秒级精确过滤。

## 技能资源
- `stock_plugin.py`：核心逻辑文件，包含 `StockAnnouncementPlugin` 类及沪深两市的抓取和过滤逻辑。使用标准 requests 库实现，无需复杂环境。

## 前置条件
需要安装 requests 库：
```bash
pip install requests
```
