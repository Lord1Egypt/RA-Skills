## Description:

Query Credit Karma (creditkarma.com) transactions from a shell with the fpx CLI (@fetchproxy/cli) instead of running the creditkarma-mcp server — capture the signed-in session cookie once, then curl the GraphQL transactions endpoint directly. Use when you want Credit Karma transaction data without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to capture a signed-in Credit Karma browser session and retrieve, paginate, and inspect their transaction records from shell scripts without installing the Credit Karma MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example commands can leave login tokens and financial records in inadequately protected temporary files.

Mitigation: Keep tokens in shell memory where possible; otherwise use a private directory created with mktemp -d, restrictive permissions, and cleanup. Avoid recording tokens in terminal logs.

Risk: Refreshing a token can affect the signed-in browser session.

Mitigation: Refresh only when the access token has expired.

Risk: External dependency code has not been audited.

Mitigation: Verify the CLI and extension releases, and approve only the stated domain and cookies.

## Reference(s):

- [Requests reference](references/requests.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Transaction data]

**Output Format:** [Markdown instructions with inline shell commands; transaction results as JSON or tab-separated text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cursor-paginated transaction records with signed USD amounts]

## Skill Version(s):

3.4.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
