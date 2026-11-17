## Description:

Confidential computers for AI swarms: rent a confidential VM (Intel TDX) for each agent by the hour with USDC over x402 and run a Docker workload on it. No signup; the paying wallet owns the machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to price, deploy, and monitor paid confidential VMs for agent workloads. They can run container workloads on dedicated Intel TDX machines and retrieve their endpoints and attestation quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployments incur USDC charges, and prices can change with network gas costs.

Mitigation: Read the live amount from the payment offer before authorizing it; obtain human approval or stay within an authorized budget.

Risk: Workload configuration and supplied secrets are sent to the provider, and the remote service was not audited.

Mitigation: Assess the provider's confidentiality and attestation guarantees before sending sensitive data, and keep secrets re-settable.

Risk: A workload without a published port can run and incur charges without a reachable service endpoint.

Mitigation: Ensure the container configuration publishes a port before deployment.

## Reference(s):

- [Agentgates Compute API documentation](https://api.agentgates.ai/api/compute/docs)
- [Agentgates Compute MCP service](https://mcp.agentgates.ai/compute)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTTP and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure and launch paid compute workloads using USDC.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
