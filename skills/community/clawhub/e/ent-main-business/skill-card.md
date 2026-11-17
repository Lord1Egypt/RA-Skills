## Description:

基于企业名称查询工商信息和主营业务数据，生成专业详尽的主营业务与核心产品解析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daviddatamining](https://clawhub.ai/user/daviddatamining)

### License/Terms of Use:

MIT-0

## Use Case:

Investment, business development, due diligence, and partner-analysis users can provide a company name, resolve the intended company, fetch main-business data, and receive a structured report about the company's business, products, markets, and competitive position.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names and enterprise IDs are sent to an external service over plaintext HTTP.

Mitigation: Use only when that data sharing is acceptable; prefer an updated HTTPS endpoint before handling sensitive company research.

Risk: API request and response details may appear in logs.

Mitigation: Disable verbose logging or review logs for sensitive business data before using the skill in shared environments.

Risk: External lookup results may be incomplete, unavailable, or contain missing fields.

Mitigation: Require user confirmation when multiple companies match and mark missing or unverified report fields as pending verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daviddatamining/skills/ent-main-business)
- [Publisher profile](https://clawhub.ai/user/daviddatamining)

## Skill Output:

**Output Type(s):** [Markdown, Text, API Calls, Guidance]

**Output Format:** [Markdown report with tables and concise narrative sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user to choose from multiple company candidates before producing the final report.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-06-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
