---
name: "drt-market-lens"
description: "DRT/ICT market analysis framework: 1h klines, premium/discount zones and daily bias for 17 instruments (indices, forex, metals, crypto). 100% lokal analyse — ingen netværkskald, ingen API-nøgle."
metadata: {"clawbot": {"requires": {"python3": true}, "notes": "100% lokal analyse — ingen netværkskald, ingen API-nøgle."}}
---

# DRT Market Lens 🔭📊

Real-time market analysis framework based on Dealing Range Theory (DRT) + ICT concepts. Gives you the full market picture for **17 instruments** in one shot: indices (SP500, NAS100, DJ30), forex (EURUSD, GBPUSD, USDJPY, USDCHF), metals (XAUUSD, XAGUSD) and crypto (BTCUSD, ETHUSD, SOLUSD + more).

**100% lokal analyse** — ingen netværkskald, ingen API-nøgle, ingen eksterne afhængigheder. Kører med Python 3 og standardbiblioteket.

## Hvad skill'en giver dig 🎯

For hver af de 17 symboler får du:

1. **1h klines** — seneste 1h-candles til at vurdere prisstruktur
2. **ICT daily bias** — premium/discount vurdering (er prisen i discount = købszone, eller premium = salgszone?)
3. **SMA50/200** — trendfilter: pris over begge = bullish bias, under begge = bearish
4. **DRT-kontekst** — hvor i dealing range'en befinder prisen sig (25DRT / 50DRT / 75DRT)

## Sådan bruger du den 🛠️

```bash
# Kør market lens for alle 17 symboler
python3 scripts/market_lens.py

# Kør for udvalgte symboler
python3 scripts/market_lens.py XAUUSD EURUSD BTCUSD

# Output: tabel med bias + premium/discount + SMA-status pr. symbol
```

Hvis du ikke har data lokalt, kan du hente 1h-klines fra en gratis kilde (f.eks. Binance API for krypto, eller din brokers data) og gemme som CSV — scriptet læser standard-formatet.

## Analyse-logik 🧠

| Signale | Betydning |
|---|---|
| Pris i **discount** (under 50DRT / 25DRT zone) | Købszone — long bias (ICT) |
| Pris i **premium** (over 50DRT / 75DRT zone) | Salgszone — short bias (ICT) |
| Pris > SMA50 og SMA200 | Bullish trendfilter |
| Pris < SMA50 og SMA200 | Bearish trendfilter |
| Daily bias + trendfilter i samme retning | A+ setup-kontekst |

## De 17 symboler 📋

- **Indices:** SP500, NAS100, DJ30
- **Forex:** EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD
- **Metals:** XAUUSD (guld), XAGUSD (sølv)
- **Crypto:** BTCUSD, ETHUSD, SOLUSD, BNBUSD, XRPUSD, DOGEUSD, ADAUSD

## Integration med andre skills 🤝

- **drt-trading** — brug market lens til at finde bias, derefter drt-trading til entry-modeller (25/75DRT closure, 50DRT displacement)
- **trading-news-guard** — tjek nyhedskalenderen før du tager et signal fra lens
- **crypto-sentiment-pulse** — kombiner sentiment med bias for stærkere filtrering

## Sikkerhed 🔒

- Ingen netværkskald, ingen data forlader din maskine
- Ingen API-nøgler, ingen eksterne pakker — kun Python 3 standardbibliotek
- Læs kun markedsdata, udfører ALDRIG handler
