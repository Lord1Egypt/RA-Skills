## Description:

Feishu Voice Sender sends local audio files through the Feishu OpenAPI as inline voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zheyanyan](https://clawhub.ai/user/zheyanyan)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to send selected audio files to a Feishu chat as playable voice messages through an existing Feishu channel configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any readable local file path supplied to it using stored OpenClaw Feishu credentials.

Mitigation: Use it only in trusted workflows, pass an explicit audio file path, and review the selected file before execution.

Risk: An automated agent could send audio to an unintended Feishu recipient if it selects or accepts an untrusted recipient identifier.

Mitigation: Require an explicit recipient value from a trusted operator or environment variable and confirm it before sending.

Risk: The release has limited safeguards around audio validation, file size, and path canonicalization.

Mitigation: Add audio type validation, file size limits, canonical path checks, and a clear upload confirmation or warning.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zheyanyan/skills/feishu-voice-sender-zhe)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, curl, a configured OpenClaw Feishu channel, an explicit audio file path, and a Feishu recipient identifier.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
