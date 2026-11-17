## Description:

Retrieves monthly import and export trend data for a specified HS code, including trade counts, quantities, weights, amounts, and buyer and seller counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade analysts, supply chain managers, market researchers, and developers use this skill to inspect recent monthly customs trends for a product HS code and compare import versus export activity over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an UpKuaJing API key and may read or reference a local key file.

Mitigation: Use an environment variable or protected secret store, avoid printing or sharing the key file, and keep any local key file readable only by the owner.

Risk: Trend queries and account top-up flows can incur fees.

Mitigation: Confirm every paid query or top-up action explicitly before execution and use the documented pricing flow for current fees.

Risk: Error reports can include request or response details that may contain sensitive business data.

Mitigation: Review and redact request parameters, response data, and context before sending an error report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-analysis-trends)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Customs Analysis Trends API Reference](references/customs-analysis-trends-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Structured JSON API responses with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful trend queries include export and import data, fee information, and a request identifier; paid calls require explicit user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
