## Description: <br>
Deploy serverless backends for REST APIs, webhooks, data storage, scheduled jobs, queue workers, and autonomous workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canuto](https://clawhub.ai/user/canuto) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to give an OpenClaw agent a Codehooks backend for REST APIs, webhooks, persistent storage, scheduled jobs, queues, and autonomous workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad non-interactive control over a live Codehooks backend. <br>
Mitigation: Use a dedicated non-production project where possible, use the narrowest or shortest-lived admin token available, and require manual review before deployments or data import/export. <br>
Risk: Webhook and callback endpoints can receive or send sensitive integration data. <br>
Mitigation: Validate callback destinations, verify webhook signatures with raw request bodies, and keep API keys and secrets in environment variables. <br>
Risk: Deployed code, scheduled jobs, and queues may continue running after the agent finishes a task. <br>
Mitigation: Monitor logs, scheduled jobs, queue workers, and workflow status, and rotate the admin token if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/canuto/codehooks-backend) <br>
- [Codehooks Documentation](https://codehooks.io/docs) <br>
- [Codehooks CLI Reference](https://codehooks.io/docs/cli) <br>
- [Codehooks AI Prompt](https://codehooks.io/llms.txt) <br>
- [OpenAPI/Swagger Docs](https://codehooks.io/docs/openapi-swagger-docs) <br>
- [Codehooks Templates](https://github.com/RestDB/codehooks-io-templates) <br>
- [Codehooks MCP Server](https://github.com/RestDB/codehooks-mcp-server) <br>
- [webhook-verify](https://www.npmjs.com/package/webhook-verify) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the coho CLI and CODEHOOKS_ADMIN_TOKEN for non-interactive backend management.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
