## Description: <br>
Automates Douyin account video collection, transcript extraction, transcript cleanup, and cross-video content summarization using browser access and douyin-mcp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fishisnow](https://clawhub.ai/user/fishisnow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, creators, and agent users use this skill to collect recent video links from a Douyin account, extract speech transcripts, remove conversational filler while preserving substantive points, and summarize themes across videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands that inspect MCP configuration can expose API keys or local configuration details in logs. <br>
Mitigation: Redact secrets before sharing output, avoid printing full configuration unless necessary, and keep API keys in managed environment configuration. <br>
Risk: Douyin URLs and extracted transcripts may be sent to mcporter, douyin-mcp, and configured API providers. <br>
Mitigation: Use the skill only when those tools and providers are trusted for the content being processed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fishisnow/douyin-video-analyst) <br>
- [Setup Guide](references/setup.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured transcript sections, command examples, and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes multiple Douyin video links in source order and recommends concurrent transcript extraction when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
