# Freelance Scope Shield

**The formal thing to point at when the client asks for "just one small
thing" — again.** A scope registry with explicit IN/OUT deliverables, a
request classifier (in-scope / out-of-scope / ambiguous), change-order
pricing with a late-project risk ladder, a creep-pattern detector, and
polite decline/counter letters that cite the registry instead of your
patience.

## The real-world problem

Scope creep is the #1 margin killer in freelance work. 20 "free" creep
hours on a 60-hour fixed-price project is a 25% pay cut taken invisibly.
It persists because objecting feels like conflict — there's no artifact
both sides can read that says what was agreed. This tool is that
artifact, plus the workflow around it.

## What it does

- **Registry** — deliverables flagged included/excluded with hour budgets
  and the implied blended rate
- **Classifier** — every request matched against the registry:
  IN-SCOPE (do it), OUT-OF-SCOPE (change order first), AMBIGUOUS
  (written clarification first)
- **Change orders** — hours × rate × week-based risk multiplier
  (×1.0 early → ×1.3 week 6+ → ×1.5 post-delivery), with rationale
- **Pattern detector** — creep velocity (h/week), creep ratio vs
  contracted hours, dispute rates, and the goodwill ledger (unbilled
  waived hours in currency — your strongest repricing argument)
- **Letters** — decline / counter / escalate modes, warm to the person,
  firm on the scope, math attached
- **Contract clauses** — the six anti-creep clauses to put in your next
  contract

## Quick start

```bash
python3 scripts/scope.py init --project . --project-name "Acme site" --rate 65
python3 scripts/scope.py deliverable --project . --name "5-page website" --hours 40 --included
python3 scripts/scope.py classify --project . \
    --request "add a blog section" --title "Blog section" --hours 8
python3 scripts/scope.py changeorder --project . --title "Blog section" \
    --hours 8 --at-week 6
python3 scripts/scope.py letter --project . --title "Blog section" \
    --mode counter --client Sarah --out letter.md
```

Stdlib-only Python 3. State in one `scope.json` per project.

## License

MIT © 2026 Denis Voronin
