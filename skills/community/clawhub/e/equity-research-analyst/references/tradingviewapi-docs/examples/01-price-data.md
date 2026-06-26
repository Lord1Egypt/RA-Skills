# Price Data

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Get Price History

`GET /api/price/{symbol}`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/price/BINANCE:BTCUSDT?timeframe=1&range=10' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "symbol": "BINANCE:BTCUSDT",
    "current": {
      "time": 1776769080,
      "open": 76761.31,
      "close": 76761.2,
      "max": 76761.31,
      "min": 76754.38,
      "volume": 2.21
    },
    "history": [
      {
        "time": 1776769080,
        "open": 76761.31,
        "close": 76761.2,
        "max": 76761.31,
        "min": 76754.38,
        "volume": 2.21
      },
      {
        "time": 1776769020,
        "open": 76777.86,
        "close": 76761.3,
        "max": 76777.87,
        "min": 76746.67,
        "volume": 7.78
      },
      {
        "time": 1776768960,
        "open": 76804.68,
        "close": 76777.86,
        "max": 76810.56,
        "min": 76777.86,
        "volume": 9.34
      },
      {
        "time": 1776768900,
        "open": 76834,
        "close": 76804.68,
        "max": 76866.55,
        "min": 76804.68,
        "volume": 9.16
      },
      {
        "time": 1776768840,
        "open": 76817.42,
        "close": 76834.01,
        "max": 76850,
        "min": 76808.08,
        "volume": 9.59
      },
      {
        "time": 1776768780,
        "open": 76820.86,
        "close": 76817.43,
        "max": 76825,
        "min": 76802.99,
        "volume": 8.94
      },
      {
        "time": 1776768720,
        "open": 76788.56,
        "close": 76820.87,
        "max": 76823.55,
        "min": 76743.23,
        "volume": 40.73
      },
      {
        "time": 1776768660,
        "open": 76789.99,
        "close": 76788.56,
        "max": 76866.55,
        "min": 76788.55,
        "volume": 22.97
      },
      {
        "time": 1776768600,
        "open": 76730.49,
        "close": 76790,
        "max": 76790,
        "min": 76730.49,
        "volume": 15.86
      },
      {
        "time": 1776768540,
        "open": 76718.74,
        "close": 76730.49,
        "max": 76734.68,
        "min": 76676.4,
        "volume": 7.88
      }
    ],
    "info": {
      "series_id": "ser_1",
      "source2": {
        "country": "MT",
        "description": "Binance",
        "exchange-type": "exchange",
        "id": "BINANCE",
        "name": "Binance",
        "url": "https://www.binance.com/en"
      },
      "currency_code": "USDT",
      "source_id": "BINANCE",
      "subsession_id": "regular",
      "provider_id": "binance",
      "base_currency_id": "XTVCBTC",
      "base_currency": "BTC",
      "currency_id": "XTVCUSDT",
      "format": "price",
      "formatter": "price",
      "pro_perm": "",
      "volume_type": "base",
      "measure": "price",
      "allowed_adjustment": "none",
      "short_description": "Bitcoin / TetherUS",
      "variable_tick_size": "",
      "name": "BTCUSDT",
      "full_name": "BINANCE:BTCUSDT",
      "pro_name": "BINANCE:BTCUSDT",
      "base_name": [
        "BINANCE:BTCUSDT"
      ],
      "description": "Bitcoin / TetherUS",
      "exchange": "Binance",
      "pricescale": 100,
      "pointvalue": 1,
      "minmov": 1,
      "session": "24x7",
      "session_display": "24x7",
      "subsessions": [
        {
          "description": "Regular Trading Hours",
          "id": "regular",
          "private": false,
          "session": "24x7",
          "session-display": "24x7"
        }
      ],
      "type": "spot",
      "typespecs": [
        "crypto",
        "defi"
      ],
      "has_intraday": true,
      "fractional": false,
      "listed_exchange": "BINANCE",
      "legs": [
        "BINANCE:BTCUSDT"
      ],
      "is_tradable": true,
      "minmove2": 0,
      "timezone": "Etc/UTC",
      "aliases": [],
      "alternatives": [],
      "is_replayable": true,
      "has_adjustment": false,
      "has_extended_hours": false,
      "bar_source": "trade",
      "bar_transform": "none",
      "bar_fillgaps": false,
      "visible_plots_set": "ohlcv",
      "is-tickbars-available": true,
      "exchange_listed_name": "Binance"
    }
  },
  "msg": "Success"
}
```

## Get Batch Price History

`POST /api/price/batch`

### Request

```bash
curl --request POST \
	--url 'https://tradingview-data1.p.rapidapi.com/api/price/batch' \
	--header 'Content-Type: application/json' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY' \
	--data '{"requests":[{"symbol":"BINANCE:BTCUSDT","timeframe":"60","range":20}]}'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "total": 1,
    "successful": 1,
    "failed": 0,
    "data": [
      {
        "success": true,
        "symbol": "BINANCE:BTCUSDT",
        "current": {
          "time": 1776765600,
          "open": 76362.78,
          "close": 76761.2,
          "max": 76866.55,
          "min": 76349.59,
          "volume": 532.02
        },
        "history": [
          {
            "time": 1776765600,
            "open": 76362.78,
            "close": 76761.2,
            "max": 76866.55,
            "min": 76349.59,
            "volume": 532.02
          },
          {
            "time": 1776762000,
            "open": 76507.21,
            "close": 76362.77,
            "max": 76587.82,
            "min": 76155,
            "volume": 582.67
          },
          {
            "time": 1776758400,
            "open": 76084.34,
            "close": 76507.21,
            "max": 76927.57,
            "min": 76063.98,
            "volume": 915.24
          },
          {
            "time": 1776754800,
            "open": 75974.12,
            "close": 76084.34,
            "max": 76300,
            "min": 75814.26,
            "volume": 1236.72
          },
          {
            "time": 1776751200,
            "open": 75802,
            "close": 75974.11,
            "max": 76129.95,
            "min": 75703.85,
            "volume": 408.87
          },
          {
            "time": 1776747600,
            "open": 75813.8,
            "close": 75802,
            "max": 75981.1,
            "min": 75782.75,
            "volume": 321.54
          },
          {
            "time": 1776744000,
            "open": 75710.31,
            "close": 75813.81,
            "max": 75823.49,
            "min": 75600,
            "volume": 259.64
          },
          {
            "time": 1776740400,
            "open": 75581.33,
            "close": 75710.3,
            "max": 75721.12,
            "min": 75474.77,
            "volume": 256.25
          },
          {
            "time": 1776736800,
            "open": 75927.58,
            "close": 75581.33,
            "max": 75932.7,
            "min": 75580,
            "volume": 536.09
          },
          {
            "time": 1776733200,
            "open": 76092.46,
            "close": 75927.59,
            "max": 76263.4,
            "min": 75866.01,
            "volume": 391.14
          },
          {
            "time": 1776729600,
            "open": 75840.97,
            "close": 76092.45,
            "max": 76099.19,
            "min": 75700,
            "volume": 428.96
          },
          {
            "time": 1776726000,
            "open": 75974.24,
            "close": 75840.97,
            "max": 75974.24,
            "min": 75617.6,
            "volume": 301.78
          },
          {
            "time": 1776722400,
            "open": 75954.72,
            "close": 75974.24,
            "max": 76143.71,
            "min": 75904.39,
            "volume": 220.64
          },
          {
            "time": 1776718800,
            "open": 76276.18,
            "close": 75954.71,
            "max": 76357.2,
            "min": 75784.05,
            "volume": 523.28
          },
          {
            "time": 1776715200,
            "open": 76296.97,
            "close": 76276.17,
            "max": 76558.62,
            "min": 76113.07,
            "volume": 1418.86
          },
          {
            "time": 1776711600,
            "open": 76423.69,
            "close": 76296.96,
            "max": 76486.67,
            "min": 76154.49,
            "volume": 1368.12
          },
          {
            "time": 1776708000,
            "open": 75898.14,
            "close": 76423.69,
            "max": 76453.19,
            "min": 75898.14,
            "volume": 1544.76
          },
          {
            "time": 1776704400,
            "open": 75338.75,
            "close": 75898.14,
            "max": 75991.47,
            "min": 75289.92,
            "volume": 642.61
          },
          {
            "time": 1776700800,
            "open": 75716.78,
            "close": 75338.74,
            "max": 75723.99,
            "min": 75299.26,
            "volume": 630.72
          },
          {
            "time": 1776697200,
            "open": 75034.79,
            "close": 75716.77,
            "max": 75772.72,
            "min": 74702,
            "volume": 1196.95
          }
        ],
        "info": {
          "series_id": "ser_1",
          "source2": {
            "country": "MT",
            "description": "Binance",
            "exchange-type": "exchange",
            "id": "BINANCE",
            "name": "Binance",
            "url": "https://www.binance.com/en"
          },
          "currency_code": "USDT",
          "source_id": "BINANCE",
          "subsession_id": "regular",
          "provider_id": "binance",
          "base_currency_id": "XTVCBTC",
          "base_currency": "BTC",
          "currency_id": "XTVCUSDT",
          "format": "price",
          "formatter": "price",
          "pro_perm": "",
          "volume_type": "base",
          "measure": "price",
          "allowed_adjustment": "none",
          "short_description": "Bitcoin / TetherUS",
          "variable_tick_size": "",
          "name": "BTCUSDT",
          "full_name": "BINANCE:BTCUSDT",
          "pro_name": "BINANCE:BTCUSDT",
          "base_name": [
            "BINANCE:BTCUSDT"
          ],
          "description": "Bitcoin / TetherUS",
          "exchange": "Binance",
          "pricescale": 100,
          "pointvalue": 1,
          "minmov": 1,
          "session": "24x7",
          "session_display": "24x7",
          "subsessions": [
            {
              "description": "Regular Trading Hours",
              "id": "regular",
              "private": false,
              "session": "24x7",
              "session-display": "24x7"
            }
          ],
          "type": "spot",
          "typespecs": [
            "crypto",
            "defi"
          ],
          "has_intraday": true,
          "fractional": false,
          "listed_exchange": "BINANCE",
          "legs": [
            "BINANCE:BTCUSDT"
          ],
          "is_tradable": true,
          "minmove2": 0,
          "timezone": "Etc/UTC",
          "aliases": [],
          "alternatives": [],
          "is_replayable": true,
          "has_adjustment": false,
          "has_extended_hours": false,
          "bar_source": "trade",
          "bar_transform": "none",
          "bar_fillgaps": false,
          "visible_plots_set": "ohlcv",
          "is-tickbars-available": true,
          "exchange_listed_name": "Binance"
        }
      }
    ]
  },
  "msg": "Success"
}
```
