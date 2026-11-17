# Clause Guide — What Each Detector Means and Why It Matters

This guide documents every red-flag pattern the scanner looks for, the real-world
harm each clause causes, and what a fairer alternative looks like. Use it to
interpret findings and to draft counter-proposals.

## Severity Model

| Severity | Meaning | Weight |
|---|---|---|
| HIGH | Can trap you in the contract, waive fundamental rights, or cost months of payments | 10 |
| MEDIUM | Materially one-sided economics or friction; negotiate before signing | 4 |
| LOW | Worth knowing; usually negotiable with one sentence | 1 |

Scrutiny score = min(sum(weights) × 2, 100). 0–19 = ordinary contract; 20–39 =
read carefully; 40–59 = negotiate; 60+ = targeted lawyer review recommended.

## Renewal & Exit Traps

### AUTO-RENEWAL WITH STRICT NOTICE WINDOW (HIGH)
The contract continues for a full new term unless you send written notice inside
a narrow window (typically 30–90 days before term end). Harm: miss the window by
one day → locked for another year (lease) or another 12 billing cycles
(subscription). Fair version: converts to month-to-month after the initial term,
or 30-day notice any time before term end, accepted by email.

### EARLY TERMINATION — RENT ACCELERATION (HIGH)
"All remaining rent becomes immediately due" on breach or early exit. Harm: a
2-year lease broken in month 3 can demand 21 months of rent at once. Many US
states require the landlord to mitigate (re-rent) and treat acceleration as an
unenforceable penalty — but only if you know to argue it. Fair version: exposure
capped at a defined fee (commonly 1–2 months) or rent until re-rental, whichever
is less.

### SUBSCRIPTION CANCELLATION FRICTION (MEDIUM)
Cancellation only by certified mail ≥ 30 days before renewal, with a fee. Harm:
the gym-membership pattern — you pay for months you believed were cancelled.
Fair version: cancel online, effective at end of current period, no fee after an
initial term.

### AUTOMATIC BILLING / STORED PAYMENT (LOW)
Recurring charges to a stored card until cancelled. Not harmful alone, but it is
the enforcement mechanism for every fee clause. Calendar the renewal window the
day you sign.

## Rights Waivers

### BINDING ARBITRATION / CLASS-ACTION WAIVER (HIGH)
Disputes go to a private arbitrator; you waive class actions (often also a jury).
Harm: arbitration filing fees can exceed the disputed amount, killing small
claims individually; class waivers eliminate the only economical remedy for
widely-spread small harms. Note: some jurisdictions prohibit mandatory
arbitration in consumer/employment contracts, and some contracts include an
opt-out window (often 30 days) — read for it. Fair version: small-claims court
carve-out, mutual arbitrator selection, or strike entirely.

### JURY TRIAL WAIVER (HIGH)
Separate from arbitration: even in court, no jury. Often paired with arbitration
so that if one falls, the other still limits you.

## One-Sided Economics

### LATE FEE — FLAT PLUS DAILY ACCRETION (MEDIUM)
Flat fee + per-day charge + monthly-percentage interest compound from a single
late payment. Many states cap late fees (e.g., flat reasonable fee, no daily
accrual) — check yours. Fair version: 5-day grace, flat fee, hard cap.

### ONE-SIDED INDEMNIFICATION (MEDIUM)
You cover their losses/legal costs even for harms they partly caused. Fair
version: mutual indemnity limited to third-party claims arising from each
party's own negligence.

### LIABILITY CAP / DAMAGES WAIVER (MEDIUM)
Their liability capped (often "fees paid in 12 months") while yours is unlimited
via the indemnity clause. Read the two clauses together — the asymmetry is the
point.

### ONE-SIDED ATTORNEY FEES (MEDIUM)
Fees awarded only to the landlord/company regardless of who wins. Fair version:
"prevailing party" recovers fees — this cuts both ways and keeps disputes honest.

### LIQUIDATED DAMAGES FORFEITURE (MEDIUM)
A fixed forfeiture "and not a penalty" — drafted that way because penalties are
unenforceable. Courts sometimes disagree when the figure wildly exceeds actual
damages.

## Scope Creep

### NON-COMPETE / NON-SOLICIT (HIGH)
Post-contract restrictions on working or soliciting. Several jurisdictions now
ban or sharply limit employee non-competes; scope/geography/duration determine
enforceability. Fair version: 12 months, direct competitors, defined radius — or
nothing.

### BROAD IP ASSIGNMENT (MEDIUM)
Standard for employees; dangerous for contractors when it sweeps "all IP
conceived during the engagement," capturing unrelated side projects. Fair
version: assignment limited to work product for this client; pre-existing IP
listed in an exhibit.

### UNILATERAL AMENDMENT (HIGH)
"We may change these terms at any time" + "continued use constitutes
acceptance." Harm: the deal you signed can be rewritten. Fair version: material
changes require consent or 30-day notice with penalty-free cancellation.

### NON-DISPARAGEMENT (LOW)
Gags negative statements indefinitely. Has been found unenforceable in some
consumer/employment contexts; don't rely on it.

## Operational

### ENTRY WITHOUT NOTICE (MEDIUM)
Access to premises "at any time" / "sole discretion." Most states imply
reasonable notice (24–48h) except emergencies — but only a written notice term
is easy to enforce. Fair version: 24-hour written notice; emergency = fire,
flood, gas.

### AS-IS CONDITION (MEDIUM)
You accept the property as found and waive reliance on verbal promises. Any
promise that matters must be written into the contract or an addendum that
survives the as-is clause.

### GOVERNING LAW / VENUE FAR FROM YOU (LOW)
Disputes in their state. For consumer contracts this usually makes enforcement
impractical both ways — but it's their waiver, not yours.

### ASSIGNMENT WITHOUT CONSENT (LOW)
They can transfer your contract to anyone (collections firm, new property
manager); you usually can't. Fair version: consent not to be unreasonably
withheld, both directions.

## Missing-Protection Checklists

Absence of a protective clause is often worse than a present-but-imperfect one,
because it leaves the default rules — which the drafter counted on.

**Lease should contain:** repair/habitability obligation; deposit return
deadline (N days); entry notice requirement; grace period before late fees.

**Employment should contain:** termination notice or severance terms; final
paycheck timing; title/duties definition.

**ToS should contain:** data export/deletion on account closure; availability or
refund commitment; notice before material changes.

**Subscription should contain:** explicit cancellation method; refund/proration
policy.

## Legal Disclaimer

This scanner is pattern-based triage, not legal advice. False negatives are
possible (novel phrasings evade regexes) and false positives happen (a matched
pattern may be benign in context). A clean scan is not clearance. For HIGH
findings, contracts over life-changing amounts, or anything already in dispute,
consult a licensed attorney in your jurisdiction.
