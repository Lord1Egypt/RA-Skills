## Description:

飞书语音消息自动回复技能 - 使用 Edge TTS 生成语音并通过飞书 API 发送

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmx0632](https://clawhub.ai/user/xmx0632)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to turn short text responses into Chinese voice audio and send them as native Feishu voice messages when a voice reply or voice notification is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send voice messages silently after generation.

Mitigation: Require explicit user confirmation or tighter trigger rules before allowing the skill to send Feishu voice messages.

Risk: Text and generated audio may pass through Microsoft Edge TTS, OpenClaw Gateway, and Feishu.

Mitigation: Do not use the skill with secrets, regulated data, or sensitive business messages unless that data flow has been approved.

Risk: The installer fetches the edge-tts dependency from a package index without a pinned version.

Mitigation: Install in an isolated environment from the skill directory and pin the dependency version before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xmx0632/skills/feishu-voice-reply)
- [edge-tts on PyPI](https://pypi.org/project/edge-tts/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate MP3 voice files and send them through Feishu when invoked in an OpenClaw environment.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
