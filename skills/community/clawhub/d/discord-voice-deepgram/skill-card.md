## Description:

Voice-channel conversations in Discord using Deepgram streaming STT and low-latency TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adriel1006](https://clawhub.ai/user/adriel1006)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this Clawdbot/OpenClaw plugin to let an agent join Discord voice channels, transcribe permitted speakers with Deepgram, route transcripts to the agent, and play replies back through Deepgram TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unintended speakers may be captured in a Discord voice channel.

Mitigation: Configure a primary speaker or explicit allowlist using Discord user IDs, and disable voice speaker switching unless the workflow requires it.

Risk: Voice transcripts may expose sensitive conversation content through logs.

Mitigation: Remove or tightly restrict transcript logging and use low-retention, access-controlled logs for any retained voice session data.

Risk: Voice prompts may reach the agent's full toolset.

Mitigation: Run Discord voice sessions with a constrained agent profile or isolate the voice agent from high-impact tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adriel1006/skills/discord-voice-deepgram)
- [ClawHub publisher profile](https://clawhub.ai/user/adriel1006)
- [Deepgram speech-to-text endpoint](https://api.deepgram.com/v1/listen)
- [Deepgram text-to-speech endpoint](https://api.deepgram.com/v1/speak)

## Skill Output:

**Output Type(s):** [text, audio, configuration, shell commands, guidance]

**Output Format:** [Text responses, JSON status payloads, setup snippets, and Ogg/Opus voice playback in Discord.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Discord and Deepgram credentials; voice behavior depends on configured speaker controls.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
