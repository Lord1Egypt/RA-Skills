## Description:

Helps agents read, create, update, and delete Airtable records and manage bases through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents assisting users with Airtable can query bases and records, make approved changes, and set up user-requested automations through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Airtable grants Maton access to data within the approved scopes.

Mitigation: Use OAuth, approve the connection explicitly, and grant only the scopes needed for the task.

Risk: Record changes and deletions can alter or remove user data.

Mitigation: Prefer read-only operations and confirm each write or delete before execution.

Risk: Triggers can continuously forward future event data to a destination.

Mitigation: Review and approve the trigger and its destination before activation; remove it when no longer needed.

## Reference(s):

- [ClawHub Airtable skill](https://clawhub.ai/byungkyu/skills/airtable)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Airtable API overview](https://airtable.com/developers/web/api/introduction)
- [Airtable formula reference](https://support.airtable.com/docs/formula-field-reference)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions operate within the user's authorized Airtable connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
