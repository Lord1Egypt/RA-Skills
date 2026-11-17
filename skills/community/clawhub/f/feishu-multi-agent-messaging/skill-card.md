## Description:

Guides agents through Feishu group-chat collaboration with multiple bots, including message handoff, group mentions, direct messages, and per-bot user ID mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wulinsquarelikui](https://clawhub.ai/user/wulinsquarelikui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to coordinate OpenClaw multi-agent work over Feishu chats, especially when separate bots need to send group updates, @mentions, and direct messages under their own identities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu bot secrets, per-bot open_id mappings, message contents, screenshots, or logs may expose sensitive workspace information.

Mitigation: Treat appSecret values, open_id mappings, message contents, and screenshots or logs containing them as sensitive; store and share them only through approved channels.

Risk: Incorrect accountId or open_id mappings can send private messages or group @mentions from the wrong bot identity or to the wrong recipient.

Mitigation: Verify accountId values and recipient IDs against the maintained per-bot mapping table before sending direct messages or group mentions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wulinsquarelikui/skills/feishu-multi-agent-messaging)
- [README](artifact/README.md)
- [Architecture](artifact/docs/architecture.md)
- [User ID Mapping](artifact/docs/id-mapping.md)
- [Group Collaboration Workflow](artifact/docs/workflow.md)
- [Troubleshooting](artifact/docs/troubleshooting.md)
- [OpenClaw Configuration Example](artifact/examples/openclaw.json)
- [Message Samples](artifact/examples/message-samples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and Feishu message command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable code or generated files are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
