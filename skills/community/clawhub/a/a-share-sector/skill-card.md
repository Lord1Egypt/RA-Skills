## Description:

A Share Sector helps agents query A-share industry, concept, and regional sector performance, capital flow, and constituent-stock details for realtime or specified historical dates using EastMoney data via akshare.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yituwangpeng](https://clawhub.ai/user/yituwangpeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis users use this skill to answer A-share sector questions by running the bundled query script and summarizing sector rankings, capital-flow leaderboards, and constituent-stock tables. It is intended for research reference and market-data reporting, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install unpinned Python packages into the active environment.

Mitigation: Install and run it in an isolated virtual environment, review dependency versions first, and pin packages for managed deployments.

Risk: The query script removes proxy-related environment variables before making market-data requests.

Mitigation: Review or remove the proxy-clearing behavior when enterprise proxy, monitoring, or package-mirror controls are required.

Risk: The skill makes direct outbound requests to public market-data interfaces that may be delayed, unavailable, or changed upstream.

Mitigation: Run it only where outbound data access is approved, treat results as reference data, and keep the non-investment-advice disclaimer with user-facing summaries.

## Reference(s):

- [EastMoney](https://quote.eastmoney.com/)
- [akshare GitHub Repository](https://github.com/akfamily/akshare)
- [akshare Documentation](https://akshare.akfamily.xyz/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tables with concise narrative summaries and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes market-data source and non-investment-advice disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
