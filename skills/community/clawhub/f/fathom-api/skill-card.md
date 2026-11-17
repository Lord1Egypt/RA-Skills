## Description:

Connects to Fathom to retrieve meeting recordings, transcripts, summaries, and action items, and to manage webhooks with user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can retrieve and search Fathom meeting content and, with approval, configure webhooks or automations for meeting notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting recordings, transcripts, and summaries can contain sensitive information.

Mitigation: Prefer read-only actions, authorize only necessary access, and confirm recipients before sharing meeting content.

Risk: Webhooks and hosted automations may persist and forward meeting data to unintended destinations.

Mitigation: Require approval for creation or changes, verify every destination URL and scope, and delete unused webhooks, triggers, functions, and connections.

## Reference(s):

- [ClawHub Fathom skill](https://clawhub.ai/byungkyu/skills/fathom-api)
- [Maton](https://maton.ai)
- [Fathom API documentation](https://developers.fathom.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive meeting content or user-approved webhook settings.]

## Skill Version(s):

1.2.8 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
