## Description: <br>
Converts Feishu voice messages, local audio files, and public audio URLs into text using Volcengine BigModel ASR flash and standard recognition modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to transcribe user-provided voice messages, local audio files, or public audio URLs before continuing the conversation or workflow with the recognized text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio may be sent to Volcengine or Feishu-related cloud services for transcription or file retrieval. <br>
Mitigation: Use the skill only when that data flow is acceptable for the audio content and the user's environment. <br>
Risk: The skill can attempt to install ffmpeg and ffprobe through local package managers when they are missing. <br>
Mitigation: Prefer preinstalling ffmpeg and ffprobe through the normal managed software path before enabling the skill. <br>
Risk: API-key management behavior can use ARK_SKILL_API_KEY or ARK_SKILL_API_BASE if MODEL_SPEECH_API_KEY is not set. <br>
Mitigation: Set MODEL_SPEECH_API_KEY explicitly through the normal secret-management path and avoid exposing ARK_SKILL_API_KEY or ARK_SKILL_API_BASE unless intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-voice-to-text) <br>
- [Volcengine BigModel ASR](https://www.volcengine.com/docs/6561/1354870) <br>
- [Volcengine quick start and authentication](https://www.volcengine.com/docs/6561/2119699) <br>
- [Volcengine API key usage](https://www.volcengine.com/docs/6561/1816214) <br>
- [Audio routing and large-file handling strategy](references/routing_strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcriptions, JSON diagnostics, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MODEL_SPEECH_API_KEY and may use ffmpeg or ffprobe for local audio inspection and conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
