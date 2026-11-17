## Description:

Tracks crypto portfolios across multi-chain wallets, centralized exchanges, and prediction-market positions, then returns structured portfolio analysis and risk guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, investors, analysts, and developers use this skill to consolidate crypto asset data from wallets, exchanges, and prediction markets, calculate portfolio performance, and receive structured risk analysis. It is intended for normal ClawHub commercial release usage, subject to review of its execution and financial-account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command execution and file-write capability can modify local files or run unintended commands.

Mitigation: Require command previews, sandboxed execution where available, and explicit confirmation before file writes.

Risk: Financial account or API access may expose balances or enable trades if high-privilege credentials are supplied.

Mitigation: Use read-only exchange and API keys where possible, avoid wallet private keys, and require per-trade approval for any trade-capable workflow.

Risk: Automated portfolio and risk analysis may be misleading if source market data is incomplete, stale, or incorrectly parsed.

Mitigation: Review data sources and outputs before making financial decisions, especially when external APIs fail or return partial data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/crypto-portfolio)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Text, Guidance, JSON, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown or JSON with structured portfolio results, status fields, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require cryptocurrency data sources, exchange or wallet API keys, and agent read/exec capability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
