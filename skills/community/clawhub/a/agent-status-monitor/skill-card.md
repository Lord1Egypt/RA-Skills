## Description: <br>
Checks the runtime, process, session, and activity status of local AI development agents such as Claude Code, OpenCode, OpenClaw, and Cursor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willin](https://clawhub.ai/user/willin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check whether local AI development agents are running, active, waiting, idle, or unavailable. It is intended for local workstation status reporting across supported tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram command output may reveal which local tools are running, session counts, configuration paths, and OpenClaw status details. <br>
Mitigation: Enable Telegram integration only in private or authorized chats, and avoid use in broad group channels. <br>
Risk: The optional Telegram installer changes OpenClaw command configuration. <br>
Mitigation: Run the installer only deliberately after reviewing the configuration change and keep a backup of the existing OpenClaw configuration. <br>
Risk: Activity status is inferred from local processes and session file modification times, so it can be incomplete or stale. <br>
Mitigation: Use the status report as a local health signal and manually verify agent state when the result affects operational decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/willin/agent-status-monitor) <br>
- [Agent Commands Reference](references/agent-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status summaries with shell command output and optional configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local process status, session counts, activity recency, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
