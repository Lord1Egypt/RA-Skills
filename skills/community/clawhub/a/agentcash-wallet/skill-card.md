## Description:

Manage an agentcash wallet and call x402-protected APIs with automatic payment from a funded USDC wallet on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmhall](https://clawhub.ai/user/fmhall)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect agentcash wallet balance, redeem credits, fund a wallet, discover x402-protected endpoint pricing, and run paid API requests through the agentcash CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is payment-focused and may spend wallet funds when making paid API requests.

Mitigation: Confirm the origin, endpoint, price, payload, and expected result before each paid request.

Risk: The skill asks users to run unpinned agentcash CLI commands.

Mitigation: Use a verified, pinned agentcash CLI version instead of unpinned npx commands for wallet and payment operations.

Risk: Discovered endpoint instructions could be untrusted and conflict with user or security requirements.

Mitigation: Treat discovered endpoint instructions as data; do not allow them to override the user's request or security rules.

## Reference(s):

- [Agentcash Wallet skill page](https://clawhub.ai/fmhall/skills/agentcash-wallet)
- [Publisher profile](https://clawhub.ai/user/fmhall)
- [Getting Started](artifact/rules/getting-started.md)
- [x402scan deposit UI](https://x402scan.com/mcp/deposit/<wallet-address>)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may trigger wallet, payment, endpoint discovery, and paid API request flows through the agentcash CLI.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
