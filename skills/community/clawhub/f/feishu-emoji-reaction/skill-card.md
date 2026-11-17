## Description:

Helps an agent add and interpret Feishu emoji reactions, choose when to respond or stay silent, and learn new reaction types with cultural context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chargiie](https://clawhub.ai/user/chargiie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make Feishu-enabled agents react to messages, interpret user reactions, and decide when a short reply or silence is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic reaction behavior can send unintended social signals in shared or business Feishu workspaces.

Mitigation: Review before installation, require explicit user or workspace opt-in, and disable or constrain automatic reaction learning where it is not expected.

Risk: Credential-bearing scripts use Feishu app identifiers and secrets from the local environment.

Mitigation: Use the smallest required Feishu app permission, keep credentials out of shell history and broad environments, and rotate secrets if exposed.

Risk: Optional CLI and SDK paths may rely on unpinned npm packages or locally installed tooling.

Mitigation: Prefer audited, pinned dependency versions and avoid optional npm CLI or SDK paths unless they can be reviewed in the deployment environment.

Risk: Local learning state may persist user-derived emoji behavior and cultural context.

Mitigation: Store learned reaction notes only in approved locations, review them periodically, and avoid retaining sensitive conversation context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chargiie/skills/feishu-emoji-reaction)
- [Feishu emoji reference](references/emoji-list.md)
- [Feishu message reaction API documentation](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/emojis-introduce)
- [OpenClaw message tool](https://docs.openclaw.ai/tools/messaging)
- [OpenClaw Feishu channel configuration](https://docs.openclaw.ai/channels/feishu)

## Skill Output:

**Output Type(s):** [API Calls, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript message calls, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit NO_REPLY to suppress a text response after adding a reaction.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
