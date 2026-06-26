## Description: <br>
Transcribe audio to timestamped lyrics using OpenAI Whisper or ElevenLabs Scribe API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DumoeDss](https://clawhub.ai/user/DumoeDss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to transcribe songs or other audio into timestamped lyric files for review, correction, and downstream media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio is sent to OpenAI or ElevenLabs for transcription. <br>
Mitigation: Use the skill only with audio that is appropriate to process through the selected third-party API provider. <br>
Risk: API keys are stored locally and may be exposed through shell history or logs if handled carelessly. <br>
Mitigation: Use revocable API keys, avoid displaying raw key values, and rotate any key that may have been logged or pasted into an unsafe location. <br>
Risk: Crafted audio filenames or custom output paths may reach unsafe inline Python execution paths. <br>
Mitigation: Avoid untrusted filenames and custom output paths until path escaping is reviewed and corrected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DumoeDss/acestep-lyrics-transcription) <br>
- [OpenAI API key settings](https://platform.openai.com/api-keys) <br>
- [ElevenLabs API key settings](https://elevenlabs.io/app/settings/api-keys) <br>
- [OpenAI API base URL](https://api.openai.com/v1) <br>
- [ElevenLabs API base URL](https://api.elevenlabs.io/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated transcription files in LRC, SRT, or JSON format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, python3 or python, and a configured OpenAI or ElevenLabs API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
