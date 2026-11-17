---
name: fidacy-crabtrap-verdicts
description: Turn Brex CrabTrap's local audit into portable, signed proof. Use if you already run CrabTrap to watch your agents: this adds an independent Fidacy verdict on top of each local decision, in observe mode, without changing CrabTrap's flow. Your audit stops being something only you can read and becomes something any counterparty can verify.
version: 1.0.0
license: Apache-2.0
---

# Fidacy on CrabTrap, portable verdicts over your local audit

CrabTrap (open-sourced by Brex) makes agent requests auditable inside one
company. The missing piece is the neutral verdict every counterparty can
verify: your own log proves things to you, not to the merchant, the auditor or
the court on the other side. This skill wires the @fidacy/crabtrap adapter in
observe mode: CrabTrap keeps deciding exactly as before, and each decision
additionally receives an independent, Ed25519-signed Fidacy verdict that
travels.

## When to use this skill

You already run CrabTrap (or are evaluating it) and need your agent audit to
hold up outside your own walls: vendor reviews, insurance conversations,
disputes, regulator questions.

## How to use it

1. Install the adapter next to your CrabTrap deployment:
   `npm i @fidacy/crabtrap` (Apache-2.0). You need a free engine API key from
   https://app.fidacy.com/signup (scope assess:write).

2. Point it at CrabTrap's event stream (SSE) and it does the rest: for each
   local decision it requests a signed Fidacy verdict (kind: custom) and logs
   the pair. Observe mode means zero risk: nothing in CrabTrap's enforcement
   path changes.

3. Verify any produced verdict independently with `@fidacy/verify` against the
   public JWKS at https://api.fidacy.com/.well-known/jwks.json, or at
   https://fidacy.com/verify. `signing_valid: true` is the artifact you hand
   the counterparty.

## Why this pairing works

CrabTrap audits a company for itself; Fidacy is the neutral layer that makes
that audit adjudicable by someone who does not trust you. They stack; they
don't compete. Details and the honest comparison:
https://fidacy.com/comparison.
