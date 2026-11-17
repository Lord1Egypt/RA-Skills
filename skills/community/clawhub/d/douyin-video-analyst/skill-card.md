## Description:

Collects recent Douyin videos from an account page, extracts spoken video transcripts through douyin-mcp, cleans filler language, and summarizes themes across the videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fishisnow](https://clawhub.ai/user/fishisnow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social media teams use this skill to gather recent Douyin videos from an account, extract speech-to-text content, clean the transcripts, and produce a concise cross-video summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and troubleshooting steps may expose API keys or local MCP configuration.

Mitigation: Redact credentials before sharing logs or config output, avoid pasting API keys into shell commands or support chats, and do not run config-dump commands with real credentials unless they are redacted first.

Risk: The workflow uses a browser profile and local MCP configuration.

Mitigation: Use a dedicated browser profile when possible and review the local MCP configuration before enabling the skill.

Risk: Transcript extraction depends on API-backed services and external Douyin video access.

Mitigation: Use pinned, reviewed versions of mcporter and douyin-mcp-server and confirm that the content may be processed by the configured transcription provider.

## Reference(s):

- [Setup configuration guide](references/setup.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [SiliconFlow API key console](https://cloud.siliconflow.cn/)
- [Alibaba Cloud Bailian API key console](https://bailian.console.aliyun.com/)
- [ClawHub skill listing](https://clawhub.ai/fishisnow/skills/douyin-video-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with video links, cleaned transcripts, and a summary table; setup and troubleshooting guidance may include shell commands and JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Orders videos from newest to oldest and preserves core points while removing spoken filler.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
