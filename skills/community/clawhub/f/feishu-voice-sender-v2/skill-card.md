## Description:

Generates Xiaomi MiMo TTS voice audio for Feishu-oriented voice replies after detecting the current messaging channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enderxiao](https://clawhub.ai/user/enderxiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to let an agent convert requested text into voice audio for Feishu-oriented messaging workflows, with channel detection for Feishu and unsupported-channel handling for other platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice generation delegates execution to an unpinned external xiaomi-mimo-tts script with the subprocess environment.

Mitigation: Use only a trusted and protected xiaomi-mimo-tts installation, and restrict the subprocess environment to required variables.

Risk: The current Feishu delivery path can report success before actual Feishu message delivery is implemented and verified.

Mitigation: Do not rely on this version for real Feishu delivery until the send function is implemented, tested, and verified in the target environment.

Risk: Text used for voice generation may pass through external TTS and messaging data flows.

Mitigation: Avoid sending sensitive text unless those external data flows are acceptable for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enderxiao/skills/feishu-voice-sender-v2)
- [Xiaomi MiMo platform](https://platform.xiaomimimo.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Command-line status text and generated OGG audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIMO_API_KEY, ffmpeg, Node.js, and the xiaomi-mimo-tts dependency.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
