## Description:

Automatically extracts Douyin video links from shared text, downloads the video, transcribes its audio with SiliconFlow, and summarizes the core content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongym1234](https://clawhub.ai/user/kongym1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn messy Douyin share text into a clean video transcript and a concise structured summary. It is useful when a user wants the key points, highlights, or full transcript of a Douyin video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Douyin share text may be passed through shell execution paths if it is not handled carefully.

Mitigation: Review command construction before installation and pass user text as data, not executable shell syntax.

Risk: The skill downloads media and sends it to SiliconFlow for transcription, which may transfer user-provided or third-party video content to an external service.

Mitigation: Disclose the external transcription provider and obtain appropriate user consent before processing sensitive media.

Risk: The current release accepts a broader URL scope than the stated Douyin use case.

Mitigation: Restrict accepted URLs to expected Douyin hosts before deployment.

Risk: Sourcing a local .env file as executable shell code can run unintended commands if that file is modified.

Mitigation: Load required environment variables with a non-executing parser or otherwise ensure the environment file is trusted and controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongym1234/skills/douyin2text)
- [Publisher profile](https://clawhub.ai/user/kongym1234)
- [SiliconFlow audio transcription endpoint](https://api.siliconflow.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary or plain transcript text with command-line execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a video title, raw transcript, key points, highlights, and the extracted source URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
