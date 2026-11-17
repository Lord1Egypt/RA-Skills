## Description:

Helps an agent place user-requested orders for specific physical products through Axiom and check saved payment methods, order status, and receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axiom-wallet](https://clawhub.ai/user/axiom-wallet)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent to buy a specific physical product with their Axiom account can place an order, check their saved payment method, and review order status or receipts. The agent asks for missing product details before ordering and relays any required approval to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clear purchase request can result in an order charged to the saved payment method without another chat confirmation when it meets the user's Axiom spending rules.

Mitigation: Review spending rules, approval limits, the saved payment method, and OAuth scopes before enabling ordering; require an explicit request for a specific product and clarify missing options first.

Risk: An order above the auto-approval limit needs the user's authorization outside chat.

Mitigation: Share Axiom's approval link with the user and stop; never approve on their behalf or report completion until Axiom confirms it.

## Reference(s):

- [Axiom skill on ClawHub](https://clawhub.ai/axiom-wallet/axiom)
- [Axiom skill release](https://clawhub.ai/axiom-wallet/skills/axiom)
- [Authentication guide](artifact/references/authentication.md)
- [Tool reference](artifact/references/tool-reference.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relays order updates, approval links, and receipts from Axiom; ordering may complete after the initial response.]

## Skill Version(s):

0.3.2 (source: release metadata, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
