## Description:

AI-powered financial data analysis covering financial statements, KPI tracking, market trends, data visualization, stock screening, and automated reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts, finance teams, and business users can analyze financial statements, KPIs, and market data, then create dashboards and reports. The skill also provides stock screening and technical-analysis frameworks with risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Python, data-analysis, and SQL activation triggers may cause the skill to run for requests outside its intended finance-analysis scope.

Mitigation: Use finance-specific trigger phrases and review the skill's activation behavior in the intended agent environment.

Risk: The security scan covered only one of two components, and the manifest issue and missing reference remain unresolved.

Mitigation: Review both release components and resolve the noted manifest and reference gaps before relying on the scan for deployment confidence.

Risk: Stock screening and investment-analysis examples may produce misleading conclusions if market data is stale or incomplete.

Mitigation: Check inputs against current, reliable market sources and present generated analysis as informational with clear uncertainty and risk notes.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/gechengling/finance-data-analysis)
- [ClawHub skill release](https://clawhub.ai/gechengling/skills/finance-data-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown reports, tables, dashboard specifications, and Python-style code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Varies by request; may include financial ratios, trend summaries, screening criteria, recommendations, and risk notes.]

## Skill Version(s):

5.0.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
