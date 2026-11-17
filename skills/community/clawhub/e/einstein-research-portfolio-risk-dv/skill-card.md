## Description:

Performs a comprehensive, portfolio-level risk analysis by calculating Value at Risk, max drawdown, correlation, historical stress tests, beta, and concentration risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze equity portfolio risk from holdings data, including VaR, CVaR, drawdown, stress-test exposure, correlation, beta, and concentration signals. The resulting reports support risk review and portfolio monitoring, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive portfolio holdings and writes detailed financial reports locally.

Mitigation: Run it in a private working directory, avoid shared or synced report folders, and limit access to generated reports.

Risk: The security review flags under-disclosed investment action recommendations.

Mitigation: Treat action items as informational risk analysis and review outputs with appropriate financial judgment before acting.

Risk: The script depends on third-party market data and Python packages.

Mitigation: Install dependencies in a virtual environment with pinned versions when possible and review fetched data quality before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-portfolio-risk-dv)
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai)
- [Risk Methodologies Reference](references/risk_methodologies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language guidance with Markdown reports, JSON report files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local portfolio risk reports from user-supplied holdings and Yahoo Finance market data.]

## Skill Version(s):

0.1.0 (source: server release metadata; source skill frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
