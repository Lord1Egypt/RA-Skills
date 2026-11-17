# First-Aid Kit Auditor

**Is your first-aid kit actually adequate — for YOUR household?**

Almost no household kit is. The typical box is a decade old: hardened tape, expired children's
syrup, no burn dressing. And "what should be in it" isn't generic — it depends on who's in the
house: infants need weight-dosed syrups, an allergy household needs an epinephrine plan, hikers
need trauma capability, pet owners need a muzzle and vet wrap.

## What it does

- **Profiles your household** — people, kids, pets, adventure level, chronic conditions.
- **Audits inventory** against a 46-item evidence-based catalog (ANSI Z308.1 + Red Cross
  extended) with quantities scaled to headcount.
- **Flags expired and soon-expiring meds** — children's syrups and sterile items expire fastest.
- **Computes coverage %** and a plain verdict (READY / ADEQUATE / THIN / CRITICAL).
- **Emits a prioritized shopping list** — expired first, then missing core, then low stock.

## Quick start

```bash
python3 scripts/first_aid_auditor.py init --people 4 --kids 2 --pets 1 --adventure medium --conditions allergy
python3 scripts/first_aid_auditor.py add --item "adhesive bandages (assorted)" --qty 50 --expires 2027-06-01
python3 scripts/first_aid_auditor.py audit
python3 scripts/first_aid_auditor.py shop
```

## Real-world problem it solves

A family of four with two kids, a dog, and camping trips does a first-aid "check" and finds
band-aids and a 2025-expired children's Tylenol. Generic store checklists tell them nothing
about *their* gaps. Ten minutes with this tool shows: 7% coverage, one expired syrup, and the
two moves that actually matter — fresh fever syrup and an epinephrine conversation with the
pediatrician — plus a pharmacy-run list for everything else.

## Scope & limits

A stocking aid, not medical advice; Rx items (epinephrine, inhalers) require a clinician. In an
emergency call local emergency services first. Pure Python 3 stdlib — no dependencies. MIT license.
