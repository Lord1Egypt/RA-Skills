## Description:

Guides agents through deploying, configuring, monitoring, and optimizing GPU-backed Bittensor Subnet 85 VidAIo video compression and upscaling miners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxquick](https://clawhub.ai/user/maxquick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and maintain Bittensor SN85 mining instances on rented GPU infrastructure, including port routing, process supervision, video encoding optimizations, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet material can be exposed when copied to rented infrastructure.

Mitigation: Use dedicated low-value miner hotkeys only and never copy coldkeys or broad wallet directories to the rented host.

Risk: Root-level deployment steps and downloaded binaries increase host compromise impact.

Mitigation: Avoid running miner services as root where practical, and pin and verify downloaded code and binaries before use.

Risk: Public miner and backend ports can unintentionally expose services.

Mitigation: Expose only required ports and apply appropriate network controls while verifying external routing.

Risk: Overwriting system DNS can break name resolution or make rollback difficult.

Mitigation: Back up resolver configuration and prepare a rollback plan before changing DNS settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxquick/skills/bittensor-sn85-vibe-miner)
- [Optimization History](references/optimization-history.md)
- [Vast.ai Port Mapping Reference](references/port-mapping.md)
- [VidAIo Subnet technical repository](https://github.com/Cazure8/vidaio-subnet)
- [Bittensor documentation](https://docs.bittensor.com)
- [Vast.ai](https://vast.ai)
- [VibeMiner related reference](https://github.com/maxquick/VibeMiner)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational checks, troubleshooting steps, and concrete file edits for miner services.]

## Skill Version(s):

2.1.0 (source: release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
