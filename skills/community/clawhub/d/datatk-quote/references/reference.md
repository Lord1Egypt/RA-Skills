# QuoteNode Enums and Error Codes

## 1. Enums

<a id="enum-market"></a>
### 1.1 Market Codes

#### Stocks

| Code | Description |
| --- | --- |
| `SSE` | Shanghai Stock Exchange |
| `SZSE` | Shenzhen Stock Exchange |
| `HKEX` | Hong Kong Exchanges and Clearing |
| `US` | US stock market |

#### Futures

| Code | Description |
| --- | --- |
| `SHFE` | Shanghai Futures Exchange |
| `CZCE` | Zhengzhou Commodity Exchange |
| `DCE` | Dalian Commodity Exchange |
| `CFFEX` | China Financial Futures Exchange |
| `INE` | Shanghai International Energy Exchange |
| `COMEX` | Commodity Exchange, Inc. |
| `CME` | Chicago Mercantile Exchange |
| `CBOT` | Chicago Board of Trade |
| `NYMEX` | New York Mercantile Exchange |
| `HKFE` | Hong Kong Futures Exchange |
| `LME` | London Metal Exchange |
| `SGXFE` | Singapore futures market |

#### Forex

| Code | Description |
| --- | --- |
| `FOREX` | Foreign exchange market |

<a id="enum-security-type"></a>
### 1.2 Security Types

| Code | Description |
| --- | --- |
| `1` | Stock |
| `2` | Index |
| `3` | Other |
| `4` | Futures |
| `5` | Bond |
| `6` | Fund |
| `11` | Warrant |
| `12` | CBBC |
| `13` | Inline Warrants |
| `14` | Trust |
| `41` | ETF |

<a id="enum-flag"></a>
### 1.3 Data Flags

| Code | Description |
| --- | --- |
| `R` | Real-time quote |
| `D` | Delayed quote |
| `F` | Futu dark pool |
| `H` | Bright Smart dark pool |

<a id="enum-period"></a>
### 1.4 KLine Periods

| Code | Description |
| --- | --- |
| `1min` | 1 minute |
| `5min` | 5 minutes |
| `15min` | 15 minutes |
| `30min` | 30 minutes |
| `60min` | 60 minutes |
| `day` | Daily |
| `week` | Weekly |
| `month` | Monthly |
| `year` | Yearly |

<a id="enum-right"></a>
### 1.5 Adjustment Types

| Code | Description |
| --- | --- |
| `0` | No adjustment |
| `1` | Forward adjustment |
| `2` | Backward adjustment |

<a id="enum-direction"></a>
### 1.6 Trade Direction

| Code | Description |
| --- | --- |
| `B` | Buy |
| `S` | Sell |
| `N` | Neutral |

## 2. Error Codes

<a id="error-http"></a>
### 2.1 HTTP Status Codes

| Status | Description |
| --- | --- |
| `200` | Request succeeded |
| `400` | Invalid request parameters |
| `401` | Authentication failed |
| `403` | Permission denied |
| `429` | Rate limit exceeded |
| `500` | Internal server error |
| `502/504` | Gateway timeout |

<a id="error-openapi"></a>
### 2.2 REST Business Codes

| Code | Description |
| --- | --- |
| `0` | Success |
| `1001` | Parameter validation failed |
| `1002` | Instrument not found |
| `1003` | No data |
| `2001` | Invalid AK |
| `2002` | AK expired |
| `2003` | No endpoint permission |
| `2004` | No market permission |
| `5001` | Upstream service error |
| `5002` | System busy |

## 3. Usage Notes

- If you need the `market` or `flag` values inside `instrument`, start with this file.
- The `securityType` used by the instrument list endpoint is also defined here.
- Do not guess `period` or `right` for KLine endpoints. Use the enum values in this file directly.
