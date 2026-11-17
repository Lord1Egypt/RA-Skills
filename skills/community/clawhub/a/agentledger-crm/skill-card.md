## Description:

Lightweight AI-native CRM for solopreneurs and freelancers that helps track clients, relationships, follow-ups, deal stages, and interaction history in plain text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

Solopreneurs and freelancers use this skill to maintain a local text-file CRM, prepare for client meetings, track follow-ups, review pipeline status, and draft updates to client records for confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle confidential CRM data, including client contact details, pipeline values, relationship notes, and follow-up history.

Mitigation: Review the skill before installing for confidential CRM use, keep sensitive client data in approved local workspaces, and apply any client confidentiality or data protection obligations before syncing or sharing files.

Risk: The optional weekly Telegram cron can repeatedly send CRM summaries to external services.

Mitigation: Enable scheduled Telegram delivery only when external model processing and Telegram delivery are approved for the relevant client data.

Risk: Client markdown files could become an unsafe place for credentials or login secrets.

Mitigation: Do not place passwords, API keys, or login secrets in CRM markdown files; use an approved password manager or secret-sharing process instead.

## Reference(s):

- [Client Relationship Manager - Advanced Patterns](references/advanced-patterns.md)
- [ClawHub skill page](https://clawhub.ai/clawdssen/skills/agentledger-crm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file updates, CRM summaries, meeting briefs, follow-up queues, pipeline reviews, and optional scheduled review commands.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
