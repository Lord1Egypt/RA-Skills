## Description: <br>
Local-first agent storage for persisting SQLite data, virtual filesystem content, and memory in one local .db file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhao6741](https://clawhub.ai/user/liuhao6741) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use agt0 to persist local working state, query CSV, JSONL, logs, and stored files with SQL, and manage file-like memory through the agt0 CLI or Node API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: agt0 databases are persistent local storage and may contain sensitive data if an agent stores it there. <br>
Mitigation: Avoid storing secrets unless intentional, keep backups of important .db files, and apply normal local file access controls. <br>
Risk: The skill includes delete commands for files, branches, and databases. <br>
Mitigation: Review destructive commands before execution and back up important .db files before deleting data. <br>


## Reference(s): <br>
- [agt0 ClawHub page](https://clawhub.ai/liuhao6741/agt0) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on local SQLite-backed storage and agt0 CLI or Node API usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
