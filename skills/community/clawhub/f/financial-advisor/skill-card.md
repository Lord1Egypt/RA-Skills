## Description:

Professional financial analysis and investment advisory skill with institutional-grade valuation capabilities for analyzing stocks, funds, ETFs, market reviews, valuation models, macroeconomic context, geopolitical impact, news intelligence, and HTML report generation with real-time data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxia2013](https://clawhub.ai/user/frankxia2013)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect market data, calculate technical and risk metrics, perform valuation and macro analysis, and produce investment research reports. The skill is intended for informational financial analysis workflows, not as a substitute for personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an opaque encrypted backup file.

Mitigation: Remove the encrypted backup file before installing or redistributing the skill.

Risk: The workflow may install Python dependencies and run scripts that fetch third-party market and news data.

Mitigation: Run the skill in an isolated environment, pin and review dependencies, and confirm third-party data-source terms before use.

Risk: Generated HTML reports may include externally loaded chart assets or insufficiently escaped content.

Mitigation: Open generated reports in a sandboxed or offline context until HTML escaping and CDN integrity are reviewed.

Risk: The skill can produce actionable-looking investment recommendations from volatile or delayed data.

Mitigation: Treat outputs as informational research, validate data freshness and assumptions, and require qualified human review before financial decisions.

## Reference(s):

- [ClawHub Financial Advisor Skill Page](https://clawhub.ai/frankxia2013/skills/financial-advisor)
- [Scripts Guide](SCRIPTS_GUIDE.md)
- [Financial Data Sources Configuration](references/data-sources.md)
- [Financial Indicators Reference](references/financial-indicators.md)
- [Professional Valuation Analysis Methodology](references/valuation-analysis.md)
- [Macroeconomic and Event-Driven Analysis Framework](references/macro-event-framework.md)
- [Trading Discipline and Decision Dashboard](references/trading-discipline.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, plus generated CSV, JSON, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local financial data files, calculated metrics, AI analysis JSON, and interactive HTML reports based on third-party market and news data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
