## Description:

Decentralized stop-loss orders for DeFi. Gasless, oracle-protected, 8 EVM chains supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eranp-orbs](https://clawhub.ai/user/eranp-orbs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and DeFi operators use this skill to turn swap intent into normalized Spot order parameters, EIP-712 typed data, signed relay payloads, and lifecycle actions for supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stop-loss label understates broader live Spot advanced swap order capabilities.

Mitigation: Use the skill only when the user intends live Spot advanced swap orders, and confirm the selected order shape before approval, signing, or relay submission.

Risk: Incorrect order parameters can create unintended live trading behavior.

Mitigation: Before signing or approving, verify chain ID, token addresses, amounts, deadlines, slippage, and that output.recipient is the intended address.

Risk: The relay at agents-sink.orbs.network receives signed order data.

Mitigation: Treat the relay as a third-party service, submit only the final signed payload, and preserve the exact typed data and signature for retries, queries, and cancellation.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [Parameters](references/params.md)
- [Template, Sign, And Submit](references/sign.md)
- [Lifecycle](references/lifecycle.md)
- [Examples](references/examples.md)
- [RePermit Typed-Data Template](assets/repermit.template.json)
- [Common Token Addressbook](assets/token-addressbook.md)
- [Spot Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf)
- [Spot Chain Configuration](https://github.com/orbs-network/spot/blob/master/config.json)
- [Spot Order Relay](https://agents-sink.orbs.network/orders)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payloads, JavaScript snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local order parameters, populated EIP-712 typed data, relay payloads, query commands, and cancellation guidance; users must sign and approve with their own wallet.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact package.json declares 2.5.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
