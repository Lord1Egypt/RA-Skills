## Description:

Zoho Bigin CRM CLI support for searching deals, contacts, and accounts, adding notes, moving deal stages, and updating Bigin records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingodibella](https://clawhub.ai/user/ingodibella)

### License/Terms of Use:


## Use Case:

Developers, operators, and CRM users use this skill to query Zoho Bigin CRM records, inspect pipeline status, manage notes, and prepare clearly authorized record updates through the documented CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic CRM terms such as contacts, accounts, deals, and notes could trigger the skill when the user did not intend to access Zoho Bigin CRM data.

Mitigation: Install and activate the skill only for workflows that intentionally involve Zoho Bigin CRM, and confirm CRM intent before acting on ambiguous requests.

Risk: Commands that create, update, move, or delete CRM records can change business data.

Mitigation: Require clear user confirmation before mutation commands and use the documented BIGIN_WRITE and BIGIN_CONFIRM guardrails for write and delete operations.

Risk: The skill uses Zoho Bigin CRM credentials and can expose CRM data in command results.

Mitigation: Use the configured OAuth credential file only in trusted environments and avoid displaying or logging sensitive customer data beyond the user's requested task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ingodibella/skills/bigin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and CRM result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations are the default; record creation, update, movement, and deletion require explicit user approval and the documented write or confirmation environment variables.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
