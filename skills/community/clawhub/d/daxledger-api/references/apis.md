# DAX Ledger API Reference

Base URL\
https://app.daxledger.io

---

# Authentication

## POST /api/auth/external_api

### Request Example

```json
{
  "APIKey": "your_api_key",
  "APISecret": "your_api_secret"
}
```

### Response Example

```json
{
  "token": "your_access_token_here"
}
```

Authorization header for authenticated requests:

Authorization: Bearer `<token>`

---

# List Portfolios

## GET /api/portfolios

### Request Example

GET https://app.daxledger.io/api/portfolios Authorization: Bearer
`<token>`

### Response Example

HTTP 200

```json
{
  "items": [
    {
      "id": 1,
      "name": "Portfolio 1",
      "description": "Portfolio 1 Description",
      "status": "active",
      "createdAt": "2024-01-03T09:29:29.740Z",
      "updatedAt": "2024-01-03T09:29:29.740Z",
      "portfolioSettings": [
        {
          "id": 1321,
          "portfolioId": 1,
          "settingId": 364,
          "createdAt": "2024-06-11T09:23:59.424Z",
          "updatedAt": "2024-06-11T09:23:59.424Z",
          "settings": {
            "id": 364,
            "settingKey": "PT",
            "settingValue": "Portugal",
            "status": "ACTIVE",
            "createdAt": "2023-09-27T20:15:00.822Z",
            "updatedAt": "2023-09-27T20:15:00.822Z",
            "category": "COUNTRIES_ISO_3166"
          }
        },
        {
          "id": 1322,
          "portfolioId": 1,
          "settingId": 1180,
          "createdAt": "2024-06-11T09:23:59.424Z",
          "updatedAt": "2024-06-11T09:23:59.424Z",
          "settings": {
            "id": 1180,
            "settingKey": "Europe/Lisbon",
            "settingValue": "Europe/Lisbon",
            "status": "ACTIVE",
            "createdAt": "2024-06-11T09:02:18.502Z",
            "updatedAt": "2024-06-11T09:02:18.502Z",
            "category": "TIMEZONES"
          }
        },
        {
          "id": 1323,
          "portfolioId": 1,
          "settingId": 56,
          "createdAt": "2024-06-11T09:23:59.424Z",
          "updatedAt": "2024-06-11T09:23:59.424Z",
          "settings": {
            "id": 56,
            "settingKey": "EUR",
            "settingValue": "Euro",
            "status": "ACTIVE",
            "createdAt": "2023-09-27T20:11:38.077Z",
            "updatedAt": "2023-09-27T20:11:38.077Z",
            "category": "CURRENCIES_ISO_4217"
          }
        },
        {
          "id": 1324,
          "portfolioId": 1,
          "settingId": 1,
          "createdAt": "2024-06-11T09:23:59.424Z",
          "updatedAt": "2024-06-11T09:23:59.424Z",
          "settings": {
            "id": 1,
            "settingKey": "FIFO",
            "settingValue": "First In First Out",
            "status": "ACTIVE",
            "createdAt": "2023-09-27T20:10:25.498Z",
            "updatedAt": "2023-09-27T20:10:25.498Z",
            "category": "VALUATION_METHODS"
          }
        },
        {
          "id": 1325,
          "portfolioId": 1,
          "settingId": 725,
          "createdAt": "2024-06-11T09:23:59.424Z",
          "updatedAt": "2024-06-11T09:23:59.424Z",
          "settings": {
            "id": 725,
            "settingKey": "Portfolio",
            "settingValue": "Portfolio",
            "status": "ACTIVE",
            "createdAt": "2024-03-26T16:20:39.762Z",
            "updatedAt": "2024-03-26T16:20:39.762Z",
            "category": "CALCULATION_METHODS"
          }
        },
        {
          "id": 1326,
          "portfolioId": 1,
          "settingId": 728,
          "createdAt": "2024-06-11T09:23:59.424Z",
          "updatedAt": "2024-06-11T09:23:59.424Z",
          "settings": {
            "id": 728,
            "settingKey": "COST_BASIS_OUT",
            "settingValue": "Cost Basis Out",
            "status": "ACTIVE",
            "createdAt": "2024-03-26T16:20:50.912Z",
            "updatedAt": "2024-03-26T16:20:50.912Z",
            "category": "COST_BASIS_DIRECTION"
          }
        }
      ],
      "portfolioUser": [
        {
          "group": {
            "id": 1,
            "name": "ADMIN",
            "createdAt": "2023-09-27T20:29:03.967Z",
            "updatedAt": "2023-09-27T20:29:03.967Z"
          }
        }
      ],
      "COUNTRIES_ISO_3166": {
        "id": 364,
        "settingKey": "PT",
        "settingValue": "Portugal"
      },
      "TIMEZONES": {
        "id": 1180,
        "settingKey": "Europe/Lisbon",
        "settingValue": "Europe/Lisbon"
      },
      "CURRENCIES_ISO_4217": {
        "id": 56,
        "settingKey": "EUR",
        "settingValue": "Euro"
      },
      "VALUATION_METHODS": {
        "id": 1,
        "settingKey": "FIFO",
        "settingValue": "First In First Out"
      },
      "CALCULATION_METHODS": {
        "id": 725,
        "settingKey": "Portfolio",
        "settingValue": "Portfolio"
      },
      "COST_BASIS_DIRECTION": {
        "id": 728,
        "settingKey": "COST_BASIS_OUT",
        "settingValue": "Cost Basis Out"
      },
      "transactionCount": 53
    }
  ]
}
```

HTTP 400:

```json
{
  "message": "Invalid show parameter",
  "status": 400
}
```

---

# Compliance

## Portfolio Compliance

GET /api/portfolio/{portfolioId}/compliance

Retrieve compliance information for the portfolio, including classified addresses, unclassified addresses, and potential compliance risks.

Query parameters:

page  
pageSize  
filter  
sort

### Request Example

GET https://app.daxledger.io/api/portfolio/123/compliance?page=1&pageSize=20  
Authorization: Bearer <token>

### Response Example

```json
{
  "items": [
    {
      "id": 1,
      "portfolioId": 5,
      "address": "0x19aa5fe80d33a56d56c78e82ea5e50e5d80b4dff",
      "requestStatus": "complete",
      "provider": "WardAnalytics",
      "risk": 10,
      "providerResponse": {
        "...": "..."
      },
      "createdAt": "2023-01-01T12:00:00Z",
      "updatedAt": "2023-01-01T12:00:24Z"
    }
  ],
  "total": 1
}
```

### Available Filters

- address (operator: 'contains_in')
- riskQuick (operator: 'and_multiple_column')

### Filter Example

#### Address

```json
{
  "address": {
    "operator": "contains_in",
    "value": ["0x019EdcB493Bd91e2b25b70f26D5d9041Fd7EF946"]
  }
}
```

#### RiskQuick

Low

```json
{
  "riskQuick": {
    "operator": "and_multiple_column",
    "multipleAndField": ["risk", "risk"],
    "value": [{ "gt": 0 }, { "lte": 3 }]
  }
}
```

Medium

```json
{
  "riskQuick": {
    "operator": "and_multiple_column",
    "multipleAndField": ["risk", "risk"],
    "value": [{ "gt": 3 }, { "lte": 6 }]
  }
}
```

High

```json
{
  "riskQuick": {
    "operator": "and_multiple_column",
    "multipleAndField": ["risk", "risk"],
    "value": [{ "gt": 6 }, { "lte": 9 }]
  }
}
```

Critical

```json
{
  "riskQuick": {
    "operator": "and_multiple_column",
    "multipleAndField": ["risk", "risk"],
    "value": [{ "gt": 9 }]
  }
}
```

---

# Portfolio KPIs

## GET /api/portfolio/{portfolioId}/kpis/portfolio

### Request Example

GET https://app.daxledger.io/api/portfolio/123/kpis/portfolio
Authorization: Bearer `<token>`

### Response Example

HTTP 200

```json
{
  "kpis": [
    {
      "id": 14,
      "portfolioId": 5,
      "kpiName": "totalBalance",
      "kpiValue": {
        "type": "currency",
        "value": 1312.026208674356
      },
      "kpiType": "kpi"
    },
    {
      "id": 15,
      "portfolioId": 5,
      "kpiName": "numberOfTransactions",
      "kpiValue": {
        "type": "number",
        "value": 99083
      },
      "kpiType": "kpi"
    }
  ]
}
```

---

# Findings

## List Findings

GET /api/portfolio/{portfolioId}/findings

Query parameters:

page\
pageSize

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/findings?page=1&pageSize=20
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "id": 1,
      "portfolioId": 6,
      "category": "Balance",
      "message": {
        "message": "The balance for digital asset ticker ADA is showing as negative (-608.5101638500146). Ensure all transactions, both incoming and outgoing, are fully imported — whether through connection or manual entry.",
        "digitalAssetTicker": "ADA"
      },
      "createdAt": "2023-01-01T12:00:00Z",
      "updatedAt": "2023-01-01T12:00:51Z",
      "identifier": 1
    },
    {
      "id": 2,
      "portfolioId": 7,
      "category": "CostBasis",
      "message": {
        "message": "For the digital asset BTC, the outgoing transaction with ID 90b3c26118ec73e840de2a19c47d698fe5f2793fbdd53f28973fb99d485c38a7 on 13/12/2023, 09:56:17 exceeds the available balance 0.001326171574697936. Please ensure all transactions are fully imported, either through connections or manual entry.",
        "transactionId": "100321",
        "digitalAssetTicker": "BTC"
      },
      "createdAt": "2023-01-01T11:20:30Z",
      "updatedAt": "2023-01-01T11:21:41Z",
      "identifier": 3
    }
  ],
  "total": 2
}
```

---

## Finding By Rule Id

GET /api/portfolio/{portfolioId}/finding/{ruleId}

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/finding/001
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "id": 10,
      "portfolioId": 123,
      "category": "Balance",
      "message": {
        "message": "The balance for digital asset ticker ADA is showing as negative.",
        "digitalAssetTicker": "ADA"
      },
      "createdAt": "2023-01-01T12:00:00Z",
      "identifier": "001",
      "status": "TO_ANALYZE",
      "connectionName": "Binance",
      "_count": {
        "portfolioFindingNotes": 2
      }
    }
  ],
  "total": 1
}
```

---

# Position Snapshot

## Positions Snapshot

GET /api/portfolio/{portfolioId}/position_snapshot

Query parameters:

page\
pageSize\
filter\
sort

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/position_snapshot?page=1&pageSize=20
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "id": 62610,
      "digitalAssetTicker": "ETH",
      "reportedBalance": 0.5885102890229292,
      "currentValue": 1350.5762268216672,
      "fiatTicker": "EUR",
      "iconUrl": "https://www.cryptocompare.com/media/37746238/eth.png",
      "portfolioPercentage": 0.9763012191191435
    }
  ],
  "total": 1
}
```

---

## Position Snapshot Graph (Overall)

GET /api/portfolio/{portfolioId}/position_snapshot/graph

Query parameters:

span

- 7: 7 days interval
- 30: 30 days interval
- 365: 365 days interval
- -1: all range available

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/position_snapshot/graph?span=7
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "date": "2025-05-05",
      "sum": 1010,
      "fiatTicker": "EUR"
    }
  ],
  "total": 1
}
```

## Position Snapshot Graph By Ticker

GET /api/portfolio/{portfolioId}/position_snapshot/graph/{ticker}

Query parameters:

span

- 7: 7 days interval
- 30: 30 days interval
- 365: 365 days interval
- -1: all range available

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/position_snapshot/graph/BTC?span=7
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "date": "2025-05-05",
      "sum": 1010,
      "fiatTicker": "EUR"
    }
  ],
  "total": 1
}
```

---

## DeFi Positions

GET /api/portfolio/{portfolioId}/positions_report/defi

### Request Example

GET https://app.daxledger.io/api/portfolio/123/positions_report/defi
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": {
    "GMX V2": [
      {
        "id": 7945,
        "digitalAssetTicker": "WETH",
        "digitalAssetQuantity": 89.45073765538102,
        "currentValue": 205284.3348803455,
        "portfolioConnectionId": 1,
        "iconUrl": "https://www.cryptocompare.com/media/38553079/weth.png",
        "fiatTicker": "EUR",
        "portfolioConnectionName": "ARB"
      }
    ]
  },
  "total": 1
}
```

---

# Reports

## Capital Gains Report

GET /api/portfolio/{portfolioId}/capital_gains_report

Query parameters:

page\
pageSize\
filter\
sort

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/capital_gains_report?page=1&pageSize=20
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "id": 1,
      "digitalAssetTicker": "BTC",
      "originalCost": 1000.55,
      "currentValue": 1250.1,
      "quantity": 0.02,
      "realizedLongTerm": 10,
      "realizedShortTerm": 25.5,
      "unrealizedLongTerm": 150,
      "unrealizedShortTerm": 64.05,
      "year": 2024,
      "connectionId": null,
      "fiatTicker": "USD",
      "portfolioId": 123,
      "realizedDetails": [],
      "unrealizedDetails": [],
      "hasMissingValues": {
        "realizedLongTerm": false,
        "realizedShortTerm": false,
        "unrealizedLongTerm": false,
        "unrealizedShortTerm": false
      },
      "createdAt": "Mon Jan 01 2024 10:00:00 GMT+0000 (Coordinated Universal Time)",
      "updatedAt": "Mon Jan 01 2024 10:00:00 GMT+0000 (Coordinated Universal Time)",
      "digitalAssetImage": "https://www.cryptocompare.com/media/37746251/btc.png"
    }
  ],
  "total": 1,
  "showWarning": false,
  "isEveryTransactionNonTaxable": false,
  "isSeparateSetting": false,
  "hasDefiPositions": false
}
```

### Available Filters

- year (operator: '=')
- digitalAssetTicker (operator: 'contains_in')
- portfolioConnection (operator: '=')

---

## Capital Gains Available Filters

GET /api/portfolio/{portfolioId}/capital_gains_report/filters

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/capital_gains_report/filters
Authorization: Bearer `<token>`

---

## Sanity Check Report

GET /api/portfolio/{portfolioId}/sanity_check_report

Query parameters:

page\
pageSize\
filter

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/sanity_check_report?page=1&pageSize=20
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "id": 385502,
      "portfolioId": 102,
      "portfolioConnectionId": 56,
      "digitalAssetTicker": "ETH",
      "calculatedBalance": 4.0831,
      "reportedBalance": 4.0819,
      "differenceBalance": 0.0012,
      "numberOfTransactions": 5,
      "createdAt": "2024-07-22T14:36:24.095Z",
      "updatedAt": "2024-07-22T14:36:24.095Z",
      "iconUrl": "https://www.cryptocompare.com/media/37746251/eth.png",
      "connectionName": "Binance"
    }
  ],
  "total": 1
}
```

### Available Filters

- portfolioConnectionName (operator: 'contains_in')
- digitalAssetTicker (operator: 'contains_in')
- ignoreSpamTokens (operator: '=', value: true or false)

---

## Calculation Summary Report

GET /api/portfolio/{portfolioId}/calculation_summary_report

Query parameters:

page\
pageSize\
filter\
sort

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/calculation_summary_report?page=1&pageSize=20
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "id": 1,
      "portfolioId": 123,
      "fiatTicker": "USD",
      "item": "realizedGains",
      "value": 1024.55,
      "formula": null,
      "filters": null,
      "createdAt": "2024-01-01T10:00:00Z",
      "updatedAt": "2024-01-01T10:00:00Z",
      "year": 2024
    }
  ],
  "total": 1,
  "isSeparate": false
}
```

### Available Filters

- portfolioConnection (operator: '=')
- year (operator: '=')

---

## Fiscal Report

GET /api/portfolio/{portfolioId}/fiscal_report

Query parameters:

page\
pageSize\
filter\
sort

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/fiscal_report?page=1&pageSize=20
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": [
    {
      "id": 1,
      "portfolioId": 123,
      "portfolioConnectionId": 50,
      "connectionName": "Binance",
      "digitalAssetQuantity": 0.5,
      "digitalAssetTicker": "BTC",
      "digitalAssetImage": "https://www.cryptocompare.com/media/37746251/btc.png",
      "transactionHash": "0xabc123",
      "transactionHeaderId": 1001,
      "acquisitionDate": "2024-01-01T10:00:00.000Z",
      "costBasis": 10000.5,
      "saleDate": "2024-03-01T10:00:00.000Z",
      "salePrice": 12000.75,
      "expenses": 50,
      "holdingPeriod": 60,
      "fiatTicker": "USD",
      "createdAt": "2024-03-01T10:00:00.000Z",
      "updatedAt": "2024-03-01T10:00:00.000Z",
      "labels": ["Exchange"]
    }
  ],
  "total": 1
}
```

### Available Filters

- portfolioConnectionName (operator: 'contains_in')
- digitalAssetTicker (operator: 'contains_in')
- saleDate (operator: 'between', value: startDate and endDate)
- acquisitionDate (operator: 'between', value: startDate and endDate)
- holdingTerm (operator: '=', value: short-term, long-term, all)

---

# Transactions

GET /api/portfolio/{portfolioId}/transactions

Query parameters:

page\
pageSize\
filter

### Request Example

GET
https://app.daxledger.io/api/portfolio/123/transactions?page=1&pageSize=20
Authorization: Bearer `<token>`

### Response Example

HTTP 200:

```json
{
  "items": {
    "items": [
      {
        "id": 1909699,
        "portfolioId": 186,
        "transactionDate": "2024-04-16T12:33:11.000Z",
        "fromAddress": "0xf72b89176c84017a16eaeb648bbc511ed123b120",
        "toAddress": "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43",
        "blockchain": "ETH",
        "transactionHash": "0x86c678edb3b66a5cb58ac913237ec3b7c206a618d0ca2f85aa95e5e8cb491faf",
        "transactionType": "withdrawal",
        "direction": "out",
        "inDetailId": null,
        "inDigitalAssetQuantity": "0.00000000",
        "inDigitalAssetTicker": "",
        "inFiatAmount": "0.00000000",
        "inFiatTicker": "",
        "outDetailId": 2831017,
        "outDigitalAssetQuantity": "0.79328919",
        "outDigitalAssetTicker": "ETH",
        "outFiatAmount": "2297.29172751",
        "outFiatTicker": "EUR",
        "feeDetailId": 2831016,
        "feeDigitalAssetQuantity": "0.00026916",
        "feeDigitalAssetTicker": "ETH",
        "feeFiatAmount": "0.77945139",
        "feeFiatTicker": "EUR",
        "fromContact": {
          "name": "ETH"
        },
        "portfolioConnectionName": "ETH",
        "portfolioConnectionInfo": {
          "address": "0xf72b89176C84017A16eaEb648bbc511ED123B120",
          "...": "..."
        },
        "portfolioConnectionId": 408,
        "labels": [
          {
            "id": 5,
            "name": "Taxable Event",
            "default": true
          }
        ],
        "explorerUrl": "https://etherscan.io/",
        "costBasis": 2304.633628236674,
        "rawData": {
          "...": "..."
        },
        "pnl": -8.121352111028045,
        "pnlTicker": "EUR",
        "classification": "withdrawal",
        "salesProceeds": 2296.512276125646,
        "feeTickerImg": "https://www.cryptocompare.com/media/37746238/eth.png",
        "outTickerImg": "https://www.cryptocompare.com/media/37746238/eth.png",
        "hasProblem": false
      }
    ],
    "hasProblems": false,
    "total": 1
  }
}
```

### Available Filters

- transactionHash (operator: 'contains')
- address (operator: 'contains_in')
- portfolioConnectionName (operator: 'contains_in')
- digitalAssetTicker (operator: 'contains_in')
- transactionType (operator: 'contains_in')
- transactionDate (operator: 'between', value: startDate and endDate, format: YYYY-MM-DD)

---

# Encoding

Browser:

btoa(JSON.stringify(filter))

Node:

Buffer.from(JSON.stringify(filter)).toString("base64")

---

# Epoch Fields

If an API field is an epoch timestamp, convert it to ISO date before
returning it.

Rule:

10 digits -\> seconds 13 digits -\> milliseconds

Example:

new Date(Number(epoch) \< 1e12 ? Number(epoch) \* 1000 :
Number(epoch)).toISOString()

---

# Pagination

page starts at 1

pageSize default = 20

Continue requesting pages while:

items.length < total

---

# Other HTTP Responses

HTTP 401:

```json
{
  "message": "Unauthorized",
  "status": 401
}
```

HTTP 403:

```json
{
  "message": "Access Denied",
  "status": 403
}
```

HTTP 500:

```json
{
  "message": "Internal Server Error",
  "status": 500
}
```
