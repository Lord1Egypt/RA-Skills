## Description:

Audio Meeting Minutes transcribes meeting recordings with Alibaba Cloud NLS, helps an agent summarize conclusions and action items, and renders an HTML meeting-minutes document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[namedsir](https://clawhub.ai/user/namedsir)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business teams use this skill to convert permitted meeting recordings into transcripts, AI-drafted summaries, decisions, action items, and shareable HTML minutes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting recordings and transcripts may contain sensitive, confidential, personal, or regulated information and are sent to Alibaba Cloud NLS for speech recognition.

Mitigation: Use only recordings your organization permits sending to Alibaba Cloud NLS, and confirm the data flow is acceptable before processing.

Risk: The skill asks users for Alibaba Cloud NLS credentials through conversation.

Mitigation: Use short-lived tokens where possible, provide credentials through environment variables or a secret manager, and avoid sharing long-lived AccessKey secrets in chat.

Risk: Generated HTML from untrusted recordings or transcripts may be unsafe if transcript and summary fields are not escaped.

Mitigation: Sanitize or escape transcript and summary content before sharing output, and avoid opening generated HTML from untrusted recordings until the renderer is reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/namedsir/skills/audio-meeting-minutes)
- [README](README.md)
- [Alibaba Cloud NLS console](https://nls-portal.console.aliyun.com/applist)
- [Alibaba Cloud NLS ASR endpoint](https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands, a structured summary object, transcript text, and generated HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a recording folder and Alibaba Cloud NLS AppKey and AccessToken; generated HTML is written to the meeting-minutes output folder.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
