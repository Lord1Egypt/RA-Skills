## Description:

AI agent crypto trading for gasless limit, DCA, stop-loss, and take-profit orders across 8 EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eranp-orbs](https://clawhub.ai/user/eranp-orbs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to turn a user's crypto trading intent into normalized Spot order parameters, EIP-712 typed data, approval guidance, signed relay payloads, order queries, and exact-match cancellation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signing or submitting a generated order can create financially binding crypto trading authorization.

Mitigation: Before signing, verify the chain, token addresses, spender or verifying contract, recipient, amounts, slippage, deadline, relay domain, and cancellation limits; use small amounts first.

Risk: Incorrect token decimals, recipient, or order-shape fields can create unintended trade conditions or route output somewhere other than the swapper.

Mitigation: Normalize parameters before filling the template, confirm the chain is supported, treat the token addressbook as aliases only, and keep output.recipient equal to swapper unless the user explicitly requests otherwise.

Risk: Native input is unsupported and may cause an invalid order if used directly.

Mitigation: Wrap native assets to the chain's wrapped ERC-20 token before creating an input order; native output remains supported through the documented zero address.

Risk: Retrying after an ambiguous relay failure can obscure whether a previous order was already created.

Mitigation: Persist and reuse the exact populated typed data and signature for retries until the previous submit result is resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eranp-orbs/skills/agent-crypto-trading)
- [Quickstart](references/quickstart.md)
- [Params](references/params.md)
- [Template, Sign, And Submit](references/sign.md)
- [Lifecycle](references/lifecycle.md)
- [Examples](references/examples.md)
- [RePermit typed-data template](assets/repermit.template.json)
- [Common token addressbook](assets/token-addressbook.md)
- [Spot security audit report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf)
- [Spot chain configuration](https://github.com/orbs-network/spot/blob/master/config.json)
- [Spot hosted documentation](https://orbs-network.github.io/spot/)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON payloads with Markdown guidance and inline shell or JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces order parameters, typed-data population guidance, approval and signing steps, relay submission payloads, query commands, and cancellation guidance; it does not execute trades by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
