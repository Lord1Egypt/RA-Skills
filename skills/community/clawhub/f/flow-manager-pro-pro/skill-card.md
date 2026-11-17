## Description:

流程管理器(专业版) helps agents administer Node-RED environments across multiple instances, backups, Docker orchestration, monitoring, rollback, and audit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, DevOps engineers, SREs, and automation operations teams use this skill to manage Node-RED instances, backups, Docker operations, monitoring alerts, version rollback, and audit reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad production-impacting changes to Node-RED and Docker environments.

Mitigation: Restrict use to approved instances, require explicit confirmation for production changes, and prefer dry-run or diff review before sync, deploy, rollback, or recovery actions.

Risk: Backups and configuration exports may contain secrets, environment variables, or authentication material.

Mitigation: Protect backup files, use encryption where available, and avoid exposing tokens or configuration archives in logs or shared channels.

Risk: Multi-instance sync, rollback, and recovery actions can overwrite flows or change runtime behavior.

Mitigation: Review target instance diffs, keep recent backups, and confirm the intended environment before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/flow-manager-pro-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production-impacting operational steps for Node-RED and Docker environments.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
