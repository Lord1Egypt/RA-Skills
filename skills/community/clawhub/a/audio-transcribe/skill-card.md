## Description: <br>
Auto-transcribes audio files locally with faster-whisper and selectable Whisper model sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AKTheKnight](https://clawhub.ai/user/AKTheKnight) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to transcribe voice messages or supported audio files into readable text without an API key. It is useful when local transcription is preferred and the user can manage downloaded model files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice messages and audio files may contain sensitive information that becomes easier to read and share after transcription. <br>
Mitigation: Treat source audio and generated transcripts as sensitive, and confirm where transcripts are stored or displayed before enabling automatic transcription. <br>
Risk: The skill depends on faster-whisper and downloaded model files at runtime. <br>
Mitigation: Install only in environments where the faster-whisper package and model download source are trusted. <br>


## Reference(s): <br>
- [ClawHub Audio Transcribe release page](https://clawhub.ai/AKTheKnight/audio-transcribe) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/AKTheKnight) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript with language and confidence metadata, plus CLI status and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Model size is configured in the script; faster-whisper model files download automatically on first use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
