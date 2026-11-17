## Description:

Claw-Net lets agents ask plain-language questions and route them to ClawNet APIs for orchestrated data answers, structured data-skill queries, and optional provenance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1xmint](https://clawhub.ai/user/1xmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to ClawNet for natural-language data orchestration, marketplace skill browsing, direct structured data queries, and paid x402/API-key workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and related metadata are sent to ClawNet and may be routed to downstream providers.

Mitigation: Avoid secrets and confidential data in prompts; review ClawNet data handling before using sensitive workloads.

Risk: Paid x402/API usage can spend credits or USDC automatically.

Mitigation: Use spending controls, low-balance wallets, and cost estimation before production use.

Risk: The MCP setup references an unpinned local command for code that is not included while exposing an API key.

Mitigation: Review the referenced server code, pin dependencies through a controlled lockfile, and scope CLAWNET_API_KEY before enabling MCP.

## Reference(s):

- [Claw-Net ClawHub listing](https://clawhub.ai/1xmint/skills/claw-net)
- [ClawNet homepage](https://claw-net.org)
- [ClawNet SOMA identity](https://api.claw-net.org/.well-known/soma.json)
- [Soma protocol paper](https://doi.org/10.5281/zenodo.19260081)
- [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides API-key, x402, and MCP setup; protected endpoints require CLAWNET_API_KEY or wallet-based payment.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
