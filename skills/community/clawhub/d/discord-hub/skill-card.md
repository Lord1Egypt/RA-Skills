## Description: <br>
OpenClaw skill for Discord Bot API workflows, covering interactions, commands, messages, and operations using direct HTTPS requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design Discord bot workflows with slash commands, interactions, REST message operations, token handling, and operational checklists for safe deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bot tokens or interaction secrets could be exposed through logs or shared outputs. <br>
Mitigation: Use a dedicated Discord bot token with minimal permissions, avoid sharing or logging secrets, separate development and production applications, and rotate compromised tokens immediately. <br>
Risk: Generated workflows may post, edit, delete, or moderate Discord content. <br>
Mitigation: Test workflows in a development server first and require clear user confirmation before live message or moderation operations. <br>
Risk: Incorrect interaction handling or rate-limit assumptions can cause failed or unreliable bot behavior. <br>
Mitigation: Validate incoming interaction signatures, respond or defer quickly, read rate-limit headers, and back off on 429 responses. <br>


## Reference(s): <br>
- [Discord API Overview](references/discord-api-overview.md) <br>
- [Application Commands](references/discord-app-commands.md) <br>
- [Auth and Tokens](references/discord-auth-and-tokens.md) <br>
- [Discord Bot Feature Map](references/discord-feature-map.md) <br>
- [Gateway vs Webhooks](references/discord-gateway-webhooks.md) <br>
- [Interactions](references/discord-interactions.md) <br>
- [Messages and Components](references/discord-messages-components.md) <br>
- [Rate Limits and Reliability](references/discord-rate-limits.md) <br>
- [HTTP Request Templates](references/discord-request-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with HTTP request and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational checklists, command designs, token-handling guidance, and REST API request templates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
