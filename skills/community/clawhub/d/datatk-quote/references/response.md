# QuoteNode REST Response Field Guide

> This file covers REST APIs only. WebSocket fields are outside the scope of this skill.

## 1. Security Detail `/Api/V1/Quotation/Detail`

### Stocks

| Field | Example | Description |
| --- | --- | --- |
| `code` | `0` | Business status code |
| `msg` | `success` | Status message |
| `data.market` | `HKEX` | Market |
| `data.symbol` | `00700` | Symbol |
| `data.name` | `Tencent Holdings` | Name |
| `data.latestPrice` | `404.2` | Latest price |
| `data.open` | `405.2` | Open price |
| `data.high` | `413.4` | High price |
| `data.low` | `401.6` | Low price |
| `data.close` | `401` | Previous close |
| `data.chg` | `3.2` | Price change |
| `data.gain` | `0.008` | Change ratio |
| `data.volume` | `20493537` | Volume |
| `data.amount` | `8334918073.622` | Turnover |
| `data.currency` | `HKD` | Currency |
| `data.lotSize` | `100` | Shares per lot |
| `data.latestTime` | `1731917288` | Latest timestamp |
| `data.securityType` | `1` | Security type |
| `data.securityStatus` | `1` | Security status |

### Futures

Common fields are similar to stocks. Also note:

| Field | Example | Description |
| --- | --- | --- |
| `data.market` | `COMEX` | Market |
| `data.symbol` | `GC2604` | Contract code |
| `data.latestPrice` | `5354.8` | Latest price |
| `data.volume` | `301813` | Volume |
| `data.latestTime` | `1770591000` | Latest timestamp, in seconds |

### Forex

Common fields are similar to stocks. Also note:

| Field | Example | Description |
| --- | --- | --- |
| `data.from` | `USD` | Base currency |
| `data.to` | `JPY` | Quote currency |

## 2. Instrument List `/Api/V1/Basic/BasicInfo`

Common fields:

| Field | Example | Description |
| --- | --- | --- |
| `code` | `0` | Business status code |
| `msg` | `success` | Status message |
| `data.totalNum` | `2500` | Total record count |
| `data.list[].market` | `HKEX` | Market |
| `data.list[].symbol` | `00700` | Instrument symbol |
| `data.list[].securityType` | `1` | Security type |
| `data.list[].nameZh` | `腾讯控股` | Simplified Chinese name |
| `data.list[].nameTc` | `騰訊控股` | Traditional Chinese name |
| `data.list[].nameEn` | `TENCENT` | English name |

Additional common stock fields:

| Field | Example | Description |
| --- | --- | --- |
| `data.list[].lotSize` | `100` | Shares per lot |
| `data.list[].currency` | `HKD` | Currency |
| `data.list[].tickSize` | `0.2` | Minimum price increment |
| `data.list[].spreadTableCode` | `A` | Spread table code |

Additional common futures fields:

| Field | Example | Description |
| --- | --- | --- |
| `data.list[].contractCode` | `2505` | Contract month code |
| `data.list[].contractSize` | `100` | Contract multiplier |
| `data.list[].isContinuous` | `false` | Whether it is a continuous contract |
| `data.list[].isMain` | `false` | Whether it is the main contract |
| `data.list[].productCode` | `GC` | Product code |

## 3. Tick Trades `/Api/V1/Quotation/Tick`

| Field | Example | Description |
| --- | --- | --- |
| `data.list[].direction` | `B` | Trade direction |
| `data.list[].price` | `649.5` | Trade price |
| `data.list[].quantity` | `900` | Trade quantity |
| `data.list[].tickTime` | `1758850673511` | Trade time in milliseconds |
| `data.list[].type` | `U` | Tick type |

## 4. Level-2 Depth `/Api/V1/Quotation/DepthQuoteL2`

| Field | Example | Description |
| --- | --- | --- |
| `data.market` | `HKEX` | Market |
| `data.symbol` | `00700` | Instrument symbol |
| `data.latestPrice` | `0` | Latest price |
| `data.ask[].price` | `0` | Ask price |
| `data.ask[].vol` | `0` | Ask volume |
| `data.ask[].depthNo` | `0` | Ask depth level |
| `data.bid[].price` | `0` | Bid price |
| `data.bid[].vol` | `0` | Bid volume |
| `data.bid[].depthNo` | `0` | Bid depth level |

## 5. TimeLine `/Api/V1/History/TimeLine`

Detail fields:

| Field | Example | Description |
| --- | --- | --- |
| `data.detail.market` | `HKEX` | Market |
| `data.detail.symbol` | `00700` | Instrument symbol |
| `data.detail.name` | `string` | Name |
| `data.detail.latestPrice` | `0` | Latest price |

List fields:

| Field | Example | Description |
| --- | --- | --- |
| `data.list[].time` | `0` | Time |
| `data.list[].price` | `0` | Price |
| `data.list[].volume` | `0` | Volume |
| `data.list[].avgPrice` | `0` | Average price |

## 6. KLine `/Api/V1/History/KLine`

Detail fields:

| Field | Example | Description |
| --- | --- | --- |
| `data.detail.market` | `HKEX` | Market |
| `data.detail.symbol` | `00700` | Instrument symbol |
| `data.detail.securityType` | `1` | Security type |
| `data.detail.name` | `string` | Name |

KLine fields:

| Field | Example | Description |
| --- | --- | --- |
| `data.list[].time` | `0` | Time |
| `data.list[].open` | `0` | Open price |
| `data.list[].close` | `0` | Close price |
| `data.list[].high` | `0` | High price |
| `data.list[].low` | `0` | Low price |
| `data.list[].price` | `0` | Current or representative price |
| `data.list[].volume` | `0` | Volume |
| `data.list[].amount` | `0` | Turnover |
| `data.list[].volumeFloatPart` | `0` | Fractional volume part, present in some markets |

## 7. Broker List `/Api/V1/Quotation/Brokers`

| Field | Example | Description |
| --- | --- | --- |
| `data[].brokerId` | `2840` | Broker ID |
| `data[].nameZh` | `麥格理資本` | Simplified Chinese name |
| `data[].nameTc` | `麥格理資本` | Traditional Chinese name |
| `data[].nameEn` | `Macquarie Capital` | English name |

## 8. Broker Queue `/Api/V1/Quotation/Broker`

| Field | Example | Description |
| --- | --- | --- |
| `data.market` | `HKEX` | Market |
| `data.symbol` | `00700` | Instrument symbol |
| `data.buy[].level` | `0` | Bid level |
| `data.buy[].price` | `0` | Bid price |
| `data.buy[].num` | `0` | Number of bid brokers |
| `data.buy[].list[].brokerId` | `2840` | Bid broker ID |
| `data.sell[].level` | `0` | Ask level |
| `data.sell[].price` | `0` | Ask price |
| `data.sell[].num` | `0` | Number of ask brokers |
| `data.sell[].list[].brokerId` | `2842` | Ask broker ID |

## 9. Trading Calendar `/Api/V1/Basic/Holiday`

| Field | Example | Description |
| --- | --- | --- |
| `data[].market` | `HKEX` | Market |
| `data[].date` | `2025-01-01` | Date |
| `data[].type` | `2` | Calendar type |
| `data[].reasonZh` | `元旦` | Chinese reason |
| `data[].reasonTc` | `元旦` | Traditional Chinese reason |
| `data[].reasonEn` | `New Year's Day` | English reason |
| `data[].openTime` | `0` | Open time |
| `data[].closeTime` | `0` | Close time |
