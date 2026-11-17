## Description:

CDP Bridge MCP Browser Control lets an agent operate a real browser through a CDP Bridge extension and MCP service, including tab discovery, page scanning, JavaScript execution, navigation, screenshots, waiting, batch CDP commands, and cookie access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miyan1221](https://clawhub.ai/user/miyan1221)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to inspect and control an installed CDP Bridge-enabled browser session for page reading, navigation, screenshot capture, JavaScript execution, cookie access, and other browser operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent control of a real browser profile can expose logged-in sessions and sensitive page data.

Mitigation: Use a dedicated browser profile without unrelated logged-in accounts and install only when real-browser control is intentional.

Risk: Cookie access and arbitrary JavaScript, click, navigation, or batch CDP actions can expose credentials or change account state.

Mitigation: Avoid cookie access unless strictly necessary and confirm JavaScript, click, navigation, and batch CDP actions before execution.

Risk: Using cdp-bridge@latest can pull unreviewed behavior at runtime.

Mitigation: Prefer a pinned, reviewed cdp-bridge version.

## Reference(s):

- [CDP Bridge MCP API calling guide](references/cdp-bridge-api.md)
- [CDP Bridge operation examples](references/cdp-bridge-examples.md)
- [CDP Bridge tool parameter guide](references/cdp-bridge-tools.md)
- [ClawHub skill page](https://clawhub.ai/miyan1221/skills/cdp-bridge)
- [ClawHub publisher profile](https://clawhub.ai/user/miyan1221)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PowerShell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser operation guidance and MCP call examples; invoked tools can return tab lists, page text, screenshots as base64 PNG, and cookies.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
