# Cat Litter Box Doctor

House-soiling is a **leading cause of cat surrender to shelters** — and most cases are solvable without a behaviorist. What kills cats is wrong order of operations: owners try "behavior" fixes while a painful bladder (cystitis, crystals, constipation, arthritis) teaches the cat to blame the box. And a blocked male cat is a die-in-24-hours emergency, not a litter-brand problem.

This skill encodes the veterinary-consensus ladder as a working instrument:

1. **Red-flag emergency screen** — straining with no urine / bloody urine → ER NOW, stop triage
2. **Medical-first screen** — 7 signals (PU/PD, straining, weight loss, arthritis…) → vet before behavior, always
3. **Marking vs toileting fork** — spraying (vertical, small, anxiety-territory) vs box rejection (beside-box, soft surfaces); each fork gets its own plan
4. **Box-management audit** — cats+1 rule, scoop cadence, hood traps, appliance-zone locations, senior low-entry doctrine
5. **7-day litter transition** — 75/50/25/0 stages with a fallback box; rollback triggers named
6. **Decontamination protocol** — why ammonia cleaners *re-invite* the cat (uric-acid crystals persist for years; enzymes are the only class that removes the signal), blacklight site-maps, never-steam-before-enzymatic

## Real problem it solves
A cat that suddenly stops using the box triggers a spiral: punishment (worsens it), hood-closing (worsens it), ammonia mopping (re-marks the spot), surrender. The ladder resolves the majority at steps 1–3 — a urinalysis plus four free management fixes — and tells you exactly when it's an emergency instead.

## Quick start
```bash
python3 scripts/litter_doctor.py diagnose     # interactive 4-step ladder
python3 scripts/litter_doctor.py boxes --cats 2 --boxes 1 --hooded yes \
    --location "laundry room (washer spin)" --scooped weekly
# -> 3 management failures — fix ALL before any behavior conclusion
python3 scripts/litter_doctor.py transition --from clay --to wood-pellet
python3 scripts/litter_doctor.py decon --surface "fabric couch" --severity set-in
```

## Contents
- `SKILL.md` — diagnosis ladder, box-audit rules table, decontamination chemistry, pitfalls
- `references/elimination-rules-and-protocols.md` — medical differentials, AAFP/Ohio-State doctrine, spraying-vs-toileting table, follow-up escalation ladder
- `scripts/litter_doctor.py` — stdlib-only CLI (diagnose / boxes / transition / decon)

Not a substitute for urinalysis or an emergency vet visit — the tool itself tells you when to stop and go.

## License
MIT
