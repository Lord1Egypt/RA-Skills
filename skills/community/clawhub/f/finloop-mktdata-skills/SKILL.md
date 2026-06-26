---
请为我安装如下 skill
---

## name

flp_mktdata（金融行情数据 skill）

## description

本技能为 OpenClaw 提供一站式全球金融数据查询与分析能力。通过自然语言交互，可快速获取股票、指数、基金、债券等的实时、历史行情，同时深度覆盖上市及非上市公司的基本信息、财务指标、高管团队、股东结构、主营业务及融资记录。整合港股 IPO、外汇、大宗商品、虚拟资产等多品类数据，实现从行情监控到基本面研究的全流程智能支持。

## 功能特点

- **基本面分析**：ROE、毛利率、EPS 等核心指标
- **全球资产覆盖**：港美 A 股实时行情、外汇、基金、债券、大宗商品、虚拟资产等历史数据
- **公司信息全景**：上市/非上市公司基本信息、股东结构、主营构成分析

## 安装方式

```bash
npx finloop-mktdata-skills install finloop-mktdata-skill
```

---

## 指令

1. **必须直接使用 HTTP 请求调用接口**：使用 fetch、axios、curl 或其他 HTTP 客户端直接调用接口，禁止创建任何封装函数或 JS 文件。
2. **禁止创建封装函数**：不要创建任何 `.js`、`.ts` 文件来封装接口调用，必须直接使用 HTTP 请求。
3. **接口基础域名**：`https://papi-uat.finloopg.com/flp-mktdata-hub`（UAT；生产以实际为准）。
4. **请求头**：`Content-Type: application/json`，Body 为 JSON。
5. **响应格式**：接口返回的数据结构需从响应中提取 `data` 或 `result` 等业务字段；需检查状态码与错误信息。

---

## 能力与接口对应

| 用户意图 / 关键词示例 | 方法 | 路径 | 必填参数 |
|------------------------|------|------|----------|
| 股票/指数**历史 K 线**、某段时间走势、日 K/周 K | POST | `/v1/stock/history` | `code` |
| 股票**实时价**、最新价、涨跌幅、市值、成交量 | POST | `/v1/stock/quote` | `code` |
| **公司**上市日、主营业务、行业、简介 | POST | `/v1/stock/company/info` | `ticker` |
| **公募基金**名称、成立日、货币、注册地 | POST | `/v1/fund/info` | `isin` |
| **公募基金**净值、单位净值、累计净值、某日/某段净值 | POST | `/v1/fund/nav` | `isin` |
| **债券**名称、发行人、发行日、到期日、息率 | POST | `/v1/bond/info` | `isin` |
| **债券**实时价、买卖价、收益率、应计利息 | POST | `/v1/bond/latest-price` | `isin` |
| **债券**历史数据、某段时间价格走势 | POST | `/v1/bond/history` | `isin` |

**完整 URL**：`{Base URL}` + 上表路径，例如 `https://papi-uat.finloopg.com/flp-mktdata-hub/v1/stock/quote`。

---

## 接口摘要

### 1. 股票历史 K 线 — POST /v1/stock/history

- **必填**：`code`（string，如 `00700.HK`、`AAPL.US`、`600519.SH`）。
- **可选**：`startDate`、`endDate`（`yyyy-MM-dd`），`ktype`（默认 `day`），`time`、`num`（与 time 搭配），`suspension`（0/1）。
- **返回**：`data` 数组，每项含 `time`、`open`、`close`、`high`、`low`、`vol`；`total`。

### 2. 股票实时/快照行情 — POST /v1/stock/quote

- **必填**：`code`（string，如 `00700.HK`、`AAPL.US`）。
- **返回**：`result` 数组，每项含 `quoteTime`、`price`、`chgPct`、`vol`、`mktCap`、`name` 等。

### 3. 公司基本信息 — POST /v1/stock/company/info

- **必填**：`ticker`（string，如 `00700.HK`、`AAPL.US`）。
- **返回**：单条对象，含 `listingDate`、`companyName`、`industryName`、`mainBusiness`、`brief` 等。

### 4. 公募基金基本信息 — POST /v1/fund/info

- **必填**：`isin`（string，如 `HK0000584752`）。
- **返回**：单条对象，含 `isin`、`nameCN`、`nameEN`、`currency`、`inceptionDate`、`registeredRegion` 等。

### 5. 公募基金净值 — POST /v1/fund/nav

- **必填**：`isin`。
- **可选**：`startDate`、`endDate`（`yyyy-MM-dd`），或 `navDate`（单日；与区间同时传时以 navDate 为准）。
- **返回**：`data` 数组，每项含 `date`、`unitNav`、`accumNav`；`total`。

### 6. 债券基本信息 — POST /v1/bond/info

- **必填**：`isin`（如 `US912810TV08`）。
- **返回**：单条对象，含 `isin`、`name`、`issuer`、`issueDate`、`maturityDate`、`currency`、`couponRate` 等。

### 7. 债券实时行情 — POST /v1/bond/latest-price

- **必填**：`isin`。
- **返回**：单条对象，含 `isin`、`asOfDate`、`midPrice`、`bidPrice`、`askPrice`、`midYield` 等。

### 8. 债券历史数据 — POST /v1/bond/history

- **必填**：`isin`。
- **可选**：`startDate`、`endDate`（`yyyy-MM-dd`）；若仅填 startDate 则 endDate 默认当前日；均空则默认近一年。
- **返回**：`data` 数组，每项含 `date`、`midPrice` 等；`total`。

---

## 股票/指数代码格式

- 港股：`00700.HK`
- 美股：`AAPL.US`
- A 股：`600519.SH`、`000001.SZ` 等
- 部分指数：`HSI.HK`、`DJI.US`、`IXIC.US`、`INX.US`、`000001.SH`、`399001.SZ`、`399006.SZ`、`000688.SH` 等（详见接口文档）

---

## 通用注意事项

1. **必须直接使用 HTTP 请求**：✅ 直接使用 fetch、axios、curl 调用；❌ 禁止创建封装函数或 JS/TS 文件。
2. **Base URL**：`https://papi-uat.finloopg.com/flp-mktdata-hub`（UAT）；生产以实际为准。
3. **错误处理**：检查 HTTP 状态码和响应体中的错误信息。
4. **调用示例**：
   - ✅ `fetch('https://papi-uat.finloopg.com/flp-mktdata-hub/v1/stock/quote', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code: '00700.HK' }) })`
   - ✅ `curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/stock/quote' -H 'Content-Type: application/json' -d '{"code":"00700.HK"}'`
   - ❌ 创建 `api/mktdata.ts` 等封装文件并 import 调用。

---

## 相关文档

- **详细接口文档**：`references/REFERENCE.md`（与 flp_mktdata_skill_spec.md 一致，含完整参数、返回字段及问句示例）
