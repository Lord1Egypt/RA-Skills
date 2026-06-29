## Description: <br>
Helps agents guide developers through sending and receiving transactional email with Cloudflare Email Service, including Workers bindings, REST API usage, Email Routing, setup, and deliverability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creativerezz](https://clawhub.ai/user/creativerezz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add transactional email sending, inbound routing, and deliverability checks to Cloudflare Workers, Agents SDK apps, or external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to send real email or change Cloudflare Email Routing. <br>
Mitigation: Confirm the sender, recipients, content, attachments, routing changes, and whether a message will actually be sent before approving commands or API calls. <br>
Risk: Cloudflare OAuth tokens, API tokens, or other sensitive credentials may be required. <br>
Mitigation: Use least-privilege credentials stored in secrets or environment variables, avoid logging them, and review generated code for accidental token exposure. <br>
Risk: Email content and routing decisions can expose sensitive information or be used outside transactional email use cases. <br>
Mitigation: Review message content and routing destinations before use, and send sensitive content only when explicitly intended and permitted. <br>


## Reference(s): <br>
- [Cloudflare Email Service Docs](https://developers.cloudflare.com/email-service/) <br>
- [Cloudflare Email Sending API Reference](https://developers.cloudflare.com/api/resources/email_sending) <br>
- [Cloudflare Workers Types](https://www.npmjs.com/package/@cloudflare/workers-types) <br>
- [Cloudflare Agents Docs](https://developers.cloudflare.com/agents/) <br>
- [Sending Emails - Workers Binding and Agents SDK](references/sending.md) <br>
- [Sending Emails - REST API](references/rest-api.md) <br>
- [Receiving and Routing Inbound Email](references/routing.md) <br>
- [CLI, MCP, and Project Setup](references/cli-and-mcp.md) <br>
- [Email Deliverability and Best Practices](references/deliverability.md) <br>
- [Cloudflare Email Service on ClawHub](https://clawhub.ai/creativerezz/cloudflare-email-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, JSON configuration, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend real Cloudflare email sending, routing, Wrangler, REST API, or MCP actions that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
