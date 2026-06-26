# Quote Data

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Get Batch Quotes

`POST /api/quote/batch`

### Request

```bash
curl --request POST \
	--url 'https://tradingview-data1.p.rapidapi.com/api/quote/batch' \
	--header 'Content-Type: application/json' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY' \
	--data '{"symbols":["BINANCE:BTCUSDT","BINANCE:ETHUSDT"],"session":"regular","fields":"all"}'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "total": 2,
    "successful": 2,
    "failed": 0,
    "data": [
      {
        "success": true,
        "symbol": "BINANCE:BTCUSDT",
        "data": {
          "bid": 76761.2,
          "ask": 76761.21,
          "current_session": "market",
          "chp": 1.21,
          "rchp": null,
          "provider_id": "binance",
          "type": "spot",
          "update_mode": "streaming",
          "fractional": false,
          "price_52_week_high": 126199.63,
          "pro_name": "BINANCE:BTCUSDT",
          "rch": null,
          "open_price": 75840.97,
          "lp_time": 1776769112,
          "prev_close_price": 75840.97,
          "ch": 920.24,
          "lp": 76761.21,
          "price_percent_change_52_week": -10.175390153751087,
          "currency-logoid": "crypto/XTVCUSDT",
          "short_name": "BTCUSDT",
          "high_price": 76927.57,
          "all_time_high": 126199.63,
          "description": "Bitcoin / TetherUS",
          "rtc": null,
          "volume": 5869.16258,
          "original_name": "BINANCE:BTCUSDT",
          "minmov": 1,
          "price_52_week_low": 60000,
          "format": "price",
          "currency_code": "USDT",
          "average_volume": 16394.661909,
          "rtc_time": null,
          "low_price": 75474.77,
          "exchange": "Binance",
          "base-currency-logoid": "crypto/XTVCBTC",
          "timezone": "Etc/UTC",
          "pricescale": 100,
          "all_time_low": 2817,
          "is_tradable": true,
          "minmove2": 0
        }
      },
      {
        "success": true,
        "symbol": "BINANCE:ETHUSDT",
        "data": {
          "bid": 2333,
          "ask": 2333.01,
          "current_session": "market",
          "chp": 0.83,
          "rchp": null,
          "provider_id": "binance",
          "type": "spot",
          "update_mode": "streaming",
          "fractional": false,
          "price_52_week_high": 4956.78,
          "pro_name": "BINANCE:ETHUSDT",
          "rch": null,
          "open_price": 2313.84,
          "lp_time": 1776769113,
          "prev_close_price": 2313.85,
          "ch": 19.16,
          "lp": 2333.01,
          "price_percent_change_52_week": 46.077134361455514,
          "currency-logoid": "crypto/XTVCUSDT",
          "short_name": "ETHUSDT",
          "high_price": 2338.75,
          "all_time_high": 4956.78,
          "description": "Ethereum / TetherUS",
          "rtc": null,
          "volume": 66934.6523,
          "original_name": "BINANCE:ETHUSDT",
          "minmov": 1,
          "price_52_week_low": 1722.9,
          "format": "price",
          "currency_code": "USDT",
          "average_volume": 308551.30876000004,
          "rtc_time": null,
          "low_price": 2300.01,
          "exchange": "Binance",
          "base-currency-logoid": "crypto/XTVCETH",
          "timezone": "Etc/UTC",
          "pricescale": 100,
          "all_time_low": 81.79,
          "is_tradable": true,
          "minmove2": 0
        }
      }
    ]
  },
  "msg": "Success"
}
```

## Get Quote

`GET /api/quote/{symbol}`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/quote/NASDAQ:AAPL?session=regular&fields=all' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "symbol": "NASDAQ:AAPL",
    "data": {
      "bid": 271.94,
      "ask": 272.32,
      "earnings_per_share_basic_ttm": 7.9334,
      "current_session": "pre_market",
      "market_cap_basic": 4008685001793,
      "chp": 1.04,
      "rchp": -0.37,
      "provider_id": "ice",
      "type": "stock",
      "update_mode": "streaming",
      "fractional": false,
      "price_52_week_high": 288.62,
      "pro_name": "NASDAQ:AAPL",
      "rch": -1.01,
      "open_price": 270.33,
      "lp_time": 1776729598,
      "ceo": "Timothy Donald Cook",
      "total_shares_outstanding_current": 14681100000,
      "prev_close_price": 270.23,
      "ch": 2.82,
      "lp": 273.05,
      "price_percent_change_52_week": 38.4634888438134,
      "currency-logoid": "country/US",
      "short_name": "AAPL",
      "high_price": 274.275,
      "total_revenue": 416161000000,
      "earnings_release_date": 1769722200,
      "all_time_high": 288.62,
      "description": "Apple Inc.",
      "rtc": 272.04,
      "sector": "Electronic Technology",
      "logoid": "apple",
      "volume": 36590169,
      "recommendation_mark": 1.443396,
      "beta_1_year": 1.1557966,
      "original_name": "BATS:AAPL",
      "minmov": 1,
      "country_code": "US",
      "language": "en",
      "price_52_week_low": 193.25,
      "web_site_url": "http://www.apple.com",
      "local_description": "Apple Inc.",
      "price_earnings_ttm": 34.18988334725069,
      "industry": "Telecommunications Equipment",
      "currency_code": "USD",
      "average_volume": 43846173.29999931,
      "business_description": "Apple, Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other varieties of related services. It operates through the following geographical segments: Americas, Europe, Greater China, Japan, and Rest of Asia Pacific. The Americas segment includes North and South America. The Europe segment consists of European countries, as well as India, the Middle East, and Africa. The Greater China segment comprises China, Hong Kong, and Taiwan. The Rest of Asia Pacific segment includes Australia and Asian countries. Its products and services include iPhone, Mac, iPad, AirPods, Apple TV, Apple Watch, Beats products, AppleCare, iCloud, digital content stores, streaming, and licensing services. The company was founded by Steven Paul Jobs, Ronald Gerald Wayne, and Stephen G. Wozniak in April 1976 and is headquartered in Cupertino, CA.",
      "rtc_time": 1776769104,
      "price_earnings": 34.18988334725069,
      "low_price": 270.29,
      "exchange": "Cboe One",
      "timezone": "America/New_York",
      "pricescale": 100,
      "all_time_low": 0.049107,
      "is_tradable": true,
      "minmove2": 0,
      "earnings_release_next_date": 1777581000,
      "founded": 1976,
      "dividends_yield": 0.38088262223036073,
      "basic_eps_net_income": 7.4931
    }
  },
  "msg": "Success"
}
```
