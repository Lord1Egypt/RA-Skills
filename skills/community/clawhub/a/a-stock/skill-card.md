## Description:

A股智投大师 helps agents analyze A-share market data, fundamentals, stock screening, watchlists, news, and monitoring alerts using East Money and Miaoxiang data services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasxing1](https://clawhub.ai/user/lucasxing1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to support A-share research workflows such as market quotes, fundamental analysis, stock screening, watchlist management, news review, and monitoring alerts. Outputs are for investment research support and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-installed dependency skills may expand the trust boundary.

Mitigation: Confirm the publisher and every dependency before installation, and prefer pinned reviewed versions.

Risk: External East Money API calls may expose API keys or sensitive investment strategy text.

Mitigation: Use a dedicated API key with limited exposure and avoid sending sensitive strategy text unless remote processing is acceptable.

Risk: Self-select and monitoring workflows can change account-linked watchlists or alerts.

Mitigation: Require explicit user confirmation before adding, deleting, or creating watchlist and alert entries.

Risk: Market data and generated analysis may be delayed, incomplete, or unsuitable for a user's financial circumstances.

Mitigation: Present outputs as research support only and keep investment-risk disclaimers visible to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasxing1/skills/a-stock)
- [Publisher profile](https://clawhub.ai/user/lucasxing1)
- [README](README.md)
- [East Money Miaoxiang API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional code blocks, API-call guidance, and configuration commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include investment-analysis guidance and watchlist or alert-management instructions; not investment advice.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
