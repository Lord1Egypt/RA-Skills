## Description:

Enables OpenClaw agents to prepare Feishu group-chat messages, mentions, replies, and optional image posts through a configured user identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clear0](https://clawhub.ai/user/clear0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let OpenClaw agents participate in Feishu group chats, including sending structured post messages, mentioning configured contacts, replying to group activity, and attaching generated or local images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Feishu group messages as the user and may upload images through Feishu APIs.

Mitigation: Require explicit user confirmation before sending messages or uploading images, and keep Feishu app credentials and chat/contact IDs outside published artifacts.

Risk: The helper script emits shell variables and the security guidance warns that sourcing its output as shell code is unsafe.

Mitigation: Review and fix the helper script before installation; parse its structured outputs cautiously instead of sourcing untrusted shell text.

Risk: Broad Feishu OAuth permissions can expose group messages, chat metadata, image upload capability, and user-message sending.

Mitigation: Grant only the Feishu scopes needed for the intended workflow and review authorization state before first use.

Risk: Group messages and display-name prefixes can be spoofed or otherwise untrusted.

Mitigation: Verify authenticated sender IDs and configured contact mappings before treating a group message as coming from a known agent or user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clear0/skills/feishu-group-chat)
- [Publisher profile](https://clawhub.ai/user/clear0)
- [README.md](artifact/README.md)
- [PERMISSIONS.md](artifact/PERMISSIONS.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and helper-script outputs for Feishu post-message content; requires user OAuth, configured contacts, configured groups, and careful handling of local credentials and message content.]

## Skill Version(s):

1.1.1 (source: server release metadata, created 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
