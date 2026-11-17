## Description:

Agent trading on BNB Chain for limit, DCA, stop-loss, and take-profit orders with non-custodial, zero-fee workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn-orbs](https://clawhub.ai/user/shawn-orbs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn trading intent into signed Spot order payloads for non-custodial swaps, including limit, TWAP, stop-loss, take-profit, delayed-start, query, and cancellation workflows on BNB Chain and other listed EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises BNB Chain trading while the artifact supports signed orders across several EVM chains.

Mitigation: Before approval or signing, confirm the exact chain ID, adapter, verifying contract, relay destination, and intended token pair.

Risk: Wallet approvals and EIP-712 signatures can authorize token movement if order details are wrong.

Mitigation: Prefer exact per-order approvals, verify spender, input token, maximum amount, recipient, deadline, and slippage, and avoid standing approvals unless explicitly needed.

Risk: Mock examples include placeholder payloads and signatures that are not suitable for live orders.

Mitigation: Use examples only as shape references and regenerate all addresses, amounts, timing fields, typed data, and signatures from the user's actual order intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn-orbs/skills/bnb-chain-trading)
- [Quickstart](references/quickstart.md)
- [Parameter reference](references/params.md)
- [Template, signing, and submission](references/sign.md)
- [Lifecycle](references/lifecycle.md)
- [Examples](references/examples.md)
- [Token addressbook](assets/token-addressbook.md)
- [RePermit typed-data template](assets/repermit.template.json)
- [Spot chain configuration](https://github.com/orbs-network/spot/blob/master/config.json)
- [Security Audit Report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell or JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces locally assembled EIP-712 typed data and relay payloads; does not execute external helper code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
