## Description: <br>
Auto-update OpenClaw and skills with OpenClaw cron, per-skill defaults, backups, and migration-aware summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure recurring OpenClaw and ClawHub skill updates with per-skill defaults, backups, migration gates, and update summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring update automation can apply OpenClaw or skill changes after setup. <br>
Mitigation: Review the exact cron entry before approving it, and use notify, manual, or all-out modes when tighter control is needed. <br>
Risk: Backups can copy sensitive folders if the user intentionally includes them. <br>
Mitigation: Keep credential folders out of backup scope unless there is an explicit need to copy them. <br>
Risk: Skill updates may involve migration or state-path changes. <br>
Mitigation: Keep migration pauses enabled so unclear or stateful changes require review before application. <br>


## Reference(s): <br>
- [Auto-Update ClawHub page](https://clawhub.ai/ivangdavila/auto-update) <br>
- [Auto-Update homepage](https://clawic.com/skills/auto-update) <br>
- [Setup guide](artifact/setup.md) <br>
- [Daily execution order](artifact/execution.md) <br>
- [Defaults and modes](artifact/policy.md) <br>
- [Rollback rules](artifact/recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local policy, schedule, backup, migration, and run-log ledgers when the user approves setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
