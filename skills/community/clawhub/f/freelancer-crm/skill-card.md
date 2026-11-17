## Description:

Autonomous CRM for freelancers that tracks clients, detects follow-up opportunities, generates proposals, tracks invoices, and sends a weekly digest through WhatsApp Bridge or the official API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omermalix](https://clawhub.ai/user/omermalix)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers and small-business operators use this skill to manage client follow-ups, invoice reminders, proposal drafting, client status summaries, and weekly CRM digests from an OpenClaw agent connected to WhatsApp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes client records and stores WhatsApp configuration locally.

Mitigation: Keep config.json and clients.json out of version control, restrict file permissions, and review local storage practices before installing.

Risk: Official API mode can place WhatsApp credentials in config.json.

Mitigation: Move API tokens to a secret manager or environment variable before production use.

Risk: Outbound WhatsApp messages may disclose client or business information.

Mitigation: Review each drafted message before approval and sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omermalix/skills/freelancer-crm)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Plain text, Markdown-style proposal drafts, JSON from CRM CLI commands, and local configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local clients.json and config.json during setup and can send WhatsApp messages after user approval.]

## Skill Version(s):

1.0.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
