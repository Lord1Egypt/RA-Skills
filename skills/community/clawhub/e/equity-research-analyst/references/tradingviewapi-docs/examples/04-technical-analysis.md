# Technical Analysis

- Source: `openapi.json`
- Generated At: `2026-04-21T18:58:33+08:00`
- Live Requests: `enabled`

## Get Technical Analysis

`GET /api/ta/{symbol}`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/ta/BINANCE:BTCUSDT' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "1": {
      "Other": 0,
      "All": 0.666,
      "MA": 1.334
    },
    "5": {
      "Other": -0.546,
      "All": 0.528,
      "MA": 1.6
    },
    "15": {
      "Other": 0.182,
      "All": 1.024,
      "MA": 1.866
    },
    "60": {
      "Other": 0.546,
      "All": 1.206,
      "MA": 1.866
    },
    "240": {
      "Other": 0.364,
      "All": 1.116,
      "MA": 1.866
    },
    "1D": {
      "Other": 0.364,
      "All": 0.848,
      "MA": 1.334
    },
    "1W": {
      "Other": 0.182,
      "All": -0.042,
      "MA": -0.266
    },
    "1M": {
      "Other": 0.364,
      "All": 0.028,
      "MA": -0.308
    }
  },
  "msg": "Success"
}
```

## Get Technical Indicators

`GET /api/ta/{symbol}/indicators`

### Request

```bash
curl --request GET \
	--url 'https://tradingview-data1.p.rapidapi.com/api/ta/BINANCE:BTCUSDT/indicators' \
	--header 'x-rapidapi-host: tradingview-data1.p.rapidapi.com' \
	--header 'x-rapidapi-key: YOUR_RAPIDAPI_KEY'
```

### Response

HTTP `200`

```json
{
  "success": true,
  "data": {
    "ADX": 19.652487681663818,
    "ADX+DI": 24.161442624343998,
    "ADX+DI[1]": 24.107709917495246,
    "ADX-DI": 15.05945224768997,
    "ADX-DI[1]": 15.715010661700024,
    "AO": 5023.2678823530005,
    "AO[1]": 4773.818411764762,
    "AO[2]": 4652.421588235346,
    "BBPower": 3913.5008482531557,
    "CCI20": 101.85872220705717,
    "CCI20[1]": 86.76734493591583,
    "EMA10": 74780.5606040116,
    "EMA100": 75331.624080014,
    "EMA20": 73240.35381466728,
    "EMA200": 82719.03255409811,
    "EMA30": 72383.40753068113,
    "EMA50": 72130.97430961842,
    "HullMA9": 75728.77085185186,
    "Ichimoku.BLine": 71666.5,
    "MACD.macd": 1763.4939112112334,
    "MACD.signal": 1385.901728770365,
    "Mom": 3711.8399999999965,
    "Mom[1]": 2878.279999999999,
    "Pivot.M.Camarilla.Middle": 69761.49333333333,
    "Pivot.M.Camarilla.R1": 69292.81333333332,
    "Pivot.M.Camarilla.R2": 70301.14666666667,
    "Pivot.M.Camarilla.R3": 71309.48,
    "Pivot.M.Camarilla.S1": 67276.14666666667,
    "Pivot.M.Camarilla.S2": 66267.81333333332,
    "Pivot.M.Camarilla.S3": 65259.479999999996,
    "Pivot.M.Classic.Middle": 69761.49333333333,
    "Pivot.M.Classic.R1": 74522.98666666666,
    "Pivot.M.Classic.R2": 80761.49333333333,
    "Pivot.M.Classic.R3": 91761.49333333333,
    "Pivot.M.Classic.S1": 63522.986666666664,
    "Pivot.M.Classic.S2": 58761.49333333333,
    "Pivot.M.Classic.S3": 47761.49333333333,
    "Pivot.M.Demark.Middle": 71321.12,
    "Pivot.M.Demark.R1": 77642.23999999999,
    "Pivot.M.Demark.S1": 66642.23999999999,
    "Pivot.M.Fibonacci.Middle": 69761.49333333333,
    "Pivot.M.Fibonacci.R1": 73963.49333333333,
    "Pivot.M.Fibonacci.R2": 76559.49333333333,
    "Pivot.M.Fibonacci.R3": 80761.49333333333,
    "Pivot.M.Fibonacci.S1": 65559.49333333333,
    "Pivot.M.Fibonacci.S2": 62963.49333333333,
    "Pivot.M.Fibonacci.S3": 58761.49333333333,
    "Pivot.M.Woodie.Middle": 69392.245,
    "Pivot.M.Woodie.R1": 73784.48999999999,
    "Pivot.M.Woodie.R2": 80392.245,
    "Pivot.M.Woodie.R3": 84784.48999999999,
    "Pivot.M.Woodie.S1": 62784.48999999999,
    "Pivot.M.Woodie.S2": 58392.244999999995,
    "Pivot.M.Woodie.S3": 51784.48999999999,
    "RSI": 62.32032133359257,
    "RSI[1]": 60.33441551235267,
    "Rec.BBPower": 0,
    "Rec.HullMA9": 1,
    "Rec.Ichimoku": 0,
    "Rec.Stoch.RSI": 0,
    "Rec.UO": 0,
    "Rec.VWMA": 1,
    "Rec.WR": 0,
    "Recommend.All": 0.4242424242424242,
    "Recommend.MA": 0.6666666666666666,
    "Recommend.Other": 0.18181818181818182,
    "SMA10": 74841.63299999997,
    "SMA100": 74029.35089999987,
    "SMA20": 72412.94299999985,
    "SMA200": 86127.83279999996,
    "SMA30": 71062.32999999997,
    "SMA50": 70728.8624,
    "Stoch.D": 72.09683327831802,
    "Stoch.D[1]": 66.97928657906914,
    "Stoch.K": 71.23027622473747,
    "Stoch.K[1]": 58.75843873494322,
    "Stoch.RSI.K": 49.046112060737244,
    "UO": 54.236726965625174,
    "VWMA": 72554.81333444374,
    "W.R": -20.058472098639886,
    "close": 76755
  },
  "msg": "Success"
}
```
