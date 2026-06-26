---
name: cap-table-manager
version: 1.0.0
description: >
  Equity cap table management for startups and growth-stage companies.
  Models SAFEs, convertible notes, priced equity rounds, token allocations,
  dilution scenarios, and 409A valuation prep. Outputs investor-ready cap
  tables, waterfall analyses, and scenario models.
tags:
  - finance
  - equity
  - startup
  - cap-table
  - saas
  - legal
author: PrecisionLedger / Sam Ledger
---

# Cap Table Manager

Manage equity ownership from Day 1 through exit. Model rounds, dilution, SAFEs, options pools, and token side-tables. Output investor-ready cap tables and scenario analyses.

## When to Use

- Modeling pre-seed / seed / Series A+ rounds and dilution impact
- Tracking SAFE conversions (MFN, pro-rata, discount, valuation cap)
- Building a convertible note conversion schedule
- Calculating fully diluted share counts and ownership percentages
- Scenario planning: best / base / bear case valuations and payout waterfalls
- Preparing 409A valuation support materials
- Modeling option pool expansion (pre-money vs post-money shuffle)
- Token allocation tables alongside equity (hybrid company structures)
- Generating investor-ready cap table exports (CSV, Google Sheets, Excel)

## When NOT to Use

- Public company equity management (use Carta, Shareworks, or a transfer agent)
- Complex secondary transactions requiring legal execution (refer to securities counsel)
- Tax advice on stock option grants, ISOs vs NSOs (refer to CPA with PTIN)
- Cap table maintenance in a state with specific securities filing requirements — flag for attorney review
- Replacing a cap table tool of record (Carta, Pulley, LTSE) for an active company with >25 stakeholders
- Anything requiring custodianship, ledger finality, or board-authorized record keeping

---

## Core Concepts

### Share Classes
- **Common Stock** — founders and employees; lowest liquidation preference
- **Preferred Stock** — investors; liquidation preference + conversion rights
- **Options/Warrants** — unissued; part of fully diluted but not issued shares
- **SAFEs** — Simple Agreement for Future Equity; convert at next priced round
- **Convertible Notes** — debt converting to equity at a discount or cap

### Key Metrics
| Metric | Formula |
|--------|---------|
| Ownership % | Shares Held / Total Fully Diluted Shares |
| Pre-Money Valuation | Post-Money − New Investment |
| Price Per Share | Pre-Money Valuation / Pre-Money Fully Diluted Shares |
| Dilution % | 1 − (Old Shares / New Fully Diluted Shares) |
| Liquidation Preference | Investment Amount × Preference Multiple |

---

## Workflows

### 1. Build a Baseline Cap Table

Collect and structure current ownership:

```
Stakeholder | Class | Shares | % Ownership | Notes
------------|-------|--------|-------------|------
Founder A   | Common | 4,000,000 | 40% | Vesting 4yr/1yr cliff
Founder B   | Common | 3,000,000 | 30% | Vesting 4yr/1yr cliff
Option Pool | Options | 1,000,000 | 10% | 2024 Plan, unissued
Angel 1     | SAFE   | —      | —   | $250K @ $5M cap, 20% discount
Angel 2     | SAFE   | —      | —   | $100K MFN SAFE
TOTAL (pre-conversion) | | 8,000,000 | 80% issued |
```

**Calculation prompt:**
> "Build me a cap table. Founders: Alice 4M shares, Bob 3M shares. Option pool: 1M shares. Pre-money fully diluted: 8M shares. We have a $250K SAFE at $5M cap and 20% discount, and a $100K MFN SAFE. We're raising a $2M seed at $8M pre-money. Show post-close ownership for all parties."

---

### 2. Model a Priced Round

**Inputs needed:**
- Pre-money valuation
- Investment amount
- New option pool size (if expanding pre-money)
- Existing cap table (issued + options + SAFEs outstanding)

**Step-by-step:**

1. **Calculate post-money option pool** (if pre-money shuffle):
   - New option pool shares = Target % × Post-Money Fully Diluted
   - Example: 15% post-close pool on 12M post-money FD shares = 1.8M options reserved

2. **Calculate price per share:**
   - Pre-Money FD shares (including new pool) = existing shares + new pool shares
   - PPS = Pre-Money Valuation / Pre-Money FD shares

3. **Convert SAFEs:**
   - Conversion price = lower of: (PPS × (1 − discount)) OR (Cap / Pre-SAFE FD shares)
   - SAFE shares = Investment / Conversion Price

4. **Issue new investor shares:**
   - New shares = Investment / PPS

5. **Rebuild fully diluted table post-close**

**Example — Seed Round:**
```
Pre-money valuation:     $8,000,000
New investment:          $2,000,000
Post-money valuation:    $10,000,000

Pre-money FD shares (incl. pool shuffle): 9,500,000
Price per share: $8M / 9.5M = $0.8421

SAFE #1 conversion ($250K @ $5M cap, 20% disc):
  Cap price:      $5M / 8M pre-SAFE shares = $0.625
  Discount price: $0.8421 × 0.80 = $0.6737
  Conversion at:  $0.625 (lower)
  SAFE shares:    $250K / $0.625 = 400,000 shares

SAFE #2 conversion (MFN → matches best terms = $0.625):
  SAFE shares:    $100K / $0.625 = 160,000 shares

New investor shares: $2M / $0.8421 = 2,375,012 shares

Post-close fully diluted: 9,500,000 + 400,000 + 160,000 + 2,375,012 = 12,435,012
```

---

### 3. Option Pool Modeling

**Pre-money pool shuffle (standard VC ask):**
> New pool is carved out pre-close, diluting founders not investors.

```
Target post-close option pool: 15%
Post-money FD shares (target): X
New pool = 0.15 × X

Solve: X = existing_shares + new_pool + investor_shares
       X = existing_shares + 0.15X + (investment / PPS)
       PPS = pre_money / (existing_shares + 0.15X)
```
Use iteration or algebra to solve. Common shortcut: model in a spreadsheet with goal-seek on ownership %.

**Prompt template:**
> "I have 8M fully diluted shares pre-round. VC wants 20% post-money ownership for $3M. They also want a 15% option pool post-close, pre-money shuffle. What's the pre-money valuation implied, PPS, and final ownership table?"

---

### 4. Waterfall Analysis (Exit Scenarios)

Model liquidation preference payout order at various exit values.

**Standard waterfall order:**
1. Debt repayment (if any)
2. Preferred liquidation preferences (1x non-participating is most common)
3. Common stock (pro-rata with preferred if participating, or preferred converts)
4. Option/warrant holders (exercise if in-the-money)

**Example — 1x non-participating preferred:**
```
Exit value: $15,000,000
Preferred investment: $2,000,000 (Series Seed, 1x non-participating)
Common shares: 10M | Preferred shares: 2.4M | FD: 12.4M

Option A (preferred takes preference):
  Preferred gets: $2,000,000 (1x)
  Remaining for common: $13,000,000
  Common per share: $13M / 10M = $1.30

Option B (preferred converts to common):
  All shares pro-rata: $15M / 12.4M = $1.21/share
  Preferred gets: 2.4M × $1.21 = $2,903,226

Preferred chooses: Option A ($2M) vs Option B ($2.9M) → converts to common
```

**Build exit scenarios at: $5M, $10M, $20M, $50M, $100M** — show each stakeholder's payout.

---

### 5. 409A Valuation Prep

Gather inputs for a 409A (required before each option grant):

**Required inputs:**
- Current cap table (fully diluted, all classes)
- Most recent priced round (date, PPS, investors)
- Any SAFEs or convertible notes outstanding
- Company financials: revenue, ARR, burn rate, cash runway
- Comparable company multiples (revenue multiple, EBITDA multiple)
- Any material events since last 409A (new contracts, pivots, key hires)

**Common 409A methods:**
| Method | Best For | Common Weight |
|--------|----------|---------------|
| Market Approach (OPM) | VC-backed, priced rounds | 60–80% |
| Income Approach (DCF) | Revenue-generating | 10–30% |
| Asset Approach | Pre-revenue / distress | 0–20% |

**Output to provide to 409A firm:**
- Fully diluted cap table (CSV)
- Most recent investor presentation / pitch deck
- 3 years of financials (actuals + projections)
- List of comparable public companies or recent M&A transactions

---

### 6. Token Allocation Table (Hybrid Structures)

For companies with both equity and token components:

```
Token Allocation (Total Supply: 1,000,000,000)
-----------------------------------------------
Team & Founders:   20% = 200M tokens | 4yr vest, 1yr cliff
Investors:         15% = 150M tokens | 2yr vest, 6mo cliff
Ecosystem/DAO:     30% = 300M tokens | 5yr linear release
Public Sale:       10% = 100M tokens | Unlocked at TGE
Treasury:          15% = 150M tokens | DAO governed
Advisors:           5% =  50M tokens | 2yr vest, 6mo cliff
Liquidity/Market:   5% =  50M tokens | Unlocked at TGE

Equity ↔ Token relationship:
- Token grants to equity holders: [document separately]
- Anti-dilution protection: [specify if tokens trigger]
- Side letter required for investor token rights
```

---

### 7. CSV/Sheets Export Format

Standard investor-ready cap table columns:

```csv
Stakeholder,Type,Share Class,Shares Issued,Options,Warrants,SAFE (Unconverted),Fully Diluted Shares,Ownership %,Investment,Note
Alice Chen,Founder,Common,4000000,,,,,32.2%,,4yr vest 1yr cliff
Bob Smith,Founder,Common,3000000,,,,,24.2%,,4yr vest 1yr cliff
Option Pool,Employees,Options,,1500000,,,1500000,12.1%,,2024 Equity Plan
Sequoia Capital,Investor,Series Seed Pref,2375012,,,,,19.1%,"$2,000,000",1x non-part
SAFE Holder 1,Investor,Common (converted),400000,,,,,3.2%,"$250,000",Converted @ $0.625
SAFE Holder 2,Investor,Common (converted),160000,,,,,1.3%,"$100,000",MFN converted
TOTALS,,,9935012,1500000,,,12435012,100%,"$2,350,000",
```

---

## Common Errors & Watch-Outs

| Issue | Symptom | Fix |
|-------|---------|-----|
| Double-counting SAFEs | FD shares too high | Only count SAFEs post-conversion |
| Pre/post money confusion | Wrong PPS | Confirm: pre-money = before investment, post-money = after |
| Option pool shuffle missed | Founders less diluted than expected | Confirm pool created pre-close |
| Participating preferred math | Payout too high | Check if preferred also gets pro-rata after preference |
| Wrong discount application | SAFE converts at wrong price | Discount on PPS, cap on pre-SAFE FD shares |

---

## Quick Reference — Useful Formulas

```
Post-money valuation     = Pre-money + New Investment
Price Per Share (PPS)    = Pre-money / Pre-money FD Shares
SAFE conversion shares   = SAFE Amount / min(Cap PPS, Discount PPS)
Discount PPS             = PPS × (1 - Discount Rate)
Cap PPS                  = Valuation Cap / Pre-SAFE FD Shares
Option pool shares       = Target % × Post-money FD Shares  [if post-money basis]
Dilution %               = New Shares / (Old FD + New Shares)
Ownership %              = Stakeholder Shares / Total FD Shares
```

---

## Escalation Triggers

Flag to attorney or CPA when:
- Preferred stock has complex liquidation preferences (2x, participating, caps)
- Anti-dilution provisions (broad-based vs narrow-based weighted average, full ratchet)
- Drag-along, tag-along, or ROFR rights affect modeling assumptions
- 83(b) election windows, ISO limits ($100K/yr rule), or QSBS eligibility
- Token rights embedded in equity instruments (side letters, token warrants)
- Company has international founders or investors (foreign private issuer rules)

---

## Example Prompts

**Round modeling:**
> "We're raising a $5M Series A at a $20M pre-money. Current cap: 8M founder shares, 1.5M option pool, $500K SAFE at $8M cap 20% discount. VC wants 15% post-money option pool, pre-money shuffle. Show me the full post-close cap table."

**Dilution check:**
> "How much will founders dilute if we raise $3M at $12M pre-money with a 20% post-close option pool?"

**Exit waterfall:**
> "Model our exit waterfall at $10M, $25M, $50M. We have: 2x participating preferred ($2M invested), then common. Show who gets what at each exit."

**SAFE conversion:**
> "We have three SAFEs: $200K at $4M cap, $100K at $6M cap 15% discount, $150K MFN. We're pricing a round at $10M pre-money with 9M pre-money FD shares. Calculate conversion prices and resulting shares for each SAFE."

**409A prep:**
> "Prepare the inputs list for our 409A valuation. Last priced round: $2M seed at $8M pre-money, closed January 2025. Current ARR: $180K. Cash: 18 months runway. Provide the document checklist and financial data template."
