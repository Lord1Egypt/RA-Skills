## Description:

Personal CRM for managing contacts, relationships, and follow-ups using markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xz-cn](https://clawhub.ai/user/xz-cn)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to maintain a lightweight personal CRM in markdown files, including contacts, companies, events, interaction notes, follow-ups, reminders, and CSV or vCard import/export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists personal contact details and notes into local searchable memory.

Mitigation: Avoid storing secrets or highly sensitive personal details, and review what will be indexed before adding contacts.

Risk: Imports can transform untrusted CSV, vCard, or LinkedIn export data into CRM contact files.

Mitigation: Use the documented dry-run preview and inspect imported contact data before creating or overwriting files.

Risk: Exports can write contact data to user-selected paths where it may be shared or retained unexpectedly.

Mitigation: Export to a dedicated CRM export folder and review file permissions and destination before sharing.

## Reference(s):

- [CRM Schema Reference](artifact/references/schema.md)
- [ClawHub skill page](https://clawhub.ai/xz-cn/skills/clawdbot-crm-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, command-line text, CSV, vCard, and JSON reminder data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local contact files under memory/contacts and can import or export contact data.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
