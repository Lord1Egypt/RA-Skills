## Description:

Interact with the Ceaser privacy protocol on Base L2 using the ceaser-mcp MCP tools for shield, unshield, note management, and protocol queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyra-v21](https://clawhub.ai/user/zyra-v21)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to query Ceaser protocol state, prepare shield transactions, manage local notes, and unshield ETH through Ceaser's Base L2 privacy workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Bash and unpinned npx execution for workflows that may handle ETH withdrawal notes.

Mitigation: Review the ceaser-mcp package before installation or use, and run commands only in an environment where fetching npm code at use time is acceptable.

Risk: Ceaser backup strings and ~/.ceaser-mcp/notes.json can control later withdrawals.

Mitigation: Treat note backups and the local notes file like wallet private keys; avoid shared machines and secure backups before transacting.

Risk: Incorrect recipient addresses or transaction details can cause irreversible asset loss.

Mitigation: Independently verify recipient addresses, denominations, fees, and unsigned transaction data before signing or settling.

Risk: The skill contacts ceaser.org and depends on its facilitator and API availability.

Mitigation: Check facilitator health, status, and indexer sync before relying on shield or unshield workflows.

## Reference(s):

- [Ceaser homepage](https://ceaser.org)
- [ClawHub skill page](https://clawhub.ai/zyra-v21/skills/ceaser)
- [Publisher profile](https://clawhub.ai/user/zyra-v21)
- [Ceaser MCP package](https://www.npmjs.com/package/ceaser-mcp)
- [OpenAPI specification](references/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run ceaser-mcp CLI commands and public Ceaser API calls; transaction details, note backups, and recipient addresses require user review.]

## Skill Version(s):

1.4.2 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
