## Description:

Feishu Mood Music detects a user's emotional state, generates matching supportive music, and sends it to a Feishu group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external Feishu users can use this skill to receive mood-matched music in a group chat when they explicitly request music or express qualifying emotional signals. Developers can also use the included scripts to generate MiniMax music audio and deliver it as a Feishu audio message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically generate and send audio to Feishu based on emotional signals.

Mitigation: Use it only in chats where users have opted in, and disable no-mention auto-triggering or require confirmation before generating and sending audio.

Risk: The skill reads local Feishu credentials.

Mitigation: Provide Feishu credentials through a controlled secret path and limit access to the runtime account.

Risk: The security evidence reports a local code-injection bug in the OPENCLAW_CONFIG credential-loading path.

Mitigation: Fix the OPENCLAW_CONFIG parsing bug before use and review the skill before installing.

Risk: The setup flow installs the MiniMax CLI through npm.

Mitigation: Avoid running npm install with elevated privileges.

## Reference(s):

- [MiniMax CLI](https://github.com/MiniMax-AI/cli)
- [MiniMax Music Generation API](https://api.minimaxi.com/v1/music_generation)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated audio file delivery steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or sends mood-matched MP3/audio messages through MiniMax and Feishu integrations.]

## Skill Version(s):

1.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
