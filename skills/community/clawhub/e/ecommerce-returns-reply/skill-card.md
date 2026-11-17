## Description:

Generates warm, policy-aligned Chinese customer-service replies for ecommerce return, exchange, refund, shipping-fee, and after-sales questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce customer-service agents use this skill to draft clear Chinese replies for returns, exchanges, refunds, shipping-fee questions, quality issues, wrong shipments, and after-sales policy disputes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Return-policy timeframes, fee rules, or exception handling may not match the user's ecommerce platform.

Mitigation: Review and update the policy-rules reference for the target platform before relying on generated replies.

Risk: Broad return and refund trigger phrases may overlap with other customer-service skills.

Mitigation: Narrow activation phrases when deploying alongside multiple customer-service skills.

Risk: The skill could produce an inaccurate commitment if order status or policy eligibility is incomplete.

Mitigation: Require agents to verify customer order details and use the provided fallback language when policy details are uncertain.

## Reference(s):

- [policy-rules.md](references/policy-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style customer-service reply text with structured sections and numbered steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language response template with policy checks, timeframes, fee responsibility guidance, and fallback language when details need verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
