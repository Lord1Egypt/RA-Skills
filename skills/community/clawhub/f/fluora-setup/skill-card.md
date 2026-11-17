## Description:

Interactive setup wizard for Fluora marketplace integration that clones fluora-mcp from GitHub, builds locally, generates a wallet, and configures mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chetan-guevara](https://clawhub.ai/user/chetan-guevara)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to prepare a local Fluora marketplace integration, including a local fluora-mcp build, wallet setup, funding guidance, and mcporter registry configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup downloads and runs mutable upstream GitHub code and npm dependencies.

Mitigation: Inspect or pin the upstream fluora-ai/fluora-mcp revision and review npm dependencies before running the setup.

Risk: The setup handles a real cryptocurrency wallet and private key file.

Mitigation: Use a fresh low-balance wallet, verify wallet file permissions, and avoid storing more funds than needed for testing.

Risk: The setup persistently changes mcporter configuration, and the advertised skip controls are not implemented in the submitted script.

Mitigation: Back up and review mcporter.json after running the setup, and manually remove or adjust the Fluora registry entry if needed.

## Reference(s):

- [Fluora marketplace](https://fluora.ai)
- [fluora-mcp GitHub repository](https://github.com/fluora-ai/fluora-mcp)
- [ClawHub skill listing](https://clawhub.ai/chetan-guevara/skills/fluora-setup)
- [Base network](https://base.org)
- [Base bridge](https://bridge.base.org)
- [Base block explorer](https://basescan.org)
- [USDC information](https://www.circle.com/en/usdc)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Interactive terminal text with command guidance, local configuration changes, and a setup result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, and git; creates or updates local Fluora, wallet, and mcporter files.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact package.json and _meta.json list 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
