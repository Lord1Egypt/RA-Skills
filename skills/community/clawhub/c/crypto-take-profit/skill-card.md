## Description:

Automated crypto take-profit orders. Gasless, oracle-protected across 8 EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eranp-orbs](https://clawhub.ai/user/eranp-orbs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate EVM swap intent into Spot order parameters, EIP-712 typed data, approval and signing guidance, relay submission, and lifecycle actions for take-profit and related advanced order shapes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill label focuses on take-profit orders, while the artifact also supports market, limit, TWAP, stop-loss, delayed-start, and chunked order shapes.

Mitigation: Use it only when a broader Spot advanced EVM swap-order workflow is acceptable, and confirm the intended order shape before building or signing payloads.

Risk: Approval, signer, spender, verifying contract, recipient, amount, deadline, trigger, or relay mistakes can create unwanted crypto transactions.

Mitigation: Before signing or submitting, verify every transaction-critical field and prefer exact ERC-20 approvals over standing maxUint approvals.

Risk: Wrong chain, token address, token decimals, or unsupported native-input handling can produce invalid or harmful order payloads.

Mitigation: Confirm the chain is explicitly supported, validate token addresses and decimals, and wrap native input tokens before order creation.

Risk: Ambiguous relay failures can lead to duplicate or inconsistent orders if payloads are rebuilt before status is resolved.

Mitigation: Persist the exact typedData and signature, query the relay by order hash or swapper, and retry only after confirming the previous submission state.

## Reference(s):

- [Skill Instructions](artifact/SKILL.md)
- [Quickstart](artifact/references/quickstart.md)
- [Parameters](artifact/references/params.md)
- [Template, Sign, And Submit](artifact/references/sign.md)
- [Lifecycle](artifact/references/lifecycle.md)
- [Examples](artifact/references/examples.md)
- [RePermit typed-data template](artifact/assets/repermit.template.json)
- [Token addressbook](artifact/assets/token-addressbook.md)
- [Spot security audit report](https://github.com/orbs-network/spot/blob/master/Audit-AstraSec.pdf)
- [Spot chain configuration](https://github.com/orbs-network/spot/blob/master/config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload templates, EIP-712 typed-data fields, JavaScript snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output for local payload construction, signing, relay submission, query, and cancellation; no external helper code is fetched or executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json is 2.5.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
