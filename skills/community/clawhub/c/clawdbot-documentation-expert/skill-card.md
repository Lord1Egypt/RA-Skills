## Description:

Expert guidance on navigating, understanding, configuring, troubleshooting, and automating Clawdbot using official documentation and config snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janhcla](https://clawhub.ai/user/janhcla)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to find relevant Clawdbot documentation, retrieve documentation links, apply common configuration snippets, troubleshoot setup issues, and track documentation changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts contact docs.clawd.bot and store sitemap, documentation, index, and history files under ~/.cache/clawddocs.

Mitigation: Use the skill only where outbound access to docs.clawd.bot and local documentation caching are acceptable; refresh or remove the cache when stale or no longer needed.

Risk: Configuration snippets cover messaging providers and include placeholders for bot tokens, account identifiers, allowed users, and skill API keys.

Mitigation: Review snippets before use and substitute real tokens or account details only after the intended provider access and scope are approved.

## Reference(s):

- [Clawdbot Documentation](https://docs.clawd.bot)
- [Clawdbot Documentation Sitemap](https://docs.clawd.bot/sitemap.xml)
- [Common Clawdbot Configuration Snippets](artifact/snippets/common-configs.md)
- [ClawHub Skill Page](https://clawhub.ai/janhcla/skills/clawdbot-documentation-expert)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown answers with documentation links, shell command suggestions, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference cached or fetched Clawdbot documentation and local snippets; helper scripts use docs.clawd.bot and ~/.cache/clawddocs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
