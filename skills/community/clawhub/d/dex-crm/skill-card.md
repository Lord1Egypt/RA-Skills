## Description:

Manage Dex personal CRM contacts, notes, and reminders, including contact lookup, note creation, reminder management, and contact detail retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaybna](https://clawhub.ai/user/jaybna)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Dex personal CRM data from an agent, including searching contacts, viewing contact details, adding notes, creating or completing reminders, and archiving contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Dex API key can allow the agent to read and modify CRM contacts, notes, and reminders.

Mitigation: Install only when that access is acceptable, keep DEX_API_KEY in secret configuration, and require explicit confirmation before create, update, delete, or archive actions.

Risk: The cleanup script can bulk archive contacts that match newsletter or automated-sender patterns.

Mitigation: Run the cleanup script with --dry-run first, review matched contacts manually, and use an explicit confirmation or allowlist before archiving.

Risk: Delete and update examples can permanently alter CRM records or CRM history.

Mitigation: Prefer reversible archive or completion workflows where available, verify contact and record IDs before mutation, and preserve summaries of changed records.

## Reference(s):

- [Dex](https://getdex.com)
- [Dex API Base](https://api.getdex.com/api/rest)
- [Dex API Settings](https://getdex.com/settings/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DEX_API_KEY environment variable and can read or modify Dex CRM contacts, notes, and reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
