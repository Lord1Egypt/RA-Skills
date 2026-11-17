## Description:

Extracts Douyin video information and download links, then uses SiliconFlow or Alibaba Cloud DashScope speech recognition to produce video transcripts through CLI and MCP Server workflows.

This skill is for research and development only.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and developers use this skill to parse Douyin share links, retrieve video metadata or download links, and generate text transcripts for content review, notes, research, or MCP-enabled workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download and run FFmpeg binaries from external sources.

Mitigation: Prefer installing FFmpeg manually from a trusted package manager or a vetted source, and avoid automatic binary installation in managed environments.

Risk: Transcription uploads extracted audio or video-derived media to external speech services.

Mitigation: Do not process private or sensitive videos unless the selected provider's data handling, retention, and access controls have been reviewed.

Risk: The release has a suspicious security verdict and includes referral-based onboarding content.

Mitigation: Review the security guidance, referral behavior, URL handling, and privacy disclosures before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/douyin-text-extractor)
- [SiliconFlow API documentation](https://docs.siliconflow.cn/)
- [SiliconFlow speech service](https://cloud.siliconflow.cn/)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, JSON strings, Markdown transcript files, and CLI or MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription requires a user-provided API key; video download and transcript workflows may create local media and Markdown files.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact skill.json, README, and package.json contain different version values)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
