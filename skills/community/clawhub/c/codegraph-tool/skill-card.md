## Description:

CodeGraph is a pre-indexed code knowledge graph tool that provides semantic code intelligence for Claude Code, Cursor, Codex, Gemini, OpenCode, Hermes, Antigravity, Kiro, and other AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate CodeGraph, initialize project indexes, explore code structure, trace call chains, and evaluate change impact through MCP and CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance includes mutable remote or unpinned package code.

Mitigation: Review the CodeGraph package and installer before use, and prefer a pinned version or verified release artifact.

Risk: Optional MCP auto-allow permissions can let the server read indexed project code without per-call approval.

Mitigation: Avoid enabling auto-allow permissions unless the MCP server is trusted and the user accepts project-code access.

Risk: The skill includes curl-to-shell installation guidance.

Mitigation: Use package-manager installation or inspect the script before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/codegraph-tool)
- [CodeGraph Configuration & Reference](references/configuration.md)
- [CodeGraph Architecture](references/architecture.md)
- [Remote install script referenced by the skill](https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, MCP tool names, configuration snippets, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to use local CodeGraph MCP tools that read indexed project code and return symbol, file, caller, callee, and impact information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
