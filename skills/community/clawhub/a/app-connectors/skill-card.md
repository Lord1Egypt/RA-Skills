## Description: <br>
Connect your AI agent to 1000+ apps - discover tools, manage OAuth connections, execute actions, and provide a self-service connector dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ts-sz](https://clawhub.ai/user/ts-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to third-party apps through Composio OAuth, discover app tools, manage active connections, and execute app actions after confirming the target account and action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent act across connected third-party accounts. <br>
Mitigation: Use a scoped Composio API key and limit enabled OAuth connections to the apps and accounts required for the deployment. <br>
Risk: The skill can send messages, change records, disconnect apps, or run batches without enough built-in confirmation guidance. <br>
Mitigation: Require explicit confirmation of the target app, account, action, recipient or resource, and exact content before executing mutating or external-facing actions. <br>


## Reference(s): <br>
- [App Connectors release page](https://clawhub.ai/ts-sz/app-connectors) <br>
- [Composio Docs](https://docs.composio.dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scoped COMPOSIO_API_KEY and active OAuth connections for target apps.] <br>

## Skill Version(s): <br>
5.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
