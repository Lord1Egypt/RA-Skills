# World Economy

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Get World Economy Indicator Rankings

`GET /api/world-economy/indicators/{indicator}`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/world-economy/indicators/full-year-gdp-growth?region=g20' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "indicator": "full-year-gdp-growth",
    "region": "g20",
    "total": 20,
    "rows": [
      {
        "symbol": "INFYGDPG",
        "full_symbol": "ECONOMICS:INFYGDPG",
        "name": "India Full Year GDP Growth",
        "country_code": "IN",
        "logoid": "country/IN",
        "latest": 7.6,
        "previous": 7.1,
        "observation": "2026",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "IDFYGDPG",
        "full_symbol": "ECONOMICS:IDFYGDPG",
        "name": "Indonesia Full Year GDP Growth",
        "country_code": "ID",
        "logoid": "country/ID",
        "latest": 5.11,
        "previous": 5.03,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "CNFYGDPG",
        "full_symbol": "ECONOMICS:CNFYGDPG",
        "name": "China Full Year GDP Growth",
        "country_code": "CN",
        "logoid": "country/CN",
        "latest": 5,
        "previous": 5,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "SAFYGDPG",
        "full_symbol": "ECONOMICS:SAFYGDPG",
        "name": "Saudi Arabia Full Year GDP Growth",
        "country_code": "SA",
        "logoid": "country/SA",
        "latest": 4.5,
        "previous": 2.7,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "ARFYGDPG",
        "full_symbol": "ECONOMICS:ARFYGDPG",
        "name": "Argentina Full Year GDP Growth",
        "country_code": "AR",
        "logoid": "country/AR",
        "latest": 4.4,
        "previous": -1.7,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "TRFYGDPG",
        "full_symbol": "ECONOMICS:TRFYGDPG",
        "name": "Turkey Full Year GDP Growth",
        "country_code": "TR",
        "logoid": "country/TR",
        "latest": 3.6,
        "previous": 3.3,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "AUFYGDPG",
        "full_symbol": "ECONOMICS:AUFYGDPG",
        "name": "Australia Full Year GDP Growth",
        "country_code": "AU",
        "logoid": "country/AU",
        "latest": 2.6,
        "previous": 1.3,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "BRFYGDPG",
        "full_symbol": "ECONOMICS:BRFYGDPG",
        "name": "Brazil Full Year GDP Growth",
        "country_code": "BR",
        "logoid": "country/BR",
        "latest": 2.3,
        "previous": 3.4,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "USFYGDPG",
        "full_symbol": "ECONOMICS:USFYGDPG",
        "name": "United States Full Year GDP Growth",
        "country_code": "US",
        "logoid": "country/US",
        "latest": 2.1,
        "previous": 2.8,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "KRFYGDPG",
        "full_symbol": "ECONOMICS:KRFYGDPG",
        "name": "South Korea Full Year GDP Growth",
        "country_code": "KR",
        "logoid": "country/KR",
        "latest": 2,
        "previous": 1.4,
        "observation": "2024",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "CAFYGDPG",
        "full_symbol": "ECONOMICS:CAFYGDPG",
        "name": "Canada Full Year GDP Growth",
        "country_code": "CA",
        "logoid": "country/CA",
        "latest": 1.74,
        "previous": 2.05,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "GBFYGDPG",
        "full_symbol": "ECONOMICS:GBFYGDPG",
        "name": "United Kingdom Full Year GDP Growth",
        "country_code": "GB",
        "logoid": "country/GB",
        "latest": 1.4,
        "previous": 1.1,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "EUFYGDPG",
        "full_symbol": "ECONOMICS:EUFYGDPG",
        "name": "Euro Area Full Year GDP Growth",
        "country_code": "EU",
        "logoid": "country/EU",
        "latest": 1.4,
        "previous": 0.9,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "ZAFYGDPG",
        "full_symbol": "ECONOMICS:ZAFYGDPG",
        "name": "South Africa Full Year GDP Growth",
        "country_code": "ZA",
        "logoid": "country/ZA",
        "latest": 1.1,
        "previous": 0.5,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "RUFYGDPG",
        "full_symbol": "ECONOMICS:RUFYGDPG",
        "name": "Russia Full Year GDP Growth",
        "country_code": "RU",
        "logoid": "country/RU",
        "latest": 1,
        "previous": 4.1,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "FRFYGDPG",
        "full_symbol": "ECONOMICS:FRFYGDPG",
        "name": "France Full Year GDP Growth",
        "country_code": "FR",
        "logoid": "country/FR",
        "latest": 0.9,
        "previous": 1.1,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "MXFYGDPG",
        "full_symbol": "ECONOMICS:MXFYGDPG",
        "name": "Mexico Full Year GDP Growth",
        "country_code": "MX",
        "logoid": "country/MX",
        "latest": 0.6,
        "previous": 1.5,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "ITFYGDPG",
        "full_symbol": "ECONOMICS:ITFYGDPG",
        "name": "Italy Full Year GDP Growth",
        "country_code": "IT",
        "logoid": "country/IT",
        "latest": 0.5,
        "previous": 0.8,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "DEFYGDPG",
        "full_symbol": "ECONOMICS:DEFYGDPG",
        "name": "Germany Full Year GDP Growth",
        "country_code": "DE",
        "logoid": "country/DE",
        "latest": 0.2,
        "previous": -0.5,
        "observation": "2025",
        "unit": "Percent",
        "frequency": "Annual"
      },
      {
        "symbol": "JPFYGDPG",
        "full_symbol": "ECONOMICS:JPFYGDPG",
        "name": "Japan Full Year GDP Growth",
        "country_code": "JP",
        "logoid": "country/JP",
        "latest": 0.1,
        "previous": 1.9,
        "observation": "2024",
        "unit": "Percent",
        "frequency": "Annual"
      }
    ]
  },
  "msg": "Success"
}
```
