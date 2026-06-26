## Description: <br>
Transcribe audio files (ogg, mp3, wav, etc.) using AIMLAPI when the user provides audio messages or local audio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aimlapihello](https://clawhub.ai/user/aimlapihello) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to submit local audio files or voice messages to AIMLAPI for speech-to-text transcription and optionally save the transcript locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to AIMLAPI for transcription. <br>
Mitigation: Use a dedicated AIMLAPI key where possible and avoid transcribing highly sensitive recordings unless AIMLAPI terms fit the use case. <br>
Risk: Transcript files may be saved to a caller-provided local path. <br>
Mitigation: Review output paths before saving transcripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aimlapihello/aiml-voice) <br>
- [AIMLAPI speech-to-text API endpoint](https://api.aimlapi.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration] <br>
**Output Format:** [Plain text transcript with optional local text file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and AIMLAPI_API_KEY; supports model, language, polling interval, timeout, output path, and API key file options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
