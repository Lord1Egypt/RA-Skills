## Description:

Persistent memory enhancement for AI agents that stores conversations, searches memories with semantic retrieval, and recalls context across sessions using tiered abstract, overview, and content access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to add persistent, searchable memory to an AI agent across sessions, including user preferences, project context, conversation history, and semantically retrieved memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores conversation-derived memories locally and may send memory-related text to configured LLM and embedding providers.

Mitigation: Avoid storing secrets or regulated personal data, review what is committed to memory, and use provider configurations that meet the deployment's privacy requirements.

Risk: Configuration files may contain API keys for LLM and embedding services.

Mitigation: Keep API keys out of repositories, restrict configuration-file permissions, and rotate credentials if exposure is suspected.

Risk: Automatic memory triggering can create memories without an explicit user request.

Mitigation: Disable auto-triggering when memories should only be created after deliberate review or explicit user approval.

## Reference(s):

- [Cortex Mem GitHub Repository](https://github.com/sopaco/cortex-mem)
- [Cortex Mem GitHub Releases](https://github.com/sopaco/cortex-mem/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with bash, TOML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running cortex-mem-mcp MCP server, configured LLM and embedding providers, and Qdrant for vector storage.]

## Skill Version(s):

2.7.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
