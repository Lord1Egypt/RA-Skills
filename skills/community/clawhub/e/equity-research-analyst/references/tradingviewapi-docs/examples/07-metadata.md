# Metadata

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Get Market List

`GET /api/metadata/markets`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/metadata/markets' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": [
    "america",
    "canada",
    "austria",
    "belgium",
    "switzerland",
    "cyprus",
    "czech",
    "germany",
    "denmark",
    "estonia",
    "spain",
    "finland",
    "france",
    "greece",
    "hungary",
    "ireland",
    "iceland",
    "italy",
    "lithuania",
    "latvia",
    "luxembourg",
    "netherlands",
    "norway",
    "poland",
    "portugal",
    "serbia",
    "russia",
    "romania",
    "sweden",
    "slovakia",
    "turkey",
    "uk",
    "uae",
    "bahrain",
    "egypt",
    "israel",
    "kenya",
    "kuwait",
    "morocco",
    "nigeria",
    "qatar",
    "saudi-arabia",
    "tunisia",
    "south-africa",
    "argentina",
    "brazil",
    "chile",
    "colombia",
    "mexico",
    "peru",
    "venezuela",
    "australia",
    "bangladesh",
    "china",
    "hongkong",
    "indonesia",
    "india",
    "japan",
    "korea",
    "sri-lanka",
    "malaysia",
    "new-zealand",
    "philippines",
    "pakistan",
    "singapore",
    "thailand",
    "taiwan",
    "vietnam"
  ],
  "msg": "Success"
}
```

## Get World Economy Indicator Metadata

`GET /api/metadata/world-economy/indicators`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/metadata/world-economy/indicators?category=gdp' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "total": 25,
    "category": [
      "gdp"
    ],
    "categories": [
      {
        "category": "bsnss",
        "label": "Business"
      },
      {
        "category": "clmt",
        "label": "Climate"
      },
      {
        "category": "cnsm",
        "label": "Consumer"
      },
      {
        "category": "enrg",
        "label": "Energy"
      },
      {
        "category": "gdp",
        "label": "GDP"
      },
      {
        "category": "gov",
        "label": "Government"
      },
      {
        "category": "hlth",
        "label": "Health"
      },
      {
        "category": "hse",
        "label": "Housing"
      },
      {
        "category": "lbr",
        "label": "Labor"
      },
      {
        "category": "mny",
        "label": "Money"
      },
      {
        "category": "prce",
        "label": "Prices"
      },
      {
        "category": "trd",
        "label": "Trade"
      },
      {
        "category": "txs",
        "label": "Taxes"
      }
    ],
    "indicators": [
      {
        "slug": "economic-activity-index",
        "label": "Economic Activity Index",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "full-year-gdp-growth",
        "label": "Full Year GDP Growth",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp",
        "label": "GDP",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-external-demand-contribution",
        "label": "GDP External Demand Contribution",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-agriculture",
        "label": "GDP From Agriculture",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-construction",
        "label": "GDP From Construction",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-manufacturing",
        "label": "GDP From Manufacturing",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-mining",
        "label": "GDP From Mining",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-public-administration",
        "label": "GDP From Public Administration",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-services",
        "label": "GDP From Services",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-transport",
        "label": "GDP From Transport",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-from-utilities",
        "label": "GDP From Utilities",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-growth",
        "label": "GDP Growth",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-growth-annualized",
        "label": "GDP Growth Annualized",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-growth-rate",
        "label": "GDP Growth Rate",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-per-capita",
        "label": "GDP Per Capita",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-per-capita-ppp",
        "label": "GDP Per Capita PPP",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gdp-sales",
        "label": "GDP Sales",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gross-fixed-capital-formation",
        "label": "Gross Fixed Capital Formation",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "gross-national-product",
        "label": "Gross National Product",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "monthly-gdp-mom",
        "label": "Monthly GDP MoM",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "monthly-gdp-yoy",
        "label": "Monthly GDP YoY",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "real-consumer-spending",
        "label": "Real Consumer Spending",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "real-gdp",
        "label": "Real GDP",
        "categories": [
          "gdp"
        ]
      },
      {
        "slug": "weekly-economic-index",
        "label": "Weekly Economic Index",
        "categories": [
          "gdp"
        ]
      }
    ]
  },
  "msg": "Success"
}
```

## Get Tab Metadata

`GET /api/metadata/tabs`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/metadata/tabs?type=stocks' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": [
    {
      "id": "stocks_market_movers.all_stocks",
      "path": "all_stocks",
      "url": "/markets/stocks-china/market-movers-all-stocks/",
      "title": "All stocks",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.gainers",
      "path": "gainers",
      "url": "/markets/stocks-china/market-movers-gainers/",
      "title": "Top gainers",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.losers",
      "path": "losers",
      "url": "/markets/stocks-china/market-movers-losers/",
      "title": "Biggest losers",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.large_cap",
      "path": "large_cap",
      "url": "/markets/stocks-china/market-movers-large-cap/",
      "title": "Large-cap",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.small_cap",
      "path": "small_cap",
      "url": "/markets/stocks-china/market-movers-small-cap/",
      "title": "Small-cap",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.largest_employers",
      "path": "largest_employers",
      "url": "/markets/stocks-china/market-movers-largest-employers/",
      "title": "Largest employers",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.high_dividend",
      "path": "high_dividend",
      "url": "/markets/stocks-china/market-movers-high-dividend/",
      "title": "High-dividend",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.highest_net_income",
      "path": "highest_net_income",
      "url": "/markets/stocks-china/market-movers-highest-net-income/",
      "title": "Highest net income",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.highest_cash",
      "path": "highest_cash",
      "url": "/markets/stocks-china/market-movers-highest-cash/",
      "title": "Highest cash",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.highest_profit_per_employee",
      "path": "highest_profit_per_employee",
      "url": "/markets/stocks-china/market-movers-highest-profit-per-employee/",
      "title": "Highest profit per employee",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.highest_revenue_per_employee",
      "path": "highest_revenue_per_employee",
      "url": "/markets/stocks-china/market-movers-highest-revenue-per-employee/",
      "title": "Highest revenue per employee",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.active",
      "path": "active",
      "url": "/markets/stocks-china/market-movers-active/",
      "title": "Most active",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.unusual_volume",
      "path": "unusual_volume",
      "url": "/markets/stocks-china/market-movers-unusual-volume/",
      "title": "Unusual volume",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.most_volatile",
      "path": "most_volatile",
      "url": "/markets/stocks-china/market-movers-most-volatile/",
      "title": "Most volatile",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.high_beta",
      "path": "high_beta",
      "url": "/markets/stocks-china/market-movers-high-beta/",
      "title": "High beta",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.best_performing",
      "path": "best_performing",
      "url": "/markets/stocks-china/market-movers-best-performing/",
      "title": "Best performing",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.highest_revenue",
      "path": "highest_revenue",
      "url": "/markets/stocks-china/market-movers-highest-revenue/",
      "title": "Highest revenue",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.most_expensive",
      "path": "most_expensive",
      "url": "/markets/stocks-china/market-movers-most-expensive/",
      "title": "Most expensive",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.penny_stocks",
      "path": "penny_stocks",
      "url": "/markets/stocks-china/market-movers-penny-stocks/",
      "title": "Penny stocks",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.overbought",
      "path": "overbought",
      "url": "/markets/stocks-china/market-movers-overbought/",
      "title": "Overbought",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.oversold",
      "path": "oversold",
      "url": "/markets/stocks-china/market-movers-oversold/",
      "title": "Oversold",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.ath",
      "path": "ath",
      "url": "/markets/stocks-china/market-movers-ath/",
      "title": "All-time high",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.atl",
      "path": "atl",
      "url": "/markets/stocks-china/market-movers-atl/",
      "title": "All-time low",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.52wk_high",
      "path": "52wk_high",
      "url": "/markets/stocks-china/market-movers-52wk-high/",
      "title": "52-week high",
      "type": "stocks"
    },
    {
      "id": "stocks_market_movers.52wk_low",
      "path": "52wk_low",
      "url": "/markets/stocks-china/market-movers-52wk-low/",
      "title": "52-week low",
      "type": "stocks"
    }
  ],
  "msg": "Success"
}
```

## Get Columnset Metadata

`GET /api/metadata/columnsets`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/metadata/columnsets' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": [
    {
      "type": "stocks",
      "columnsets": [
        "overview",
        "performance",
        "valuation",
        "dividends",
        "profitability",
        "incomeStatement",
        "balanceSheet",
        "cashFlow",
        "technicals"
      ]
    },
    {
      "type": "indices",
      "columnsets": [
        "overview",
        "performance",
        "technicals"
      ]
    },
    {
      "type": "crypto",
      "columnsets": [
        "overview",
        "performance",
        "valuation",
        "addresses",
        "transactions",
        "sentiment",
        "technicals"
      ]
    },
    {
      "type": "futures",
      "columnsets": [
        "overview",
        "performance",
        "technicals"
      ]
    },
    {
      "type": "currencies",
      "columnsets": [
        "overview",
        "performance",
        "technicals"
      ]
    },
    {
      "type": "etfs",
      "columnsets": [
        "overview",
        "performance",
        "extendedHours",
        "fundFlows",
        "dividends",
        "navPerformance",
        "holdings",
        "risk",
        "technicals"
      ]
    }
  ],
  "msg": "Success"
}
```

## Get Language List

`GET /api/metadata/languages`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/metadata/languages' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": [
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "zh_CN",
      "name": "简体中文"
    },
    {
      "code": "de",
      "name": "Deutsch"
    },
    {
      "code": "fr",
      "name": "Français"
    },
    {
      "code": "es",
      "name": "Español"
    },
    {
      "code": "it",
      "name": "Italiano"
    },
    {
      "code": "pl",
      "name": "Polski"
    },
    {
      "code": "tr",
      "name": "Türkçe"
    },
    {
      "code": "ru",
      "name": "Русский"
    },
    {
      "code": "pt",
      "name": "Português"
    },
    {
      "code": "id",
      "name": "Bahasa Indonesia"
    },
    {
      "code": "ms",
      "name": "Bahasa Melayu"
    },
    {
      "code": "th",
      "name": "ภาษาไทย"
    },
    {
      "code": "vi",
      "name": "Tiếng Việt"
    },
    {
      "code": "ja",
      "name": "日本語"
    },
    {
      "code": "ko",
      "name": "한국어"
    },
    {
      "code": "zh_TW",
      "name": "繁體中文"
    },
    {
      "code": "ar",
      "name": "العربية"
    },
    {
      "code": "he",
      "name": "עברית"
    }
  ],
  "msg": "Success"
}
```

## Get Exchange List

`GET /api/metadata/exchanges`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/metadata/exchanges' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "totalExchanges": 353,
    "exchanges": [
      {
        "name": "LBank",
        "value": "LBANK",
        "desc": "LBank",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "lbank"
      },
      {
        "name": "LFJ V2.2 (Avalanche)",
        "value": "LFJ2DOT2",
        "desc": "LFJ V2.2 (Avalanche)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "lfj2dot2"
      },
      {
        "name": "BCHAIN (Nasdaq Data Link)",
        "value": "BCHAIN",
        "desc": "BCHAIN (Nasdaq Data Link)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "quandl_bchain"
      },
      {
        "name": "Biswap v2 (BNB chain)",
        "value": "BISWAP",
        "desc": "Biswap v2 (BNB chain)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "biswap"
      },
      {
        "name": "Bitazza",
        "value": "BITAZZA",
        "desc": "Bitazza",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitazza"
      },
      {
        "name": "Bithumb",
        "value": "BITHUMB",
        "desc": "Bithumb",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bithumb"
      },
      {
        "name": "Bitkub",
        "value": "BITKUB",
        "desc": "Bitkub",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitkub"
      },
      {
        "name": "Bitrue",
        "value": "BITRUE",
        "desc": "Bitrue",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitrue"
      },
      {
        "name": "BitMart",
        "value": "BITMART",
        "desc": "BitMart",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitmart"
      },
      {
        "name": "Bitso",
        "value": "BITSO",
        "desc": "Bitso",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitso"
      },
      {
        "name": "Coin Metrics",
        "value": "COINMETRICS",
        "desc": "Coin Metrics",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "coinmetrics"
      },
      {
        "name": "MEXC",
        "value": "MEXC",
        "desc": "MEXC",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "mexc"
      },
      {
        "name": "Gate",
        "value": "GATE",
        "desc": "Gate",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "gate"
      },
      {
        "name": "HTX",
        "value": "HTX",
        "desc": "HTX",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "htx"
      },
      {
        "name": "796",
        "value": "796",
        "desc": "796",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "DeDust.io (TON)",
        "value": "DEDUST",
        "desc": "DeDust.io (TON)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "dedust"
      },
      {
        "name": "Deepcoin",
        "value": "DEEPCOIN",
        "desc": "Deepcoin",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "deepcoin"
      },
      {
        "name": "Deribit",
        "value": "DERIBIT",
        "desc": "Deribit",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "deribit"
      },
      {
        "name": "DefiLlama",
        "value": "DEFILLAMA",
        "desc": "DefiLlama",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "defillama"
      },
      {
        "name": "Glassnode",
        "value": "GLASSNODE",
        "desc": "Glassnode",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "glassnode"
      },
      {
        "name": "Meteora DLMM (Solana)",
        "value": "METEORADLMM",
        "desc": "Meteora DLMM (Solana)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "meteoradlmm"
      },
      {
        "name": "Meteora DYN (Solana)",
        "value": "METEORADYN",
        "desc": "Meteora DYN (Solana)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "meteoradyn"
      },
      {
        "name": "OKX",
        "value": "OKX",
        "desc": "OKX",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "okx"
      },
      {
        "name": "Orca (Solana)",
        "value": "ORCA",
        "desc": "Orca (Solana)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "orca"
      },
      {
        "name": "Osmosis",
        "value": "OSMOSIS",
        "desc": "Osmosis",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "osmosis"
      },
      {
        "name": "Pangolin v2 (Avalanche)",
        "value": "PANGOLIN",
        "desc": "Pangolin v2 (Avalanche)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pangolin"
      },
      {
        "name": "PancakeSwap v2 (BNB chain)",
        "value": "PANCAKESWAP",
        "desc": "PancakeSwap v2 (BNB chain)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pancakeswap"
      },
      {
        "name": "Pancakeswap v3 (Arbitrum)",
        "value": "PANCAKESWAP3ARBITRUM",
        "desc": "Pancakeswap v3 (Arbitrum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pancakeswap3"
      },
      {
        "name": "Pancakeswap v3 (Base)",
        "value": "PANCAKESWAP3BASE",
        "desc": "Pancakeswap v3 (Base)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pancakeswap3"
      },
      {
        "name": "PancakeSwap v3 (BNB chain)",
        "value": "PANCAKESWAP3BSC",
        "desc": "PancakeSwap v3 (BNB chain)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pancakeswap3"
      },
      {
        "name": "PancakeSwap v3 (Ethereum)",
        "value": "PANCAKESWAP3ETH",
        "desc": "PancakeSwap v3 (Ethereum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pancakeswap3"
      },
      {
        "name": "PancakeSwap v3 (Linea)",
        "value": "PANCAKESWAP3LINEA",
        "desc": "PancakeSwap v3 (Linea)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pancakeswap3"
      },
      {
        "name": "Pancakeswap v3 (zkSync)",
        "value": "PANCAKESWAP3ZKSYNC",
        "desc": "Pancakeswap v3 (zkSync)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pancakeswap3"
      },
      {
        "name": "Curve (Ethereum)",
        "value": "CURVE",
        "desc": "Curve (Ethereum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "curve"
      },
      {
        "name": "Curve (Arbitrum)",
        "value": "CURVEARBITRUM",
        "desc": "Curve (Arbitrum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "curve"
      },
      {
        "name": "Pionex",
        "value": "PIONEX",
        "desc": "Pionex",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pionex"
      },
      {
        "name": "PulseX v2 (Pulsechain)",
        "value": "PULSEX2",
        "desc": "PulseX v2 (Pulsechain)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pulsex"
      },
      {
        "name": "Pyth",
        "value": "PYTH",
        "desc": "Pyth",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pyth"
      },
      {
        "name": "Ramses v2 (Arbitrum)",
        "value": "RAMSES2",
        "desc": "Ramses v2 (Arbitrum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "ramses2"
      },
      {
        "name": "Raydium (Solana)",
        "value": "RAYDIUM",
        "desc": "Raydium (Solana)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "raydium"
      },
      {
        "name": "Raydium CLMM (Solana)",
        "value": "RAYDIUMCLMM",
        "desc": "Raydium CLMM (Solana)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "raydiumclmm"
      },
      {
        "name": "Raydium CPMM (Solana)",
        "value": "RAYDIUMCPMM",
        "desc": "Raydium CPMM (Solana)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "raydiumcpmm"
      },
      {
        "name": "Shadow (Sonic)",
        "value": "SHADOW",
        "desc": "Shadow (Sonic)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "shadow"
      },
      {
        "name": "SpookySwap v2 (Fantom)",
        "value": "SPOOKYSWAP",
        "desc": "SpookySwap v2 (Fantom)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "spookyswap"
      },
      {
        "name": "STON.fi (TON)",
        "value": "STONFI",
        "desc": "STON.fi (TON)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "stonfi"
      },
      {
        "name": "STON.fi v2 (TON)",
        "value": "STONFI2",
        "desc": "STON.fi v2 (TON)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "stonfi"
      },
      {
        "name": "SunSwap v2 (TRON)",
        "value": "SUNSWAP2",
        "desc": "SunSwap v2 (TRON)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "sunswap"
      },
      {
        "name": "SunSwap v3 (TRON)",
        "value": "SUNSWAP3",
        "desc": "SunSwap v3 (TRON)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "sunswap"
      },
      {
        "name": "Wagmi (Sonic)",
        "value": "WAGMISONIC",
        "desc": "Wagmi (Sonic)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "wagmi"
      },
      {
        "name": "WhiteBIT",
        "value": "WHITEBIT",
        "desc": "WhiteBIT",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "whitebit"
      },
      {
        "name": "WOO X",
        "value": "WOONETWORK",
        "desc": "WOO X",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "woonetwork"
      },
      {
        "name": "Volmex",
        "value": "VOLMEX",
        "desc": "Volmex",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "volmex"
      },
      {
        "name": "zkSwap (zkSync)",
        "value": "ZKSWAP",
        "desc": "zkSwap (zkSync)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "zkswap"
      },
      {
        "name": "Zoomex",
        "value": "ZOOMEX",
        "desc": "Zoomex",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "zoomex"
      },
      {
        "name": "ADX",
        "value": "ADX",
        "desc": "ADX — Abu Dhabi Securities Exchange",
        "flag": "ae",
        "group": "Middle East / Africa",
        "country": "ae",
        "provider_id": ""
      },
      {
        "name": "ICEAD",
        "value": "ICEABUD",
        "desc": "ICEAD — ICE Futures Abu Dhabi",
        "flag": "ae",
        "group": "Middle East / Africa",
        "country": "ae",
        "provider_id": ""
      },
      {
        "name": "DFM",
        "value": "DFM",
        "desc": "DFM — Dubai Financial Market",
        "flag": "ae",
        "group": "Middle East / Africa",
        "country": "ae",
        "provider_id": ""
      },
      {
        "name": "NASDAQ",
        "value": "NASDAQDUBAI",
        "desc": "NASDAQ Dubai",
        "flag": "ae",
        "group": "Middle East / Africa",
        "country": "ae",
        "provider_id": ""
      },
      {
        "name": "AQUIS",
        "value": "AQUIS",
        "desc": "AQUIS — Aquis Stock Exchange",
        "flag": "uk",
        "group": "Europe",
        "country": "uk",
        "provider_id": ""
      },
      {
        "name": "LSE",
        "value": "LSE",
        "desc": "LSE — London Stock Exchange (UK Companies)",
        "flag": "uk",
        "group": "Europe",
        "country": "uk",
        "provider_id": ""
      },
      {
        "name": "LME",
        "value": "LME",
        "desc": "LME — London Metal Exchange",
        "flag": "uk",
        "group": "Europe",
        "country": "uk",
        "provider_id": ""
      },
      {
        "name": "LSIN",
        "value": "LSIN",
        "desc": "LSIN — London Stock Exchange (International Companies)",
        "flag": "uk",
        "group": "Europe",
        "country": "uk",
        "provider_id": ""
      },
      {
        "name": "Turquoise",
        "value": "TURQUOISE",
        "desc": "Turquoise",
        "flag": "uk",
        "group": "Europe",
        "country": "uk",
        "provider_id": ""
      },
      {
        "name": "FTSE",
        "value": "FTSE",
        "desc": "FTSE — Group Indices",
        "flag": "uk",
        "group": "Europe",
        "country": "uk",
        "provider_id": ""
      },
      {
        "name": "EUREX",
        "value": "EUREX",
        "desc": "EUREX — Eurex Exchange",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "provider_id": ""
      },
      {
        "name": "MGEX",
        "value": "MGEX",
        "desc": "MGEX — Futures",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "NASDAQ",
        "value": "NASDAQ",
        "desc": "NASDAQ — NASDAQ Stock Market",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "NYSE",
        "value": "NYSE",
        "desc": "NYSE — New York Stock Exchange",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "Arca",
        "value": "AMEX",
        "desc": "Arca — NYSE Arca",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "OTC",
        "value": "OTC",
        "desc": "OTC — OTC Markets",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "DJ",
        "value": "DJ",
        "desc": "DJ — Dow Jones Indices",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "SP",
        "value": "SP",
        "desc": "SP — S&P Indices",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "CBOE",
        "value": "CBOE",
        "desc": "CBOE — Chicago Board Options Exchange",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "MSTAR",
        "value": "MSTAR_INDICES",
        "desc": "MSTAR — CBOE MorningStar Indices",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "FINRA BTDS",
        "value": "FINRABTDS",
        "desc": "FINRA BTDS — FINRA Bond Trade Dissemination Service",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "OPRA",
        "value": "OPRA",
        "desc": "Options Price Reporting Authority",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "FINRA ATDS",
        "value": "FINRAATDS",
        "desc": "FINRA — FINRA Agency Debt Trade Dissemination Service",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "CBOE EU",
        "value": "CBOEEU",
        "desc": "CBOE EU — European Union Indices",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "provider_id": ""
      },
      {
        "name": "CBOT",
        "value": "CBOT",
        "desc": "CBOT — Chicago Board of Trade",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "CME GLOBEX",
        "value": "CME",
        "desc": "CME GLOBEX — Chicago Mercantile Exchange Globex",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "COMEX",
        "value": "COMEX",
        "desc": "COMEX — Commodity Exchange",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "NYMEX",
        "value": "NYMEX",
        "desc": "NYMEX — New York Mercantile Exchange",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "ICEUS",
        "value": "ICEUS",
        "desc": "ICEUS — ICE Futures U.S.",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "ICEUSCA",
        "value": "ICEUSCA",
        "desc": "ICEUSCA — ICE Futures U.S. Commodities - Canadian Grains",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "provider_id": ""
      },
      {
        "name": "CSE",
        "value": "CSE",
        "desc": "CSE — Canadian Securities Exchange",
        "flag": "canada",
        "group": "North America",
        "country": "ca",
        "provider_id": ""
      },
      {
        "name": "Cboe Canada",
        "value": "CBOE_CANADA",
        "desc": "Cboe Canada",
        "flag": "canada",
        "group": "North America",
        "country": "ca",
        "provider_id": ""
      },
      {
        "name": "TSX",
        "value": "TSX",
        "desc": "TSX — Toronto Stock Exchange",
        "flag": "canada",
        "group": "North America",
        "country": "ca",
        "provider_id": ""
      },
      {
        "name": "TSXV",
        "value": "TSXV",
        "desc": "TSXV — TSX Venture Exchange",
        "flag": "canada",
        "group": "North America",
        "country": "ca",
        "provider_id": ""
      },
      {
        "name": "TMX",
        "value": "TMX",
        "desc": "TMX — Montreal Exchange",
        "flag": "canada",
        "group": "North America",
        "country": "ca",
        "provider_id": ""
      },
      {
        "name": "RUS",
        "value": "RUS",
        "desc": "RUS",
        "flag": "russia",
        "group": "Europe",
        "country": "ru",
        "provider_id": ""
      },
      {
        "name": "MYX",
        "value": "MYX",
        "desc": "MYX — Bursa Malaysia Berhad",
        "flag": "malaysia",
        "group": "Asia / Pacific",
        "country": "my",
        "provider_id": ""
      },
      {
        "name": "FTSE",
        "value": "FTSEMYX",
        "desc": "FTSE — FTSE Indices",
        "flag": "malaysia",
        "group": "Asia / Pacific",
        "country": "my",
        "provider_id": ""
      },
      {
        "name": "HOSE",
        "value": "HOSE",
        "desc": "HOSE — Ho Chi Minh City Stock Exchange",
        "flag": "vietnam",
        "group": "Asia / Pacific",
        "country": "vn",
        "provider_id": ""
      },
      {
        "name": "HNX",
        "value": "HNX",
        "desc": "HNX — Hanoi Stock Exchange",
        "flag": "vietnam",
        "group": "Asia / Pacific",
        "country": "vn",
        "provider_id": ""
      },
      {
        "name": "HNX UPCoM",
        "value": "UPCOM",
        "desc": "HNX — Hanoi Stock Exchange (UPCoM)",
        "flag": "vietnam",
        "group": "Asia / Pacific",
        "country": "vn",
        "provider_id": ""
      },
      {
        "name": "CSE",
        "value": "CSELK",
        "desc": "CSE — Colombo Stock Exchange",
        "flag": "sri_lanka",
        "group": "Asia / Pacific",
        "country": "lk",
        "provider_id": ""
      },
      {
        "name": "Bitstamp",
        "value": "BITSTAMP",
        "desc": "Bitstamp",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitstamp"
      },
      {
        "name": "ActivTrades",
        "value": "ACTIVTRADES",
        "desc": "ActivTrades",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "activtrades"
      },
      {
        "name": "B2PRIME",
        "value": "B2PRIME",
        "desc": "B2PRIME",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "b2prime"
      },
      {
        "name": "BlackBull Markets",
        "value": "BLACKBULL",
        "desc": "BlackBull Markets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "blackbullmarkets"
      },
      {
        "name": "Blueberry",
        "value": "BLUEBERRY",
        "desc": "Blueberry",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "blueberry"
      },
      {
        "name": "CMC Markets",
        "value": "CMCMARKETS",
        "desc": "CMC Markets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "cmcmarkets"
      },
      {
        "name": "CXM",
        "value": "CXM",
        "desc": "CXM",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "cxm"
      },
      {
        "name": "FP Markets",
        "value": "FPMARKETS",
        "desc": "FP Markets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "fpmarkets"
      },
      {
        "name": "Fusion Markets",
        "value": "FUSIONMARKETS",
        "desc": "Fusion Markets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "fusionmarkets"
      },
      {
        "name": "GO Markets",
        "value": "GOMARKETS",
        "desc": "GO Markets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "gomarkets"
      },
      {
        "name": "IG",
        "value": "IG",
        "desc": "IG",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "ig"
      },
      {
        "name": "tastyfx",
        "value": "TASTYFX",
        "desc": "tastyfx",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "tastyfx"
      },
      {
        "name": "ThinkMarkets",
        "value": "THINKMARKETS",
        "desc": "ThinkMarkets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "thinkmarkets"
      },
      {
        "name": "Tickmill",
        "value": "TICKMILL",
        "desc": "Tickmill",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "tickmill"
      },
      {
        "name": "Trade Nation",
        "value": "TRADENATION",
        "desc": "Trade Nation",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "tradenation"
      },
      {
        "name": "Tradu",
        "value": "TRADU",
        "desc": "Tradu",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "tradu"
      },
      {
        "name": "Trive",
        "value": "TRIVE",
        "desc": "Trive",
        "flag": "Forex",
        "group": "Forex",
        "country": "",
        "provider_id": "trive"
      },
      {
        "name": "Vantage",
        "value": "VANTAGE",
        "desc": "Vantage",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "vantagefx"
      },
      {
        "name": "Velocity Trade",
        "value": "VELOCITY",
        "desc": "Velocity Trade",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "velocitytrade"
      },
      {
        "name": "FXCM",
        "value": "FX",
        "desc": "FXCM",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "fxcm"
      },
      {
        "name": "FXOpen",
        "value": "FXOPEN",
        "desc": "FXOpen",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "fxopen"
      },
      {
        "name": "FxPro",
        "value": "FXPRO",
        "desc": "FxPro",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "fxpro"
      },
      {
        "name": "Eightcap",
        "value": "EIGHTCAP",
        "desc": "Eightcap",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "eightcap"
      },
      {
        "name": "Errante",
        "value": "ERRANTE",
        "desc": "Errante",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "errante"
      },
      {
        "name": "EsaFX",
        "value": "ESAFX",
        "desc": "EsaFX",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "esafx"
      },
      {
        "name": "Osmanli FX",
        "value": "OSMANLIFX",
        "desc": "Osmanli FX",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "osmanlifx"
      },
      {
        "name": "BTC-e",
        "value": "BTCE",
        "desc": "BTC-E",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "Honeyswap v2 (Gnosis)",
        "value": "HONEYSWAP",
        "desc": "Honeyswap v2 (Gnosis)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "honeyswap"
      },
      {
        "name": "BSE",
        "value": "BSE",
        "desc": "BSE — Bombay Stock Exchange",
        "flag": "india",
        "group": "Asia / Pacific",
        "country": "in",
        "provider_id": ""
      },
      {
        "name": "MSE",
        "value": "MSEI",
        "desc": "MSE - Metropolitan Stock Exchange",
        "flag": "india",
        "group": "Asia / Pacific",
        "country": "in",
        "provider_id": ""
      },
      {
        "name": "NYMEX",
        "value": "NYMEX_MINI",
        "desc": "NYMEX — New York Mercantile Exchange",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "COMEX",
        "value": "COMEX_MINI",
        "desc": "COMEX — Commodity Exchange",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "ICEENDEX",
        "value": "ICEENDEX",
        "desc": "ICEENDEX — ICE Endex",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "provider_id": ""
      },
      {
        "name": "ICEEUR",
        "value": "ICEEURFIN",
        "desc": "ICEEUR — ICE Futures Europe Financials",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "provider_id": ""
      },
      {
        "name": "ICEEUR",
        "value": "ICEEURCOMM",
        "desc": "ICEEUR — ICE Futures Europe Commodities",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "provider_id": ""
      },
      {
        "name": "NSE",
        "value": "NSE",
        "desc": "NSE — National Stock Exchange of India",
        "flag": "india",
        "group": "Asia / Pacific",
        "country": "in",
        "provider_id": ""
      },
      {
        "name": "MCX",
        "value": "MCX",
        "desc": "MCX — Multi Commodity Exchange",
        "flag": "india",
        "group": "Asia / Pacific",
        "country": "in",
        "provider_id": ""
      },
      {
        "name": "NCDEX",
        "value": "NCDEX",
        "desc": "NCDEX — National Commodity & Derivatives Exchange",
        "flag": "india",
        "group": "Asia / Pacific",
        "country": "in",
        "provider_id": ""
      },
      {
        "name": "KCBT",
        "value": "KCBT",
        "desc": "KCBT Futures",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "CBOT",
        "value": "CBOT_MINI",
        "desc": "CBOT — Chicago Board of Trade",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "Kraken",
        "value": "KRAKEN",
        "desc": "Kraken",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "kraken"
      },
      {
        "name": "KuCoin",
        "value": "KUCOIN",
        "desc": "KuCoin",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "kucoin"
      },
      {
        "name": "LunarCrush",
        "value": "LUNARCRUSH",
        "desc": "LunarCrush",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "lunarcrush"
      },
      {
        "name": "Lynex (Linea)",
        "value": "LYNEX",
        "desc": "Lynex (Linea)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "lynex"
      },
      {
        "name": "Merchant Moe LB (Mantle)",
        "value": "MERCHANTMOELB",
        "desc": "Merchant Moe LB (Mantle)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "merchantmoelb"
      },
      {
        "name": "xExchange",
        "value": "XEXCHANGE",
        "desc": "xExchange",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "xexchange"
      },
      {
        "name": "XT.com",
        "value": "XTCOM",
        "desc": "XT.com",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "xtcom"
      },
      {
        "name": "CME",
        "value": "CME_MINI",
        "desc": "CME GLOBEX — Chicago Mercantile Exchange Globex",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "DJ",
        "value": "DJ",
        "desc": "DJ — Dow Jones Indexes",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "SP",
        "value": "SP",
        "desc": "SP — S&P Indexes",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "BTC China",
        "value": "BTCCHINA",
        "desc": "BTC China",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "Thruster v3 (Blast)",
        "value": "THRUSTER3",
        "desc": "Thruster v3 (Blast)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "thruster"
      },
      {
        "name": "ANX",
        "value": "ANX",
        "desc": "ANX",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "meXBT",
        "value": "MEXBT",
        "desc": "meXBT",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "Gemini",
        "value": "GEMINI",
        "desc": "Gemini",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "gemini"
      },
      {
        "name": "BitVC",
        "value": "BITVC",
        "desc": "BitVC",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "BitYes",
        "value": "BITYES",
        "desc": "BitYes",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "bitFlyer",
        "value": "BITFLYER",
        "desc": "bitFlyer",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitflyer"
      },
      {
        "name": "Bybit",
        "value": "BYBIT",
        "desc": "Bybit",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bybit"
      },
      {
        "name": "BYDFi",
        "value": "BIDFI",
        "desc": "BYDFi",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bydfi"
      },
      {
        "name": "BitMEX",
        "value": "BITMEX",
        "desc": "BitMEX",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitmex"
      },
      {
        "name": "Capital.com",
        "value": "CAPITALCOM",
        "desc": "Capital.com",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "capitalcom"
      },
      {
        "name": "CFI",
        "value": "CFI",
        "desc": "CFI",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "cfifinancial"
      },
      {
        "name": "CoinEx",
        "value": "COINEX",
        "desc": "CoinEx",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "coinex"
      },
      {
        "name": "CoinW",
        "value": "COINW",
        "desc": "CoinW",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "coinw"
      },
      {
        "name": "easyMarkets",
        "value": "EASYMARKETS",
        "desc": "easyMarkets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "easymarkets"
      },
      {
        "name": "FOREX.com",
        "value": "FOREXCOM",
        "desc": "FOREX.com",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "gain"
      },
      {
        "name": "ICE",
        "value": "FX_IDC",
        "desc": "ICE Data Services",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "ice"
      },
      {
        "name": "Interactive Brokers",
        "value": "IBKR",
        "desc": "Interactive Brokers",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "ibkr"
      },
      {
        "name": "iBroker",
        "value": "IBROKER",
        "desc": "iBroker",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "ibroker"
      },
      {
        "name": "IC Markets",
        "value": "ICMARKETS",
        "desc": "IC Markets",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "icmarkets"
      },
      {
        "name": "Bitfinex",
        "value": "BITFINEX",
        "desc": "Bitfinex",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitfinex"
      },
      {
        "name": "Mt.Gox",
        "value": "MTGOX",
        "desc": "Mt.Gox",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "hidden": true,
        "provider_id": "mtgox"
      },
      {
        "name": "Pharaoh (Avalanche)",
        "value": "PHARAOH",
        "desc": "Pharaoh (Avalanche)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pharaoh"
      },
      {
        "name": "Phemex",
        "value": "PHEMEX",
        "desc": "Phemex",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "phemex"
      },
      {
        "name": "Poloniex",
        "value": "POLONIEX",
        "desc": "Poloniex",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "poloniex"
      },
      {
        "name": "Pulsex (Pulsechain)",
        "value": "PULSEX",
        "desc": "Pulsex (Pulsechain)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "pulsex"
      },
      {
        "name": "QuickSwap v2 (Polygon)",
        "value": "QUICKSWAP",
        "desc": "QuickSwap v2 (Polygon)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "quickswap"
      },
      {
        "name": "QuickSwap v3 (Polygon zkEVM)",
        "value": "QUICKSWAP3POLYGONZKEVM",
        "desc": "QuickSwap v3 (Polygon zkEVM)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "quickswap3"
      },
      {
        "name": "QuickSwap v3 (Polygon)",
        "value": "QUICKSWAP3POLYGON",
        "desc": "QuickSwap v3 (Polygon)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "quickswap3"
      },
      {
        "name": "SushiSwap v2 (Ethereum)",
        "value": "SUSHISWAP",
        "desc": "SushiSwap v2 (Ethereum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "sushiswap"
      },
      {
        "name": "SushiSwap v2 (Polygon)",
        "value": "SUSHISWAPPOLYGON",
        "desc": "SushiSwap v2 (Polygon)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "sushiswap"
      },
      {
        "name": "SyncSwap (zkSync)",
        "value": "SYNCSWAP",
        "desc": "SyncSwap (zkSync)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "syncswap"
      },
      {
        "name": "SyncSwap v2 (zkSync)",
        "value": "SYNCSWAP2",
        "desc": "SyncSwap v2 (zkSync)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "syncswap2"
      },
      {
        "name": "Toobit",
        "value": "TOOBIT",
        "desc": "Toobit",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "toobit"
      },
      {
        "name": "Trader Joe v2 (Avalanche)",
        "value": "TRADERJOE",
        "desc": "Trader Joe v2 (Avalanche)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "traderjoe"
      },
      {
        "name": "Turbos Finance (Sui)",
        "value": "TURBOSFINANCE",
        "desc": "Turbos Finance (Sui)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "turbosfinance"
      },
      {
        "name": "Uniswap v2 (Ethereum)",
        "value": "UNISWAP",
        "desc": "Uniswap v2 (Ethereum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap"
      },
      {
        "name": "Uniswap v2 (Base)",
        "value": "UNISWAPBASE",
        "desc": "Uniswap v2 (Base)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap"
      },
      {
        "name": "Uniswap v2 (Unichain)",
        "value": "UNISWAPUNICHAIN",
        "desc": "Uniswap v2 (Unichain)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap"
      },
      {
        "name": "Uniswap v3 (Ethereum)",
        "value": "UNISWAP3ETH",
        "desc": "Uniswap v3 (Ethereum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap3"
      },
      {
        "name": "Uniswap v3 (Polygon)",
        "value": "UNISWAP3POLYGON",
        "desc": "Uniswap v3 (Polygon)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap3"
      },
      {
        "name": "Uniswap v3 (Arbitrum)",
        "value": "UNISWAP3ARBITRUM",
        "desc": "Uniswap v3 (Arbitrum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap3"
      },
      {
        "name": "Uniswap v3 (Optimism)",
        "value": "UNISWAP3OPTIMISM",
        "desc": "Uniswap v3 (Optimism)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap3"
      },
      {
        "name": "Uniswap v3 (BNB chain)",
        "value": "UNISWAP3BSC",
        "desc": "Uniswap v3 (BNB chain)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap3"
      },
      {
        "name": "Uniswap v3 (Base)",
        "value": "UNISWAP3BASE",
        "desc": "Uniswap v3 (Base)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap3"
      },
      {
        "name": "Uniswap v3 (Avalanche)",
        "value": "UNISWAP3AVALANCHE",
        "desc": "Uniswap v3 (Avalanche)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "uniswap3"
      },
      {
        "name": "UpBit",
        "value": "UPBIT",
        "desc": "UpBit",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "upbit"
      },
      {
        "name": "Antarctic",
        "value": "ANTARCTIC",
        "desc": "Antarctic",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "antarctic"
      },
      {
        "name": "BingX",
        "value": "BINGX",
        "desc": "BingX",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bingx"
      },
      {
        "name": "BTSE",
        "value": "BTSE",
        "desc": "BTSE",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "btse"
      },
      {
        "name": "Bittrex",
        "value": "BITTREX",
        "desc": "Bittrex",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bittrex"
      },
      {
        "name": "Bitvavo",
        "value": "BITVAVO",
        "desc": "Bitvavo",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitvavo"
      },
      {
        "name": "Bitunix",
        "value": "BITUNIX",
        "desc": "Bitunix",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitunix"
      },
      {
        "name": "Binance",
        "value": "BINANCE",
        "desc": "Binance",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "binance"
      },
      {
        "name": "Bitget",
        "value": "BITGET",
        "desc": "Bitget",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bitget"
      },
      {
        "name": "Binance.US",
        "value": "BINANCEUS",
        "desc": "Binance.US",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "binance"
      },
      {
        "name": "Delta Exchange",
        "value": "DELTA",
        "desc": "Delta Exchange",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "delta"
      },
      {
        "name": "Delta Exchange India",
        "value": "DELTAIN",
        "desc": "Delta Exchange India",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "deltain"
      },
      {
        "name": "BloFin",
        "value": "BLOFIN",
        "desc": "BloFin",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "blofin"
      },
      {
        "name": "Blackhole v3 (Avalanche)",
        "value": "BLACKHOLE3",
        "desc": "Blackhole v3 (Avalanche)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "blackhole3"
      },
      {
        "name": "Bluefin (Sui)",
        "value": "BLUEFIN",
        "desc": "Bluefin (Sui)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bluefin"
      },
      {
        "name": "Brave New Coin",
        "value": "BNC",
        "desc": "Brave New Coin",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "bnc"
      },
      {
        "name": "BTCC",
        "value": "BTCC",
        "desc": "BTCC",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "btcc"
      },
      {
        "name": "Katana (Ronin)",
        "value": "KATANA",
        "desc": "Katana (Ronin)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "katana"
      },
      {
        "name": "Katana v3 (Ronin)",
        "value": "KATANA3",
        "desc": "Katana v3 (Ronin)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "katana3"
      },
      {
        "name": "KCEX",
        "value": "KCEX",
        "desc": "KCEX",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "kcex"
      },
      {
        "name": "Camelot v2 (Arbitrum)",
        "value": "CAMELOT",
        "desc": "Camelot v2 (Arbitrum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "camelot2"
      },
      {
        "name": "Camelot v3 (Arbitrum)",
        "value": "CAMELOT3ARBITRUM",
        "desc": "Camelot v3 (Arbitrum)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "camelot3"
      },
      {
        "name": "CoinDesk Indices",
        "value": "COINDESK",
        "desc": "CoinDesk Indices",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "coindesk"
      },
      {
        "name": "Crypto.com",
        "value": "CRYPTOCOM",
        "desc": "Crypto.com",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "cryptocom"
      },
      {
        "name": "Velodrome (Optimism)",
        "value": "VELODROME",
        "desc": "Velodrome (Optimism)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "velodrome"
      },
      {
        "name": "Velodrome v2 (Optimism)",
        "value": "VELODROME2",
        "desc": "Velodrome v2 (Optimism)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "velodrome2"
      },
      {
        "name": "Velodrome SlipStream (Optimism)",
        "value": "VELODROMESLIPSTREAM",
        "desc": "Velodrome SlipStream (Optimism)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "velodromeslipstream"
      },
      {
        "name": "VVS Finance (Cronos)",
        "value": "VVSFINANCE",
        "desc": "VVS Finance (Cronos)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "vvsfinance"
      },
      {
        "name": "VVS v3 (Cronos)",
        "value": "VVS3",
        "desc": "VVS v3 (Cronos)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "vvs3"
      },
      {
        "name": "Webull Pay",
        "value": "WEBULLPAY",
        "desc": "Webull Pay",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "webullpay"
      },
      {
        "name": "Cetus (Sui)",
        "value": "CETUS",
        "desc": "Cetus (Sui)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "cetus"
      },
      {
        "name": "WEEX",
        "value": "WEEX",
        "desc": "WEEX",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "weex"
      },
      {
        "name": "MM Finance (Cronos)",
        "value": "MMFINANCE",
        "desc": "MM Finance (Cronos)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "mmfinance"
      },
      {
        "name": "Nile (Line)",
        "value": "NILE",
        "desc": "Nile (Line)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "nile"
      },
      {
        "name": "Agni (Mantle)",
        "value": "AGNI",
        "desc": "Agni (Mantle)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "agni"
      },
      {
        "name": "Aerodrome (Base)",
        "value": "AERODROME",
        "desc": "Aerodrome (Base)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "aerodrome"
      },
      {
        "name": "Aerodrome SlipStream (Base)",
        "value": "AERODROMESLIPSTREAM",
        "desc": "Aerodrome SlipStream (Base)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "aerodromeslipstream"
      },
      {
        "name": "BaseSwap (Base)",
        "value": "BASESWAP",
        "desc": "BaseSwap (Base)",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "baseswap"
      },
      {
        "name": "BYMA",
        "value": "BCBA",
        "desc": "BYMA — Argentine Stock Exchanges and Markets",
        "flag": "argentina",
        "group": "Mexico and South America",
        "country": "ar",
        "provider_id": ""
      },
      {
        "name": "ROFEX",
        "value": "MATBAROFEX",
        "desc": "ROFEX — MATBA ROFEX",
        "flag": "argentina",
        "group": "Mexico and South America",
        "country": "ar",
        "provider_id": ""
      },
      {
        "name": "B3",
        "value": "BMFBOVESPA",
        "desc": "B3 — Brasil Bolsa Balcao S.A.",
        "flag": "brasil",
        "group": "Mexico and South America",
        "country": "br",
        "provider_id": ""
      },
      {
        "name": "BMV",
        "value": "BMV",
        "desc": "BMV — Mexican Stock Exchange",
        "flag": "mexico",
        "group": "Mexico and South America",
        "country": "mx",
        "provider_id": ""
      },
      {
        "name": "BIVA",
        "value": "BIVA",
        "desc": "BIVA — Bolsa Institucional de Valores",
        "flag": "mexico",
        "group": "Mexico and South America",
        "country": "mx",
        "provider_id": ""
      },
      {
        "name": "BVL",
        "value": "BVL",
        "desc": "BVL — Bolsa de Valores de Lima",
        "flag": "peru",
        "group": "Mexico and South America",
        "country": "pe",
        "provider_id": ""
      },
      {
        "name": "SSE",
        "value": "BCS",
        "desc": "SSE — Santiago Stock Exchange",
        "flag": "chile",
        "group": "Mexico and South America",
        "country": "cl",
        "provider_id": ""
      },
      {
        "name": "BVC",
        "value": "BVC",
        "desc": "BVC — Bolsa de Valores de Colombia",
        "flag": "colombia",
        "group": "Mexico and South America",
        "country": "co",
        "provider_id": ""
      },
      {
        "name": "BVC",
        "value": "BVCV",
        "desc": "BVC — Caracas Stock Exchange",
        "flag": "venezuela",
        "group": "Mexico and South America",
        "country": "ve",
        "provider_id": ""
      },
      {
        "name": "NSE",
        "value": "NAG",
        "desc": "NSE — Nagoya Stock Exchange",
        "flag": "japan",
        "group": "Asia / Pacific",
        "country": "jp",
        "provider_id": ""
      },
      {
        "name": "TSE",
        "value": "TSE",
        "desc": "TSE — Tokyo Stock Exchange",
        "flag": "japan",
        "group": "Asia / Pacific",
        "country": "jp",
        "provider_id": ""
      },
      {
        "name": "TFEX",
        "value": "TFEX",
        "desc": "TFEX — Thailand Futures Exchange",
        "flag": "thailand",
        "group": "Asia / Pacific",
        "country": "th",
        "provider_id": ""
      },
      {
        "name": "TFX",
        "value": "TFX",
        "desc": "TFX — Tokyo Financial Exchange",
        "flag": "japan",
        "group": "Asia / Pacific",
        "country": "jp",
        "provider_id": ""
      },
      {
        "name": "TOCOM",
        "value": "TOCOM",
        "desc": "TOCOM — Tokyo Commodity Exchange",
        "flag": "japan",
        "group": "Asia / Pacific",
        "country": "jp",
        "provider_id": ""
      },
      {
        "name": "OSE",
        "value": "OSE",
        "desc": "OSE — Osaka Exchange",
        "flag": "japan",
        "group": "Asia / Pacific",
        "country": "jp",
        "provider_id": ""
      },
      {
        "name": "SGX",
        "value": "SGX",
        "desc": "SGX — Singapore Stock Exchange",
        "flag": "singapore",
        "group": "Asia / Pacific",
        "country": "sg",
        "provider_id": ""
      },
      {
        "name": "Abaxx",
        "value": "ABAXX",
        "desc": "Abaxx Exchange",
        "flag": "singapore",
        "group": "Asia / Pacific",
        "country": "sg",
        "provider_id": ""
      },
      {
        "name": "ICE Futures Singapore",
        "value": "ICESG",
        "desc": "ICE Futures Singapore",
        "flag": "singapore",
        "group": "Asia / Pacific",
        "country": "sg",
        "provider_id": ""
      },
      {
        "name": "FTSE ST",
        "value": "FTSEST",
        "desc": "FTSE ST Index Series",
        "flag": "singapore",
        "group": "Asia / Pacific",
        "country": "sg",
        "provider_id": ""
      },
      {
        "name": "SSE",
        "value": "SAPSE",
        "desc": "SSE — Sapporo Securities Exchange",
        "flag": "japan",
        "group": "Asia / Pacific",
        "country": "jp",
        "provider_id": ""
      },
      {
        "name": "FSE",
        "value": "FSE",
        "desc": "FSE — Fukuoka Stock Exchange",
        "flag": "japan",
        "group": "Asia / Pacific",
        "country": "jp",
        "provider_id": ""
      },
      {
        "name": "TPEx",
        "value": "TPEX",
        "desc": "TPEx — Taipei Exchange",
        "flag": "taiwan",
        "group": "Asia / Pacific",
        "country": "tw",
        "provider_id": ""
      },
      {
        "name": "TAIFEX",
        "value": "TAIFEX",
        "desc": "TAIFEX — Taiwan Futures Exchange",
        "flag": "taiwan",
        "group": "Asia / Pacific",
        "country": "tw",
        "provider_id": ""
      },
      {
        "name": "TWSE",
        "value": "TWSE",
        "desc": "TWSE — Taiwan Stock Exchange",
        "flag": "taiwan",
        "group": "Asia / Pacific",
        "country": "tw",
        "provider_id": ""
      },
      {
        "name": "SET",
        "value": "SET",
        "desc": "SET — Stock Exchange of Thailand",
        "flag": "thailand",
        "group": "Asia / Pacific",
        "country": "th",
        "provider_id": ""
      },
      {
        "name": "KRX",
        "value": "KRX",
        "desc": "KRX — Korea Stock Exchange",
        "flag": "south_korea",
        "group": "Asia / Pacific",
        "country": "kr",
        "provider_id": ""
      },
      {
        "name": "BHB",
        "value": "BAHRAIN",
        "desc": "BHB — Bahrain Stock Exchange",
        "flag": "bahrain",
        "group": "Middle East / Africa",
        "country": "bh",
        "provider_id": ""
      },
      {
        "name": "KSE",
        "value": "KSE",
        "desc": "KSE — Kuwait Stock Exchange",
        "flag": "kuwait",
        "group": "Middle East / Africa",
        "country": "kw",
        "provider_id": ""
      },
      {
        "name": "CSE",
        "value": "CSECY",
        "desc": "CSE — Cyprus Stock Exchange",
        "flag": "cyprus",
        "group": "Europe",
        "country": "cy",
        "provider_id": ""
      },
      {
        "name": "BVMT",
        "value": "BVMT",
        "desc": "BVMT — Tunis Stock Exchange",
        "flag": "tunisia",
        "group": "Middle East / Africa",
        "country": "tn",
        "provider_id": ""
      },
      {
        "name": "ATHEX",
        "value": "ATHEX",
        "desc": "ATHEX — Athens Stock Exchange",
        "flag": "greece",
        "group": "Europe",
        "country": "gr",
        "provider_id": ""
      },
      {
        "name": "BELEX",
        "value": "BELEX",
        "desc": "BELEX — Belgrade Stock Exchange",
        "flag": "serbia",
        "group": "Europe",
        "country": "rs",
        "provider_id": ""
      },
      {
        "name": "EGX",
        "value": "EGX",
        "desc": "EGX — Egyptian Exchange",
        "flag": "egypt",
        "group": "Middle East / Africa",
        "country": "eg",
        "provider_id": ""
      },
      {
        "name": "Tadawul",
        "value": "TADAWUL",
        "desc": "Tadawul — Saudi Exchange",
        "flag": "saudi_arabia",
        "group": "Middle East / Africa",
        "country": "sa",
        "provider_id": ""
      },
      {
        "name": "CSE",
        "value": "CSEMA",
        "desc": "CSE — Casablanca Stock Exchange",
        "flag": "morocco",
        "group": "Middle East / Africa",
        "country": "ma",
        "provider_id": ""
      },
      {
        "name": "IDX",
        "value": "IDX",
        "desc": "IDX — Indonesia Stock Exchange",
        "flag": "indonesia",
        "group": "Asia / Pacific",
        "country": "id",
        "provider_id": ""
      },
      {
        "name": "HSI",
        "value": "HSI",
        "desc": "HSI — Hang Seng Indices",
        "flag": "hong_kong",
        "group": "Asia / Pacific",
        "country": "hk",
        "provider_id": ""
      },
      {
        "name": "QSE",
        "value": "QSE",
        "desc": "QSE — Qatar Stock Exchange",
        "flag": "qatar",
        "group": "Middle East / Africa",
        "country": "qa",
        "provider_id": ""
      },
      {
        "name": "OANDA",
        "value": "OANDA",
        "desc": "OANDA",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "oanda"
      },
      {
        "name": "Opofinance",
        "value": "OPOFINANCE",
        "desc": "Opofinance",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "opofinance"
      },
      {
        "name": "Saxo",
        "value": "SAXO",
        "desc": "Saxo",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "saxobank"
      },
      {
        "name": "Pepperstone",
        "value": "PEPPERSTONE",
        "desc": "Pepperstone",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "pepperstone"
      },
      {
        "name": "Phillip Nova",
        "value": "PHILLIPNOVA",
        "desc": "Phillip Nova",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "phillipnova"
      },
      {
        "name": "Purple Trading",
        "value": "PURPLETRADING",
        "desc": "Purple Trading",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "purpletrading"
      },
      {
        "name": "Skilling",
        "value": "SKILLING",
        "desc": "Skilling",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "skilling"
      },
      {
        "name": "Spreadex",
        "value": "SPREADEX",
        "desc": "Spreadex",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "spreadex"
      },
      {
        "name": "Swissquote",
        "value": "SWISSQUOTE",
        "desc": "Swissquote",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "swissquote"
      },
      {
        "name": "GBE brokers",
        "value": "GBEBROKERS",
        "desc": "GBE brokers",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "gbebrokers"
      },
      {
        "name": "Euronext",
        "value": "EURONEXT",
        "desc": "Euronext — Euronext NV",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "provider_id": ""
      },
      {
        "name": "EURONEXTAMS",
        "value": "EURONEXTAMS",
        "desc": "Euronext — Euronext Amsterdam",
        "flag": "netherlands",
        "group": "Europe",
        "country": "nl",
        "provider_id": ""
      },
      {
        "name": "EURONEXTBRU",
        "value": "EURONEXTBRU",
        "desc": "Euronext — Euronext Brussels",
        "flag": "belgium",
        "group": "Europe",
        "country": "be",
        "provider_id": ""
      },
      {
        "name": "EURONEXTDUB",
        "value": "EURONEXTDUB",
        "desc": "Euronext — Euronext Dublin",
        "flag": "ireland",
        "group": "Europe",
        "country": "ie",
        "provider_id": ""
      },
      {
        "name": "EURONEXTLIS",
        "value": "EURONEXTLIS",
        "desc": "Euronext — Euronext Lisbon",
        "flag": "portugal",
        "group": "Europe",
        "country": "pt",
        "provider_id": ""
      },
      {
        "name": "EURONEXTPAR",
        "value": "EURONEXTPAR",
        "desc": "Euronext — Euronext Paris",
        "flag": "france",
        "group": "Europe",
        "country": "fr",
        "provider_id": ""
      },
      {
        "name": "EURONEXTOSE",
        "value": "OSL",
        "desc": "Euronext — Euronext Oslo",
        "flag": "norway",
        "group": "Europe",
        "country": "no",
        "provider_id": ""
      },
      {
        "name": "EUROTLX",
        "value": "EUROTLX",
        "desc": "Euronext — EuroTLX",
        "flag": "italy",
        "group": "Europe",
        "country": "it",
        "provider_id": ""
      },
      {
        "name": "OMX",
        "value": "OMX",
        "desc": "OMX — Nasdaq OMX Group",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "provider_id": ""
      },
      {
        "name": "FWB",
        "value": "FWB",
        "desc": "FWB — Frankfurt Stock Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "FRA",
        "value": "FRA",
        "desc": "FRA — Frankfurt Stock Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "LS",
        "value": "LS",
        "desc": "Lang & Schwarz TradeCenter AG & Co. KG",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "LSX",
        "value": "LSX",
        "desc": "Lang & Schwarz TradeCenter AG & Co. KG",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "SWB",
        "value": "SWB",
        "desc": "SWB — Stuttgart Stock Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "XETR",
        "value": "XETR",
        "desc": "XETR — Xetra",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "BME",
        "value": "BME",
        "desc": "BME — Bolsa de Madrid",
        "flag": "spain",
        "group": "Europe",
        "country": "es",
        "provider_id": ""
      },
      {
        "name": "BSSE",
        "value": "BSSE",
        "desc": "BSSE — Bratislava Stock Exchange",
        "flag": "slovakia",
        "group": "Europe",
        "country": "sk",
        "provider_id": ""
      },
      {
        "name": "BVB",
        "value": "BVB",
        "desc": "BVB — Bucharest Stock Exchange",
        "flag": "romania",
        "group": "Europe",
        "country": "ro",
        "provider_id": ""
      },
      {
        "name": "BET",
        "value": "BET",
        "desc": "BET — Budapest Stock Exchange",
        "flag": "hungary",
        "group": "Europe",
        "country": "hu",
        "provider_id": ""
      },
      {
        "name": "GPW",
        "value": "GPW",
        "desc": "GPW — Warsaw Stock Exchange",
        "flag": "poland",
        "group": "Europe",
        "country": "pl",
        "provider_id": ""
      },
      {
        "name": "GPW — NewConnect",
        "value": "NEWCONNECT",
        "desc": " GPW — NewConnect",
        "flag": "poland",
        "group": "Europe",
        "country": "pl",
        "provider_id": ""
      },
      {
        "name": "LUXSE",
        "value": "LUXSE",
        "desc": "LuxSE — Luxembourg Stock Exchange",
        "flag": "luxembourg",
        "group": "Europe",
        "country": "lu",
        "provider_id": ""
      },
      {
        "name": "MIL",
        "value": "MIL",
        "desc": "MIL — Milan Stock Exchange",
        "flag": "italy",
        "group": "Europe",
        "country": "it",
        "provider_id": ""
      },
      {
        "name": "NGM",
        "value": "NGM",
        "desc": "NGM — Nordic Growth Market",
        "flag": "sweden",
        "group": "Europe",
        "country": "se",
        "provider_id": ""
      },
      {
        "name": "DUS",
        "value": "DUS",
        "desc": "DUS — Dusseldorf Stock Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "HAM",
        "value": "HAM",
        "desc": "HAM — Hamburg Stock Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "HAN",
        "value": "HAN",
        "desc": "HAN — Hannover Stock Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "MUN",
        "value": "MUN",
        "desc": "MUN — Munich Stock Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "TRADEGATE",
        "value": "TRADEGATE",
        "desc": "Tradegate Exchange",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": ""
      },
      {
        "name": "GETTEX",
        "value": "GETTEX",
        "desc": "Gettex - Gettex",
        "flag": "germany",
        "group": "Europe",
        "country": "de",
        "provider_id": "finanzen"
      },
      {
        "name": "MILSEDEX",
        "value": "MILSEDEX",
        "desc": "MILSEDEX — Milan Stock Exchange",
        "flag": "italy",
        "group": "Europe",
        "country": "it",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "IST",
        "value": "IST",
        "desc": "IST — Istanbul Stock Exchange",
        "flag": "turkey",
        "group": "Europe",
        "country": "tr",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "BIST",
        "value": "BIST",
        "desc": "BIST — Borsa Istanbul",
        "flag": "turkey",
        "group": "Europe",
        "country": "tr",
        "provider_id": ""
      },
      {
        "name": "TASE",
        "value": "TASE",
        "desc": "TASE — Tel Aviv Stock Exchange",
        "flag": "israel",
        "group": "Middle East / Africa",
        "country": "il",
        "provider_id": ""
      },
      {
        "name": "SIX",
        "value": "SIX",
        "desc": "SIX — SIX Swiss Exchange",
        "flag": "switzerland",
        "group": "Europe",
        "country": "ch",
        "provider_id": ""
      },
      {
        "name": "BX",
        "value": "BX",
        "desc": "BX — BX Swiss",
        "flag": "switzerland",
        "group": "Europe",
        "country": "ch",
        "provider_id": ""
      },
      {
        "name": "PSE",
        "value": "PSECZ",
        "desc": "PSE — Prague Stock Exchange",
        "flag": "czech",
        "group": "Europe",
        "country": "cz",
        "provider_id": ""
      },
      {
        "name": "ASX",
        "value": "ASX",
        "desc": "ASX — Australian Securities Exchange",
        "flag": "australia",
        "group": "Asia / Pacific",
        "country": "au",
        "provider_id": ""
      },
      {
        "name": "Cboe Australia",
        "value": "CHIXAU",
        "desc": "Cboe Australia",
        "flag": "australia",
        "group": "Asia / Pacific",
        "country": "au",
        "provider_id": ""
      },
      {
        "name": "WB",
        "value": "VIE",
        "desc": "WB - Vienna Stock Exchange",
        "flag": "austria",
        "group": "Europe",
        "country": "at",
        "provider_id": ""
      },
      {
        "name": "DSE",
        "value": "DSEBD",
        "desc": "DSE — Dhaka Stock Exchange",
        "flag": "bangladesh",
        "group": "Asia / Pacific",
        "country": "bd",
        "provider_id": ""
      },
      {
        "name": "NZX",
        "value": "NZX",
        "desc": "NZX — New Zealand Stock Exchange",
        "flag": "new_zealand",
        "group": "Asia / Pacific",
        "country": "nz",
        "provider_id": ""
      },
      {
        "name": "CFFEX",
        "value": "CFFEX",
        "desc": "CFFEX — China Financial Futures Exchange",
        "flag": "china",
        "group": "Asia / Pacific",
        "country": "cn",
        "provider_id": ""
      },
      {
        "name": "SSE",
        "value": "SSE",
        "desc": "SSE — Shanghai Stock Exchange",
        "flag": "china",
        "group": "Asia / Pacific",
        "country": "cn",
        "provider_id": ""
      },
      {
        "name": "SHFE",
        "value": "SHFE",
        "desc": "SHFE — Shanghai Futures Exchange",
        "flag": "china",
        "group": "Asia / Pacific",
        "country": "cn",
        "provider_id": ""
      },
      {
        "name": "SZSE",
        "value": "SZSE",
        "desc": "SZSE — Shenzhen Stock Exchange",
        "flag": "china",
        "group": "Asia / Pacific",
        "country": "cn",
        "provider_id": ""
      },
      {
        "name": "ZCE",
        "value": "ZCE",
        "desc": "ZCE — Zhengzhou Commodity Exchange",
        "flag": "china",
        "group": "Asia / Pacific",
        "country": "cn",
        "provider_id": ""
      },
      {
        "name": "HKEX",
        "value": "HKEX",
        "desc": "HKEX — Hong Kong Exchange",
        "flag": "hong_kong",
        "group": "Asia / Pacific",
        "country": "hk",
        "provider_id": ""
      },
      {
        "name": "PSE",
        "value": "PSE",
        "desc": "PSE — Philippine Stock Exchange",
        "flag": "philippines",
        "group": "Asia / Pacific",
        "country": "ph",
        "provider_id": ""
      },
      {
        "name": "PSX",
        "value": "PSX",
        "desc": "PSX — Pakistan Stock Exchange",
        "flag": "pakistan",
        "group": "Asia / Pacific",
        "country": "pk",
        "provider_id": ""
      },
      {
        "name": "NSE",
        "value": "NSENG",
        "desc": "NSE — Nigerian Stock Exchange",
        "flag": "nigeria",
        "group": "Middle East / Africa",
        "country": "ng",
        "provider_id": ""
      },
      {
        "name": "NSE",
        "value": "NSEKE",
        "desc": "NSE — Nairobi Securities Exchange",
        "flag": "kenya",
        "group": "Middle East / Africa",
        "country": "ke",
        "provider_id": ""
      },
      {
        "name": "JSE",
        "value": "JSE",
        "desc": "JSE — Johannesburg Stock Exchange",
        "flag": "south_africa",
        "group": "Middle East / Africa",
        "country": "za",
        "provider_id": ""
      },
      {
        "name": "JFX",
        "value": "JFX",
        "desc": "JFX",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "jfx"
      },
      {
        "name": "MATSUI",
        "value": "MATSUI",
        "desc": "MATSUI",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "matsui"
      },
      {
        "name": "Coinbase",
        "value": "COINBASE",
        "desc": "Coinbase",
        "flag": "bitcoin",
        "group": "Cryptocurrency",
        "country": "",
        "provider_id": "coinbase"
      },
      {
        "name": "City Index",
        "value": "CITYINDEX",
        "desc": "City Index",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "cityindex"
      },
      {
        "name": "USI",
        "value": "USI",
        "desc": "USI",
        "flag": "usa",
        "group": "North America",
        "country": "us",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "HEX",
        "value": "OMXHEX",
        "desc": "HEX — Nasdaq Helsinki",
        "flag": "finland",
        "group": "Europe",
        "country": "fi",
        "provider_id": ""
      },
      {
        "name": "ICEX",
        "value": "OMXICE",
        "desc": "ICEX — Nasdaq Iceland",
        "flag": "iceland",
        "group": "Europe",
        "country": "is",
        "provider_id": ""
      },
      {
        "name": "CSE",
        "value": "OMXCOP",
        "desc": "CSE — Nasdaq Copenhagen",
        "flag": "denmark",
        "group": "Europe",
        "country": "dk",
        "provider_id": ""
      },
      {
        "name": "STO",
        "value": "OMXSTO",
        "desc": "STO — Nasdaq Stockholm",
        "flag": "sweden",
        "group": "Europe",
        "country": "se",
        "provider_id": ""
      },
      {
        "name": "VSE",
        "value": "OMXVSE",
        "desc": "VSE — Nasdaq Vilnius",
        "flag": "lithuania",
        "group": "Europe",
        "country": "lt",
        "provider_id": ""
      },
      {
        "name": "TALSE",
        "value": "OMXTSE",
        "desc": "TALSE — Nasdaq Tallinn",
        "flag": "estonia",
        "group": "Europe",
        "country": "ee",
        "provider_id": ""
      },
      {
        "name": "OMXR",
        "value": "OMXRSE",
        "desc": "OMXR — Nasdaq Riga",
        "flag": "latvia",
        "group": "Europe",
        "country": "lv",
        "provider_id": ""
      },
      {
        "name": "OMXNORDIC",
        "value": "OMXNORDIC",
        "desc": "OMXNORDIC",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "OMXBALTIC",
        "value": "OMXBALTIC",
        "desc": "OMXBALTIC",
        "flag": "europe",
        "group": "Europe",
        "country": "eu",
        "hidden": true,
        "provider_id": ""
      },
      {
        "name": "FRED",
        "value": "FRED",
        "desc": "Federal Reserve Economic Data",
        "flag": "usa",
        "group": "Economy",
        "country": "",
        "provider_id": "fred2"
      },
      {
        "name": "ISM",
        "value": "ISM",
        "desc": "Institute for Supply Management",
        "flag": "usa",
        "group": "Economy",
        "country": "",
        "provider_id": "quandl_ism"
      },
      {
        "name": "FRBNY",
        "value": "FRBNY",
        "desc": "Federal Reserve Bank of New York",
        "flag": "usa",
        "group": "Economy",
        "country": "",
        "provider_id": "quandl_frbny"
      },
      {
        "name": "FRBP",
        "value": "FRBP",
        "desc": "Federal Reserve Bank of Philadelphia",
        "flag": "usa",
        "group": "Economy",
        "country": "",
        "provider_id": "quandl_frbp"
      },
      {
        "name": "Trading Economics",
        "value": "ECONOMICS",
        "desc": "World economic data",
        "flag": "usa",
        "group": "Economy",
        "country": "",
        "provider_id": "economics"
      },
      {
        "name": "WH SelfInvest",
        "value": "WHSELFINVEST",
        "desc": "WH SelfInvest",
        "flag": "forex",
        "group": "Forex",
        "country": "",
        "provider_id": "whselfinvest"
      }
    ]
  },
  "msg": "Success"
}
```
