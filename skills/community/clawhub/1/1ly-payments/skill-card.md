## Description:

1ly Payments helps agents buy and sell paid APIs and services through 1ly MCP/x402, accept USDC on Solana or Base, manage stores and paid links, and launch, trade, or claim fees for Solana tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1lystore](https://clawhub.ai/user/1lystore)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to integrate agent-native payments, paid API calls, seller store and link management, and Solana/Base wallet payment flows. It also guides token launch, trade, and fee-claim workflows that require explicit wallet and budget controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw wallet keys and seller credentials may be exposed or persisted locally.

Mitigation: Use a dedicated low-balance wallet, prefer a constrained wallet provider where possible, avoid inline private keys and /tmp key files, and store seller API keys securely.

Risk: Paid calls, token trades, fee claims, withdrawals, key revocations, and link deletions can have direct financial or account impact.

Mitigation: Set explicit per-call and daily budgets, disable autonomous spend when not needed, and manually confirm high-impact actions and destination addresses before execution.

Risk: The skill depends on external npm/MCP code for payment behavior.

Mitigation: Review the external package before installation and verify package integrity during setup.

## Reference(s):

- [1ly homepage](https://1ly.store)
- [1ly documentation](https://docs.1ly.store/)
- [@1ly/mcp-server npm package](https://www.npmjs.com/package/@1ly/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, environment variables, MCP tool names, and JSON tool input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through payment, seller, wallet, token, and budget workflows; paid actions depend on configured wallets and explicit budgets.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
