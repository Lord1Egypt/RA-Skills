## Description: <br>
Search, register, and manage internet domains for AI agents via DomainForAgents API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[midnight-rgb](https://clawhub.ai/user/midnight-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent search, register, renew, and configure domains through DomainForAgents, including DNS and payment-related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can register or renew domains and use payment-linked credentials. <br>
Mitigation: Use a dedicated low-balance or scoped account when available, and require explicit confirmation before purchases, renewals, payments, or payment-link creation. <br>
Risk: DNS record changes and webhook setup can affect live services. <br>
Mitigation: Review requested DNS and webhook changes before execution, prefer test domains for validation, and require approval before applying changes to production domains. <br>
Risk: The MCP server is installed from an external npm package. <br>
Mitigation: Verify the @domainforagents/mcp package source and version before running it in an agent environment. <br>


## Reference(s): <br>
- [DomainForAgents documentation](https://domainforagents.io/docs) <br>
- [DomainForAgents OpenAPI specification](https://api.domainforagents.io/api/openapi.json) <br>
- [DomainForAgents MCP package](https://www.npmjs.com/package/@domainforagents/mcp) <br>
- [ClawHub skill listing](https://clawhub.ai/midnight-rgb/domainforagents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and curl code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup commands and REST API examples; external API operations can affect billing, domains, and DNS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
