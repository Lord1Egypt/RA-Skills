## Description:

Helps agents manage GetResponse contacts, marketing campaigns, messages, and automations through a connected account, with approval required for changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agents use this skill to review and manage GetResponse campaigns, contacts, messages, and automations through an authorized account. Changes and outbound messages require explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may reach real contacts or be sent to the wrong audience.

Mitigation: Confirm the audience, content, and timing before sending newsletters, SMS, or transactional emails.

Risk: Deletes, imports, and workflow changes may alter contacts or campaigns.

Mitigation: Review the target and intended effect, and obtain explicit approval before each change.

Risk: Functions, triggers, and destinations can create ongoing automated data flows.

Mitigation: Review and approve the function, trigger, or destination before enabling it.

## Reference(s):

- [GetResponse skill on ClawHub](https://clawhub.ai/byungkyu/skills/getresponse)
- [GetResponse API documentation](https://apidocs.getresponse.com/v3)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a Maton account, and user approval before changes.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
