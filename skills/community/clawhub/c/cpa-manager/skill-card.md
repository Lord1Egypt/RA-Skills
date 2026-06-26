## Description: <br>
CLIProxyAPI (CPA) operations tool based on cpa-warden for inventory scans, 401 and quota cleanup, uploads, refill workflows, and local state tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violin321](https://clawhub.ai/user/violin321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer CLIProxyAPI auth-file pools, inspect account health, remove invalid accounts, handle quota-limited accounts, upload replacement auth files, and track local maintenance state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or remove managed CPA accounts. <br>
Mitigation: Run scan or --no-delete-401 first, review exported account lists, and require explicit human approval before maintain, upload, refill, re-enable, or auto_register operations. <br>
Risk: Management tokens, config files, logs, state databases, and account exports may expose sensitive operational data. <br>
Mitigation: Use least-privilege management tokens, keep config/state/log/export files out of shared locations and version control, and verify no real credentials are packaged. <br>
Risk: An incorrect CPA base URL or broad maintenance action can affect the wrong deployment or account set. <br>
Mitigation: Verify the CPA base URL and target auth directory before uploads or deletes, and keep backups outside the CPA auth directory. <br>
Risk: The optional auto_register hook can execute an external shell command. <br>
Mitigation: Leave auto_register disabled unless the command, working directory, output directory, and timeout have been reviewed and approved. <br>


## Reference(s): <br>
- [CPA Warden Manual Workflow](references/workflow.md) <br>
- [CPA Manager Safety Guidelines](safety.md) <br>
- [CPA Manager Troubleshooting Guide](troubleshooting.md) <br>
- [CPA Manager ClawHub Page](https://clawhub.ai/violin321/cpa-manager) <br>
- [cpa-warden](https://github.com/fantasticjoe/cpa-warden) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and Python utility scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSON exports, SQLite state, and logs when its scripts are executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
