## Description:

Email Address Validation - Single verifies one email address for syntax, DNS/MX reachability, SMTP mailbox status without sending mail, and signals such as disposable, role-based, spam-trap, catch-all, or unknown results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to validate a single submitted email address before signup, checkout, CRM updates, lead qualification, or email sending workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checked email addresses are sent to an AgentPMT-hosted service.

Mitigation: Require explicit user consent before validating third-party or customer email addresses and avoid submitting sensitive addresses unless that data sharing is acceptable.

Risk: Each verification consumes account credits.

Mitigation: Confirm the user intends to spend a verification credit before calling the remote validation action.

Risk: The skill includes broad activation, setup, reinstall, and update guidance.

Mitigation: Use pinned or ClawHub-managed installation paths and review setup or update instructions before execution.

## Reference(s):

- [Email Address Validation - Single marketplace page](https://www.agentpmt.com/marketplace/email-address-validation-single)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/email-address-validation-single)
- [Email Address Validation - Single schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [AgentPMT MCP server](https://api.agentpmt.com/mcp/)
- [AgentPMT REST invoke endpoint](https://api.agentpmt.com/products/purchase)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, API calls, JSON]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides a single remote email verification action and may return status flags, suggested corrections, execution timing, address metadata, and account credit information.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
