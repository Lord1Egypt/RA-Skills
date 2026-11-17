## Description:

When asked to generate a daily work report, this skill collects work data from CSV, JSON, or Git sources, categorizes items, and produces a structured report in Markdown, HTML, or PDF format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mizhimin](https://clawhub.ai/user/mizhimin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to turn daily task data, work logs, and recent Git activity into a structured end-of-day report. It is intended for work-status summaries that may be reviewed locally, exported, or sent through configured email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe Git path handling could allow shell command execution when Git integration is used.

Mitigation: Use the Git workflow only with trusted repository paths in a restricted workspace until command execution is made argument-safe.

Risk: Generated HTML may include unsanitized report content from CSV, JSON, or Git commit messages.

Mitigation: Avoid HTML, PDF, and email workflows with untrusted input until output escaping and validation are added.

Risk: Email sending can distribute report contents beyond the local workspace.

Mitigation: Require explicit recipient review and send confirmation before enabling email delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mizhimin/skills/enterprise-daily-report)
- [Publisher profile](https://clawhub.ai/user/mizhimin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, or PDF report content with optional command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report content is derived from user-provided CSV, JSON, or Git activity sources; email delivery and HTML/PDF output depend on configuration and optional tooling.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
