## Description:

Connect to the native board demo through local-mcp and one fixed UXC link. Use when the user wants to inspect or edit the shared board at board.holon.run or a local board instance through browser WebMCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and update a shared or local board through browser WebMCP, including reading board state, upserting nodes and edges, applying layouts, and exporting diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update a shared board through browser automation, so unintended writes may be visible to other users or persist in the board profile.

Mitigation: Use a local or sandbox board when possible, review current board state before writing, and keep the board profile isolated from other sites.

Risk: The launcher can run unpinned external npm tooling through npx.

Mitigation: Pin or preinstall the required npm tooling in a controlled environment before enabling the skill.

Risk: Custom WEBMCP_LOCAL_MCP_COMMAND values can change what command the persistent launcher runs.

Mitigation: Avoid custom launcher commands unless the command is fully trusted and reviewed.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Link Creation Helper](scripts/ensure-links.sh)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/board-webmcp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide browser WebMCP board reads and writes through a fixed board-webmcp-cli link.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
