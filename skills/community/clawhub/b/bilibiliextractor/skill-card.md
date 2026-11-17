## Description:

Extracts subtitles from Bilibili videos and summarizes the core points, main topics, and key conclusions, with full transcript output when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongym1234](https://clawhub.ai/user/kongym1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a Bilibili video URL or BV identifier into a readable transcript summary. When the user explicitly asks for raw subtitles, the skill outputs the extracted transcript instead of a summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send Bilibili video requests to Bilibili and may upload audio to SiliconFlow for transcription when subtitles are unavailable.

Mitigation: Use it only with videos the user is comfortable processing through those services, and obtain clear user consent before ASR fallback.

Risk: The skill instructions source a broad local .env file to load secrets.

Mitigation: Provide only SILICONFLOW_API_KEY through a trusted secret mechanism instead of sourcing unrelated local environment variables.

Risk: The artifact includes overbroad temporary-file cleanup guidance and runtime dependency installation guidance.

Mitigation: Avoid wildcard cleanup commands during agent execution and prefer preinstalled or pinned dependencies over runtime installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongym1234/skills/bilibiliextractor)
- [Publisher profile](https://clawhub.ai/user/kongym1234)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary or plain transcript text with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to a structured summary; full transcript output is used only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
