## Description:

AugmentiQ is a memory system that lets agents recall, reason, record, and consolidate persistent, evolving memory through the AugmentiQ MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upsurge911-lgtm](https://clawhub.ai/user/upsurge911-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to connect an AI agent to a local AugmentiQ MCP server for persistent Obsidian-vault memory. It guides agents through recalling context, reasoning over it, recording selected memories, and periodically consolidating stored context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify an Obsidian vault through local MCP tools.

Mitigation: Start with read-only mode or a dedicated test vault until the access pattern is acceptable.

Risk: The skill is designed to keep long-term local memories about preferences, projects, decisions, and inferred context.

Mitigation: Avoid storing secrets or sensitive personal information, and review or clear memory and profile files regularly.

Risk: Bearer-token access protects the local MCP server, but exposed tokens could permit unintended local access.

Mitigation: Keep the token out of shared logs and files, rotate it if exposed, and keep the service bound to loopback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upsurge911-lgtm/skills/augmentiq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers local MCP actions for memory, vault, edit, graph, and system diagnostics.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
