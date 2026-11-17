## Description:

Gate DEX Trade guides agents through on-chain token swap execution, including quotes, balance checks, staged signing, transaction submission, and status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through Gate DEX swap workflows for same-chain and cross-chain token trades. The skill helps collect trade parameters, route between MCP and OpenAPI modes, enforce confirmation steps, and produce the commands or API calls needed for execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill participates in real on-chain trading and transaction signing, which can move funds irreversibly.

Mitigation: Require explicit user review of the trading pair, quote, slippage, target contract, gas, and signature authorization before any signing or submission step.

Risk: Wallet private keys, keystore files, .env files, API keys, or MCP tokens could be exposed if pasted into the agent or read from local files.

Mitigation: Prefer an external wallet or hardware signer, avoid pasting private keys into chat, keep secret files out of agent-readable workflows, and mask secret keys in any displayed configuration.

Risk: Installation can alter persistent agent routing and MCP configuration.

Mitigation: Review and back up existing agent and MCP configuration files before running the installer, then inspect generated routing rules before using the skill.

Risk: Local check-in binaries and mutable remote rules influence transaction execution.

Mitigation: Run only bundled or independently verified binaries, confirm hashes where possible, and do not execute missing or separately downloaded check-in binaries without source and hash verification.

## Reference(s):

- [Gate DEX Trade on ClawHub](https://clawhub.ai/gate-exchange/skills/gate-dex-trade)
- [Skill Routing Definition](artifact/SKILL.md)
- [MCP Mode Reference](artifact/references/mcp.md)
- [OpenAPI Mode Reference](artifact/references/openapi.md)
- [MCP Setup Guide](artifact/references/setup.md)
- [Transaction Check-In Tool Reference](artifact/tools/tx-checkin/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction, signing, setup, and API-call guidance that requires user review before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter version 2026.4.2-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
