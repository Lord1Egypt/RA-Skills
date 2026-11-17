## Description:

AI-powered wireless network manager that diagnoses Wi-Fi and hotspot connectivity, scores RF conditions, explains congestion and interference, and proposes or runs approved optimization actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and laptop users use this skill to let a local agent diagnose wireless problems, compare Wi-Fi and mobile hotspot options, explain RF interference, and guide connectivity improvements. It can also support monitoring and presence-sensing workflows when the user explicitly enables them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or execute network changes such as DNS updates, DHCP renewal, Wi-Fi switching, or adapter restart.

Mitigation: Use quick scan or read-only mode by default, require explicit approval for remediation commands, and review each command before allowing privileged execution.

Risk: Sentinel and presence-sensing modes can infer nearby movement from RF signal changes.

Mitigation: Enable these modes only with informed consent from affected people and avoid using them for surveillance or security decisions.

Risk: Monitoring modes may store RF history, calibration data, model weights, and action logs locally.

Mitigation: Keep the data directory user-controlled, prune retained history, and avoid enabling background monitoring when persistent local records are not acceptable.

Risk: The runtime depends on local shell execution and optional Python dependencies.

Mitigation: Run in a pinned virtual environment, install only reviewed dependencies, and limit shell permissions to the operating modes the user actually needs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielfoojunwei/skills/agentic-wireless-manager)
- [README](README.md)
- [Permissions and Controls](docs/PERMISSIONS_AND_CONTROLS.md)
- [RF Environment Intelligence](docs/RF_ENVIRONMENT_INTELLIGENCE.md)
- [SAC-LTC Architecture](docs/SAC_LTC_ARCHITECTURE.md)
- [Training Pipeline](docs/TRAINING_PIPELINE.md)
- [Cross-Platform Commands](docs/CROSS_PLATFORM_COMMANDS.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON outputs from the Python CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local RF history, model weights, calibration data, and action logs under ~/.net-intel/ when those modes are enabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
