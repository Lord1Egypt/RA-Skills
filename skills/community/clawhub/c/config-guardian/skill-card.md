## Description: <br>
Config Guardian helps agents make safe OpenClaw config updates with automatic backup, validation, and rollback to prevent invalid changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdhilabs](https://clawhub.ai/user/abdhilabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators using OpenClaw can have an agent apply openclaw.json changes through a backup, validation, and rollback workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An incorrect config path or value could disrupt OpenClaw behavior. <br>
Mitigation: Review the exact config path and value before approving a run; the atomic apply workflow validates with OpenClaw doctor and rolls back on validation failure. <br>
Risk: Config backups may contain sensitive values. <br>
Mitigation: Keep backups only until the change is confirmed and periodically remove old backups from ~/.openclaw/config-guardian-backups/. <br>


## Reference(s): <br>
- [Config Guardian ClawHub listing](https://clawhub.ai/abdhilabs/config-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local OpenClaw config backups under ~/.openclaw/config-guardian-backups/ when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
