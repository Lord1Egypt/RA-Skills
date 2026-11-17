# contract-triage-lite

Offline contract risk triage for freelancers — flags IP grabs, uncapped
liability, non-competes and payment traps in an NDA/MSA/SOW. Zero
dependencies, zero network — the contract never leaves your machine.
Node 18+.

**Triage, not legal advice** — it finds what to question before you sign.

## Install

```bash
npx skills add NenadZivotic/lite-agent-skills --skill contract-triage-lite
```

Or clone and point your agent at `contract-triage-lite/SKILL.md`.

## Run

```bash
node scripts/clauses.js contract.txt
```

JSON flags on stdout; exit `1` when risks are found.

## Full version

The full `contract-triage-nda-msa-riREDACTED-SECRET` skill ($29)
checks **all 10 risk categories** (adds termination asymmetry, perpetual
confidentiality, forced arbitration/jurisdiction, auto-renewal lock-ins,
scope-creep, warranty traps), detailed missing-protection analysis, a
severity-ranked report format, plus negotiation email and redline
drafting guidance. Ask for it by slug.
