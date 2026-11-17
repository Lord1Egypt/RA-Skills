## Description:

Browse Airtable bases and tables, inspect records, create records, and manage fields, comments, and table actions via the Airtable API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Airtable bases, read table data, and create or modify records, fields, comments, and tables through a connected Airtable account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external ClawLink plugin that handles OAuth-backed Airtable access.

Mitigation: Review the plugin and its requested Airtable scopes before installation, and revoke Airtable OAuth access when the skill is no longer needed.

Risk: Write and delete actions can change or permanently remove Airtable data.

Mitigation: Use an Airtable account with the narrowest practical access and confirm the target resource and intended effect before every create, update, or delete operation.

## Reference(s):

- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
- [Airtable Base Schema](https://airtable.com/developers/web/api/schema)
- [Airtable Records](https://airtable.com/developers/web/api/records)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/airtable-records)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Airtable API calls through ClawLink tools after user connection and confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
