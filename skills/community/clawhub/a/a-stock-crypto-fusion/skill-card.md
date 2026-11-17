## Description:

Generates evidence-constrained A-share, crypto, and morning briefing reports from structured market JSON, with fixed templates for decisions, win rate, drawdown, risk, and data limitations.

This skill is for research and development only.

## Publisher:

[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to draft research-oriented A-share, crypto, dual-market, and morning briefing reports from supplied or fetched JSON market data. The skill is intended for structured analysis and briefing support, not financial, legal, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading reports could be mistaken for financial advice or could contain misleading market guidance if source data is incomplete.

Mitigation: Treat reports as research drafts, review all outputs before acting, and preserve the skill's evidence-list and data-insufficiency requirements.

Risk: The crypto news path can use and transmit a saved CryptoPanic token when the environment variable is set.

Mitigation: Unset CRYPTOPANIC_TOKEN unless news is explicitly needed, avoid passing tokens on the command line, and never echo or store user-provided tokens.

Risk: The included fetch scripts make network calls to public market-data providers and may depend on vulnerable or outdated packages.

Mitigation: Run scripts only in environments where those network calls are acceptable, inspect or update dependencies before regular use, and review scan results before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xinyuqinfeng/skills/a-stock-crypto-fusion)
- [Data Sources](references/data_sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and JSON-producing helper script commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs require evidence lists with concrete JSON paths and values; helper scripts may return partial JSON with errors recorded when upstream market-data providers fail.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
