## Description: <br>
Security engineering workflow for OpenClaw privilege governance and hardening, including least-privilege execution, approval-first privileged actions, idle timeout controls, port and egress monitoring, and ISO 27001/NIST-aligned compliance reporting with mitigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FletcherFrimpong](https://clawhub.ai/user/FletcherFrimpong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, platform engineers, and security engineers use this skill to enforce approval-first privileged operations, command and prompt policy checks, local port and egress monitoring, and compliance reporting for OpenClaw environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mediate privileged OpenClaw operations through sudo-related controls and local runtime monitoring. <br>
Mitigation: Review the sudo shim before enabling the runtime hook, configure a restrictive command-policy.json, and keep a documented removal path for any LaunchAgent PATH change. <br>
Risk: Security state and policy files under ~/.openclaw influence privileged execution and monitoring behavior. <br>
Mitigation: Protect ~/.openclaw and ~/.openclaw/security permissions and review command, prompt, approved port, and egress allowlist policies before operational use. <br>
Risk: Notification hooks may execute operator-configured commands. <br>
Mitigation: Avoid OPENCLAW_VIOLATION_NOTIFY_CMD unless the configured command is fully trusted and scoped to the intended notification behavior. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/FletcherFrimpong/fletcher-cyber-security-engineer) <br>
- [Least-Privilege Policy For OpenClaw](artifact/references/least-privilege-policy.md) <br>
- [Port Monitoring Policy For OpenClaw](artifact/references/port-monitoring-policy.md) <br>
- [Compliance Controls Map](artifact/references/compliance-controls-map.json) <br>
- [Command Policy Template](artifact/references/command-policy.template.json) <br>
- [Egress Allowlist Template](artifact/references/egress-allowlist.template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status reports with check IDs, risk, evidence, mitigations, and optional JSON or shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should include affected check IDs, status, risk, concise evidence, concrete mitigations, and network finding details when applicable.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
