---
name: first-aid-kit-auditor
description: "Use when building, restocking, or auditing a home/car/travel first-aid kit — profiles the household (kids, pets, allergies, adventure level), checks the inventory against a 46-item evidence-based catalog, flags expired meds, computes coverage %, and emits a prioritized shopping list."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [first-aid, emergency-preparedness, home-safety, inventory, expiry]
---

# First-Aid Kit Auditor

## Overview
Every household has a first-aid kit; almost none are adequate. The typical kit is a decade-old
box with hardened bandage tape, one expired children's fever syrup, and no burn dressing. The
problem is that "what should be in a first-aid kit" is a moving target that depends on **who**
is in the house: infants need weight-dosed syrups, an allergy household needs an epinephrine
plan, hikers need trauma capability, pet owners need a muzzle and vet wrap. Store checklists are
generic; this tool makes it personal and keeps it current with expiry tracking.

The auditor maintains a simple JSON registry of what you own. `audit` compares it against a
catalog calibrated to your household profile and outputs: coverage %, expired items, expiring
soon, missing core items, low stock, and a verdict. `shop` turns the gaps into a prioritized
shopping list.

## When to Use
- "What should I put in a first-aid kit?" (→ init with household profile, then shop)
- "Is my first-aid kit good enough for a family with two kids and a dog?"
- Yearly kit restock / daylight-saving reset ritual.
- After using items (post-incident restock check).
- Building a car kit or hiking/travel kit (adventure profile).
- "My ibuprofen expired 2 years ago — is everything else expired too?" (expiry sweep)

**Don't use for:** actual medical emergencies (call emergency services); prescription planning
(auto-injectors, inhalers need a doctor — the tool flags them as Rx, it does not dose them).

## How It Works — Numbered Steps
1. Init the profile:
   `python3 scripts/first_aid_auditor.py init --people 4 --kids 2 --pets 1 --adventure medium --conditions allergy`
2. Register what you already own, with expiry dates for anything that degrades:
   `python3 scripts/first_aid_auditor.py add --item "adhesive bandages (assorted)" --qty 50 --expires 2027-06-01`
3. Audit:
   `python3 scripts/first_aid_auditor.py audit` → coverage %, expired/expiring, missing, verdict.
4. Shop: `python3 scripts/first_aid_auditor.py shop` → prioritized list (expired first, then
   missing core, then low stock).
5. Re-audit yearly and after every incident that consumed supplies.

## Catalog Logic (what drives requirements)

| Profile input | What it adds |
|---|---|
| `--people N` | scales baseline quantities (calibrated at 4 people) |
| `--kids N` | children's fever/pain syrups, children's antihistamine, temple thermometer |
| `--pets N` | vet wrap, styptic powder, muzzle/soft cone, vet-dosed antihistamine |
| `--adventure medium/high` | trauma layer: SAM splint, hemostatic gauze, tourniquet, CPR mask, triangle sling |
| `--conditions allergy/asthma/diabetes` | Rx items flagged (epinephrine auto-injector, inhaler, glucose gel) |

Expiry: meds and sterile items get expiry dates on `add`; anything within 180 days is flagged
"expiring", past date is EXPIRED and lands at the top of the shopping list.

## Common Pitfalls
1. **No children's formulations when kids are present.** Adult pills can't be split for a
   toddler; children's acetaminophen/ibuprofen syrups are non-negotiable and expire fastest.
2. **Storing the kit in the bathroom medicine cabinet.** Humidity and heat degrade meds and
   adhesive; use a sealed box in a cool dry room, above child reach.
3. **Car kits cook.** A kit living in a hot car deades in 1-2 seasons — swap car-kit meds on a
   shorter calendar (spring and fall).
4. **Owning but not knowing.** A kit nobody can find at 2 AM is decorative. One location,
   everyone knows it, labeled.
5. **Tools without training.** A tourniquet or epinephrine auto-injector you've never practiced
   with is a liability; take a first-aid/CPR course (the audit verdict reminds you).
6. **Forgetting the info layer.** Emergency contact card, consent forms for kids' caretakers,
   and a handbook matter as much as gauze.

## Example
```
Family of 4 (kids 3 & 6), a dog, camping trips, one bee-sting allergy.

$ python3 scripts/first_aid_auditor.py init --people 4 --kids 2 --pets 1 \
      --adventure medium --conditions allergy
$ python3 scripts/first_aid_auditor.py add --item "adhesive bandages (assorted)" --qty 50 --expires 2027-06-01
$ python3 scripts/first_aid_auditor.py add --item "children's acetaminophen" --qty 1 --expires 2025-01-01
$ python3 scripts/first_aid_auditor.py audit
Coverage: 7% (3/46)
EXPIRED — replace now:
  ! children's acetaminophen (expired 2025-01-01)
MISSING — core gaps:
  - epinephrine auto-injector (rx)  (medications (allergy profile))
  - children's ibuprofen, burn gel, hemostatic gauze, ...
VERDICT: CRITICAL — this is not a first-aid kit yet.

→ The two moves that matter most: fresh children's fever syrup and an
  epinephrine conversation with the pediatrician. The rest is one pharmacy run.
```

## Safety Note
The catalog follows Red Cross / ANSI Z308.1 minimums extended for household profiles. It is a
stocking aid, not medical advice; Rx items require a clinician. In an emergency, call local
emergency services first.

## References
- `references/catalog-rationale.md` — why each item earns its slot, category by category.
- `references/storage-and-rotation.md` — storage conditions, car-kit heat reality, rotation
  calendar, and the "one box, one place" rule.
