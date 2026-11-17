## Description:

Enables OpenClaw's Feishu permission tool so agents can add, view, and remove collaborators for Feishu documents, spreadsheets, folders, and bitables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benleyl](https://clawhub.ai/user/benleyl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to enable Feishu permission management and provide agents with guidance for adding, listing, and removing collaborators on Feishu content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper persistently enables Feishu permission management for every configured Feishu account, which can expand document administration capability beyond the intended account.

Mitigation: Review configured Feishu accounts before installation, enable permission management only for accounts that need it, confirm Feishu app scopes, and back up ~/.openclaw/openclaw.json before running the helper.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/benleyl/skills/feishu-perm-help)
- [Publisher Profile](https://clawhub.ai/user/benleyl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu permission examples and OpenClaw gateway verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
