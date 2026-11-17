## Description:

Use Chrome DevTools MCP through UXC over local stdio for page navigation, DOM/a11y snapshots, network inspection, console inspection, and performance tooling, with a live-browser autoConnect default and optional browserUrl or isolated fallback modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an agent to Chrome DevTools MCP through UXC for browser inspection, debugging, network analysis, console review, accessibility snapshots, and performance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the current npm-published `chrome-devtools-mcp` package at use time.

Mitigation: Pin or vet the package version before creating persistent UXC links.

Risk: The skill can attach to a live debuggable Chrome session and inspect browser state.

Mitigation: Use an isolated browser profile, avoid sensitive tabs, and prefer the isolated headless fallback when live browser state is not needed.

Risk: Page-mutating operations such as click, fill, upload, dialog handling, or script evaluation can alter browser state.

Mitigation: Start with read-only inspection tools and require explicit confirmation before mutating page state.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Chrome DevTools MCP Repository](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/chrome-devtools-mcp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes JSON-envelope parsing, help-first discovery, read-first inspection, and confirmation before page-mutating actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
