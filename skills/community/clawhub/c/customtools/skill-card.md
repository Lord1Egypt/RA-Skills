## Description:

Provides OpenClaw utility tools for task management, skill lookup, LSP-style code navigation, configuration helpers, and MCP HTTP client interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[v4leileiv4](https://clawhub.ai/user/v4leileiv4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw use this plugin to manage lightweight tasks, search or load known skills, request code-navigation information, inspect configuration actions, and interact with MCP HTTP servers from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client can contact arbitrary URLs from inside the user's OpenClaw environment.

Mitigation: Use trusted MCP endpoints, avoid internal or sensitive network addresses, and pin the package to the reviewed version before installation.

Risk: Some task, code-navigation, and configuration helpers return local, stub, or advisory output rather than authoritative platform state.

Mitigation: Confirm important task, code, and configuration decisions against the relevant OpenClaw or project source before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/v4leileiv4/skills/customtools)
- [ClawHub publisher profile](https://clawhub.ai/user/v4leileiv4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON snippets, and Markdown-style command examples returned as tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most tools return a single text response; task detail responses may include formatted JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
