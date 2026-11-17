## Description:

Trade tokens on Solana using the ClawDex CLI. Use when the user asks to swap tokens, check balances, get quotes, or manage a Solana trading wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelccodes](https://clawhub.ai/user/joelccodes)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to quote Solana token swaps, check wallet balances, simulate trades, and execute swaps through the ClawDex CLI with JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a mutable global ClawDex CLI and use wallet/API access.

Mitigation: Install a pinned, verified ClawDex version and review the CLI before granting wallet or API access.

Risk: The skill supports non-interactive live swaps with swap authority.

Mitigation: Use an isolated low-value wallet or hardware/approval-based signer, simulate first, and execute only after confirming tokens, amount, slippage, route, destination, and fees.

## Reference(s):

- [ClawDex Trading on ClawHub](https://clawhub.ai/joelccodes/skills/clawdex-trading)
- [Publisher profile: joelccodes](https://clawhub.ai/user/joelccodes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to request JSON output, parse balances as strings, check exit codes, and simulate swaps before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
