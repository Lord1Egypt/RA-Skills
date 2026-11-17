## Description:

Generate or review Alibaba Cloud WAF 3.0 security operations reports, customer assessments, rule-tuning reports, and focused false-positive or false-negative investigations using WAF OpenAPI, SLS traffic logs, authorized read-only verification, or user-supplied offline WAF samples and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and WAF operations teams use this skill to generate evidence-based Alibaba Cloud WAF reports, security patrols, API Security reviews, BOT analysis, and focused false-positive or false-negative investigations. It supports offline user-supplied evidence and authorized read-only online collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional IP ownership lookups can send queried IP addresses to ipinfo.io.

Mitigation: Skip these lookups or require separate approval when customer IP telemetry or incident indicators must remain inside the approved environment.

Risk: The skill can guide live cloud evidence collection for WAF assessments.

Mitigation: Install and use it only for authorized assessments with a dedicated least-privilege read-only RAM identity and an existing authenticated CLI context.

Risk: Assessment materials may contain credentials, tokens, cookies, customer identifiers, or other sensitive values.

Mitigation: Avoid supplying raw credentials and redact sensitive values in all outputs and artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-report)
- [Assessment methodology](references/methodology.md)
- [OpenAPI and SLS command reference](references/openapi-cheatsheet.md)
- [Required RAM permissions](references/ram-policies.md)
- [SLS query cookbook](references/sls-query-cookbook.md)
- [WAF attack analysis checklist](references/attack-analysis-checklist.md)
- [OWASP API Security Top 10 query guide](references/owasp-api-top10-queries.md)
- [Report template](assets/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with pipe tables, inline shell commands, SQL snippets, and concise assessment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redacts sensitive values, preserves evidence scope, and labels unsupported conclusions as unverifiable.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
