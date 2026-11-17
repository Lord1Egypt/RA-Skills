## Description:

Guides agents through sending and receiving transactional email with Cloudflare Email Service, including Workers bindings, REST API use, Email Routing, Agents SDK handling, setup, deliverability, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creativerezz](https://clawhub.ai/user/creativerezz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add transactional email sending, inbound email routing, Cloudflare Workers email bindings, REST API calls, and deliverability checks to applications and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-send email examples can send messages to unintended recipients or expose sensitive content.

Mitigation: Confirm recipients, sender, content, and attachments before sending, and avoid personal data or secrets unless authorized.

Risk: Broad Cloudflare credentials or logged email bodies can increase the impact of mistakes or credential exposure.

Mitigation: Use least-privilege Cloudflare tokens, store secrets outside source code, and avoid full email-body logging.

Risk: Unpinned Wrangler or npm tooling can change behavior between runs.

Mitigation: Pin Wrangler and npm dependency versions for reproducible setup and deployment.

Risk: Unsanitized content inserted into HTML email can create unsafe or misleading messages.

Mitigation: Escape or sanitize text before inserting it into HTML email templates.

## Reference(s):

- [Cloudflare Email Service docs](https://developers.cloudflare.com/email-service/)
- [Cloudflare Email Sending API reference](https://developers.cloudflare.com/api/resources/email_sending)
- [Cloudflare Workers types](https://www.npmjs.com/package/@cloudflare/workers-types)
- [Cloudflare Agents SDK docs](https://developers.cloudflare.com/agents/)
- [Cloudflare Agents email docs](https://github.com/cloudflare/agents/tree/main/docs)
- [Cloudflare MCP server](https://github.com/cloudflare/mcp)
- [Email deliverability docs](https://developers.cloudflare.com/email-service/concepts/deliverability/)
- [Email authentication docs](https://developers.cloudflare.com/email-service/concepts/email-authentication/)
- [ClawHub skill page](https://clawhub.ai/creativerezz/skills/cloudflare-email-service)
- [Workers Binding and Agents SDK sending guide](references/sending.md)
- [REST API sending guide](references/rest-api.md)
- [Inbound email routing guide](references/routing.md)
- [CLI, MCP, and setup guide](references/cli-and-mcp.md)
- [Deliverability guide](references/deliverability.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks, shell commands, configuration snippets, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real-send examples that require recipient, sender, content, attachment, token, and logging review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
