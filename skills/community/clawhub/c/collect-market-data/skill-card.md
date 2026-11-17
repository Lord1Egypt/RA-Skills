## Description:

Collects global financial market data across U.S., China, Hong Kong, Europe, and Asia-Pacific markets to support daily financial report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szrw1825](https://clawhub.ai/user/szrw1825)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-reporting agents use this skill to gather market performance, policy, company, economic, holiday, and daily-summary data before producing a financial daily report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs scripts with broad network and file access.

Mitigation: Install and execute it only in a contained environment with reviewed network and filesystem permissions.

Risk: The artifact imports configuration from hard-coded external user paths and writes to configured output and log paths.

Mitigation: Verify config.py, output directories, and log paths before use, and replace hard-coded paths with deployment-local configuration.

Risk: Market symbols and web-search queries may be sent to third-party providers.

Mitigation: Review provider terms and avoid submitting confidential prompts, watchlists, or business-sensitive market queries.

Risk: Browser automation disables the Chromium sandbox.

Mitigation: Remove or constrain the no-sandbox setting before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szrw1825/skills/collect-market-data)
- [Bocha Web Search API endpoint](https://api.bocha.cn/v1/web-search)
- [FRED CSV data endpoint](https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&limit={limit})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON market_data file with logs and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes market_data.json under a configured daily output directory and records collection activity in a configured log file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
