## Description:

A financial statement analysis and forecasting skill that helps agents collect or accept company financial data, calculate key ratios, create visualizations, and draft structured informational financial reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[interccy-stack](https://clawhub.ai/user/interccy-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to interpret company financial statements, calculate profitability, growth, and health metrics, visualize trends, and draft informational financial analysis reports. The skill is not intended for stock trading recommendations, real-time market data lookup, or bookkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends a remote curl-to-shell installer.

Mitigation: Use the web upload path or independently verify and pin the installer before running it.

Risk: The HTML tool loads third-party browser code that can access entered financial data.

Mitigation: Avoid entering sensitive financial data unless the dependency is trusted, pinned, and acceptable for the deployment environment.

Risk: The generated analysis and forecasts may be mistaken for investment advice.

Mitigation: Keep the output informational, preserve the no-investment-advice disclaimer, and require human review before acting on conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/interccy-stack/skills/financial-report)
- [Chart.js browser dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, generated HTML tool output, and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scenario forecasts, calculated financial ratios, visualization guidance, and informational disclaimers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
