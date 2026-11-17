## Description:

Swap tokens on Ethereum via the AIDEX aggregator; agents can search tokens, check exchange rates, view balances, and execute swaps while transaction signing remains local.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almiashev](https://clawhub.ai/user/almiashev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Aidex to let an OpenClaw agent search Ethereum tokens, quote swaps, inspect wallet balances, execute signed swaps, and check transaction status. Swap execution requires a locally configured wallet private key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A high-value private key could be exposed if the agent host or its environment is compromised.

Mitigation: Use a dedicated wallet with limited funds and avoid configuring a wallet that controls high-value assets.

Risk: API-controlled swap terms could result in a bad trade or unexpectedly high gas fees.

Mitigation: Verify the final swap terms, exchange rate, slippage, and fees independently before execution.

Risk: Token approvals may grant the router spending authority beyond the immediate swap.

Mitigation: Review allowances before and after swaps, and revoke unneeded approvals when appropriate.

## Reference(s):

- [ClawHub Aidex Skill Page](https://clawhub.ai/almiashev/skills/aidex)
- [AIDEX Homepage](https://ai-dex.io/)
- [AIDEX Scripts Reference](artifact/references/scripts.md)
- [AIDEX Security Model](artifact/references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON results from Node.js command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only operations return token, rate, balance, or status data; swap operations can produce signed Ethereum transaction hashes.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
