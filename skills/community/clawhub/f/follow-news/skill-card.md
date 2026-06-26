## Description: <br>
Generate tech news digests with unified source model, internal ranking, and multi-format output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangwz](https://clawhub.ai/user/tangwz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical teams, and news-monitoring users use this skill to collect technology updates from RSS, Twitter/X, GitHub, Reddit, web search, and podcasts, then produce ranked digests for chat, Discord, email, markdown, or PDF delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can interact with browser sessions, sensitive credentials, and OpenCLI update or cleanup behavior. <br>
Mitigation: Review configuration before installation, use narrowly scoped API tokens, disable OpenCLI auto-update and browser cleanup unless intentionally enabled, and avoid running it against a sensitive live browser profile. <br>
Risk: Scheduled digest delivery could send collected information to the wrong destination if configured incorrectly. <br>
Mitigation: Verify email, Discord, and other delivery destinations before enabling recurring digests. <br>


## Reference(s): <br>
- [ClawHub Follow News Listing](https://clawhub.ai/tangwz/follow-news) <br>
- [Publisher Profile](https://clawhub.ai/user/tangwz) <br>
- [Project Homepage](https://github.com/tangwz/follow-news) <br>
- [README](README.md) <br>
- [Digest Prompt](references/digest-prompt.md) <br>
- [Podcast Summary Prompt](references/summarize-podcast.md) <br>
- [Tweet Summary Prompt](references/summarize-tweets.md) <br>
- [Chat Output Template](references/templates/chat.md) <br>
- [Discord Output Template](references/templates/discord.md) <br>
- [Email Output Template](references/templates/email.md) <br>
- [PDF Output Template](references/templates/pdf.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Markdown digests, JSON source and merge data, optional HTML email and PDF files, plus shell command and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on configured source credentials, optional tools, delivery templates, and archive-based deduplication state.] <br>

## Skill Version(s): <br>
3.18.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
