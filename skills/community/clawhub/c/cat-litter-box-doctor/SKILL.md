---
name: cat-litter-box-doctor
description: Use when a cat pees outside the litter box, refuses the box, or fights housemates over it — veterinary-rule-based diagnosis ladder (medical first), box-count formula cats+1, litter-type transition protocol, location rules, and soiled-area decontamination with the enzyme-vs-ammonia trap.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [cats, litter-box, inappropriate-elimination, pets, behavior]
---

# Cat Litter Box Doctor

## Overview
Inappropriate elimination — peeing or spraying outside the box — is a **leading cause of cat surrender and euthanasia**, and most cases are solvable without a behaviorist. The discipline that saves cats is *order of operations*: **medical causes first** (FLUTD, crystals, UTI, constipation, arthritis — pain gets associated with the box, and a blocked male cat is a hours-to-death emergency), then **box management** (count, cleanliness, litter type, location), then **territory/soiling-conflict** analysis (spraying vs squatting, vertical vs horizontal, marking vs toileting).

This skill encodes the veterinary consensus ladder as an interactive diagnostic: 20 questions with red-flag routing (blocked-cat emergency, hematuria, polyuria/polydipsia cluster), a box-configuration audit against the cats+1 rule and size/hood/entrance doctrine, a 7-day litter-transition protocol (abrupt switches cause refusals), and a decontamination protocol that explains why ammonia-based cleaners *re-invite* the cat back to the same spot.

## When to Use
- Cat suddenly pees/poops outside the box (any age, any duration)
- New cat, new home, renovation, new baby, new pet — and litter habits broke
- Multi-cat tension: blocking, ambushing, box-guarding
- Choosing box setup for a new cat or new home (get it right day one)
- Senior cat stops using the hooded box (arthritis signature)

**Don't use for:** dogs or rabbits (different systems), post-op cats still on meds (follow the surgeon's protocol), or a cat currently straining without producing urine — that is **GO TO THE EMERGENCY VET NOW**, not a diagnostic session (see Red Flags).

## Quick Start
```bash
# Interactive diagnostic (20 questions -> ranked causes + action plan)
python3 scripts/litter_doctor.py diagnose

# Box-setup audit for a 2-cat household, 1 box, hooded, in the laundry room
python3 scripts/litter_doctor.py boxes --cats 2 --boxes 1 --hooded yes \
    --location "laundry room (washer spin)" --scooped weekly

# Transition from clay to wood-pellet litter without a refusal strike
python3 scripts/litter_doctor.py transition --from clay --to wood-pellet --days 7

# The couch corner got hit: clean it so the cat doesn't return
python3 scripts/litter_doctor.py decon --surface "fabric couch" --severity fresh
```

## The Diagnosis Ladder (order is the skill)
1. **MEDICAL FIRST — always.** A cat that "has always used the box" and suddenly stops has a body problem until proven otherwise. Painful urination (FLUTD/cystitis/crystals) makes the cat blame the box; constipation or diarrheal urgency overrides training; arthritis makes high-sided boxes impossible; kidney disease drives volume the box schedule can't absorb. Any sudden change = vet visit before behavior work. Urinalysis + age-appropriate bloodwork resolves the majority of "behavioral" cases.
2. **RED FLAGS = EMERGENCY NOW** (any one):
   - Male cat straining, crying in the box, producing no urine → **urethral obstruction: death in 24–72 h. ER NOW.**
   - Blood in urine (pink/red litter) → same-day vet.
   - Frequent small attempts + licking genitals + hiding → urgent (same 24 h).
   - No urine ≥ 12–18 h in any cat, vomiting + lethargy + no urine → ER.
3. **Box management audit** (the fixable 60%): count (cats + 1), scoop (daily minimum; 2×/day for picky cats), size (1.5× body length; many "XL" boxes aren't), hood/entrance (hood = trap and stink-dome for anxious or ambushed cats; low entry for seniors), location (quiet, escape-routable, never next to the washer spin or the dog's bowl).
4. **Litter substrate**: most cats prefer fine unscented clumping clay; scented litters, pellet swaps, and litter-robot mechanics each cause refusal strikes. Transition over 7 days (25/50/75/100) with a fallback box of the old litter.
5. **Territory & marking**: spraying (vertical surfaces, standing, tail quiver, small amounts) vs toileting (horizontal, squatting, full volumes). Spraying = anxiety/territory response: identify the trigger (outdoor cat at the window, new housemate, renovation noise) and reduce it; feliway-class pheromones and (severe cases) vet-discussed anxiety medication help. Never punish — it raises the anxiety that drives marking.

## Box Audit Rules (what `boxes` encodes)
| Parameter | Rule | Why |
|---|---|---|
| Count | cats + 1 (minimum 2 for 1 cat) | one cat's guard shouldn't lock out another |
| Scoop | daily; box wash weekly (mild soap, no ammonia/bleach perfumes) | cats' nose is 14× human; a "fine" box is a latrine to them |
| Size | ≥1.5× cat nose-to-tail-base | tiny boxes force hanging-out urination |
| Hood | off for anxious/ambushed/senior cats | hood traps odor inside and blocks escape sightlines |
| Liners/deodorizers | skip liners; unscented only | liners tear under claws; perfume = different box |
| Location | quiet, lit at night, two exits' worth of open sightline, away from appliances | ambush fear and washer-spin terror are real |
| Depth | 2–3 in (clumping) | too deep wastes litter; too shallow invites digging out |
| One per social zone in multicat | spread, not clustered in one room | a single room = a single guardable gate |

## Decontamination (why the cat returns to the spot)
Cat urine is urea+uric acid; dried residue re-activates with humidity and *keeps smelling like a toilet to the cat for years*. Ammonia-based cleaners add ammonia — the signature of cat territorial marking — literally advertising the spot; bleach doesn't touch uric acid crystals. The protocol: blot (never rub) fresh urine; rinse; **enzymatic cleaner** (nature's-miracle class) saturated to the same depth the urine reached, kept wet per label, air-dry; repeat once. Carpet = lift and treat pad/underlay; a 2-week-old accident needs a urine-specific blacklight pass to find every crystal site. Untreated sites teach "this room is the latrine".

## Common Pitfalls
1. **Skipping the vet.** Half of "behavioral" eliminators have cystitis, crystals, or constipation. Diagnose the body first.
2. **Punishing or rubbing noses** — increases fear, worsens both spraying and avoidance; the cat learns to hide the behavior, not stop it.
3. **Closing the hood "to contain smell"** for an anxious cat — makes the box a trap; smell containment is a scoop-frequency problem.
4. **N=1 box for 2 cats "because they're siblings"** — resource guarding is about perception of scarcity, not affection.
5. **Aromatic disinfectants in the box** (pine, citrus, ammonia) — box becomes unfamiliar; refusals follow.
6. **Moving the box away from the accident site mid-crisis** without a temporary box AT the preferred site, then gradually moving it 30 cm/day to the destination.

## Verification Checklist
- [ ] Red-flag screen passed (no straining/blood/PU-PD cluster) or ER visited
- [ ] Vet exam + urinalysis done or scheduled for any sudden-change case
- [ ] Box count ≥ cats+1, scooped daily, hood decision per cat temperament
- [ ] Litter unchanged or transitioned 25→100% over 7 days with fallback box
- [ ] Accident sites enzymatically treated (not ammonia/bleach), blacklight pass for old sites
- [ ] 2-week log: accidents declining; if not, escalate per follow-up ladder

## Example Session
```
$ python3 scripts/litter_doctor.py boxes --cats 2 --boxes 1 --hooded yes \
    --location "laundry room (washer spin)" --scooped weekly
BOX AUDIT — 2 cats, 1 box
  [FAIL] count: 1 box for 2 cats (rule: cats+1 = 3)
  [FAIL] hood: hooded box + any ambush/anxiety history = trap; remove or offer
         one open box alongside
  [FAIL] location: appliance noise zone; move to quiet corridor w/ sightline
  [FAIL] scooped weekly: daily minimum, 2x/day during resolution
Verdict: 4/4 management failures — fix ALL before any behavior conclusion.
```
