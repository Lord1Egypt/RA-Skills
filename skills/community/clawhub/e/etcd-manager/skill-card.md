## Description:

Manage etcd key-value store operations including list, get, put, and delete with safety checks and backup-oriented workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fpbear](https://clawhub.ai/user/fpbear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage etcd configuration and distributed-system state across dev, test, and production environments. It is most appropriate when the user can supply an authorized etcd endpoint and review proposed write or delete operations before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to read, write, or delete etcd keys using credentials available in the current environment.

Mitigation: Use only trusted endpoints and credentials, restrict key prefixes where possible, and require human review before put or delete operations.

Risk: The artifact describes backup, confirmation, production-safety, and audit controls more strongly than the helper scripts can enforce by themselves.

Mitigation: Add external backup, confirmation, allowlist, and audit mechanisms before using the skill on production or shared clusters.

Risk: The connection test script creates and deletes a test key on the supplied etcd endpoint.

Mitigation: Run connection tests only against disposable or explicitly approved clusters.

## Reference(s):

- [etcd Commands Reference](references/etcd_commands.md)
- [etcd Safety Guidelines](references/safety_guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/fpbear/skills/etcd-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and structured operation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current values, proposed new values, deletion backups, endpoint details, and risk notes for user review.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
