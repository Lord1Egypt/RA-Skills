## Description:

Crypto limit orders. Gasless, oracle-protected execution across 8 EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eranp-orbs](https://clawhub.ai/user/eranp-orbs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and crypto users use this skill to convert trading intent into gasless, non-custodial Spot order payloads on supported EVM chains. It guides parameter normalization, EIP-712 typed-data population, approval guidance, signing, relay submission, order status queries, and exact-match cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help prepare and submit real crypto orders or cancellations.

Mitigation: Require review of the final transaction or typed data before signing or submission, including token addresses, chain ID, amounts, recipient, deadline, nonce, order shape, relay endpoint, and cancellation digest.

Risk: Signed payloads and signatures can authorize order execution and should be treated as sensitive.

Mitigation: Persist and reuse the exact populated typed data and signature only for the intended retry or cancellation flow, and avoid exposing signatures outside the signing and relay submission path.

Risk: Incorrect token aliases, decimals, approvals, or chain support assumptions can create unintended orders.

Mitigation: Use the supported-chain list as authoritative, treat the token address book only as a convenience reference, and default approval guidance to the exact input.maxAmount rather than standing unlimited approval.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [Parameters](references/params.md)
- [Template, Sign, And Submit](references/sign.md)
- [Lifecycle](references/lifecycle.md)
- [Examples](references/examples.md)
- [Common Token Addressbook](assets/token-addressbook.md)
- [RePermit Typed-Data Template](assets/repermit.template.json)
- [Spot Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf)
- [Spot Chain Configuration](https://github.com/orbs-network/spot/blob/master/config.json)
- [ClawHub Skill Page](https://clawhub.ai/eranp-orbs/skills/crypto-limit-order)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payloads and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces locally prepared order parameters, typed-data payloads, relay payloads, approval guidance, query commands, and cancellation guidance; it does not execute helper code by itself.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact package.json lists 2.5.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
