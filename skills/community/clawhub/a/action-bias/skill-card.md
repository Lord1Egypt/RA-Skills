## Description:

Action Bias helps restructure agent prompts, cron jobs, and shifts so agents produce outbound actions such as emails, posts, API calls, and code pushes instead of only writing plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crewhaus](https://clawhub.ai/user/crewhaus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to rewrite recurring agent prompts and shifts toward externally visible actions with proof logs, while preserving report-only work when explicitly appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages real outbound actions such as emails, posts, code pushes, directory submissions, and state-changing API calls.

Mitigation: Use explicit approvals for each outbound or state-changing action, restrict available tools and accounts, and limit destinations before deployment.

Risk: Proof logs may contain contact details, platform identifiers, URLs, or API response information.

Mitigation: Redact or minimize action logs, avoid unnecessary personal data, and store logs only where the intended operators can review them.

Risk: Action-first prompting can be misapplied to sessions where a report is the appropriate deliverable.

Mitigation: Keep report-only exceptions for security audits, system health checks, analyst reviews, planning sessions, and human-requested analysis.

## Reference(s):

- [Action Audit Guide](references/action-audit.md)
- [Shift Restructuring Guide](references/shift-restructuring.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with prompt templates, checklists, and inline command placeholders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proof-of-action logging requirements such as URLs, IDs, email recipients, or API response codes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
