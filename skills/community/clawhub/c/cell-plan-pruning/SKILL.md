---
name: cell-plan-pruning
description: "Use when reviewing, downgrading, or comparing mobile phone plans and bills — family plans, multiline waste, per-line data reality vs bucket size, add-on insurance, autopay/paperless discounts, or switching carriers / MVNOs. Audits the bill line-by-line and computes annual savings of pruning."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [phone-plans, mvno, carrier, bill-audit, savings]
---

# Cell-Plan Pruning — Phone Bill Audit & Carrier-Switch Math

## Overview

Phone bills inflate silently: a family plan sized for a teenage-streaming era, $15–$25/line
"device protection" on phones worth $150, per-line insurance bought at flagship launch and never
revisited, upgrade fees, and the assumption that switching is a hassle that keeps people paying
$40–$60/line for usage an MVNO would carry at $15–$25.

This skill audits a bill (paste the line items) against **actual usage reality** (per-line data
consumption, phone ages/values), classifies every recurring charge KEEP / DOWNGRADE / DROP /
SWITCH, and computes the honest annual savings of each action — including the switching costs
(taxes/fees differences, eSIM activation, phone-lock status, trade-in treadmill exit).

## When to Use

- "My phone bill is $220/month for 4 lines — is that bad?" (it is)
- Considering MVNO switch (Mint/US Mobile/Tello/Visible/Boost...) vs premium carrier
- Reviewing whether device-protection/insurance lines are worth it on current phone values
- Kids/parents joining or leaving a family plan; a line nobody uses anymore
- Comparing prepaid vs postpaid for the same usage
- Don't use for: phone purchase decisions per se (that's phone-shopping), international roaming
  trips (travel eSIM skill territory), or enterprise/business fleet plans

## Core Knowledge

### 1. The bill anatomy and where the fat is

```
bill = base plan (bucket) + per-line access fees + device protection × N
     + add-ons (cloud, AppleCare-ish, premium visual voicemail) + taxes/fees (~15-25%)
```

Typical fat, in order of size:
1. **Oversized data bucket** — median household usage is well under what people pay for;
   "unlimited" is a comfort purchase for most light users
2. **Insurance on old phones** — $15/mo × 24 mo = $360 + deductible $150–$300 on a phone worth
   $200. Breakeven math almost always says drop after year 2
3. **Per-line access fees on postpaid** — $20–$40/line that MVNOs simply don't charge
4. **The upgrade treadmill** — carrier "free" phones are financed into the plan; leaving means
   paying the balance. Exiting the treadmill is the biggest structural save

### 2. Per-line data reality (the audit's core input)

Pull 3–6 months of per-line usage from the carrier app. Classify each line:
- **Light** (<5 GB/mo): WiFi-heavy, music/podcast user → MVNO pooled or capped plan
- **Medium** (5–15 GB): occasional video, maps → mid-tier MVNO
- **Heavy** (>15 GB consistently): commuter streaming, tethering → unlimited tier justified —
  or premium-deprioritized unlimited (fine for most)

Then compare bucket size vs *sum of actuals + 20% headroom*. Most families find they pay for
2–3× their usage.

### 3. MVNO truth table (US market, typical)

MVNOs ride the same towers (coverage = host network), with trade-offs:
- **Deprioritization** under congestion (rarely noticeable outside stadiums/airports)
- **Hotspot caps** (often 5–10 GB even on "unlimited")
- **No roaming fanciness**, weaker international rates (usually)
- **Fewer perks** (no "free" streaming bundles)
- Phone must be **carrier-unlocked & paid off**; eSIM makes switching same-day

| Usage class | Premium postpaid | MVNO typical | Annual delta |
|---|---|---|---|
| Light line | $55–$75 | $15–$25 | **$360–$600/line** |
| Medium line | $65–$85 | $25–$40 | $300–$600 |
| Heavy line | $75–$95 | $40–$55 | $240–$480 |

### 4. Device protection decision rule

```
keep if: monthly×18 + deductible < 40% of current replacement value
drop if: phone age > 24 mo or replacement value < $400
alternative: self-insure (put the premium in a jar) after year 2
```

The script computes this per line from phone age + model value.

### 5. Switching friction checklist

- Phones unlocked + installment balances paid (or accept payoff)
- Number porting: do NOT cancel first — port-out cancels the line automatically; get the
  account number + PIN/transfer PIN (postpaid likes to hide these)
- eSIM: activation minutes, not days; physical SIM fallback
- Taxes/fees differ by plan type — compare *all-in* prices (script takes tax % for both)
- Watch promo credits: "30 bill credits" — leaving early claws them back

## Workflow

1. **Collect the bill**: every recurring line + amounts, number of lines, per-line usage
   (3–6 mo average), phone ages + rough resale values, current insurance cost/line.
2. **Audit:**
   ```bash
   python3 scripts/plan_pruner.py --demo
   python3 scripts/plan_pruner.py --bill bill.json      # your data, see bill.example.json
   ```
3. **Read verdicts** per line-item and per phone-line: KEEP/DOWNGRADE/DROP/SWITCH with $/yr each.
4. **Sanity-gate before switching**: coverage on the target MVNO's host network where you live
   (coverage map + a friend's phone test), hotspot caps OK for your use, phone unlocked.
5. **Execute pruning in order** (no-switch steps first): drop insurance on old phones, remove
   add-ons, downgrade bucket, then the MVNO decision as the last move.
6. **Port correctly**: new carrier initiates the port with account # + transfer PIN; lines
   port one at a time if family members want to stagger.

## Common Pitfalls

1. **Comparing sticker prices, not all-in.** Postpaid "unlimited $65" is $78+ after taxes/fees;
   some prepaid prices are tax-inclusive. Always compare final monthly totals.
2. **Keeping insurance by inertia.** The premium+deductible on a 2.5-year-old phone exceeds its
   replacement value within 18 months. The script flags this per line.
3. **Ignoring installment-lock reality.** "0% financing" with 20 remaining months = you owe it at
   port-out. Promo credits cancel too. Compute the exit cost before declaring savings.
4. **Dropping the whole family to a 2 GB shared plan** because averages looked small — one
   heavy line ruins it. Prune per-line, not per-family.
5. **Porting wrong**: canceling the old line first kills the number. The NEW carrier's port
   process does the canceling.
6. **Chasing a promo price with a 3-month teaser that reverts.** MVNO pricing is often flat;
   premium-carrier promos are often time-boxed credits. Model the steady state.

## Verification Checklist

- [ ] Every recurring bill line classified KEEP / DOWNGRADE / DROP / SWITCH with $/yr
- [ ] Per-line data usage tabulated (3–6 month average, not one month)
- [ ] Bucket vs actual usage gap computed (×2/×3 oversize flag)
- [ ] Insurance breakeven computed per phone (age + value vs premium + deductible)
- [ ] Exit costs included in the switch math (installment balances, lost promo credits)
- [ ] Target network coverage verified where the user lives/works
- [ ] Annual savings total stated as the sum of independently-executable actions

## One-Shot Recipe: 4-line family at $327/mo all-in

Lines: 2 adults (8–12 GB), 1 teen (26 GB), 1 grandparent (1.5 GB). Bill: unlimited premium ×4,
insurance on 2 phones ($17/ea), $10 cloud + $5 voicemail add-ons. Audit: grandparent → LIGHT
capped MVNO line (~$25 all-in, −$355/yr), adults → MEDIUM mid-tier (−$494/ea), teen → HEAVY
unlimited is justified but an MVNO unlimited tier carries it (−$302); insurance: both phones
fail the 40%-of-value breakeven (18-mo premium+deductible $506 vs values $320/$900) → DROP
(−$481); add-ons → free-tier equivalents (−$212). Result: $327 → ~$132/mo ≈ **$2,338/yr saved**
with zero behavior change and the same towers.
