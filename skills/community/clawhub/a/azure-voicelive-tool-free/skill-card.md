## Description:

使用 Azure VoiceLive 构建基础实时语音 AI 应用，支持文本和音频输出与基本会话管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to build basic Azure VoiceLive real-time voice assistants, text-to-speech interactions, and speech transcription flows with environment-variable API key configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to install packages, run Python code, and use an Azure key.

Mitigation: Review generated commands before execution, keep API keys in environment variables, and limit use to Azure VoiceLive tasks.

Risk: VoiceLive workflows may transmit text or microphone audio to Azure.

Mitigation: Avoid sensitive speech data unless there is consent and the Azure resource is approved for the data involved.

Risk: The security evidence says the skill describes broader actions than its Azure VoiceLive examples justify.

Mitigation: Restrict the skill to VoiceLive setup, session configuration, audio streaming, and transcription workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-voicelive-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Azure endpoint and API key environment variables; may propose package installation and Python execution for Azure VoiceLive tasks.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
