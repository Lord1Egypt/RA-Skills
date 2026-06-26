# QuoteNode REST API Guide

> For developers who access QuoteNode market data over HTTP.

## 1. Prerequisites

### 1.1 Endpoint

The deployment environment provides the domain or gateway address. Replace `https://<endpoint>` with the real value when calling the API.

### 1.2 Request Conventions

All REST requests should include these headers:

```http
X-API-KEY: <your AK>
Content-Type: application/json
```

Use `POST` by default. The request body is JSON.

## 2. Endpoint List

### 2.1 Security Detail

**URL** `/Api/V1/Quotation/Detail`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `instrument` | string | Yes | Instrument identifier: `{market}\|{symbol}` or `{market}\|{symbol}\|{flag}` |
| `lang` | string | No | Language: `zh-CN`, `tc`, `en` |

**Example**

```json
{"instrument":"US|AAPL","lang":"en"}
```

For response fields, see `response.md#1-security-detail-apiv1quotationdetail`.

### 2.2 Instrument List

**URL** `/Api/V1/Basic/BasicInfo`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `instrument` | string | Yes | Format: `{market}\|{securityType}` |
| `page` | int | Yes | Page number, starting from 1 |
| `pageSize` | int | Yes | Page size, maximum `500` |
| `lang` | string | No | Language |

### 2.3 Tick Trades

**URL** `/Api/V1/Quotation/Tick`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `instrument` | string | Yes | Instrument identifier: `{market}\|{symbol}\|{flag}` |
| `page` | int | Yes | Page number |
| `pageSize` | int | Yes | Page size |
| `startTime` | int64 | No | Start time in milliseconds |
| `endTime` | int64 | No | End time in milliseconds |

### 2.4 Level-2 Depth

**URL** `/Api/V1/Quotation/DepthQuoteL2`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `instrument` | string | Yes | Instrument identifier: `{market}\|{symbol}\|{flag}` |
| `depth` | int | Yes | Depth level, range `[1,10]` |

### 2.5 TimeLine

**URL** `/Api/V1/History/TimeLine`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `instrument` | string | Yes | Instrument identifier: `{market}\|{symbol}` |
| `period` | string | Yes | Period: `day`, `5day` |

### 2.6 KLine

**URL** `/Api/V1/History/KLine`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `instrument` | string | Yes | Instrument identifier: `{market}\|{symbol}` |
| `period` | string | Yes | Period, see `reference.md#enum-period` |
| `right` | int | No | Adjustment type, see `reference.md#enum-right` |
| `endTime` | int64 | No | End time in seconds |

### 2.7 Broker List

**URL** `/Api/V1/Quotation/Brokers`

Send `{}` as the request body.

### 2.8 Broker Queue

**URL** `/Api/V1/Quotation/Broker`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `instrument` | string | Yes | Instrument identifier: `{market}\|{symbol}` |
| `lang` | string | No | Language |

### 2.9 Trading Calendar

**URL** `/Api/V1/Basic/Holiday`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `market` | string | Yes | Market code, see `reference.md#enum-market` |
| `startDate` | string | Yes | Start date in `YYYY-MM-DD` format |
| `endDate` | string | Yes | End date in `YYYY-MM-DD` format |
| `lang` | string | No | Language |

## 3. Common Request Examples

### 3.1 Query Security Detail

```json
{"instrument":"US|AAPL","lang":"en"}
```

### 3.2 Query Hong Kong Stock List

```json
{"instrument":"HKEX|1","page":1,"pageSize":50,"lang":"zh-CN"}
```

### 3.3 Query KLine

```json
{"instrument":"HKEX|00700","period":"day","right":0}
```

## 4. Error Responses

When the HTTP status is not `200`, the response body format is:

| Field | Type | Description |
| --- | --- | --- |
| `code` | int | HTTP status code |
| `reason` | string | Error identifier |
| `message` | string | Error description |

Example:

```json
{"code":429,"reason":"OPENAPI_QUOTA_EXCEEDED","message":"Rate limit exceeded"}
```

For error codes and business codes, see `reference.md#error-http` and `reference.md#error-openapi`.

## 5. Which Document to Read

- For endpoint paths, parameters, and examples, read this file.
- For enum values, market codes, and error codes, read `reference.md`.
- For response field meanings, read `response.md`.
- For multilingual sample code, the original examples are in `docs/project/integration/demo/openapi.md`.
