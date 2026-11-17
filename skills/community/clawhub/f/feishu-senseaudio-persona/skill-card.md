## Description:

This skill helps an agent run a Feishu persona voice companion that initializes a user-defined character, transcribes incoming speech with SenseAudio ASR, generates persona-aligned reply text, synthesizes speech with SenseAudio TTS, and sends Feishu-native OPUS audio messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klilyz](https://clawhub.ai/user/klilyz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create a customizable role-play or companion voice assistant inside Feishu private chats. The skill supports first-use persona setup, text or voice input handling, persona prompt generation, SenseAudio speech processing, and Feishu voice-message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Feishu chat text and audio can be processed by external services.

Mitigation: Require user consent before use, disclose SenseAudio processing, and restrict the bot to intended chats or workspaces.

Risk: Broad chat triggers can cause the bot to process messages outside the intended role-play context.

Mitigation: Limit deployment scope, bind operation to approved chat IDs, and review access before installing in shared or sensitive workspaces.

Risk: Runtime dependency installation and configurable endpoints can increase supply-chain and data-routing risk.

Mitigation: Install and pin dependencies during setup, avoid runtime package installs in managed deployments, and allowlist approved SenseAudio HTTPS endpoints.

Risk: Persona state and generated audio files may persist locally longer than users expect.

Mitigation: Store persona data per user or chat and delete generated audio files after sending unless retention is explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/klilyz/skills/feishu-senseaudio-persona)
- [OpenClaw homepage metadata](https://clawhub.ai/Anightmare2/feishu-voice-skill)
- [SenseAudio API base](https://api.senseaudio.cn)
- [SenseAudio ASR endpoint](https://api.senseaudio.cn/v1/asr)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance with inline shell commands and plain-text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime workflow can create WAV and OPUS audio files for Feishu delivery; successful send-voice execution suppresses normal text output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
