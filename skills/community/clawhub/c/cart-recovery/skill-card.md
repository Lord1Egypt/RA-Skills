## Description:

Decomposes three-step checkout abandonment, classifies friction by exit step, and generates step-specific recovery tactics with a required three-part abandoned-checkout email sequence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and ecommerce operators use this skill to diagnose where shoppers abandon checkout and translate that drop-off into recovery tactics, compensation offers, and compliant follow-up email drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add abandoned-cart email drafts by default, including urgency and ultimatum framing, even when the user did not explicitly request email copy.

Mitigation: Review generated outreach before use and enforce merchant email frequency, consent, unsubscribe, and truthful urgency rules.

Risk: Recovery recommendations could become overly broad if the agent is expected to stay tightly scoped to a narrow user request.

Mitigation: Confirm that checkout recovery guidance is relevant to the request, especially for order tracking, product copy, regulated claims, or non-funnel support cases.

## Reference(s):

- [Checkout Dropoff Recovery Playbook](references/checkout_recovery_playbook.md)
- [Cart Recovery on ClawHub](https://clawhub.ai/rijoyai/skills/cart-recovery)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown tables, classifications, recovery tactics, and email skeletons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces strategy and copy drafts only; it does not send messages, run code, or access external systems.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
