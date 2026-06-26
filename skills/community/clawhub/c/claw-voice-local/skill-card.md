## Description: <br>
Convert text to offline Telegram voice messages using piper TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[photon78](https://clawhub.ai/user/photon78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn agent text into local Piper-generated OGG Opus audio and optionally deliver it as a Telegram voice note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated voice audio and optional captions can leave the local machine when Telegram delivery is used. <br>
Mitigation: Use the Telegram send feature only for intended recipients, protect bot credentials, and avoid sending sensitive text or captions. <br>
Risk: The skill is framed as local/offline, but Telegram upload requires network access and bot credentials. <br>
Mitigation: Treat local TTS generation and Telegram delivery as separate behaviors; enable credentials and network access only when message delivery is required. <br>
Risk: Generated output paths can overwrite existing files when audio generation is directed to a fixed path. <br>
Mitigation: Use temporary or dedicated output paths and avoid pointing output arguments at important existing files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/photon78/claw-voice-local) <br>
- [Piper TTS](https://github.com/rhasspy/piper) <br>
- [Piper voice models](https://huggingface.co/rhasspy/piper-voices) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, audio files, API calls, guidance] <br>
**Output Format:** [Command-line text, OGG Opus audio files, and Telegram voice messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Piper TTS and ffmpeg for audio generation; Telegram delivery requires bot credentials and network access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
