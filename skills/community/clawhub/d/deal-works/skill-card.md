## Description:

AI agent infrastructure for deals, escrow, attestations, and autonomous agents. 39 tools across 9 engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swgoettelman](https://clawhub.ai/user/swgoettelman)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this MCP server to connect agents to deal.works workflows for deal management, escrow, wallet operations, marketplace actions, autonomous agent deployment, attestations, disputes, learning resources, and dashboard checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Money-moving and agent-management tools can initiate transfers, cashouts, escrow funding, agent deployment or funding, marketplace publishing, voting, deal state changes, and vault sealing.

Mitigation: Require explicit human confirmation before each high-impact mutation and disable unused mutation tools where the host client supports tool filtering.

Risk: The skill requires a deal.works API key for authenticated access.

Mitigation: Use a dedicated, revocable, least-privilege API key and rotate it if it appears in shared logs, prompts, or configuration files.

Risk: Some installation examples may use an incorrect package name or an unpinned npm invocation.

Mitigation: Verify the package name is @swgoettelman/deal-works-mcp and pin a trusted version before installing or running the MCP server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swgoettelman/skills/deal-works)
- [deal.works homepage](https://deal.works)
- [deal.works documentation](https://docs.deal.works)
- [deal.works API reference](https://docs.deal.works/api)
- [npm package](https://www.npmjs.com/package/@swgoettelman/deal-works-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [JSON tool and resource responses, Markdown prompt guidance, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a DEAL_WORKS_API_KEY for authenticated deal.works access.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
