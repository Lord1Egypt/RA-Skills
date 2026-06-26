## Description: <br>
Perfect Agent Comms helps two OpenClaw agents communicate through an authenticated HTTP bridge with cron-based polling, helper scripts, monitoring, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelsalespossible](https://clawhub.ai/user/joelsalespossible) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up agent-to-agent communication between controlled OpenClaw agents across instances, containers, or machines. It provides bridge deployment steps, cron polling templates, helper scripts, and operational guidance for monitoring and troubleshooting the bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous communication can let remote bridge messages drive broad workspace actions. <br>
Mitigation: Use the bridge only between agents you control, review cron jobs before enabling them, and keep bridge-derived state in dedicated files. <br>
Risk: Exposed bridge traffic or shared tokens can allow unauthorized access to agent messages. <br>
Mitigation: Bind or firewall the bridge server, use HTTPS/TLS for non-local traffic, and protect and rotate the shared token. <br>
Risk: The bridge includes a clear endpoint that can delete message state. <br>
Mitigation: Remove or restrict /api/clear before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joelsalespossible/bridge-poll) <br>
- [Cron Job Templates](artifact/references/cron-templates.md) <br>
- [Known Bugs & Gotchas](artifact/references/gotchas.md) <br>
- [Monitoring & Health Checks](artifact/references/monitoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON cron templates and shell/Python helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires operator-supplied bridge URL and shared tokens; output may include cron schedules, commands, and configuration placeholders.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
