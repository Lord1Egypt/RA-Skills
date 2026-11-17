## Description:

Analyzes China A-share stocks, especially CSI 2000 constituents, using technical indicators, financial data, news sentiment, and local caching to generate text reports and buy/sell-style signals.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[evanslin99](https://clawhub.ai/user/evanslin99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent to run or adapt A-share stock analysis workflows for ticker research, technical-indicator summaries, news-sentiment checks, and report generation. Outputs should be treated as informational demos unless connected to verified market and financial data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated or hardcoded market and financial data may be presented with buy/sell-style recommendations.

Mitigation: Use only as a demo or prototype until verified data sources are configured, synthetic output is clearly labeled, and recommendations are reviewed before financial use.

Risk: Report generation can write analysis output to files.

Mitigation: Constrain report writes to an approved output directory and validate user-provided paths before automated use.

Risk: News analysis can require network calls and API credentials.

Mitigation: Run with least-privilege environment variables, document permitted network endpoints, and respect third-party API limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evanslin99/skills/csi-stock-analyzer)
- [Publisher profile](https://clawhub.ai/user/evanslin99)
- [Tavily](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown reports, Python API examples, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report files, call network news APIs, and default to simulated market and financial data unless configured otherwise.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
