## Description:

AICash Network auto-miner for $CASH tokens on Base L2. Use when setting up automated Proof of Compute mining on the AICash mempool network. Supports multi-instance mining, systemd service management, and real-time stats tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doctor-1017](https://clawhub.ai/user/doctor-1017)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and manage automated Proof of Compute mining for the AICash mempool network on systems intended for continuous mining.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent root-level mining services and performs continuous network activity.

Mitigation: Use only on a dedicated machine where continuous mining, network traffic, and boot-persistent services are intended.

Risk: Credentials and endpoint values may be stored insecurely by the setup flow.

Mitigation: Prefer storing API keys and wallet configuration in protected files or environment settings and do not pass untrusted API key, wallet, endpoint, service name, or instance values.

Risk: Service management scripts target miner services by name pattern.

Mitigation: Confirm the exact services before start or stop operations, or update the scripts to target only owned service units.

## Reference(s):

- [AICash Network](https://aicash.network)
- [AICash Miner on ClawHub](https://clawhub.ai/doctor-1017/skills/aicash-miner)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Text]

**Output Format:** [Markdown with shell commands and generated service configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and management guidance for persistent miner services, including status text and runtime statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
