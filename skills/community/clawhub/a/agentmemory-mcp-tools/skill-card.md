## Description:

Map of every agentmemory MCP tool, what each does, and its parameters. Use when choosing which memory tool to call, when a tool name or argument is unclear, or when answering what agentmemory can do via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose the appropriate agentmemory MCP tool and understand the documented parameters before calling memory, retrieval, session, graph, slot, governance, or health tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced agentmemory tools can save and retrieve persistent memory, which may retain secrets or sensitive private content if used carelessly.

Mitigation: Avoid storing secrets or sensitive private content unless the memory backend, access controls, and retention policy are trusted.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/rohitg00/agentmemory/tree/main/plugin/skills/agentmemory-mcp-tools)
- [ClawHub skill page](https://clawhub.ai/rohitg00/skills/agentmemory-mcp-tools)
- [Publisher profile](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with inline MCP tool names and parameter notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable reference guidance; no files, shell commands, or configuration are produced directly.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
