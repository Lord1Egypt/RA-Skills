# Estimate Hynix 2x Open

[中文说明](README.zh-CN.md)

An agent skill for estimating the fair opening or intraday value of **CSOP SK Hynix Daily (2x) Leveraged Product (HKEX: 07709)** from:

- the latest 07709 NAV and secondary-market price;
- SK hynix common stock on KRX (`000660`);
- SK hynix ADS on Nasdaq (`SKHY`);
- the ADS conversion ratio and USD/KRW;
- the previous 07709 market premium or discount.

The skill separates **NAV fair value** from a **tradable-price scenario**. It treats the live KRX return as the primary anchor, the Nasdaq ADS return as an overnight direction check, and ADS absolute-price parity as a diagnostic only.

## What it returns

- NAV-based fair value from the KRX open or latest quote
- A carried-discount scenario based on the previous 07709 close
- An ADS-return signal value
- ADS-implied Korean common-share value and parity premium
- Warnings for stale inputs, large cross-market divergence, extreme KRX moves, and secondary-market discount risk

## Requirements

- An agent capable of obtaining timestamped market data
- Python 3.9 or later for the deterministic calculator
- No API key or third-party Python package is required by the bundled script

The calculator does not fetch quotes or place trades. The calling agent must collect and verify the inputs.

## Install from ClawHub

```bash
clawhub install estimate-hynix-2x-open
```

Then ask your agent:

```text
Use $estimate-hynix-2x-open to estimate today's fair opening price for HK 07709.
```

## Calculator example

Run from the skill directory:

```bash
python3 scripts/estimate_open.py \
  --nav-hkd 27.249 \
  --product-prev-market 25.36 \
  --kr-prev-close 1322000 \
  --kr-open 1697000 \
  --kr-current 1628000 \
  --adr-prev-close 126.79 \
  --adr-close 149 \
  --usdkrw 1427.68
```

Windows PowerShell:

```powershell
py -3.10 .\scripts\estimate_open.py `
  --nav-hkd 27.249 `
  --product-prev-market 25.36 `
  --kr-prev-close 1322000 `
  --kr-open 1697000 `
  --kr-current 1628000 `
  --adr-prev-close 126.79 `
  --adr-close 149 `
  --usdkrw 1427.68
```

## Model

```text
KRX return = KRX anchor / KRX previous close - 1
NAV fair value = previous NAV × (1 + 2 × KRX return + tracking adjustment)

ADS return = ADS close / ADS previous close - 1
ADS signal value = previous NAV × (1 + 2 × ADS return)

ADS-implied common value = ADS close × ADSs per common share × USDKRW
ADS parity premium = ADS-implied common value / KRX anchor - 1

Previous 07709 discount = previous market close / previous NAV - 1
Carried-discount value = NAV fair value × (1 + previous discount)
```

Do not use the previous 07709 market close as the leverage base. It already contains a secondary-market premium or discount.

## Data hierarchy

1. Live KRX `000660` quote immediately before the HKEX open
2. Latest KRX opening or intraday quote
3. Nasdaq `SKHY` percentage return
4. ADS absolute parity only when the parity gap is small

If the ADS parity gap exceeds 5%, the skill flags the ADS as a direction signal rather than a fair-value anchor.

## Risks and limitations

- 07709 targets twice the **daily** return; it is not a long-term 2x holding.
- Swap and option capacity, market-maker inventory, creation/redemption availability, and bid-ask spreads can keep the exchange price away from NAV.
- KRX circuit breakers, daily limits, suspensions, and delayed quotes can invalidate an estimate.
- ADS issuance/cancellation, settlement, liquidity, and market-hour differences can distort SKHY parity.
- The result is a timestamped estimate, not a guaranteed executable quote or investment recommendation.

See [the methodology reference](references/methodology.md) for source priority and product-document links.

## License

Skills published on ClawHub are released under MIT-0.

