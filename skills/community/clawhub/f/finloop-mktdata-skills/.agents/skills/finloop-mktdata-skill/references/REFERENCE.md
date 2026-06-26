# 金融行情数据 Skill 接口参考 (flp_mktdata)

与 **flp_mktdata_skill_spec.md** 一致，供本 skill 详细查阅。Base URL：`https://papi-uat.finloopg.com/flp-mktdata-hub`。请求均为 `POST`，`Content-Type: application/json`，Body 为 JSON。

---

## 能力与接口对应

| 用户意图 / 关键词示例 | 路径 | 必填参数 |
|------------------------|------|----------|
| 股票/指数历史 K 线、某段时间走势、日 K/周 K | `POST /v1/stock/history` | `code` |
| 股票实时价、最新价、涨跌幅、市值、成交量 | `POST /v1/stock/quote` | `code` |
| 公司上市日、主营业务、行业、简介 | `POST /v1/stock/company/info` | `ticker` |
| 公募基金名称、成立日、货币、注册地 | `POST /v1/fund/info` | `isin` |
| 公募基金净值、单位/累计净值、某日/某段净值 | `POST /v1/fund/nav` | `isin` |
| 债券名称、发行人、发行日、到期日、息率 | `POST /v1/bond/info` | `isin` |
| 债券实时价、买卖价、收益率、应计利息 | `POST /v1/bond/latest-price` | `isin` |
| 债券历史数据、某段时间价格走势 | `POST /v1/bond/history` | `isin` |

---

## 功能接口一：股票历史 K 线

- **路径**：`/v1/stock/history`
- **必填**：`code`（如 `00700.HK`、`AAPL.US`、`600519.SH`）
- **可选**：`startDate`、`endDate`（yyyy-MM-dd），`ktype`（默认 day），`time`、`num`，`suspension`（0/1）
- **返回**：`data[]`（time, open, close, high, low, vol），`total`
- **指数示例**：HSI.HK、DJI.US、IXIC.US、INX.US、000001.SH、399001.SZ、399006.SZ、000688.SH

---

## 功能接口二：股票实时/快照行情

- **路径**：`/v1/stock/quote`
- **必填**：`code`
- **返回**：`result[]`（quoteTime, price, chgPct, vol, mktCap, name）

---

## 功能接口三：公司基本信息

- **路径**：`/v1/stock/company/info`
- **必填**：`ticker`（如 00700.HK、AAPL.US）
- **返回**：listingDate, companyName, englishName, industryName, mainBusiness, brief

---

## 功能接口四：公募基金基本信息

- **路径**：`/v1/fund/info`
- **必填**：`isin`（如 HK0000584752）
- **返回**：isin, nameCN, nameEN, currency, inceptionDate, registeredRegion

---

## 功能接口五：公募基金净值

- **路径**：`/v1/fund/nav`
- **必填**：`isin`
- **可选**：`startDate`、`endDate`，或 `navDate`（单日；与区间同传时以 navDate 为准）
- **返回**：`data[]`（date, unitNav, accumNav），`total`

---

## 功能接口六：债券基本信息

- **路径**：`/v1/bond/info`
- **必填**：`isin`（如 US912810TV08）
- **返回**：isin, name, nameEn, issuer, issueDate, maturityDate, currency, couponRate

---

## 功能接口七：债券实时行情

- **路径**：`/v1/bond/latest-price`
- **必填**：`isin`
- **返回**：isin, asOfDate, midPrice, bidPrice, askPrice, midYield

---

## 功能接口八：债券历史数据

- **路径**：`/v1/bond/history`
- **必填**：`isin`
- **可选**：`startDate`、`endDate`（仅 startDate 时 endDate 默认当前日；均空默认近一年）
- **返回**：`data[]`（date, midPrice），`total`

---

## 请求示例（curl）

```bash
# 股票实时
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/stock/quote' \
  -H 'Content-Type: application/json' -d '{"code":"00700.HK"}'

# 股票历史
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/stock/history' \
  -H 'Content-Type: application/json' -d '{"code":"00700.HK","startDate":"2025-03-10","endDate":"2025-03-12"}'

# 公司信息
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/stock/company/info' \
  -H 'Content-Type: application/json' -d '{"ticker":"00700.HK"}'

# 基金信息 / 净值
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/fund/info' \
  -H 'Content-Type: application/json' -d '{"isin":"HK0000584752"}'
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/fund/nav' \
  -H 'Content-Type: application/json' -d '{"isin":"HK0000584752","startDate":"2025-01-13","endDate":"2025-01-14"}'

# 债券信息 / 实时价 / 历史
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/bond/info' \
  -H 'Content-Type: application/json' -d '{"isin":"US912810TV08"}'
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/bond/latest-price' \
  -H 'Content-Type: application/json' -d '{"isin":"XS2343337122"}'
curl -X POST 'https://papi-uat.finloopg.com/flp-mktdata-hub/v1/bond/history' \
  -H 'Content-Type: application/json' -d '{"isin":"US91282CJS17","startDate":"2025-05-05"}'
```
