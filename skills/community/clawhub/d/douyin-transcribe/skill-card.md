## Description: <br>
Transcribes Douyin links or uploaded video files into punctuated Chinese text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junweiren98-rgb](https://clawhub.ai/user/junweiren98-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to turn Douyin video links or local video files into readable Chinese transcripts for review, reuse, or knowledge-base capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, audio, and transcript text may be exposed because the skill asks for API keys in chat, persists them locally, and sends media content to Groq or OpenAI. <br>
Mitigation: Review before installing, use only non-sensitive videos, avoid pasting API keys into chat, and prefer a version that stores secrets in a secure secret store. <br>
Risk: Shell commands built from user-controlled input may execute unsafely. <br>
Mitigation: Prefer a fixed version that uses argument-array process execution instead of shell strings, and review command behavior before deployment. <br>
Risk: Transcript files are saved locally and may retain sensitive video content after the task finishes. <br>
Mitigation: Limit use to non-sensitive media and clean local transcript and temporary output directories according to the deployment's retention policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/junweiren98-rgb/douyin-transcribe) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Groq](https://groq.com) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown transcript text with setup and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local Markdown transcript files under douyin-transcripts when run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
