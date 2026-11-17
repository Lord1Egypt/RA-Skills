## Description:

抖音视频转文字。用户发抖音链接或视频文件，自动转录为带标点的中文文本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junweiren98-rgb](https://clawhub.ai/user/junweiren98-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Douyin links or local video files into punctuated, segmented Chinese transcripts. It can return the transcription to the user and save a Markdown transcript for later use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports material risk from command execution and API-key handling.

Mitigation: Review before installing, run only in a sandboxed environment, and patch command execution to use argument arrays with strict URL and file-path validation before processing untrusted inputs.

Risk: The skill requires Groq or OpenAI API credentials and may process private videos or account sessions.

Mitigation: Configure secrets through a safer local or platform secret mechanism, avoid sensitive videos and private logged-in sessions, and do not paste API keys into normal chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junweiren98-rgb/skills/douyin-transcribe)
- [OpenClaw](https://openclaw.ai)
- [Groq](https://groq.com)
- [FFmpeg](https://ffmpeg.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown transcript files under douyin-transcripts/ and temporary media files under temp/.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
