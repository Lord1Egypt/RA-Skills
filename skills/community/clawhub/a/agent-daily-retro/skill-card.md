## Description: <br>
Runs a daily retrospective for an OpenClaw agent by collecting prior session records, summarizing six review dimensions, updating memory and agent profile files, writing a completion lock, and reporting the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morrison230](https://clawhub.ai/user/morrison230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators use this skill to run a repeatable daily review of OpenClaw session history, capture lessons learned, and persist updates into workspace memory and agent configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads prior OpenClaw conversation history, which may contain private user or project information. <br>
Mitigation: Run it only after explicit consent for the target workspace and agent session directory, and review what session data is available before scheduling automated runs. <br>
Risk: The skill persists user and agent profile conclusions into memory and core configuration files. <br>
Mitigation: Run manually first, inspect generated changes, and keep backups of MEMORY.md, USER.md, SOUL.md, and AGENTS.md before accepting persistent updates. <br>
Risk: The bundled configuration includes external Feishu reporting. <br>
Mitigation: Disable or replace the webhook before use, and verify that any external notification channel is approved for the information being sent. <br>
Risk: Scheduled or root cron execution can repeatedly modify workspace files without active review. <br>
Mitigation: Avoid root cron unless required, prefer a scoped user account, and use the dated lock files plus log review to confirm each run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/morrison230/agent-daily-retro) <br>
- [README.md](artifact/README.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown memory entries and reports, file updates, console text, and optional Feishu notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily memory files, may update MEMORY.md, USER.md, SOUL.md, and AGENTS.md, creates dated lock files, and includes backup behavior before core file changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
