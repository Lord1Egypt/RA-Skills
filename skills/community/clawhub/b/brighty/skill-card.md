## Description:

Banking interface for AI bots and automation. Get a bank account, issue a Mastercard, buy and sell crypto, send payments and invoices - all via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maay](https://clawhub.ai/user/maay)

### License/Terms of Use:


## Use Case:

External developers and automation operators use this skill to connect an agent to Brighty business or freelance banking workflows, including account, card, transfer, payout, and team-management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-runs mutable GitHub code while using a sensitive Brighty owner API token.

Mitigation: Install only after reviewing a pinned commit or vetted package release, use the least-privileged revocable token available, and rotate or monitor the token when the dependency changes.

Risk: Banking actions can move funds or close accounts if executed without clear owner approval.

Mitigation: Keep payout confirmations outside the MCP server, show amounts and recipients clearly, and require explicit confirmation before payouts or account termination.

Risk: The BRIGHTY_API_KEY can expose banking access if stored in skill text, memory files, or chat history.

Mitigation: Store the key only in the local environment or local MCP configuration and avoid including it in prompts, logs, memory, or committed files.

## Reference(s):

- [Brighty MCP homepage](https://github.com/Maay/brighty_mcp)
- [Brighty API documentation](https://apidocs.brighty.app/docs/api/brighty-api)
- [Brighty](https://brighty.app)
- [ClawHub skill page](https://clawhub.ai/maay/skills/brighty)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and BRIGHTY_API_KEY for live Brighty API access.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
