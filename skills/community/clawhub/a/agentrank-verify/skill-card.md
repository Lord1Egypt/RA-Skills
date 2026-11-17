## Description:

Verifies whether an AI agent or x402 service is real and settlement-backed before payment or trust by returning a 0-1000 AgentRank reputation score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andysalvo](https://clawhub.ai/user/andysalvo)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to check a wallet or domain before settling an x402 payment, extending credit, fronting work, routing a task, or gating service access by caller reputation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses or domains checked with the skill are sent to AgentRank/Crest Deployment Systems LLC.

Mitigation: Install and use the skill only when sharing the queried wallet address or domain with that service is acceptable.

Risk: The returned score can be mistaken for proof of safety, identity, or financial fitness.

Mitigation: Treat the score as one input to a broader trust decision and not as financial advice or a standalone safety guarantee.

## Reference(s):

- [AgentRank Skill Page](https://clawhub.ai/andysalvo/skills/agentrank-verify)
- [Publisher Profile](https://clawhub.ai/user/andysalvo)
- [AgentRank](https://agentrank.info)
- [Resolve API Example](https://api.agentrank.info/resolve/blockrun.ai)
- [AgentRank MCP Server](https://api.agentrank.info/mcp)
- [AgentRank Agent Card](https://agentrank.info/.well-known/agent-card.json)
- [Coverage Endpoint](https://api.agentrank.info/coverage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline HTTP, MCP, A2A, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses wallet addresses or domains as lookup inputs and returns reputation interpretation guidance; no local files are produced by the skill.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
