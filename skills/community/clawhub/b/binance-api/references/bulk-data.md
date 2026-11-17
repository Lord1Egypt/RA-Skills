# Binance Public Data Archive (data.binance.vision)

Free, key-less downloadable archives of Binance's complete market history —
ZIP-compressed CSV files, one per symbol per day or per month, going back to
each symbol's listing date. For backtesting or any analysis needing more than
a few thousand candles, downloading these files is hundreds of times faster
than paging the REST API (a month of 1m klines = 1 file vs ~44 API calls).

Browse the archive interactively at:
`https://data.binance.vision/?prefix=data/spot/monthly/klines/BTCUSDT/`

Official reference: https://github.com/binance/binance-public-data

## URL patterns (verified)

```
https://data.binance.vision/data/<market>/<period>/<dataType>/<SYMBOL>/[<interval>/]<FILENAME>.zip
```

| Part | Values |
|---|---|
| `<market>` | `spot`, `futures/um` (USDⓈ-M), `futures/cm` (COIN-M) |
| `<period>` | `monthly`, `daily` |
| `<dataType>` | `klines`, `trades`, `aggTrades`; futures also: `fundingRate` (monthly only), `markPriceKlines`, `indexPriceKlines`, `premiumIndexKlines` |
| `<interval>` | klines only: `1s` (spot), `1m` … `1M` — same values as the REST API |
| `<FILENAME>` | `<SYMBOL>-<interval or dataType>-<YYYY-MM>` (monthly) or `<YYYY-MM-DD>` (daily) |

Verified working examples:

```
https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1d/BTCUSDT-1d-2025-01.zip
https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2026-07-04.zip
https://data.binance.vision/data/spot/monthly/aggTrades/BTCUSDT/BTCUSDT-aggTrades-2025-01.zip
https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2025-01.zip
https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-2025-01.zip
https://data.binance.vision/data/futures/cm/monthly/klines/BTCUSD_PERP/1d/BTCUSD_PERP-1d-2025-01.zip
```

Every `.zip` has a companion `.zip.CHECKSUM` file (sha256). A missing
file returns 404 — daily files appear the next day (UTC), monthly files a few
days after month end. For the current month, stitch daily files or fall back
to the REST API.

## CSV formats — two traps (both verified)

**1. Spot files have NO header row; futures files HAVE one.** Don't skip the
first line of a spot file, and don't parse the futures header as data.

**2. Spot timestamps are in MICROSECONDS (16 digits); futures are in
milliseconds (13 digits).** Spot archives switched to microseconds with the
2025-01 files. Detect by magnitude rather than assuming:

```python
def to_ms(ts: int) -> int:
    return ts // 1000 if ts >= 10**15 else ts
```

Spot kline row (no header — columns match the REST kline array exactly):

```
1735689600000000,93576.00000000,95151.15000000,92888.00000000,94591.79000000,10373.32613000,1735775999999999,975444194.13799830,1516556,5347.73648000,502914035.64059070,0
```

Futures kline file (with header, ms timestamps):

```
open_time,open,high,low,close,volume,close_time,quote_volume,count,taker_buy_volume,taker_buy_quote_volume,ignore
1735689600000,93548.80,94449.20,93460.20,94363.60,5744.609,1735693199999,539615914.46460,105263,3278.334,308056781.54270,0
```

Funding rate file:

```
calc_time,funding_interval_hours,last_funding_rate
1735689600015,8,0.00010000
```

## Loading recipe (pandas)

Pandas reads a ZIP URL directly — no manual download/extract needed:

```python
import pandas as pd

KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume",
              "close_time", "quote_volume", "count", "taker_buy_volume",
              "taker_buy_quote_volume", "ignore"]

def load_spot_klines_month(symbol: str, interval: str, month: str) -> pd.DataFrame:
    url = (f"https://data.binance.vision/data/spot/monthly/klines/"
           f"{symbol}/{interval}/{symbol}-{interval}-{month}.zip")
    df = pd.read_csv(url, header=None, names=KLINE_COLS)  # spot: no header
    ts = df["open_time"].where(df["open_time"] < 10**15, df["open_time"] // 1000)
    df["open_time"] = pd.to_datetime(ts, unit="ms")
    return df

df = load_spot_klines_month("BTCUSDT", "1d", "2025-01")
```

For futures files use `pd.read_csv(url)` as-is (header row present, ms
timestamps). To cover a long range, loop months (`2023-01` … `2025-12`) and
`pd.concat`; skip 404s for months before the symbol listed.

## When to use archive vs REST

- **Archive**: anything over ~1,000 candles, full-history backtests, trade
  tick data, funding rate history beyond 1,000 entries.
- **REST**: current/recent data (the archive lags by a day), the still-open
  candle, small ad-hoc lookups.
- A common pattern: bulk-load history from monthly files, top up the most
  recent days with daily files, then the last 24h from `GET /api/v3/klines`.
