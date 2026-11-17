## Description:

ClawLaunch helps agents launch, discover, quote, and trade AI agent tokens on the Base bonding-curve launchpad using ClawLaunch API and CLI guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smokealot420](https://clawhub.ai/user/smokealot420)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to configure ClawLaunch access, inspect available tokens, request launch or trading API calls, and generate code or shell commands for Base token workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide autonomous agents through token launches and buy or sell workflows that may affect real crypto assets.

Mitigation: Use testnet or read-only credentials first, keep very small wallet balances, and require manual confirmation before every mainnet launch, buy, or sell.

Risk: API keys and wallet credentials exposed to an autonomous trading workflow could be misused.

Mitigation: Store secrets outside prompts and logs, use restricted credentials, and only use keys or wallets you are willing to expose to the workflow.

Risk: On-chain memos are public and permanent, so private strategy or sensitive information may be disclosed.

Mitigation: Do not include secrets, private trading strategy, or sensitive personal information in memos.

Risk: Changing the API URL could direct requests to an untrusted endpoint.

Mitigation: Restrict the API URL to the official ClawLaunch endpoint before using credentials or wallet-connected operations.

## Reference(s):

- [ClawLaunch Website](https://www.clawlaunch.fun)
- [ClawLaunch API Documentation](references/api-docs.md)
- [ClawLaunch Token Trading Reference](references/token-trading.md)
- [ClawLaunch Agent Autonomy Patterns](references/agent-patterns.md)
- [ClawLaunch Error Handling Reference](references/error-handling.md)
- [Factory Contract on BaseScan](https://basescan.org/address/0xb3e479f1e2639A3Ed218A0E900D0d2d3a362ec6b)
- [Registry Contract on BaseScan](https://basescan.org/address/0x7a05ACcA1CD4df32c851F682B179dCd4D6d15683)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, bash, Python, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request examples, CLI invocations, wallet configuration guidance, and transaction calldata handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
