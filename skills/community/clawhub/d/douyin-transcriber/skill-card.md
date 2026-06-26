## Description: <br>
Transcribe speech from audio or video files by extracting media audio and converting it to text with Docker Whisper ASR for Douyin/TikTok workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[don068589](https://clawhub.ai/user/don068589) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-processing agents use this skill to turn Douyin/TikTok audio or video files into transcribed text using a local Docker Whisper ASR service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media submitted for transcription can contain private or sensitive speech. <br>
Mitigation: Only submit files intentionally selected for transcription, keep the ASR service bound to localhost, and stop or remove the container when finished. <br>
Risk: The transcription workflow depends on a Docker Whisper ASR image that must be trusted before use. <br>
Mitigation: Confirm the image source before installing and consider pinning a specific version or digest instead of using a floating tag. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/don068589/douyin-transcriber) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local transcription workflows; ASR responses may include transcript text, timed segments, and detected language.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
