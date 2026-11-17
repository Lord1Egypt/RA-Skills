## Description:

Simple CRM for freelancers. Track contacts, projects, invoices, follow-ups, communication history. All through conversation with your agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External freelancers and independent operators use this skill to track client contacts, projects, invoices, follow-ups, communication history, pipeline status, and revenue summaries through an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client, invoice, and revenue records may contain sensitive business information and are stored in a local plain text JSON file.

Mitigation: Treat ./clients/clients.json as sensitive, keep it out of source control, avoid shared workspaces unless file permissions are controlled, maintain backups, and use stronger storage protections for confidential client or financial data.

## Reference(s):

- [Client Tracker README](README.md)
- [Client Tracker on ClawHub](https://clawhub.ai/theshadowrose/skills/client-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-compatible CRM records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores CRM data locally in ./clients/clients.json when the bundled JavaScript helper is used.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
