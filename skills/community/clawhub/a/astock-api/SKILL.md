---
name: astock-api
description: "A股实时行情、K线技术指标、资金流向、财务数据查询。支持任意A股代码，返回结构化数据。"
homepage: https://api.jyfg.de5.net:2096
license: MIT
tags: "finance,stock,china,A股,行情,股票,数据API"
version: "1.0.1"
---

# A股数据查询 (A-Share Stock API)

通过HTTP API查询A股实时行情、技术指标、资金流向和财务数据。单次查询返回完整字段，无需处理多数据源拼接。

## 可用端点（14个）

| 端点 | 说明 |
|------|------|
| `/v1/quote` | 实时行情（最新价/涨跌幅/量比/换手率/PE等） |
| `/v1/kline` | K线+技术指标(MA/MACD/KDJ) |
| `/v1/flow` | 资金流向(主力/大单/中单/小单) |
| `/v1/finance` | 财务数据(营收/净利/增长率) |
| `/v1/concept` | 概念板块列表(486个) |
| `/v1/limit/up` | 涨停池 |
| `/v1/limit/down` | 跌停池 |
| `/v1/blocktrade` | 大宗交易 |
| `/v1/hk/company` | 港股公司信息 |
| `/v1/macro/gdp` | GDP季度数据 |
| `/v1/macro/cpi` | CPI月度数据 |
| `/v1/macro/pmi` | PMI数据 |
| `/v1/macro/money` | 货币供应量 |
| `/v1/etf/prices` | ETF价格 |

## 基础地址

```
https://api.jyfg.de5.net:2096
```

## 认证

请求头 `X-API-Key` 或 URL参数 `token` 携带 API Key

### 免费体验Token

安装后即可使用以下Token测试，无需申请：

```
token = trial_free_2026
```

- 每分钟限制：30次
- 每日限制：**500次**
- 覆盖所有端点的体验

如需更高调用次数，请联系作者获取专属Token。

## 调用示例

```bash
# 茅台实时行情
curl "https://api.jyfg.de5.net:2096/v1/quote?code=600519&token=trial_free_2026"

# 资金流向
curl "https://api.jyfg.de5.net:2096/v1/flow?code=600207&token=trial_free_2026"

# 今日涨停池
curl "https://api.jyfg.de5.net:2096/v1/limit/up?token=trial_free_2026"

# 最新GDP数据
curl "https://api.jyfg.de5.net:2096/v1/macro/gdp?token=trial_free_2026"

# 港股腾讯信息
curl "https://api.jyfg.de5.net:2096/v1/hk/company?code=00700.HK&token=trial_free_2026"
```

## 响应格式

```json
{
  "数据字段...": "值",
  "cost_s": 0.35
}
```

## 覆盖范围

- **A股主板** (600xxx/000xxx) ✅
- **创业板** (300xxx) ✅
- **科创板** (688xxx) ✅
- **港股** ✅
- **ETF** ✅
- **宏观经济** ✅

## 使用场景

- 量化策略的数据后端
- 个人看盘工具的数据源
- AI交易助手的实时行情接口
- 每日复盘自动生成数据
