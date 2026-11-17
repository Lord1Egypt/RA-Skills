## Description:

Clawdwallet helps agents install and control a multi-chain Web3 wallet Chrome extension for wallet setup, dApp connections, transaction signing, and crypto management across EVM, Bitcoin, Solana, and Cosmos chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neomaking](https://clawhub.ai/user/neomaking)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure an agent-controlled browser wallet, connect to dApps, review wallet requests, and approve or reject signing actions across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-controlled wallet setup and signing actions can move funds or grant approvals if a request is approved without careful review.

Mitigation: Use a dedicated low-balance wallet, a trusted local agent setup, and a reviewed pinned build; manually verify the request origin, chain, recipient, amount, and approval details before signing.

Risk: Recovery phrases, mnemonics, or WebSocket URLs exposed in chat, logs, or public settings can compromise the wallet.

Mitigation: Do not paste real recovery phrases into chat or logs, and never expose mnemonic material or the WebSocket URL publicly.

## Reference(s):

- [Clawdwallet ClawHub skill page](https://clawhub.ai/neomaking/skills/clawdwallet)
- [Repository URL listed by the skill artifact](https://github.com/NeOMakinG/clawdwallet.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup steps, gateway configuration, wallet command examples, request handling guidance, and supported-chain information.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
