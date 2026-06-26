## Description: <br>
Provides persistent, versioned memory and engagement analysis for AI agents supporting creators and influencers across social media platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WillNigri](https://clawhub.ai/user/WillNigri) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers working with creator or influencer workflows use CrowTerminal to store creator memory, query engagement history, inspect schema metadata, and retrieve performance insights across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creator or client analytics sent to CrowTerminal may include sensitive third-party data and are stored by an external service. <br>
Mitigation: Use a dedicated API key stored as a secret, minimize or redact sensitive data before upload, and review CrowTerminal privacy, retention, deletion, and webhook-security practices before production use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/WillNigri/crowterminal) <br>
- [CrowTerminal homepage](https://crowterminal.com) <br>
- [CrowTerminal LLM docs](https://crowterminal.com/llms.txt) <br>
- [CrowTerminal MCP manifest](https://crowterminal.com/.well-known/mcp.json) <br>
- [CrowTerminal OpenAPI specification](https://api.crowterminal.com/api/docs.json) <br>
- [API key registration endpoint](https://api.crowterminal.com/api/agent/register) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CROWTERMINAL_API_KEY for authenticated endpoints; sandbox endpoints are documented for unauthenticated testing.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
