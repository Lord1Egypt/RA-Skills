## Description:

Ensures any purchase, booking, or financial commitment is verified for item, price, terms, authorization, payment privacy, and reversibility before proceeding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill before purchases, bookings, subscriptions, renewals, transfers, or similar financial commitments to verify exact terms and obtain explicit user approval. It is especially useful for workflows that prepare carts, reservations, review payloads, or user-facing decision summaries without making unauthorized commitments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial or booking actions may proceed with incomplete cost, terms, reversibility, or authorization details.

Mitigation: Verify the exact commitment, total price, fees, refund and cancellation terms, payment method, reversibility, and explicit user approval before final submission.

Risk: Review payloads may expose sensitive payment, identity, reservation, or account data.

Mitigation: Use minimal redacted summaries and omit full payment numbers, bank details, credentials, identity documents, full reservation codes, raw receipts, and unrelated purchase history.

Risk: External checker integrations could be untrusted or misconfigured.

Mitigation: Use only approved host tools, approved in-memory API connectors, or manual review, and keep review payloads redacted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-purchase-booking-guardrail)
- [Review payload schema](artifact/schemas/purchase-booking-review.schema.json)
- [Redacted review payload example](artifact/examples/redacted-purchase-booking-review.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown instructions with optional JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; review payloads should be minimal and redacted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
