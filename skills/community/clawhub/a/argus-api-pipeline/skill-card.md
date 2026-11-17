## Description:

Connects multiple REST APIs, fetches and transforms data, and pushes it to a live Google Sheets dashboard that auto-updates on a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and business teams use this skill to connect multiple REST APIs, transform and merge data, and maintain an automatically updated Google Sheets dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google service account credentials or connected API tokens could grant broader access than the pipeline needs.

Mitigation: Use least-privilege API credentials and share the Google service account only with the intended Sheet.

Risk: Failed-write buffers and run logs may contain business, financial, customer, or operational data.

Mitigation: Clarify where buffers and logs are stored, restrict access to them, and define when they are deleted.

Risk: Invalid API responses or failed Google Sheets writes could produce stale or incorrect dashboard data.

Mitigation: Validate API response schemas before writing, retry failed Sheets writes as documented, and review failure alerts and run logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neo1307/skills/argus-api-pipeline)
- [ClawHub publisher profile](https://clawhub.ai/user/neo1307)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with setup steps, configuration details, and generated pipeline instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Google Sheets dashboard updates, pipeline run logs, and failure alerts when implemented by an agent.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
