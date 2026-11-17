## Description:

Create a Shieldz crypto payment link or tip jar for a wallet the user explicitly provides, and read payment status back after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shieldz](https://clawhub.ai/user/shieldz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when an agent needs to create a confirmed Shieldz crypto payment link or tip jar, or check payment status for a user-provided Shieldz manage token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell examples and the optional local MCP package introduce review-worthy execution risk.

Mitigation: Review before installing, prefer the REST flow with a structured HTTP client or safe JSON serialization, and avoid the optional local npx MCP path unless the package is trusted and sandboxed.

Risk: Wallet address, amount, memo or title, optional email, and manage tokens are sent to Shieldz.

Mitigation: Confirm the user is comfortable sending this data before each external call, omit email unless explicitly consented to, and keep manage_url and manage_token private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shieldz/skills/crypto-payments)
- [Shieldz payment link API](https://shieldz.cash/api/v1/links)
- [Shieldz tip jar API](https://shieldz.cash/api/v1/tip-jars)
- [Shieldz MCP server](https://shieldz.cash/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST and MCP usage guidance, confirmation prompts, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public payment URLs and private manage URLs or manage tokens that require careful handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
