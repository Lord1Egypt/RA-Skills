---
name: fence-line-negotiator
description: "Use when a fence with a neighbor is planned, damaged, disputed, or being replaced — determines boundary responsibility, applies state cost-sharing doctrines (good-neighbor fence laws), prices fair shares, drafts the statutory notice letter, and de-escalates line/side/maintenance disputes before they become lawyer bills."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [fence, boundary, neighbors, property, dispute, diy]
---

# Fence Line Negotiator

## Overview

Fences are the #1 trigger of neighbor legal disputes. Not because fences are complicated — because three questions get answered by assumption instead of evidence: **Whose line is it on? Who pays? Whose problem is the broken panel?** When the assumptions differ, a $2,000 fence becomes a $12,000 feud.

This skill answers the three questions with law and math instead of vibes:

1. **Line**: is the fence ON the boundary, and does it even matter here? (It matters enormously — cost-sharing duties, repair responsibility, and even ownership of the fence itself turn on feet and inches.)
2. **Money**: most US states put boundary-fence cost on BOTH owners ("partition fence" / good-neighbor doctrine), several put it on whoever builds, and a few leave it entirely to handshake. The script prices fair shares and buyouts.
3. **Peace**: statutory notice letters (required before invoking shared-cost law in several states), damage-responsibility routing (storm vs tree vs neglect), and a de-escalation ladder with the exact words to use.

Includes the adverse-possession trap (why mowing 5 feet past the fence for 20 years can quietly transfer land) and the "spite fence" line you must not cross.

## When to Use

- Planning a new fence on or near a shared line (BEFORE ordering materials)
- A shared fence is damaged (storm, tree, rot) and "who pays" is unclear
- Neighbor started building on a fence line without discussing cost
- Disputes over fence side, height, maintenance, or replacement materials
- You suspect the existing fence is NOT on the legal boundary
- Selling/buying and a fence encroachment surfaced in survey

Don't use for: HOA architectural-control approvals (read your CC&Rs — they can override), pool-code barriers (safety regs, separate track), or full boundary litigation (this routes AVOIDANCE, not lawsuits).

## The Three Questions

### 1. Whose line? (get this right first)

- **Get the plat/survey, not the assumption.** Fences drift: built by a long-gone owner, off by inches or feet. County GIS/plat maps are free online in most US counties; a boundary survey is $500-1,500 and is the only binding answer when it's close.
- **Fence ON the boundary** → shared-cost doctrines apply (state law, below).
- **Fence fully on ONE side** → that owner owns it entirely; the other owner has no duty to pay and no right to alter it — but CAN usually attach nothing without permission (the "good side" faces whoever paid, by custom and some codes).
- **Encroaching** → fix it before it ages in: see Adverse Possession trap.
- **Agreement beats stakes**: a signed 1-page "boundary maintenance agreement" (both owners, line description, cost split) recorded with the county ends future ambiguity for the price of a notary.

### 2. Who pays? (state doctrine map)

| Doctrine | Rule of thumb | Example states |
|---|---|---|
| **Good-neighbor / partition fence statutes** | BOTH owners share reasonable cost of boundary fence (equitable share), usually after written notice | CA (Civ. Code 841 — notice letter REQUIRED), and ~20+ states with partition-fence statutes, many rooted in agricultural law |
| **Common-law "fence built by me is mine"** | No automatic sharing for residential fences; contribution only by agreement | Most non-statute states (TX, FL common interpretation) |
| **Local fence-viewer / line-fence ordinances** | Township/county officials assign shares (mostly rural/Midwest) | WI, MI, OH townships |

Two practical universals:
- **A signed agreement beats any default** — even in sharing states, you must give NOTICE first (CA 841 requires a 30-day written notice with the cost-sharing proposal before costs are owed).
- **"Reasonable cost" sharing ≠ top-spec fence sharing.** If you want cedar+black-iron and neighbor agrees to pressure-treated pine, share the pine cost; the upgrade delta is yours. The script splits exactly this way.

### 3. Who fixes the broken one?

| Cause | Responsibility pattern |
|---|---|
| Storm/wind (act of god) | Each own side doctrine varies; sharing states → shared repair; otherwise owner of record |
| Neighbor's tree fell on it | Tree owner pays (negligence if tree was visibly dead — document with photos BEFORE removal) |
| Rot/neglect (age) | Owner(s) of the fence by line/ownership; shared if boundary |
| You/kids/guests broke it | You pay, obviously — offer before being asked |
| Neighbor's contractor damaged it | Contractor's liability; get the company name same-day |

## The Notice Letter (sharing states)

Before any shared-cost claim, send (certified mail + email): both addresses, the fence's location/length, the proposed work with 2 quotes, each share, the timeline, and a response deadline (14-30 days). Offer to discuss adjustments. Keep tone factual; this letter is Exhibit A if it ever escalates — write it like a judge will read it, because one might.

## Using the Script

```bash
# Price a shared fence: 160 ft, $28/ft installed, neighbor wants premium
python3 fence_deal.py cost --length 160 --price-base 28 --price-upgrade 41 --share 0.5

# Damage responsibility router
python3 fence_deal.py damage --cause "neighbor tree fell" --boundary yes

# Draft the cost-sharing notice letter
python3 fence_deal.py notice --length 160 --cost 4480 --share 0.5 \
    --neighbor "J. Alvarez, 14 Maple St" --deadline 21

# Dispute de-escalation ladder for a specific conflict
python3 fence_deal.py ladder --issue "neighbor says fence is 2ft onto his land"
```

`cost` splits base cost fairly and prices the upgrade delta to whoever wants it. `notice` produces the ready-to-send statutory-style letter. `ladder` prints the 5-rung escalation with what to do/say at each rung and when to stop.

## The Adverse Possession Trap (both directions)

- **You mow/landscape past the fence for years**: in many states (periods 5-20 yrs, e.g., TX 10, CA 5 with taxes) a neighbor can claim your side-strip or you can accidentally claim theirs — it needs hostile+open+continuous use. Marked boundary + occasional written permission ("you may keep using that strip") defeats hostile element and protects owners.
- **Fence encroaching for decades** can transfer the strip at sale time — surveys before buying are cheaper than litigation after.
- Fix: locate line, then either move the fence, sign a boundary agreement, or grant written revocable permission (kills the "hostile" element).

## Spite Fence Line

A fence built substantially taller than norms DELIBERATELY to annoy a neighbor is actionable as a private nuisance in most states ("spite fence" doctrine, e.g., CA CC 841.4). Build for privacy/function, not punishment: 6 ft is the near-universal residential back-yard norm (front yards often 3.5-4 ft — check local height ordinance before ANY build; permits are usually required above 6-7 ft).

## Common Pitfalls

1. **Building first, discussing never.** On a boundary, unilaterally building then billing the neighbor fails in most states without PRIOR notice — send the letter first.
2. **Assuming the fence marks the line.** Old fences drift; get the plat/GIS before anchoring posts. Moving a fence later costs 2×.
3. **The "good side" fight.** Many codes now require finished side out (to neighbors or street). If not codified, custom alternates or faces the payer. Settle it in the agreement sentence, not after framing.
4. **Sharing top-spec unequally.** Share the baseline; the premium payer owns the premium. Anything else breeds resentment arithmetic.
5. **Verbal cost agreements.** "He said he'd chip in" doesn't survive a changed mind or a house sale. One page, signed, both owners, filed.
6. **Escalating past the ladder.** Surveyor → letter → mediation (many counties offer free/dispute-resolution) → attorney demand. Skipping to lawyers first hardens positions and costs more than most fences.
7. **Tearing out a disputed fence "because it's mine".** If ownership is contested, removal can convert a dispute into damages liability. Freeze, document, route the ladder.
8. **Ignoring local height/setback permits.** A $9,000 non-compliant fence can be ordered altered or removed; the ordinance office call takes 10 minutes.

## Verification Checklist

- [ ] Line established: plat/GIS checked or survey ordered BEFORE build/repair commitments
- [ ] State doctrine class known (sharing-statute / agreement / fence-viewer)
- [ ] If sharing: statutory-style notice letter sent with quotes and deadline BEFORE costs incurred
- [ ] Cost split = baseline shared, upgrades to the wanter; put in one signed page
- [ ] Damage cause documented with photos same-day; responsibility routed per cause table
- [ ] Height/setback/permit rules verified locally
- [ ] Any encroachment addressed in writing (boundary agreement or permission letter), not silence
- [ ] Escalation stopped at mediation unless safety/structure demands more
