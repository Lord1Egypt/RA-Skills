## Description:

Chainflip Swap helps agents quote, start, and monitor native cross-chain cryptocurrency swaps through Chainflip Broker as a Service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baas](https://clawhub.ai/user/baas)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agent-assisted native crypto swaps across supported assets. It supports route discovery, quote presentation, deposit-address swap creation, and status checks through the Chainflip BaaS MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a mutable remote MCP service for deposit-address generation and swap status for irreversible real-funds transfers.

Mitigation: Before funding any address, independently verify the endpoint, asset identifiers, recipient address, refund address, minimum price, fees, and deposit address.

Risk: Remote prompt guidance from the service could change independently of the released skill artifact.

Mitigation: Avoid loading the remote prompt unless it is needed, and review any remote guidance before using it for a funded swap.

Risk: An optional partner API key may be sent to the remote service when starting a swap.

Mitigation: Omit the API key unless broker commission attribution is intentionally required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baas/skills/chainflip)
- [Chainflip BaaS documentation](https://chainflip-broker.io/ai)
- [Chainflip Broker as a Service](https://chainflip-broker.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with MCP tool calls, inline shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include real-funds swap quotes, deposit addresses, swap IDs, status updates, and optional MCP setup instructions.]

## Skill Version(s):

1.0.0 (source: release metadata; SKILL.md metadata reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
