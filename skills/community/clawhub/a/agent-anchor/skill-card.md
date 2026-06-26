## Description: <br>
Agent Anchor is a local OpenClaw dashboard that snapshots agent state, tracks tasks, monitors cron jobs, and helps recover after interruptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metariot2026](https://clawhub.ai/user/metariot2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to set up and operate a local dashboard for agent recovery, task tracking, activity review, and cron-job monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to clone an unspecified external repository, so the code source and version are not identified. <br>
Mitigation: Confirm the repository URL, publisher, version, and code before installing or running it. <br>
Risk: Automatic agent-state snapshots may capture secrets or private workflow data. <br>
Mitigation: Review what state is saved, exclude secrets and sensitive data, and confirm how stored state can be deleted. <br>
Risk: One-click cron-job fixes can change scheduled job behavior. <br>
Mitigation: Preview proposed fixes and require explicit confirmation before applying any cron-job change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metariot2026/agent-anchor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configuration guidance centers on local state and cron-job settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
