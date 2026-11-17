## Description:

Send voice/audio messages to Feishu (Lark) chats using TTS, using OpenAI TTS when OPENAI_API_KEY is set and macOS say as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zihui](https://clawhub.ai/user/zihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send spoken Feishu or Lark messages from an agent workflow, including direct chats and group chats. It is intended for macOS environments with Feishu bot credentials and audio tooling installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message text and generated audio may be sent to Feishu recipients and to OpenAI when OPENAI_API_KEY is configured.

Mitigation: Use non-sensitive content, choose recipients explicitly, and avoid setting OPENAI_API_KEY when local macOS speech is sufficient.

Risk: The skill reads Feishu bot credentials from the user's OpenClaw configuration.

Mitigation: Run with ordinary user privileges and ensure the Feishu bot has only the permissions and recipient scope required for the message.

Risk: Security evidence reports unsafe shell handling in the bundled script.

Mitigation: Review or revise the script before installation, including mktemp usage, cleanup traps, JSON serialization, and receive_id_type validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zihui/skills/feishu-macos-voice)
- [OpenAI audio speech API endpoint](https://api.openai.com/v1/audio/speech)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu voice-message guidance and command invocations that may send generated audio through Feishu and, when configured, OpenAI.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
