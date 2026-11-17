## Description:

OpenClaw configuration monitoring that tracks Gateway status, configuration change frequency, backup health, installed configuration skills, and log errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samlinfj](https://clawhub.ai/user/samlinfj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw Gateway configuration health, review change and backup status, and produce configuration health reports with response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends persistent scheduled execution of local monitoring commands.

Mitigation: Review the referenced local scripts before use and add cron jobs only when persistent monitoring is intentional and removable.

Risk: The backup cleanup example can delete files without a separate review step.

Mitigation: Inspect candidate backup files first and replace the direct deletion pipeline with a safer deletion flow.

Risk: The monitoring and rollback procedures rely on local scripts that are referenced but not bundled with the artifact.

Mitigation: Confirm the expected scripts exist locally and review their behavior before running status, rollback, logging, or report commands.

## Reference(s):

- [Config Monitor skill page](https://clawhub.ai/samlinfj/skills/config-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitoring procedures, report structure, alert-response steps, and scheduled monitoring command examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
