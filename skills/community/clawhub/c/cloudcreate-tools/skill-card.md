## Description:

Enumerates CloudCreate.ai in-browser tool capabilities and builds production or local shareable URLs with English or Chinese locale paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangzhibin](https://clawhub.ai/user/zhangzhibin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to map file or creative-tool intents to CloudCreate.ai browser tools and generate production or self-hosted deep links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide agents to run mutable npm code through npx --yes @cloudcreate/cli.

Mitigation: Prefer manually constructed URLs or a pinned, reviewed CLI version, and avoid running mutable npm commands in sensitive workspaces.

Risk: The skill exposes a watermark-removal route that can be misused on content the user is not authorized to modify.

Mitigation: Use watermark removal only for content the user owns or is otherwise authorized to edit.

Risk: Using the public CloudCreate.ai site may be unsuitable for sensitive files or environments with strict host-trust requirements.

Mitigation: Use the documented local or self-hosted route when stricter privacy or compliance boundaries are required.

## Reference(s):

- [CloudCreate.ai](https://cloudcreate.ai)
- [CloudCreate.ai AI Spec](https://cloudcreate.ai/en/ai-spec)
- [CloudCreate.ai Source Repository](https://github.com/cloudcreate-ai/cloudcreate.ai)
- [ClawHub Skill Page](https://clawhub.ai/zhangzhibin/skills/cloudcreate-tools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with URLs and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locale-specific production URLs or localhost URLs for self-hosted use.]

## Skill Version(s):

1.0.4 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
