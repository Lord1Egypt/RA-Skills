## Description:

Feishu Voice Chat helps an agent transcribe Feishu voice messages with Volcengine ASR and generate OGG voice replies with Volcengine TTS for Feishu audio messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-neo](https://clawhub.ai/user/li-neo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add voice-message handling to Feishu-connected agents: inbound audio can be transcribed to text, and requested spoken replies can be synthesized as Feishu-compatible audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASR file handling may process unintended local audio paths if an agent receives untrusted file paths or message IDs.

Mitigation: Restrict ASR input to the intended Feishu inbound media directory, resolve paths before use, reject symlinks, and validate audio files before submission.

Risk: Generated Feishu message command strings can look executable and may be unsafe to pass through unreviewed tool-calling flows.

Mitigation: Prefer structured message data over executable-looking command strings and require the agent runtime to validate message action, channel, message ID, and media path.

Risk: Volcengine credentials are required for ASR and TTS requests.

Mitigation: Use a dedicated Volcengine token with minimal scope and keep required credential environment variables out of chat transcripts and logs.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Pin runtime dependencies before production deployment and review updates before upgrading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/li-neo/skills/feishu-voice-chat)
- [ClawHub Publisher Profile](https://clawhub.ai/user/li-neo)
- [Volcengine Speech Service Console](https://console.volcengine.com/speech/app)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [JSON status objects, OGG audio files, and Feishu message command strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Volcengine speech credentials and is intended for Feishu/OpenClaw audio message workflows.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
