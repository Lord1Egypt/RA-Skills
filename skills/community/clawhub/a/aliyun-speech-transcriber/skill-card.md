## Description:

Transcribe publicly accessible audio or video URLs with Aliyun speech services. Use when the user wants speech-to-text via Aliyun DashScope, needs transcript JSON or extracted plain text, or wants to process a cloud-accessible media URL into transcription results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenggongdu](https://clawhub.ai/user/chenggongdu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to transcribe one or more publicly accessible audio or video URLs with Aliyun DashScope and return both structured JSON and extracted plain text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media URLs and their audio or video contents are sent to Aliyun DashScope for processing.

Mitigation: Use only media URLs whose contents may be disclosed to Aliyun for transcription, and avoid sensitive internal-only media unless that disclosure is approved.

Risk: Aliyun API credentials could be exposed if copied into commands, source files, or shared logs.

Mitigation: Provide credentials through ASR_DASHSCOPE_API_KEY or DASHSCOPE_API_KEY environment variables and do not hardcode or print them.

Risk: Public or signed media URLs may remain accessible beyond the intended transcription workflow.

Mitigation: Prefer scoped signed URLs for private media, limit their lifetime where possible, and share only URLs intended for transcription.

## Reference(s):

- [Aliyun DashScope](https://dashscope.aliyun.com/)
- [Aliyun speech environment variables](references/env-example.md)
- [ClawHub skill page](https://clawhub.ai/chenggongdu/skills/aliyun-speech-transcriber)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [JSON response with transcript text and transcription metadata; agent guidance may include Markdown and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ASR_DASHSCOPE_API_KEY or DASHSCOPE_API_KEY and publicly accessible media URLs; model, language hints, polling interval, and timeout are configurable through environment variables.]

## Skill Version(s):

0.1.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
