## Description:

Analyzes Amazon product reviews with Sorftime data to identify product pain points, return drivers, improvement suggestions, and customer service response templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdabiao](https://clawhub.ai/user/liangdabiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, Amazon marketplace operators, and product teams use this skill to fetch Amazon product and negative-review data, classify recurring pain points, and generate actionable product, listing, and customer-service recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local Sorftime API key and uses URL-based requests that can expose credentials in shell history, logs, or tool traces.

Mitigation: Use managed secrets or header-based authentication where possible, redact credentials from traces, and avoid pasting raw keys into prompts or commands.

Risk: The skill sends Amazon product and review requests to Sorftime.

Mitigation: Run it only when the user is comfortable using Sorftime for the selected ASIN and marketplace, and avoid submitting data the user is not authorized to process.

Risk: The workflow persists raw product and review responses locally.

Mitigation: Let users choose retention behavior, store reports in an access-controlled location, and delete or redact raw captures when they are no longer needed.

Risk: The artifact includes shell-command examples that interpolate user-provided ASIN and site values.

Mitigation: Validate ASIN and site values before generating commands, quote shell variables, and avoid executing commands assembled from untrusted input.

## Reference(s):

- [Pain Point Taxonomy](artifact/references/painpoint_taxonomy.md)
- [Amazon Review Reply Email Template Library](artifact/assets/email_templates/quality_issue.md)
- [Review Analysis Skill Design Document](artifact/设计文档.md)
- [Sorftime MCP](https://sorftime.com/zh-cn/mcp)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report, structured JSON analysis files, and inline shell/API command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a report directory containing raw SSE captures, parsed review analysis data, and a final report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
