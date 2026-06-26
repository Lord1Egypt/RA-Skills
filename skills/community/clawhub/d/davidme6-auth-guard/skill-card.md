## Description: <br>
Auth Guard adds an opt-in authorization and audit wrapper that asks users to approve external API operations before an agent or integration proceeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Auth Guard to require explicit approval for sensitive external API actions, configure strict or whitelist authorization behavior, and review audit logs for agent-driven operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on Auth Guard as a universal API firewall even though the scan evidence describes it as an opt-in wrapper. <br>
Mitigation: Use it only where API calls explicitly invoke the wrapper, and keep separate platform controls for credentials, network access, and tool permissions. <br>
Risk: Agents or automated processes could approve requests or write decision files. <br>
Mitigation: Do not let agents run the approve command or write to the decision directory; keep approval actions under user-controlled permissions. <br>
Risk: Default or placeholder configuration can weaken protection or expose sensitive payloads through notifications. <br>
Mitigation: Keep STRICT mode enabled, replace placeholder API keys, restrict permissions on ~/.auth_guard, use trusted webhook destinations, and avoid sending sensitive payloads in notification messages. <br>
Risk: Installer behavior may overwrite existing configuration. <br>
Mitigation: Review or modify the installer before running it, especially on systems with an existing ~/.auth_guard configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/davidme6-auth-guard) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [ClawHub manifest](artifact/clawhub.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown documentation, Python code, JSON configuration, shell commands, and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When used, the skill can write local configuration, decision, and audit-log files under ~/.auth_guard.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
