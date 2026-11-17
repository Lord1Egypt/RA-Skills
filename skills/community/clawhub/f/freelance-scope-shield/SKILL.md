---
name: freelance-scope-shield
description: Use when a freelance client keeps adding "just one small thing" and the project has quietly doubled — formal scope registry with change-order math (impact hours × blended rate), creep pattern detector (who asks, what type, which requests become disputes), auto-generated polite decline/counter letters, and contract clauses that prevent the next creep.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [freelancing, scope-creep, change-orders, contracts, client-management, consulting]
---

# Freelance Scope Shield

## Overview

Scope creep is the #1 margin killer in freelance and consulting work. The
pattern is always the same: a "small favor" in week 2, another in week 4,
and by delivery the client is receiving 170% of what was priced — at 100%
of the price. The freelancer knew it was happening and couldn't object
without sounding hostile, because **nothing formal existed to point at**.

This skill creates the formal thing:

1. **Scope registry** — every deliverable of the engagement as structured
   data: what's IN, what's explicitly OUT, price, and the hourly rate
   implied by the original agreement.
2. **Request classifier** — each incoming client request is scored:
   IN-SCOPE (already paid for), OUT-OF-SCOPE (new work → change order),
   or AMBIGUOUS (boundary case → clarify in writing before touching).
3. **Change-order math** — impact hours × blended rate × risk multiplier
   (changes late in a project cost more — schedule compression, rework,
   context switching), producing a fair price for "just one small thing".
4. **Creep pattern detector** — over the engagement: who asks, what types
   of requests, what share become disputes, and a creep velocity metric
   (added hours per week) that tells you when a client is unprofitable.
5. **Letter generator** — polite, professional decline/counter letters
   that cite the registry and offer a path forward. The machine is the
   bad cop so you can stay the good cop.
6. **Contract clauses** — the six clauses that prevent the next creep
   (change-order procedure, acceptance windows, revision caps...).

## When to Use

- "The client asked for X — is that in scope?" → classify, then decide
- Drafting a change order with defensible pricing
- Client pushing back on a change-order price → the letter cites math
- Engagement retro: was this client profitable? What request types crept?
- Writing your next contract with anti-creep clauses

**Don't use for:** employment disputes (different law), fixed-price
catastrophes already in legal territory, or estimating new projects
(that's pre-scope — this skill manages an agreed scope).

## Quick Start

```bash
# 1. Register the agreed scope (the contract's deliverable list)
python3 scripts/scope.py init --project "Acme website" --rate 65 --currency USD
python3 scripts/scope.py deliverable --project . --name "5-page website" \
    --hours 40 --included
python3 scripts/scope.py deliverable --project . --name "logo design" \
    --hours 0 --excluded --note "explicitly out per contract §2"

# 2. Classify a client request
python3 scripts/scope.py classify --project . \
    --request "add a blog section to the site" --title "Blog section" --hours 8

# 3. Price it as a change order (late-project risk multiplier)
python3 scripts/scope.py changeorder --project . --title "Blog section" \
    --hours 8 --at-week 6

# 4. Record what actually happened (feeds the pattern detector)
python3 scripts/scope.py record --project . --title "Blog section" \
    --hours 8 --status disputed

# 5. See the creep pattern
python3 scripts/scope.py pattern --project .

# 6. Generate the letter (decline / counter / escalate)
python3 scripts/scope.py letter --project . --title "Blog section" \
    --mode counter --out letter.md
```

## How Classification Works

A request is classified by explicit matching against the registry:
- **IN-SCOPE** — matches a deliverable flagged `included` (the client
  already paid; do it, log it against that deliverable's hours)
- **OUT-OF-SCOPE** — matches an `excluded` entry or no entry (new work:
  change order required before work starts)
- **AMBIGUOUS** — partially overlaps an included deliverable; the tool
  drafts a one-paragraph clarification request, because ambiguity
  resolved verbally becomes tomorrow's dispute

No AI classification — the registry is explicit, so decisions are
checkable by both sides. That's the point: it converts a social
confrontation into arithmetic.

## Change-Order Pricing

```
price = hours × rate × risk_multiplier(week)
risk_multiplier: week 1-2 → 1.0    (cheap to change early)
                 week 3-5 → 1.15   (rework + context switch)
                 week 6+  → 1.3    (schedule compression)
                 post-delivery → 1.5 (new engagement terms)
```

The multipliers aren't punishment — they're what the change actually
costs: late changes force rework of finished work, break concentration,
and compress testing. Publishing this formula in your proposal is the
single most effective anti-creep move (see contract clauses).

## The Letters

Three modes, always citing the registry:
- **decline** — "outside our agreed scope (§ registry), happy to quote
  as a separate engagement"
- **counter** — "outside scope; here's the change order at $X (math
  attached); approve and I start Monday"
- **escalate** — for the 3rd+ unpaid out-of-scope request: restates the
  boundary, lists the accumulated goodwill work, and asks for a
  scope-realignment conversation

Tone rule baked into templates: warm to the person, firm on the scope.
The relationship stays human; the boundary stays mechanical.

## Common Pitfalls

1. **Not writing down what's OUT.** An "included" list without an
   "excluded" list is half a contract. Explicitly excluded items
   (revisions beyond 2, third-party costs, content writing) are what
   make classification defensible.
2. **Doing the ambiguous favor "just this once".** Every undocumented
   favor rewrites the de-facto scope. Classify first, even when the
   answer will be yes.
3. **Pricing changes at the original rate late in the project.** Late
   changes cost more than early ones; charging the same flat rate
   subsidizes the client's indecision.
4. **Skipping `record`.** The pattern detector only works on logged
   requests. A creep pattern you can't show is a pattern you can't
   negotiate with (or a client you can't fire).
5. **Using the letter as a weapon.** The letters are polite by design;
   if you're angry, draft, sleep, then send. The tool is the bad cop.

## Verification Checklist

- [ ] Registry has explicit included AND excluded entries before work starts
- [ ] Every client request gets classified before it gets worked
- [ ] Change orders priced with the week-based risk multiplier
- [ ] All requests (even declined) recorded for the pattern view
- [ ] Letters cite the registry, not feelings

## One-Shot Recipes

**The 6th "small favor":**
```bash
scope.py classify --project . --request "add contact form" --hours 3
scope.py changeorder --project . --title "Contact form" --hours 3 --at-week 7
scope.py letter --project . --title "Contact form" --mode counter --out l.md
```

**Engagement retro before renewal:**
```bash
scope.py pattern --project .
# creep velocity > 15% of contracted hours/week → reprice or decline renewal
```

**Next contract:**
```bash
scope.py clauses
```
