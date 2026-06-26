## Description: <br>
Persistent memory enhancement for AI agents that stores conversations, searches memories with semantic retrieval, and recalls context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure and operate a Cortex memory MCP server so an agent can persist user preferences, conversation context, and project knowledge across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can store sensitive, regulated, or unnecessary conversation data. <br>
Mitigation: Avoid storing secrets or regulated data, review what is committed to memory, and delete memory entries that should not persist. <br>
Risk: Configured LLM and embedding providers may receive memory content during extraction, embedding, or retrieval workflows. <br>
Mitigation: Use scoped provider API keys, keep configuration files out of repositories, restrict configuration file permissions, and verify provider handling requirements before use. <br>
Risk: Auto-triggered memory processing may save content without an explicit user action. <br>
Mitigation: Disable auto-triggering with the documented flag when explicit control over saved content is required. <br>
Risk: The skill depends on an external MCP package and local services that must be installed and trusted. <br>
Mitigation: Verify the upstream cortex-mem-mcp package or release before installing and confirm Qdrant and MCP client configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sopaco/cortex-mem-mcp) <br>
- [Project homepage](https://github.com/sopaco/cortex-mem) <br>
- [Project releases](https://github.com/sopaco/cortex-mem/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, TOML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured cortex-mem-mcp MCP server, LLM provider, embedding provider, and Qdrant vector database.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
