## Description:

A2A Agent Lookup helps agents verify AI agents, find A2A endpoints, and check trust and reputation data by querying RNWY's registry of verified AI agent cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rnwy](https://clawhub.ai/user/rnwy)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this skill before interacting or transacting with an AI agent to retrieve live A2A card data, including identity, endpoints, on-chain registration details, and RNWY trust metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on RNWY-hosted registry data when checking agents and endpoints.

Mitigation: Review returned agent card data, endpoint identity, and trust metrics before relying on them for transactions or agent hiring decisions.

Risk: The skill requires network access to RNWY registry endpoints for its lookup behavior.

Mitigation: Limit use to the documented RNWY registry and A2A card endpoints and avoid sending unrelated sensitive data in requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rnwy/skills/a2a-agent-lookup)
- [RNWY registry](https://rnwy.com)
- [RNWY agents API](https://rnwy.com/api/agents)
- [RNWY A2A card endpoint pattern](https://rnwy.com/explorer/base/{agentId}/.well-known/agent-card.json)
- [Maven Vesper example A2A card](https://rnwy.com/explorer/base/19544/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown with HTTP endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No local execution, persistence, or credential handling found in the release evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata; released 2026-02-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
