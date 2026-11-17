# Scope Creep Management — The Full Method

## The economics of creep

A fixed-price project priced at $4,000 for 60 hours assumes $67/h blended.
If 20 creep hours get added "for free", the effective rate drops to $50/h
— a 25% pay cut taken in the least visible way possible. Across a
portfolio, unmanaged creep is the difference between a profitable year
and a burned-out one.

Creep is rarely malicious. Clients genuinely don't see the boundary
because **nobody wrote it down**. The fix is a registry both sides can
read, not vigilance.

## The registry

Structure per deliverable:
- name, included/excluded flag, hours budgeted, notes
- the implied hourly rate: total price / total included hours

The registry is derived from the contract/ proposal but sharper: contracts
say "5-page website"; the registry says "5 pages, client-provided content,
2 revision rounds, contact form NOT included (see excluded)".

## Classification procedure (per request)

1. Client states request.
2. Match against registry: exact included? → IN-SCOPE. Matches excluded
   or nothing? → OUT-OF-SCOPE. Partial overlap? → AMBIGUOUS.
3. IN-SCOPE: do it, log hours against that deliverable.
4. OUT-OF-SCOPE: change order BEFORE work. No verbal yes.
5. AMBIGUOUS: send written clarification ("to confirm: this includes A,
   excludes B — correct?"). Reply becomes registry evidence.

The clarification letter is the highest-leverage artifact in the whole
method: it converts he-said-she-said into a documented boundary the
client themselves confirmed.

## Change-order pricing rationale

Late changes cost more for mechanical reasons:
- **Rework**: finished, reviewed work gets reopened.
- **Context switching**: re-loading a "closed" mental module costs
  30-60 min per switch (attention residue literature).
- **Schedule compression**: the same fixed deadline + more work = overtime
  or quality cuts, both of which the freelancer absorbs.

Hence the multiplier ladder: 1.0 early, 1.15 mid, 1.3 late, 1.5
post-delivery. Publishing the ladder in the proposal does two things:
makes surcharges feel mechanical rather than punitive, and motivates
clients to consolidate requests early — which is genuinely cheaper for
everyone.

## Creep pattern metrics

Track per request: date, requester, type (new feature / revision /
expansion / format-change / deadline-shift), hours, status
(approved/declined/disputed/waived-goodwill).

Derived metrics:
- **Creep velocity** = added (approved + goodwill) hours / weeks elapsed
- **Creep ratio** = added hours / contracted hours (>30% = the estimate
  was wrong or the client is unpriceable)
- **Dispute rate** by request type and requester — reveals whether the
  problem is one person, one category, or the engagement structure
- **Goodwill ledger** = waived hours; show it at renewal ("the $2,400
  included this year") — the strongest repricing argument available

## The six contract clauses

1. **Change-order procedure** — out-of-scope work requires written change
   order with price and schedule impact, signed before work starts.
2. **Definition of deliverable** — page/feature counts, content source,
   revision rounds (2 standard), what "revision" vs "new work" means.
3. **Acceptance window** — delivered work is deemed accepted after N
   business days (5 standard) absent written objections.
4. **Revision cap with overflow rate** — revisions beyond cap billed at
   rate X (make the cap explicit, not infinite).
5. **Client dependency clause** — delays from client inputs (content,
   approvals, access) shift the schedule day-for-day; 2 weeks of client
   silence = project paused clause.
6. **Late-change pricing ladder** — the risk multiplier table, stated in
   the proposal, so change-order prices are pre-agreed mechanics.

## Psychology notes

- Freelancers avoid boundary conversations because they feel like
  conflict. Framing changes everything: "happy to do it — here's the
  change order" is service, not refusal.
- Clients respect documented boundaries MORE, not less — it signals
  process maturity. The clients who rage at a change order were
  unprofitable anyway; the registry finds that out in week 3 instead of
  month 9.
- Never negotiate in the moment. "Let me check the scope registry and
  send you the change order this afternoon" is always available and
  always professional.

## Escalation ladder (when a client disputes every order)

1. Counter letter with math (mode: counter)
2. Scope-realignment call offer — reprice the whole engagement to
   actuals; often the client doesn't realize they've doubled the work
3. Goodwill ledger + renewal terms (mode: escalate)
4. Decline further work / refer out — some clients are structure
   mismatches, not targets for better boundaries
