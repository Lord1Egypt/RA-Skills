# Role construction

## The test

Before accepting a role set, check: **can you name a decision where role A wins
only if role B loses?** If not, the roles are cosmetic and the debate will be
theater.

Bad set (no conflict): developer, designer, tester, architect — all want the
same thing, differ only in vocabulary.

Good set (structural conflict): developer wants time, marketer wants launch
date, security wants controls, finance wants it cheap. Every pair has at least
one decision where they cannot both win.

## Role template

```
Role: <profession>
Priority: <the one thing it will not trade away>
Will impose: <cost it forces on others to protect that priority>
Blind spot: <what it systematically underweights>
Opening stance: <a position it holds before hearing anyone else>
```

The opening stance matters — a role that forms its view only after reading the
others will converge with them.

## Prepared sets

### Website / web application
- **Developer** — maintainability; imposes delay; underweights time-to-market;
  opens with "this needs to be built properly or it will be rewritten in a year"
- **Marketer** — launch speed; imposes technical debt; underweights operating
  cost; opens with "a perfect site six months late is worth nothing"
- **Security** — attack surface; imposes friction; underweights usability; opens
  with "assume it will be attacked in week one"
- **Legal/compliance** — documentation and obligations; imposes paperwork;
  underweights whether anyone will read it; opens with "unregistered data
  processing is a fine, not a detail"

### Home renovation / construction
- **Site manager** — schedule and sequencing; imposes standardization
- **Electrician** — code compliance and load; imposes routing constraints
- **Plumber** — access and serviceability; imposes layout constraints
- **Interior designer** — how it looks and lives; imposes cost

### Infrastructure / homelab
- **SRE** — availability and recovery; imposes redundancy cost
- **Security** — isolation and least privilege; imposes operational friction
- **Cost** — bills and power draw; imposes constraints on everything
- **Operator** — will this be maintainable at 2am; imposes simplicity

### Business decision
- **Finance** — cash and margin
- **Operations** — feasibility with current staff
- **Sales** — what the customer will actually pay for
- **Risk** — what happens when it goes wrong

Prepared sets are starting points. Adapt to the specific topic; a generic set
produces a generic report.

---

# Phase templates

## Phase 0 — Role proposal

```
Topic: <restated in one sentence>

Proposed council:

1. <role> — priority: <x> | imposes: <y> | blind spot: <z>
2. ...

Structural conflicts:
- <role A> vs <role B> over <decision>
- <role C> vs <role D> over <decision>

Approve, or tell me which roles to swap.
```

Then stop. Do not proceed without approval.

## Phase 1 — Interview batch

```
Batch <n>/<total> — <theme>

1. <question>
2. ...

Answer what you can. "Don't know" is a valid answer and goes into the report
as a gap.
```

## Phase 3 — Position

```
## <issue> — <role>

Recommendation: <what to do>
Reasoning: <why, from this role's priority>
Cost: <what it costs in time, money, or friction>
If ignored: <what breaks>
Confidence: high | medium | low
```

## Phase 4 — Cross-examination

```
## <role> defends: <issue>

<position summary>

--- Challenges ---
<role B>: <objection>
<role C>: <objection>
<role D>: <objection>

--- Defense ---
<response to each, or explicit concession>

--- Resolution ---
Vote: <n>:<n> (<roles>)
Outcome: upheld | overturned | modified | UNRESOLVED
Reservation: <if a losing role files one>
```

## Phase 5 — Report structure

```markdown
# <Topic>

## Summary
<3-5 sentences. What to do, what it costs, biggest risk.>

## Do this, in this order
1. <action> — <why first>

## Decisions
### <issue>
<conclusion and reasoning, in the user's terms — no role names>

## Unresolved
### <issue>
Position A: <...>
Position B: <...>
Why it matters: <...>
What would settle it: <...>

## Gaps
<questions the user could not answer, and what they block>

## Risks
<what could go wrong, likelihood, mitigation>

## Deliberately out of scope
<what was considered and dropped, and why>
```

The report never mentions roles, votes, or the debate. If a sentence only makes
sense to someone who read the transcript, rewrite it.

---

# Budget accounting

| Phase | Calls |
|---|---|
| 0 — role proposal | 1 |
| 1 — interview questions | 1 |
| 2 — issue assignment | 0 |
| 3 — positions | 4 |
| 4 — cross-examination | 4 |
| 5 — report | 1 |
| **Base** | **11** |
| Reserve for tie-breaks | 4 |
| **Ceiling** | **15** |

Reserve the Phase 5 call before starting Phase 3. The report is the deliverable;
everything else is process. If the budget tightens, cut issues, never the report.
