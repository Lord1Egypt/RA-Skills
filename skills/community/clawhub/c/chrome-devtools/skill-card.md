## Description:

Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[podcasting101](https://clawhub.ai/user/podcasting101)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect web pages, automate browser interactions, analyze performance, and troubleshoot network behavior through Chrome DevTools MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable third-party npm package at runtime.

Mitigation: Prefer a pinned and reviewed chrome-devtools-mcp version before use.

Risk: The configured Chrome launch arguments disable sandbox protections.

Mitigation: Avoid sensitive browser profiles and run Chrome or the MCP server in a restricted account or container, especially on untrusted sites.

## Reference(s):

- [Chrome DevTools documentation](https://developer.chrome.com/docs/devtools)
- [Chrome DevTools AI assistance documentation](https://developer.chrome.com/docs/devtools/ai-assistance)
- [chrome-devtools-mcp troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/podcasting101/skills/chrome-devtools)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline tool names, commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct browser inspection, screenshots, snapshots, traces, and MCP tool calls.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
