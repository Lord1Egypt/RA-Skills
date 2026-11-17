## Description:

AI-powered daily task management MCP Server — recommend next task, inherit uncompleted todos, detect overdue, generate reviews. Deterministic ops in code (zero tokens), AI only when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asuranale](https://clawhub.ai/user/asuranale)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this MCP server with compatible AI agents to manage daily Markdown task files, choose the next task, carry forward unfinished work, check overdue tasks, and generate end-of-day reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can run code from a mutable remote source and install an unpinned dependency.

Mitigation: Install from a pinned, reviewed commit or packaged artifact, and pin or review the fastmcp dependency before use.

Risk: The --auto setup path can modify MCP configuration files for detected AI editors.

Mitigation: Back up existing editor configuration files and prefer manual MCP configuration unless automatic changes are acceptable.

Risk: The MCP server reads and writes local daily task and review Markdown files in the configured data directory.

Mitigation: Configure a dedicated task-data directory and review generated daily reviews before relying on them for planning or records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asuranale/skills/daily-assistant)
- [Project homepage](https://github.com/AsuraNale/daily-assistant-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Plain text and Markdown task-management responses, with JSON MCP configuration generated during setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English response text through config.json; task data is stored in local Markdown files.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
