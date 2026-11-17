## Description:

AgentRecall provides persistent, local memory for AI agents through MCP tools for session context, recall, saving, checks, and digest workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldentrii](https://clawhub.ai/user/goldentrii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using MCP-compatible coding agents use AgentRecall to preserve session context, decisions, corrections, and cross-project lessons across local projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can store prompts, corrections, project summaries, and cross-project insights.

Mitigation: Review stored files under ~/.agent-recall and avoid saving sensitive content unless the user has approved that storage.

Risk: Automatic hooks and /arsaveall may read broader agent transcript or configuration files than basic MCP usage.

Mitigation: Start with basic MCP mode and review the exact files read before enabling hooks or /arsaveall.

Risk: Installing command files from a mutable branch can change behavior after review.

Mitigation: Pin or verify downloaded command files before installing them.

Risk: Deletion or cleanup flows can remove local memory.

Mitigation: Back up ~/.agent-recall before using deletion or cleanup commands.

## Reference(s):

- [AgentRecall ClawHub listing](https://clawhub.ai/goldentrii/skills/agent-recall)
- [agent-recall-mcp npm package](https://www.npmjs.com/package/agent-recall-mcp)
- [agent-recall-sdk npm package](https://www.npmjs.com/package/agent-recall-sdk)
- [agent-recall-cli npm package](https://www.npmjs.com/package/agent-recall-cli)
- [MCP adapter specification](docs/mcp-adapter-spec.md)
- [Command reference](docs/commands.md)
- [Recall scoring design rationale](docs/SCORING.md)
- [Intelligent Distance Protocol](docs/intelligent-distance-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON tool responses with shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist local markdown and JSON memory under ~/.agent-recall when configured.]

## Skill Version(s):

3.3.27 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
