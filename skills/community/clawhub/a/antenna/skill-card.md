## Description: <br>
Inter-host OpenClaw session messaging over reachable HTTPS using built-in gateway webhook hooks for sending messages, checking peer health, managing peer registries, exchanging trust material, and enabling cross-host agent communication outside visible chat channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cshirley001](https://clawhub.ai/user/cshirley001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use Antenna to let agents coordinate across separately hosted OpenClaw instances, send messages to specific sessions, pair trusted peers, and review or drain inbound message queues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation grants broad gateway, session, sandbox, and credential authority. <br>
Mitigation: Review the gateway diff before setup and install only when that level of local administrative control is acceptable. <br>
Risk: Overly broad peer or session access could allow unwanted cross-host message delivery. <br>
Mitigation: Keep inbound and outbound peer allowlists and session allowlists narrow, and enable inbox review for new or less trusted peers. <br>
Risk: Hooks tokens and identity secrets are sensitive credentials. <br>
Mitigation: Protect credential files, rotate hooks tokens and identity secrets when exposure is suspected, and audit permissions with Antenna status or doctor checks. <br>
Risk: Optional ClawReef pairing can involve third-party storage of webhook credentials. <br>
Mitigation: Avoid ClawReef unless the operator accepts that credential-storage model. <br>
Risk: Dry-run or test-report workflows may write prompts, secrets, or other sensitive content to local logs. <br>
Mitigation: Do not use those features with sensitive content unless local log exposure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cshirley001/antenna) <br>
- [Repository](https://github.com/cshirley001/openclaw-skill-antenna) <br>
- [GitHub releases](https://github.com/cshirley001/openclaw-skill-antenna/releases) <br>
- [Antenna User Guide](references/USER-GUIDE.md) <br>
- [Antenna Relay Protocol Functional Specification](references/ANTENNA-RELAY-FSD.md) <br>
- [Security Policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance and command invocations for local Antenna scripts; setup and relay flows may create or update local runtime configuration, peer registry, inbox, log, and gateway registration state.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata, skill frontmatter, changelog released 2026-04-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
