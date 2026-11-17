## Description:

Look up ERC-8004 agents in the on-chain identity index and read their Cybercentry verification results before trusting them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cybercentry](https://clawhub.ai/user/cybercentry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query public ERC-8004 agent identity data and Cybercentry verification results before deciding whether to interact with an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to a remote paid MCP service.

Mitigation: Use the free catalogue and index statistics first, make precise lookups, and provide an API key or payment-capable client only when paid usage is intended.

Risk: Broad or speculative browsing can spend quota or USDC unnecessarily.

Mitigation: Prefer direct lookup by wallet or agent ID and confirm before using higher-cost report retrieval.

Risk: Verification scores can be misread when an agent has not been assessed.

Mitigation: Report the risk level and which checks have run, and describe unassessed agents as unverified rather than dangerous.

## Reference(s):

- [ERC-8126: AI Agent Verification](https://eips.ethereum.org/EIPS/eip-8126)
- [ERC-8004: Trustless Agents](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-8126scan ClawHub listing](https://clawhub.ai/cybercentry/skills/erc-8126-scan)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call a remote read-only MCP service that can require USDC payment or an API key for paid lookups.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
