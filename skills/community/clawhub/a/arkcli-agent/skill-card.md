## Description:

arkcli agent：管理 ARK Managed Agents，包括 Agent / Skill / Env / Session / File / Memory Store / Vault / MCP OAuth。控制面优先走 ForTop/OpenTOP，Session 运行时和 Files 走数据面直联。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create, configure, query, and troubleshoot ARK Managed Agents and their skills, environments, sessions, files, memory stores, vaults, and MCP connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags guidance to create cloud environments with unrestricted networking; the scan was incomplete.

Mitigation: Consider avoiding installation until the unrestricted-networking guidance is clarified or corrected, as advised by the security evidence.

## Reference(s):

- [ARK CLI Agent release](https://clawhub.ai/jasonstarlight/skills/arkcli-agent)
- [Agent configuration and model selection](references/agent.md)
- [Sessions and files](references/session-files.md)
- [Events and chat](references/events-chat.md)
- [Vaults and MCP OAuth](references/mcp-vault.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-specific identifiers and configuration values supplied or retrieved during the task.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter reports 1.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
