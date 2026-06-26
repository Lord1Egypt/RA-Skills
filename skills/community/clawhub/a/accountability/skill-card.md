## Description: <br>
Tracks follow-ups for every action with a future outcome - deploys, crons, fixes, configs - by maintaining a centralized FOLLOWUPS.md with structured items, escalating failures, and archiving resolved items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to register, verify, escalate, and archive follow-ups for deploys, cron jobs, fixes, configuration changes, migrations, integrations, and data pipeline runs with future outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may maintain persistent operations follow-up files that influence later agent behavior. <br>
Mitigation: Keep FOLLOWUPS.md and related accountability files trusted, reviewed, and scoped to the intended workspace. <br>
Risk: Stored check commands may run production-like verification commands or use environment variables. <br>
Mitigation: Require confirmation before running stored commands and use environment variable references instead of embedding secrets. <br>
Risk: Heartbeat or external automation could run checks without clear approval boundaries. <br>
Mitigation: Inspect and approve any heartbeat or automation setup before enabling it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tracking entries, status summaries, and copy-pasteable shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain persistent ACCOUNTABILITY.md, FOLLOWUPS.md, and ARCHIVE.md files in the workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
