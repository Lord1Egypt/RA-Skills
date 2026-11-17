## Description:

Formats a completed request's task trace and results into a concise debugging report with call outcomes and actionable fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeypetrakov](https://clawhub.ai/user/sergeypetrakov)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill when a user explicitly requests a breakdown of a recent run, to explain tool-call outcomes, errors, and possible fixes without inventing unavailable trace details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reporting recent task results and trace details in chat could expose secrets or sensitive data from earlier work.

Mitigation: Avoid invoking the skill after sensitive tasks, and review trace details before sharing the report.

## Reference(s):

- [Debug-trace on ClawHub](https://clawhub.ai/sergeypetrakov/skills/debug)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown debug report with trace details and summary bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only available completed-task traces; states when the requested trace is unavailable.]

## Skill Version(s):

1.0.3 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
