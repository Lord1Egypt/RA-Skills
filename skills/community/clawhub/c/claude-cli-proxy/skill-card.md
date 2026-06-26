## Description: <br>
Set up a local HTTP proxy that routes OpenClaw model requests through Claude Code CLI using a Team, Max, or Pro subscription instead of API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxsorto](https://clawhub.ai/user/maxsorto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw to send local Anthropic-compatible model requests through Claude Code CLI and a persistent acpx session. It helps users run OpenClaw with Claude subscription authentication while preserving streaming-compatible provider behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The proxy forwards full OpenClaw system context, recent conversation history, and the current user message through Claude Code. <br>
Mitigation: Install only when that routing is intended, keep the proxy bound to localhost, and avoid placing secrets or broad identity files in persistent configs. <br>
Risk: The proxy writes system prompt content to `.ccproxy-system-context.md`, which can persist on disk between requests. <br>
Mitigation: Use a controlled workspace, review what context is written there, and remove the file or workspace data when decommissioning the proxy. <br>
Risk: Autostart options can create persistent LaunchAgent, systemd, heartbeat, or acpx session state. <br>
Mitigation: Review the scripts before enabling autostart and keep clear stop and removal steps for the service and acpx session. <br>


## Reference(s): <br>
- [Claude CLI Proxy on ClawHub](https://clawhub.ai/maxsorto/claude-cli-proxy) <br>
- [Auto-Start Configuration](references/autostart.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, JSON, plist, systemd, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps and proxy scripts for a localhost HTTP service that forwards OpenClaw context through Claude Code CLI.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
