## Description:

Seamlessly migrate your agent's configuration and memory to a new machine using TiDB Zero.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilyjazz](https://clawhub.ai/user/lilyjazz)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to pack an agent workspace, configuration, and memory into a TiDB-backed transfer payload, then restore that state on another machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transfer broad workspace data to TiDB, including files the ignore list does not exclude.

Mitigation: Review the workspace before packing, avoid sensitive workspaces, and use a trusted database configuration when possible.

Risk: The DSN functions as a restore credential for the transferred workspace data.

Mitigation: Protect the DSN like a password and delete or rotate the database after restoration.

Risk: Restore writes files into the current directory and can overwrite local files.

Mitigation: Restore only into an isolated or backed-up directory until the restored contents have been reviewed.

## Reference(s):

- [Agent Teleport Skill Page](https://clawhub.ai/lilyjazz/skills/agent-teleport)
- [Publisher Profile](https://clawhub.ai/user/lilyjazz)
- [TiDB Zero API endpoint](https://zero.tidbapi.com/v1alpha1/instances)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [JSON status output with restore instructions and local filesystem changes during restore]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, curl, pymysql, and TiDB connection settings or automatic TiDB Zero provisioning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
