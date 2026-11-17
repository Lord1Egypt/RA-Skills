## Description:

Use this skill for GoHighLevel CRM work for realtors: contact lookup and updates, opportunity/pipeline actions, conversation messaging, calendar slots, and workflow enrollment using GoHighLevel API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

External real estate teams and their agents use this skill to manage GoHighLevel CRM workflows for lead intake, contact updates, pipeline follow-up, appointment context, messaging, and workflow enrollment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a live CRM with a long-lived GoHighLevel private integration token.

Mitigation: Use a narrowly scoped token, keep credentials out of chat and logs, and rotate the token on a regular schedule.

Risk: Broad list commands can expose customer records, conversations, invoices, transactions, or other CRM data in terminal or agent logs.

Mitigation: Prefer targeted read commands and run broad list commands only when the user explicitly asks for that scope of data.

Risk: Write actions can delete contacts, send messages, change workflows, create appointments, create invoices, or publish social posts.

Mitigation: Require explicit user confirmation before destructive, external-facing, billing-related, or workflow-changing actions.

Risk: Troubleshooting steps may display environment variables or API responses containing sensitive data.

Mitigation: Mask secrets before sharing output and avoid commands that print raw tokens.

## Reference(s):

- [Contacts API Reference](references/contacts.md)
- [Opportunities & Pipelines API Reference](references/opportunities.md)
- [Conversations & Messaging API Reference](references/conversations.md)
- [Calendars & Appointments API Reference](references/calendars.md)
- [Troubleshooting Reference](references/troubleshooting.md)
- [GoHighLevel API Docs](https://marketplace.gohighlevel.com/docs/)
- [GoHighLevel OpenAPI Specs](https://github.com/GoHighLevel/highlevel-api-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return CRM records, API response JSON, setup guidance, or command suggestions depending on the requested workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
