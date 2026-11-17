## Description:

Sends local image, voice, video, or file media to DingTalk users or group chats when the user explicitly asks for DingTalk delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shyzhen](https://clawhub.ai/user/shyzhen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send local media files through DingTalk after confirming the file path, target user or group ID, and DingTalk account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local file may be sent to the wrong DingTalk user, group, or account.

Mitigation: Confirm the exact file path, recipient or group ID, and DingTalk account before each send, especially in multi-account environments.

Risk: Sensitive files or DingTalk credentials may be exposed through unnecessary sends, environment output, or debug logs.

Mitigation: Avoid sending sensitive files unless necessary, use a least-privilege DingTalk app, and do not share unredacted environment or log output containing DINGTALK credentials.

Risk: Automatic account or target-type detection may be ambiguous in multi-account or unusual target-ID scenarios.

Mitigation: Specify the account ID and use --group or --user when automatic detection is not reliable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shyzhen/skills/dingtalk-send-media)
- [DingTalk Open Platform](https://open.dingtalk.com/)
- [DingTalk OpenClaw connector issue 456](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues/456)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands; the execution script returns JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python or python3, DingTalk credentials, a local file path, a target user or group ID, and optional account, media type, group/user, or debug flags.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
