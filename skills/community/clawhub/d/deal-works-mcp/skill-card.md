## Description:

AI agent infrastructure for deals, escrow, attestations, and autonomous agents. 39 tools across 9 engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swgoettelman](https://clawhub.ai/user/swgoettelman)

### License/Terms of Use:

MIT

## Use Case:

Developers and external teams use this MCP server to let agents interact with deal.works workflows for deal lifecycle management, escrow, attestations, disputes, marketplace actions, agent deployment, and dashboard resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports live financial, publishing, dispute, governance, and agent-deployment actions without clear confirmation safeguards.

Mitigation: Require explicit human confirmation and spending or action limits before fund transfers, external cashouts, escrow funding, marketplace publishing, deal actions, vault sealing, disputes, voting, or agent deployment.

Risk: The security review reports inconsistent unpinned npm examples.

Mitigation: Install only the intended package, @swgoettelman/deal-works-mcp, and avoid copying the inconsistent @goettelman npx examples.

Risk: The server requires a DEAL_WORKS_API_KEY for live platform actions.

Mitigation: Use a narrowly scoped API key with transaction limits and rotate it if exposed.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/swgoettelman/skills/deal-works-mcp)
- [deal.works](https://deal.works)
- [deal.works documentation](https://docs.deal.works)
- [deal.works API reference](https://docs.deal.works/api)
- [npm package](https://www.npmjs.com/package/@swgoettelman/deal-works-mcp)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration]

**Output Format:** [MCP tool, resource, and prompt responses with JSON data and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEAL_WORKS_API_KEY and a Node.js MCP host using stdio transport.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
