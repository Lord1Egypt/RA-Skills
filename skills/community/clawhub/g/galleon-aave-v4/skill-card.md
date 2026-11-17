## Description:

Guides inspection of Aave V4 positions and preparation of unsigned supply, borrow, repay, and withdrawal plans with health previews and confirmation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi users inspect a specific Aave V4 position, assess borrowing or withdrawal health, and review a complete unsigned action sequence before separately authorizing any wallet transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect chain, token units, reserve, or approval spender could produce an unintended DeFi transaction.

Mitigation: Verify the live chain and position, exact amounts and units, spender, allowances, and every unsigned payload before wallet authorization.

Risk: A stale position or health preview may obscure borrowing constraints or leave residual debt after repayment.

Mitigation: Refresh position data, review health-factor warnings and accrued debt, and reconcile receipts and balances before dependent actions.

## Reference(s):

- [Aave V4 positions on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-aave-v4)
- [V4 official interface procedure](references/operations.md)
- [V4 worked records](references/examples.md)
- [Aave MCP tools](https://aave.com/docs/mcp/tools)
- [Aave V4 TypeScript guide](https://aave.com/docs/aave-v4/getting-started/typescript)

## Skill Output:

**Output Type(s):** [Text, Guidance, Unsigned transaction plans]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Position and health analysis, warnings, ordered unsigned approval and transaction steps, and confirmation prerequisites; no signer.]

## Skill Version(s):

0.3.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
