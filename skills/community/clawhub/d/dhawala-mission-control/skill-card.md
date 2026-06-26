## Description: <br>
CLI-first system health aggregator for autonomous AI agents that checks agent processes, resource health, cron jobs, services, logs, and OpenClaw status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DhawalA4](https://clawhub.ai/user/DhawalA4) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and infrastructure maintainers use this skill to run quick health checks, inspect autonomous agent processes, review service and cron status, and gather host resource signals before deployments or incident follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive local host details, including process names, service state, listening ports, cron jobs, resource usage, and recent logs. <br>
Mitigation: Install only on hosts where the agent is trusted with operational visibility, and avoid sharing generated reports outside authorized operations channels. <br>
Risk: The restart command can restart arbitrary systemd services when run with sudo. <br>
Mitigation: Require explicit human approval before restarts and constrain sudoers policy or script behavior to known OpenClaw services where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DhawalA4/dhawala-mission-control) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only status commands by default; restart commands require explicit confirmation and sudo.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
