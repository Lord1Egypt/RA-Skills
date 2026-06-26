## Description: <br>
Create, configure, and orchestrate autonomous AI agents on OpenClaw, including personas, memory systems, cron schedules, and multi-agent teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crispyangles](https://clawhub.ai/user/Crispyangles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scaffold autonomous OpenClaw agent workspaces, define agent persona and memory files, and configure scheduled workflows for ongoing operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous cron workflows can act on local files or connected services outside the operator's intended scope. <br>
Mitigation: Define allowed files, connected accounts, approval gates, alert destinations, quotas, and a quick disable path before enabling cron workflows. <br>
Risk: Generated agents may store sensitive operator context or operational details in memory files. <br>
Mitigation: Limit workspace access, define sensitive-data redaction rules, and keep audit logs for autonomous actions. <br>
Risk: Scheduled agents may communicate externally or create obligations if those actions are not constrained. <br>
Mitigation: Require human approval before external communication, spending, irreversible actions, or actions outside the defined scope. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Crispyangles/autonomous-agent-toolkit) <br>
- [Cron Patterns for Autonomous Agents](references/cron-patterns.md) <br>
- [SOUL.md Patterns & Templates](references/soul-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, shell command examples, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generator can create SOUL.md, AGENTS.md, HEARTBEAT.md, USER.md, MEMORY.md, and a daily memory log.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
