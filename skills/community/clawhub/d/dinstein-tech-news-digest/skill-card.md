## Description: <br>
Generates quality-scored tech news digests from RSS, Twitter/X, GitHub, Reddit, and web search with Discord, email, markdown, and PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to generate scheduled or on-demand technology news digests from configured sources and deliver them through Discord, email, markdown, or PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials and delivery targets can expose data or send digests to unintended destinations if configured too broadly. <br>
Mitigation: Use dedicated least-privilege API keys, avoid broad personal GitHub tokens, and verify channel IDs and email recipients before enabling scheduled delivery. <br>
Risk: Optional enrichment and source collection make outbound requests to configured feeds and APIs. <br>
Mitigation: Enable only the sources and backends needed for the deployment, and disable enrichment in restricted environments. <br>
Risk: Scheduled archive cleanup can remove files from the configured digest archive path. <br>
Mitigation: Set WORKSPACE to a skill-specific archive directory before enabling scheduled cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asterisk622/dinstein-tech-news-digest) <br>
- [Publisher profile](https://clawhub.ai/user/asterisk622) <br>
- [Digest prompt template](references/digest-prompt.md) <br>
- [Discord output template](references/templates/discord.md) <br>
- [Email output template](references/templates/email.md) <br>
- [PDF output template](references/templates/pdf.md) <br>
- [Configuration schema](config/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest content with optional JSON intermediates, HTML email, and PDF output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quality scoring, deduplication, source health checks, configurable sources and topics, and optional delivery to Discord or email.] <br>

## Skill Version(s): <br>
3.15.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
