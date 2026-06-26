## Description: <br>
End-to-end voice workflow with Deepgram STT and TTS for transcribing voice messages, generating spoken replies, and building a shell-based audio pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MengBad](https://clawhub.ai/user/MengBad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe input audio with Deepgram, optionally generate MP3 spoken replies, and return structured outputs for chat or bot automation workflows. It is especially suited to shell-based Telegram, QQ, OneBot, and Chinese speech pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio inputs and reply text are sent to Deepgram for speech-to-text and text-to-speech processing. <br>
Mitigation: Use the skill only for content that may be shared with Deepgram, and review the applicable data handling requirements before processing sensitive audio or text. <br>
Risk: Transcript text, raw API JSON, and MP3 outputs are written to local paths and may contain sensitive content. <br>
Mitigation: Choose output directories deliberately and clean up transcript, JSON, and MP3 files after use when they contain sensitive information. <br>
Risk: The scripts can read DEEPGRAM_API_KEY from /root/.openclaw/.env if the environment variable is not already set. <br>
Mitigation: Use a scoped Deepgram API key and confirm that /root/.openclaw/.env is an approved secret source in the target environment. <br>


## Reference(s): <br>
- [STT Notes](references/stt-notes.md) <br>
- [TTS Notes](references/tts-notes.md) <br>
- [Pipeline Notes](references/pipeline-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/MengBad/deepgram-voice-workflow) <br>
- [Publisher Profile](https://clawhub.ai/user/MengBad) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Transcript text files, raw API JSON files, MP3 audio files, and pipeline JSON printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPGRAM_API_KEY; default STT output includes transcript text plus raw JSON, default TTS output is MP3, and the full pipeline reports output paths and transcript content.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
