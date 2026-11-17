## Description:

Integrates with Content360 to create, schedule, publish, analyze, upload media for, and manage social media content across major social platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noesis-boss](https://clawhub.ai/user/noesis-boss)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and agents use this skill to connect Notion content calendars with Content360, create drafts or scheduled posts, and manage Content360 API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles high-impact publishing workflows and account credentials with weak scoping and safeguards.

Mitigation: Use least-privilege Content360 and Notion credentials, avoid primary account passwords where possible, and review planned publishing actions before live execution.

Risk: Incorrect workspace, database, or platform settings could create or schedule posts in the wrong Content360 or Notion context.

Mitigation: Run with --dry-run first, verify workspace and database identifiers, and confirm target platforms before enabling live synchronization.

Risk: Live scheduling, deletion, or approval actions can affect public social media channels.

Mitigation: Require human review before enabling scheduling, deletion, approval, or production account actions.

## Reference(s):

- [Content360 ClawHub Skill Page](https://clawhub.ai/noesis-boss/skills/content360)
- [Content360 Application](https://app.content360.io)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with Python script, shell commands, environment variable configuration, and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform dry-run previews, platform-filtered syncs, Content360 post creation, and Notion status updates when supplied with credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
