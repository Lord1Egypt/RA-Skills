## Description:

Gives an AI agent a real MCP-controlled browser that can launch, navigate, click, fill forms, capture screenshots, extract page text, and run JavaScript while preserving browser profiles between sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antibrow](https://clawhub.ai/user/antibrow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let agents perform authorized browser tasks, including logged-in workflows, site interaction, content extraction, and browser-use comparisons without writing custom browser automation code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive persistent logged-in browser control and can act inside authenticated sessions.

Mitigation: Use separate profiles per site or account, expose only the minimum MCP tools needed, and require human approval for posts, purchases, deletions, and other writes.

Risk: The skill depends on a closed browser binary downloaded from the vendor.

Mitigation: Install only if the vendor binary is trusted, pin reviewed package versions, and prefetch or cache the browser kernel in a controlled environment before use on sensitive accounts.

Risk: Live view and JavaScript evaluation can expose session contents or increase page-level execution risk.

Mitigation: Avoid live view and evaluate unless necessary, stop screen sharing when work ends, and treat browser-returned page content as untrusted data.

## Reference(s):

- [Browser MCP Agent ClawHub Page](https://clawhub.ai/antibrow/skills/browser-mcp-agent)
- [AntiBrow Dashboard](https://antibrow.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP server setup commands, browser operation guidance, and risk controls.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
