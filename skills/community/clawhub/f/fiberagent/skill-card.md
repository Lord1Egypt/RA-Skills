## Description:

FiberAgent helps OpenClaw agents search products across merchants, compare cryptocurrency cashback, and return tracked shopping links for Monad wallet rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawlaurent](https://clawhub.ai/user/openclawlaurent)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use FiberAgent to add shopping, cashback comparison, agent registration, and earnings lookup to OpenClaw agents. It is intended for user shopping queries where affiliate-tracked links and crypto rewards are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party shopping service receives product queries, agent IDs, and wallet addresses.

Mitigation: Review the service terms before installation, send only intended shopping data, and use purpose-specific agent IDs and wallet addresses where practical.

Risk: Purchase links are affiliate-tracked and may influence cashback and reputation outcomes.

Mitigation: Disclose affiliate tracking to users and validate merchant, price, cashback rate, and destination URL before recommending a purchase.

Risk: The documented future npm install path is unpinned and has no server-resolved provenance in this release evidence.

Mitigation: Prefer the reviewed local or ClawHub install path, or pin and verify the package version and provenance before using npm installation.

## Reference(s):

- [FiberAgent Website](https://fiberagent.shop)
- [FiberAgent API Docs](https://fiberagent.shop/api/docs)
- [OpenAPI Spec](https://fiberagent.shop/server/openapi.json)
- [Agent Card](https://fiberagent.shop/.well-known/agent-card.json)
- [MCP Server](https://fiberagent.shop/api/mcp)
- [ERC-8004 Profile](https://www.8004scan.io/agents/monad/135)
- [Live Demo](https://fiberagent.shop/compare)
- [ClawHub Skill Page](https://clawhub.ai/openclawlaurent/skills/fiberagent)
- [Publisher Profile](https://clawhub.ai/user/openclawlaurent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, API endpoints, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns product search results, cashback details, affiliate URLs, agent registration responses, and agent earnings statistics through FiberAgent API calls.]

## Skill Version(s):

1.0.1 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
