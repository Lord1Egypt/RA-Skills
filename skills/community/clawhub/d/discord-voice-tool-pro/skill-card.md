## Description:

Discord语音工具专业版 helps enterprise and community teams operate Discord voice AI assistants with multi-provider STT/TTS, streaming transcription, reconnect handling, channel scheduling, permissions, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, enterprise teams, and community operators use this skill to configure and run Discord voice AI assistants for meetings, support channels, community interaction, and low-latency voice Q&A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Discord audio may be transcribed or processed by third-party STT/TTS providers without clear participant awareness.

Mitigation: Use the skill only in servers and channels where participants know audio may be processed, and document which providers are enabled.

Risk: Discord tokens and STT/TTS API keys can be exposed if they are placed in prompts, files, logs, or command arguments.

Mitigation: Keep credentials in environment variables or a secret manager, rotate them regularly, and review logs for accidental disclosure.

Risk: Auto-join behavior can connect the bot to a voice channel at startup, including when a private or sensitive conversation is underway.

Mitigation: Disable auto-join unless required, limit it to dedicated AI channels, and configure allowed users before deployment.

Risk: Audit logs can contain sensitive operational data such as session times, channel IDs, participants, provider usage, and error details.

Mitigation: Set explicit retention and access rules, encrypt logs where appropriate, and avoid recording secrets or unnecessary personal data.

Risk: The skill uses executable commands for installation and operation, which can introduce command execution risk.

Mitigation: Review commands before execution, restrict operations to known tooling and expected channel IDs, and avoid composing shell commands from untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-voice-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON/JSON5 configuration examples, shell command examples, and structured JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational status, execution logs, configuration values, and error information; secrets should remain in environment variables.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
