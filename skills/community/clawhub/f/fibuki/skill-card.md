## Description:

Connect to European bank accounts via PSD2 Open Banking to browse transactions, match receipts to payments, categorize expenses, and manage business partners through FiBuKI.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felixtosh](https://clawhub.ai/user/felixtosh)

### License/Terms of Use:

MIT-0

## Use Case:

Businesses, bookkeepers, and agents working with European banking data use this skill to connect FiBuKI accounts, browse PSD2 transactions, match receipts and invoices to payments, categorize expenses, and manage partners.

### Deployment Geography for Use:

Europe

## Known Risks and Mitigations:

Risk: The skill asks users to provide a FiBuKI financial API key during setup.

Mitigation: Enter the key only through a trusted secret or configuration UI, avoid pasting it into chat, and rotate or revoke the key if it may have been exposed.

Risk: The delete_source action deletes an entire account source rather than an individual transaction.

Mitigation: Require a clear account or source name and deliberate confirmation before allowing delete_source to run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felixtosh/skills/fibuki)
- [FiBuKI homepage](https://fibuki.com)
- [FiBuKI machine-readable docs](https://fibuki.com/llm.txt)
- [FiBuKI OpenAPI spec](https://fibuki.com/api/openapi.json)
- [FiBuKI MCP SSE endpoint](https://fibuki.com/api/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint, tool, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIBUKI_API_KEY for authenticated FiBuKI API access.]

## Skill Version(s):

0.1.15 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
