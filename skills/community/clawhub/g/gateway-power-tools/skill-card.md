## Description: <br>
Operate and maintain OpenClaw installations with CLI commands, configuration management, channel, agent, and model setup, security auditing, troubleshooting, and gateway administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyafeichina](https://clawhub.ai/user/liyafeichina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer OpenClaw installations, including channel setup, agent and model management, configuration changes, security audits, troubleshooting, gateway operations, cron, logs, and memory tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested administrative commands can change OpenClaw configuration, remove channels or agents, alter cron jobs, restart gateways, or index memory. <br>
Mitigation: Confirm the target environment, back up relevant configuration, review commands before execution, and verify changes with OpenClaw status or doctor commands. <br>
Risk: The skill covers workflows that may involve OAuth tokens, bot tokens, API keys, passwords, and other sensitive credentials. <br>
Mitigation: Avoid exposing secrets in prompts or logs, prefer credential stores, environment variables, or token files, restrict file permissions, and run security audits before and after changes. <br>
Risk: Gateway auth, open DM policies, wildcard origins, broad subagent access, or weak file permissions can expose an OpenClaw installation. <br>
Mitigation: Enable gateway token auth, restrict origins and allowlists, scope subagent access, harden credential permissions, and rerun deep security audits after remediation. <br>


## Reference(s): <br>
- [OpenClaw CLI Cheat Sheet](references/cli-cheatsheet.md) <br>
- [OpenClaw Security Audit Reference](references/security-audit.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw CLI Documentation](https://docs.openclaw.ai/cli) <br>
- [OpenClaw Channel CLI Documentation](https://docs.openclaw.ai/cli/channels) <br>
- [OpenClaw Agent CLI Documentation](https://docs.openclaw.ai/cli/agents) <br>
- [OpenClaw Model CLI Documentation](https://docs.openclaw.ai/cli/models) <br>
- [OpenClaw Config CLI Documentation](https://docs.openclaw.ai/cli/config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational checklists, CLI command sequences, configuration paths, diagnostics, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
