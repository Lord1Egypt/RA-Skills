## Description:

Help users make better Didi ride-booking decisions from public ride-choice logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare Didi ride categories and choose between price, wait time, reliability, luggage or passenger needs, and comfort trade-offs before booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake public ride-option guidance for live Didi account actions, bookings, coupons, order history, or real-time price retrieval.

Mitigation: Use the skill only for general ride-choice advice; for logged-in pages, bookings, coupons, order history, or live page state, use an appropriate browser workflow with user control.

Risk: Ride-choice heuristics may be treated as guaranteed outcomes.

Mitigation: Present trade-offs as decision support and tell users to verify current wait time, price, reliability, luggage or passenger fit, and payment details before booking.

## Reference(s):

- [Ride Choice Guide](references/ride-choice-guide.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Analysis]

**Output Format:** [Markdown with best option, reasons, caveats, and final advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not perform login, account access, cookie handling, order retrieval, coupon claiming, local persistence, browser automation, or live price retrieval.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
