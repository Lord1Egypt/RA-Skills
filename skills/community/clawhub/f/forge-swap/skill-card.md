## Description:

Cross-chain swap routing via THORChain that gets quotes and builds non-custodial swap transaction details across 44+ assets, with a 0.5% affiliate fee to forgemb on every routed swap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morebetterclaw](https://clawhub.ai/user/morebetterclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to request THORChain cross-chain swap quotes, generate vault deposit addresses and memos, inspect supported assets, and configure MCP or REST access. It is intended for non-custodial swap workflows where the user's wallet executes the transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hosted service generates vault addresses and memos for irreversible crypto swaps.

Mitigation: Independently verify returned vault addresses and memos against THORChain data before sending funds.

Risk: Wrong address, memo, chain, asset, amount, or destination can permanently lose funds.

Mitigation: Confirm the exact asset, chain, amount, destination address, memo, and wallet transaction details before execution.

Risk: Every routed swap includes a 0.5% affiliate fee.

Mitigation: Disclose and confirm the 0.5% forgemb affiliate fee in the wallet transaction before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/morebetterclaw/skills/forge-swap)
- [Publisher Profile](https://clawhub.ai/user/morebetterclaw)
- [MoreBetter Studios Homepage](https://morebetterstudios.com)
- [FORGE API Base](https://forge-api-production-50de.up.railway.app)
- [FORGE MCP Endpoint](https://forge-api-production-50de.up.railway.app/mcp)
- [FORGE MCP Discovery](https://forge-api-production-50de.up.railway.app/.well-known/mcp.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP server configuration, REST API examples, asset formats, and self-hosting environment variables.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
