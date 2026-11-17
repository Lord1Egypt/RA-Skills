## Description:

Fetches daily finance trending lists and investment news from sources such as Wallstreetcn, Xueqiu, Yicai, Baidu Finance, and Sina Finance to help users quickly understand current market focus areas; it does not provide real-time K-line market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxxc](https://clawhub.ai/user/foxxc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused analysts use this skill to collect, filter, and summarize daily market news and trending finance topics. It is suited for quick finance-news briefings, not for real-time trading data or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public finance ranking pages, so source availability, page changes, and third-party news quality can affect output accuracy.

Mitigation: Review summarized finance items against their original public sources before acting on them.

Risk: The skill may activate for broad finance-news prompts and return market summaries that users could mistake for investment advice.

Mitigation: Use the output as an informational briefing and avoid treating it as personalized trading, legal, or financial advice.

Risk: The optional AkShare extension requires installing an additional package for real-time market-data tooling.

Mitigation: Install AkShare only when needed, preferably in a virtual environment with a reviewed package version.

## Reference(s):

- [Daily Finance on ClawHub](https://clawhub.ai/foxxc/skills/daily-finance)
- [TopHub Wallstreetcn Daily Ranking](https://tophub.today/n/G2me3ndwjq)
- [TopHub Xueqiu Today Topics](https://tophub.today/n/X12owXzvNV)
- [TopHub Sina Finance 7x24](https://tophub.today/n/WmoO9qYd4E)
- [TopHub Sina Finance Click Ranking](https://tophub.today/n/rx9ozj7oXb)
- [TopHub Baidu Finance Ranking](https://tophub.today/n/ARe1p17d7n)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style finance briefing with ranked news items and optional shell command guidance for AkShare installation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits curated highlights to up to five selected items and separates sections with ======.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
