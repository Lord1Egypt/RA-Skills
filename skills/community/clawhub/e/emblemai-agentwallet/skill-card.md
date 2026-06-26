## Description: <br>
Connects to EmblemVault and manages crypto wallets via Emblem AI Agent Hustle across Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genecyber](https://clawhub.ai/user/genecyber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect agents to EmblemVault, check wallet addresses and balances, query crypto portfolio data, and request wallet operations through the Emblem AI CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-mode wallet commands can request high-impact transfers, swaps, or other transaction actions. <br>
Mitigation: Use wallets with limited funds and require explicit human review and approval before any transfer, swap, signing, order, or DeFi operation. <br>
Risk: EMBLEM_PASSWORD and files under ~/.emblemai can grant access to wallet sessions or deterministic wallets. <br>
Mitigation: Protect the password and local credential files, avoid logging secrets or storing them in shell history, and prefer browser authentication for interactive use. <br>
Risk: The skill depends on a third-party npm CLI that runs locally with the user's permissions. <br>
Mitigation: Install only if you trust EmblemVault and the @emblemvault/agentwallet package, and inspect package contents before use in sensitive environments. <br>
Risk: The server security summary states that the transaction approval boundary is not fully demonstrated in the submitted artifact. <br>
Mitigation: Do not permit unattended agent-mode transfers or swaps unless you independently verify that every transaction requires explicit human approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/genecyber/emblemai-agentwallet) <br>
- [EmblemVault homepage](https://emblemvault.dev) <br>
- [npm package: @emblemvault/agentwallet](https://www.npmjs.com/package/@emblemvault/agentwallet) <br>
- [Hustle AI](https://agenthustle.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and text responses returned by emblemai] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, emblemai, and EMBLEM_PASSWORD or browser authentication; CLI responses may include wallet, portfolio, market, and transaction details.] <br>

## Skill Version(s): <br>
3.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
