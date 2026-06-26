## Description: <br>
Automatically reload AGENTS.md regularly to maintain fresh context, prevent session drift, and keep memory and tasks updated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kentaroid-bot](https://clawhub.ai/user/kentaroid-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to keep long-running OpenClaw sessions aligned with local identity, instruction, and memory files. It proposes periodic context refreshes, heartbeat updates, cron scheduling, and MEMORY.md distillation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring local memory maintenance can repeatedly read sensitive agent context and memory files. <br>
Mitigation: Install only in workspaces where recurring context refresh is intended, and review AGENTS.md, IDENTITY.md, SOUL.md, USER.md, and memory logs before enabling the cron schedule. <br>
Risk: The skill can lead to recurring writes to MEMORY.md and HEARTBEAT.md. <br>
Mitigation: Periodically inspect MEMORY.md and HEARTBEAT.md for unwanted changes and adjust or disable the schedule when the workflow is no longer needed. <br>
Risk: The bundled cron example uses a specific timezone and schedule that may not match the user's operating context. <br>
Mitigation: Review and adjust the cron timezone and cadence before enabling the scheduled refresh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kentaroid-bot/agents-refresh) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell and cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace file-edit and scheduling guidance; no Python scripts are included.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
