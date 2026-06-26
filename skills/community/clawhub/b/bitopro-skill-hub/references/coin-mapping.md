# BitoPro Coin Mapping

Complete mapping between BitoPro symbols, CoinGecko IDs, and CoinPaprika IDs.

> Last verified: 2026-04-14

## Full Mapping Table

| BitoPro Symbol | Name | CoinGecko ID | CoinPaprika ID | Notes |
|----------------|------|-------------|----------------|-------|
| BTC | Bitcoin | `bitcoin` | `btc-bitcoin` | |
| ETH | Ethereum | `ethereum` | `eth-ethereum` | |
| USDT | Tether | `tether` | `usdt-tether` | Stablecoin |
| USDC | USD Coin | `usd-coin` | `usdc-usd-coin` | Stablecoin |
| XRP | XRP | `ripple` | `xrp-xrp` | |
| SOL | Solana | `solana` | `sol-solana` | |
| BNB | BNB | `binancecoin` | `bnb-binance-coin` | |
| DOGE | Dogecoin | `dogecoin` | `doge-dogecoin` | |
| ADA | Cardano | `cardano` | `ada-cardano` | |
| TRX | TRON | `tron` | `trx-tron` | |
| TON | Toncoin | `the-open-network` | `ton-toncoin` | |
| LTC | Litecoin | `litecoin` | `ltc-litecoin` | |
| BCH | Bitcoin Cash | `bitcoin-cash` | `bch-bitcoin-cash` | |
| SHIB | Shiba Inu | `shiba-inu` | `shib-shiba-inu` | |
| POL | POL (ex-MATIC) | `polygon-ecosystem-token` | `matic-polygon` | CoinPaprika still uses old MATIC ID |
| APE | ApeCoin | `apecoin` | `ape-apecoin` | |
| KAIA | Kaia | `kaia` | `kaia-kaia` | Formerly Klaytn (KLAY) |
| BITO | BITO Coin | `bito-coin` | `bito-bito-coin` | BitoPro exchange token |

## CoinGecko IDs (comma-separated, for API calls)

> Canonical list used as the default `ids=` for Tool 3 (`get_coin_rankings`). **If you add/remove a coin here, also update the same string embedded in `SKILL.md` → Tool 3 → params → `ids` default value.** Keeping both in sync ensures the T3 cache key stays stable across overview turns.

```
bitcoin,ethereum,tether,ripple,binancecoin,usd-coin,solana,dogecoin,cardano,tron,the-open-network,litecoin,bitcoin-cash,shiba-inu,polygon-ecosystem-token,apecoin,kaia,bito-coin
```

## BitoPro Symbol Set (for filtering)

```
BTC,ETH,USDT,USDC,XRP,SOL,BNB,DOGE,ADA,TRX,TON,LTC,BCH,SHIB,POL,APE,KAIA,BITO
```

## BitoPro Trading Pairs

As of 2026-04-14, BitoPro has active trading pairs across TWD and USDT quote currencies for the 18 base coins above.

### TWD Pairs
BTC_TWD, ETH_TWD, USDT_TWD, USDC_TWD, XRP_TWD, SOL_TWD, BNB_TWD, DOGE_TWD, ADA_TWD, TRX_TWD, TON_TWD, LTC_TWD, BCH_TWD, SHIB_TWD, POL_TWD, APE_TWD, KAIA_TWD, BITO_TWD

### USDT Pairs
BTC_USDT, ETH_USDT, XRP_USDT, SOL_USDT, BNB_USDT, DOGE_USDT, ADA_USDT, TRX_USDT, TON_USDT, LTC_USDT, BCH_USDT, SHIB_USDT, POL_USDT, APE_USDT, KAIA_USDT

> Always call Tool 7 (`get_bitopro_pairs`) with `Accept: application/json` header to verify live pair availability — the hard-coded list above is for reference only.

## Updating This Mapping

When BitoPro adds new coins:

1. Call `GET https://api.bitopro.com/v3/provisioning/trading-pairs` to get updated list
2. For new coins, find CoinGecko ID via `GET https://api.coingecko.com/api/v3/search?query={coin_name}`
3. For CoinPaprika, search via `GET https://api.coinpaprika.com/v1/search?q={coin_name}`
4. Update this mapping file

## Known ID Discrepancies

- **POL/MATIC**: CoinGecko uses `polygon-ecosystem-token` (new name), CoinPaprika still uses `matic-polygon` (old name). Both resolve to the same asset.
- **KAIA/KLAY**: Formerly Klaytn, rebranded to Kaia. Both CoinGecko and CoinPaprika now use Kaia IDs.

## Handling Partial Data

A coin in this mapping may return `market_cap_rank: null` or `market_cap: 0` from CoinGecko depending on listing coverage. When this happens, display rank as `—`, skip the market-cap column, and still show price and 24h change.

## Handling Pairs Outside This Mapping

If `get_bitopro_pairs` returns a pair whose `base` is not listed in this mapping, treat it as out of scope: exclude it from the main table and flag it separately under "⚠️ 不在映射內". Refresh this mapping periodically (see below) to keep it aligned with the live BitoPro listing.

## News matching patterns (for Tool 8)

Used by `get_bitopro_relevant_news` to match articles to BitoPro coins. Each coin has multiple patterns: ticker, English name(s), 繁中 name(s). Patterns are **case-insensitive** with **word boundaries** for tickers (so `BTC` matches `BTC` but not `BTCUSD-something-other`).

> **Order matters**: longer / more specific patterns must be checked first to avoid false matches. For example, check `Bitcoin Cash` before `Bitcoin` (else BCH articles get tagged as BTC).

| Symbol | Patterns (ticker / EN name / 中文名) |
|--------|-------------------------------------|
| USDT | `\bUSDT\b`, `\bTether\b`, `泰達(幣\|)` |
| USDC | `\bUSDC\b`, `\bUSD Coin\b` |
| BCH  | `\bBCH\b`, `Bitcoin Cash`, `比特幣現金` |
| SHIB | `\bSHIB\b`, `Shiba Inu`, `柴犬幣?` |
| DOGE | `\bDOGE\b`, `Dogecoin`, `狗狗幣` |
| KAIA | `\bKAIA\b` |
| BITO | `\bBITO\b` |
| APE  | `\bAPE\b`, `Apecoin`, `ApeCoin` |
| POL  | `\bPOL\b`, `\bMATIC\b`, `Polygon` |
| TON  | `\bTON\b`, `Toncoin`, `The Open Network` |
| TRX  | `\bTRX\b`, `\bTron\b`, `波場` |
| LTC  | `\bLTC\b`, `Litecoin`, `萊特幣` |
| ADA  | `\bADA\b`, `Cardano`, `卡爾達諾` |
| SOL  | `\bSOL\b`, `Solana`, `索拉納` |
| BNB  | `\bBNB\b`, `Binance Coin`, `幣安幣` |
| XRP  | `\bXRP\b`, `Ripple`, `瑞波` |
| ETH  | `\bETH\b`, `Ethereum`, `以太(坊\|幣\|)` |
| BTC  | `\bBTC\b`, `Bitcoin`, `比特幣` |

> Note `MATIC` is included under POL because legacy English news still uses the old ticker. Some articles refer to "Polygon (MATIC)" — both forms should hit POL.

### Reference implementation (Python)

```python
import re

PATTERNS = [
    ('USDT', [r'\bUSDT\b', r'\bTether\b', r'泰達(幣|)']),
    ('USDC', [r'\bUSDC\b', r'\bUSD Coin\b']),
    ('BCH',  [r'\bBCH\b', r'Bitcoin Cash', r'比特幣現金']),
    # ... (longer first, shorter last — see table above)
    ('ETH',  [r'\bETH\b', r'Ethereum', r'以太(坊|幣|)']),
    ('BTC',  [r'\bBTC\b', r'Bitcoin', r'比特幣']),
]
COMPILED = [(sym, [re.compile(p, re.IGNORECASE) for p in pats]) for sym, pats in PATTERNS]

def find_coins(text: str) -> list[str]:
    matched, seen = [], set()
    for sym, regexes in COMPILED:
        if any(r.search(text) for r in regexes):
            if sym not in seen:
                matched.append(sym); seen.add(sym)
    return matched
```

### Maintenance

When BitoPro lists a new coin:
1. Add full mapping (symbol, name, CoinGecko ID, CoinPaprika ID) to the table at the top.
2. Add ticker / English name / 中文名 patterns to the **News matching patterns** table above.
3. Update T3's canonical `ids=` string in SKILL.md.
4. Re-run T8 evals to verify the new coin appears in news matches.

When a coin is delisted from BitoPro:
1. Remove from the top mapping table.
2. Remove from the News matching patterns table (so news no longer surfaces it).
3. Keep an internal note in `CLAUDE.md` about the delisting (do NOT publish).
