## Description: <br>
Real-time voice conversations in Discord voice channels with Claude AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avatarneil](https://clawhub.ai/user/avatarneil) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw or Clawdbot agent join Discord voice channels, transcribe speech, route it through the agent, and speak responses back. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-channel speech can reach the normal agent toolset with broad default access. <br>
Mitigation: Restrict allowedUsers, avoid auto-joining public channels, and require approval before the underlying agent performs sensitive actions from voice prompts. <br>
Risk: Audio or transcripts may be processed by third-party speech providers. <br>
Mitigation: Tell participants when external providers are used, protect provider credentials, and prefer local STT/TTS providers for sensitive conversations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/avatarneil/discord-voice) <br>
- [README](artifact/README.md) <br>
- [Security Model](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Audio, Shell commands, Configuration] <br>
**Output Format:** [Discord voice-channel audio, text transcripts or status messages, and Markdown documentation with JSON-style configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Discord voice permissions, ffmpeg/native audio dependencies, and configured STT/TTS provider credentials; local STT/TTS options can reduce third-party audio processing.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
