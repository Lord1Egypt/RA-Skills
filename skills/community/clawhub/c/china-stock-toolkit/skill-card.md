## Description:

China Stock Toolkit provides an agent-facing market dashboard for A-share, Hong Kong, U.S., Japan and Korea indices, precious metals, watchlists, stock detail analysis, news sentiment, trading fee calculations, and configurable data sources.

This skill is for research and development only.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query China and global market snapshots, manage watchlists, fetch news sentiment, and calculate A-share trading fees. It is informational market tooling and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote news data rendered in the HTML dashboard may execute script if a provider or returned item is compromised.

Mitigation: Do not expose or rely on the news dashboard until remote fields are rendered with textContent or sanitized HTML and all outbound links are validated.

Risk: Market and news queries are sent to third-party providers.

Mitigation: Review data-provider exposure before use and avoid submitting sensitive portfolio or account information through queries.

Risk: Financial market data, sentiment labels, and fee calculations may be delayed, incomplete, or inaccurate.

Mitigation: Use outputs as informational context only and verify prices, fees, and decisions against authoritative financial sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/china-stock-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON market data, Markdown guidance, shell command examples, configuration snippets, and a local HTML dashboard file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query third-party market and news data providers; some expanded markets require user-provided API keys or proxy configuration.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
