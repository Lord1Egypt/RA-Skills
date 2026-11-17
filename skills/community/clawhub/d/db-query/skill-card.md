## Description:

MYSQL QUERY helps agents execute SQL against configured MySQL databases and manage optional SSH tunnels for databases that are not directly reachable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenixp](https://clawhub.ai/user/zenixp)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to list configured MySQL databases and run SQL queries, including through short-lived SSH tunnels when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unrestricted SQL, so an agent using privileged credentials could read, modify, or delete sensitive database data.

Mitigation: Use read-only database accounts by default, review queries before execution, and reserve production write credentials for explicitly approved workflows.

Risk: The security evidence reports a credential-handling bug that may send a database password to an SSH server.

Mitigation: Do not use password-based SSH with this version unless the credential-confusion bug is fixed; prefer key-based SSH or separate SSH_PASSWORD_* values after review.

Risk: Database or SSH secrets stored in the JSON config file may be exposed through local file access or loose permissions.

Mitigation: Store secrets in environment variables where possible, or restrict the config file to owner-only permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zenixp/skills/db-query)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text and markdown guidance with shell command examples; query results are emitted as mysql client text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local JSON database configuration, mysql client, and optional ssh or sshpass support.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
