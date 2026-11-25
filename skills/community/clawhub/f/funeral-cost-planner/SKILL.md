---
name: funeral-cost-planner
description: "Use when planning a funeral or comparing funeral home prices: itemizes GPL quotes against the FTC Funeral Rule, builds trade-off tables (burial vs cremation vs green), catches package-padding and casket markups, and drafts price-match negotiation scripts during the worst week of your life."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [funeral, end-of-life, FTC-funeral-rule, GPL, cremation, burial, cost-defense]
---

# Funeral Cost Planner

## Overview

Funerals are bought in the worst possible state: 48 hours of grief, zero price anchors,
and a seller whose default is a package "because that's what most families choose." The
median US funeral runs **$8,300–$11,000** (burial with vault) — but the same dignity
costs $2,500–$4,000 when itemized and shopped. The **FTC Funeral Rule** gives you rights
most grieving families never hear about: the funeral home MUST give you an itemized
General Price List, MUST sell you a plain casket or urn (they can't refuse one you buy
elsewhere), and CANNOT charge a "casket fee" for using an outside casket.

This skill itemizes quotes, compares them to national/cremation norms, flags the classic
padding patterns, and writes the negotiation scripts — so the decisions get made by
number, not by nodding through a hallway.

## When to Use

- A death has occurred (or is imminent) and arrangements must be made this week
- Comparing 2-3 funeral home GPLs (by law you can collect them by phone — no visit needed)
- Reviewing a prepaid funeral contract / funeral insurance
- "Is this price fair?" on any line item: casket, vault, embalming, viewing
- Planning ahead: own-arrangements spec sheet with inflation assumptions

**Don't use for:** estate/legal execution (see estate-settlement-navigator), or state
variations beyond the US (Funeral Rule is US federal; UK/CA differ — noted in references).

## Your FTC Funeral Rule Rights (the leverage)

1. **General Price List (GPL)** — must be handed to you at arrangement, must itemize.
   Phone requests: must be answered with prices.
2. **Casket/urn price list separately** — and they **cannot refuse or charge a fee** for
   a casket you buy elsewhere (Costco ~$900-2,000, Amazon, online).
3. **No embalming requirement** — refrigeration is the lawful alternative almost
   everywhere; embalming is only required for public open-casket viewing in some states,
   or cross-state transport. Direct cremation/burial never needs it.
4. **No bundled "must-buy" packages** — you may decline any item, including "professional
   services staff." (Watch for "non-declinable basic services fee" — legal, ~$2,000, but
   everything else is à la carte.)
5. **Cash advances at cost** — flowers, obituary, death certificates: must be itemized;
   "handling fees" on them are padding.
6. **Cremation container** — no casket required for cremation; a cardboard/alternative
   container is lawful and often free-loaner.

## Numbered Workflow

1. **Collect the GPLs by phone** (script in references): 3 funeral homes, 6 anchor prices:
   direct cremation, immediate burial, viewing+service, casket 18ga steel, vault, basic
   services fee. Legally they must quote by phone.
2. Enter quotes in `scripts/funeral_compare.py quotes.json` — output:
   - Per-home itemized table vs national median (NFDA 2023-2025 bands)
   - Padding flags: package vs à-la-carte delta, embalming pushed without viewing,
     "required" vault (only cemeteries require vaults, not the law), cash-advance markups
   - Trade-off table: direct cremation / cremation+memorial / burial / green burial
     with real cost ranges
3. Run the casket decision: the $2,400 steel casket vs Costco $1,200 identical-gauge
   item — the script prices the honest alternatives (no casket for cremation, rental
   casket $800-1,200 for viewing+cremation, cloth-covered $1,000 for burial on a budget).
4. Print the negotiation script + rights card (FTC citations to read aloud).
5. If prepaid contract exists: `--prepaid` mode flags the portability/cancel/inflation
   traps (see references).

## Padding Patterns the Script Flags

| Pattern | What it looks like | The counter |
|---|---|---|
| Package padding | "Traditional Package $7,995" bundling embalming+viewing+casket you didn't ask for | Ask for the same items à la carte; require the GPL |
| Embalming default | Charged on cremation "for sanitation" | Not required by law; refrigeration is lawful; refuse the line |
| Grief upcharge | "Memory table," "tribute DVD," custom printing | Decline; DIY for 1/10th the price |
| Cash-advance markup | Obituary $450 "placement service" | Newspapers charge $150-250 direct; place it yourself |
| Vault as "required" | "State law requires a vault" | FALSE in every state; some CEMETERIES require them (private rule, not law) — ask which cemetery rule and whether lower-tier vault passes |
| Outside-casket fee | "Casket handling fee $300" | Illegal under the Funeral Rule — cite 16 CFR 453.4(b)(2) |
| "Low-end casket hidden" | GPL shows caskets from $2,400 | They must show all; ask for the least-expensive options; they cannot require you buy one |

## Pitfalls

1. **Deciding in one room.** The Funeral Rule exists so you can price-shop by phone in
   20 minutes. Get 3 GPLs before signing ANYTHING.
2. **Signing the arrangement form as presented** — it often includes pre-selected
   "traditional" items. Cross out what you decline; initial it.
3. **Paying for embalming with direct cremation** — the most common single padding line
   ($500-800 that buys nothing).
4. **Confusing cemetery rules with law** (vaults, vault liners, grave liners). Cemetery
   requirements are contract terms; ask for theirs in writing and compare their shop too.
5. **Prepaid contract traps** (if reviewing one): non-portable trusts, item locks that
   inflate, "guaranteed price" that excludes cash advances. See references before
   signing anything new.
6. **Upcharges on death certificates** — the state charges $6-25 each; funeral homes may
   only pass through at cost (get 5-10: estates need more than families expect).
7. **Donating body/science or medical school route** ignored — often free (transport
   excepted) with cremated remains returned; check local programs if cost is the barrier.

## Example

```
$ python3 scripts/funeral_compare.py examples/two-homes.json

HOME A (Restlawn): direct cremation $2,395 | basic fee INCLUDED | caskets from $1,895
HOME B (Fairhaven): direct cremation $1,495 | +basic fee $1,950 → real $3,445 (⚠ +$1,300 hidden)
  ⚠ B's "package" quotes only after the non-declinable fee — always ask for the FEE+item total

DIRECT CREMATION (no viewing):
  A: $2,395  |  B: $3,445*  |  national median $2,505 — A is fair, B is padded
  *includes $695 "sanitation/embalming credit" — embalming NOT required for direct cremation: REFUSE

VIEWING + CREMATION (rental casket, one day):
  A: $2,395 + viewing/staff $450 + rental casket $995 = $3,840  ← still beats B's package $4,995

BURIAL compare: A immediate burial $2,895 + cemetery (plot 1,500-4,000 + opening 1,200 + vault 1,400)
  = $7,000-9,500 — the CEMETERY is half the cost, price it separately!

NEGOTIATION: "Per the FTC Funeral Rule I'd like the General Price List, itemized. I'm
  declining embalming (not required for direct cremation). Please show me your
  least-expensive cremation container and confirm no outside-container fee applies."
```

## Verification Checklist

- [ ] 3 GPLs collected (phone is lawful) — itemized, with the basic-services fee TOTAL
- [ ] Embalming charged only where viewing requires it (state law) — otherwise removed
- [ ] Casket decision made against outside-retail prices (Costco/Amazon) and no-fee rule
- [ ] Cemetery costs priced separately (plot, opening/closing, vault/liner, marker)
- [ ] Cash advances verified at pass-through cost (obituary, certificates, flowers)
- [ ] Death certificates ordered generously (5-10)
- [ ] Everything declined is crossed out and initialed on the arrangement form
- [ ] Prepaid contract (if any) reviewed for portability/inflation traps before changes
