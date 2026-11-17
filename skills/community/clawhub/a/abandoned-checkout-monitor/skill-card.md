## Description:

Provides cart-to-checkout funnel diagnostics, checkout friction analysis, payment troubleshooting, and abandoned-cart recovery playbooks for e-commerce merchants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce merchants and operators use this skill to diagnose abandoned carts, checkout drop-off, shipping shock, payment failures, and recovery messaging opportunities. It produces a structured playbook with hypotheses, A/B copy tests, troubleshooting steps, and recovery email drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may answer broad sales-performance questions with checkout-abandonment guidance even when the root issue is traffic quality, pricing, inventory, merchandising, or broader conversion strategy.

Mitigation: Confirm the question involves orders, checkout, payment, or abandonment before applying the full playbook; redirect to a more relevant analysis when checkout friction is not supported by the available context.

Risk: Recommendations can be incorrect or misleading when funnel metrics, payment errors, regional shipping costs, or recovery compliance requirements are missing.

Mitigation: Label assumptions, request or instrument the missing metrics, and have a qualified operator review proposed recovery copy, incentives, and troubleshooting steps before implementation.

## Reference(s):

- [Abandonment and checkout friction playbook](references/abandonment_playbook.md)
- [ClawHub skill page](https://clawhub.ai/rijoyai/skills/abandoned-checkout-monitor)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown playbook with diagnostic tables, checklists, A/B copy, and email drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory text only; no tool execution, data access, persistence, or destructive behavior.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
