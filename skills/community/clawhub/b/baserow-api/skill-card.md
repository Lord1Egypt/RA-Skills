## Description:

Helps agents read and manage Baserow database rows, fields, and tables through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Baserow users can use this skill to query and manage connected databases, including rows, fields, and tables. It also provides guidance for user-approved automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Baserow access runs through Maton, which manages the account connection.

Mitigation: Confirm you trust Maton before connecting; use CLI sign-in when possible and limit access to the needed account.

Risk: Writes and connection changes can alter database content or account access.

Mitigation: Obtain explicit user approval before every write or connection change.

Risk: Hosted functions, triggers, and destinations can continue acting on or forwarding event data.

Mitigation: Review the destination and payload, require approval before enabling automation, and remove it when no longer needed.

## Reference(s):

- [Baserow API documentation](https://baserow.io/api-docs)
- [Baserow Database API](https://baserow.io/user-docs/database-api)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton](https://maton.ai)
- [Baserow skill on ClawHub](https://clawhub.ai/byungkyu/skills/baserow-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include data from the connected Baserow account; minimize exposure of credentials and personal data.]

## Skill Version(s):

1.2.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
