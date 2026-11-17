# Methodology and Sources

## Source priority

1. Product manager or HKEX product documents for product design, current disclosures, NAV, iNAV, creations, and market makers.
2. KRX or a KRX-licensed feed for 000660 previous close, open, and latest price.
3. Nasdaq/primary market feed for SKHY previous and latest close.
4. SEC issuer filings or the depositary bank for the ADS ratio.
5. Institutional market data such as Wind as a cross-check. Record the exact symbol and timestamp.

Never merge stale observations without labels. State each market's date and local timestamp.

## Product facts

- 07709 targets twice the **daily** performance of SK hynix common stock, KRX 000660, before fees and expenses.
- It primarily uses partially funded swaps and may use options. It is not a conventional cash equity ETF.
- Its base currency is USD; its exchange trading currency is HKD.
- The manager publishes near-real-time HKD indicative NAV during SEHK hours, updated every 15 seconds.
- The June 2026 Product Key Facts states an estimated annual average daily tracking difference of -0.30%, but this is not a guaranteed per-day haircut.
- The product document says swap and option costs may be high, capacity constraints may prevent creations, and secondary-market units may trade at substantial premium or discount.

Primary product document:

- https://www.hkexnews.hk/listedco/listconews/sehk/2026/0622/2026062200892.pdf
- https://www.csopasset.com/en/products/hk-skhy-2l

## ADS ratio and parity

The current SKHY ADS represents one-tenth of one SK hynix common share. Therefore:

```text
one common share = 10 ADS
ADR-implied common value in KRW = SKHY price in USD × 10 × USDKRW
```

Confirm the ratio on every material change or corporate action:

- SEC filing: https://www.sec.gov/Archives/edgar/data/2120882/000119312526299963/d32785d424b4.htm
- Citi DR directory: https://depositaryreceipts.citi.com/

Parity is only a diagnostic. Depositary issuance/cancellation mechanics, settlement, capital flows, borrow, liquidity, market hours, and demand can leave SKHY far from KRX parity. If parity is distorted, retain the SKHY percentage move as an overnight sentiment signal but do not convert its absolute price into the 07709 fair value.

## Interpretation

Use the immediately preceding 07709 NAV as the clean base:

```text
NAV fair value = prior NAV × (1 + 2 × KRX return)
```

This is a gross theoretical value, not a promised quote. Separately model the exchange price:

```text
tradable scenario = NAV fair value × (1 + assumed secondary-market premium/discount)
```

The prior market discount is a useful stress scenario, not a law. It may close rapidly after creations resume or widen under one-way order flow and derivative-capacity constraints.

For an SEHK opening estimate:

- Before KRX opens: use SKHY return as a provisional signal.
- After KRX opens and before SEHK opens: replace it with latest KRX return.
- During SEHK hours: prefer the manager's iNAV; use this calculator as an independent reasonableness check.

