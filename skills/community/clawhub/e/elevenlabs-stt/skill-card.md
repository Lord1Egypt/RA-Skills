## Description: <br>
Transcribe audio files using ElevenLabs Speech-to-Text (Scribe v2). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbotborges](https://clawhub.ai/user/clawdbotborges) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe selected audio or video files into text or JSON output with optional diarization, language hints, word timestamps, and audio event tagging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio or video files are sent to ElevenLabs for transcription. <br>
Mitigation: Use the skill only with recordings approved for ElevenLabs processing, and avoid confidential, regulated, or consent-sensitive content unless approved. <br>
Risk: The transcription script depends on jq for JSON parsing and error handling. <br>
Mitigation: Install jq before use and verify that curl, jq, and ELEVENLABS_API_KEY are available in the execution environment. <br>


## Reference(s): <br>
- [ElevenLabs Speech-to-Text](https://elevenlabs.io/speech-to-text) <br>
- [ElevenLabs Speech-to-Text API Documentation](https://elevenlabs.io/docs/api-reference/speech-to-text) <br>
- [ClawHub Skill Page](https://clawhub.ai/clawdbotborges/elevenlabs-stt) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text transcript or JSON response from the transcription API; documentation includes Markdown with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, ELEVENLABS_API_KEY, and a local audio or video file selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
