## Description:

Top-level macOS computer-use skill with a bundled standalone runtime that bootstraps itself without any local Claude installation, private native modules, or extracted app assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an agent controlled macOS desktop-use capabilities through a bundled standalone MCP runtime for screenshots, mouse and keyboard input, app launch, window/display inspection, and clipboard access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime needs macOS Accessibility and Screen Recording permissions, which can expose desktop contents and allow broad local app control.

Mitigation: Run it only in a trusted, controlled macOS account or environment, grant permissions deliberately, and revoke them when the skill is no longer needed.

Risk: Clipboard read/write and system-key access may expose sensitive content or disrupt active applications.

Mitigation: Avoid using the runtime around sensitive apps or data, monitor sessions, and require explicit approval before actions that touch the clipboard or system keys.

Risk: The current runtime reports screenshotFiltering: none, so screenshots are not compositor-filtered.

Mitigation: Rely on MCP-layer allowlists and action gates, and avoid use on screens containing information the agent should not see.

Risk: Security evidence says the runtime does not yet provide explicit user approval prompts or a strict allowlist.

Mitigation: Treat the host as trusted-local only and keep human review in the loop until approval prompts or a strict allowlist are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wimi321/skills/computer-use-macos)
- [wimi321 publisher profile](https://clawhub.ai/user/wimi321)
- [Project README](artifact/project/README.md)
- [Example MCP configuration](artifact/project/examples/mcp-config.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; the bundled runtime can execute local desktop-control actions when launched.]

## Skill Version(s):

0.2.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
