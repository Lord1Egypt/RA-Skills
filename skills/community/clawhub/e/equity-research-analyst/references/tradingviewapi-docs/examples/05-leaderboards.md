# Leaderboards

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Get Stock Leaderboard

`GET /api/leaderboard/stocks`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/stocks?tab=gainers&market_code=america&columnset=overview&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 2081,
    "data": [
      {
        "rank": 1,
        "symbol": "NASDAQ:ENVB",
        "description": "Enveric Biosciences, Inc.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "enveric-biosciences",
          "style": "single"
        },
        "logoid": "enveric-biosciences",
        "name": "ENVB",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 100.54945054945054,
        "price": 3.65,
        "currency": "USD",
        "volume": 158694731,
        "relativevolume": 125.31953277558104,
        "marketcap": 6889503.000000001,
        "pricetoearnings": null,
        "epsdiluted": -40.8497,
        "epsdilutedgrowth": 84.04362197207438,
        "dividendsyield": 0,
        "sector": "Health technology",
        "analystrating": "NoRating"
      },
      {
        "rank": 2,
        "symbol": "NASDAQ:FGI",
        "description": "FGI Industries Ltd.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "fgi-industries-ltd",
          "style": "single"
        },
        "logoid": "fgi-industries-ltd",
        "name": "FGI",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 50.615384615384606,
        "price": 9.79,
        "currency": "USD",
        "volume": 2517949,
        "relativevolume": 23.441360036047172,
        "marketcap": 18868522,
        "pricetoearnings": null,
        "epsdiluted": -3.1998,
        "epsdilutedgrowth": -408.3081810961081,
        "dividendsyield": 0,
        "sector": "Producer manufacturing",
        "analystrating": "StrongBuy"
      },
      {
        "rank": 3,
        "symbol": "NASDAQ:PBM",
        "description": "Psyence Biomedical Ltd.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "psyence",
          "style": "single"
        },
        "logoid": "psyence",
        "name": "PBM",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 48.68421052631581,
        "price": 11.3,
        "currency": "USD",
        "volume": 42269832,
        "relativevolume": 4.045649231514533,
        "marketcap": 11550600,
        "pricetoearnings": null,
        "epsdiluted": null,
        "epsdilutedgrowth": null,
        "dividendsyield": null,
        "sector": "Health technology",
        "analystrating": "NoRating"
      },
      {
        "rank": 4,
        "symbol": "NASDAQ:JLHL",
        "description": "Julong Holding Limited",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "julong-limited",
          "style": "single"
        },
        "logoid": "julong-limited",
        "name": "JLHL",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 48.661417322834644,
        "price": 9.44,
        "currency": "USD",
        "volume": 1477700,
        "relativevolume": 9.218277354303869,
        "marketcap": 202475079,
        "pricetoearnings": 55.62757807896288,
        "epsdiluted": 0.1697,
        "epsdilutedgrowth": null,
        "dividendsyield": 0,
        "sector": "Commercial services",
        "analystrating": "NoRating"
      },
      {
        "rank": 5,
        "symbol": "NASDAQ:INV",
        "description": "Innventure, Inc.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "innventure",
          "style": "single"
        },
        "logoid": "innventure",
        "name": "INV",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 34.565217391304365,
        "price": 6.19,
        "currency": "USD",
        "volume": 7117099,
        "relativevolume": 6.181688386091924,
        "marketcap": 495629099.99999994,
        "pricetoearnings": null,
        "epsdiluted": -5.7593,
        "epsdilutedgrowth": -195.39416320459557,
        "dividendsyield": 0,
        "sector": "Miscellaneous",
        "analystrating": "StrongBuy"
      }
    ],
    "metadata": {
      "asset_type": "stocks",
      "tab": {
        "id": "stocks_market_movers.gainers",
        "title": "Top gainers"
      },
      "market": {
        "name": "United States",
        "market_code": "america",
        "exchanges": [
          "NASDAQ",
          "NYSE",
          "NYSE ARCA",
          "OTC"
        ]
      },
      "columnset": {
        "id": "overview",
        "title": "Overview"
      }
    }
  },
  "msg": "Success"
}
```

## Get Index Leaderboard

`GET /api/leaderboard/indices`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/indices?tab=major&columnset=overview&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 25,
    "data": [
      {
        "rank": 1,
        "symbol": "SP:SPX",
        "base-currency-logoid": null,
        "description": "S&P 500",
        "exchange": "SP",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "indices/s-and-p-500",
          "style": "single"
        },
        "logoid": "indices/s-and-p-500",
        "name": "SPX",
        "type": "index",
        "typespecs": [
          "main",
          "cfd"
        ],
        "price": 7109.13,
        "currency": "USD",
        "change": -0.237438693245207,
        "changeabs": -16.920000000000073,
        "high": 7122.65,
        "low": 7084.41,
        "technicalrating": "Buy"
      },
      {
        "rank": 2,
        "symbol": "TVC:IXIC",
        "base-currency-logoid": null,
        "description": "US Composite Index",
        "exchange": "TVC",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "indices/nasdaq-composite",
          "style": "single"
        },
        "logoid": "indices/nasdaq-composite",
        "name": "IXIC",
        "type": "index",
        "typespecs": [
          "cfd"
        ],
        "price": 24404.3934,
        "currency": "USD",
        "change": -0.26191655122154434,
        "changeabs": -64.08699999999953,
        "high": 24435.9243,
        "low": 24221.5308,
        "technicalrating": "Buy"
      },
      {
        "rank": 3,
        "symbol": "DJ:DJI",
        "base-currency-logoid": null,
        "description": "Dow Jones Industrial Average Index",
        "exchange": "DJ",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "indices/dow-30",
          "style": "single"
        },
        "logoid": "indices/dow-30",
        "name": "DJI",
        "type": "index",
        "typespecs": [
          "main",
          "cfd"
        ],
        "price": 49442.57,
        "currency": "USD",
        "change": -0.009848841517382132,
        "changeabs": -4.870000000002619,
        "high": 49489.63,
        "low": 49245.6,
        "technicalrating": "Buy"
      },
      {
        "rank": 4,
        "symbol": "CBOE:VIX",
        "base-currency-logoid": null,
        "description": "CBOE Volatility Index",
        "exchange": "CBOE",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "indices/volatility-s-and-p-500",
          "style": "single"
        },
        "logoid": "indices/volatility-s-and-p-500",
        "name": "VIX",
        "type": "index",
        "typespecs": [
          "main"
        ],
        "price": 18.91,
        "currency": null,
        "change": 0.2119766825649133,
        "changeabs": 0.03999999999999915,
        "high": 19.19,
        "low": 18.9,
        "technicalrating": "Sell"
      },
      {
        "rank": 5,
        "symbol": "TSX:TSX",
        "base-currency-logoid": null,
        "description": "S&P/TSX Composite index",
        "exchange": "TSX",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "indices/s-and-p-tsx-composite-index",
          "style": "single"
        },
        "logoid": "indices/s-and-p-tsx-composite-index",
        "name": "TSX",
        "type": "index",
        "typespecs": [
          "main"
        ],
        "price": 34360.03,
        "currency": "CAD",
        "change": 0.040004320699551434,
        "changeabs": 13.739999999997963,
        "high": 34371.89,
        "low": 34211.75,
        "technicalrating": "Buy"
      }
    ],
    "metadata": {
      "asset_type": "indices",
      "tab": {
        "id": "indices_quotes.major",
        "title": "Major world indices"
      },
      "market": null,
      "columnset": {
        "id": "overview",
        "title": "Overview"
      }
    }
  },
  "msg": "Success"
}
```

## Get Crypto Leaderboard

`GET /api/leaderboard/crypto`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/crypto?tab=gainers&columnset=overview&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 157,
    "data": [
      {
        "rank": 82,
        "symbol": "CRYPTO:RAVEDUSD",
        "base-currency-logoid": "crypto/XTVCRAVED",
        "description": "RaveDAO",
        "exchange": "CRYPTO",
        "logo": {
          "logoid": "crypto/XTVCRAVED",
          "style": "single"
        },
        "name": "RAVE",
        "type": "spot",
        "typespecs": [
          "crypto",
          "cryptoasset",
          "synthetic"
        ],
        "price": 1.75596,
        "currency": "USD",
        "changecrypto": 99.43774628006821,
        "marketcapcalc": 435556046.13233805,
        "volume24hcoin": 709259270.9241372,
        "supplycirculating": 248044400.858982,
        "volumetomarketcap": 1.6283995532199271,
        "socialdominance": null,
        "cryptocategory": [
          "Social media and content",
          "DAO"
        ],
        "technicalrating": "Sell"
      },
      {
        "rank": 21,
        "symbol": "CRYPTO:MEMECOREUSD",
        "base-currency-logoid": "crypto/XTVCMEMECORE",
        "description": "MemeCore",
        "exchange": "CRYPTO",
        "logo": {
          "logoid": "crypto/XTVCMEMECORE",
          "style": "single"
        },
        "name": "M",
        "type": "spot",
        "typespecs": [
          "crypto",
          "cryptoasset",
          "synthetic"
        ],
        "price": 4.1654,
        "currency": "USD",
        "changecrypto": 19.829153559781812,
        "marketcapcalc": 5384309049.725333,
        "volume24hcoin": 21060537.21436149,
        "supplycirculating": 1292627130.5817769,
        "volumetomarketcap": 0.003911465151770186,
        "socialdominance": 0.05678098571791206,
        "cryptocategory": [
          "Memes",
          "Layer 1"
        ],
        "technicalrating": "StrongBuy"
      },
      {
        "rank": 102,
        "symbol": "CRYPTO:IMXUSD",
        "base-currency-logoid": "crypto/XTVCIMXIMMUTABLEX",
        "description": "Immutable",
        "exchange": "CRYPTO",
        "logo": {
          "logoid": "crypto/XTVCIMXIMMUTABLEX",
          "style": "single"
        },
        "name": "IMX",
        "type": "spot",
        "typespecs": [
          "crypto",
          "cryptoasset",
          "synthetic"
        ],
        "price": 0.17756,
        "currency": "USD",
        "changecrypto": 10.803721975894593,
        "marketcapcalc": 355120000,
        "volume24hcoin": 20965573.08595738,
        "supplycirculating": 2000000000,
        "volumetomarketcap": 0.05903799584917036,
        "socialdominance": 0.1193453057513071,
        "cryptocategory": [
          "Developments tools",
          "Gaming",
          "NFTs and collectibles",
          "Scaling",
          "Marketplace"
        ],
        "technicalrating": "Buy"
      },
      {
        "rank": 107,
        "symbol": "CRYPTO:SPX6USD",
        "base-currency-logoid": "crypto/XTVCSPX6",
        "description": "SPX6900",
        "exchange": "CRYPTO",
        "logo": {
          "logoid": "crypto/XTVCSPX6",
          "style": "single"
        },
        "name": "SPX",
        "type": "spot",
        "typespecs": [
          "crypto",
          "cryptoasset",
          "synthetic"
        ],
        "price": 0.35716,
        "currency": "USD",
        "changecrypto": 10.446792732665926,
        "marketcapcalc": 332513492.0494012,
        "volume24hcoin": 9932211.40528916,
        "supplycirculating": 930993090.07,
        "volumetomarketcap": 0.02987010044035609,
        "socialdominance": 0.7318067041643843,
        "cryptocategory": [
          "Memes"
        ],
        "technicalrating": "Buy"
      },
      {
        "rank": 129,
        "symbol": "CRYPTO:PENDLEUSD",
        "base-currency-logoid": "crypto/XTVCPENDLEPENDLE",
        "description": "Pendle",
        "exchange": "CRYPTO",
        "logo": {
          "logoid": "crypto/XTVCPENDLEPENDLE",
          "style": "single"
        },
        "name": "PENDLE",
        "type": "spot",
        "typespecs": [
          "crypto",
          "cryptoasset",
          "synthetic"
        ],
        "price": 1.3993,
        "currency": "USD",
        "changecrypto": 9.685761303973038,
        "marketcapcalc": 233551217.30366603,
        "volume24hcoin": 40472683.21702509,
        "supplycirculating": 166905750.94952193,
        "volumetomarketcap": 0.17329253807485845,
        "socialdominance": 0.022899589478892264,
        "cryptocategory": [
          "Social media and content",
          "DeFi",
          "Web3",
          "Real-world assets"
        ],
        "technicalrating": "Buy"
      }
    ],
    "metadata": {
      "asset_type": "crypto",
      "tab": {
        "id": "crypto_coins.gainers",
        "title": "Gainers"
      },
      "market": null,
      "columnset": {
        "id": "overview",
        "title": "Overview"
      }
    }
  },
  "msg": "Success"
}
```

## Get Futures Leaderboard

`GET /api/leaderboard/futures`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/futures?tab=all&columnset=overview&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 489,
    "data": [
      {
        "rank": 1,
        "symbol": "CBOT_MINI:10Y1!",
        "base-currency-logoid": null,
        "description": "10-Year Yield Futures",
        "exchange": "CBOT_MINI",
        "kind": "delay",
        "kind-delay": 600,
        "logo": {
          "logoid": "indices/micro-10-year",
          "style": "single"
        },
        "logoid": "indices/micro-10-year",
        "name": "10Y1!",
        "type": "futures",
        "typespecs": [
          "continuous",
          "micro",
          "synthetic"
        ],
        "price": 4.252,
        "currency": "USD",
        "change": 0.04705882352940658,
        "changeabs": 0.0019999999999997797,
        "high": 4.261,
        "low": 4.239,
        "technicalrating": "Sell"
      },
      {
        "rank": 2,
        "symbol": "COMEX:1OZ1!",
        "base-currency-logoid": null,
        "description": "1-Ounce Gold Futures",
        "exchange": "COMEX",
        "kind": "delay",
        "kind-delay": 600,
        "logo": {
          "logoid": "metal/gold",
          "style": "single"
        },
        "logoid": "metal/gold",
        "name": "1OZ1!",
        "type": "futures",
        "typespecs": [
          "continuous",
          "synthetic"
        ],
        "price": 4805.75,
        "currency": "USD",
        "change": -0.4763137457934248,
        "changeabs": -23,
        "high": 4857,
        "low": 4791,
        "technicalrating": "Buy"
      },
      {
        "rank": 3,
        "symbol": "CBOT_MINI:2YY1!",
        "base-currency-logoid": null,
        "description": "2-Year Yield Futures",
        "exchange": "CBOT_MINI",
        "kind": "delay",
        "kind-delay": 600,
        "logo": {
          "logoid": "indices/micro-2-year",
          "style": "single"
        },
        "logoid": "indices/micro-2-year",
        "name": "2YY1!",
        "type": "futures",
        "typespecs": [
          "continuous",
          "micro",
          "synthetic"
        ],
        "price": 3.806,
        "currency": "USD",
        "change": 0,
        "changeabs": 0,
        "high": 3.806,
        "low": 3.806,
        "technicalrating": "Buy"
      },
      {
        "rank": 4,
        "symbol": "CBOT_MINI:30Y1!",
        "base-currency-logoid": null,
        "description": "30-Year Yield Futures",
        "exchange": "CBOT_MINI",
        "kind": "delay",
        "kind-delay": 600,
        "logo": {
          "logoid": "indices/micro-30-year",
          "style": "single"
        },
        "logoid": "indices/micro-30-year",
        "name": "30Y1!",
        "type": "futures",
        "typespecs": [
          "continuous",
          "micro",
          "synthetic"
        ],
        "price": 4.908,
        "currency": "USD",
        "change": 0,
        "changeabs": 0,
        "high": 4.908,
        "low": 4.908,
        "technicalrating": "Buy"
      },
      {
        "rank": 5,
        "symbol": "CBOT:55U1!",
        "base-currency-logoid": null,
        "description": "30-Year UMBS TBA Futures - 5.5% Coupon",
        "exchange": "CBOT",
        "kind": "delay",
        "kind-delay": 600,
        "logo": {
          "logoid": "indices/30-year-umbs-tba",
          "style": "single"
        },
        "logoid": "indices/30-year-umbs-tba",
        "name": "55U1!",
        "type": "futures",
        "typespecs": [
          "continuous",
          "synthetic"
        ],
        "price": 101.0625,
        "currency": "USD",
        "change": -0.02318621211191485,
        "changeabs": -0.023437999999998738,
        "high": 101.0625,
        "low": 101.0625,
        "technicalrating": "Buy"
      }
    ],
    "metadata": {
      "asset_type": "futures",
      "tab": {
        "id": "futures.quotes_all",
        "title": "All futures"
      },
      "market": null,
      "columnset": {
        "id": "overview",
        "title": "Overview"
      }
    }
  },
  "msg": "Success"
}
```

## Get Forex Leaderboard

`GET /api/leaderboard/forex`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/forex?tab=major&columnset=overview&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 7,
    "data": [
      {
        "rank": 1,
        "symbol": "FX_IDC:EURUSD",
        "base-currency-logoid": "country/EU",
        "currency-logoid": "country/US",
        "description": "EURO / U.S. DOLLAR",
        "exchange": "FX_IDC",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/EU",
          "logoid2": "country/US",
          "style": "pair"
        },
        "logoid": "",
        "name": "EURUSD",
        "type": "forex",
        "typespecs": [
          ""
        ],
        "price": 1.17594,
        "currency": "USD",
        "change": -0.21722528638100277,
        "changeabs": -0.0025600000000001177,
        "bid": 1.17587,
        "ask": 1.17594,
        "high": 1.1791,
        "low": 1.17566,
        "technicalrating": "Buy"
      },
      {
        "rank": 2,
        "symbol": "FX_IDC:USDJPY",
        "base-currency-logoid": "country/US",
        "currency-logoid": "country/JP",
        "description": "U.S. DOLLAR / JAPANESE YEN",
        "exchange": "FX_IDC",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/US",
          "logoid2": "country/JP",
          "style": "pair"
        },
        "logoid": "",
        "name": "USDJPY",
        "type": "forex",
        "typespecs": [
          ""
        ],
        "price": 159.193,
        "currency": "JPY",
        "change": 0.2790551181102438,
        "changeabs": 0.44300000000001205,
        "bid": 159.196,
        "ask": 159.203,
        "high": 159.254,
        "low": 158.744,
        "technicalrating": "Buy"
      },
      {
        "rank": 3,
        "symbol": "FX_IDC:GBPUSD",
        "base-currency-logoid": "country/GB",
        "currency-logoid": "country/US",
        "description": "BRITISH POUND / U.S. DOLLAR",
        "exchange": "FX_IDC",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/GB",
          "logoid2": "country/US",
          "style": "pair"
        },
        "logoid": "",
        "name": "GBPUSD",
        "type": "forex",
        "typespecs": [
          ""
        ],
        "price": 1.3509,
        "currency": "USD",
        "change": -0.16996748448122737,
        "changeabs": -0.0022999999999999687,
        "bid": 1.3508,
        "ask": 1.3509,
        "high": 1.3539,
        "low": 1.3483,
        "technicalrating": "Buy"
      },
      {
        "rank": 4,
        "symbol": "FX_IDC:AUDUSD",
        "base-currency-logoid": "country/AU",
        "currency-logoid": "country/US",
        "description": "AUSTRALIAN DOLLAR / U.S. DOLLAR",
        "exchange": "FX_IDC",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/AU",
          "logoid2": "country/US",
          "style": "pair"
        },
        "logoid": "",
        "name": "AUDUSD",
        "type": "forex",
        "typespecs": [
          ""
        ],
        "price": 0.7158,
        "currency": "USD",
        "change": -0.17989373718780255,
        "changeabs": -0.0012900000000000134,
        "bid": 0.71577,
        "ask": 0.71581,
        "high": 0.7183,
        "low": 0.71438,
        "technicalrating": "Buy"
      },
      {
        "rank": 5,
        "symbol": "FX_IDC:USDCAD",
        "base-currency-logoid": "country/US",
        "currency-logoid": "country/CA",
        "description": "U.S. DOLLAR / CANADIAN DOLLAR",
        "exchange": "FX_IDC",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/US",
          "logoid2": "country/CA",
          "style": "pair"
        },
        "logoid": "",
        "name": "USDCAD",
        "type": "forex",
        "typespecs": [
          ""
        ],
        "price": 1.366,
        "currency": "CAD",
        "change": 0.10993037742763334,
        "changeabs": 0.0015000000000000568,
        "bid": 1.36593,
        "ask": 1.36603,
        "high": 1.36637,
        "low": 1.36389,
        "technicalrating": "Sell"
      }
    ],
    "metadata": {
      "asset_type": "forex",
      "tab": {
        "id": "currencies_rates.major",
        "title": "Major"
      },
      "market": null,
      "columnset": {
        "id": "overview",
        "title": "Overview"
      }
    }
  },
  "msg": "Success"
}
```

## Get Government Bond Leaderboard

`GET /api/leaderboard/bonds`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/bonds?tab=major&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 17,
    "data": [
      {
        "rank": 1,
        "symbol": "TVC:US10Y",
        "description": "United States 10 Year Government Bonds Yield",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/US",
          "style": "single"
        },
        "logoid": "country/US",
        "name": "US10Y",
        "type": "bond",
        "typespecs": [
          "government",
          "yield",
          "benchmark"
        ],
        "coupon": 4.125,
        "bondyield": 4.258,
        "maturitydate": 20360215,
        "timetomaturity": 3587,
        "bondprice": 98.9375,
        "currency": "PCTPAR",
        "change": 0,
        "bondchangeabs": 0
      },
      {
        "rank": 2,
        "symbol": "TVC:CA10Y",
        "description": "Canada 10 Year Government Bonds Yield",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/CA",
          "style": "single"
        },
        "logoid": "country/CA",
        "name": "CA10Y",
        "type": "bond",
        "typespecs": [
          "government",
          "yield",
          "benchmark"
        ],
        "coupon": 3.25,
        "bondyield": 3.44,
        "maturitydate": 20351201,
        "timetomaturity": 3511,
        "bondprice": 98.452,
        "currency": "PCTPAR",
        "change": 0.029078220412907526,
        "bondchangeabs": 0.0009999999999998899
      },
      {
        "rank": 3,
        "symbol": "TVC:GB10Y",
        "description": "United Kingdom 10 Year Government Bonds Yield",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/GB",
          "style": "single"
        },
        "logoid": "country/GB",
        "name": "GB10Y",
        "type": "bond",
        "typespecs": [
          "government",
          "yield",
          "benchmark"
        ],
        "coupon": 4.75,
        "bondyield": 4.838,
        "maturitydate": 20351022,
        "timetomaturity": 3471,
        "bondprice": 99.333,
        "currency": "PCTPAR",
        "change": 0.04135649296939164,
        "bondchangeabs": 0.0019999999999997797
      },
      {
        "rank": 4,
        "symbol": "TVC:DE10Y",
        "description": "Germany 10 Year Government Bonds Yield",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/DE",
          "style": "single"
        },
        "logoid": "country/DE",
        "name": "DE10Y",
        "type": "bond",
        "typespecs": [
          "government",
          "yield",
          "benchmark"
        ],
        "coupon": 2.9,
        "bondyield": 2.9747,
        "maturitydate": 20360215,
        "timetomaturity": 3587,
        "bondprice": 99.359,
        "currency": "PCTPAR",
        "change": -0.09068314636931299,
        "bondchangeabs": -0.0026999999999999247
      },
      {
        "rank": 5,
        "symbol": "TVC:FR10Y",
        "description": "France 10 Year Government Bonds Yield",
        "kind": "rt",
        "kind-delay": 0,
        "logo": {
          "logoid": "country/FR",
          "style": "single"
        },
        "logoid": "country/FR",
        "name": "FR10Y",
        "type": "bond",
        "typespecs": [
          "government",
          "yield",
          "benchmark"
        ],
        "coupon": 3.5,
        "bondyield": 3.6019,
        "maturitydate": 20351125,
        "timetomaturity": 3505,
        "bondprice": 99.171,
        "currency": "PCTPAR",
        "change": -0.135854497061098,
        "bondchangeabs": -0.004899999999999682
      }
    ],
    "metadata": {
      "asset_type": "bonds",
      "tab": {
        "id": "government_bonds.major_10y",
        "title": "Major 10Y"
      },
      "market": null,
      "columnset": null
    }
  },
  "msg": "Success"
}
```

## Get Corporate Bond Leaderboard

`GET /api/leaderboard/corporate-bonds`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/corporate-bonds?tab=highest-yield&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 627,
    "data": [
      {
        "rank": 1,
        "symbol": "SWB:US71654QDD16",
        "ticker": "US71654QDD16",
        "currency": "USD",
        "yieldtomaturity": 8.497230699706515,
        "issuercountry": "Mexico",
        "bondclose": 91.72999999999999,
        "volume1d": 0,
        "currentcoupon": 7.69,
        "maturitydate": 20500123,
        "outstandingamount": 8047831000,
        "facevalue": 1000,
        "minimumdenominationamount": 10000
      },
      {
        "rank": 2,
        "symbol": "LUXSE:US40049JBC09",
        "ticker": "US40049JBC09",
        "currency": "USD",
        "yieldtomaturity": 8.479468404049362,
        "issuercountry": "Mexico",
        "bondclose": 77.554,
        "volume1d": 1,
        "currentcoupon": 6.125,
        "maturitydate": 20460131,
        "outstandingamount": 879572000,
        "facevalue": 1000,
        "minimumdenominationamount": 200000
      },
      {
        "rank": 3,
        "symbol": "FINRA:TV4837441",
        "ticker": "TV4837441",
        "currency": "USD",
        "yieldtomaturity": 8.4404706366076,
        "issuercountry": "Mexico",
        "bondclose": 67.75,
        "volume1d": 1000000,
        "currentcoupon": 5.25,
        "maturitydate": 20490524,
        "outstandingamount": 660928000,
        "facevalue": 1000,
        "minimumdenominationamount": 200000
      },
      {
        "rank": 4,
        "symbol": "FINRA:PEMX5055132",
        "ticker": "PEMX5055132",
        "currency": "USD",
        "yieldtomaturity": 8.41208102530131,
        "issuercountry": "Mexico",
        "bondclose": 83.615,
        "volume1d": 9870000,
        "currentcoupon": 6.95,
        "maturitydate": 20600128,
        "outstandingamount": 3796812000,
        "facevalue": 1000,
        "minimumdenominationamount": 10000
      },
      {
        "rank": 5,
        "symbol": "LUXSE:US40049JBA43",
        "ticker": "US40049JBA43",
        "currency": "USD",
        "yieldtomaturity": 8.374341320144252,
        "issuercountry": "Mexico",
        "bondclose": 68.081,
        "volume1d": 1,
        "currentcoupon": 5,
        "maturitydate": 20450513,
        "outstandingamount": 790610000,
        "facevalue": 1000,
        "minimumdenominationamount": 200000
      }
    ],
    "metadata": {
      "asset_type": "corporate_bonds",
      "tab": {
        "id": "corporate_bonds.rates_highest_yield",
        "title": "Highest yield"
      },
      "market": null,
      "columnset": null
    }
  },
  "msg": "Success"
}
```

## Get ETF Leaderboard

`GET /api/leaderboard/etfs`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/etfs?tab=largest&columnset=overview&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 5944,
    "data": [
      {
        "rank": 1,
        "symbol": "AMEX:VOO",
        "description": "Vanguard S&P 500 ETF",
        "exchange": "AMEX",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "vanguard",
          "style": "single"
        },
        "logoid": "vanguard",
        "name": "VOO",
        "type": "fund",
        "typespecs": [
          "etf"
        ],
        "assetsundermanagement": 908262081825.198,
        "currency": "USD",
        "price": 651.54,
        "change": -0.18995680014706473,
        "volumeprice": 4159486089.3599997,
        "relativevolume": 1.0299532403509462,
        "navtotalreturn": 79.09250267149382,
        "expenseratio": 0.03,
        "assetclass": "Equity",
        "focus": "Large cap"
      },
      {
        "rank": 2,
        "symbol": "AMEX:IVV",
        "description": "iShares Core S&P 500 ETF",
        "exchange": "AMEX",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "ishares",
          "style": "single"
        },
        "logoid": "ishares",
        "name": "IVV",
        "type": "fund",
        "typespecs": [
          "etf"
        ],
        "assetsundermanagement": 783684064948,
        "currency": "USD",
        "price": 712.09,
        "change": -0.17803072782325638,
        "volumeprice": 3576911384.53,
        "relativevolume": 0.9925793037669888,
        "navtotalreturn": 79.11221282393261,
        "expenseratio": 0.03,
        "assetclass": "Equity",
        "focus": "Large cap"
      },
      {
        "rank": 3,
        "symbol": "AMEX:SPY",
        "description": "SPDR S&P 500 ETF TRUST",
        "exchange": "AMEX",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "spdr-sandp500-etf-tr",
          "style": "single"
        },
        "logoid": "spdr-sandp500-etf-tr",
        "name": "SPY",
        "type": "fund",
        "typespecs": [
          "etf"
        ],
        "assetsundermanagement": 714796356873.986,
        "currency": "USD",
        "price": 708.72,
        "change": -0.19996057115497776,
        "volumeprice": 30861987739.68,
        "relativevolume": 0.7274399436694816,
        "navtotalreturn": 78.17864756902947,
        "expenseratio": 0.0945,
        "assetclass": "Equity",
        "focus": "Large cap"
      },
      {
        "rank": 4,
        "symbol": "AMEX:VTI",
        "description": "Vanguard Total Stock Market ETF",
        "exchange": "AMEX",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "vanguard",
          "style": "single"
        },
        "logoid": "vanguard",
        "name": "VTI",
        "type": "fund",
        "typespecs": [
          "etf"
        ],
        "assetsundermanagement": 615195414982.1,
        "currency": "USD",
        "price": 350.21,
        "change": -0.09129033178329764,
        "volumeprice": 1419797917.9299998,
        "relativevolume": 1.0709959018447286,
        "navtotalreturn": 77.85213109361979,
        "expenseratio": 0.03,
        "assetclass": "Equity",
        "focus": "Total market"
      },
      {
        "rank": 5,
        "symbol": "NASDAQ:QQQ",
        "description": "Invesco QQQ Trust, Series 1",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "invesco",
          "style": "single"
        },
        "logoid": "invesco",
        "name": "QQQ",
        "type": "fund",
        "typespecs": [
          "etf"
        ],
        "assetsundermanagement": 425337228750,
        "currency": "USD",
        "price": 646.79,
        "change": -0.31748478076597964,
        "volumeprice": 24020817529.69,
        "relativevolume": 0.8274630729409178,
        "navtotalreturn": 107.89327700983571,
        "expenseratio": 0.18,
        "assetclass": "Equity",
        "focus": "Large cap"
      }
    ],
    "metadata": {
      "asset_type": "etfs",
      "tab": {
        "id": "etfs_funds.largest",
        "title": "Largest"
      },
      "market": null,
      "columnset": {
        "id": "overview",
        "title": "Overview"
      }
    }
  },
  "msg": "Success"
}
```

## Get Generic Leaderboard Data

`GET /api/leaderboard/data`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/leaderboard/data?id=stocks_market_movers.gainers&market_code=america&columnset=overview&start=0&count=5&lang=en' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalCount": 2081,
    "data": [
      {
        "rank": 1,
        "symbol": "NASDAQ:ENVB",
        "description": "Enveric Biosciences, Inc.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "enveric-biosciences",
          "style": "single"
        },
        "logoid": "enveric-biosciences",
        "name": "ENVB",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 100.54945054945054,
        "price": 3.65,
        "currency": "USD",
        "volume": 158694731,
        "relativevolume": 125.31953277558104,
        "marketcap": 6889503.000000001,
        "pricetoearnings": null,
        "epsdiluted": -40.8497,
        "epsdilutedgrowth": 84.04362197207438,
        "dividendsyield": 0,
        "sector": "Health technology",
        "analystrating": "NoRating"
      },
      {
        "rank": 2,
        "symbol": "NASDAQ:FGI",
        "description": "FGI Industries Ltd.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "fgi-industries-ltd",
          "style": "single"
        },
        "logoid": "fgi-industries-ltd",
        "name": "FGI",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 50.615384615384606,
        "price": 9.79,
        "currency": "USD",
        "volume": 2517949,
        "relativevolume": 23.441360036047172,
        "marketcap": 18868522,
        "pricetoearnings": null,
        "epsdiluted": -3.1998,
        "epsdilutedgrowth": -408.3081810961081,
        "dividendsyield": 0,
        "sector": "Producer manufacturing",
        "analystrating": "StrongBuy"
      },
      {
        "rank": 3,
        "symbol": "NASDAQ:PBM",
        "description": "Psyence Biomedical Ltd.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "psyence",
          "style": "single"
        },
        "logoid": "psyence",
        "name": "PBM",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 48.68421052631581,
        "price": 11.3,
        "currency": "USD",
        "volume": 42269832,
        "relativevolume": 4.045649231514533,
        "marketcap": 11550600,
        "pricetoearnings": null,
        "epsdiluted": null,
        "epsdilutedgrowth": null,
        "dividendsyield": null,
        "sector": "Health technology",
        "analystrating": "NoRating"
      },
      {
        "rank": 4,
        "symbol": "NASDAQ:JLHL",
        "description": "Julong Holding Limited",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "julong-limited",
          "style": "single"
        },
        "logoid": "julong-limited",
        "name": "JLHL",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 48.661417322834644,
        "price": 9.44,
        "currency": "USD",
        "volume": 1477700,
        "relativevolume": 9.218277354303869,
        "marketcap": 202475079,
        "pricetoearnings": 55.62757807896288,
        "epsdiluted": 0.1697,
        "epsdilutedgrowth": null,
        "dividendsyield": 0,
        "sector": "Commercial services",
        "analystrating": "NoRating"
      },
      {
        "rank": 5,
        "symbol": "NASDAQ:INV",
        "description": "Innventure, Inc.",
        "exchange": "NASDAQ",
        "kind": "delay",
        "kind-delay": 900,
        "logo": {
          "logoid": "innventure",
          "style": "single"
        },
        "logoid": "innventure",
        "name": "INV",
        "type": "stock",
        "typespecs": [
          "common"
        ],
        "change": 34.565217391304365,
        "price": 6.19,
        "currency": "USD",
        "volume": 7117099,
        "relativevolume": 6.181688386091924,
        "marketcap": 495629099.99999994,
        "pricetoearnings": null,
        "epsdiluted": -5.7593,
        "epsdilutedgrowth": -195.39416320459557,
        "dividendsyield": 0,
        "sector": "Miscellaneous",
        "analystrating": "StrongBuy"
      }
    ],
    "metadata": {
      "asset_type": "stocks",
      "tab": {
        "id": "stocks_market_movers.gainers",
        "title": "Top gainers"
      },
      "market": {
        "name": "United States",
        "market_code": "america",
        "exchanges": [
          "NASDAQ",
          "NYSE",
          "NYSE ARCA",
          "OTC"
        ]
      },
      "columnset": {
        "id": "overview",
        "title": "Overview"
      }
    }
  },
  "msg": "Success"
}
```
