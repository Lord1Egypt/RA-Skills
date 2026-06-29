---
name: 股票数据接口服务
description: 基于akshare-one的MCP服务器，提供中国股票市场数据的全面接口，包括历史数据、实时数据、新闻数据和财务报表等金融信息。
version: 1.0.0
---

# 股票数据接口服务

基于akshare-one的MCP服务器，提供中国股票市场数据的全面接口，包括历史数据、实时数据、新闻数据和财务报表等金融信息。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Get historical stock market data. 'eastmoney_direct' support all A,B,H shares | `scripts.tools.get_hist_data` |
| Get real-time stock market data. 'eastmoney_direct' support all A,B,H shares | `scripts.tools.get_realtime_data` |
| Get stock-related news data. | `scripts.tools.get_news_data` |
| Get company balance sheet data. | `scripts.tools.get_balance_sheet` |
| Get company income statement data. | `scripts.tools.get_income_statement` |
| Get company cash flow statement data. | `scripts.tools.get_cash_flow` |
| Get company insider trading data. | `scripts.tools.get_inner_trade_data` |
| Get key financial metrics from the three major financial statements. | `scripts.tools.get_financial_metrics` |
| Get current time with ISO format, timestamp, and the last trading day. | `scripts.tools.get_time_info` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_hist_data
工具描述：Get historical stock market data. 'eastmoney_direct' support all A,B,H shares
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |Stock symbol/ticker (e.g. '000001')|
|interval|string|false|"day"|Time interval|
|interval_multiplier|integer|false|1.0|Interval multiplier|
|start_date|string|false|"1970-01-01"|Start date in YYYY-MM-DD format|
|end_date|string|false|"2030-12-31"|End date in YYYY-MM-DD format|
|adjust|string|false|"none"|Adjustment type|
|source|string|false|"eastmoney"|Data source|
|indicators_list|null|false| |Technical indicators to add|
|recent_n|null|false|100.0|Number of most recent records to return|

---

## scripts.tools.get_realtime_data
工具描述：Get real-time stock market data. 'eastmoney_direct' support all A,B,H shares
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|null|false| |Stock symbol/ticker (e.g. '000001')|
|source|string|false|"eastmoney_direct"|Data source|

---

## scripts.tools.get_news_data
工具描述：Get stock-related news data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |Stock symbol/ticker (e.g. '000001')|
|recent_n|null|false|10.0|Number of most recent records to return|

---

## scripts.tools.get_balance_sheet
工具描述：Get company balance sheet data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |Stock symbol/ticker (e.g. '000001')|
|recent_n|null|false|10.0|Number of most recent records to return|

---

## scripts.tools.get_income_statement
工具描述：Get company income statement data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |Stock symbol/ticker (e.g. '000001')|
|recent_n|null|false|10.0|Number of most recent records to return|

---

## scripts.tools.get_cash_flow
工具描述：Get company cash flow statement data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |Stock symbol/ticker (e.g. '000001')|
|source|string|false|"sina"|Data source|
|recent_n|null|false|10.0|Number of most recent records to return|

---

## scripts.tools.get_inner_trade_data
工具描述：Get company insider trading data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |Stock symbol/ticker (e.g. '000001')|

---

## scripts.tools.get_financial_metrics
工具描述：Get key financial metrics from the three major financial statements.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |Stock symbol/ticker (e.g. '000001')|
|recent_n|null|false|10.0|Number of most recent records to return|

---

## scripts.tools.get_time_info
工具描述：Get current time with ISO format, timestamp, and the last trading day.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据