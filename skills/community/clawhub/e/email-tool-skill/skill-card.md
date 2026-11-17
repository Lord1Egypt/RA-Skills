## Description:

Helps an agent send plain-text email by generating and running a standalone Python stdlib smtplib script against smtp.yeah.net:465 with the documented workspace SMTP account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgy2e](https://clawhub.ai/user/wgy2e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when they intentionally want an agent to create and run a standalone Python script that sends a plain-text email through the documented yeah.net SMTP account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds live SMTP credentials for validates@yeah.net, allowing anyone with access to send email through that account.

Mitigation: Rotate or remove the embedded SMTP password before installing, sharing, logging, or storing the skill outside a trusted private workspace.

Risk: The skill enables arbitrary outbound email through the documented account without enough guardrails.

Mitigation: Limit use to intended recipients and review the generated recipient, subject, and body before execution.

## Reference(s):

- [Python smtplib documentation](https://docs.python.org/3/library/smtplib.html)
- [ClawHub skill page](https://clawhub.ai/wgy2e/skills/email-tool-skill)
- [Publisher profile](https://clawhub.ai/user/wgy2e)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python stdlib smtplib and requires python3; sends plain-text email via SMTP_SSL when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
