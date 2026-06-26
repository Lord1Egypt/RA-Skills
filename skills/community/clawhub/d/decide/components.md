# Decision Components

Major decisions should be stored as a structured question plus the components that actually determine the answer.

## Minimum Decision Card

- **Question** — what is being decided
- **Domain** — code, product, ops, vendor, publishing, architecture
- **Components** — the factors that materially affect the answer
- **Options considered** — realistic branches
- **Chosen option** — what the human picked
- **Why** — the reasoning or tradeoff
- **Outcome** — accepted, corrected, still pending

## Example Component Sets

| Decision Type | Components That Usually Matter |
|---------------|--------------------------------|
| Framework choice | client, platform, team skill, project size, long-term maintenance |
| Vendor choice | budget, contract risk, lock-in, support needs, compliance |
| Publish choice | surface, audience, reversibility, review path, blast radius |
| Migration choice | data safety, rollback path, downtime tolerance, compatibility |
| Spend choice | amount, approval threshold, urgency, alternatives, recurring cost |

## Match Rule

Do not reuse a stored decision because one label matches.

Reuse is only safe when:
- the question is materially the same
- the key components are present
- the key components match closely enough to support the same answer
- no known exception applies

If any of those fail, ask first.
