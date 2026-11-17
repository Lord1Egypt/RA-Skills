## Description:

Integrate Stripe payment intents, capture flow, and webhook reconciliation for A2A orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Stripe-backed authorization, capture, cancellation, refund-path planning, and webhook reconciliation to A2A order settlement flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stripe payment actions can have financial impact if credentials, capture, refund, or cancellation behavior are used against live accounts without review.

Mitigation: Confirm whether Stripe credentials are test or live, require explicit review before capture, refund, or cancel actions, and validate behavior before production use.

Risk: Webhook handling can misstate payment or order status if signatures and duplicate event handling are not enforced.

Mitigation: Keep webhook signature verification, idempotency keys, and explicit provider status mappings in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/skills/a2a-market-stripe-payment)
- [Publisher profile](https://clawhub.ai/user/luoqianchenguni-max)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with code and project layout recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces payment integration contracts, webhook mapping guidance, guardrails, and suggested runtime code paths.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
