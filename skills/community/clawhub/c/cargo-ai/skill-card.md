## Description: <br>
Create and configure AI agents, attach knowledge for RAG, manage MCP servers, and handle agent memories using the Cargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Cargo AI agent resources, configure and deploy agent releases, connect MCP servers, and maintain agent-scoped memories from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that change, deploy, or delete live Cargo workspace resources. <br>
Mitigation: Verify target UUIDs before remove or deploy commands and review draft release contents before making them live. <br>
Risk: The skill requires Cargo authentication through browser sign-in or an API token. <br>
Mitigation: Keep Cargo tokens out of shared logs and chats and use only the credentials intended for the target workspace. <br>
Risk: Agent templates and workflows may support lead research or email-drafting use cases with privacy and anti-spam implications. <br>
Mitigation: Apply privacy, consent, and anti-spam rules before using generated lead research or email-drafting configurations. <br>


## Reference(s): <br>
- [Cargo skills homepage](https://github.com/getcargohq/cargo-skills) <br>
- [Cargo Ai on ClawHub](https://clawhub.ai/cargo-ai/cargo-ai) <br>
- [Response Shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Agent Examples](references/examples/agents.md) <br>
- [MCP Server Examples](references/examples/mcp-servers.md) <br>
- [AI Template Examples](references/examples/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Cargo CLI commands, direct API curl examples, and JSON configuration snippets.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
