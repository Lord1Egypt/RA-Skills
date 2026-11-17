## Description:

DCA orders for crypto. Split buys over time, gasless, oracle-protected, 8 EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eranp-orbs](https://clawhub.ai/user/eranp-orbs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate crypto trading intent into normalized Spot DCA, TWAP, limit, stop-loss, take-profit, delayed-start, or cancellation workflows on supported EVM chains. It guides local parameter preparation, EIP-712 typed-data population, approval decisions, signing, relay submission, and order status follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broader crypto trading actions than DCA buys, including approvals, signatures, order submission, and cancellation.

Mitigation: Review each order as an advanced crypto trade and confirm the chain, token addresses, recipient, amounts, slippage, deadlines, and order type before approval or signature.

Risk: Standing maximum token approvals can grant repeat-use spend authority beyond a single order.

Mitigation: Prefer exact approvals for input.maxAmount unless the user deliberately chooses a standing approval for repeated use.

Risk: Typed data and signatures are sensitive and can authorize real token movement through the configured relay and contracts.

Mitigation: Keep populated typedData and signatures private, submit only the final signed payload, and reuse the exact populated typedData when resolving ambiguous retries or cancellations.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [Params](references/params.md)
- [Template, Sign, And Submit](references/sign.md)
- [Lifecycle](references/lifecycle.md)
- [Examples](references/examples.md)
- [Common Token Addressbook](assets/token-addressbook.md)
- [RePermit Typed-Data Template](assets/repermit.template.json)
- [Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf)
- [ClawHub Skill Page](https://clawhub.ai/eranp-orbs/skills/dca-order)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload shapes, EIP-712 typed-data configuration, and optional shell or JavaScript command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; the agent prepares order data locally and submits only the final signed payload when directed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
