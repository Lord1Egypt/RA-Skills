## Description:

Provides AI agents with internet access across major web, social, video, and forum platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to search and retrieve public web, social, video, and forum content for news discovery, content aggregation, transcript retrieval, and discussion lookup. Some platform access depends on user-provided cookies, proxy settings, or optional service credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad installer and credential-handling behavior as suspicious for normal installation.

Mitigation: Review before installing, run in a virtual environment or sandbox, and prefer manually pinned dependencies from trusted sources.

Risk: Some platform features rely on browser cookies or social-session credentials.

Mitigation: Use dedicated low-risk accounts, provide only the cookies required for the task, encrypt stored cookies, and rotate or revoke them regularly.

Risk: The installer and setup guides may configure external tools, global packages, proxies, or containers.

Mitigation: Avoid automatic global installs where possible, verify each external tool and endpoint, and disable unused platform integrations.

Risk: Retrieved content may be subject to platform rate limits, access restrictions, or terms of use.

Mitigation: Use conservative request rates, respect platform terms, and confirm downstream use rights before storing or redistributing collected data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/07)
- [Agent Reach repository](https://github.com/Panniantong/agent-reach)
- [Xiaohongshu MCP repository](https://github.com/xpzouying/xiaohongshu-mcp)
- [Exa MCP endpoint](https://mcp.exa.ai/mcp)
- [Groq console](https://console.groq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and retrieved platform content as text or structured records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include search results, post metadata, comments, subtitles, web summaries, and setup guidance for platform-specific access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
