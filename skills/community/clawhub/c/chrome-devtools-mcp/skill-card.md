## Description:

Use Chrome DevTools MCP for safe, configurable browser automation, page inspection, debugging, screenshots, network inspection, and performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aihlp](https://clawhub.ai/user/aihlp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and operate Chrome DevTools MCP for authorized browser automation, page inspection, debugging, screenshots, network inspection, and performance analysis in OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures Chrome DevTools MCP through an unpinned npm package that can change at runtime.

Mitigation: Pin chrome-devtools-mcp to a reviewed exact version or use a preinstalled, locked package source before production use.

Risk: Browser automation can expose cookies, storage, authenticated pages, or normal browser profile state.

Mitigation: Keep isolated browser mode as the default, redact sensitive values in summaries, and use existing-session or real profiles only after an explicit user choice.

Risk: Remote debugging endpoints can expose browser control if bound beyond localhost.

Mitigation: Require existing-session browser URLs to use localhost-only hosts such as 127.0.0.1, localhost, or [::1].

Risk: Browser actions may create external effects such as submissions, payments, account changes, publishing, or deletions.

Mitigation: Require explicit user confirmation before externally visible, destructive, account-changing, payment, or production-affecting actions.

## Reference(s):

- [Chrome DevTools MCP Skill Page](https://clawhub.ai/aihlp/skills/chrome-devtools-mcp)
- [Browser Modes](references/browser-modes.md)
- [Configuration](references/configuration.md)
- [OpenClaw MCP Installation](references/openclaw-mcp-install.md)
- [Security Policy](references/security-policy.md)
- [SkillSpector](references/skillspector.md)
- [User Settings](references/user-settings.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON or JSON5 configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, and an enabled OpenClaw MCP server definition for chrome-devtools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
