## Description: <br>
Automatic Speech Recognition (ASR) using Coze API. Use when you need to transcribe audio files to text. Supports Chinese audio transcription via Coze's speech-to-text API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe local MP3, WAV, or OGG audio files through the Coze speech-to-text API and receive the transcription as JSON text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are uploaded to Coze for transcription. <br>
Mitigation: Use only audio that is approved for external transcription and avoid sensitive or confidential recordings unless authorization is in place. <br>
Risk: The skill depends on a COZE_API_KEY credential. <br>
Mitigation: Store the API key in the environment, avoid committing it, and rotate it if exposure is suspected. <br>
Risk: The release metadata lists jq, while security guidance also notes that curl is needed. <br>
Mitigation: Confirm both jq and curl are installed before relying on the transcription script. <br>


## Reference(s): <br>
- [Coze Platform](https://www.coze.cn/) <br>
- [Coze audio transcription API endpoint](https://api.coze.cn/v1/audio/transcriptions) <br>
- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/coze-asr) <br>
- [Publisher profile](https://clawhub.ai/user/franklu0819-lang) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [JSON transcription output with status and transcript text printed by the shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COZE_API_KEY, jq, curl, and a local audio file; the optional language parameter defaults to zh.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
