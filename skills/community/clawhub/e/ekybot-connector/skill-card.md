## Description: <br>
Connect OpenClaw to Ekybot for remote agent control, Companion machine health, and project memory sync. Use when installing/configuring the connector, validating connectivity, or improving onboarding from first connection to first successful live test. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regiomag](https://clawhub.ai/user/regiomag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to install and operate an Ekybot connector that lets Ekybot web and mobile clients monitor and manage local OpenClaw agents, relay inter-agent mentions, sync selected memory files, and validate connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cloud-driven control over local OpenClaw agents can change local agent configuration and relay prompts after enrollment. <br>
Mitigation: Install only for an intended Ekybot-managed environment, use a dedicated OpenClaw setup, keep backups of ~/.openclaw, and disconnect or revoke the companion token when remote management is no longer needed. <br>
Risk: Memory sync and telemetry can upload selected workspace memory files, inventory, and machine health metadata to Ekybot. <br>
Mitigation: Review the documented data scope before first run, disable memory sync with EKYBOT_COMPANION_MEMORY_SYNC=false or telemetry with EKYBOT_COMPANION_POLL_INTERVAL_MS=0 when appropriate, and avoid sensitive workspaces unless this upload is acceptable. <br>
Risk: Remote desired-state operations may remove managed agents or delete associated workspaces. <br>
Mitigation: Back up OpenClaw configuration and managed workspaces before setup, review dashboard-driven changes before applying them, and preserve workspaces when deletion is not intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/regiomag/ekybot-connector) <br>
- [Ekybot homepage](https://www.ekybot.com) <br>
- [Ekybot Companion enrollment](https://www.ekybot.com/companion) <br>
- [Ekybot API endpoint](https://www.ekybot.com/api) <br>
- [API reference](references/api.md) <br>
- [Security model](references/security.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Inter-Agent Communication Protocol](templates/INTER-AGENT-PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install a Node.js daemon, write local OpenClaw/Ekybot configuration, run health checks, and relay remote operations after enrollment.] <br>

## Skill Version(s): <br>
6.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
