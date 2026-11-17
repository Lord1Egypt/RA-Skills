# Consumer Complaint Escalation — Reference

## Why complaints fail

Companies process complaints through a cost lens: a complaint is expensive
in proportion to (a) the regulator attention it can attract, (b) the public
review damage it can do, and (c) the staff time it consumes. Consumers fail
when they are cheap to ignore: no written record, no named consequence, no
deadline, no follow-up. The fix is mechanical, not rhetorical.

## The paper trail

Every letter cites the full incident timeline: dated events, amounts,
evidence references. This does two things:

1. It forces the company's reviewer (a person with authority, eventually)
   to confront the record rather than the retelling.
2. It creates the exhibit list a regulator or chargeback dispute will want
   later. The same document serves rung 1 and rung 4.

## Escalation ladder theory

Horizontal escalation (more agents) is a dissipation strategy. Vertical
escalation moves to people whose incentives differ:

- **Supervisors** — measured on resolution time
- **Executives (CEO/exec office email)** — measured on escalation risk and
  brand damage; a well-documented case reaching exec email is often
  resolved in days
- **Regulators** — the company must spend real money responding; even a
  copy-in-cc changes the tone

The ladder's timing matters: each rung must give the previous rung a fair,
documented chance. Arriving at the regulator with a complete written record
("complaint sent day 0, escalated day 7, final notice day 14, no adequate
response") is a strong filing; arriving with a chat scroll is a bounce.

## Regulator routing (built into `regulators`)

| Industry | US | EU/UK | What they actually do |
|---|---|---|---|
| Telecom/broadband | FCC, state PUCs | national regulators (Ofcom UK, BNetzA DE) | fines; enforced resolution programs |
| Airlines | DOT | national CAA + EU261 statutory claims | DOT complaints are answered under statute; EU261 is directly claimable |
| Banking/cards | CFPB, OCC, FDIC | national banks' complaints units (FOS UK) | CFPB filings get company response within 15 days by rule |
| Retail/e-commerce | state AG consumer divisions | ECC (European Consumer Centres) for cross-border | mediation, pattern tracking |
| Utilities | state PUC | national energy regulators | billing dispute freezes |
| Auto (US) | NHTSA (safety) | — | safety complaints trigger investigations |
| Privacy/data | state AGs, FTC | DPAs (GDPR Art.77 right to complain) | GDPR complaints are free and enforceable |

`regulators` prints the ladder for the case's industry+country in filing
order, with what each body responds to.

## Statutory overlays (what turns policy into law)

Common hard rights the letter generator can cite:

- **EU/UK**: 14-day distance-selling withdrawal; 2-year minimum
  conforming-goods liability; GDPR Art.15/17 access and erasure; EU261
  airline compensation (€250–600 by distance) for 3h+ delays/cancellations.
- **US**: FCBA billing-dispute window (60 days from statement, written
  dispute forces investigation); chargeback windows (Visa/MC ~120 days from
  transaction or expected delivery); Magnuson-Moss warranty implied
  warranties; DOT rules on tarmac delays and refunds for canceled flights.
- **Everywhere**: the merchant's own published policy is contractually
  binding once you relied on it — a screenshot is evidence.

The reference data here is a simplification; the tool prints the right
questions to ask and the right names to cite, and always marks "verify
current rule" — laws move faster than skills.

## Detonation sequencing

Public pressure (review sites, social, CEO email) is a one-shot resource:

- **Too early** — reads as unhinged; companies respond with legal-defensive
  posture instead of settlement; your escalation path is burned.
- **Too late** — refund/chargeback windows may have closed.

Optimal sequencing (what `plan` computes): public detonation happens at
rung 4, *together with* the regulator filing — the company now faces the
regulator response deadline AND a public, documented narrative AND a named
exec recipient simultaneously. Each alone is ignorable; the three together
rarely are.

## Follow-up cadence — never die of neglect

Silence is a strategy: most consumers drop cases at the first stall. The
tracker enforces:

- every contact logged (date, channel, person, result)
- `due` shows follow-ups owed: +5 business days after any promise, +7 after
  any letter
- a broken promise automatically advances the ladder in `plan`

## Tone

Firm, factual, specific. The letters never insult; they document. The
person reading rung 3 is deciding whether you're cheaper to pay than to
fight — make the record do the talking.
