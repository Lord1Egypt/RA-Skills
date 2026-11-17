## Description:

Sends rich collaboration-platform cards to Feishu users or groups with Markdown, titles, colored headers, buttons, images, and persona-styled messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and automation workflows use this skill to send formatted notifications, reports, alerts, and assistant messages to collaboration-platform users or groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send externally visible messages and files to collaboration-platform users or groups.

Mitigation: Review each recipient, message body, Markdown file, image path, and button URL before sending.

Risk: Broad invocation guidance could encourage use outside card-notification workflows.

Mitigation: Use the skill only for intended Feishu or collaboration-platform message sending, not unrelated ETL, analysis, extraction, or system automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feishu-card-builder)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for sending text, Markdown files, images, buttons, and persona-styled collaboration cards.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
