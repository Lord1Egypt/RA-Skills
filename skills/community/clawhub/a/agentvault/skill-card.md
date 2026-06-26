## Description: <br>
Encrypted credential vault and persistent memory for AI agents that helps install and manage AgentVault, sandbox agent access to secrets, store and query encrypted memory, run an MCP server, and audit credential access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maheen-sajjad](https://clawhub.ai/user/maheen-sajjad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up and operate a local encrypted credential and memory vault for agents, including read-only inspection, profile previews, secret and memory workflows, MCP configuration, and audit review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret retrieval, vault export, plaintext export, signing, and wallet or private-key commands can expose sensitive material if run without clear user intent. <br>
Mitigation: Require explicit user approval before retrieving secret values, exporting vault data, using plaintext export, signing, or touching wallet/private-key commands. <br>
Risk: Starting MCP broadens agent access to vault tools and may expose sensitive operations to connected clients. <br>
Mitigation: Connect MCP only to trusted local clients and ask before starting the server. <br>
Risk: The workflow depends on an external npm package for the actual vault implementation. <br>
Mitigation: Install only when the user trusts the package and has a concrete need for an agent-facing credential vault. <br>


## Reference(s): <br>
- [AgentVault documentation](https://agentvault.inflectiv.ai/documentation) <br>
- [AgentVault website](https://agentvault.inflectiv.ai) <br>
- [npm package](https://www.npmjs.com/package/@inflectiv-ai/agentvault) <br>
- [Agent Vault Protocol specification](https://agentvaultprotocol.org/) <br>
- [Command reference](references/commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/maheen-sajjad/agentvault) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for user approval before write, install, export, server-start, secret retrieval, signing, wallet, or destructive operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
