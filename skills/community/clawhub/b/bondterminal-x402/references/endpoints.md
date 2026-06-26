# BondTerminal API v1 — Endpoint Reference

Base URL: `https://bondterminal.com/api/v1`

Cost on x402 routes: $0.01 USDC per request (Base mainnet)

## Free Endpoints

```
GET /treasury-curve          US Treasury yield curve (live)
```

## x402-Protected Endpoints

```
GET /bonds                           List all bonds (~60 sovereign + corporate)
GET /bonds?search=AL30               Search by name/ticker
GET /bonds/:id                       Bond details (ISIN or local ticker with D/C suffix)
GET /bonds/:id/analytics             Price, YTM, duration, spreads, issuance data
GET /bonds/:id/cashflows             Full cashflow schedule
GET /bonds/:id/history               Historical price/yield/spread series
GET /bonds/:id/history?range=1y      Filtered history (1w, 1m, 3m, 6m, 1y, all)
POST /calculate                      Calculate analytics from custom price
GET /riesgo-pais                     Current Argentina country risk spread
GET /riesgo-pais/history             Historical riesgo país
GET /riesgo-pais/history?range=1m    Filtered history
```

## Bearer-Only Endpoints

```
POST /calculate/batch                Batch bond calculations (subscription required)
```

## Auth Behavior

- x402 routes return `402` with `PAYMENT-REQUIRED` header when called without auth
- Client signs EIP-3009 payment and retries with `PAYMENT-SIGNATURE` (v2), with `X-PAYMENT` as legacy fallback
- Bearer token auth (`Authorization: Bearer <key>`) also accepted on all x402 routes
- Successful payment returns `PAYMENT-RESPONSE` header with settlement tx hash

## Identifier Formats

- **ISIN**: `US040114HS26`, `ARARGE3209S6`
- **Local ticker**: requires D (USD) or C (ARS) suffix — `AL30D`, `GD30D`, `AN29D`
- **NOT**: `AL30`, `GD30` (missing suffix will fail)

## Key Sovereign Tickers

**NY Law (ARGENT):** GD29D, GD30D, GD35D, GD38D, GD41D, GD46D
**AR Law (ARGBON):** AL29D, AN29D, AL30D, AL35D, AE38D, AL41D
