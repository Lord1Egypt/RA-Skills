# Market Search

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Search Markets

`GET /api/search/market/{query}`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/search/market/AAPL?filter=stock' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "markets": [
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "cik_code": "0000320193",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "is_primary_listing": true,
        "typespecs": [
          "common"
        ],
        "id": "NASDAQ:AAPL",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "APPLE INC / US DOLLAR",
        "type": "stock",
        "exchange": "Pyth",
        "found_by_isin": false,
        "found_by_cusip": false,
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "provider_id": "pyth",
        "source_logoid": "provider/pyth",
        "source2": {
          "id": "PYTH",
          "name": "Pyth",
          "description": "Pyth"
        },
        "source_id": "PYTH",
        "typespecs": [
          "crypto",
          "oracle"
        ],
        "prefix": "PYTH",
        "id": "PYTH:AAPL",
        "fullExchange": "Pyth",
        "full_name": "PYTH:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc. Shs Cert Deposito Arg Repr 0.05 Shs",
        "type": "dr",
        "exchange": "BYMA",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "ARDEUT116183",
        "currency_code": "ARS",
        "currency-logoid": "country/AR",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BCBA",
        "source2": {
          "id": "BCBA",
          "name": "Buenos Aires Stock Exchange",
          "description": "Buenos Aires Stock Exchange"
        },
        "source_id": "BCBA",
        "country": "AR",
        "prefix": "BCBA",
        "id": "BCBA:AAPL",
        "fullExchange": "BYMA",
        "full_name": "BCBA:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc. Shs Canadian Depositary Receipt Repr Shs Reg S",
        "type": "dr",
        "exchange": "TSX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "03785Y100",
        "isin": "CA03785Y1007",
        "currency_code": "CAD",
        "currency-logoid": "country/CA",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/TSX",
        "source2": {
          "id": "TSX",
          "name": "Toronto Stock Exchange",
          "description": "Toronto Stock Exchange"
        },
        "source_id": "TSX",
        "country": "CA",
        "id": "TSX:AAPL",
        "fullExchange": "TSX",
        "full_name": "TSX:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "BMV",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "MXN",
        "currency-logoid": "country/MX",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BMV",
        "source2": {
          "id": "BMV",
          "name": "Mexican Stock Exchange",
          "description": "Mexican Stock Exchange"
        },
        "source_id": "BMV",
        "country": "MX",
        "typespecs": [
          "common"
        ],
        "id": "BMV:AAPL",
        "fullExchange": "BMV",
        "full_name": "BMV:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "BIVA",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "MXN",
        "currency-logoid": "country/MX",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "sixgroup",
        "source_logoid": "source/BIVA",
        "source2": {
          "id": "BIVA",
          "name": "Institutional Stock Exchange",
          "description": "Institutional Stock Exchange"
        },
        "source_id": "BIVA",
        "country": "MX",
        "typespecs": [
          "common"
        ],
        "id": "BIVA:AAPL",
        "fullExchange": "BIVA",
        "full_name": "BIVA:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "BCS",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BCS",
        "source2": {
          "id": "BCS",
          "name": "Santiago Stock Exchange",
          "description": "Santiago Stock Exchange"
        },
        "source_id": "BCS",
        "country": "CL",
        "typespecs": [
          "common"
        ],
        "id": "BCS:AAPL",
        "fullExchange": "BCS",
        "full_name": "BCS:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "SIX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "CHF",
        "currency-logoid": "country/CH",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/SIX",
        "source2": {
          "id": "SIX",
          "name": "SIX Swiss Exchange",
          "description": "SIX Swiss Exchange"
        },
        "source_id": "SIX",
        "country": "CH",
        "typespecs": [
          "common"
        ],
        "id": "SIX:AAPL",
        "fullExchange": "SIX",
        "full_name": "SIX:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc. Shs Canadian Depositary Receipt Repr Shs Reg S",
        "type": "dr",
        "exchange": "NEO",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "03785Y100",
        "isin": "CA03785Y1007",
        "currency_code": "CAD",
        "currency-logoid": "country/CA",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/NEO",
        "source2": {
          "id": "NEO",
          "name": "Cboe Canada",
          "description": "Cboe Canada"
        },
        "source_id": "NEO",
        "country": "CA",
        "id": "NEO:AAPL",
        "fullExchange": "NEO",
        "full_name": "NEO:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "BVL",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BVL",
        "source2": {
          "id": "BVL",
          "name": "Lima Stock Exchange",
          "description": "Lima Stock Exchange"
        },
        "source_id": "BVL",
        "country": "PE",
        "typespecs": [
          "common"
        ],
        "id": "BVL:AAPL",
        "fullExchange": "BVL",
        "full_name": "BVL:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "BOATS",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BOATS",
        "source2": {
          "id": "BOATS",
          "name": "Blue Ocean Alternative Trade System",
          "description": "Blue Ocean Alternative Trade System"
        },
        "source_id": "BOATS",
        "country": "US",
        "typespecs": [
          "common"
        ],
        "id": "BOATS:AAPL",
        "fullExchange": "BOATS",
        "full_name": "BOATS:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "BVC",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "COP",
        "currency-logoid": "country/CO",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BVC",
        "source2": {
          "id": "BVC",
          "name": "Colombia Securities Exchange",
          "description": "Colombia Securities Exchange"
        },
        "source_id": "BVC",
        "country": "CO",
        "typespecs": [
          "common"
        ],
        "id": "BVC:AAPL",
        "fullExchange": "BVC",
        "full_name": "BVC:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "GPW",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "PLN",
        "currency-logoid": "country/PL",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/GPW",
        "source2": {
          "id": "GPW",
          "name": "Warsaw Stock Exchange",
          "description": "Warsaw Stock Exchange"
        },
        "source_id": "GPW",
        "country": "PL",
        "typespecs": [
          "common"
        ],
        "id": "GPW:AAPL",
        "fullExchange": "GPW",
        "full_name": "GPW:AAPL"
      },
      {
        "symbol": "AAPL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "VIE",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/VIE",
        "source2": {
          "id": "VIE",
          "name": "Vienna Stock Exchange",
          "description": "Vienna Stock Exchange"
        },
        "source_id": "VIE",
        "country": "AT",
        "typespecs": [
          "common"
        ],
        "id": "VIE:AAPL",
        "fullExchange": "VIE",
        "full_name": "VIE:AAPL"
      },
      {
        "symbol": "AAPLD",
        "description": "Apple Inc. Shs Cert Deposito Arg Repr 0.05 Shs",
        "type": "dr",
        "exchange": "BYMA",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "ARDEUT116183",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BCBA",
        "source2": {
          "id": "BCBA",
          "name": "Buenos Aires Stock Exchange",
          "description": "Buenos Aires Stock Exchange"
        },
        "source_id": "BCBA",
        "country": "AR",
        "prefix": "BCBA",
        "id": "BCBA:AAPLD",
        "fullExchange": "BYMA",
        "full_name": "BCBA:AAPLD"
      },
      {
        "symbol": "AAPLB",
        "description": "Apple Inc. Shs Cert Deposito Arg Repr 0.05 Shs",
        "type": "dr",
        "exchange": "BYMA",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "ARDEUT116183",
        "currency_code": "ARS",
        "currency-logoid": "country/AR",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BCBA",
        "source2": {
          "id": "BCBA",
          "name": "Buenos Aires Stock Exchange",
          "description": "Buenos Aires Stock Exchange"
        },
        "source_id": "BCBA",
        "country": "AR",
        "prefix": "BCBA",
        "id": "BCBA:AAPLB",
        "fullExchange": "BYMA",
        "full_name": "BCBA:AAPLB"
      },
      {
        "symbol": "AAPLC",
        "description": "Apple Inc. Shs Cert Deposito Arg Repr 0.05 Shs",
        "type": "dr",
        "exchange": "BYMA",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "ARDEUT116183",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BCBA",
        "source2": {
          "id": "BCBA",
          "name": "Buenos Aires Stock Exchange",
          "description": "Buenos Aires Stock Exchange"
        },
        "source_id": "BCBA",
        "country": "AR",
        "prefix": "BCBA",
        "id": "BCBA:AAPLC",
        "fullExchange": "BYMA",
        "full_name": "BCBA:AAPLC"
      },
      {
        "symbol": "AAPLN",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "TURQUOISE",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/TURQUOISE",
        "source2": {
          "id": "TURQUOISE",
          "name": "Turquoise",
          "description": "Turquoise"
        },
        "source_id": "TURQUOISE",
        "country": "GB",
        "typespecs": [
          "common"
        ],
        "id": "TURQUOISE:AAPLN",
        "fullExchange": "TURQUOISE",
        "full_name": "TURQUOISE:AAPLN"
      },
      {
        "symbol": "AAPU",
        "description": "Direxion Daily AAPL Bull 2X ETF",
        "type": "fund",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "25461A874",
        "isin": "US25461A8743",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "direxion",
        "logo": {
          "style": "single",
          "logoid": "direxion"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "typespecs": [
          "etf"
        ],
        "id": "NASDAQ:AAPU",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPU"
      },
      {
        "symbol": "AAPL80",
        "description": "Apple Inc. Units Thailand Depository Receipt Repr 0.001 Sh",
        "type": "dr",
        "exchange": "SET",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "TH0150120408",
        "currency_code": "THB",
        "currency-logoid": "country/TH",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/SET",
        "source2": {
          "id": "SET",
          "name": "Stock Exchange of Thailand",
          "description": "Stock Exchange of Thailand"
        },
        "source_id": "SET",
        "country": "TH",
        "id": "SET:AAPL80",
        "fullExchange": "SET",
        "full_name": "SET:AAPL80"
      },
      {
        "symbol": "AAPL01",
        "description": "Apple Inc. Units Thailand Depositery Receipts Repr 0.01 Sh",
        "type": "dr",
        "exchange": "SET",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "TH0809121500",
        "currency_code": "THB",
        "currency-logoid": "country/TH",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/SET",
        "source2": {
          "id": "SET",
          "name": "Stock Exchange of Thailand",
          "description": "Stock Exchange of Thailand"
        },
        "source_id": "SET",
        "country": "TH",
        "id": "SET:AAPL01",
        "fullExchange": "SET",
        "full_name": "SET:AAPL01"
      },
      {
        "symbol": "AAPL19",
        "description": "Apple Inc. Units Thailand Depositery Receipts Repr 0.01 Sh",
        "type": "dr",
        "exchange": "SET",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "TH8483124708",
        "currency_code": "THB",
        "currency-logoid": "country/TH",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/SET",
        "source2": {
          "id": "SET",
          "name": "Stock Exchange of Thailand",
          "description": "Stock Exchange of Thailand"
        },
        "source_id": "SET",
        "country": "TH",
        "id": "SET:AAPL19",
        "fullExchange": "SET",
        "full_name": "SET:AAPL19"
      },
      {
        "symbol": "AAPL03",
        "description": "Apple Inc. Units Thailand Depositery Receipts Repr 0.01 Sh",
        "type": "dr",
        "exchange": "SET",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "TH0241121001",
        "currency_code": "THB",
        "currency-logoid": "country/TH",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/SET",
        "source2": {
          "id": "SET",
          "name": "Stock Exchange of Thailand",
          "description": "Stock Exchange of Thailand"
        },
        "source_id": "SET",
        "country": "TH",
        "id": "SET:AAPL03",
        "fullExchange": "SET",
        "full_name": "SET:AAPL03"
      },
      {
        "symbol": "AAPLCL",
        "description": "Apple Inc.",
        "type": "stock",
        "exchange": "BCS",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "037833100",
        "isin": "US0378331005",
        "currency_code": "CLP",
        "currency-logoid": "country/CL",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BCS",
        "source2": {
          "id": "BCS",
          "name": "Santiago Stock Exchange",
          "description": "Santiago Stock Exchange"
        },
        "source_id": "BCS",
        "country": "CL",
        "typespecs": [
          "common"
        ],
        "id": "BCS:AAPLCL",
        "fullExchange": "BCS",
        "full_name": "BCS:AAPLCL"
      },
      {
        "symbol": "AAPL34",
        "description": "Apple Inc. Shs Unsponsored Brazilian Depository Receipt Repr 0.05 Sh",
        "type": "dr",
        "exchange": "BMFBOVESPA",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "BRAAPLBDR004",
        "currency_code": "BRL",
        "currency-logoid": "country/BR",
        "logoid": "apple",
        "logo": {
          "style": "single",
          "logoid": "apple"
        },
        "provider_id": "ice",
        "source_logoid": "source/BMFBOVESPA",
        "source2": {
          "id": "BMFBOVESPA",
          "name": "B3",
          "description": "B3"
        },
        "source_id": "BMFBOVESPA",
        "country": "BR",
        "id": "BMFBOVESPA:AAPL34",
        "fullExchange": "BMFBOVESPA",
        "full_name": "BMFBOVESPA:AAPL34"
      },
      {
        "symbol": "AAPLWXX",
        "description": "JPMorgan Chase Financial Company LLC Dual Directional Buffer Note AAPLWXX",
        "type": "structured",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "48133VKW9",
        "isin": "US48133VKW99",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "params": [
          "eod"
        ],
        "id": "NASDAQ:AAPLWXX",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPLWXX"
      },
      {
        "symbol": "AAPLYXX",
        "description": "Barclays Bank PLC Point to Point Buffer Note AAPLYXX",
        "type": "structured",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "06749NUN0",
        "isin": "US06749NUN01",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "barclays",
        "logo": {
          "style": "single",
          "logoid": "barclays"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "params": [
          "eod"
        ],
        "id": "NASDAQ:AAPLYXX",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPLYXX"
      },
      {
        "symbol": "AAPLDXX",
        "description": "Barclays Bank PLC Capped Point to Point Fully Principally Protected Note AAPLDXX",
        "type": "structured",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "06749NV58",
        "isin": "US06749NV583",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "barclays",
        "logo": {
          "style": "single",
          "logoid": "barclays"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "params": [
          "eod"
        ],
        "id": "NASDAQ:AAPLDXX",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPLDXX"
      },
      {
        "symbol": "AAPLTXX",
        "description": "Bank of Montreal Capped Point to Point Fully Principally Protected Note AAPLTXX",
        "type": "structured",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "06374VRH1",
        "isin": "US06374VRH14",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "bank-of-montreal",
        "logo": {
          "style": "single",
          "logoid": "bank-of-montreal"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "params": [
          "eod"
        ],
        "id": "NASDAQ:AAPLTXX",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPLTXX"
      },
      {
        "symbol": "AAPLZXX",
        "description": "Citigroup Global Markets Holdings Inc. Issuer Callable Contingent Interest Barrier Note AAPLZXX",
        "type": "structured",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "17331CYT8",
        "isin": "US17331CYT88",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "citigroup",
        "logo": {
          "style": "single",
          "logoid": "citigroup"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "params": [
          "eod"
        ],
        "id": "NASDAQ:AAPLZXX",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPLZXX"
      },
      {
        "symbol": "AAPLIXX",
        "description": "Barclays Bank PLC Point to Point Worst Of Buffer Note AAPLIXX",
        "type": "structured",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "06749NZ70",
        "isin": "US06749NZ709",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "barclays",
        "logo": {
          "style": "single",
          "logoid": "barclays"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "params": [
          "eod"
        ],
        "id": "NASDAQ:AAPLIXX",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPLIXX"
      },
      {
        "symbol": "AAPLVXX",
        "description": "Citigroup Global Markets Holdings Inc. Capped Point to Point Worst Of Barrier Note AAPLVXX",
        "type": "structured",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "17331CEM5",
        "isin": "US17331CEM55",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "citigroup",
        "logo": {
          "style": "single",
          "logoid": "citigroup"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "params": [
          "eod"
        ],
        "id": "NASDAQ:AAPLVXX",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPLVXX"
      },
      {
        "symbol": "AAPW",
        "description": "Roundhill AAPL WeeklyPay ETF",
        "type": "fund",
        "exchange": "CBOE",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "77926X791",
        "isin": "US77926X7912",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "roundhmetave-aeoa",
        "logo": {
          "style": "single",
          "logoid": "roundhmetave-aeoa"
        },
        "provider_id": "ice",
        "source_logoid": "source/CBOE",
        "source2": {
          "id": "CBOE",
          "name": "Cboe",
          "description": "Cboe"
        },
        "source_id": "CBOE",
        "country": "US",
        "typespecs": [
          "etf"
        ],
        "id": "CBOE:AAPW",
        "fullExchange": "CBOE",
        "full_name": "CBOE:AAPW"
      },
      {
        "symbol": "AAPD",
        "description": "Direxion Daily AAPL Bear 1X ETF",
        "type": "fund",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "25461A304",
        "isin": "US25461A3041",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "direxion",
        "logo": {
          "style": "single",
          "logoid": "direxion"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "typespecs": [
          "etf"
        ],
        "id": "NASDAQ:AAPD",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPD"
      },
      {
        "symbol": "AAPB",
        "description": "GraniteShares 2x Long AAPL Daily ETF",
        "type": "fund",
        "exchange": "NASDAQ",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "38747R884",
        "isin": "US38747R8842",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "graniteshares",
        "logo": {
          "style": "single",
          "logoid": "graniteshares"
        },
        "provider_id": "ice",
        "source_logoid": "source/NASDAQ",
        "source2": {
          "id": "NASDAQ",
          "name": "Nasdaq Stock Market",
          "description": "Nasdaq Stock Market"
        },
        "source_id": "NASDAQ",
        "country": "US",
        "typespecs": [
          "etf"
        ],
        "id": "NASDAQ:AAPB",
        "fullExchange": "NASDAQ",
        "full_name": "NASDAQ:AAPB"
      },
      {
        "symbol": "AAPY",
        "description": "Kurv Yield Premium Strategy Apple (AAPL) ETF",
        "type": "fund",
        "exchange": "CBOE",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "500948500",
        "isin": "US5009485005",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "neos-etf-trust-kurv-yield-premium-strategy-microsoft-msft-etf",
        "logo": {
          "style": "single",
          "logoid": "neos-etf-trust-kurv-yield-premium-strategy-microsoft-msft-etf"
        },
        "provider_id": "ice",
        "source_logoid": "source/CBOE",
        "source2": {
          "id": "CBOE",
          "name": "Cboe",
          "description": "Cboe"
        },
        "source_id": "CBOE",
        "country": "US",
        "typespecs": [
          "etf"
        ],
        "id": "CBOE:AAPY",
        "fullExchange": "CBOE",
        "full_name": "CBOE:AAPY"
      },
      {
        "symbol": "APLY",
        "description": "YieldMax AAPL Option Income Strategy ETF",
        "type": "fund",
        "exchange": "NYSE",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "88634T857",
        "isin": "US88634T8577",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "yieldmax-tsla-option-income-strategy-etf",
        "logo": {
          "style": "single",
          "logoid": "yieldmax-tsla-option-income-strategy-etf"
        },
        "provider_id": "ice",
        "source_logoid": "source/AMEX",
        "source2": {
          "id": "AMEX",
          "name": "NYSE American",
          "description": "NYSE American"
        },
        "source_id": "AMEX",
        "country": "US",
        "typespecs": [
          "etf"
        ],
        "prefix": "AMEX",
        "id": "AMEX:APLY",
        "fullExchange": "NYSE Arca",
        "full_name": "AMEX:APLY"
      },
      {
        "symbol": "AAPI",
        "description": "IncomeShares Apple (AAPL) Options ETP",
        "type": "fund",
        "exchange": "LSE",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "XS2901884663",
        "currency_code": "GBX",
        "currency-logoid": "country/GB",
        "logoid": "leverage-shares",
        "logo": {
          "style": "single",
          "logoid": "leverage-shares"
        },
        "provider_id": "ice",
        "source_logoid": "source/LSE",
        "source2": {
          "id": "LSE",
          "name": "London Stock Exchange",
          "description": "London Stock Exchange"
        },
        "source_id": "LSE",
        "country": "GB",
        "typespecs": [
          "etf"
        ],
        "id": "LSE:AAPI",
        "fullExchange": "LSE",
        "full_name": "LSE:AAPI"
      },
      {
        "symbol": "F34588",
        "description": "VON F LEV LG X 3 VONT 3X L AAPL V 180627",
        "type": "structured",
        "exchange": "MILSEDEX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "DE000VU329Q9",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "provider_id": "ice",
        "source_logoid": "source/MILSEDEX",
        "source2": {
          "id": "MILSEDEX",
          "name": "Euronext Milan",
          "description": "Euronext Milan"
        },
        "source_id": "MILSEDEX",
        "country": "IT",
        "id": "MILSEDEX:F34588",
        "fullExchange": "MILSEDEX",
        "full_name": "MILSEDEX:F34588"
      },
      {
        "symbol": "AAPY",
        "description": "IncomeShares Apple (AAPL) Options ETP",
        "type": "fund",
        "exchange": "LSE",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "XS2901884663",
        "currency_code": "USD",
        "currency-logoid": "country/US",
        "logoid": "leverage-shares",
        "logo": {
          "style": "single",
          "logoid": "leverage-shares"
        },
        "provider_id": "ice",
        "source_logoid": "source/LSE",
        "source2": {
          "id": "LSE",
          "name": "London Stock Exchange",
          "description": "London Stock Exchange"
        },
        "source_id": "LSE",
        "country": "GB",
        "typespecs": [
          "etf"
        ],
        "id": "LSE:AAPY",
        "fullExchange": "LSE",
        "full_name": "LSE:AAPY"
      },
      {
        "symbol": "F34608",
        "description": "VON F LEV SH X -3 VONT 3X S AAPL 180627",
        "type": "structured",
        "exchange": "MILSEDEX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "DE000VU32939",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "provider_id": "ice",
        "source_logoid": "source/MILSEDEX",
        "source2": {
          "id": "MILSEDEX",
          "name": "Euronext Milan",
          "description": "Euronext Milan"
        },
        "source_id": "MILSEDEX",
        "country": "IT",
        "id": "MILSEDEX:F34608",
        "fullExchange": "MILSEDEX",
        "full_name": "MILSEDEX:F34608"
      },
      {
        "symbol": "F34630",
        "description": "VON F LEV LG X 5 VONT 5X L AAPL V 180627",
        "type": "structured",
        "exchange": "MILSEDEX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "DE000VU33AR4",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "provider_id": "ice",
        "source_logoid": "source/MILSEDEX",
        "source2": {
          "id": "MILSEDEX",
          "name": "Euronext Milan",
          "description": "Euronext Milan"
        },
        "source_id": "MILSEDEX",
        "country": "IT",
        "id": "MILSEDEX:F34630",
        "fullExchange": "MILSEDEX",
        "full_name": "MILSEDEX:F34630"
      },
      {
        "symbol": "F55447",
        "description": "VON F LEV SH X -5 VONT 5X S AAPL 180627",
        "type": "structured",
        "exchange": "MILSEDEX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "DE000VC5LYF5",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "provider_id": "ice",
        "source_logoid": "source/MILSEDEX",
        "source2": {
          "id": "MILSEDEX",
          "name": "Euronext Milan",
          "description": "Euronext Milan"
        },
        "source_id": "MILSEDEX",
        "country": "IT",
        "id": "MILSEDEX:F55447",
        "fullExchange": "MILSEDEX",
        "full_name": "MILSEDEX:F55447"
      },
      {
        "symbol": "F80659",
        "description": "VON EXP AAPL/META/NVDA/MSFT 60 081127",
        "type": "structured",
        "exchange": "MILSEDEX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "DE000VH8GP52",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "provider_id": "ice",
        "source_logoid": "source/MILSEDEX",
        "source2": {
          "id": "MILSEDEX",
          "name": "Euronext Milan",
          "description": "Euronext Milan"
        },
        "source_id": "MILSEDEX",
        "country": "IT",
        "id": "MILSEDEX:F80659",
        "fullExchange": "MILSEDEX",
        "full_name": "MILSEDEX:F80659"
      },
      {
        "symbol": "I76744",
        "description": "MRX EXP AAPL/AMZN/GOOG/NVDA 50 100231",
        "type": "structured",
        "exchange": "EUROTLX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "IT0006767443",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "provider_id": "ice",
        "source_logoid": "source/EUROTLX",
        "source2": {
          "id": "EUROTLX",
          "name": "BorsaItaliana",
          "description": "BorsaItaliana"
        },
        "source_id": "EUROTLX",
        "country": "IT",
        "typespecs": [
          "etn"
        ],
        "id": "EUROTLX:I76744",
        "fullExchange": "EUROTLX",
        "full_name": "EUROTLX:I76744"
      },
      {
        "symbol": "F92350",
        "description": "VON EXP AAPL/GOOG/META/MSFT 55 021028",
        "type": "structured",
        "exchange": "MILSEDEX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "DE000VY0G7W3",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "provider_id": "ice",
        "source_logoid": "source/MILSEDEX",
        "source2": {
          "id": "MILSEDEX",
          "name": "Euronext Milan",
          "description": "Euronext Milan"
        },
        "source_id": "MILSEDEX",
        "country": "IT",
        "id": "MILSEDEX:F92350",
        "fullExchange": "MILSEDEX",
        "full_name": "MILSEDEX:F92350"
      },
      {
        "symbol": "AAPU",
        "description": "Savvylong 2X AAPL ETF",
        "type": "fund",
        "exchange": "TSX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "cusip": "54315B771",
        "isin": "CA54315B7714",
        "currency_code": "CAD",
        "currency-logoid": "country/CA",
        "logoid": "longpoint-etf-savvyshort-geared-crude-oil-etf",
        "logo": {
          "style": "single",
          "logoid": "longpoint-etf-savvyshort-geared-crude-oil-etf"
        },
        "provider_id": "ice",
        "source_logoid": "source/TSX",
        "source2": {
          "id": "TSX",
          "name": "Toronto Stock Exchange",
          "description": "Toronto Stock Exchange"
        },
        "source_id": "TSX",
        "country": "CA",
        "typespecs": [
          "etf"
        ],
        "id": "TSX:AAPU",
        "fullExchange": "TSX",
        "full_name": "TSX:AAPU"
      },
      {
        "symbol": "AAPY",
        "description": "IncomeShares Apple (AAPL) Options ETP",
        "type": "fund",
        "exchange": "GETTEX",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "XS2901884663",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "logoid": "leverage-shares",
        "logo": {
          "style": "single",
          "logoid": "leverage-shares"
        },
        "provider_id": "sixgroup",
        "source_logoid": "source/GETTEX",
        "source2": {
          "id": "GETTEX",
          "name": "Gettex",
          "description": "Gettex"
        },
        "source_id": "GETTEX",
        "country": "DE",
        "typespecs": [
          "etf"
        ],
        "id": "GETTEX:AAPY",
        "fullExchange": "GETTEX",
        "full_name": "GETTEX:AAPY"
      },
      {
        "symbol": "AAPY",
        "description": "IncomeShares Apple (AAPL) Options ETP",
        "type": "fund",
        "exchange": "XETR",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "XS2901884663",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "logoid": "leverage-shares",
        "logo": {
          "style": "single",
          "logoid": "leverage-shares"
        },
        "provider_id": "ice",
        "source_logoid": "source/XETR",
        "source2": {
          "id": "XETR",
          "name": "Deutsche Borse Xetra",
          "description": "Deutsche Borse Xetra"
        },
        "source_id": "XETR",
        "country": "DE",
        "typespecs": [
          "etf"
        ],
        "id": "XETR:AAPY",
        "fullExchange": "XETR",
        "full_name": "XETR:AAPY"
      },
      {
        "symbol": "AAPY",
        "description": "IncomeShares Apple (AAPL) Options ETP",
        "type": "fund",
        "exchange": "FWB",
        "found_by_isin": false,
        "found_by_cusip": false,
        "isin": "XS2901884663",
        "currency_code": "EUR",
        "currency-logoid": "country/EU",
        "logoid": "leverage-shares",
        "logo": {
          "style": "single",
          "logoid": "leverage-shares"
        },
        "provider_id": "ice",
        "source_logoid": "source/FWB",
        "source2": {
          "id": "FWB",
          "name": "Frankfurt Stock Exchange",
          "description": "Frankfurt Stock Exchange"
        },
        "source_id": "FWB",
        "country": "DE",
        "typespecs": [
          "etf"
        ],
        "id": "FWB:AAPY",
        "fullExchange": "FWB",
        "full_name": "FWB:AAPY"
      }
    ],
    "count": 50
  },
  "msg": "Success"
}
```
