## Description: <br>
Manage etcd key-value store operations including list, get, put, and delete with safety checks and backup-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fpbear](https://clawhub.ai/user/fpbear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and modify etcd key-value data across development, test, and production environments while following read-first and backup-before-change practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly change or delete important etcd data. <br>
Mitigation: Use read-only or non-production credentials by default, keep independent backups and audit logs, and require separate human confirmation for put, delete, or lease revoke operations. <br>
Risk: The release overstates safety controls relative to the direct write and delete behavior exposed through etcdctl. <br>
Mitigation: Treat built-in checks as guidance, not an access-control boundary; enforce production safeguards through credentials, reviews, and operational change controls outside the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fpbear/etcd-manager) <br>
- [etcd command reference](references/etcd_commands.md) <br>
- [etcd safety guidelines](references/safety_guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include etcd key names, current values, proposed new values, deletion backups, status summaries, and risk notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
