## Description:

Deploy OpenClaw subagents to their own cloud server: start another OpenClaw agent on a confidential virtual machine (CVM, a sealed Intel TDX VM) for agents that hold keys or money, or on a cheap plain VM for workers with nothing secret, one per agent, for trading swarms or any swarm, by the hour, paid in USDC from a prepaid Agentgates balance. Its model is Agentgates inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to provision, manage, and message separate OpenClaw workers on Agentgates virtual machines. They can place sensitive workloads on confidential VMs and reserve plain VMs for public work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the skill suspicious for environment and network capabilities beyond its declared permissions; its partial scan covered 66.7% of components and included opaque script content.

Mitigation: Review the skill's script and verify that you trust Agentgates and understand what data and credentials it receives before use.

Risk: On a plain VM, the host can read the disk, memory, and environment, including the gateway token and inference key; the skill documents no proof for this plan.

Mitigation: Keep secrets and private data on confidential machines, use plain VMs only for public work, and check the confidential machine's proof page before sending it secrets.

Risk: The skill provisions and renews hourly machines and consumes prepaid compute and inference balances.

Mitigation: Set explicit --max-usd limits for purchases and renewals, and keep only the intended budget in each prepaid balance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/agentgates/skills/agentgates-swarm)
- [Agentgates project](https://github.com/agentgates-ai/agentgates)
- [Agentgates compute API documentation](https://api.agentgates.ai/api/compute/docs)
- [Agentgates inference API documentation](https://api.agentgates.ai/api/inference/docs)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Guidance, Text]

**Output Format:** [Shell commands, API requests, JSON configuration, and agent response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provisioning and renewal require an explicit per-purchase USD cap and available prepaid compute balance.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
