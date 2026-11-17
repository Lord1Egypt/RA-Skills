## Description:

Create, trade, settle, and redeem prediction markets on Base with ERC20 collateral for market-based forecasting, contests, token utility, and related prediction-market workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[proxima424](https://clawhub.ai/user/proxima424)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to create, trade, settle, and redeem Base prediction markets backed by ERC20 collateral. It supports forecasting, contests, token-utility, automated market creation, and event-driven market workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run wallet-backed Base mainnet transaction scripts that spend funds and incur gas.

Mitigation: Use a dedicated low-balance wallet, review every command before execution, and treat examples as live mainnet transactions.

Risk: The release uses mutable npm dependency ranges and no bundled lockfile evidence was provided.

Mitigation: Pin and audit dependencies with a lockfile before installing or running the scripts.

Risk: ERC20 approvals may be broad, including an infinite approval model described by the artifact.

Mitigation: Prefer exact or capped token approvals where possible and revoke allowances after use.

Risk: Trading commands may execute with no effective slippage floor when users accept default zero minimum output.

Mitigation: Set explicit nonzero slippage protection before trading.

## Reference(s):

- [PNP SDK API Reference](references/api-reference.md)
- [PNP Markets Use Cases](references/use-cases.md)
- [PNP Markets - Complete Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/proxima424/skills/create-prediction-markets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and JSON transaction output from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate wallet-backed Base mainnet transactions when users run the included scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
